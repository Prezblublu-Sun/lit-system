"""
Classify each PDF in library_index.json by reading its first page and asking the
local LLM to label as: bioprinting / metal_am / both / other.

Output: library_classification.json
        [{"doc_id": ..., "filename": ..., "domain": "bioprinting", "confidence": "high",
          "evidence": "...first page snippet..."}]

Resumable: skips already-classified entries.
"""
import sys
import json
import time
import requests
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = ROOT / "library_index.json"
CLASS_FILE = ROOT / "library_classification.json"
INBOX = ROOT / "inbox"

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL  = "qwen2.5-14b-32k"

PROMPT_TEMPLATE = """You are classifying a research paper by reading the first page (title + abstract area).

Classify into EXACTLY ONE of these labels:
- bioprinting      : ANY of these topics counts: 3D bioprinting / biofabrication / bioink / cell-laden hydrogels / tissue engineering with living cells / scaffold for cell growth / regenerative medicine / organoid / spheroid / vascularization / printing organs/tissues / stem cell printing. Even if the paper is broadly "AI for biofabrication" without specific cell details, classify as bioprinting.
- metal_am         : metal additive manufacturing / laser powder bed fusion (LPBF) / selective laser melting (SLM) / directed energy deposition (DED) / NiTi/Ti/Al/Ni/Fe alloys / metal 3D printing / metal implants / metallic biomedical implants (even if "biocompatible", these are METAL components)
- both             : substantively covers BOTH bioprinting AND metal AM as primary topics
- other            : neither (e.g. polymer-only, general ML for materials, textbook, unrelated topic)

IMPORTANT: If title mentions "bioprinting" or "biofabrication" the label is bioprinting unless the paper is actually about metal implants.

Output ONLY a JSON object on a single line:
{"label": "bioprinting"|"metal_am"|"both"|"other", "confidence": "high"|"medium"|"low", "reason": "<one short sentence>"}

First page text:
---
{page_text}
---
"""


def extract_first_page(pdf_path: Path, max_chars: int = 4500):
    """Read first few pages until we have enough text. P1 had a noisy cover
    page, so reading only page 1 misclassified it."""
    try:
        r = PdfReader(str(pdf_path))
        if not r.pages:
            return None
        out = []
        total = 0
        for page in r.pages[:3]:
            t = page.extract_text() or ""
            out.append(t)
            total += len(t)
            if total >= max_chars:
                break
        return ("\n".join(out))[:max_chars]
    except Exception as e:
        return None


def call_llm(prompt: str):
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_ctx": 8192, "temperature": 0.0},
        }, timeout=120)
        r.raise_for_status()
        return r.json().get("response", "")
    except Exception as e:
        return f"__ERROR__: {e}"


def parse_label(raw: str):
    """Find first {...} JSON in raw output. Tolerate noise around it."""
    import re
    m = re.search(r"\{[^}]*\"label\"[^}]*\}", raw, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def main():
    index = json.load(open(INDEX_FILE))
    print(f"[setup] {len(index)} papers in library_index.json")

    # Resume support
    existing = {}
    if CLASS_FILE.exists():
        for c in json.load(open(CLASS_FILE)):
            existing[c["doc_id"]] = c
        print(f"[setup] {len(existing)} already classified, will skip")

    results = list(existing.values())
    t0 = time.time()
    new_done = 0
    failures = 0

    for i, r in enumerate(index, 1):
        doc_id = r["doc_id"]
        if doc_id in existing:
            continue
        pdf = INBOX / f"{doc_id}.pdf"
        if not pdf.exists():
            print(f"  [skip] {doc_id}: no symlink in inbox")
            continue

        page = extract_first_page(pdf)
        if not page or len(page.strip()) < 50:
            results.append({
                "doc_id": doc_id, "filename": r["filename"],
                "label": "other", "confidence": "low",
                "reason": "could not extract first page text",
            })
            new_done += 1
            continue

        prompt = PROMPT_TEMPLATE.replace("{page_text}", page)
        raw = call_llm(prompt)
        parsed = parse_label(raw)

        if parsed and "label" in parsed:
            results.append({
                "doc_id": doc_id,
                "filename": r["filename"],
                "label": parsed.get("label", "other"),
                "confidence": parsed.get("confidence", "low"),
                "reason": parsed.get("reason", ""),
            })
        else:
            failures += 1
            results.append({
                "doc_id": doc_id,
                "filename": r["filename"],
                "label": "other", "confidence": "low",
                "reason": f"parse_failed: {raw[:120]}",
            })
        new_done += 1

        # Periodic save (every 25 papers) so crashes don't lose work
        if new_done % 25 == 0:
            CLASS_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2))
            elapsed = time.time() - t0
            rate = new_done / elapsed
            eta_min = (len(index) - len(existing) - new_done) / rate / 60 if rate > 0 else 0
            print(f"  [{i}/{len(index)}] done={new_done}, failures={failures}, "
                  f"rate={rate:.1f}/s, ETA {eta_min:.0f}m")

    # Final save
    CLASS_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2))

    # Summary
    from collections import Counter
    by_label = Counter(r["label"] for r in results)
    by_conf  = Counter(r["confidence"] for r in results)
    elapsed = time.time() - t0
    print(f"\n{'='*60}\nCLASSIFICATION REPORT")
    print(f"  classified: {len(results)}  (this run: {new_done})")
    print(f"  elapsed:    {elapsed:.0f}s ({elapsed/60:.1f}m)")
    print(f"  failures:   {failures}")
    print(f"\n  by label:")
    for k, n in by_label.most_common():
        print(f"    {k:14s} {n}")
    print(f"\n  by confidence:")
    for k, n in by_conf.most_common():
        print(f"    {k:14s} {n}")
    print(f"\n  saved: {CLASS_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
