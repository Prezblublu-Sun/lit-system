"""scripts/canonical_doi.py - read-only DOI normalization + dedup analyzer.

A what-if analyzer for the lit-system metadata corpus. Walks metadata/P*.json,
normalizes each DOI string, groups papers by normalized DOI to surface
duplicates, and cross-references the findings against decisions/doi_aliases.json
(the hand-audited alias map).

Does NOT modify any metadata file, does NOT modify doi_aliases.json, does NOT
call the hot-path ingest pipeline. Safe to run while overnight ingest is alive.

Usage:
    python scripts/canonical_doi.py                          # JSON to stdout
    python scripts/canonical_doi.py --format markdown        # markdown to stdout
    python scripts/canonical_doi.py --apply-aliases          # show remaining
                                                              # collisions after
                                                              # applying alias map
    python scripts/canonical_doi.py --output PATH            # write to file

================================================================================
JSON OUTPUT SCHEMA -- v1
================================================================================

Top-level object:
    schema_version       str   "v1"
    tool                 str   "canonical_doi"
    timestamp            str   ISO 8601 Zulu, second precision
    mode                 str   "raw" | "aliases_applied"
    inputs               dict  {metadata_dir, metadata_files,
                                 aliases_file, aliases_count}
    normalization_rules  list[str]  ordered list of rule names applied
    summary              dict  counts (see Summary keys below)
    papers               list  per-paper records (one per file)
    collisions           list  groups where >1 paper shares a normalized DOI
    alias_audit          list  per alias-map entry, status + detail

Summary keys:
    papers_total, papers_with_doi, papers_without_doi,
    unique_normalized_dois,
    collision_groups, collisions_consistent_with_aliases,
    collisions_new, collisions_partial, collisions_remaining_after_aliases,
    alias_entries_total, alias_entries_corroborated, alias_entries_null_side,
    alias_entries_conflict,
    extraction_method_counts

Per-paper record:
    paper_id              str
    metadata_file         str   path relative to repo root
    raw_doi               str | null
    normalized_doi        str | null
    doi_method            str   from source_block.doi._meta.method
    normalization_applied list[str]

Collision group record:
    normalized_doi        str
    paper_ids             list[str]   sorted
    raw_dois              dict[paper_id -> raw_doi]
    alias_map_status      "consistent" | "new" | "partial"
    alias_map_canonical   str | null    set when status == consistent
    suggested_action      str

Alias audit record:
    alias                 str
    canonical             str
    alias_doi             str | null    normalized
    canonical_doi         str | null    normalized
    status                "corroborated" | "null_side" | "conflict"
    detail                str
    suggested_action      str | null    set when status == conflict
================================================================================
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
from collections import Counter
from dataclasses import dataclass, asdict
from typing import Optional


ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_METADATA_DIR = ROOT / "metadata"
DEFAULT_ALIASES_PATH = ROOT / "decisions" / "doi_aliases.json"

SCHEMA_VERSION = "v1"


# ============================================================================
# Normalization
# ============================================================================

_DOI_ORG_PREFIX_RE = re.compile(r"^https?://(?:dx\.)?doi\.org/", re.IGNORECASE)
_DOI_WORD_PREFIX_RE = re.compile(r"^doi[:\s]+", re.IGNORECASE)
_TRAILING_PUNCT_RE = re.compile(r"[.,;\)\]]+$")

NORMALIZATION_RULES = [
    "strip_whitespace",
    "strip_doi_org_prefix",
    "strip_doi_word_prefix",
    "strip_trailing_punct",
    "lowercase",
]


def normalize_doi(raw: Optional[str]) -> tuple[Optional[str], list[str]]:
    """Normalize a raw DOI string. Returns (normalized_or_None, rules_applied)."""
    if raw is None or not isinstance(raw, str):
        return None, []
    applied: list[str] = []

    s = raw.strip()
    if s != raw:
        applied.append("strip_whitespace")
    if not s:
        return None, applied

    s2 = _DOI_ORG_PREFIX_RE.sub("", s)
    if s2 != s:
        applied.append("strip_doi_org_prefix")
        s = s2

    s2 = _DOI_WORD_PREFIX_RE.sub("", s)
    if s2 != s:
        applied.append("strip_doi_word_prefix")
        s = s2

    s2 = _TRAILING_PUNCT_RE.sub("", s)
    if s2 != s:
        applied.append("strip_trailing_punct")
        s = s2

    lower = s.lower()
    if lower != s:
        applied.append("lowercase")
        s = lower

    return (s if s else None), applied


# ============================================================================
# Metadata loading
# ============================================================================

@dataclass
class PaperRecord:
    paper_id: str
    metadata_file: str
    raw_doi: Optional[str]
    normalized_doi: Optional[str]
    doi_method: str
    normalization_applied: list[str]


def _extract_doi_field(blob: dict) -> tuple[Optional[str], str]:
    """Return (raw_doi, method). Handles both dict and string shapes."""
    sb = blob.get("source_block") or {}
    field = sb.get("doi")
    if isinstance(field, dict):
        value = field.get("value")
        meta = field.get("_meta") or {}
        method = meta.get("method") or "unknown"
        return (value if isinstance(value, str) else None), method
    if isinstance(field, str):
        return field, "string_shape_legacy"
    return None, "no_doi_field"


def load_papers(metadata_dir: pathlib.Path,
                repo_root: pathlib.Path) -> list[PaperRecord]:
    records: list[PaperRecord] = []
    for path in sorted(metadata_dir.glob("P*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        paper_id = data.get("_paper_id") or path.stem
        raw, method = _extract_doi_field(data)
        normalized, applied = normalize_doi(raw)
        try:
            rel = str(path.relative_to(repo_root))
        except ValueError:
            rel = str(path)
        records.append(PaperRecord(
            paper_id=paper_id, metadata_file=rel,
            raw_doi=raw, normalized_doi=normalized,
            doi_method=method, normalization_applied=applied,
        ))
    return records


def load_aliases(aliases_path: pathlib.Path) -> dict:
    """Return the parsed aliases JSON, or an empty stub if missing."""
    if not aliases_path.exists():
        return {"aliases": {}, "canonical_notes": {}, "pending_verification": []}
    try:
        return json.loads(aliases_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"aliases": {}, "canonical_notes": {}, "pending_verification": []}


# ============================================================================
# Collision detection + classification
# ============================================================================

def _paper_id_sort_key(pid: str):
    """Sort P-IDs by their integer suffix when present."""
    m = re.match(r"^P(\d+)$", pid)
    return (0, int(m.group(1))) if m else (1, pid)


def _suggest_collision_action(paper_ids: list[str], status: str,
                              aliases: dict) -> str:
    pids_disp = ", ".join(paper_ids)
    if status == "consistent":
        return f"already documented in doi_aliases.json"
    if status == "new":
        return (f"PDF compare {pids_disp}; if same paper, "
                f"add to doi_aliases.json")
    # partial
    in_map = [p for p in paper_ids if p in aliases or p in aliases.values()]
    return (f"PDF compare {pids_disp}; alias map already mentions "
            f"{', '.join(in_map)} - reconcile with this collision")


def find_collisions(papers: list[PaperRecord], aliases: dict) -> list[dict]:
    """Group papers by normalized DOI; return collision records (groups >= 2)."""
    alias_map: dict[str, str] = aliases.get("aliases") or {}
    alias_keys = set(alias_map.keys())
    alias_vals = set(alias_map.values())
    known_in_map = alias_keys | alias_vals

    by_doi: dict[str, list[PaperRecord]] = {}
    for r in papers:
        if r.normalized_doi is None:
            continue
        by_doi.setdefault(r.normalized_doi, []).append(r)

    collisions: list[dict] = []
    for ndoi, group in by_doi.items():
        if len(group) < 2:
            continue
        sorted_pids = sorted([r.paper_id for r in group], key=_paper_id_sort_key)
        # Status:
        canonical_set = {alias_map.get(p, p) for p in sorted_pids}
        canonical = None
        if len(canonical_set) == 1:
            status = "consistent"
            canonical = next(iter(canonical_set))
        elif any(p in known_in_map for p in sorted_pids):
            status = "partial"
        else:
            status = "new"
        raw_dois = {r.paper_id: r.raw_doi for r in group}
        collisions.append({
            "normalized_doi": ndoi,
            "paper_ids": sorted_pids,
            "raw_dois": raw_dois,
            "alias_map_status": status,
            "alias_map_canonical": canonical,
            "suggested_action": _suggest_collision_action(
                sorted_pids, status, alias_map),
        })
    collisions.sort(key=lambda c: (
        {"new": 0, "partial": 1, "consistent": 2}.get(c["alias_map_status"], 3),
        c["normalized_doi"],
    ))
    return collisions


# ============================================================================
# Alias audit
# ============================================================================

def audit_aliases(papers: list[PaperRecord], aliases: dict,
                  collisions: list[dict]) -> list[dict]:
    """For each alias entry, compare it to DOI evidence and report status."""
    alias_map: dict[str, str] = aliases.get("aliases") or {}
    doi_by_pid: dict[str, Optional[str]] = {r.paper_id: r.normalized_doi
                                            for r in papers}
    collision_lookup: dict[str, dict] = {}
    for c in collisions:
        for pid in c["paper_ids"]:
            collision_lookup[pid] = c

    audit: list[dict] = []
    for alias_pid, canonical_pid in alias_map.items():
        a_doi = doi_by_pid.get(alias_pid)
        c_doi = doi_by_pid.get(canonical_pid)
        extra_finding: Optional[str] = None
        suggested: Optional[str] = None

        if a_doi and c_doi:
            if a_doi == c_doi:
                status = "corroborated"
                detail = "alias and canonical share the same normalized DOI"
            else:
                status = "conflict"
                detail = (f"DOIs differ: alias_doi={a_doi}, "
                          f"canonical_doi={c_doi}")
                suggested = (f"human investigation: PDF compare "
                             f"{alias_pid}/{canonical_pid} to determine "
                             f"correct DOI")
        else:
            status = "null_side"
            detail = (f"alias_doi={a_doi or 'null'}, "
                      f"canonical_doi={c_doi or 'null'}")

        col = collision_lookup.get(alias_pid)
        if col and col["alias_map_status"] in ("new", "partial"):
            others = [p for p in col["paper_ids"] if p != alias_pid]
            if canonical_pid not in others:
                extra_finding = (f"alias {alias_pid} collides by DOI with "
                                 f"{', '.join(others)}, not {canonical_pid}")
                if status == "null_side":
                    status = "conflict"
                    suggested = (f"human investigation: PDF compare "
                                 f"{alias_pid}/{canonical_pid} to determine "
                                 f"correct DOI (DOI evidence points elsewhere)")

        entry = {
            "alias": alias_pid,
            "canonical": canonical_pid,
            "alias_doi": a_doi,
            "canonical_doi": c_doi,
            "status": status,
            "detail": detail,
        }
        if extra_finding:
            entry["extra_finding"] = extra_finding
        if suggested:
            entry["suggested_action"] = suggested
        audit.append(entry)
    return audit


# ============================================================================
# Apply-aliases mode: compute remaining collisions after alias map applied
# ============================================================================

def apply_aliases_to_collisions(collisions: list[dict],
                                aliases: dict) -> tuple[list[dict], int]:
    """Return (remaining_collisions, resolved_count).

    A collision is "resolved" if all its paper_ids collapse to one canonical
    paper_id under the alias map; otherwise it "remains".
    """
    alias_map: dict[str, str] = aliases.get("aliases") or {}
    resolved = 0
    remaining: list[dict] = []
    for c in collisions:
        canonicals = {alias_map.get(p, p) for p in c["paper_ids"]}
        if len(canonicals) <= 1:
            resolved += 1
            continue
        entry = dict(c)
        entry["paper_ids_after_aliases"] = sorted(canonicals,
                                                  key=_paper_id_sort_key)
        remaining.append(entry)
    return remaining, resolved


# ============================================================================
# Report assembly
# ============================================================================

def build_report(papers: list[PaperRecord], aliases: dict,
                 metadata_dir: pathlib.Path, aliases_path: pathlib.Path,
                 repo_root: pathlib.Path,
                 apply_aliases: bool) -> dict:
    collisions = find_collisions(papers, aliases)
    alias_audit = audit_aliases(papers, aliases, collisions)
    alias_map = aliases.get("aliases") or {}

    method_counts = Counter(r.doi_method for r in papers)
    n_with_doi = sum(1 for r in papers if r.normalized_doi is not None)

    consistent = sum(1 for c in collisions if c["alias_map_status"] == "consistent")
    new = sum(1 for c in collisions if c["alias_map_status"] == "new")
    partial = sum(1 for c in collisions if c["alias_map_status"] == "partial")

    corroborated = sum(1 for a in alias_audit if a["status"] == "corroborated")
    null_side = sum(1 for a in alias_audit if a["status"] == "null_side")
    conflict = sum(1 for a in alias_audit if a["status"] == "conflict")

    if apply_aliases:
        remaining_collisions, resolved_count = apply_aliases_to_collisions(
            collisions, aliases)
        emitted_collisions = remaining_collisions
        mode = "aliases_applied"
        remaining_count: Optional[int] = len(remaining_collisions)
    else:
        emitted_collisions = collisions
        mode = "raw"
        remaining_count = None

    try:
        md_rel = str(metadata_dir.relative_to(repo_root))
    except ValueError:
        md_rel = str(metadata_dir)
    try:
        al_rel = str(aliases_path.relative_to(repo_root))
    except ValueError:
        al_rel = str(aliases_path)

    summary = {
        "papers_total": len(papers),
        "papers_with_doi": n_with_doi,
        "papers_without_doi": len(papers) - n_with_doi,
        "unique_normalized_dois": len({r.normalized_doi for r in papers
                                       if r.normalized_doi}),
        "collision_groups": len(collisions),
        "collisions_consistent_with_aliases": consistent,
        "collisions_new": new,
        "collisions_partial": partial,
        "alias_entries_total": len(alias_map),
        "alias_entries_corroborated": corroborated,
        "alias_entries_null_side": null_side,
        "alias_entries_conflict": conflict,
        "extraction_method_counts": dict(method_counts.most_common()),
    }
    if remaining_count is not None:
        summary["collisions_remaining_after_aliases"] = remaining_count

    return {
        "schema_version": SCHEMA_VERSION,
        "tool": "canonical_doi",
        "timestamp": dt.datetime.now(dt.timezone.utc)
                       .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": mode,
        "inputs": {
            "metadata_dir": md_rel,
            "metadata_files": len(papers),
            "aliases_file": al_rel,
            "aliases_count": len(alias_map),
        },
        "normalization_rules": NORMALIZATION_RULES,
        "summary": summary,
        "papers": [asdict(r) for r in papers],
        "collisions": emitted_collisions,
        "alias_audit": alias_audit,
    }


# ============================================================================
# Markdown rendering
# ============================================================================

def _md_row(*cells: str) -> str:
    return "| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |"


def render_markdown(report: dict) -> str:
    lines: list[str] = []
    lines.append("# canonical_doi.py - DOI canonicalization audit")
    lines.append("")
    inputs = report["inputs"]
    lines.append(f"Generated {report['timestamp']}. Mode: `{report['mode']}`.")
    lines.append(f"Source: `{inputs['metadata_dir']}` "
                 f"({inputs['metadata_files']} papers), "
                 f"`{inputs['aliases_file']}` "
                 f"({inputs['aliases_count']} aliases).")
    lines.append("")

    # Findings section (always first, even when clean)
    non_consistent = [c for c in report["collisions"]
                      if c.get("alias_map_status") in ("new", "partial")]
    conflicts = [a for a in report["alias_audit"]
                 if a.get("status") == "conflict"]

    lines.append("## Findings requiring action")
    lines.append("")
    if not non_consistent and not conflicts:
        lines.append("**None.** All DOI collisions are documented in "
                     "`doi_aliases.json`, and every alias-map entry is either "
                     "corroborated by DOI evidence or supported by title/"
                     "content audit (null-side).")
        lines.append("")
    else:
        if non_consistent:
            lines.append(f"### {len(non_consistent)} DOI collision(s) not "
                         f"consistent with `doi_aliases.json`")
            lines.append("")
            lines.append(_md_row("Normalized DOI", "Paper IDs",
                                 "Status", "Suggested action"))
            lines.append(_md_row("---", "---", "---", "---"))
            for c in non_consistent:
                lines.append(_md_row(
                    f"`{c['normalized_doi']}`",
                    ", ".join(c["paper_ids"]),
                    c["alias_map_status"],
                    c["suggested_action"],
                ))
            lines.append("")
        if conflicts:
            lines.append(f"### {len(conflicts)} alias-map entry contradicted "
                         f"by DOI evidence")
            lines.append("")
            lines.append(_md_row("Alias entry", "Alias DOI", "Canonical DOI",
                                 "Detail", "Suggested action"))
            lines.append(_md_row("---", "---", "---", "---", "---"))
            for a in conflicts:
                detail = a.get("extra_finding") or a.get("detail", "")
                lines.append(_md_row(
                    f"{a['alias']} -> {a['canonical']}",
                    f"`{a.get('alias_doi') or 'null'}`",
                    f"`{a.get('canonical_doi') or 'null'}`",
                    detail,
                    a.get("suggested_action", ""),
                ))
            lines.append("")

    # Summary
    s = report["summary"]
    lines.append("## Summary")
    lines.append("")
    lines.append(_md_row("Metric", "Value"))
    lines.append(_md_row("---", "---"))
    lines.append(_md_row("Papers total", str(s["papers_total"])))
    lines.append(_md_row("Papers with DOI", str(s["papers_with_doi"])))
    lines.append(_md_row("Papers without DOI", str(s["papers_without_doi"])))
    lines.append(_md_row("Unique normalized DOIs",
                         str(s["unique_normalized_dois"])))
    lines.append(_md_row("Collision groups", str(s["collision_groups"])))
    lines.append(_md_row("  consistent with aliases",
                         str(s["collisions_consistent_with_aliases"])))
    lines.append(_md_row("  new (neither in alias map)",
                         str(s["collisions_new"])))
    lines.append(_md_row("  partial (one side in alias map)",
                         str(s["collisions_partial"])))
    if "collisions_remaining_after_aliases" in s:
        lines.append(_md_row("Collisions remaining after --apply-aliases",
                             str(s["collisions_remaining_after_aliases"])))
    lines.append(_md_row("Alias entries", str(s["alias_entries_total"])))
    lines.append(_md_row("  corroborated by DOI",
                         str(s["alias_entries_corroborated"])))
    lines.append(_md_row("  null-side (title/content audit only)",
                         str(s["alias_entries_null_side"])))
    lines.append(_md_row("  conflict (DOI evidence disagrees)",
                         str(s["alias_entries_conflict"])))
    lines.append("")
    lines.append("Extraction method counts: " + ", ".join(
        f"`{k}`={v}" for k, v in s["extraction_method_counts"].items()))
    lines.append("")

    # Collision groups (full table)
    lines.append("## Collision groups")
    lines.append("")
    if not report["collisions"]:
        lines.append("_No collisions in current mode._")
        lines.append("")
    else:
        lines.append(_md_row("Normalized DOI", "Paper IDs",
                             "Status", "Suggested action"))
        lines.append(_md_row("---", "---", "---", "---"))
        for c in report["collisions"]:
            lines.append(_md_row(
                f"`{c['normalized_doi']}`",
                ", ".join(c["paper_ids"]),
                c["alias_map_status"],
                c["suggested_action"],
            ))
        lines.append("")

    # Alias audit (full table)
    lines.append("## Alias audit")
    lines.append("")
    if not report["alias_audit"]:
        lines.append("_No alias entries to audit._")
        lines.append("")
    else:
        lines.append(_md_row("Alias entry", "Alias DOI", "Canonical DOI",
                             "Status", "Detail"))
        lines.append(_md_row("---", "---", "---", "---", "---"))
        for a in report["alias_audit"]:
            detail = a.get("extra_finding") or a.get("detail", "")
            lines.append(_md_row(
                f"{a['alias']} -> {a['canonical']}",
                f"`{a.get('alias_doi') or 'null'}`",
                f"`{a.get('canonical_doi') or 'null'}`",
                a["status"],
                detail,
            ))
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# CLI
# ============================================================================

def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only DOI canonicalization + dedup analyzer "
                    "for lit-system metadata. Produces a report; never "
                    "modifies metadata or doi_aliases.json.")
    parser.add_argument("--metadata-dir", type=pathlib.Path,
                        default=DEFAULT_METADATA_DIR,
                        help="Directory containing P*.json files "
                             "(default: metadata/).")
    parser.add_argument("--aliases", type=pathlib.Path,
                        default=DEFAULT_ALIASES_PATH,
                        help="Alias map JSON (default: "
                             "decisions/doi_aliases.json).")
    parser.add_argument("--output", type=pathlib.Path, default=None,
                        help="Write report to this path. Default: stdout.")
    parser.add_argument("--format", choices=("json", "markdown"),
                        default="json",
                        help="Output format (default: json).")
    parser.add_argument("--apply-aliases", action="store_true",
                        help="Apply doi_aliases.json before grouping; "
                             "report only the collisions that remain.")
    parser.add_argument("--repo-root", type=pathlib.Path,
                        default=ROOT,
                        help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    papers = load_papers(args.metadata_dir, args.repo_root.resolve())
    aliases = load_aliases(args.aliases)
    report = build_report(
        papers=papers, aliases=aliases,
        metadata_dir=args.metadata_dir, aliases_path=args.aliases,
        repo_root=args.repo_root.resolve(),
        apply_aliases=args.apply_aliases,
    )

    if args.format == "json":
        out = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        out = render_markdown(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
