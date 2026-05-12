"""
Phase 1 验证: Docling 解析 P1
观察: 耗时 / 输出结构 / 图表数 / 显存占用
"""
import time
import json
from pathlib import Path
from docling.document_converter import DocumentConverter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF = PROJECT_ROOT / "corpus" / "golden" / "AI for bioprinting.pdf"
OUT_DIR = PROJECT_ROOT / "assets" / "docling_test"
OUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"PDF: {PDF}")
print(f"输出目录: {OUT_DIR}")
print()

print("初始化 DocumentConverter...")
t_init = time.time()
converter = DocumentConverter()
print(f"  初始化耗时: {time.time()-t_init:.1f}s")
print()

print("开始解析 P1...")
t0 = time.time()
result = converter.convert(str(PDF))
duration = time.time() - t0
print(f"解析耗时: {duration:.1f} 秒")
print()

doc = result.document
print(f"文档类型: {type(doc).__name__}")

# 导出 markdown
md = doc.export_to_markdown()
md_file = OUT_DIR / "P1_docling.md"
md_file.write_text(md)
print(f"Markdown: {md_file} ({len(md)} 字符)")

# 导出 dict
try:
    doc_dict = doc.export_to_dict()
    json_file = OUT_DIR / "P1_docling.json"
    json_file.write_text(json.dumps(doc_dict, indent=2, ensure_ascii=False))
    print(f"JSON: {json_file} ({json_file.stat().st_size:,} 字节)")
except Exception as e:
    print(f"JSON 导出失败: {e}")

# 统计结构
try:
    tables = list(doc.tables) if hasattr(doc, 'tables') else []
    pictures = list(doc.pictures) if hasattr(doc, 'pictures') else []
    print(f"\n结构元素:")
    print(f"  表格数: {len(tables)}")
    print(f"  图片数: {len(pictures)}")
except Exception as e:
    print(f"统计失败: {e}")

# Preview
print(f"\n--- markdown 头 800 字符 ---")
print(md[:800])
