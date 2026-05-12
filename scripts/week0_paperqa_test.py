"""
Week 0 · PaperQA2 冒烟测试 v3
目标:验证 paper-qa + Ollama (qwen2.5:14b + bge-m3) 全本地链路

关键修复:
- 绝对路径,避免相对路径递归扫错目录
- 显式 IndexSettings,关闭子目录递归
- use_doc_details=False,跳过 Semantic Scholar 抓取
- 索引存到项目内 index/ 目录,可清理可观察
"""
import os
import sys
from pathlib import Path

# ---------- 路径(绝对,自动从脚本位置推断项目根) ----------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = PROJECT_ROOT / "corpus" / "golden"
INDEX_DIR = PROJECT_ROOT / "index" / "paperqa_week0"

print(f"[setup] PROJECT_ROOT = {PROJECT_ROOT}")
print(f"[setup] PAPERS_DIR   = {PAPERS_DIR}")
print(f"[setup] INDEX_DIR    = {INDEX_DIR}")

# 防呆检查:论文目录必须存在且只有 5 个 PDF
if not PAPERS_DIR.exists():
    print(f"[FATAL] 论文目录不存在: {PAPERS_DIR}")
    sys.exit(1)
pdfs = list(PAPERS_DIR.glob("*.pdf"))
print(f"[setup] 找到 {len(pdfs)} 个 PDF:")
for p in pdfs:
    print(f"        - {p.name}")
if len(pdfs) == 0:
    print("[FATAL] 目录里没有 PDF")
    sys.exit(1)

INDEX_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Ollama 配置 ----------
# litellm 即使走 Ollama 也会校验 OPENAI_API_KEY,塞个假值绕过
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

# ---------- paper-qa 设置 ----------
from paperqa import Settings, ask
from paperqa.settings import AgentSettings, IndexSettings, ParsingSettings

settings = Settings(
    parsing=ParsingSettings(multimodal=False),
    paper_directory=str(PAPERS_DIR),
    use_doc_details=False,  # 跳过 Semantic Scholar / Crossref 抓取
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
            recurse_subdirectories=False,  # 只看顶层,不递归
            use_absolute_paper_directory=True,
        ),
    ),
)

# ---------- 跑一个问题 ----------
question = (
    "What are the main applications of AI in 3D bioprinting "
    "discussed in these papers? Give a concise list."
)

print(f"\n{'='*70}")
print(f"Question: {question}")
print(f"{'='*70}\n")

answer = ask(question, settings=settings)

print(f"\n{'='*70}")
print("ANSWER:")
print(f"{'='*70}")
print(answer.session.formatted_answer)
print(f"{'='*70}\n")
