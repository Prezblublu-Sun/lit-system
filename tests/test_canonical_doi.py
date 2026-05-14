"""Tests for scripts/canonical_doi.py.

Covers normalization rules, collision detection + classification, alias audit
(corroborated / null_side / conflict), apply-aliases mode, markdown rendering
(including the "Findings requiring action" lead section), and JSON schema
shape.

Run with:
    pytest tests/test_canonical_doi.py
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import canonical_doi as cd  # noqa: E402


# ============================================================================
# Helpers
# ============================================================================

def _make_metadata(paper_id: str, *, doi=None, method="regex") -> dict:
    """Build a synthetic metadata blob matching real schema."""
    if doi is None:
        doi_field = {
            "value": None,
            "_meta": {"method": "all_failed", "details": "no_match"},
        }
    else:
        doi_field = {
            "value": doi,
            "_meta": {"method": method, "details": "matched"},
        }
    return {
        "_paper_id": paper_id,
        "id_block": {"doc_id": "abc123" + paper_id, "content_hash": "x"},
        "source_block": {"doi": doi_field, "title": f"Title {paper_id}"},
    }


def _write_metadata(metadata_dir: pathlib.Path, paper_id: str,
                    *, doi=None, method="regex") -> pathlib.Path:
    metadata_dir.mkdir(parents=True, exist_ok=True)
    p = metadata_dir / f"{paper_id}.json"
    p.write_text(json.dumps(_make_metadata(paper_id, doi=doi, method=method)))
    return p


def _write_aliases(repo_root: pathlib.Path, mapping: dict) -> pathlib.Path:
    p = repo_root / "decisions" / "doi_aliases.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"aliases": mapping}))
    return p


def _run(tmp_path: pathlib.Path, *,
         apply_aliases: bool = False,
         format_: str = "json") -> tuple[int, dict | str]:
    metadata_dir = tmp_path / "metadata"
    aliases_path = tmp_path / "decisions" / "doi_aliases.json"
    out_path = tmp_path / "out.dat"
    argv = [
        "--metadata-dir", str(metadata_dir),
        "--aliases", str(aliases_path),
        "--output", str(out_path),
        "--format", format_,
        "--repo-root", str(tmp_path),
    ]
    if apply_aliases:
        argv.append("--apply-aliases")
    rc = cd.main(argv)
    raw = out_path.read_text()
    if format_ == "json":
        return rc, json.loads(raw)
    return rc, raw


@pytest.fixture
def tmp_repo(tmp_path: pathlib.Path) -> pathlib.Path:
    (tmp_path / "metadata").mkdir()
    (tmp_path / "decisions").mkdir()
    _write_aliases(tmp_path, {})
    return tmp_path


# ============================================================================
# Normalization
# ============================================================================

def test_normalize_none_returns_none():
    n, rules = cd.normalize_doi(None)
    assert n is None
    assert rules == []


def test_normalize_empty_string_returns_none():
    n, _ = cd.normalize_doi("")
    assert n is None


def test_normalize_whitespace_only_returns_none():
    n, rules = cd.normalize_doi("   ")
    assert n is None
    assert "strip_whitespace" in rules


def test_normalize_lowercases():
    n, rules = cd.normalize_doi("10.1109/JBHI.2017.2743526")
    assert n == "10.1109/jbhi.2017.2743526"
    assert "lowercase" in rules


def test_normalize_strips_doi_org_prefix():
    n, rules = cd.normalize_doi("https://doi.org/10.1234/abc")
    assert n == "10.1234/abc"
    assert "strip_doi_org_prefix" in rules


def test_normalize_strips_dx_doi_org_prefix():
    n, _ = cd.normalize_doi("http://dx.doi.org/10.1234/abc")
    assert n == "10.1234/abc"


def test_normalize_strips_doi_word_prefix():
    n, rules = cd.normalize_doi("DOI: 10.1234/abc")
    assert n == "10.1234/abc"
    assert "strip_doi_word_prefix" in rules


def test_normalize_strips_trailing_punct():
    n, rules = cd.normalize_doi("10.1234/abc.")
    assert n == "10.1234/abc"
    assert "strip_trailing_punct" in rules


def test_normalize_strips_multiple_trailing_punct():
    n, _ = cd.normalize_doi("10.1234/abc).,")
    assert n == "10.1234/abc"


def test_normalize_already_clean_no_rules_applied():
    n, rules = cd.normalize_doi("10.1234/abc")
    assert n == "10.1234/abc"
    assert rules == []


def test_normalize_combined_rules():
    n, rules = cd.normalize_doi("  https://doi.org/10.1234/AbC.  ")
    assert n == "10.1234/abc"
    assert set(rules) >= {"strip_whitespace", "strip_doi_org_prefix",
                          "strip_trailing_punct", "lowercase"}


# ============================================================================
# Loading
# ============================================================================

def test_load_papers_dict_shape(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/abc")
    _write_metadata(tmp_repo / "metadata", "P2", doi=None)
    rc, rep = _run(tmp_repo)
    assert rc == 0
    by_pid = {p["paper_id"]: p for p in rep["papers"]}
    assert by_pid["P1"]["normalized_doi"] == "10.1/abc"
    assert by_pid["P2"]["normalized_doi"] is None
    assert by_pid["P2"]["doi_method"] == "all_failed"


def test_load_papers_string_shape_legacy(tmp_repo):
    # Defensive: some old metadata might still have a string DOI directly.
    blob = {
        "_paper_id": "P5",
        "source_block": {"doi": "10.1/legacy", "title": "x"},
    }
    (tmp_repo / "metadata" / "P5.json").write_text(json.dumps(blob))
    rc, rep = _run(tmp_repo)
    by_pid = {p["paper_id"]: p for p in rep["papers"]}
    assert by_pid["P5"]["normalized_doi"] == "10.1/legacy"
    assert by_pid["P5"]["doi_method"] == "string_shape_legacy"


def test_load_papers_paper_id_falls_back_to_filename(tmp_repo):
    blob = {"source_block": {"doi": {"value": "10.1/x", "_meta": {}}}}
    (tmp_repo / "metadata" / "P99.json").write_text(json.dumps(blob))
    rc, rep = _run(tmp_repo)
    assert rep["papers"][0]["paper_id"] == "P99"


# ============================================================================
# Collision detection
# ============================================================================

def test_no_collisions_when_all_distinct(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/a")
    _write_metadata(tmp_repo / "metadata", "P2", doi="10.1/b")
    rc, rep = _run(tmp_repo)
    assert rep["collisions"] == []
    assert rep["summary"]["collision_groups"] == 0


def test_collision_two_papers_same_doi(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/shared")
    _write_metadata(tmp_repo / "metadata", "P2", doi="10.1/shared")
    rc, rep = _run(tmp_repo)
    assert len(rep["collisions"]) == 1
    c = rep["collisions"][0]
    assert c["paper_ids"] == ["P1", "P2"]
    assert c["alias_map_status"] == "new"


def test_collision_consistent_with_alias_map(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P5", doi="10.1/x")
    _write_metadata(tmp_repo / "metadata", "P90", doi="10.1/x")
    _write_aliases(tmp_repo, {"P5": "P90"})
    rc, rep = _run(tmp_repo)
    c = rep["collisions"][0]
    assert c["alias_map_status"] == "consistent"
    assert c["alias_map_canonical"] == "P90"


def test_collision_partial_one_side_in_alias_map(tmp_repo):
    # P123 is in alias map -> P74, but collides by DOI with P71.
    _write_metadata(tmp_repo / "metadata", "P71",  doi="10.1/conflict")
    _write_metadata(tmp_repo / "metadata", "P123", doi="10.1/conflict")
    _write_metadata(tmp_repo / "metadata", "P74",  doi=None)
    _write_aliases(tmp_repo, {"P123": "P74"})
    rc, rep = _run(tmp_repo)
    c = next(c for c in rep["collisions"]
             if set(c["paper_ids"]) == {"P71", "P123"})
    assert c["alias_map_status"] == "partial"


def test_collision_case_normalized_in_grouping(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P29", doi="10.1109/JBHI.2017.2743526")
    _write_metadata(tmp_repo / "metadata", "P30", doi="10.1109/jbhi.2017.2743526")
    rc, rep = _run(tmp_repo)
    assert len(rep["collisions"]) == 1
    assert rep["collisions"][0]["normalized_doi"] == "10.1109/jbhi.2017.2743526"


# ============================================================================
# Alias audit
# ============================================================================

def test_alias_audit_corroborated(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P5",  doi="10.1/x")
    _write_metadata(tmp_repo / "metadata", "P90", doi="10.1/x")
    _write_aliases(tmp_repo, {"P5": "P90"})
    rc, rep = _run(tmp_repo)
    a = next(a for a in rep["alias_audit"] if a["alias"] == "P5")
    assert a["status"] == "corroborated"


def test_alias_audit_null_side(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P4",  doi=None)
    _write_metadata(tmp_repo / "metadata", "P26", doi="10.1/y")
    _write_aliases(tmp_repo, {"P4": "P26"})
    rc, rep = _run(tmp_repo)
    a = next(a for a in rep["alias_audit"] if a["alias"] == "P4")
    assert a["status"] == "null_side"


def test_alias_audit_conflict_via_collision(tmp_repo):
    # P123 -> P74 in alias map, but P123's DOI matches P71's.
    _write_metadata(tmp_repo / "metadata", "P71",  doi="10.1/conflict")
    _write_metadata(tmp_repo / "metadata", "P74",  doi=None)
    _write_metadata(tmp_repo / "metadata", "P123", doi="10.1/conflict")
    _write_aliases(tmp_repo, {"P123": "P74"})
    rc, rep = _run(tmp_repo)
    a = next(a for a in rep["alias_audit"] if a["alias"] == "P123")
    assert a["status"] == "conflict"
    assert "suggested_action" in a
    assert "PDF compare" in a["suggested_action"]
    assert "extra_finding" in a


def test_alias_audit_conflict_via_differing_dois(tmp_repo):
    # Both have DOIs but they differ -> direct conflict.
    _write_metadata(tmp_repo / "metadata", "Pa", doi="10.1/a")
    _write_metadata(tmp_repo / "metadata", "Pb", doi="10.1/b")
    _write_aliases(tmp_repo, {"Pa": "Pb"})
    rc, rep = _run(tmp_repo)
    a = rep["alias_audit"][0]
    assert a["status"] == "conflict"


# ============================================================================
# Apply-aliases mode
# ============================================================================

def test_apply_aliases_resolves_consistent_collision(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P5",  doi="10.1/x")
    _write_metadata(tmp_repo / "metadata", "P90", doi="10.1/x")
    _write_aliases(tmp_repo, {"P5": "P90"})
    rc, rep = _run(tmp_repo, apply_aliases=True)
    assert rep["mode"] == "aliases_applied"
    assert rep["summary"]["collisions_remaining_after_aliases"] == 0
    assert rep["collisions"] == []


def test_apply_aliases_keeps_unresolved_collision(tmp_repo):
    # Partial collision (P71/P123 with alias P123->P74) survives apply-aliases.
    _write_metadata(tmp_repo / "metadata", "P71",  doi="10.1/conflict")
    _write_metadata(tmp_repo / "metadata", "P123", doi="10.1/conflict")
    _write_metadata(tmp_repo / "metadata", "P74",  doi=None)
    _write_aliases(tmp_repo, {"P123": "P74"})
    rc, rep = _run(tmp_repo, apply_aliases=True)
    assert rep["summary"]["collisions_remaining_after_aliases"] == 1
    assert len(rep["collisions"]) == 1
    c = rep["collisions"][0]
    assert "paper_ids_after_aliases" in c
    assert set(c["paper_ids_after_aliases"]) == {"P71", "P74"}


# ============================================================================
# Markdown rendering (the "Findings requiring action" lead section)
# ============================================================================

def test_markdown_leads_with_findings_section(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/a")
    rc, md = _run(tmp_repo, format_="markdown")
    # The first H2 in the output must be Findings requiring action.
    h2s = [line for line in md.splitlines() if line.startswith("## ")]
    assert h2s, "no H2 headers found"
    assert h2s[0] == "## Findings requiring action"


def test_markdown_findings_section_when_clean(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/a")
    _write_metadata(tmp_repo / "metadata", "P2", doi="10.1/b")
    rc, md = _run(tmp_repo, format_="markdown")
    assert "## Findings requiring action" in md
    assert "**None.**" in md


def test_markdown_findings_lists_new_collision_paper_ids(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P2",   doi="10.1/shared")
    _write_metadata(tmp_repo / "metadata", "P120", doi="10.1/shared")
    rc, md = _run(tmp_repo, format_="markdown")
    findings_section = md.split("## Findings requiring action")[1].split("## Summary")[0]
    assert "P2, P120" in findings_section
    assert "10.1/shared" in findings_section
    assert "1 DOI collision(s) not consistent" in findings_section


def test_markdown_findings_lists_conflict_explicitly(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "Pa", doi="10.1/a")
    _write_metadata(tmp_repo / "metadata", "Pb", doi="10.1/b")
    _write_aliases(tmp_repo, {"Pa": "Pb"})
    rc, md = _run(tmp_repo, format_="markdown")
    findings_section = md.split("## Findings requiring action")[1].split("## Summary")[0]
    assert "1 alias-map entry contradicted" in findings_section
    assert "Pa -> Pb" in findings_section


def test_markdown_findings_separates_collisions_and_conflicts(tmp_repo):
    # Both a new collision AND an alias map conflict.
    _write_metadata(tmp_repo / "metadata", "P2",   doi="10.1/shared")
    _write_metadata(tmp_repo / "metadata", "P120", doi="10.1/shared")
    _write_metadata(tmp_repo / "metadata", "Pa", doi="10.1/a")
    _write_metadata(tmp_repo / "metadata", "Pb", doi="10.1/b")
    _write_aliases(tmp_repo, {"Pa": "Pb"})
    rc, md = _run(tmp_repo, format_="markdown")
    findings = md.split("## Findings requiring action")[1].split("## Summary")[0]
    assert "DOI collision(s) not consistent" in findings
    assert "alias-map entry contradicted" in findings


# ============================================================================
# Extraction method counts
# ============================================================================

def test_extraction_method_counts_in_summary(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/a", method="regex")
    _write_metadata(tmp_repo / "metadata", "P2", doi="10.1/b", method="crossref")
    _write_metadata(tmp_repo / "metadata", "P3", doi=None)
    rc, rep = _run(tmp_repo)
    counts = rep["summary"]["extraction_method_counts"]
    assert counts.get("regex") == 1
    assert counts.get("crossref") == 1
    assert counts.get("all_failed") == 1


# ============================================================================
# JSON schema
# ============================================================================

def test_json_schema_top_level_keys(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/a")
    rc, rep = _run(tmp_repo)
    for key in ("schema_version", "tool", "timestamp", "mode", "inputs",
                "normalization_rules", "summary", "papers", "collisions",
                "alias_audit"):
        assert key in rep, f"missing top-level key: {key}"
    assert rep["schema_version"] == "v1"
    assert rep["tool"] == "canonical_doi"
    assert rep["mode"] == "raw"


def test_json_schema_summary_keys(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/a")
    rc, rep = _run(tmp_repo)
    for key in ("papers_total", "papers_with_doi", "papers_without_doi",
                "unique_normalized_dois", "collision_groups",
                "collisions_consistent_with_aliases", "collisions_new",
                "collisions_partial", "alias_entries_total",
                "alias_entries_corroborated", "alias_entries_null_side",
                "alias_entries_conflict", "extraction_method_counts"):
        assert key in rep["summary"], f"missing summary key: {key}"


def test_json_schema_per_paper_keys(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/a")
    rc, rep = _run(tmp_repo)
    p = rep["papers"][0]
    for key in ("paper_id", "metadata_file", "raw_doi", "normalized_doi",
                "doi_method", "normalization_applied"):
        assert key in p, f"missing per-paper key: {key}"


def test_apply_aliases_mode_field(tmp_repo):
    _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/a")
    rc, rep = _run(tmp_repo, apply_aliases=True)
    assert rep["mode"] == "aliases_applied"
    assert "collisions_remaining_after_aliases" in rep["summary"]


# ============================================================================
# Read-only guarantee
# ============================================================================

def test_metadata_files_not_modified(tmp_repo):
    p1 = _write_metadata(tmp_repo / "metadata", "P1", doi="10.1/a")
    p2 = _write_metadata(tmp_repo / "metadata", "P2", doi="10.1/a")
    aliases_path = _write_aliases(tmp_repo, {})
    before_p1 = p1.read_text()
    before_p2 = p2.read_text()
    before_aliases = aliases_path.read_text()
    _run(tmp_repo, apply_aliases=True)
    assert p1.read_text() == before_p1
    assert p2.read_text() == before_p2
    assert aliases_path.read_text() == before_aliases
