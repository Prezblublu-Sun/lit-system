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

# SOP_v2 fields we benchmark (path within metadata JSON)
SOP_FIELDS = {
    "L1_background":  ("factual", "sop_l1_background_raw"),
    "L1_methods":     ("factual", "methods_raw"),
    "L2_problem":     ("interpretive", "core_problem_raw"),
    "L2_scoring":     ("interpretive", "scoring_10_dim_local"),
    "L3_personal":    ("personal_relevance", "sop_l3_raw"),
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

def check_field_completeness(metadata: dict) -> dict:
    """Verify all 5 SOP fields are present and non-empty."""
    status = {}
    for label, (block, key) in SOP_FIELDS.items():
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
    
    return result

# === Aggregate ===

def aggregate(results: list[dict]) -> dict:
    """Cross-paper summary stats."""
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
    }
    
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
    out_path = RESULTS_DIR / "benchmark_sop_v2_baseline.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print()
    print(f"Saved: {out_path}")
    print(f"Size: {out_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
