"""
Phase 1.5: Docling 跑 5 篇黄金集
观察: 各出版社 noise 模式 / 表格图片识别率 / 耗时分布
"""
import time
import json
from pathlib import Path
from docling.document_converter import DocumentConverter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = PROJECT_ROOT / "corpus" / "golden"
OUT_DIR = PROJECT_ROOT / "assets" / "docling_test"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PAPERS = [
    ("P1", "AI for biofabrication", "AI for bioprinting.pdf"),
    ("P2", "AI-driven 3D bioprinting for regenerative medicine", "review for regenerative medicine 2025.pdf"),
    ("P3", "Robotic-assisted automated in situ bioprinting", "review robotic bioprinting 2022.pdf"),
    ("P4", "Self-driving bioprinting laboratories", "review self-driving 2026.pdf"),
    ("P5", "The Synergy of Artificial Intelligence and 3D Bioprinting", "review AI and Bioprinting great 2026.pdf"),
]

print("初始化 DocumentConverter...")
t_init = time.time()
converter = DocumentConverter()
print(f"  耗时: {time.time()-t_init:.1f}s\n")

results_summary = {}
for pid, title, filename in PAPERS:
    pdf = PAPERS_DIR / filename
    if not pdf.exists():
        print(f"[{pid}] PDF 不存在: {pdf}")
        continue

    print(f"=== {pid}: {title[:50]} ===")
    print(f"    文件: {filename}")
    print(f"    大小: {pdf.stat().st_size//1024} KB")

    t0 = time.time()
    try:
        result = converter.convert(str(pdf))
        doc = result.document
        duration = time.time() - t0

        md = doc.export_to_markdown()
        md_file = OUT_DIR / f"{pid}_docling.md"
        md_file.write_text(md)

        try:
            doc_dict = doc.export_to_dict()
            json_file = OUT_DIR / f"{pid}_docling.json"
            json_file.write_text(json.dumps(doc_dict, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"    JSON 导出失败: {e}")

        try:
            tables = list(doc.tables) if hasattr(doc, 'tables') else []
            pictures = list(doc.pictures) if hasattr(doc, 'pictures') else []
        except Exception:
            tables, pictures = [], []

        results_summary[pid] = {
            "ok": True,
            "duration_sec": round(duration, 1),
            "md_chars": len(md),
            "tables": len(tables),
            "pictures": len(pictures),
            "md_first_300": md[:300],
            "md_last_200": md[-200:],
        }
        print(f"    解析: {duration:.1f}s, md={len(md)} 字符, 表={len(tables)}, 图={len(pictures)}\n")
    except Exception as e:
        results_summary[pid] = {
            "ok": False,
            "duration_sec": round(time.time()-t0, 1),
            "error": str(e)[:300],
        }
        print(f"    失败: {e}\n")

# 写盘
summary_file = OUT_DIR / "_summary.json"
summary_file.write_text(json.dumps(results_summary, indent=2, ensure_ascii=False))

print("="*70)
print("Docling 5 篇汇总")
print("="*70)
print(f"{'PID':<5}{'OK':<5}{'秒':<8}{'字符':<10}{'表':<5}{'图':<5}{'首 60 字':<50}")
for pid, r in results_summary.items():
    if r.get("ok"):
        first = r["md_first_300"][:60].replace("\n", " ")
        print(f"{pid:<5}OK   {r['duration_sec']:<8}{r['md_chars']:<10}{r['tables']:<5}{r['pictures']:<5}{first}")
    else:
        print(f"{pid:<5}FAIL {r['duration_sec']:<8}{r.get('error', '')[:60]}")

print(f"\n输出汇总: {summary_file}")
print(f"逐篇 md/json: {OUT_DIR}/")
