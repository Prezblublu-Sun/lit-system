# ADR-0012: Resource boundary — local GPU stays in lit-system, Radar uses DeepSeek API

**Status**: Accepted
**Date**: 2026-05-14
**Decision-maker**: Weikang Sun
**Cross-reference**: `research-radar/SCOPE.md` § "Resource division of labor: GPU vs API"

---

## Context

`lit-system` and `research-radar` run on the same physical machine
(`prezlinuxstation`, RTX 5060 Ti 16GB, 31GB RAM). Both are research
infrastructure for the same PhD work but serve different roles:

- `research-radar` is the daily-running **discovery layer**: scans
  arXiv/OpenAlex/PubMed for new papers, scores relevance via LLM, syncs
  to Zotero, renders an HTML digest.
- `lit-system` is the **deep-parsing / RAG layer**: ingests selected
  PDFs via Docling, extracts structured metadata via 5 SOP prompts,
  builds Chroma vector store for chapter writing.

A natural question arises: should both systems share the local GPU
(running Qwen2.5-14B via Ollama), or should Radar use a cloud LLM
(DeepSeek API) while lit-system keeps the GPU?

This ADR locks in the answer.

---

## Decision

**The local GPU is reserved exclusively for lit-system.** Radar uses
DeepSeek API for all LLM scoring (daily runs and historical backfill).

### Concrete rules

1. Radar must not run Ollama, must not generate embeddings locally,
   must not depend on the local Qwen model for any feature.
2. lit-system must not assume DeepSeek API access. Its design must
   remain viable offline (e.g., for sensitive documents or when API
   credits run out).
3. Resource borrowing in either direction requires updating BOTH this
   ADR AND `research-radar/SCOPE.md` first. Default is no sharing.

---

## Rationale

### Workload shape is asymmetric

| Aspect | Radar scoring | lit-system SOP |
|---|---|---|
| Output length | ~200 tokens | 1000-2000 tokens |
| Quality bar | classification-grade | structured prose |
| Per-paper time on local Qwen | ~30-50s | 75-200s |
| Total papers/year | ~30,000 (with backfill) | ~124 (curated) |
| Volume × time on local | infeasible (~14 days) | feasible (~21h) |

Radar's "shallow but broad" pattern fits DeepSeek-V3 (fast, batched,
classification-grade quality). lit-system's "narrow but deep" pattern
fits local Qwen (high latency per call is amortized over few papers,
structured prose benefits from local-controlled prompts).

### Cost is not a real constraint

DeepSeek API for Radar:
- Daily: ~¥0.0023/paper × ~200 papers = ~¥0.5/day
- One-time backfill: ~¥10-70 for 2024-2026 across 4 directions
- Monthly bill: ~¥15

This is negligible compared to GPU time saved for lit-system. The
"local model is free" argument ignores that GPU time is the real
scarce resource here, not API tokens.

### Asymmetric data sensitivity

Radar processes **public abstracts** from arXiv/OpenAlex/PubMed. There
is no concern about sending these to DeepSeek API.

lit-system processes **user-curated PDFs** including draft chapters,
in-progress research notes, and full-text papers acquired via Zotero.
Some of this is sensitive (unpublished work, supervisor exchanges).
Local-only processing for lit-system is a real privacy posture.

---

## Consequences

### Positive

- No GPU scheduling conflicts. lit-system overnight ingest (~16-21h)
  cannot be slowed by Radar.
- Radar can run on GitHub Actions free tier without local dependencies.
- Clear infrastructure boundary if either project is migrated, paused,
  or rewritten.
- Future contributors / Claude Code instances cannot accidentally
  propose "use local Qwen for Radar to save money" without first
  reading this ADR.

### Negative

- Radar incurs an ongoing API cost (~¥15/month). Acceptable.
- lit-system cannot batch-score 124 papers via DeepSeek to save 14h
  of overnight time. Acceptable — overnight runs happen rarely, and
  the prompt iteration speed of local control is valuable for lit-system's
  research nature.
- Two LLM environments to maintain (DeepSeek prompts in Radar,
  Qwen prompts in lit-system). Acceptable — they iterate independently.

### Exceptions (documented)

None currently. If Radar later requires local inference (e.g., for a
re-ranker that must be local for latency reasons), this ADR must be
amended FIRST, before any code change.

---

## Implementation status

This is a documentation-only ADR. No code changes required because:
- Radar already uses DeepSeek exclusively (see `pipeline/run_daily.py`)
- lit-system already uses Ollama exclusively (see `scripts/ingest/pipeline.py`)

The contribution is making the resource boundary **explicit** and
**unidirectional**, so it survives future memory loss, agent restarts,
or "optimization" proposals from LLM-generated reviews.

---

## Related ADRs

- ADR-0001: LLM runtime (local Qwen via Ollama for lit-system)
- ADR-0004: Commercial API strategy (general policy for API usage)
- `research-radar/SCOPE.md`: § "Resource division of labor: GPU vs API"
  (mirror document with same constraint, written from Radar's side)
