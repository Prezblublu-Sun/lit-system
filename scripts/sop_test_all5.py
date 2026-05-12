"""
Week 1 Day 2 - SOP 全黄金集
对 5 篇论文逐一跑完整 5 类 SOP, 产出每篇的结构化资料
配置: qwen2.5-14b-8k + nomic-embed-text (复用 v7 索引)

特性:
- 续跑: 已成功的不重跑
- 单篇失败不影响其他
- 增量写盘 (sop_all5.json)
"""
import os
import sys
import json
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = PROJECT_ROOT / "corpus" / "golden"
INDEX_DIR = PROJECT_ROOT / "index" / "paperqa_week0"
RESULTS_DIR = PROJECT_ROOT / "results"
OUTLINE_FILE = PROJECT_ROOT / "corpus" / "outline" / "review_outline.md"
OUT_FILE = RESULTS_DIR / "sop_all5.json"

OUTLINE_TEXT = OUTLINE_FILE.read_text()[:3500]
print(f"[setup] 纲要长度: {len(OUTLINE_TEXT)} 字符 (截到 8000 喂给 LLM)")

os.environ["OPENAI_API_KEY"] = "ollama-placeholder"
LLM = "ollama/qwen2.5-14b-8k"
EMBED = "ollama/nomic-embed-text"

local_llm_config = {
    "model_list": [{
        "model_name": LLM,
        "litellm_params": {
            "model": LLM,
            "api_base": "http://localhost:11434",
            "timeout": 600,
        },
    }]
}

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
        rebuild_index=False,
        index=IndexSettings(
            paper_directory=str(PAPERS_DIR),
            index_directory=str(INDEX_DIR),
            recurse_subdirectories=False,
            use_absolute_paper_directory=True,
            sync_with_paper_directory=False,
        ),
    ),
)

PAPERS = [
    ("P1", "AI for biofabrication"),
    ("P2", "AI-driven 3D bioprinting for regenerative medicine"),
    ("P3", "Robotic-assisted automated in situ bioprinting"),
    ("P4", "Self-driving bioprinting laboratories"),
    ("P5", "The Synergy of Artificial Intelligence and 3D Bioprinting"),
]

def build_tasks(phrase):
    return [
        ("L1_factual_background", "类 1 factual: 背景",
         f"Focus only on the paper containing the phrase: '{phrase}'. "
         f"Extract these factual fields, write each as 1-2 sentences with verbatim quote and page: "
         f"1) research_background, 2) core_concepts (list 3-5), 3) common_pitfalls or failure modes, "
         f"4) design_objectives, 5) evaluation_metrics. "
         f"If the paper is not found, say 'PAPER NOT FOUND' clearly."),

        ("L1_factual_methods", "类 1 factual: 方法清单",
         f"Focus only on the paper containing the phrase: '{phrase}'. "
         f"List methods in 3 categories: "
         f"A) experimental methods, B) analytical/modeling methods, C) validation methods. "
         f"For each method give name + 1-sentence purpose + page. "
         f"If paper not found, say 'PAPER NOT FOUND'."),

        ("L2_interpretive_problem", "类 2 interpretive: 问题与难题",
         f"Focus only on the paper containing the phrase: '{phrase}'. "
         f"Answer 4 parts: 1) Most central problem and why it matters. "
         f"2) 2-3 hardest technical difficulties and why hard. "
         f"3) What did authors CLAIM vs what evidence ACTUALLY supports? Gaps? "
         f"4) One-sentence judgment of intellectual contribution. "
         f"If paper not found, say 'PAPER NOT FOUND'."),

        ("L2_interpretive_scoring", "类 2 interpretive: 10 维评分",
         f"Focus only on the paper containing the phrase: '{phrase}'. "
         f"Score 1-5 on these 10 dims with 1-sentence justification each: "
         f"(1) problem_importance, (2) clarity, (3) literature_positioning, "
         f"(4) methodological_soundness, (5) novelty, (6) evidence_strength, "
         f"(7) analytical_depth, (8) limitation_acknowledgment, (9) writing_quality, "
         f"(10) inspirational_value. "
         f"Sum out of 50 + position label: intensive_read / supporting / supplementary / low. "
         f"If paper not found, say 'PAPER NOT FOUND'."),

        ("L3_personal_relevance", "类 3 personal: 综述定位",
         f"Focus only on the paper containing the phrase: '{phrase}'. "
         f"I am writing a book chapter, outline below:\n"
         f"---OUTLINE START---\n{OUTLINE_TEXT}\n---OUTLINE END---\n"
         f"Answer: 1) Which section (e.g. X.3.2.1) does this paper best support and why? "
         f"2) Which 1-2 specific arguments in my outline could it provide evidence for? "
         f"3) Single biggest writing/research insight to borrow. "
         f"Be specific - cite outline section + paper page. "
         f"If paper not found, say 'PAPER NOT FOUND'."),
    ]

def run_one(question_text):
    t0 = time.time()
    try:
        answer = ask(question_text, settings=settings)
        return {
            "ok": True,
            "duration_sec": round(time.time() - t0, 1),
            "answer": answer.session.formatted_answer,
        }
    except Exception as e:
        return {
            "ok": False,
            "duration_sec": round(time.time() - t0, 1),
            "error": str(e)[:500],
        }

# 续跑: 读已有 JSON, 跳过已成功的 (paper_id, task_id) 组合
if OUT_FILE.exists():
    print(f"读取已有 {OUT_FILE}")
    results = json.loads(OUT_FILE.read_text())
else:
    results = {
        "config": {
            "model": LLM,
            "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "papers": {},  # {pid: {task_id: result}}
    }

# 补 P5 的现有数据(从 sop_test_p5.json 拷过来,避免重跑)
p5_existing = RESULTS_DIR / "sop_test_p5.json"
if p5_existing.exists() and "P5" not in results["papers"]:
    print("从 sop_test_p5.json 复制 P5 现有结果, 避免重跑")
    p5_data = json.loads(p5_existing.read_text())
    results["papers"]["P5"] = {}
    task_id_map = {
        "类 1 (factual): 提取背景知识": "L1_factual_background",
        "类 1 (factual): 提取方法清单": "L1_factual_methods",
        "类 2 (interpretive): 核心问题与难题判断": "L2_interpretive_problem",
        "类 2 (interpretive): 10 维评分": "L2_interpretive_scoring",
        "类 3 (personal_relevance): 综述定位": "L3_personal_relevance",
    }
    for t in p5_data["tasks"]:
        tid = task_id_map.get(t["label"]) or t.get("task_id")
        if tid:
            results["papers"]["P5"][tid] = {
                "ok": t["ok"],
                "duration_sec": t["duration_sec"],
                "answer": t.get("answer", ""),
            }

def save():
    OUT_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))

save()

# 主循环
total = len(PAPERS) * 5
done = 0
for pid, phrase in PAPERS:
    if pid not in results["papers"]:
        results["papers"][pid] = {"_title": phrase}
    tasks = build_tasks(phrase)
    for task_id, label, prompt in tasks:
        if task_id in results["papers"][pid] and results["papers"][pid][task_id].get("ok"):
            done += 1
            print(f"[{done}/{total}] {pid} x {task_id}: skip (already done)")
            continue
        print(f"\n[{done+1}/{total}] {pid} x {task_id}: {label}")
        sys.stdout.flush()
        r = run_one(prompt)
        # 判断答案是不是 "PAPER NOT FOUND"
        if r["ok"]:
            ans_lower = r["answer"].lower()
            if "paper not found" in ans_lower or "cannot answer" in ans_lower or "no papers" in ans_lower:
                r["paper_found"] = False
            else:
                r["paper_found"] = True
        results["papers"][pid][task_id] = r
        done += 1
        status = "OK" if r["ok"] else "FAIL"
        found = " (paper found)" if r.get("paper_found") else " (PAPER NOT FOUND)" if r["ok"] else ""
        print(f"  --> {status} {r['duration_sec']}s{found}")
        sys.stdout.flush()
        save()

results["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
save()

# 总结
print("\n" + "="*70)
print("DONE - 各论文成功率")
print("="*70)
for pid, phrase in PAPERS:
    tasks = results["papers"].get(pid, {})
    real_tasks = [t for k, t in tasks.items() if not k.startswith("_")]
    ok_count = sum(1 for t in real_tasks if t.get("ok"))
    found_count = sum(1 for t in real_tasks if t.get("paper_found"))
    print(f"  {pid} ({phrase[:50]}): {ok_count}/5 跑通, {found_count}/5 找到论文")
print(f"\nOutput: {OUT_FILE}")
