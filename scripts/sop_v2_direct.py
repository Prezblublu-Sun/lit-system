"""
Week 1 Day 2 - SOP v2 (绕过 paper-qa, 直接 Ollama)
- 用 pypdf 提取 PDF 全文
- 32K context 装整篇论文
- 直接调 Ollama HTTP API
- 5 类 SOP × 5 篇 = 25 任务
"""
import os
import sys
import json
import time
import requests
from pathlib import Path
from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = PROJECT_ROOT / "corpus" / "golden"
RESULTS_DIR = PROJECT_ROOT / "results"
OUTLINE_FILE = PROJECT_ROOT / "corpus" / "outline" / "review_outline.md"
OUT_FILE = RESULTS_DIR / "sop_v2.json"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

LLM_MODEL = "qwen2.5-14b-32k"
OLLAMA_URL = "http://localhost:11434/api/generate"

# 纲要精简到 3500 字符
OUTLINE_TEXT = OUTLINE_FILE.read_text()[:3500]
print(f"[setup] 纲要长度: {len(OUTLINE_TEXT)} 字符")

# 5 篇黄金集 - 用 PDF 文件名直接定位
PAPERS = [
    ("P1", "AI for biofabrication", "AI for bioprinting.pdf"),
    ("P2", "AI-driven 3D bioprinting for regenerative medicine", "review for regenerative medicine 2025.pdf"),
    ("P3", "Robotic-assisted automated in situ bioprinting", "review robotic bioprinting 2022.pdf"),
    ("P4", "Self-driving bioprinting laboratories", "review self-driving 2026.pdf"),
    ("P5", "The Synergy of Artificial Intelligence and 3D Bioprinting", "review AI and Bioprinting great 2026.pdf"),
]


def extract_pdf_text(pdf_path: Path, max_chars: int = 60000) -> str:
    """提取 PDF 全文, 截到 max_chars 避免超 32K context (约 24K tokens)"""
    reader = PdfReader(str(pdf_path))
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
            pages.append(f"\n[Page {i+1}]\n{text}")
        except Exception as e:
            pages.append(f"\n[Page {i+1} EXTRACTION ERROR: {e}]\n")
    full = "".join(pages)
    if len(full) > max_chars:
        # 保留前 2/3 + 后 1/3 (intro/method 在前, conclusion 在后)
        cut = (max_chars * 2) // 3
        tail = max_chars - cut
        full = full[:cut] + "\n\n[...content trimmed...]\n\n" + full[-tail:]
    return full


def build_prompt(paper_text: str, paper_id: str, paper_title: str, task_label: str, task_question: str) -> str:
    return f"""You are a research assistant. Read the following paper and answer the question precisely with page citations.

==========PAPER START ({paper_id}: {paper_title})==========
{paper_text}
==========PAPER END==========

QUESTION ({task_label}):
{task_question}

Answer in English. Cite page numbers using format (page N). Be specific, do not summarize generically."""


def build_tasks(paper_title: str):
    return [
        ("L1_factual_background", "类 1 factual: 背景",
         "Extract these factual fields, each 1-2 sentences with verbatim quote and page: "
         "1) research_background, 2) core_concepts (list 3-5), 3) common_pitfalls or failure modes, "
         "4) design_objectives, 5) evaluation_metrics."),

        ("L1_factual_methods", "类 1 factual: 方法清单",
         "List methods in 3 categories: A) experimental methods, "
         "B) analytical/modeling methods, C) validation methods. "
         "For each method: name + 1-sentence purpose + page."),

        ("L2_interpretive_problem", "类 2 interpretive: 问题与难题",
         "Answer 4 parts: 1) Most central problem and why it matters. "
         "2) 2-3 hardest technical difficulties and why they are hard. "
         "3) What did the authors CLAIM vs what evidence ACTUALLY supports? Gaps? "
         "4) One-sentence judgment of intellectual contribution."),

        ("L2_interpretive_scoring", "类 2 interpretive: 10 维评分",
         "Score 1-5 on these 10 dimensions with 1-sentence justification: "
         "(1) problem_importance, (2) clarity, (3) literature_positioning, "
         "(4) methodological_soundness, (5) novelty, (6) evidence_strength, "
         "(7) analytical_depth, (8) limitation_acknowledgment, (9) writing_quality, "
         "(10) inspirational_value. "
         "End with sum/50 and position label: intensive_read / supporting / supplementary / low."),

        ("L3_personal_relevance", "类 3 personal: 综述定位",
         f"I am writing a book chapter, outline below:\n"
         f"---OUTLINE START---\n{OUTLINE_TEXT}\n---OUTLINE END---\n"
         f"Answer: 1) Which section (e.g. X.3.2.1) does this paper best support and why? "
         f"2) Which 1-2 specific arguments in my outline could it provide evidence for? "
         f"3) Single biggest writing/research insight to borrow. "
         f"Be specific - cite outline section + paper page."),
    ]


def call_ollama(prompt: str, timeout: int = 600) -> dict:
    """直接调 Ollama generate API"""
    t0 = time.time()
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1, "num_ctx": 32768},
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "ok": True,
            "duration_sec": round(time.time() - t0, 1),
            "answer": data.get("response", ""),
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": data.get("eval_count", 0),
        }
    except Exception as e:
        return {
            "ok": False,
            "duration_sec": round(time.time() - t0, 1),
            "error": str(e)[:500],
        }


# 续跑: 读已有 JSON
if OUT_FILE.exists():
    print(f"读取已有 {OUT_FILE}")
    results = json.loads(OUT_FILE.read_text())
else:
    results = {
        "config": {
            "model": LLM_MODEL,
            "approach": "direct Ollama API, no paper-qa agent",
            "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "papers": {},
    }


def save():
    OUT_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))


save()

# 主循环
total = len(PAPERS) * 5
done = 0
for pid, title, filename in PAPERS:
    if pid not in results["papers"]:
        results["papers"][pid] = {"_title": title, "_filename": filename}

    # 提取 PDF 文本(每篇只提取一次)
    if "_pdf_text" not in results["papers"][pid]:
        pdf_path = PAPERS_DIR / filename
        if not pdf_path.exists():
            print(f"[FATAL] {pid} 找不到 PDF: {pdf_path}")
            continue
        print(f"\n[{pid}] 提取 PDF 文本: {filename}")
        text = extract_pdf_text(pdf_path)
        print(f"      提取了 {len(text)} 字符 (~{len(text)//4} tokens)")
        results["papers"][pid]["_pdf_chars"] = len(text)
        save()
        sys.stdout.flush()
    else:
        text = None  # 已记录字符数, 但每次跑都要重新提取(没缓存进 JSON)
        pdf_path = PAPERS_DIR / filename
        text = extract_pdf_text(pdf_path)

    tasks = build_tasks(title)
    for task_id, label, task_question in tasks:
        if task_id in results["papers"][pid] and results["papers"][pid][task_id].get("ok"):
            done += 1
            print(f"[{done}/{total}] {pid} x {task_id}: skip (already done)")
            continue
        print(f"\n[{done+1}/{total}] {pid} x {task_id}: {label}")
        sys.stdout.flush()
        prompt = build_prompt(text, pid, title, label, task_question)
        r = call_ollama(prompt)
        results["papers"][pid][task_id] = r
        done += 1
        status = "OK" if r["ok"] else "FAIL"
        tokens = f"{r.get('prompt_tokens', 0)}p/{r.get('completion_tokens', 0)}c" if r["ok"] else ""
        print(f"  --> {status} {r['duration_sec']}s {tokens}")
        if r["ok"]:
            preview = r["answer"][:200].replace("\n", " ")
            print(f"      preview: {preview}...")
        else:
            print(f"      error: {r.get('error', '')[:200]}")
        sys.stdout.flush()
        save()

results["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
save()

print("\n" + "="*70)
print("DONE")
print("="*70)
for pid, title, _ in PAPERS:
    tasks_data = results["papers"].get(pid, {})
    real_tasks = [k for k in tasks_data if not k.startswith("_")]
    ok_count = sum(1 for k in real_tasks if tasks_data[k].get("ok"))
    print(f"  {pid}: {ok_count}/5 成功")
print(f"\nOutput: {OUT_FILE}")
