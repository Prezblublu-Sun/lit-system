"""
Re-extract first page from low-confidence PDFs using Docling instead of pypdf.
For those that Docling can read, re-classify with LLM.
For those Docling also fails, fall back to filename-based heuristic.

Updates library_classification.json in place.
"""
import sys
import json
import time
import requests
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.classify_library import (
    PROMPT_TEMPLATE, call_llm, parse_label
)

INBOX = ROOT / "inbox"
CLASS_FILE = ROOT / "library_classification.json"


def docling_first_page(pdf_path: Path, max_chars: int = 4500):
    """Try Docling, return first 4500 chars of markdown, or None."""
    try:
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))
        md = result.document.export_to_markdown()
        if not md or len(md.strip()) < 50:
            return None
        return md[:max_chars]
    except Exception as e:
        return None


# Filename-based heuristic for last-resort classification
def filename_heuristic(filename: str):
    """Return label based on filename keywords. Returns None if unclear."""
    n = filename.lower()
    # Normalize all separator chars to standard hyphen
    for sep in ["_", "–", "—", "‐", "‑", "−"]:
        n = n.replace(sep, "-")

    # Strong metal AM signals (these terms rarely show up outside metal AM)
    metal_strong = [
        # English process names
        "lpbf", "laser powder bed fusion", "selective laser melt", "slm",
        "directed energy deposition", "ded", "laser cladding",
        "wire arc", "waam", "electron beam melt", "ebm",
        # Chinese process names
        "粉末床熔合", "粉末床熔融", "激光选区熔化", "选区激光熔化",
        "激光直接能量沉积", "激光增材制造", "激光熔覆", "激光熔凝",
        "电子束熔化", "增材制造", "金属打印",
        # Alloy systems (English)
        "tc4", "ti-6al-4v", "ti6al4v", "niti", "ni-ti", "ni_ti",
        "incone", "inconel", "316l", "alsi10mg", "h13", "a356", "tc1",
        "feni", "fe-ni", "fe_ni", "femco", "fecoNi", "fecocrniMn",
        "cuti", "cu-ti", "cu_ti", "ti-cu", "ti_cu", "ticu",
        "alti", "al-ti", "al_ti", "ti-ni", "ti_ni", "tini",
        "invar",  # 因瓦合金
        # Alloy systems (Chinese)
        "钛合金", "镍合金", "铝合金", "铜合金", "镁合金",
        "高熵合金", "形状记忆合金", "记忆合金", "非晶合金",
        "金属间化合物", "增材制造钛", "增材制造金属",
        "镍钛", "钛镍", "因瓦合金", "因瓦",
        "镍基合金", "铁基合金", "铁合金",
        "金属材料",
        # More alloy systems
        "amorphous alloy", "amorph",
        "al-cu", "cu-ni", "sn-ni", "ti-ni", "ni-ti", "ti-cu", "cu-ti",
        "mg-zn", "mg-gd", "mg-y", "mg-al",
        "ni alloy", "ni 合金", "fe alloy", "al alloy",
        # Chinese AM
        "3d打印", "金属3d打印", "金属激光", "激光烧结", "选区激光",
        "超弹性", "包晶", "相图", "相平衡", "相变",
        "孔隙", "熔池", "凝固", "强化", "断裂行为",
    ]
    # Strong bioprinting signals
    bio_strong = [
        "bioprint", "bioink", "biofabr",
        "细胞 打印", "组织工程", "生物打印", "生物制造",
        "hydrogel print", "cell-laden",
    ]
    # Strong HIP/orthopedic
    implant_strong = [
        "hip arthroplasty", "hip implant", "femoral implant",
        "knee implant", "orthopaed", "orthoped",
        "髋关节", "膝关节", "股骨", "假体",
    ]
    # FEA/numerical
    fea_strong = [
        "finite element", "fea ", "peridyn", "comsol", "abaqus", "ansys",
        "molecular dynamics", "first principle", "dft ",
        "有限元", "近场动力学", "第一性原理", "分子动力学",
        "计算材料",
    ]

    if any(k in n for k in metal_strong):  return "metal_am"
    if any(k in n for k in bio_strong):    return "bioprinting"
    if any(k in n for k in implant_strong): return "other"  # implant clinical, mark as other (细分留待 Week 3)
    if any(k in n for k in fea_strong):    return "other"   # FEA, 同上
    return None


def main():
    classifications = json.load(open(CLASS_FILE))
    low_conf = [r for r in classifications if r["confidence"] == "low"]
    print(f"[setup] {len(low_conf)} low-confidence entries to rescue")

    by_id = {r["doc_id"]: r for r in classifications}

    docling_success = 0
    llm_reclassified = 0
    filename_fallback = 0
    still_unknown = 0
    t0 = time.time()

    for i, r in enumerate(low_conf, 1):
        doc_id = r["doc_id"]
        filename = r["filename"]
        pdf = INBOX / f"{doc_id}.pdf"

        if not pdf.exists():
            print(f"  [{i}/{len(low_conf)}] {filename[:60]}: no inbox file")
            continue

        # Step 1: Try Docling
        page = docling_first_page(pdf)
        if page:
            docling_success += 1
            prompt = PROMPT_TEMPLATE.replace("{page_text}", page)
            raw = call_llm(prompt)
            parsed = parse_label(raw)
            if parsed and "label" in parsed:
                new_label = parsed.get("label", "other")
                new_conf  = parsed.get("confidence", "low")
                new_reason = "docling-rescue: " + parsed.get("reason", "")[:100]
                by_id[doc_id]["label"] = new_label
                by_id[doc_id]["confidence"] = new_conf
                by_id[doc_id]["reason"] = new_reason
                llm_reclassified += 1
                print(f"  [{i}/{len(low_conf)}] [{new_label}|{new_conf}] (docling+LLM) {filename[:60]}")
                continue

        # Step 2: Filename heuristic fallback
        heuristic = filename_heuristic(filename)
        if heuristic:
            by_id[doc_id]["label"] = heuristic
            by_id[doc_id]["confidence"] = "medium"  # heuristic = medium, not high
            by_id[doc_id]["reason"] = f"filename-heuristic: matched {heuristic} keywords"
            filename_fallback += 1
            print(f"  [{i}/{len(low_conf)}] [{heuristic}|medium] (heuristic) {filename[:60]}")
            continue

        still_unknown += 1
        # leave as-is (other / low)
        by_id[doc_id]["reason"] = "rescue_failed: docling unreadable + no filename match"
        print(f"  [{i}/{len(low_conf)}] [?] still unknown: {filename[:60]}")

        # Periodic save
        if i % 20 == 0:
            CLASS_FILE.write_text(json.dumps(list(by_id.values()),
                                            ensure_ascii=False, indent=2))

    CLASS_FILE.write_text(json.dumps(list(by_id.values()),
                                    ensure_ascii=False, indent=2))

    elapsed = time.time() - t0
    print(f"\n{'='*60}\nRESCUE REPORT")
    print(f"  total low_conf:      {len(low_conf)}")
    print(f"  docling read OK:     {docling_success}")
    print(f"  LLM re-classified:   {llm_reclassified}")
    print(f"  filename heuristic:  {filename_fallback}")
    print(f"  still unknown:       {still_unknown}")
    print(f"  elapsed:             {elapsed:.0f}s ({elapsed/60:.1f}m)")

    # Final tally
    from collections import Counter
    all_cls = list(by_id.values())
    print(f"\n  updated full distribution:")
    by_label = Counter(r["label"] for r in all_cls)
    for k, n in by_label.most_common():
        print(f"    {k:14s} {n}")


if __name__ == "__main__":
    main()
