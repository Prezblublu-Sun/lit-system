"""Week 0 evaluation v2 - skip done, retry, no rebuild."""
import os
import sys
import json
import time
import traceback
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = PROJECT_ROOT / "corpus" / "golden"
INDEX_DIR = PROJECT_ROOT / "index" / "paperqa_week0"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_FILE = RESULTS_DIR / "evaluation.json"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

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

PAPERS = [
    ("P1", "AI for biofabrication"),
    ("P2", "AI-driven 3D bioprinting for regenerative medicine"),
    ("P3", "Robotic-assisted automated in situ bioprinting"),
    ("P4", "Self-driving bioprinting laboratories"),
    ("P5", "The Synergy of Artificial Intelligence and 3D Bioprinting"),
]

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

def run_one(question_text, max_retry=2):
    last_error = None
    for attempt in range(max_retry + 1):
        t0 = time.time()
        try:
            answer = ask(question_text, settings=settings)
            session = answer.session
            return {
                "ok": True,
                "duration_sec": round(time.time() - t0, 1),
                "attempts": attempt + 1,
                "question": question_text,
                "answer": session.formatted_answer,
            }
        except Exception as e:
            last_error = e
            if attempt < max_retry:
                print(f"         retry {attempt+1}/{max_retry} after error: {str(e)[:100]}")
                sys.stdout.flush()
                time.sleep(5)
            continue
    return {
        "ok": False,
        "duration_sec": round(time.time() - t0, 1),
        "attempts": max_retry + 1,
        "question": question_text,
        "error": str(last_error),
        "traceback": traceback.format_exc()[-2000:],
    }

if RESULTS_FILE.exists():
    print(f"读取已有 {RESULTS_FILE}")
    results = json.loads(RESULTS_FILE.read_text())
else:
    print(f"新建 {RESULTS_FILE}")
    results = {
        "config": {
            "llm": LLM,
            "embed": EMBED,
            "papers_dir": str(PAPERS_DIR),
            "index_dir": str(INDEX_DIR),
            "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "mode_B_cross_paper": [],
        "mode_A_per_paper": [],
    }

b_done = {r["qid"] for r in results["mode_B_cross_paper"] if r.get("ok")}
a_done = {(r["qid"], r["pid"]) for r in results["mode_A_per_paper"] if r.get("ok")}
print(f"已完成 Mode B: {sorted(b_done)}")
print(f"已完成 Mode A: {len(a_done)}/25")

def save():
    RESULTS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))

results["mode_B_cross_paper"] = [r for r in results["mode_B_cross_paper"] if r.get("ok")]
results["mode_A_per_paper"] = [r for r in results["mode_A_per_paper"] if r.get("ok")]
save()

print("\n" + "=" * 70)
print("MODE B (cross-paper)")
print("=" * 70)
for qid, label, q_text in QUESTIONS:
    if qid in b_done:
        print(f"[Mode B] {qid}: skip (already done)")
        continue
    full_q = f"{q_text} Synthesize findings across the provided papers."
    print(f"\n[Mode B] {qid}: {label}")
    sys.stdout.flush()
    r = run_one(full_q)
    r.update({"qid": qid, "label": label})
    results["mode_B_cross_paper"].append(r)
    print(f"         {'OK' if r['ok'] else 'FAIL'} {r['duration_sec']}s (attempts={r['attempts']})")
    save()

print("\n" + "=" * 70)
print("MODE A (per-paper)")
print("=" * 70)
for qid, label, q_text in QUESTIONS:
    for pid, p_title in PAPERS:
        if (qid, pid) in a_done:
            print(f"[Mode A] {qid} x {pid}: skip (already done)")
            continue
        full_q = (
            f"Focus only on the paper titled or containing the phrase: '{p_title}'. "
            f"For that specific paper, answer: {q_text} "
            f"Give a clear yes/partial/no judgment with one-sentence justification."
        )
        print(f"\n[Mode A] {qid} x {pid}: {p_title[:60]}")
        sys.stdout.flush()
        r = run_one(full_q)
        r.update({"qid": qid, "pid": pid, "label": label, "paper_title": p_title})
        results["mode_A_per_paper"].append(r)
        print(f"         {'OK' if r['ok'] else 'FAIL'} {r['duration_sec']}s (attempts={r['attempts']})")
        save()

results["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
save()

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
b_ok = sum(1 for r in results["mode_B_cross_paper"] if r.get("ok"))
a_ok = sum(1 for r in results["mode_A_per_paper"] if r.get("ok"))
print(f"Mode B success: {b_ok}/5")
print(f"Mode A success: {a_ok}/25")
print(f"Output: {RESULTS_FILE}")
