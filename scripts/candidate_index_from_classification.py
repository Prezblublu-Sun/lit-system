#!/usr/bin/env python3
"""
candidate_index_from_classification.py

把 library_classification.json (920 unique PDFs, 4 类已分) 
转成 per-domain candidate index CSV.

按 ADR-0008 Candidate Index Before Full Ingest, 这是 lit-system 引入 Layer 0
(Literature Acquisition Layer) 的第一步.

- bioprinting 124  -> ingest_status=ingested (or in_progress, 让 ingest.py 决定)
- metal_am   515   -> ingest_status=candidate, priority=B default
- other      281   -> ingest_status=candidate, priority=C default

输出 results/candidates/:
  bioprinting_candidate_index.csv
  metal_am_candidate_index.csv
  other_candidate_index.csv

字段 (per ADR-0008):
  paper_id        CAND-{n} or P{n} if already ingested
  doc_id          sha256[:16]
  title           暂用 filename (后续 ingest 时被真 title 替代)
  authors         (空, 后续填)
  year            (空, 后续填)
  doi             (空, 后续 CrossRef 填)
  abstract        (空)
  domain          bioprinting | metal_am | other
  theme           (空, 待人工细化)
  priority        A | B | C (默认按 domain 给, 待人工细化)
  why_relevant    LLM 分类时的 reason
  confidence      LLM 分类置信度 (high/medium/low/unknown)
  pdf_status      have (因为已在 inbox)
  ingest_status   candidate / ingested / in_progress
  source          local_library_2026_05_11 (本次大库上传)
  added_at        2026-05-12 (本次 candidate index 创建日期)
  notes           (空)
"""

import json
import csv
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "lit-system"
CLS_FILE = ROOT / "library_classification.json"
CAND_DIR = ROOT / "results" / "candidates"
META_DIR = ROOT / "metadata"

# 已 ingest 的 doc_id -> paper_id 映射 (从现有 metadata 读取)
def load_ingested_papers():
    """Scan metadata/P*.json, return {doc_id: paper_id} for all ingested papers."""
    mapping = {}
    for p in sorted(META_DIR.glob("P*.json")):
        try:
            d = json.loads(p.read_text())
            doc_id = d["id_block"]["doc_id"]
            paper_id = d["_paper_id"]
            mapping[doc_id] = paper_id
        except Exception as e:
            print(f"  WARN: cannot read {p.name}: {e}", file=sys.stderr)
    return mapping

# 默认 priority 按 domain
DEFAULT_PRIORITY = {
    "bioprinting": "B",   # 默认中等, 实际 ingest 后人工调
    "metal_am": "B",      # 中等, 待写金属 AM 综述时筛
    "other": "C",         # 低, 多为教材 / 学位论文 / 低相关
}

# Output schema (per ADR-0008)
FIELDS = [
    "paper_id", "doc_id", "title", "authors", "year", "doi", "abstract",
    "domain", "theme", "priority", "why_relevant", "confidence",
    "pdf_status", "ingest_status", "source", "added_at", "notes"
]

def main():
    if not CLS_FILE.exists():
        print(f"ERROR: {CLS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    classification = json.loads(CLS_FILE.read_text())
    ingested_map = load_ingested_papers()
    print(f"Loaded {len(classification)} classified PDFs")
    print(f"Found {len(ingested_map)} already-ingested papers in metadata/")
    print()

    CAND_DIR.mkdir(parents=True, exist_ok=True)

    # 按 domain 分组
    by_domain = {"bioprinting": [], "metal_am": [], "other": []}
    for rec in classification:
        label = rec.get("label", "other")
        if label == "both":
            label = "bioprinting"  # both 归 bioprinting (历史决策: 0 篇实际 both)
        if label not in by_domain:
            label = "other"
        by_domain[label].append(rec)

    now = datetime.now().strftime("%Y-%m-%d")
    cand_counter = 1  # CAND-1, CAND-2, ... 全局递增

    total_written = {"bioprinting": 0, "metal_am": 0, "other": 0}
    total_ingested = {"bioprinting": 0, "metal_am": 0, "other": 0}

    for domain, records in by_domain.items():
        out_csv = CAND_DIR / f"{domain}_candidate_index.csv"
        rows = []
        for rec in records:
            doc_id = rec["doc_id"]
            filename = rec["filename"]
            confidence = rec.get("confidence", "unknown")
            reason = rec.get("reason", "")

            # 决定 paper_id 和 ingest_status
            if doc_id in ingested_map:
                paper_id = ingested_map[doc_id]
                ingest_status = "ingested"
                total_ingested[domain] += 1
            else:
                paper_id = f"CAND-{cand_counter:04d}"
                cand_counter += 1
                ingest_status = "candidate"

            row = {
                "paper_id":      paper_id,
                "doc_id":        doc_id,
                "title":         filename,  # placeholder, ingest 后被真 title 替代
                "authors":       "",
                "year":          "",
                "doi":           "",
                "abstract":      "",
                "domain":        domain,
                "theme":         "",
                "priority":      DEFAULT_PRIORITY[domain],
                "why_relevant":  reason[:500],  # 截断防止 CSV 单行过长
                "confidence":    confidence,
                "pdf_status":    "have",  # 都已在 inbox/
                "ingest_status": ingest_status,
                "source":        "local_library_2026_05_11",
                "added_at":      now,
                "notes":         "",
            }
            rows.append(row)
            total_written[domain] += 1

        # 写 CSV
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows)
        print(f"  {domain:12s} -> {out_csv.name}: {len(rows)} rows "
              f"({total_ingested[domain]} ingested, {len(rows) - total_ingested[domain]} candidate)")

    print()
    print(f"Total written: {sum(total_written.values())} rows")
    print(f"  bioprinting:  {total_written['bioprinting']:4d} "
          f"(ingested: {total_ingested['bioprinting']}, candidate: {total_written['bioprinting'] - total_ingested['bioprinting']})")
    print(f"  metal_am:     {total_written['metal_am']:4d} "
          f"(ingested: {total_ingested['metal_am']}, candidate: {total_written['metal_am'] - total_ingested['metal_am']})")
    print(f"  other:        {total_written['other']:4d} "
          f"(ingested: {total_ingested['other']}, candidate: {total_written['other'] - total_ingested['other']})")
    print()
    print(f"Output dir: {CAND_DIR}")

if __name__ == "__main__":
    main()
