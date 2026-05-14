# CLAUDE.md — lit-system

Guidance for Claude Code working in this repository. Read this before
proposing or making changes. Sources of truth: `README.md`,
`decisions/0001..0012-*.md`, `decisions/roadmap/roadmap_v2.md`. If those
conflict with this file, they win — and this file should be updated.

Companion project: `~/research-radar/` is the discovery layer that will
feed this system once the `candidates.jsonl` handshake is in place
(research-radar TODO B1). The resource boundary between the two is
locked by ADR-0012.

---

## 1. Project purpose

lit-system is a local-first **research-evidence operating system**: it
ingests PDFs into structured metadata (`metadata/P*.json`) and vector
chunks (Chroma at `assets/chroma_db/`) so the author can write reviews
backed by traceable evidence. It is not a chatbot, not a PDF manager,
not a generic RAG demo. The current real-world workload is the **RSC
bioprinting review** (124 papers, currently in an overnight `--force`
re-ingest).

---

## 2. Active versions / pipeline state

These are the live versions wired into `scripts/ingest/pipeline.py` as
of 2026-05-14. **Do not assume version names from older ADRs reflect
current code — read the constants at the top of `pipeline.py` first.**

- **Cleaning**: `CLEANING_VERSION = "v2_section_boundary_body"`
  (cleaning_v2 from ADR-0011 is active; detects body via
  `section_header` markers — start: `abstract|introduction|1\.`;
  end: `references|bibliography|acknowledgments|funding|...`).
- **SOP prompts**: `SOP_PROMPTS` in `pipeline.py` is the v3 rule-set
  (`_SOP_V3_RULES` constant; 5 tasks: `L1_factual_background`,
  `L1_factual_methods`, `L2_interpretive_problem`,
  `L2_interpretive_scoring`, `L3_personal_relevance`).
- **Chunking**: `CHUNKER_VERSION = "token_window_chunker_v3"`,
  800 tokens / 150 overlap, abstract→references auto-trim
  (`START_HEADER_RE` / `END_HEADER_RE` in `pipeline.py`).
- **Embeddings**: bge-m3 via Ollama (1024-dim, multilingual; see README).
- **LLM**: `LLM_MODEL = "qwen2.5-14b-32k"` (local Ollama only; ADR-0001
  + ADR-0012 require this — see §6).
- **Vector store**: ChromaDB at `assets/chroma_db/`, incremental
  upsert via `scripts/ingest/chroma_sync.py`.
- **Identity**: `doc_id` = first 16 hex of pdf sha256;
  `paper_id` = `P{n}` allocated by `paper_id.py`.

> ⚠️ KNOWN DRIFT: prompt_version field
>
> `pipeline.py:48` stamps `"sop_v2_qwen14b_32k"` but active prompts are
> `_SOP_V3_RULES`. Every `metadata/P*.json` written during Week 3 has a
> misleading `prompt_version` field. Awaiting decision: bump the
> constant, or keep intentionally frozen for cross-version comparison?
>
> Tracked in: TODO.md (needs to be logged)

---

## 3. Hot path — DO NOT TOUCH during overnight ingest

When an overnight ingest is running (`tmux ls` shows `overnight_*` or
`ps -ef | grep ingest.py` shows a live process), these files are the
hot path. Editing them mid-run risks corrupting in-flight papers.

- `scripts/ingest.py` — batch CLI entry, hosts the Ollama-restart
  hook (`OLLAMA_RESTART_EVERY = 10`) and DOI-collision warner.
- `scripts/ingest/pipeline.py` — single-paper pipeline (Docling →
  cleaning → DOI → SOP → metadata → chunks).
- `scripts/ingest/chroma_sync.py` — Chroma upserts; concurrent edits
  can collide with the live process holding the collection.
- `scripts/ingest/cleaning_v2.py`, `doi_extract.py`, `paper_id.py` —
  imported helpers.
- `metadata/P*.json` — written by ingest; do not hand-edit mid-run.
- `assets/chroma_db/` — live Chroma store.
- `results/ingest_log.jsonl` — append-only audit log.

Safe during ingest: anything under `decisions/`, `docs/`, `README.md`,
new files under `scripts/` that don't import the hot-path modules,
anything in `tests/`, and read-only inspection of all of the above.

**Before any code edit, run `ps -ef | grep ingest.py` and check
`tmux ls`. If overnight is alive, restrict yourself to read-only work
or net-new files.**

---

## 4. Recent decisions and active work

Read these ADRs in this order if context is fresh:

- **ADR-0001** — LLM runtime: local Qwen via Ollama (binding).
- **ADR-0003** — Literature asset schema (paper_id, doc_id, metadata layout).
- **ADR-0007** — Clean SOP output rules (filler / fake page / markdown bans).
- **ADR-0010** — Grounded extraction with citation validation
  (verbatim_quote + char_offset deferred per ADR-0011 § "Excluded
  from SOP v3").
- **ADR-0011** — cleaning_v2 + SOP_v3 implementation. The "before"
  baseline is `results/benchmark_sop_v2_baseline.json`; validation
  compares re-ingested metadata against it.
- **ADR-0012** — Resource boundary. This is a **TWO-SIDED** constraint:
    - lit-system must NOT use cloud APIs (privacy / offline posture)
    - radar must NOT use the local GPU (resource competition)

  Both directions require amending ADR-0012 first.

Active work (Week 3, as of 2026-05-14):
- Overnight `--force` re-ingest of all 124 bioprinting PDFs, started
  2026-05-13 16:23 BST. Tracked in `results/overnight_124_*.log` and
  `results/overnight_snapshots/snapshot_*.log`.
- Snapshot diff consumer landed (`scripts/diff_snapshots.py`).
  The snapshot generator itself does not yet exist — no script in
  `scripts/` references the `overnight_snapshots/` directory; the
  one existing snapshot file (`snapshot_0003.log`) appears to have
  been generated manually.
- Per `decisions/roadmap/roadmap_v2.md` Stage 1, next planned items
  are post-ingest metadata audit, tiered library generation, then
  RSC section dry-run.

---

## 5. Entry points

User-facing CLIs (all run from project root with `.venv/bin/python`):

- **Ingest one or many PDFs**:
  `python scripts/ingest.py inbox/*.pdf [--force] [--dry-run] [--no-sop]`
  This is the hot path (§3). `--force` re-ingests in place;
  `--dry-run` skips Chroma upsert; `--no-sop` skips the 5 LLM calls.
- **Scan + dedupe library**: `python scripts/scan_library.py`.
- **Classify library (4-class triage)**: `python scripts/classify_library.py`.
- **Build candidate index**: `python scripts/candidate_index_from_classification.py`.
- **Retrieve test**: `python scripts/retrieve_test_v1.py --query "..." --top 5`.
- **Benchmark metadata quality**: `python scripts/run_benchmark_v1.py`.
- **Snapshot diff**: `python scripts/diff_snapshots.py A.log B.log`.
- **Tests**: `pytest tests/` (requires `pip install -r requirements-dev.txt`).

Backups live next to their files (e.g.
`scripts/ingest/pipeline.py.backup_sop_v2_20260513`). Do not delete them
without asking.


## 6. What Claude Code should and shouldn't do in this repo

### Should

- **Investigate read-only first.** Many ad-hoc tasks here (status,
  snapshots, audits) can be done without touching the hot path.
  Phase A = read-only; Phase B = anything that writes or makes live
  calls. Default to A unless explicitly asked otherwise.
- **Check liveness before edits.** `ps -ef | grep ingest.py`,
  `tmux ls`, `ls -la results/overnight_*.log` — if overnight ingest
  is alive, treat §3 files as untouchable.
- **Draft ADRs** for substantive changes (new SOP version, schema
  bump, new pipeline stage). Place them in `decisions/00XX-<slug>.md`
  matching the existing numbering.
- **Write helper tools** that consume but do not mutate ingest
  outputs — diff tools, validators, exporters, benchmark scripts.
- **Add tests** under `tests/` following the pattern in
  `tests/test_diff_snapshots.py` (sys.path insert into `scripts/`,
  synthetic fixtures via `tmp_path`).

### Shouldn't

- **Don't edit `scripts/ingest.py` or `scripts/ingest/*.py` during
  a live overnight run.** There is no in-process rollback path if
  mid-paper state is corrupted.
- **Don't bump `CLEANING_VERSION`, `PROMPT_VERSION`, or
  `CHUNKER_VERSION` in place.** Create a new constant and prompt
  set; the old version's provenance is referenced by every existing
  `metadata/P*.json`.
- **Don't overwrite ADRs.** Iterate by adding a new ADR that
  supersedes the old one.
- **Don't propose a cloud API** (DeepSeek, OpenAI, Claude API) for
  any lit-system function. ADR-0012 makes this explicit; the
  privacy / offline posture is intentional.
- **Don't propose running Radar workload on this machine's GPU.**
  Same ADR, opposite direction.
- **Don't `git push`, force-push, amend pushed commits, or
  open/close PRs/issues** without explicit instruction.
- **Don't add runtime dependencies casually.** New entries to
  `requirements.txt` need justification; dev-only dependencies
  go in `requirements-dev.txt`.
- **Don't run `python scripts/ingest.py` without `--dry-run`** unless
  the user has explicitly asked for a live ingest. SOP calls cost
  ~75–200s each × 5 per paper, and a stray real run during an
  overnight session would collide with the live process.

---

Last reviewed: 2026-05-14.
