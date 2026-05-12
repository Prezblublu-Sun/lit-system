"""
Single-paper ingest pipeline. Each function is independently re-runnable.
Stage order: docling -> cleaning -> doi -> sop_v2 -> metadata -> chunks
"""
import json
import hashlib
import re
import time
import requests
from pathlib import Path
from datetime import datetime, timezone

from .doi_extract import get_doi

# ============ Constants (mirror existing scripts) ============

CLEANING_VERSION  = "v1_content_layer_body"
CHUNKER_VERSION   = "token_window_chunker_v3"
PROMPT_VERSION    = "sop_v2_qwen14b_32k"

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL  = "qwen2.5-14b-32k"

# Stop sections for chunking (mirror build_chunks_v1.py v3)
START_HEADER_PATTERNS = [
    r"^abstract$", r"^summary$", r"^摘要$", r"^概要$",
    r"^introduction$", r"^引言$", r"^背景$",
    r"^1\.?\s+introduction$", r"^i\.?\s+introduction$",
]
END_HEADER_PATTERNS = [
    r"^references$", r"^bibliography$", r"^reference\s*list$",
    r"^literature\s*cited$", r"^works\s+cited$",
    r"^参考文献$", r"^引用$",
    r"^acknowledgements?$", r"^acknowledgments?$",
    r"^conflicts?\s+of\s+interest$", r"^conflict\s+of\s+interest\s+statement$",
    r"^author\s+contributions?$",
    r"^data\s+availability(\s+statement)?$",
    r"^funding(\s+statement)?$",
    r"^supplementary\s+(material|information|data)$",
    r"^appendix(\s+[a-z0-9])?$",
    r"^致谢$", r"^author\s+information$",
]
START_HEADER_RE = re.compile("|".join(START_HEADER_PATTERNS), re.IGNORECASE)
END_HEADER_RE   = re.compile("|".join(END_HEADER_PATTERNS),   re.IGNORECASE)

WINDOW_TOKENS    = 800
OVERLAP_TOKENS   = 150
MIN_CHUNK_TOKENS = 50


# ============ Stage 1: doc_id from PDF ============

def compute_doc_id(pdf_path: Path):
    """Return (doc_id_16hex, full_sha256)."""
    h = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    full = h.hexdigest()
    return full[:16], full


# ============ Stage 2: Docling parse ============

def run_docling(pdf_path: Path, out_dir: Path, paper_id: str):
    """Parse PDF with Docling. Write {paper_id}_docling.json + .md."""
    from docling.document_converter import DocumentConverter
    out_dir.mkdir(parents=True, exist_ok=True)
    json_out = out_dir / f"{paper_id}_docling.json"
    md_out   = out_dir / f"{paper_id}_docling.md"

    t0 = time.time()
    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    doc = result.document

    md_out.write_text(doc.export_to_markdown())
    json_out.write_text(json.dumps(doc.export_to_dict(), indent=2, ensure_ascii=False))

    return {
        "json_path": json_out,
        "md_path":   md_out,
        "duration_sec": round(time.time() - t0, 1),
    }


# ============ Stage 3: cleaning ============

def run_cleaning(docling_json_path: Path, out_dir: Path, paper_id: str):
    """content_layer == body filter. Write {paper_id}_clean.json + .md."""
    from collections import Counter
    out_dir.mkdir(parents=True, exist_ok=True)
    d = json.loads(docling_json_path.read_text())
    texts = d.get("texts", [])
    before = len(texts)
    kept    = [t for t in texts if t.get("content_layer") == "body"]
    dropped = [t for t in texts if t.get("content_layer") != "body"]

    cleaned = dict(d)
    cleaned["texts"] = kept
    cleaned["_cleaning"] = {
        "version": CLEANING_VERSION,
        "input_blocks": before,
        "kept_blocks": len(kept),
        "dropped_blocks": len(dropped),
        "dropped_label_distribution": dict(
            Counter(t.get("label", "?") for t in dropped)
        ),
    }
    md_lines = []
    for t in kept:
        label = t.get("label", "text")
        text = (t.get("text") or "").strip()
        if not text:
            continue
        if label == "section_header":
            md_lines.append(f"\n## {text}\n")
        elif label == "caption":
            md_lines.append(f"\n*{text}*\n")
        elif label == "list_item":
            md_lines.append(f"- {text}")
        else:
            md_lines.append(text)
    md_out = "\n".join(md_lines)

    json_path = out_dir / f"{paper_id}_clean.json"
    md_path   = out_dir / f"{paper_id}_clean.md"
    json_path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2))
    md_path.write_text(md_out)

    return {
        "json_path": json_path,
        "md_path":   md_path,
        "input_blocks":  before,
        "kept_blocks":   len(kept),
        "dropped_blocks": len(dropped),
    }


# ============ Stage 4: SOP v2 (5 LLM calls) ============

# Each tuple: (sop_key, prompt_template_fn) -- prompts mirror sop_v2_direct.py
# We keep the prompts inline here to make the pipeline self-contained.

SOP_PROMPTS = {
    "L1_factual_background": (
        "You are extracting factual content from a research paper.\n\n"
        "Paper text:\n{text}\n\n"
        "Extract the following with exact quotes and page numbers where possible:\n"
        "1) Research Background\n2) Core Concepts\n3) Common Pitfalls or Failure Modes\n"
        "4) Design Objectives\n5) Evaluation Metrics"
    ),
    "L1_factual_methods": (
        "You are extracting methods from a research paper.\n\n"
        "Paper text:\n{text}\n\n"
        "List all methods organized as:\nA) Experimental Methods\n"
        "B) Analytical/Modeling Methods\nC) Validation Methods\n"
        "Include page numbers."
    ),
    "L2_interpretive_problem": (
        "You are critically analyzing a research paper.\n\n"
        "Paper text:\n{text}\n\n"
        "Answer with page references:\n"
        "1) Most central problem and why it matters\n"
        "2) Hardest technical difficulties\n"
        "3) What did the authors CLAIM vs what evidence ACTUALLY supports? Gaps\n"
        "4) One-sentence judgment of intellectual contribution"
    ),
    "L2_interpretive_scoring": (
        "Score the paper 1-10 on each of these 10 dimensions, with one-sentence justification each:\n"
        "Novelty, Clarity, Methodological rigor, Empirical strength, Reproducibility,\n"
        "Theoretical contribution, Practical impact, Scope appropriateness, "
        "Writing quality, Citation/literature use.\n\n"
        "Paper text:\n{text}"
    ),
    "L3_personal_relevance": (
        "Given this paper and the review outline below, identify the top 3 sections of the "
        "review outline this paper most belongs to, with reasoning.\n\n"
        "Review outline:\n{outline}\n\nPaper text:\n{text}"
    ),
}


def call_ollama(prompt: str, max_retries: int = 2):
    """Single Ollama generation call. Returns (ok, answer, prompt_tokens, completion_tokens, duration_sec)."""
    for attempt in range(max_retries + 1):
        try:
            t0 = time.time()
            r = requests.post(
                OLLAMA_URL,
                json={"model": LLM_MODEL, "prompt": prompt, "stream": False,
                      "options": {"num_ctx": 32768}},
                timeout=600,
            )
            r.raise_for_status()
            j = r.json()
            return {
                "ok": True,
                "answer": j.get("response", ""),
                "prompt_tokens":     j.get("prompt_eval_count", 0),
                "completion_tokens": j.get("eval_count", 0),
                "duration_sec": round(time.time() - t0, 1),
            }
        except Exception as e:
            if attempt == max_retries:
                return {"ok": False, "error": str(e), "duration_sec": 0}
            time.sleep(2)


def run_sop_v2(pdf_text: str, outline_text: str, paper_id: str, max_chars: int = 60000):
    """Run 5 SOP tasks. Returns dict matching sop_v2.json shape."""
    paper_text = pdf_text[:max_chars]
    results = {
        "_title":      None,  # caller fills
        "_filename":   None,  # caller fills
        "_pdf_chars":  len(pdf_text),
    }
    for sop_key, template in SOP_PROMPTS.items():
        prompt = template.format(text=paper_text, outline=outline_text)
        print(f"  [{paper_id}] {sop_key} ...")
        out = call_ollama(prompt)
        results[sop_key] = out
        if out.get("ok"):
            print(f"    OK in {out['duration_sec']}s, {out['completion_tokens']} tok")
        else:
            print(f"    FAILED: {out.get('error', 'unknown')}")
    return results


# ============ Stage 5: metadata.json ============

# Mapping mirrors build_metadata_v1.py
SOP_TO_SCHEMA = [
    ("L1_factual_background",  "factual",            "sop_l1_background_raw", None),
    ("L1_factual_methods",     "factual",            "methods_raw",           None),
    ("L2_interpretive_problem","interpretive",       "core_problem_raw",
        "kept under interpretive per sop_v2 naming; ADR-0003 lists under factual"),
    ("L2_interpretive_scoring","interpretive",       "scoring_10_dim_local",
        "D-grade local LLM output; pending Path C web chat review"),
    ("L3_personal_relevance",  "personal_relevance", "sop_l3_raw",            None),
]


def build_metadata(paper_id, doc_id, content_hash, filename, title,
                   sop_results, doi_info, assets, produced_at=None):
    """Assemble schema v1 metadata dict (matches build_metadata_v1.py output)."""
    now = datetime.now(timezone.utc).isoformat()
    produced_at = produced_at or now

    md = {
        "_schema_version": "v1",
        "_paper_id":       paper_id,
        "_ingested_at":    now,
        "_schema_notes": [
            "v1: factual/interpretive fields may contain raw markdown blocks (atomization deferred to v2)",
            "v1: core_problem_raw kept under interpretive per sop_v2 naming; ADR-0003 lists under factual (resolve in v2)",
        ],
        "id_block": {
            "doc_id":       doc_id,
            "filename":     filename,
            "content_hash": content_hash,
        },
        "source_block": {
            "title": {
                "value": title,
                "_meta": {
                    "produced_by": "human-wei",
                    "prompt_version": "manual_v1",
                    "produced_at": produced_at,
                    "reviewed_by": None,
                    "reviewed_at": None,
                    "evidence": [],
                },
            },
            "doi": {
                "value": doi_info.get("doi"),
                "_meta": {
                    "produced_by": "regex_or_crossref",
                    "prompt_version": "doi_extract_v1",
                    "produced_at": produced_at,
                    "reviewed_by": None,
                    "reviewed_at": None,
                    "method":  doi_info.get("method"),
                    "details": doi_info.get("details"),
                    "evidence": [],
                },
            },
        },
        "factual": {},
        "interpretive": {},
        "personal_relevance": {},
        "assets": dict(assets),
    }

    for sop_key, block, schema_field, note in SOP_TO_SCHEMA:
        entry = sop_results.get(sop_key)
        if not entry or not entry.get("ok"):
            md[block][schema_field] = {
                "value": None,
                "_meta": {
                    "produced_by": "qwen2.5-14b-32k",
                    "prompt_version": PROMPT_VERSION,
                    "produced_at": produced_at,
                    "reviewed_by": None,
                    "reviewed_at": None,
                    "evidence": [],
                    "note": note,
                    "failed": True,
                    "error":  entry.get("error") if entry else "missing",
                },
            }
            continue
        md[block][schema_field] = {
            "value": entry["answer"],
            "_meta": {
                "produced_by": "qwen2.5-14b-32k",
                "prompt_version": PROMPT_VERSION,
                "produced_at": produced_at,
                "reviewed_by": None,
                "reviewed_at": None,
                "evidence": [],
                "note": note,
            },
        }
    return md


# ============ Stage 6: chunks.jsonl ============

def _block_to_text(block):
    label = block.get("label", "text")
    text  = (block.get("text") or "").strip()
    if not text: return ""
    if label == "section_header": return f"\n## {text}\n"
    if label == "caption":        return f"\n*{text}*\n"
    if label == "list_item":      return f"- {text}"
    return text


def _block_provenance(block):
    out = []
    for prov in block.get("prov", []):
        bbox = prov.get("bbox", {})
        if isinstance(bbox, dict):
            bbox_list = [bbox.get("l"), bbox.get("t"), bbox.get("r"), bbox.get("b")]
        else:
            bbox_list = bbox
        out.append({"page": prov.get("page_no"), "bbox": bbox_list,
                    "block_label": block.get("label")})
    return out


def _find_start(texts):
    for i, t in enumerate(texts):
        if t.get("label") != "section_header": continue
        h = (t.get("text") or "").strip().rstrip(".:")
        if START_HEADER_RE.match(h):
            return i, f"matched_header:{h!r}"
    for i, t in enumerate(texts):
        if t.get("label") == "section_header":
            return i, "fallback_first_section_header"
    return 0, "fallback_block_0"


def _find_end(texts, start_idx):
    for i in range(start_idx + 1, len(texts)):
        t = texts[i]
        if t.get("label") != "section_header": continue
        h = (t.get("text") or "").strip().rstrip(".:")
        if END_HEADER_RE.match(h):
            return i, f"matched_header:{h!r}"
    return len(texts), "fallback_eof"


def build_chunks(clean_json_path: Path, doc_id: str, paper_id: str,
                 chunks_out_path: Path):
    """Token-windowed chunks v3. Write jsonl. Return summary dict."""
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    count_tokens = lambda s: len(enc.encode(s))

    d = json.loads(clean_json_path.read_text())
    texts = d.get("texts", [])
    start_idx, start_reason = _find_start(texts)
    end_idx,   end_reason   = _find_end(texts, start_idx)

    block_data = []
    for i, b in enumerate(texts):
        if i < start_idx or i >= end_idx: continue
        txt = _block_to_text(b)
        if not txt: continue
        block_data.append({"idx": i, "block": b, "text": txt,
                           "tokens": count_tokens(txt),
                           "label": b.get("label", "text")})

    chunks = []
    now = datetime.now(timezone.utc).isoformat()
    n = len(block_data)
    i = 0
    chunk_idx = 0
    prev_range = None

    while i < n:
        j = i
        cur_tokens = 0
        while j < n and cur_tokens + block_data[j]["tokens"] <= WINDOW_TOKENS:
            cur_tokens += block_data[j]["tokens"]
            j += 1
        if j == i:
            j = i + 1
            cur_tokens = block_data[i]["tokens"]

        window = block_data[i:j]
        win_start = window[0]["idx"]
        win_end   = window[-1]["idx"]

        skip = False
        if prev_range is not None:
            ps, pe = prev_range
            if win_start >= ps and win_end <= pe: skip = True

        text = "\n".join(b["text"] for b in window).strip()
        tok_count = count_tokens(text)
        if tok_count < MIN_CHUNK_TOKENS: skip = True

        if not skip:
            headers = [b["block"].get("text", "").strip()
                       for b in window if b["label"] == "section_header"]
            provenance = []
            for b in window: provenance.extend(_block_provenance(b["block"]))
            chunks.append({
                "chunk_id": f"{doc_id}_c{chunk_idx:04d}",
                "doc_id": doc_id, "paper_id": paper_id,
                "chunk_index": chunk_idx, "chunk_type": "token_window",
                "text": text, "token_count": tok_count,
                "block_count": len(window),
                "block_index_range": [win_start, win_end],
                "section_headers_seen": headers,
                "provenance": provenance,
                "_meta": {
                    "produced_by": "docling_v2.93.0 + " + CHUNKER_VERSION,
                    "chunker_version": CHUNKER_VERSION,
                    "cleaning_version": CLEANING_VERSION,
                    "window_tokens": WINDOW_TOKENS,
                    "overlap_tokens": OVERLAP_TOKENS,
                    "min_chunk_tokens": MIN_CHUNK_TOKENS,
                    "start_block_idx": start_idx, "start_reason": start_reason,
                    "end_block_idx":   end_idx,   "end_reason":   end_reason,
                    "produced_at": now,
                },
            })
            prev_range = (win_start, win_end)
            chunk_idx += 1

        if j >= n: break
        back_tokens = 0
        k = j
        while k > i and back_tokens < OVERLAP_TOKENS:
            k -= 1
            back_tokens += block_data[k]["tokens"]
        new_i = max(k, i + 1)
        if prev_range is not None:
            while new_i < n and block_data[new_i]["idx"] <= prev_range[1] and \
                  (j < n and block_data[j]["idx"] <= prev_range[1]):
                new_i += 1
        i = new_i

    chunks_out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(chunks_out_path, "w") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return {
        "n_chunks": len(chunks),
        "start_block_idx": start_idx, "start_reason": start_reason,
        "end_block_idx":   end_idx,   "end_reason":   end_reason,
        "path": str(chunks_out_path),
    }


# ============ PDF text extraction (for SOP) ============

def extract_pdf_text(pdf_path: Path, max_chars: int = 60000):
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    out = []
    total = 0
    for page in reader.pages:
        txt = page.extract_text() or ""
        out.append(txt)
        total += len(txt)
        if total >= max_chars * 1.2:
            break
    return "\n".join(out)[:max_chars]
