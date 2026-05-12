"""
Week 0 评估脚本 · v7 配置
目标:跑两种评估方式,产出 JSON 报告,供 Week 4 决策使用

方式 B(跨文档,5 次调用):每个问题让 paper-qa 综合所有论文回答
方式 A(逐篇,25 次调用):每个问题 × 每篇论文,问 paper-qa 这一篇的情况

复用 v7 已建好的索引,不重建。
错误捕获:某个问题挂了,记录后继续,不让整个评估崩。
"""
import os
import sys
import json
import time
import traceback
from pathlib import Path

# ---------- 路径 ----------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = PROJECT_ROOT / "corpus" / "golden"
INDEX_DIR = PROJECT_ROOT / "index" / "paperqa_week0"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------- 问题集 ----------
QUESTIONS = [
    ("Q1", "AI/ML for bioink/parameter optimization",
     "Does the study use AI or machine learning to optimize bioink formulation or bioprinting parameters?"),
    ("Q2", "Real-time monitoring / in-line process control",
     "Does the study include real-time monitoring or in-line process control during bioprinting?"),
    ("Q3", "Biological validation beyond printability",
     "Does the study report biological validation beyond printability, such as cell viability, differentiation, gene expression, or tissue maturation?"),
    ("Q4", "Robotic / in situ bioprinting",
     "Does the study involve robotic-assisted or in situ bioprinting on curved, irregular, or living tissue surfaces?"),
    ("Q5", "Reproducibility / scalability / clinical translation",
     "Does the study address reproducibility, scalability, quality control, or clinical translation of bioprinted products?"),
]

# ---------- 5 篇论文的简短 ID(用来在 mode A 里指定论文) ----------
# 这些标题片段帮 paper-qa 在 mode A 里聚焦到单篇
PAPERS = [
    ("P1", "AI for biofabrication"),
    ("P2", "AI-driven 3D bioprinting for regenerative medicine"),
    ("P3", "Robotic-assisted automated in situ bioprinting"),
    ("P4", "Self-driving bioprinting laboratories"),
    ("P5", "The Synergy of Artificial Intelligence and 3D Bioprinting"),
]

# ---------- Ollama 配置 ----------
os.environ["OPENAI_API_KEY"] = "ollama-placeholder"

LLM = "ollama/qwen2.5-14b-8k"
EMBED = "ollama/nomic-embed-text"

local_llm_config = {
    "model_list": [
        {
            "model_name": LLM,
            "litellm_params": {
                "model": LLM,
                "api_base": "http://localhost:11434",
                "timeout": 600,
            },
        }
    ]
}

# ---------- paper-qa 设置(完全复用 v7) ----------
from paperqa import Settings, ask
from paperqa.settings import AgentSettings, IndexSettings, ParsingSettings

settings = Settings(
    paper_directory=str(PAPERS_DIR),
    use_doc_details=False,
    parsing=ParsingSettings(multimodal=False),
    llm=LLM,
    llm_config=local_llm_config,
    summary_llm=LLM,
    summary_llm_config=local_llm_config,
    embedding=EMBED,
    agent=AgentSettings(
        agent_llm=LLM,
        agent_llm_config=local_llm_config,
        index=IndexSettings(
            paper_directory=str(PAPERS_DIR),
            index_directory=str(INDEX_DIR),
            recurse_subdirectories=False,
            use_absolute_paper_directory=True,
        ),
    ),
)

# ---------- 辅助:把一次 ask 的结果提取成纯字典 ----------
def run_one(question_text):
    """跑一次 paper-qa,返回 dict;失败也返回 dict 含 error"""
    t0 = time.time()
    try:
        answer = ask(question_text, settings=settings)
        session = answer.session
        return {
            "ok": True,
            "duration_sec": round(time.time() - t0, 1),
            "question": question_text,
            "answer": session.formatted_answer,
            "raw_answer": session.answer if hasattr(session, "answer") else None,
            "references": getattr(session, "references", None),
        }
    except Exception as e:
        return {
            "ok": False,
            "duration_sec": round(time.time() - t0, 1),
            "question": question_text,
            "error": str(e),
            "traceback": traceback.format_exc()[-2000:],
        }

# ---------- 主流程 ----------
results = {
    "config": {
        "llm": LLM,
        "embed": EMBED,
        "papers_dir": str(PAPERS_DIR),
        "index_dir": str(INDEX_DIR),
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    },
    "mode_B_cross_paper": [],  # 5 次跨文档
    "mode_A_per_paper": [],     # 25 次逐篇
}

print("=" * 70)
print("MODE B: cross-paper synthesis (5 questions, ~5-15 min)")
print("=" * 70)

for qid, label, q_text in QUESTIONS:
    full_q = f"{q_text} Synthesize findings across the provided papers."
    print(f"\n[Mode B] {qid}: {label}")
    print(f"         {q_text}")
    sys.stdout.flush()
    r = run_one(full_q)
    r.update({"qid": qid, "label": label})
    results["mode_B_cross_paper"].append(r)
    print(f"         {'✓' if r['ok'] else '✗'} {r['duration_sec']}s")
    sys.stdout.flush()
    # 增量写盘,跑挂也不丢
    (RESULTS_DIR / "evaluation.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False)
    )

print("\n" + "=" * 70)
print("MODE A: per-paper drill-down (5 questions × 5 papers = 25, ~30-45 min)")
print("=" * 70)

for qid, label, q_text in QUESTIONS:
    for pid, p_title in PAPERS:
        full_q = (
            f"Focus only on the paper titled or containing the phrase: '{p_title}'. "
            f"For that specific paper, answer: {q_text} "
            f"Give a clear yes/partial/no judgment with one-sentence justification."
        )
        print(f"\n[Mode A] {qid} × {pid}: {p_title[:60]}")
        sys.stdout.flush()
        r = run_one(full_q)
        r.update({"qid": qid, "pid": pid, "label": label, "paper_title": p_title})
        results["mode_A_per_paper"].append(r)
        print(f"         {'✓' if r['ok'] else '✗'} {r['duration_sec']}s")
        sys.stdout.flush()
        (RESULTS_DIR / "evaluation.json").write_text(
            json.dumps(results, indent=2, ensure_ascii=False)
        )

results["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
(RESULTS_DIR / "evaluation.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False)
)

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
b_ok = sum(1 for r in results["mode_B_cross_paper"] if r["ok"])
a_ok = sum(1 for r in results["mode_A_per_paper"] if r["ok"])
print(f"Mode B success: {b_ok}/5")
print(f"Mode A success: {a_ok}/25")
print(f"Output: {RESULTS_DIR}/evaluation.json")
