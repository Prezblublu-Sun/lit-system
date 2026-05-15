"""
Ingest one or more PDFs:
  python scripts/ingest.py inbox/*.pdf
  python scripts/ingest.py path/to/foo.pdf --force
  python scripts/ingest.py corpus/golden/*.pdf --dry-run

Pipeline per paper:
  doc_id <- sha256(pdf)
  Check dedup: if doc_id in metadata/, skip (unless --force)
  Allocate paper_id = next P{n}
  Docling -> cleaning -> DOI -> SOP_v2 -> metadata.json -> chunks.jsonl
  Chroma upsert (incremental)
"""
import sys
import argparse
import json
import time
from pathlib import Path

# Allow running from project root: python scripts/ingest.py
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.ingest import pipeline, chroma_sync
from scripts.ingest.paper_id import load_existing_index, next_paper_id
from scripts.ingest.doi_extract import get_doi


import requests

def extract_title_via_llm(md_text, max_chars=3000):
    """Ask the LLM to extract the paper title from the first few KB of cleaned md."""
    head = md_text[:max_chars]
    prompt = (
        "Extract the title of this research paper. Respond with ONLY the title text, "
        "nothing else, no quotes, no prefix.\n\n"
        "Paper first page:\n---\n" + head + "\n---\n\nTitle:"
    )
    try:
        r = requests.post("http://localhost:11434/api/generate", json={
            "model": "qwen2.5-14b-32k",
            "prompt": prompt,
            "stream": False,
            "options": {"num_ctx": 4096, "temperature": 0.0},
        }, timeout=60)
        r.raise_for_status()
        title = r.json().get("response", "").strip()
        title = title.strip('"\'\u201c\u201d')
        if len(title) < 10 or len(title) > 300:
            return None
        if "\n" in title:
            title = title.split("\n")[0].strip()
        return title
    except Exception as e:
        return None


METADATA_DIR = ROOT / "metadata"
DOCLING_DIR  = ROOT / "assets" / "docling_test"
CLEAN_DIR    = ROOT / "assets" / "docling_clean"
CHUNKS_DIR   = ROOT / "assets" / "chunks"
CHROMA_DIR   = ROOT / "assets" / "chroma_db"
OUTLINE_FILE = ROOT / "corpus" / "outline" / "review_outline.md"
INGEST_LOG   = ROOT / "results" / "ingest_log.jsonl"

METADATA_DIR.mkdir(exist_ok=True)
INGEST_LOG.parent.mkdir(exist_ok=True)


def log_event(record):
    record["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(INGEST_LOG, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def ingest_one(pdf_path: Path, paper_id: str, doc_id: str, content_hash: str,
               outline_text: str, dry_run: bool, skip_sop: bool = False):
    """Run the full pipeline for one paper. Returns dict summary."""
    summary = {"paper_id": paper_id, "doc_id": doc_id,
               "pdf": str(pdf_path.name), "stages": {}}

    # Stage: Docling
    print(f"  [docling] parsing {pdf_path.name}...")
    docling_r = pipeline.run_docling(pdf_path, DOCLING_DIR, paper_id)
    summary["stages"]["docling"] = {"duration_sec": docling_r["duration_sec"]}
    print(f"    done in {docling_r['duration_sec']}s")

    # Stage: cleaning
    print(f"  [cleaning] content_layer == body filter...")
    clean_r = pipeline.run_cleaning(docling_r["json_path"], CLEAN_DIR, paper_id)
    summary["stages"]["cleaning"] = {
        "kept": clean_r["kept_blocks"], "dropped": clean_r["dropped_blocks"]
    }
    print(f"    kept {clean_r['kept_blocks']}, dropped {clean_r['dropped_blocks']}")

    # Stage: DOI extraction (extract real title from cleaned md first)
    print(f"  [doi] extracting...")
    md_text = clean_r["md_path"].read_text()
    title_extracted = extract_title_via_llm(md_text)
    if title_extracted:
        title_for_doi = title_extracted
        print(f"    title (LLM): {title_for_doi[:80]}")
    else:
        title_for_doi = pdf_path.stem
        print(f"    title (filename fallback): {title_for_doi[:80]}")
    doi_info = get_doi(md_text, title=title_for_doi)
    doi_info["title_used"] = title_for_doi
    doi_info["title_method"] = "llm" if title_extracted else "filename_stem"
    summary["stages"]["doi"] = doi_info
    print(f"    DOI {doi_info['method']}: {doi_info['doi'] or '(none)'} -- {doi_info['details']}")
    
    # === DOI dedup WARN-only check ===
    # Scan existing metadata for duplicate DOI; log a warning but do NOT skip.
    # This produces an audit trail of DOI collisions during overnight --force re-ingest.
    if doi_info.get("doi"):
        _doi_to_check = doi_info["doi"].lower().strip()
        _other_pids_with_same_doi = []
        try:
            for _f in sorted(METADATA_DIR.glob("P*.json")):
                if _f.stem == paper_id:
                    continue  # don't compare to self
                try:
                    _other = json.loads(_f.read_text())
                    _od = _other.get("source_block", {}).get("doi")
                    if isinstance(_od, dict):
                        _od = _od.get("value")
                    if _od and _od.lower().strip() == _doi_to_check:
                        _other_pids_with_same_doi.append(_f.stem)
                except Exception:
                    pass
        except Exception:
            pass
        if _other_pids_with_same_doi:
            print(f"    [doi-dedup-warn] DOI {_doi_to_check} also present in: {_other_pids_with_same_doi}")
            doi_info["dedup_collisions"] = _other_pids_with_same_doi
            log_event({
                "action": "doi_collision",
                "paper_id": paper_id,
                "doi": _doi_to_check,
                "other_paper_ids": _other_pids_with_same_doi,
                "pdf": pdf_path.name,
            })

    # Stage: SOP v2 (skippable)
    if dry_run or skip_sop:
        print(f"  [sop_v2] SKIPPED ({'dry-run' if dry_run else '--no-sop'})")
        # Keys must match SOP_PROMPTS in pipeline.py (ADR-0014 SOP_v4: 6 tasks).
        sop_results = {
            "L1_factual_background":    {"ok": False, "error": "skipped"},
            "L1_factual_methods":       {"ok": False, "error": "skipped"},
            "L2_interpretive_problem":  {"ok": False, "error": "skipped"},
            "L2_interpretive_scoring":  {"ok": False, "error": "skipped"},
            "L3_outline_relevance":     {"ok": False, "error": "skipped"},
            "L4_domain_classification": {"ok": False, "error": "skipped"},
        }
        summary["stages"]["sop_v2"] = {"skipped": True}
    else:
        pdf_text = pipeline.extract_pdf_text(pdf_path)
        print(f"  [sop_v2] running 6 LLM tasks on {len(pdf_text):,} chars...")
        sop_results = pipeline.run_sop_v2(pdf_text, outline_text, paper_id)
        # ADR-0017: preserve 'skipped_no_outline' as a distinct (truthy) value so
        # the failure reporter below does not flag deliberately-skipped L3 as bad.
        def _stage_status(r):
            if r.get("ok"):
                return True
            if r.get("error") == "skipped_no_outline":
                return "skipped_no_outline"
            return False
        summary["stages"]["sop_v2"] = {
            sop_key: _stage_status(r) for sop_key, r in sop_results.items()
            if isinstance(r, dict) and "ok" in r
        }

    # Stage: metadata.json
    print(f"  [metadata] building schema v1...")
    final_title = title_extracted if title_extracted else pdf_path.stem
    sop_results["_title"]    = final_title
    sop_results["_filename"] = pdf_path.name
    assets = {
        "pdf_source":   str(pdf_path.relative_to(ROOT)) if pdf_path.is_relative_to(ROOT) else str(pdf_path),
        "docling_json": str(docling_r["json_path"].relative_to(ROOT)),
        "docling_md":   str(docling_r["md_path"].relative_to(ROOT)),
        "cleaned_json": str(clean_r["json_path"].relative_to(ROOT)),
        "cleaned_md":   str(clean_r["md_path"].relative_to(ROOT)),
    }
    md = pipeline.build_metadata(
        paper_id=paper_id, doc_id=doc_id, content_hash=content_hash,
        filename=pdf_path.name, title=final_title,
        sop_results=sop_results, doi_info=doi_info, assets=assets,
    )
    out_md_path = METADATA_DIR / f"{paper_id}.json"
    out_md_path.write_text(json.dumps(md, indent=2, ensure_ascii=False))
    summary["stages"]["metadata"] = {"path": str(out_md_path.relative_to(ROOT))}
    print(f"    -> {out_md_path.relative_to(ROOT)}")

    # Stage: chunks.jsonl
    print(f"  [chunks] building token_window v3...")
    chunks_path = CHUNKS_DIR / f"{paper_id}_chunks.jsonl"
    chunk_r = pipeline.build_chunks(clean_r["json_path"], doc_id, paper_id, chunks_path)
    summary["stages"]["chunks"] = {
        "n_chunks": chunk_r["n_chunks"],
        "start_reason": chunk_r["start_reason"],
        "end_reason":   chunk_r["end_reason"],
    }
    print(f"    {chunk_r['n_chunks']} chunks "
          f"[{chunk_r['start_reason']} -> {chunk_r['end_reason']}]")

    # Stage: Chroma upsert
    if not dry_run:
        print(f"  [chroma] incremental upsert...")
        _, coll, _ = chroma_sync.get_or_create_collection(CHROMA_DIR)
        # If forcing re-ingest, remove existing chunks of this paper first
        existing = chroma_sync.chunks_for_paper(coll, paper_id)
        if existing > 0:
            chroma_sync.remove_paper(coll, paper_id)
        chunks = chroma_sync.load_chunks_jsonl(chunks_path)
        elapsed = chroma_sync.upsert_chunks(coll, chunks)
        summary["stages"]["chroma"] = {
            "upserted": len(chunks), "removed_before": existing,
            "elapsed_sec": elapsed,
        }
        print(f"    upserted {len(chunks)} (had {existing}), {elapsed}s")
    else:
        summary["stages"]["chroma"] = {"skipped": "dry_run"}

    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdfs", nargs="+", help="PDF paths to ingest")
    ap.add_argument("--force", action="store_true",
                    help="Re-ingest even if doc_id already exists")
    ap.add_argument("--dry-run", action="store_true",
                    help="Run pipeline but skip Chroma upsert (test mode)")
    ap.add_argument("--no-sop", action="store_true",
                    help="Skip SOP_v2 (5 LLM calls per paper). "
                         "Metadata will have null factual/interpretive/personal_relevance fields.")
    ap.add_argument("--no-outline", action="store_true",
                    help="Skip L3_outline_relevance (saves ~30s/paper). "
                         "Use for batches unrelated to the current review outline "
                         "(per ADR-0017). L3 entry gets a 'skipped_no_outline' "
                         "placeholder; interpretive.outline_match_status becomes "
                         "'skipped_no_outline'.")
    args = ap.parse_args()

    pdfs = [Path(p).resolve() for p in args.pdfs]
    
    # === Ollama restart hook: every N papers, restart to avoid KV cache bloat ===
    OLLAMA_RESTART_EVERY = 10
    import subprocess
    import time as _time_for_restart
    _papers_processed = 0
    
    def _restart_ollama_if_needed():
        nonlocal _papers_processed
        _papers_processed += 1
        if _papers_processed > 0 and _papers_processed % OLLAMA_RESTART_EVERY == 0:
            print(f"  [ollama-hook] restarting ollama after {_papers_processed} papers...")
            try:
                subprocess.run(['sudo', '-n', 'systemctl', 'restart', 'ollama'],
                               check=True, timeout=30)
                _time_for_restart.sleep(15)
                print(f"  [ollama-hook] restarted, slept 15s, continuing")
            except Exception as e:
                print(f"  [ollama-hook] WARNING: restart failed: {e}")
    
    for p in pdfs:
        if not p.exists():
            print(f"[error] not found: {p}")
            sys.exit(1)

    # ADR-0017: --no-outline forces outline_text=None; run_sop_v2 then skips L3
    # entirely and emits a 'skipped_no_outline' placeholder.
    if args.no_outline:
        outline_text = None
        print("[setup] --no-outline: L3_outline_relevance will be skipped (ADR-0017)")
    else:
        outline_text = OUTLINE_FILE.read_text()[:3500] if OUTLINE_FILE.exists() else ""
        if not outline_text:
            print("[warn] no review outline file found; L3_outline_relevance will be "
                  "skipped (ADR-0017 empty-outline branch)")

    doc_id_idx, doi_idx, used_nums = load_existing_index(METADATA_DIR)
    print(f"[setup] existing: {len(used_nums)} papers, used nums {sorted(used_nums)[:10]}...")
    print(f"[setup] mode: {'FORCE re-ingest' if args.force else 'skip-if-exists'}"
          f"{', DRY-RUN' if args.dry_run else ''}")

    all_summaries = []
    skipped, ingested, failed = 0, 0, 0

    for pdf in pdfs:
        print(f"\n{'='*60}\n  PDF: {pdf.name}")
        doc_id, content_hash = pipeline.compute_doc_id(pdf)
        print(f"  doc_id: {doc_id}")

        if doc_id in doc_id_idx and not args.force:
            existing_pid = doc_id_idx[doc_id]
            print(f"  [skip] already ingested as {existing_pid} (use --force to re-run)")
            log_event({"action": "skip", "doc_id": doc_id, "existing": existing_pid,
                       "pdf": pdf.name})
            skipped += 1
            continue

        if doc_id in doc_id_idx and args.force:
            paper_id = doc_id_idx[doc_id]
            print(f"  [force] re-ingesting existing {paper_id}")
        else:
            paper_id, n = next_paper_id(used_nums)
            used_nums.add(n)
            doc_id_idx[doc_id] = paper_id
            print(f"  [new] assigned {paper_id}")

        try:
            summary = ingest_one(pdf, paper_id, doc_id, content_hash,
                                 outline_text, args.dry_run, args.no_sop)
            summary["status"] = "ok"
            log_event({"action": "ingest_ok", **summary})
            ingested += 1
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(f"  [FAILED] {e}")
            print(tb)
            log_event({"action": "ingest_fail", "doc_id": doc_id,
                       "paper_id": paper_id, "pdf": pdf.name,
                       "error": str(e), "traceback": tb})
            failed += 1
            continue
        all_summaries.append(summary)
        _restart_ollama_if_needed()

    # Final report
    print(f"\n{'='*60}\nINGEST REPORT")
    print(f"  ingested: {ingested}    skipped: {skipped}    failed: {failed}")

    doi_missing = [s for s in all_summaries
                   if not s["stages"].get("doi", {}).get("doi")]
    if doi_missing:
        print(f"\n  DOI missing for {len(doi_missing)} paper(s):")
        for s in doi_missing:
            d = s["stages"]["doi"]
            print(f"    {s['paper_id']}  {s['pdf']}  -- {d.get('method')}: {d.get('details')}")
        print(f"  -> fill manually later (see ADR-0003)")

    sop_failed = []
    for s in all_summaries:
        sop_r = s["stages"].get("sop_v2", {})
        bad = [k for k, ok in sop_r.items() if not ok]
        if bad:
            sop_failed.append((s["paper_id"], bad))
    if sop_failed:
        print(f"\n  SOP failures:")
        for pid, bad in sop_failed:
            print(f"    {pid}: {bad}")

    print(f"\n  log: {INGEST_LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
