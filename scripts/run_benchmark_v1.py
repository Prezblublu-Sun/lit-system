#!/usr/bin/env python3
"""
run_benchmark_v1.py — SOP_v2 baseline benchmark for 5 golden papers.

Tests 6 automatic dimensions on each paper's metadata:
  1. title presence and length
  2. DOI presence and format
  3. filler rate (LLM conversational prefixes)
  4. fake page rate ("(page X)" / "(pages X-Y)" patterns)
  5. markdown pollution (**bold**, ###, numbered lists at line start)
  6. prompt echo (LLM repeating prompt phrasing)
  7. field completeness (5 SOP fields non-null and non-empty)

Output: results/benchmark_sop_v2_baseline.json
        + human-readable summary in stdout

Usage:
  python scripts/run_benchmark_v1.py
"""

import json
import re
from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "lit-system"
METADATA_DIR = ROOT / "metadata"
RESULTS_DIR = ROOT / "results"
GOLDEN_PAPERS = ["P1", "P5", "P44", "P77", "P117"]

# SOP fields we benchmark (path within metadata JSON).
# Key rename per ADR-0014: L3_personal -> L3_outline (block + field name unchanged).
# L4 is checked separately below (different cleanliness rules + label parsing).
SOP_FIELDS = {
    "L1_background":  ("factual", "sop_l1_background_raw"),
    "L1_methods":     ("factual", "methods_raw"),
    "L2_problem":     ("interpretive", "core_problem_raw"),
    "L2_scoring":     ("interpretive", "scoring_10_dim_local"),
    "L3_outline":     ("personal_relevance", "sop_l3_raw"),
}

# L4 paths (factual.l4_raw + factual.domain_classification per ADR-0014)
L4_RAW_PATH    = ("factual", "l4_raw")
L4_PARSED_PATH = ("factual", "domain_classification")

VALID_DOMAIN_LABELS = {
    "bioprinting", "hip_implant", "fea_surrogate", "additive_manufacturing",
    "tissue_engineering", "biomechanics", "machine_learning_general",
    "other_medical", "other_engineering", "out_of_scope",
}

# === Detection patterns ===

FILLER_PATTERNS = [
    r"^Based on the (provided|given) (text|content|paper|abstract|context)",
    r"^Certainly[!.,]",
    r"^Sure[!.,]",
    r"^Here (is|are) the (extracted|requested|relevant)",
    r"^I('ll| will| have) (analyze|provide|extract|summarize)",
    r"^According to (the|this) paper",
    r"^The (provided|given) (text|content|paper) (discusses|describes|presents)",
]

FAKE_PAGE_PATTERNS = [
    r"\(page \d+",
    r"\(pages \d+",
    r"\(p\.\s*\d+",
    r"on page \d+",
    r"pages? \d+[-\u2013]\d+",
]

MARKDOWN_PATTERNS = [
    r"\*\*[^*]+\*\*",         # **bold**
    r"^#+\s",                  # ### headers
    r"^\d+\.\s\*\*",           # 1. **Bold**
    r"^[A-Z]\)\s\*\*",         # A) **Bold**
    r"^\*\s",                  # bullet *
    r"^-\s\*\*",               # - **bold**
]

PROMPT_ECHO_PATTERNS = [
    r"This paper best supports",
    r"The most central problem (addressed|identified) by this paper",
    r"The main (methods?|approaches?|techniques?) used (in this paper )?(are|is)",
    r"The (provided|given) text discusses",
]

# === Detection functions ===

def detect_filler(text: str) -> dict:
    """Check first 200 chars for filler patterns."""
    head = text[:200]
    matches = []
    for pat in FILLER_PATTERNS:
        if re.search(pat, head, re.IGNORECASE | re.MULTILINE):
            matches.append(pat)
    return {"present": bool(matches), "matched_patterns": matches}

def detect_fake_page(text: str) -> dict:
    """Count page references in text."""
    counts = []
    for pat in FAKE_PAGE_PATTERNS:
        c = len(re.findall(pat, text, re.IGNORECASE))
        if c > 0:
            counts.append((pat, c))
    total = sum(c for _, c in counts)
    return {"present": total > 0, "count": total, "matched_patterns": counts}

def detect_markdown(text: str) -> dict:
    """Count markdown formatting markers."""
    counts = []
    for pat in MARKDOWN_PATTERNS:
        c = len(re.findall(pat, text, re.MULTILINE))
        if c > 0:
            counts.append((pat, c))
    total = sum(c for _, c in counts)
    return {"present": total > 0, "count": total, "matched_patterns": counts}

def detect_prompt_echo(text: str) -> dict:
    """Check if LLM is parroting prompt phrasing."""
    matches = []
    for pat in PROMPT_ECHO_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            matches.append(pat)
    return {"present": bool(matches), "matched_patterns": matches}

def check_l4_cleanliness(raw: str) -> dict:
    """ADR-0014 L4 must be exactly two non-empty lines:
        primary_domain: <label>. <justification>.
        secondary_domains: <labels>. <reason>.   (or 'none.')
    Anything else (extra lines, markdown, missing prefix) is a cleanliness failure.
    """
    issues = []
    if not raw or not raw.strip():
        return {"clean": False, "issues": ["empty_l4_output"], "n_nonempty_lines": 0}

    lines = [l.strip() for l in raw.strip().splitlines() if l.strip()]
    n = len(lines)
    if n != 2:
        issues.append(f"expected_2_lines_got_{n}")

    # Line 1 must start with primary_domain:
    if n >= 1 and not lines[0].lower().startswith("primary_domain:"):
        issues.append("line1_missing_primary_domain_prefix")
    # Line 2 must start with secondary_domains:
    if n >= 2 and not lines[1].lower().startswith("secondary_domains:"):
        issues.append("line2_missing_secondary_domains_prefix")

    # No markdown anywhere
    md_count = 0
    for pat in MARKDOWN_PATTERNS:
        md_count += len(re.findall(pat, raw, re.MULTILINE))
    if md_count > 0:
        issues.append(f"markdown_markers:{md_count}")

    return {"clean": not issues, "issues": issues, "n_nonempty_lines": n}


def check_field_completeness(metadata: dict) -> dict:
    """Verify all 5 SOP fields are present and non-empty.

    ADR-0017: L3 may be deliberately skipped (no outline provided). Detect via
    interpretive.outline_match_status == 'skipped_no_outline' and report L3 as
    a clean skipped state rather than as a missing/failed field.
    """
    l3_skipped = False
    try:
        if metadata["interpretive"]["outline_match_status"]["value"] == "skipped_no_outline":
            l3_skipped = True
    except (KeyError, TypeError):
        pass

    status = {}
    for label, (block, key) in SOP_FIELDS.items():
        if label == "L3_outline" and l3_skipped:
            status[label] = {
                "present": False,
                "length": 0,
                "skipped_no_outline": True,
            }
            continue
        try:
            val = metadata[block][key]["value"]
            status[label] = {
                "present": val is not None,
                "length": len(val) if val else 0,
                "value_preview": (val[:80] + "...") if val and len(val) > 80 else val,
            }
        except (KeyError, TypeError) as e:
            status[label] = {"present": False, "error": str(e)}
    return status

# === Per-paper benchmark ===

def benchmark_paper(paper_id: str) -> dict:
    """Run all checks on one paper's metadata."""
    metadata_path = METADATA_DIR / f"{paper_id}.json"
    if not metadata_path.exists():
        return {"paper_id": paper_id, "error": "metadata not found"}
    
    metadata = json.loads(metadata_path.read_text())
    
    result = {
        "paper_id": paper_id,
        "doc_id": metadata.get("id_block", {}).get("doc_id"),
        "title_extracted": metadata.get("source_block", {}).get("title", {}).get("value"),
        "doi_extracted": None,
        "field_completeness": check_field_completeness(metadata),
        "filler": {},
        "fake_page": {},
        "markdown": {},
        "prompt_echo": {},
        "l4": {"present": False, "cleanliness": None, "primary": None, "secondary": []},
    }
    
    # DOI may be in source_block or factual
    doi_field = metadata.get("source_block", {}).get("doi")
    if isinstance(doi_field, dict):
        result["doi_extracted"] = doi_field.get("value")
    elif isinstance(doi_field, str):
        result["doi_extracted"] = doi_field
    
    # Run detection on each SOP field
    for label, (block, key) in SOP_FIELDS.items():
        try:
            text = metadata[block][key]["value"]
            if text is None:
                continue
            result["filler"][label] = detect_filler(text)
            result["fake_page"][label] = detect_fake_page(text)
            result["markdown"][label] = detect_markdown(text)
            result["prompt_echo"][label] = detect_prompt_echo(text)
        except (KeyError, TypeError):
            continue

    # === L4 domain classification (ADR-0014) ===
    try:
        l4_raw = metadata[L4_RAW_PATH[0]][L4_RAW_PATH[1]]["value"]
    except (KeyError, TypeError):
        l4_raw = None
    try:
        l4_parsed = metadata[L4_PARSED_PATH[0]][L4_PARSED_PATH[1]]["value"]
    except (KeyError, TypeError):
        l4_parsed = None

    if l4_raw:
        result["l4"]["present"]     = True
        result["l4"]["cleanliness"] = check_l4_cleanliness(l4_raw)
    if isinstance(l4_parsed, dict):
        result["l4"]["primary"]   = l4_parsed.get("primary")
        result["l4"]["secondary"] = l4_parsed.get("secondary", []) or []

    return result

# === Aggregate ===

def aggregate(results: list[dict]) -> dict:
    """Cross-paper summary stats."""
    from collections import Counter
    n = len(results)
    summary = {
        "n_papers": n,
        "title_present": sum(1 for r in results if r.get("title_extracted")),
        "doi_present": sum(1 for r in results if r.get("doi_extracted")),
        "filler_papers": 0,
        "fake_page_papers": 0,
        "markdown_papers": 0,
        "prompt_echo_papers": 0,
        "total_fake_page_count": 0,
        "total_markdown_count": 0,
        "per_field_filler_rate": {},
        "per_field_fake_page_rate": {},
        "per_field_markdown_rate": {},
        # === L4 (ADR-0014) ===
        "l4_present_papers": 0,
        "l4_clean_papers": 0,
        "l4_issue_counter": {},
        "primary_domain_distribution": {},
        "secondary_domain_distribution": {},
        "primary_domain_unknown": 0,
    }
    _primary_ctr   = Counter()
    _secondary_ctr = Counter()
    _issue_ctr     = Counter()
    
    for label in SOP_FIELDS:
        summary["per_field_filler_rate"][label] = 0
        summary["per_field_fake_page_rate"][label] = 0
        summary["per_field_markdown_rate"][label] = 0
    
    for r in results:
        # Any-field flags
        if any(r["filler"].get(l, {}).get("present") for l in SOP_FIELDS):
            summary["filler_papers"] += 1
        if any(r["fake_page"].get(l, {}).get("present") for l in SOP_FIELDS):
            summary["fake_page_papers"] += 1
        if any(r["markdown"].get(l, {}).get("present") for l in SOP_FIELDS):
            summary["markdown_papers"] += 1
        if any(r["prompt_echo"].get(l, {}).get("present") for l in SOP_FIELDS):
            summary["prompt_echo_papers"] += 1
        
        # Total counts
        for l in SOP_FIELDS:
            summary["total_fake_page_count"] += r["fake_page"].get(l, {}).get("count", 0)
            summary["total_markdown_count"] += r["markdown"].get(l, {}).get("count", 0)
            if r["filler"].get(l, {}).get("present"):
                summary["per_field_filler_rate"][l] += 1
            if r["fake_page"].get(l, {}).get("present"):
                summary["per_field_fake_page_rate"][l] += 1
            if r["markdown"].get(l, {}).get("present"):
                summary["per_field_markdown_rate"][l] += 1
    
    # Convert to rates
    for l in SOP_FIELDS:
        summary["per_field_filler_rate"][l] = f"{summary['per_field_filler_rate'][l]}/{n}"
        summary["per_field_fake_page_rate"][l] = f"{summary['per_field_fake_page_rate'][l]}/{n}"
        summary["per_field_markdown_rate"][l] = f"{summary['per_field_markdown_rate'][l]}/{n}"

    summary["filler_rate"]      = f"{summary['filler_papers']}/{n}"
    summary["fake_page_rate"]   = f"{summary['fake_page_papers']}/{n}"
    summary["markdown_rate"]    = f"{summary['markdown_papers']}/{n}"
    summary["prompt_echo_rate"] = f"{summary['prompt_echo_papers']}/{n}"

    # === L4 aggregation ===
    for r in results:
        l4 = r.get("l4", {}) or {}
        if l4.get("present"):
            summary["l4_present_papers"] += 1
            cleanliness = l4.get("cleanliness") or {}
            if cleanliness.get("clean"):
                summary["l4_clean_papers"] += 1
            for issue in cleanliness.get("issues", []) or []:
                # Drop the count suffix so "markdown_markers:3" and ":7" aggregate together.
                _issue_ctr[issue.split(":")[0]] += 1
            primary = l4.get("primary")
            if primary:
                _primary_ctr[primary] += 1
                if primary not in VALID_DOMAIN_LABELS:
                    summary["primary_domain_unknown"] += 1
            for sec in l4.get("secondary", []) or []:
                _secondary_ctr[sec] += 1

    summary["l4_present_rate"] = f"{summary['l4_present_papers']}/{n}"
    summary["l4_clean_rate"]   = f"{summary['l4_clean_papers']}/{n}"
    summary["l4_issue_counter"]              = dict(_issue_ctr)
    summary["primary_domain_distribution"]   = dict(_primary_ctr.most_common())
    summary["secondary_domain_distribution"] = dict(_secondary_ctr.most_common())

    return summary

# === Main ===

def main():
    print("=" * 70)
    print("BENCHMARK: SOP_v2 baseline (5 golden papers)")
    print("=" * 70)
    print()
    
    results = []
    for pid in GOLDEN_PAPERS:
        print(f"Running {pid}...", end=" ", flush=True)
        r = benchmark_paper(pid)
        results.append(r)
        if "error" in r:
            print(f"ERROR: {r['error']}")
        else:
            print("OK")
    
    print()
    print("=" * 70)
    print("PER-PAPER SUMMARY")
    print("=" * 70)
    for r in results:
        if "error" in r:
            continue
        print()
        print(f"--- {r['paper_id']} ---")
        print(f"  Title:  {r['title_extracted'][:80] if r['title_extracted'] else 'MISSING'}")
        print(f"  DOI:    {r['doi_extracted'] if r['doi_extracted'] else 'MISSING'}")
        
        for label in SOP_FIELDS:
            comp = r["field_completeness"].get(label, {})
            length = comp.get("length", 0)

            # ADR-0017: L3 skipped (no outline) is a clean state, not a failure.
            if comp.get("skipped_no_outline"):
                print(f"    {label:18s} [{length:5d} chars]  SKIPPED (no outline, ADR-0017)")
                continue

            problems = []
            if r["filler"].get(label, {}).get("present"):
                problems.append("FILLER")
            if r["fake_page"].get(label, {}).get("present"):
                n_pages = r["fake_page"][label]["count"]
                problems.append(f"FAKE_PAGE×{n_pages}")
            if r["markdown"].get(label, {}).get("present"):
                n_md = r["markdown"][label]["count"]
                problems.append(f"MARKDOWN×{n_md}")
            if r["prompt_echo"].get(label, {}).get("present"):
                problems.append("ECHO")

            problems_str = ", ".join(problems) if problems else "clean"
            print(f"    {label:18s} [{length:5d} chars]  {problems_str}")

        # L4 per-paper line (ADR-0014)
        l4 = r.get("l4", {}) or {}
        if l4.get("present"):
            cleanliness = l4.get("cleanliness") or {}
            status = "clean" if cleanliness.get("clean") else "issues=" + ",".join(cleanliness.get("issues", []) or [])
            sec_str = ",".join(l4.get("secondary") or []) or "none"
            print(f"    {'L4_domain':18s} primary={l4.get('primary')!r:30s}  secondary=[{sec_str}]  {status}")
        else:
            print(f"    {'L4_domain':18s} MISSING (no factual.l4_raw)")

    summary = aggregate([r for r in results if "error" not in r])
    
    print()
    print("=" * 70)
    print("OVERALL")
    print("=" * 70)
    print(f"Title present:      {summary['title_present']}/{summary['n_papers']}")
    print(f"DOI present:        {summary['doi_present']}/{summary['n_papers']}")
    print(f"Filler:             {summary['filler_rate']}  (any field)")
    print(f"Fake pages:         {summary['fake_page_rate']}  (any field, total occurrences: {summary['total_fake_page_count']})")
    print(f"Markdown pollution: {summary['markdown_rate']}  (any field, total: {summary['total_markdown_count']})")
    print(f"Prompt echo:        {summary['prompt_echo_rate']}  (any field)")
    print()
    print("Per-field fake_page rate:")
    for l, rate in summary["per_field_fake_page_rate"].items():
        print(f"  {l:18s} {rate}")

    # === L4 section (ADR-0014) ===
    print()
    print("L4 domain classification:")
    print(f"  Present:            {summary['l4_present_rate']}")
    print(f"  Clean (2-line, no markdown): {summary['l4_clean_rate']}")
    if summary["l4_issue_counter"]:
        print(f"  Issue breakdown: {summary['l4_issue_counter']}")
    print()
    print("Primary domain distribution:")
    if summary["primary_domain_distribution"]:
        for label, count in summary["primary_domain_distribution"].items():
            marker = "" if label in VALID_DOMAIN_LABELS else "  [UNKNOWN_LABEL]"
            print(f"  {label:32s} {count}{marker}")
    else:
        print("  (no L4 data)")
    if summary.get("primary_domain_unknown", 0) > 0:
        print(f"  Unknown-label papers: {summary['primary_domain_unknown']}")
    if summary["secondary_domain_distribution"]:
        print()
        print("Secondary domain distribution:")
        for label, count in summary["secondary_domain_distribution"].items():
            marker = "" if label in VALID_DOMAIN_LABELS else "  [UNKNOWN_LABEL]"
            print(f"  {label:32s} {count}{marker}")

    # Write JSON
    RESULTS_DIR.mkdir(exist_ok=True)
    output = {
        "benchmark_version": "v1",
        "sop_version": "v2",
        "schema_version": "v1",
        "ran_at": datetime.now().isoformat(),
        "papers": GOLDEN_PAPERS,
        "results": results,
        "summary": summary,
    }
    import sys
    out_name = sys.argv[1] if len(sys.argv) > 1 else "benchmark_sop_v2_baseline.json"
    out_path = RESULTS_DIR / out_name
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print()
    print(f"Saved: {out_path}")
    print(f"Size: {out_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
