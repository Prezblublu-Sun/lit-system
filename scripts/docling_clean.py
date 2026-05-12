"""
Phase 2 cleaning: content_layer == body filter
Input : assets/docling_test/P*_docling.json
Output: assets/docling_clean/{P*_clean.json, P*_clean.md, cleaning_metrics.json}
"""
import json
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "assets" / "docling_test"
OUTPUT_DIR = PROJECT_ROOT / "assets" / "docling_clean"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAPERS = ["P1", "P2", "P3", "P4", "P5"]
CLEANING_VERSION = "v1_content_layer_body"

metrics = {}

for pid in PAPERS:
    src = INPUT_DIR / f"{pid}_docling.json"
    if not src.exists():
        print(f"[skip] {pid}: {src.name} not found")
        continue

    d = json.load(open(src))
    texts = d.get("texts", [])
    before = len(texts)

    kept = [t for t in texts if t.get("content_layer") == "body"]
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

    (OUTPUT_DIR / f"{pid}_clean.json").write_text(
        json.dumps(cleaned, ensure_ascii=False, indent=2)
    )
    (OUTPUT_DIR / f"{pid}_clean.md").write_text(md_out)

    metrics[pid] = {
        "input_blocks": before,
        "kept_blocks": len(kept),
        "dropped_blocks": len(dropped),
        "drop_pct": round(100 * len(dropped) / before, 1) if before else 0,
        "md_chars": len(md_out),
        "dropped_labels": dict(Counter(t.get("label", "?") for t in dropped)),
    }
    print(f"[{pid}] {before} -> {len(kept)} blocks "
          f"(-{len(dropped)}, {metrics[pid]['drop_pct']}%), "
          f"md {len(md_out):,} chars")

(OUTPUT_DIR / "cleaning_metrics.json").write_text(
    json.dumps(metrics, ensure_ascii=False, indent=2)
)
print(f"\n[done] metrics -> {OUTPUT_DIR / 'cleaning_metrics.json'}")
