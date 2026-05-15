# ADR-0017: Skip L3_outline_relevance when no outline is provided

**Status**: Accepted
**Accepted-by**: Weikang Sun on 2026-05-15 after review by Web Claude
**Date**: 2026-05-15
**Decision-maker**: Weikang Sun
**Amends**: ADR-0014 (SOP_v4 — domain classification + L3 decoupling)
**Cross-reference**: ADR-0011 (cleaning_v2 + SOP_v3 versioning conventions)

---

## Context

ADR-0014 §"Why add a prompt rather than skip L3 for non-bioprinting papers"
argued *against* skipping L3 on the grounds that "skipping L3 makes the library
schema inconsistent across batches (124 papers have L3, 800 do not)." That
reasoning held while the L3 input outline applied universally. Two facts have
since changed it:

1. **The dry-run on 5 golden papers (2026-05-15 ~17:50 BST) showed L3 returns
   `no_outline_match` for 3/5 papers** even within the bioprinting batch —
   because the current `corpus/outline/review_outline.md` is a book-level chapter
   list, not a per-section breakdown. L3 already produces a degraded signal when
   the outline isn't section-granular.

2. **The next ~796 papers in `inbox/` (hip implant, FEA surrogate, AM, ML,
   miscellaneous) have no relationship to the RSC bioprinting outline by
   design.** Running L3 against an irrelevant outline for ~6.6h GPU
   (~30s/paper × 796) produces structurally hallucinated
   `no_outline_match: <reason>. Closest distant analogy: <phrase>.`
   lines — exactly the failure mode ADR-0014 §3 was written to eliminate.

The schema-uniformity argument from ADR-0014 also turns out to be weaker than
assumed in practice: a repo-wide grep (2026-05-15) found that the two evidence
generators that sound like L3 consumers — `scripts/chapter_evidence.py` and
`scripts/topic_evidence.py` — never read any L3 field, only L1 background, L1
methods, and L2 core_problem. The only live L3 consumer is the QA tool
`scripts/run_benchmark_v1.py`, which is straightforward to teach about a
skipped state.

---

## Decision

Allow L3 to be deliberately skipped per batch via an explicit `--no-outline`
flag, and record that skip in the metadata as a first-class sentinel value
(`"skipped_no_outline"`) rather than as a generic missing/null field.

Four code changes:

1. **`scripts/ingest.py`** — Add `--no-outline` argparse flag. When set,
   `outline_text = None`; the outline file is not read. The existing
   summary-builder logic in `ingest_one` is taught to surface the skip status
   as the string `"skipped_no_outline"` (truthy) so the end-of-run failure
   reporter does not flag deliberately-skipped L3 as a failure.

2. **`scripts/ingest/pipeline.py` — `run_sop_v2`** — When `outline_text` is
   `None` or empty/whitespace, skip the L3 LLM call entirely and store
   `{"ok": False, "error": "skipped_no_outline"}` in the results dict under
   key `L3_outline_relevance`. Downstream code that checks for key presence
   keeps working; the other five SOP stages run normally.

3. **`scripts/ingest/pipeline.py` — `derive_outline_match_status`** — Generalize
   the signature to accept either the L3 entry dict (preferred) or the raw
   answer string (backward-compatible). Returns `"skipped_no_outline"` when the
   entry is `None` or carries `error == "skipped_no_outline"`; keeps the
   existing `"matched"` / `"no_match"` / `"unknown"` branches. `build_metadata`
   is updated to pass the entry through, so `interpretive.outline_match_status`
   carries the skip provenance.

4. **`scripts/run_benchmark_v1.py`** — Teach `check_field_completeness` to
   detect `interpretive.outline_match_status.value == "skipped_no_outline"`
   and report L3 with a `"skipped_no_outline": True` flag rather than as a
   missing field. The per-paper print loop renders such papers as
   `SKIPPED (no outline, ADR-0017)` instead of running cleanliness detectors.
   The cross-paper aggregator already tolerates the L3-skipped case because
   per-field rate counters use `.get("present")` defaults to falsy.

Explicitly **out of scope** for this ADR (separate fixes):

- `scripts/export_corpus.py` still uses the stale `L3_personal_relevance` key
  name from before ADR-0014. It is independently broken for v4 papers and
  needs a key-rename PR; not addressed here.
- `scripts/build_metadata_v1.py` (the legacy builder, not the pipeline path)
  similarly carries the old key name; not addressed here.

---

## Rationale

1. **Path C (explicit flag) was chosen over path A (skip when outline absent)
   or path B (sentinel outline string).** The "no outline" condition for the
   796 inbox PDFs isn't an accidental empty file — it is the deliberate batch
   intent (these papers are outside the bioprinting outline by design).
   `--no-outline` captures that intent explicitly at the ingest call site,
   rather than implicit-in-file-contents.

2. **`"skipped_no_outline"` is a first-class sentinel, not a null.**
   `interpretive.outline_match_status.value` now distinguishes four states:
   `"matched"` / `"no_match"` (L3 ran), `"unknown"` (L3 attempted but failed
   or returned empty, e.g. under `--no-sop`), and `"skipped_no_outline"`
   (L3 deliberately not run). This addresses ADR-0014's schema-uniformity
   concern: the schema is uniform — every paper has the field — and the
   inconsistency in *content* is self-documenting provenance rather than
   ambiguous absence.

3. **Downstream breakage surface is small and contained.** The two evidence
   scripts don't read L3, so chapter-level and topic-level evidence generation
   is unaffected. Only `run_benchmark_v1.py` needed an update, and that
   update is one conditional in `check_field_completeness` plus one branch in
   the per-paper print loop.

4. **The implicit empty-outline case is also covered** (and improved).
   `run_sop_v2` skips L3 whenever `outline_text` is `None` *or* empty/whitespace,
   so even existing code paths that previously fed `""` to L3 (when the
   outline file was missing) now produce a clean skip rather than a forced
   hallucinated `no_outline_match` output. This is strictly a quality
   improvement.

5. **Path C future-proofs the multi-outline use case ADR-0014 §Rationale
   already anticipates.** When an FEA / hip-implant outline becomes available
   later, the same 796 PDFs can be re-ingested with
   `--outline fea_outline.md` (or whatever the flag becomes) and L3 will run
   normally with no schema migration. Papers re-ingested under a new outline
   will overwrite the `"skipped_no_outline"` sentinel with a real match
   result.

---

## Implementation cost

- ~6 lines added to `scripts/ingest.py` (argparse + conditional outline load +
  3-line `_stage_status` helper).
- ~6 lines added to `scripts/ingest/pipeline.py:run_sop_v2` (skip-L3 branch).
- ~15 lines changed in `scripts/ingest/pipeline.py:derive_outline_match_status`
  (signature widened to accept dict or string; docstring updated).
- ~2 lines changed in `scripts/ingest/pipeline.py:build_metadata` (pass
  `l3_entry` through instead of pre-extracting `l3_raw`).
- ~10 lines added to `scripts/run_benchmark_v1.py` (skipped-aware
  completeness check + per-paper print branch).

No new dependencies, no metadata schema migration for existing papers, no
re-ingest of the 124 bioprinting papers needed (their L3 entries continue to
flow through the unchanged matched/no_match/unknown branches).

L4 (`L4_domain_classification`) is **not** affected: it has no outline input,
so it always runs regardless of `--no-outline`. This is intentional — L4 is
the domain-routing signal the 796 non-bioprinting papers actually need.

---

## Open questions

1. Should `--no-outline` also write a structured note into `_ingested_meta`
   or `_schema_notes` for the paper, naming the ADR? Currently the only
   provenance signal is `interpretive.outline_match_status.value`. Probably
   sufficient, but could be surfaced more loudly.

2. Should the ingest summary report grow a per-batch line like
   `L3 skipped: N papers (--no-outline)` next to the existing
   `ingested / skipped / failed` line? Low-cost; defer until first 796-paper
   batch actually runs.

3. Should `check_l4_cleanliness`-style structured QA exist for the
   `outline_match_status` field once the corpus is mixed
   (matched / no_match / skipped / unknown distribution)? Useful but not
   blocking.

---

## Status notes

- Drafted 2026-05-15 after the 5-paper SOP_v4 dry-run (P1, P5, P44, P77, P117)
  completed ~17:50 BST. That dry-run already validated L3 behaves correctly
  when an outline is present: 3/5 papers returned `no_outline_match` against
  the book-level `corpus/outline/review_outline.md`, which is what motivated
  this ADR. The outline-granularity weakness is a separate concern (a
  per-section outline would change those 3 to `matched`); ADR-0017 narrows
  scope to "what should happen when no outline is provided at all".
- Single-paper `--no-outline` smoke test on P125 (NiTi µ-LPBF inbox PDF
  `003b6d2051aa21d9.pdf`) at 2026-05-15 19:53 BST confirmed end-to-end
  sentinel propagation: the ingest log emits
  `[P125] L3_outline_relevance SKIPPED (no outline) [ADR-0017]`,
  `metadata/P125.json` carries
  `interpretive.outline_match_status.value == "skipped_no_outline"` and
  `personal_relevance.sop_l3_raw._meta.error == "skipped_no_outline"`, and
  `run_benchmark_v1.benchmark_paper("P125")` prints L3 as
  `SKIPPED (no outline, ADR-0017)` rather than flagging it as a failure. L4
  ran cleanly on the same paper (`primary=additive_manufacturing`,
  two-line output, `clean=True`).
- Full multi-paper `--no-outline` path is intentionally not exhaustively
  pre-verified before commit because the planned 796-paper ingest will be
  its first real batch exercise; user accepts this risk on the basis that
  "no outline" is the simpler code path — L3 skip is the only behavioral
  change vs the already-validated with-outline path, and the smoke test
  above demonstrates the new branch is wired correctly through ingest,
  metadata, and benchmark.
- Accepted 2026-05-15 by Weikang Sun after review by Web Claude (see
  Accepted-by line in header).
