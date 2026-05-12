"""
Build chunks.jsonl from cleaned Docling JSON.
Token-windowed chunks (800 tokens, 150 overlap) over block sequences.
- Skips frontmatter: chunks start at first abstract/intro-like section_header.
- Truncates references: chunks stop at first references/bibliography-like section_header.
- Guards against tiny tail chunks and overlap dead-loops.
"""
import json
import re
from pathlib import Path
from datetime import datetime, timezone

try:
    import tiktoken
    ENC = tiktoken.get_encoding("cl100k_base")
    def count_tokens(s): return len(ENC.encode(s))
except ImportError:
    print("[warn] tiktoken not installed, falling back to len(s)//4 approx")
    def count_tokens(s): return len(s) // 4

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DIR    = PROJECT_ROOT / "assets" / "docling_clean"
METADATA_DIR = PROJECT_ROOT / "metadata"
CHUNKS_DIR   = PROJECT_ROOT / "assets" / "chunks"
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

CHUNKER_VERSION   = "token_window_chunker_v3"
CLEANING_VERSION  = "v1_content_layer_body"
WINDOW_TOKENS     = 800
OVERLAP_TOKENS    = 150
MIN_CHUNK_TOKENS  = 50

START_HEADER_PATTERNS = [
    r"^abstract$",
    r"^summary$",
    r"^摘要$",
    r"^概要$",
    r"^introduction$",
    r"^引言$",
    r"^背景$",
    r"^1\.?\s+introduction$",
    r"^i\.?\s+introduction$",
]
START_HEADER_RE = re.compile("|".join(START_HEADER_PATTERNS), re.IGNORECASE)

END_HEADER_PATTERNS = [
    # references-like
    r"^references$",
    r"^bibliography$",
    r"^reference\s*list$",
    r"^literature\s*cited$",
    r"^works\s+cited$",
    r"^参考文献$",
    r"^引用$",
    # post-body sections (any of these means main body ended)
    r"^acknowledgements?$",
    r"^acknowledgments?$",
    r"^conflicts?\s+of\s+interest$",
    r"^conflict\s+of\s+interest\s+statement$",
    r"^author\s+contributions?$",
    r"^data\s+availability(\s+statement)?$",
    r"^funding(\s+statement)?$",
    r"^supplementary\s+(material|information|data)$",
    r"^appendix(\s+[a-z0-9])?$",
    r"^致谢$",
    r"^author\s+information$",
]
END_HEADER_RE = re.compile("|".join(END_HEADER_PATTERNS), re.IGNORECASE)

PAPERS = ["P1", "P2", "P3", "P4", "P5"]


def block_to_text(block):
    label = block.get("label", "text")
    text  = (block.get("text") or "").strip()
    if not text:
        return ""
    if label == "section_header":
        return f"\n## {text}\n"
    if label == "caption":
        return f"\n*{text}*\n"
    if label == "list_item":
        return f"- {text}"
    return text


def block_provenance(block):
    out = []
    for prov in block.get("prov", []):
        bbox = prov.get("bbox", {})
        if isinstance(bbox, dict):
            bbox_list = [bbox.get("l"), bbox.get("t"),
                         bbox.get("r"), bbox.get("b")]
        else:
            bbox_list = bbox
        out.append({
            "page": prov.get("page_no"),
            "bbox": bbox_list,
            "block_label": block.get("label"),
        })
    return out


def find_start_block_idx(texts):
    for i, t in enumerate(texts):
        if t.get("label") != "section_header":
            continue
        header_text = (t.get("text") or "").strip().rstrip(".:")
        if START_HEADER_RE.match(header_text):
            return i, f"matched_header:{header_text!r}"
    for i, t in enumerate(texts):
        if t.get("label") == "section_header":
            return i, "fallback_first_section_header"
    return 0, "fallback_block_0"


def find_end_block_idx(texts, start_idx):
    """Find first References-like header AFTER start_idx. Return exclusive end."""
    for i in range(start_idx + 1, len(texts)):
        t = texts[i]
        if t.get("label") != "section_header":
            continue
        header_text = (t.get("text") or "").strip().rstrip(".:")
        if END_HEADER_RE.match(header_text):
            return i, f"matched_header:{header_text!r}"
    return len(texts), "fallback_eof"


def build_chunks_for_paper(pid, doc_id):
    src = CLEAN_DIR / f"{pid}_clean.json"
    d = json.load(open(src))
    texts = d.get("texts", [])

    start_idx, start_reason = find_start_block_idx(texts)
    end_idx, end_reason     = find_end_block_idx(texts, start_idx)

    block_data = []
    for i, b in enumerate(texts):
        if i < start_idx or i >= end_idx:
            continue
        txt = block_to_text(b)
        if not txt:
            continue
        block_data.append({
            "idx": i, "block": b, "text": txt,
            "tokens": count_tokens(txt),
            "label": b.get("label", "text"),
        })

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
            p_start, p_end = prev_range
            if win_start >= p_start and win_end <= p_end:
                skip = True

        text = "\n".join(b["text"] for b in window).strip()
        tok_count = count_tokens(text)
        if tok_count < MIN_CHUNK_TOKENS:
            skip = True

        if not skip:
            headers = [b["block"].get("text", "").strip()
                       for b in window
                       if b["label"] == "section_header"]
            provenance = []
            for b in window:
                provenance.extend(block_provenance(b["block"]))
            chunks.append({
                "chunk_id": f"{doc_id}_c{chunk_idx:04d}",
                "doc_id": doc_id,
                "paper_id": pid,
                "chunk_index": chunk_idx,
                "chunk_type": "token_window",
                "text": text,
                "token_count": tok_count,
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
                    "start_block_idx": start_idx,
                    "start_reason": start_reason,
                    "end_block_idx": end_idx,
                    "end_reason": end_reason,
                    "produced_at": now,
                },
            })
            prev_range = (win_start, win_end)
            chunk_idx += 1

        if j >= n:
            break

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

    return chunks, start_idx, start_reason, end_idx, end_reason


summary = {}
total = 0
for pid in PAPERS:
    mpath = METADATA_DIR / f"{pid}.json"
    if not mpath.exists():
        print(f"[skip] {pid}: no metadata")
        continue
    doc_id = json.load(open(mpath))["id_block"]["doc_id"]
    chunks, start_idx, start_reason, end_idx, end_reason = build_chunks_for_paper(pid, doc_id)
    out = CHUNKS_DIR / f"{pid}_chunks.jsonl"
    with open(out, "w") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    toks = [c["token_count"] for c in chunks]
    summary[pid] = {
        "n_chunks": len(chunks),
        "tok_min": min(toks) if toks else 0,
        "tok_max": max(toks) if toks else 0,
        "tok_mean": round(sum(toks)/len(toks), 1) if toks else 0,
        "tok_total": sum(toks),
        "start_block_idx": start_idx,
        "start_reason": start_reason,
        "end_block_idx": end_idx,
        "end_reason": end_reason,
        "path": str(out.relative_to(PROJECT_ROOT)),
    }
    total += len(chunks)
    print(f"[{pid}] {len(chunks)} chunks, tok mean={summary[pid]['tok_mean']}, "
          f"total {summary[pid]['tok_total']:,}  "
          f"[{start_idx} -> {end_idx}]  start={start_reason} end={end_reason}")

(CHUNKS_DIR / "_summary.json").write_text(json.dumps(summary, indent=2))
print(f"\n[done] {total} chunks total (was 340 in v2)")
