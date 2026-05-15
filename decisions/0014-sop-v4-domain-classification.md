# ADR-0014: SOP_v4 — add L4 domain classification, decouple L3 from RSC-specific outline

**Status**: Accepted
**Date**: 2026-05-15
**Decision-maker**: Weikang Sun
**Supersedes-partial**: ADR-0011 (cleaning_v2 + SOP_v3 implementation)
**Cross-reference**: ADR-0009 (Domain-specific SOPs, future)

---

## Context

Current SOP_v3 has 5 prompts:
- L1_factual_background (generic)
- L1_factual_methods (generic)
- L2_interpretive_problem (generic)
- L2_interpretive_scoring (generic)
- L3_personal_relevance (RSC bioprinting outline hardcoded via `outline_text` input)

124 bioprinting papers have been ingested with SOP_v3. The library now needs to
expand to ~800 additional PDFs spanning hip_implant, FEA surrogate modelling,
additive manufacturing, and miscellaneous domains. These PDFs have no external
domain metadata — only sha256-derived filenames in `inbox/`.

Two problems with current SOP_v3 for the expanded library:

1. L3 will produce hallucinated "RSC outline matches" for non-bioprinting papers,
   because the prompt forces top-3 outline section identification regardless of
   actual relevance. A hip-implant paper will be forced to claim it supports
   bioprinting outline sections.

2. No domain field exists in the metadata schema. Without it, we cannot
   filter/route papers by domain in downstream operations (chapter_evidence,
   library_scoring per domain, batch operations).

---

## Decision

Introduce SOP_v4 with these changes:

1. **Rename L3_personal_relevance to L3_outline_relevance** (no prompt change).
   This clarifies that L3 is outline-dependent, not "personal" relevance.
   When a paper does not match the current outline (e.g., a hip-implant paper
   against RSC bioprinting outline), the prompt should produce an
   explicit "no good matches" signal rather than hallucinated assignments.

2. **Add L4_domain_classification as a new independent prompt**:
   - Input: paper text (same as other prompts)
   - Output: single line classification of the form
     `primary_domain: <label>. one-sentence justification.`
     `secondary_domains: <label1>, <label2>. brief reason.`
   - Valid labels: `bioprinting`, `hip_implant`, `fea_surrogate`,
     `additive_manufacturing`, `tissue_engineering`, `biomechanics`,
     `machine_learning_general`, `other_medical`, `other_engineering`,
     `out_of_scope`.
   - Domain taxonomy must stay short (~10 labels). Extending it later requires
     re-running L4 on the entire library.

3. **L3 outline match must include explicit "no match" handling**:
   - If no outline section is genuinely supported, output:
     `no_outline_match: <reason>. Closest distant analogy: <one phrase>.`
   - Do not force top-3 invented matches.

4. **Metadata schema additions**:
   - `factual.domain_classification` (new field, populated by L4)
   - `factual.l4_raw` (raw LLM output for L4)
   - `interpretive.outline_match_status` (`"matched" | "no_match"`, derived
     from L3 output)

---

## Rationale

### Why decouple L3 from RSC outline (vs hardcode)

The RSC bioprinting chapter is the current writing target, but lit-system is
intended to support multiple research outputs over time (thesis chapters,
journal papers, grant proposals). Tying L3 semantics to one specific outline
makes the metadata non-portable. By renaming to "outline_relevance" and
swapping the input outline file per use case, the same prompt serves multiple
chapters.

### Why domain classification is a separate prompt, not an L3 extension

A paper has at most one or two primary domains, but can support many outline
sections within a domain. Mixing them into one prompt produces ambiguous output.
Separation also lets domain classification stay stable (cached, re-used) while
outline matches change when the outline changes.

### Why not detect domain from filename / external metadata

The user's inbox is a personal PDF collection accumulated over time. Most PDFs
are sha256-hashed filenames with no external mapping. Filename-based detection
is impossible. research-radar covers only ~491 DOIs vs ~920 inbox PDFs, so it
is partial at best. Reading the paper text via L4 is the only reliable signal.

### Why add a prompt rather than skip L3 for non-bioprinting papers

Skipping L3 makes the library schema inconsistent across batches (124 papers
have L3, 800 do not). A library where some papers can answer "is this relevant
to outline X" and others cannot fail silently makes downstream tooling fragile.

Adding L4 means every paper gets both fields. The "library" becomes
self-describing: any consumer can query domain first, then outline relevance
within domain.

---

## Implementation cost

- Add L4 prompt to `pipeline.py` SOP_PROMPTS dict (~30 lines)
- Update `pipeline.run_sop_v2()` to call 6 prompts instead of 5
  (function name stays `run_sop_v2` per ADR-0011 versioning; v4 happens inside)
- Add 3 fields to `build_metadata` schema
- Update benchmark script `run_benchmark_v1.py` to check L4 cleanliness
- **Re-ingest existing 124 papers** to backfill L4 + new L3 semantics
  (~21h GPU, same overnight pattern as 2026-05-13)
- Then ingest 796 new papers with the same v4 prompts
  (~7-9 days GPU, single long tmux run or batched)

Total wall time: ~9-10 days GPU continuous (1 night for 124 re-ingest + 7-9
days for 796 new).

---

## Consequences

### Positive

- Library becomes domain-aware. `chapter_evidence` and `topic_evidence` can
  filter by `domain == "bioprinting"` to avoid contamination.
- L3 becomes portable. Next chapter outline (hip_implant, FEA, etc.) reuses
  the same prompt with a different outline file.
- Library treated uniformly across domains — no special cases in downstream
  scripts.
- Future scope (lit-system for multiple research outputs) is unblocked.

### Negative

- 124 papers must be re-ingested. Lose nothing of substance (same SOP prompts
  except L3 wording + L4 added), but consumes another overnight.
- Per-paper SOP time increases by ~20% (6 prompts vs 5).
- L4 prompt requires careful design to avoid label leakage / hallucination.
  An untested L4 may produce inconsistent labels across the library.

### Risks to manage

- **Taxonomy lock-in**: changing valid labels later forces full re-ingest.
  Mitigation: start with conservative 10-label taxonomy, allow `other_*`
  catch-all, version the taxonomy.
- **L4 confidence calibration**: papers may be on domain boundaries
  (e.g., hip_implant biomechanics paper using AM = which primary?).
  Mitigation: allow `secondary_domains` with up to 2 labels.
- **Inconsistency across re-runs**: same paper, two runs, different L4 label.
  Mitigation: use deterministic decoding (temperature=0) if not already.

---

## Open questions before implementing

1. Should L4 also output a `confidence_score` (high / medium / low)? Helps
   downstream filtering but adds prompt complexity.
2. Should the existing 124 papers be re-ingested in place, or saved to a
   versioned snapshot (`metadata_v3/`) first? The 2026-05-15 backup already
   covers this.
3. Should `out_of_scope` papers be excluded from Chroma indexing, or just
   tagged? Tagging is more flexible (future re-purposing).
4. Does L4 need a chunked approach for very long papers, like L1/L2? The
   classification signal should be in title + abstract, so probably not.

---

## Resolution of open questions

Resolved 2026-05-15 by Weikang Sun, prior to implementation kickoff.

1. **Q1 — confidence_score: NO.** L4 does not output a confidence score.
   Keeping the prompt simple reduces hallucination risk and keeps the
   two-line output format stable. If downstream filtering needs confidence
   later, it can be re-derived from `secondary_domains` count or by
   re-prompting on the subset.

2. **Q2 — re-ingest strategy: IN-PLACE.** The 124 existing papers are
   re-ingested in place, overwriting `metadata/P*.json`. The full backup
   at `backups/2026-05-15_overnight_complete/` is the read-only safety
   net; no `metadata_v3/` shadow directory is created.

3. **Q3 — `out_of_scope` Chroma indexing: TAG, DO NOT EXCLUDE.**
   `out_of_scope` papers still enter the Chroma collection. The
   `domain_classification` field on each chunk's metadata is the filter
   for downstream retrieval. This preserves future re-purposing
   (a paper currently `out_of_scope` for the bioprinting review may be
   in-scope for a later chapter).

4. **Q4 — chunked approach for L4: NO.** L4 receives the same
   `paper_text[:max_chars]` prefix as L1/L2 (60K chars). The
   classification signal is dominantly in the title and abstract, both
   well within the truncation window.

---

## Implementation kickoff

Concrete steps from 2026-05-15 implementation session (this commit
records the ADR transition; code edits land in subsequent commits):

- Backup `scripts/ingest/pipeline.py` to a timestamped sibling before edit.
- Rename `L3_personal_relevance` → `L3_outline_relevance` in
  `SOP_PROMPTS`. Add `no_outline_match: …` prefix instruction so step 5
  metadata derivation has a stable signal.
- Add `L4_domain_classification` prompt with the two-line output format
  and the 10-label taxonomy fixed in §Decision above.
- Extend `build_metadata` with `factual.domain_classification` (parsed
  primary + secondary list), `factual.l4_raw`, and
  `interpretive.outline_match_status`.
- Extend `run_benchmark_v1.py` with an L4 cleanliness check (exactly two
  lines, no markdown) and a domain-label distribution at end of report.
- Dry-run on the 5 golden papers (P1, P5, P44, P77, P117) before
  scheduling the full 124-paper overnight re-ingest.

`PROMPT_VERSION` constant in `pipeline.py` is *not* bumped in this
commit (it currently still reads `"sop_v2_qwen14b_32k"` — the known
drift documented in lit-system `CLAUDE.md` §2). A `sop_v4_*` bump
should be decided alongside the metadata audit that follows the
overnight re-ingest, when it can be done with full provenance impact
in mind.

---

## Status notes

- Drafted 2026-05-15 afternoon, after first 124-paper SOP_v3 overnight
  completion and overnight-comprehensive library audit.
- Decision pending: ingest 796 papers with current SOP_v3 (defer L4 to later)
  vs. implement L4 first then re-ingest everything.
- Cost trade-off: re-ingesting 124 + 796 with v4 = ~10 days total. Running
  796 with v3 then re-running everything when v4 lands = ~16 days total.
  Implementing v4 first is the cheaper path if v4 is going to happen anyway.
