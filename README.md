# lit-system

> A local-first, research-evidence operating system for academic literature.
> Parses PDFs into structured metadata + vector chunks for retrieval-augmented
> review writing and long-term cross-domain knowledge accumulation.

**Status**: Research code, experimental. Used in production by the author for
PhD-level literature work. No support guarantees.

## What it does

- Parse PDFs end-to-end (layout, OCR, sections) via Docling
- Extract structured metadata via a 5-task local-LLM SOP (qwen2.5-14b on Ollama)
- Resolve DOIs via regex + CrossRef
- Token-window chunking with abstract-to-references auto-trim
- Embed via bge-m3 (1024-dim, multilingual)
- Persistent retrieval via Chroma
- Candidate-index layer for new-domain literature (before full ingest)
- Domain-specific schemas (bioprinting / FEA / metal AM / clinical implants)

The end product is **evidence packages** for review writing, not chatbot
answers. The author's pattern: extract locally, synthesize with web LLMs.

## Architecture

    PDF
     |
     v
    Docling parse  -->  Cleaning (content_layer=body)
     |                    |
     |                    v
     |                   LLM title extract
     |                    |
     |                    v
     |                   CrossRef DOI resolve
     |                    |
     |                    v
     |                   SOP_v2: 5 LLM tasks
     |                    |
     |                    v
     |                   metadata/P{n}.json (schema v1)
     |                    |
     |                    v
     |                   token-window chunks (800 tok / 150 overlap)
     |                    |
     |                    v
     |                   bge-m3 embed --> Chroma upsert

## Why local-first

Commercial LLMs cannot remember 1000+ papers across sessions. Vector RAG
gives traceable evidence over verbatim "trust me bro" model output. Local
extraction protects copyright-sensitive content; only structured fields and
chunk previews leave the machine.

See decisions/0004-commercial-api-strategy.md for the full split between
local extraction (this repo) and synthesis layer (web Claude/GPT chat).

## Requirements

- OS: Linux (tested Ubuntu 24.04). macOS likely works.
- Python: 3.11+
- GPU: NVIDIA 16GB+ recommended for qwen2.5-14b inference. CPU 10x slower.
- Disk: per paper ~5 MB (Docling) + ~50 KB (chunks).
- External: Ollama runtime + qwen2.5-14b + bge-m3 models.

## Quick start

    # 1. Clone & install
    git clone https://github.com/Prezblublu-Sun/lit-system.git
    cd lit-system
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # 2. Install Ollama + pull models
    # (see https://ollama.com for system install)
    ollama pull qwen2.5:14b-instruct-q5_K_M
    ollama pull bge-m3
    ollama create qwen14b-32k -f Modelfile.qwen14b-32k

    # 3. Put PDFs in library_raw/
    mkdir -p library_raw/mybooks
    cp ~/Downloads/*.pdf library_raw/mybooks/

    # 4. Scan + dedupe + create inbox/
    python scripts/scan_library.py

    # 5. Ingest one paper
    python scripts/ingest.py inbox/<doc_id>.pdf

    # 6. Batch ingest (tmux)
    tmux new-session -d -s ingest \
      "python scripts/ingest.py inbox/*.pdf 2>&1 | tee ingest.log"

    # 7. Retrieve
    python scripts/retrieve_test_v1.py --query "your topic" --top 5

See docs/USAGE.md for the full review-writing workflow.

## Project structure

    lit-system/
    |-- scripts/                 Python code
    |   |-- ingest/              Single-paper pipeline (core)
    |   |-- ingest.py            Batch CLI entry
    |   |-- scan_library.py      sha256 dedup + symlinks
    |   |-- classify_library.py  LLM 4-class triage
    |   |-- candidate_index_from_classification.py
    |   |-- retrieve_test_v1.py  Chroma retrieval test
    |   `-- ...
    |-- decisions/               ADRs + roadmap
    |   |-- 0001-0009-*.md       Architecture decisions
    |   |-- roadmap/             Long-term plan
    |   `-- inputs/              Design notes + backlog
    |-- docs/
    |   `-- USAGE.md             Review writing workflow
    |-- Modelfile.qwen14b-32k    Ollama model definition
    |-- requirements.txt
    |-- LICENSE                  MIT
    `-- README.md                You are here

See INDEX.md for a detailed file-by-file guide.

## Status and roadmap

- Phase 1 (Week 1-2, complete): single-paper pipeline + 5 golden papers
- Phase 2 (Week 2, complete): library scan + 920 unique PDFs classified
- Phase 3 (current, Week 3+): SOP prompt hardening + Schema v2 + Tier A/B/C export
- Phase 4 (Week 4-6): FEA candidate index + per-domain SOPs
- Phase 5 (Week 5+): Evidence-package export pipelines

Full roadmap: decisions/roadmap/roadmap_v2.md

## Known limitations

- SOP output cleanup pending (ADR-0007): LLM outputs currently contain
  "Based on the provided text..." prefixes.
- Docling memory leak: ~130 MB/paper GPU leak; mitigated by restarting the
  ingest process every ~40 papers.
- No tests yet. Adding pytest skeleton next.
- Bioprinting-specific only at this stage. Other domains have SOP designs
  ready but not implemented yet.

## License

MIT. See LICENSE.

## Citation

If this tool helped your research, citation is appreciated but not required.

    @software{lit_system_2026,
      author = {Sun, Weikang},
      orcid = {0009-0000-3968-2975},
      title = {lit-system: A local-first research evidence operating system},
      year = {2026},
      url = {https://github.com/Prezblublu-Sun/lit-system}
    }
