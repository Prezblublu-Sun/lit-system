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

CLEANING_VERSION  = "v2_section_boundary_body"

# === cleaning_v2 helpers ===
import re as _re_clean_v2
_BODY_START_PATTERN = _re_clean_v2.compile(
    r"^(abstract|introduction|1\.\s)", _re_clean_v2.IGNORECASE)
_BODY_END_PATTERN = _re_clean_v2.compile(
    r"^(references|bibliography|acknowledg(e?)ments?|funding|"
    r"conflict|data availability|author contributions|orcid)",
    _re_clean_v2.IGNORECASE)

def _find_body_range(texts):
    """v2: detect [start, end) of true body content via section_header markers."""
    start_idx = 0
    end_idx = len(texts)
    for i, t in enumerate(texts):
        if t.get("label") == "section_header":
            txt = (t.get("text", "") or "").strip()
            if _BODY_START_PATTERN.match(txt):
                start_idx = i
                break
    for i in range(start_idx + 1, len(texts)):
        t = texts[i]
        if t.get("label") == "section_header":
            txt = (t.get("text", "") or "").strip()
            if _BODY_END_PATTERN.match(txt):
                end_idx = i
                break
    return start_idx, end_idx

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
    # v2: detect body range first (skip pre-body TOC/affiliations, post-body refs/acks)
    _body_start, _body_end = _find_body_range(texts)
    _body_range = texts[_body_start:_body_end]
    
    kept    = [t for t in _body_range if t.get("content_layer") == "body"]
    _furniture = [t for t in _body_range if t.get("content_layer") != "body"]
    dropped = texts[:_body_start] + texts[_body_end:] + _furniture

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


# ============ Stage 4: SOP v2 (6 LLM calls; v4 prompts per ADR-0014) ============

# Each tuple: (sop_key, prompt_template_fn) -- prompts mirror sop_v2_direct.py
# We keep the prompts inline here to make the pipeline self-contained.

# SOP_v3 prompts: per ADR-0007 (clean output). v3 design philosophy:
# - No "page numbers" requested (LLM has no page info, would hallucinate)
# - No "1) 2) 3)" enumerate (triggers markdown)
# - No "A) B) C)" sub-heading (triggers bold)
# - CRITICAL OUTPUT RULES block prohibits markdown / fake pages / filler
# - L2_scoring has explicit one-line-per-dimension exception

_SOP_V3_RULES = """
CRITICAL OUTPUT RULES (must obey):
1. Plain prose paragraphs only. NO markdown.
2. NO bold (**text**), NO headers (### / ##), NO bullets (* / -), NO numbered lists (1. / 1) / A) ).
3. NO page references. You do not have page information. Do not write "page 5", "(p.2)", "pages 4-5", etc.
4. NO preamble like "Based on the provided text" or "Here are the methods". Start directly with substantive content.
5. NO repeating the question phrasing. Start with information, not "This paper addresses...".
6. Separate paragraphs with single newline. No section labels.
"""

SOP_PROMPTS = {
    "L1_factual_background": (
        "Extract the factual background of this research paper.\n\n"
        + _SOP_V3_RULES + "\n"
        + "Cover in one continuous narrative: what problem the paper studies, what concepts are relevant, "
        + "what failure modes prior work has, what the paper aims to achieve, and how it measures success.\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
    "L1_factual_methods": (
        "Extract the methods used in this research paper.\n\n"
        + _SOP_V3_RULES + "\n"
        + "Describe in continuous prose all experimental procedures, analytical or modeling techniques, "
        + "and validation approaches. Do not group them with labels. Just describe each method as a "
        + "self-contained sentence or two of prose.\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
    "L2_interpretive_problem": (
        "Critically analyze this research paper.\n\n"
        + _SOP_V3_RULES + "\n"
        + "Write a continuous prose analysis covering: the central problem and its significance, "
        + "the hardest technical difficulties, the gap between authors' claims and supporting evidence, "
        + "and a one-sentence overall judgment of intellectual contribution. "
        + "Do not label these as separate questions; weave into flowing analysis.\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
    "L2_interpretive_scoring": (
        "Score this paper on 10 dimensions. For EACH dimension, write exactly one line:\n"
        "    dimension_name: SCORE/10. One-sentence justification.\n\n"
        "Example:\n"
        "    novelty: 7/10. Combines existing ML methods in a new application domain but no new algorithm.\n"
        "    clarity: 8/10. Figures are clean and the math is well-explained.\n\n"
        "This one-line-per-dimension format is the ONLY structured list allowed; "
        "everywhere else in your output, use plain prose.\n\n"
        + _SOP_V3_RULES + "\n"
        + "Use lowercase dimension names. No bold. No quotes around dimension names.\n\n"
        + "Dimensions: novelty, clarity, methodological rigor, empirical strength, reproducibility, "
        + "theoretical contribution, practical impact, scope appropriateness, writing quality, citation use.\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
    "L3_outline_relevance": (
        "Assess whether this paper supports any section of the provided review outline. "
        "List up to 3 sections it genuinely supports. Do not invent matches or force "
        "assignments when the paper is unrelated.\n\n"
        + _SOP_V3_RULES + "\n"
        + "If the paper does NOT support any outline section, output exactly one line "
        + "beginning with the prefix 'no_outline_match:', in the form:\n"
        + "    no_outline_match: <one-sentence reason>. Closest distant analogy: <one phrase>.\n\n"
        + "Otherwise, for each genuinely-supported section write a single prose paragraph "
        + "(3-5 sentences) explaining: which section, what specific arguments the paper "
        + "supports, and what evidence type (empirical / theoretical / review / methodology). "
        + "Do not number the sections in output; separate them with blank lines.\n\n"
        + "Review outline:\n{outline}\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
    "L4_domain_classification": (
        "Classify this research paper into one of the predefined domain labels.\n\n"
        + _SOP_V3_RULES + "\n"
        + "Output exactly TWO lines in this format. This two-line format is the ONLY "
        + "structured output allowed in your response; no other lists, no markdown, no "
        + "preamble, no trailing prose.\n\n"
        + "    primary_domain: <label>. <one-sentence justification>.\n"
        + "    secondary_domains: <label1>, <label2>. <brief reason>.\n\n"
        + "If the paper has no clear secondary domain, write the second line as:\n"
        + "    secondary_domains: none.\n\n"
        + "Valid labels (use exactly one for primary; up to two for secondary):\n"
        + "    bioprinting, hip_implant, fea_surrogate, additive_manufacturing, "
        + "tissue_engineering, biomechanics, machine_learning_general, other_medical, "
        + "other_engineering, out_of_scope.\n\n"
        + "Choose the single best primary label. Use secondary labels for clearly adjacent "
        + "domains. Use other_medical / other_engineering for in-scope but uncategorized "
        + "work; use out_of_scope only when the paper is unrelated to bioprinting, "
        + "hip implants, FEA surrogate modelling, or related biomedical/engineering topics.\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
}


# ============ L4 output parsing (ADR-0014) ============

_VALID_DOMAIN_LABELS = {
    "bioprinting", "hip_implant", "fea_surrogate", "additive_manufacturing",
    "tissue_engineering", "biomechanics", "machine_learning_general",
    "other_medical", "other_engineering", "out_of_scope",
}


def parse_l4_output(raw: str):
    """Parse L4 raw output into structured dict.

    Expected two-line shape:
        primary_domain: <label>. <justification>.
        secondary_domains: <label1>, <label2>. <reason>.   (or 'secondary_domains: none.')

    Returns dict with keys: primary, primary_justification,
    secondary (list), secondary_reason, parse_warnings (list).
    Unknown labels are kept verbatim but flagged in parse_warnings.
    """
    out = {
        "primary": None,
        "primary_justification": None,
        "secondary": [],
        "secondary_reason": None,
        "parse_warnings": [],
    }
    if not raw or not raw.strip():
        out["parse_warnings"].append("empty_output")
        return out
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        low = line.lower()
        if low.startswith("primary_domain:"):
            rest = line.split(":", 1)[1].strip()
            label, _, justification = rest.partition(".")
            label = label.strip().lower()
            out["primary"] = label or None
            out["primary_justification"] = justification.strip().rstrip(".") or None
            if label and label not in _VALID_DOMAIN_LABELS:
                out["parse_warnings"].append(f"unknown_primary_label:{label!r}")
        elif low.startswith("secondary_domains:"):
            rest = line.split(":", 1)[1].strip()
            if rest.lower().lstrip().startswith("none"):
                out["secondary"] = []
                continue
            labels_part, _, reason = rest.partition(".")
            labels = [s.strip().lower() for s in labels_part.split(",") if s.strip()]
            out["secondary"] = labels
            out["secondary_reason"] = reason.strip().rstrip(".") or None
            unknown = [l for l in labels if l not in _VALID_DOMAIN_LABELS]
            if unknown:
                out["parse_warnings"].append(f"unknown_secondary_labels:{unknown!r}")
    if out["primary"] is None:
        out["parse_warnings"].append("missing_primary_domain_line")
    return out


def derive_outline_match_status(raw: str) -> str:
    """Per ADR-0014 step 5: 'no_match' if L3 starts with 'no_outline_match:', else 'matched'."""
    if not raw or not raw.strip():
        return "unknown"
    return "no_match" if raw.lstrip().lower().startswith("no_outline_match") else "matched"


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
    """Run 6 SOP tasks (L1*2 + L2*2 + L3 outline_relevance + L4 domain_classification).

    Function name retained per ADR-0011 versioning notes; v4 prompts now live inside.
    L4 has no {outline} placeholder; str.format silently ignores the unused kwarg.
    """
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
# ADR-0014: L3 key renamed personal_relevance -> outline_relevance; raw output
# still stored under the personal_relevance block + sop_l3_raw field for
# backward-compatibility with downstream consumers that read that path.
SOP_TO_SCHEMA = [
    ("L1_factual_background",  "factual",            "sop_l1_background_raw", None),
    ("L1_factual_methods",     "factual",            "methods_raw",           None),
    ("L2_interpretive_problem","interpretive",       "core_problem_raw",
        "kept under interpretive per sop_v2 naming; ADR-0003 lists under factual"),
    ("L2_interpretive_scoring","interpretive",       "scoring_10_dim_local",
        "D-grade local LLM output; pending Path C web chat review"),
    ("L3_outline_relevance",   "personal_relevance", "sop_l3_raw",
        "L3 raw output; key renamed from L3_personal_relevance per ADR-0014"),
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

    # ============ ADR-0014 additions ============
    # factual.l4_raw                : raw LLM output for L4
    # factual.domain_classification : parsed {primary, secondary, ...}
    # interpretive.outline_match_status : derived from L3 prefix
    l4_entry = sop_results.get("L4_domain_classification")
    l4_raw = l4_entry["answer"] if (l4_entry and l4_entry.get("ok")) else None
    l4_parsed = parse_l4_output(l4_raw) if l4_raw else None

    md["factual"]["l4_raw"] = {
        "value": l4_raw,
        "_meta": {
            "produced_by": "qwen2.5-14b-32k",
            "prompt_version": PROMPT_VERSION,
            "produced_at": produced_at,
            "reviewed_by": None,
            "reviewed_at": None,
            "evidence": [],
            "note": "L4 raw output; populated by ADR-0014 SOP_v4",
            "failed": l4_entry is None or not l4_entry.get("ok"),
            "error":  None if (l4_entry and l4_entry.get("ok")) else (
                (l4_entry or {}).get("error", "missing")),
        },
    }
    md["factual"]["domain_classification"] = {
        "value": l4_parsed,
        "_meta": {
            "produced_by": "parse_l4_output",
            "prompt_version": PROMPT_VERSION,
            "produced_at": produced_at,
            "reviewed_by": None,
            "reviewed_at": None,
            "evidence": [],
            "note": "Parsed from L4 raw; primary + secondary labels per ADR-0014",
        },
    }

    l3_entry = sop_results.get("L3_outline_relevance")
    l3_raw = l3_entry["answer"] if (l3_entry and l3_entry.get("ok")) else None
    md["interpretive"]["outline_match_status"] = {
        "value": derive_outline_match_status(l3_raw) if l3_raw else "unknown",
        "_meta": {
            "produced_by": "derive_outline_match_status",
            "prompt_version": PROMPT_VERSION,
            "produced_at": produced_at,
            "reviewed_by": None,
            "reviewed_at": None,
            "evidence": [],
            "note": "Derived from L3 prefix: 'no_match' if L3 starts with 'no_outline_match:', else 'matched'",
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
