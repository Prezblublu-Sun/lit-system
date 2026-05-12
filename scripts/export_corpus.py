"""
Week 1 Day 2 - export literature corpus as single large markdown
合并 25 个 SOP 答案 + Mode B 5 个跨文档答案 + 综述纲要 → 一份大 md

输出: assets/export/literature_corpus_v1.md
设计目标: 自包含, 适合贴到 Claude.ai / ChatGPT / Gemini 网页对话
"""
import json
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOP_FILE = PROJECT_ROOT / "results" / "sop_v2.json"
EVAL_FILE = PROJECT_ROOT / "results" / "evaluation.json"
OUTLINE_FILE = PROJECT_ROOT / "corpus" / "outline" / "review_outline.md"
OUT_DIR = PROJECT_ROOT / "assets" / "export"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "literature_corpus_v1.md"

# 任务标签 -> 区段标题映射
TASK_HEADINGS = {
    "L1_factual_background": "Background, concepts, pitfalls, objectives, metrics",
    "L1_factual_methods": "Methods inventory (experimental / analytical / validation)",
    "L2_interpretive_problem": "Core problem, difficulties, claims-vs-evidence, contribution",
    "L2_interpretive_scoring": "10-dimension scoring",
    "L3_personal_relevance": "Mapping to my book chapter outline",
}

TASK_ORDER = [
    "L1_factual_background",
    "L1_factual_methods",
    "L2_interpretive_problem",
    "L2_interpretive_scoring",
    "L3_personal_relevance",
]

# ---------- 1. 读所有数据 ----------
sop = json.loads(SOP_FILE.read_text())
papers = sop["papers"]

try:
    eval_data = json.loads(EVAL_FILE.read_text())
    cross_paper = eval_data.get("mode_B_cross_paper", [])
except Exception:
    cross_paper = []

outline_full = OUTLINE_FILE.read_text()
# 取纲要前 3500 字符(同 SOP 跑时用的)
outline_snip = outline_full[:3500]

# ---------- 2. 构建 markdown ----------
lines = []
lines.append("# Literature Corpus v1")
lines.append("")
lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
lines.append(f"**Source**: Local Ollama (qwen2.5-14b-32k) + 5 papers + book chapter outline")
lines.append(f"**Papers covered**: {len(papers)}")
lines.append("")
lines.append("This file is the consolidated output of:")
lines.append("- 5 systematic-reading-protocol (SOP) analyses per paper × 5 papers = 25 tasks")
lines.append("- 5 cross-paper synthesis answers (Mode B, from PaperQA2 evaluation)")
lines.append("- Compact extract of my book chapter outline")
lines.append("")
lines.append("Use this file by pasting into Claude / ChatGPT / Gemini web chat to discuss these papers in context of the book chapter.")
lines.append("")
lines.append("---")
lines.append("")

# === Section A: Book chapter outline ===
lines.append("## A. Book chapter outline (compact)")
lines.append("")
lines.append("```")
lines.append(outline_snip)
lines.append("```")
lines.append("")
lines.append("---")
lines.append("")

# === Section B: per-paper SOP analyses ===
lines.append("## B. Per-paper analyses")
lines.append("")
for pid in ["P1", "P2", "P3", "P4", "P5"]:
    if pid not in papers:
        continue
    p = papers[pid]
    title = p.get("_title", "(no title)")
    filename = p.get("_filename", "")
    pdf_chars = p.get("_pdf_chars", "?")

    lines.append(f"### {pid}: {title}")
    lines.append("")
    lines.append(f"**Filename**: `{filename}`")
    lines.append(f"**Source text chars**: {pdf_chars}")
    lines.append("")
    for task_id in TASK_ORDER:
        if task_id not in p:
            continue
        t = p[task_id]
        if not t.get("ok"):
            lines.append(f"#### {TASK_HEADINGS[task_id]}")
            lines.append("")
            lines.append(f"*(task failed: {t.get('error', 'unknown')[:120]})*")
            lines.append("")
            continue
        ans = t["answer"].strip()
        lines.append(f"#### {TASK_HEADINGS[task_id]}")
        lines.append("")
        lines.append(ans)
        lines.append("")
    lines.append("---")
    lines.append("")

# === Section C: cross-paper synthesis ===
if cross_paper:
    lines.append("## C. Cross-paper synthesis (Mode B answers)")
    lines.append("")
    lines.append("These are answers that PaperQA2 generated synthesizing across all 5 papers.")
    lines.append("Useful for the book chapter intro and conclusion sections.")
    lines.append("")
    for r in cross_paper:
        qid = r.get("qid", "?")
        label = r.get("label", "")
        ans = r.get("answer", "").strip()
        # answer 里头部有 "Question: ..." 的回声, 去掉
        if "Answer:" in ans:
            ans = ans.split("Answer:", 1)[1].strip()
        elif ans.startswith("Question:"):
            # 跳过 question 那一段
            parts = ans.split("\n\n", 1)
            if len(parts) > 1:
                ans = parts[1].strip()
        lines.append(f"### {qid}: {label}")
        lines.append("")
        lines.append(ans)
        lines.append("")
    lines.append("---")
    lines.append("")

# === Section D: usage prompt template ===
lines.append("## D. How to use this file with web chat")
lines.append("")
lines.append("Suggested opening message after pasting this corpus:")
lines.append("")
lines.append("```")
lines.append("This is my literature corpus for a book chapter on AI-driven bioprinting.")
lines.append("Section A is my chapter outline. Section B has per-paper analyses (5 papers).")
lines.append("Section C has cross-paper synthesis.")
lines.append("")
lines.append("Please help me with the following task:")
lines.append("  [your specific question, e.g. 'draft section X.3.2 using P1 and P3']")
lines.append("")
lines.append("Rules:")
lines.append("- Cite papers as P1-P5, not by author")
lines.append("- Use page numbers from the analyses, don't invent")
lines.append("- If you need information not in this corpus, say so")
lines.append("- Match the academic tone of the outline")
lines.append("```")
lines.append("")

# ---------- 3. 写盘 ----------
content = "\n".join(lines)
OUT_FILE.write_text(content)

# ---------- 4. 统计 ----------
chars = len(content)
words = len(content.split())
# 粗估 token: 英文 ~4 char/token, markdown 符号多一些
est_tokens = chars // 4

print(f"输出: {OUT_FILE}")
print(f"字符: {chars:,}")
print(f"词数: {words:,}")
print(f"估算 token: ~{est_tokens:,}")
print()
print("适配性检查:")
print(f"  ChatGPT (128K):     {'OK' if est_tokens < 100000 else 'TOO LARGE'} ({est_tokens/128000*100:.0f}% 容量)")
print(f"  Claude (200K 默认): {'OK' if est_tokens < 170000 else 'TOO LARGE'} ({est_tokens/200000*100:.0f}% 容量)")
print(f"  Gemini (1M):        {'OK' if est_tokens < 800000 else 'TOO LARGE'} ({est_tokens/1000000*100:.0f}% 容量)")
