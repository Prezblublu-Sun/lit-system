"""
Week 1 Day 1 - SOP 实测
对 P5 (Robazzi 2025, The Synergy of AI and 3D Bioprinting) 跑完整 5 层 SOP
目标: 看 qwen2.5-14b-8k 在 5 类字段上的真实质量, 为 ADR-0003 提供数据
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

OUTLINE_TEXT = OUTLINE_FILE.read_text()[:8000]
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

PAPER_PHRASE = "The Synergy of Artificial Intelligence and 3D Bioprinting"

# 5 类 SOP 任务,每类一个问题。先试最少版本,可工作后再扩
SOP_TASKS = [
    ("L1_factual_background",
     "类 1 (factual): 提取背景知识",
     f"Focus only on the paper containing the phrase: '{PAPER_PHRASE}'. "
     f"Extract these factual fields from the paper, write each as 1-2 sentences: "
     f"1) research_background, 2) core_concepts (list 3-5), 3) common_pitfalls or failure modes mentioned, "
     f"4) design_objectives the authors set, 5) evaluation_metrics they used. "
     f"For each field, quote the supporting sentence with page number if possible."),

    ("L1_factual_methods",
     "类 1 (factual): 提取方法清单",
     f"Focus only on the paper containing the phrase: '{PAPER_PHRASE}'. "
     f"List the methods discussed in three categories: "
     f"A) experimental methods (e.g. specific bioprinting techniques), "
     f"B) analytical/modeling methods (e.g. specific ML algorithms), "
     f"C) validation methods (e.g. how authors validated their AI tools). "
     f"For each method, give name + 1-sentence purpose."),

    ("L2_interpretive_problem",
     "类 2 (interpretive): 核心问题与难题判断",
     f"Focus only on the paper containing the phrase: '{PAPER_PHRASE}'. "
     f"Answer in 4 parts: "
     f"1) What is the SINGLE most central problem this paper addresses? Why does it matter? "
     f"2) What are the 2-3 hardest technical difficulties identified? Why are they hard? "
     f"3) What did the authors CLAIM, and what did the evidence ACTUALLY support? Are there gaps? "
     f"4) Your one-sentence judgment of the paper's intellectual contribution."),

    ("L2_interpretive_scoring",
     "类 2 (interpretive): 10 维评分",
     f"Focus only on the paper containing the phrase: '{PAPER_PHRASE}'. "
     f"Score this paper on a 1-5 scale for each of these 10 dimensions, "
     f"with one short sentence of justification per score: "
     f"(1) problem_importance, (2) clarity_of_research_question, (3) literature_positioning, "
     f"(4) methodological_soundness, (5) novelty, (6) evidence_strength, "
     f"(7) analytical_depth, (8) limitation_acknowledgment, (9) writing_quality, "
     f"(10) inspirational_value_for_review_writing. "
     f"At the end: sum the scores out of 50 and assign a position label: "
     f"intensive_read / supporting_evidence / supplementary_reference / low_value."),

    ("L3_personal_relevance",
     "类 3 (personal_relevance): 综述定位",
     f"Focus only on the paper containing the phrase: '{PAPER_PHRASE}'. "
     f"I am writing a book chapter with this outline (truncated):\n"
     f"---OUTLINE START---\n{OUTLINE_TEXT}\n---OUTLINE END---\n"
     f"Answer: 1) Which specific section (e.g. X.3.2.1) does this paper best support? Why? "
     f"2) Which 1-2 specific arguments in my outline could this paper provide evidence for? "
     f"3) What is the single biggest writing or research insight I should borrow from this paper? "
     f"Be specific - cite the section in my outline and the page in the paper."),
]

def run_one(label, prompt):
    t0 = time.time()
    print(f"\n{'='*70}")
    print(f"[SOP] {label}")
    print(f"{'='*70}")
    sys.stdout.flush()
    try:
        answer = ask(prompt, settings=settings)
        session = answer.session
        return {
            "ok": True,
            "duration_sec": round(time.time() - t0, 1),
            "label": label,
            "prompt": prompt,
            "answer": session.formatted_answer,
        }
    except Exception as e:
        return {
            "ok": False,
            "duration_sec": round(time.time() - t0, 1),
            "label": label,
            "prompt": prompt,
            "error": str(e),
        }

results = {
    "config": {
        "model": LLM,
        "paper": "P5 - " + PAPER_PHRASE,
        "outline_chars_included": len(OUTLINE_TEXT),
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    },
    "tasks": [],
}
out_file = RESULTS_DIR / "sop_test_p5.json"

for task_id, label, prompt in SOP_TASKS:
    r = run_one(label, prompt)
    r["task_id"] = task_id
    results["tasks"].append(r)
    print(f"\n--> {r['label']} : {'OK' if r['ok'] else 'FAIL'} ({r['duration_sec']}s)")
    if r["ok"]:
        print(f"\n--- ANSWER (first 1200 chars) ---\n{r['answer'][:1200]}\n--- end snippet ---")
    else:
        print(f"\n--- ERROR ---\n{r.get('error','')[:500]}")
    sys.stdout.flush()
    out_file.write_text(json.dumps(results, indent=2, ensure_ascii=False))

results["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
out_file.write_text(json.dumps(results, indent=2, ensure_ascii=False))

print(f"\n{'='*70}")
print(f"DONE - {sum(1 for r in results['tasks'] if r['ok'])}/{len(SOP_TASKS)} 成功")
print(f"Output: {out_file}")
print(f"{'='*70}")
