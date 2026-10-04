---
schema: advisor-review-v1
hypothesis_id: H033
proposal_version: 1
proposal_sha256: c908b3bedf691067020bca2bf86c826eae72a0082caad52e49710bef52649adc
exchange_id: X-D07-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-10-03T17:19:51Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.85).** The shared findings and the binding conditions S1–S9 are in `H031_review_v1.md`. They apply here unchanged. **S4, S7 (blend substitution) and S8 (formatting) bear most directly on this proposal.**

**What H033 is.** E033's fixed 0.5/0.5 blend applied to E042 and E043, followed by formatting into the template. The output is the final predictions.
- **Parsed-YAML comparison:** the config block equals `experiments/E033/config.yaml`, except the header fields, `folds`, and `components` (`[E042, E043]` in place of `[E029, E031]`, in the same order).
- Weights were fixed a priori in H023 v3. Nothing is fitted.
- The proposal hash matches the envelope.

**The blend path was checked in code.**
- `prc.blending.blend`:
  - refuses a component that is not COMPLETE;
  - verifies each component's prediction file against its manifest;
  - joins on the fold's validation ids with a 1:1 check;
  - refuses any null.
- `tests/test_isolation.py::test_blending_does_not_import_truth` exists.
- **Launcher gating is correct.** E044 starts only if E042 and E043 are COMPLETE and route-checked. A failed E043 route check marks E042 as not checked, so E044 is deferred.
  - It also needs now + 60 s ≤ 20:00Z.

**The formatter was checked in code and by test.** `scripts/make_submission.py`, SHA-256 `c99fdaba…c290c1`, unchanged at `eedcd47`.
- **The integrity checks behave as the docstring states:**
  - **I1:** the template SHA-256 matches its single raw-manifest entry; verified independently here (`0d383408…`).
  - **I2:** every prediction file is verified through `stored_predictions`.
  - **I3:** the template ids are unique integers, and the blend covers them 1:1 with finite values; ids are not duplicated across the folds, and there are no extra ids.
  - **I4:** the blend equals the weighted halves within 1e-9 s, with the weights read from the blend's config.
  - **I5:** rounding moves no value by more than 0.5 s, and every value is in the Int32 range.
- **Output checks:** the output's schema and row order must equal the template's.
- **Fail-safe:** any failure exits before a file is written, and the tests cover the refusals.
- **Formatter tests:** 4 passed.
- **The reference distribution is intact.** All 24 reference prediction files (E033, E029 and E031 on 8 folds) exist and match their manifests. The formatter verifies them before it writes, so a missing file would stop it safely.
- **The formatter reads no target.** From silver it reads only `MVT_ID_mvt`, `ADEP_mvt` and `AOBT_3_flt`; the template's target column is all null.

**Two points are specific to H033.**
1. **E044 loads unmasked silver.** It lists final folds, so the worker calls `load_silver(unmask_holdout_for="E044")`. The FS0 frame then carries December training labels, which the blend never uses. Integrity reading 4 must include E044 (S4). The proposal says this itself, but its blocking wording ("E042 and E043 only") contradicts it.
2. **Minor, not required:**
   - `subgroups()` reads silver without verifying silver's manifest. Only the non-blocking readings depend on it, and every run verifies silver when it loads.
   - `fold_reading` aligns the two halves by sorted id. That is safe on the final folds, where I3 and I4 have already established equal id sets, and on the reference folds, which were route-checked on identical rows.

## Scientific Validity

- The submission is the promoted champion's construction, applied without change. Its only post-processing is the rounding the template's dtype forces.
- **No floor or clip** is applied. This is correct: the training-target minimum is −12 s, and E033's evaluated figures include its 159 negative predictions. Clipping would submit a predictor that was never evaluated.
- **The readings are target-free** and anchored to the reference folds: (a) out-of-range counts, (b) mean and median, (c) the halves' disagreement, and per-airport means. Each is a disclosure (S6). The rule 12 D3-C3 rows (January, `d_sched` > 3 h and > 5 h) are reported, as the standing rule requires. July 2026 lies inside the 2025 range (Day 3 record).

## Novelty Relative to Existing Research

- **It produces the project's only submission.** Nothing in the journal duplicates it.
- **Rule 10 is not engaged.** Other weights, CatBoost alone, or draw averages would need new proposals that state the selection. None is proposed.

## Experimental Isolation

- Against E033, only the components (the SUBMIT fits) and the folds change. The weights, component order and blend code are unchanged since H023 v3.
- No ablation is needed, because no mechanism is claimed.

## Validation Quality

- **Blocking:** integrity readings 1–4 (4 as restated in S4) and I1–I5.
- **Non-blocking:** the sanity flags, with thresholds measured on E033's folds and fixed before the run.
- **Defects:** S6 states when a flag becomes a defect.
- **Upload:** S8 ties the uploaded file to the SHA-256 recorded in `SUBMISSION_RECORD.json`.
- **No calendar match:** no reference fold validates on January, so the January comparisons use H (December) and W1 (February) as calendar neighbours (rule 4). The proposal says so.

## Leakage Review

### Target Leakage

PASS

- The blend reads stored, manifest-verified predictions and no truth.
- The formatter reads only target-free silver columns and the template.
- E044's unmasked load is logged (S4), and no target value is used.

### Temporal Leakage

PASS

- The components inherit H031's and H032's temporal review.
- The blend adds no information beyond its components, which trained on 2025 only.

### Competition Availability

PASS

The output matches the challenge's stated format:
- Parquet, `submitting.parquet`;
- two columns, `MVT_ID_mvt` Float64 and `TAXITIME_SEC_mvt` Int32;
- the 344,841 ranking DEP rows, in template order.

## Compute Review

### RAM

PASS

- E033 and E041 peaked at 3.38 and 3.42 GB, under CLASS-S's 4 GB.
- The FS0 frame grows about 9 % with 12 training months, so the expected peak is 3.4–3.5 GB.
- The formatter is lighter: three silver columns plus prediction files.

### Runtime

PASS

E033 and E041 ran in 8–9 s. Expected: under 20 s, against the 60 s guard and the 450 s CLASS-S timeout.

### Disk

PASS

About 5 MB of records, plus a submission file of about 2–3 MB, which is git-ignored and covered by `SUBMISSION_RECORD.json`.

## Weakest Assumption

**That the halves are correct, not just consistent with each other.**
- I3 and I4 prove the blend is exactly 0.5·E042 + 0.5·E043 over the template's rows.
- They cannot show that either half was trained as intended. The shared final-fold path is unexercised (H031 review).

## Missing Control or Ablation

None required. The named controls of the H031 review apply.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **H033 v1: exactly one `primary` allocation,** `uv run python scripts/gate.py allocate H033 v1`, made third in the batch (expected **E044**).
  - **Config:** the Proposed Change block, with components `[<H031 id>, <H032 id>]`, weights `[0.5, 0.5]`, folds `SUBMIT_JAN` and `SUBMIT_JUL`, seed 42, CLASS-S.
  - **When:** third in the queue of the pinned `run_window.sh`, in the 2026-10-03 19:00–20:00Z window, or later under S7.
- **After E044 is COMPLETE:** one `make_submission.py E044 E042 E043 --ref E033 E029 E031` under S8, or the ids actually used under S7.
- **Blend substitution** after a component rerun follows S7: a new `--purpose rerun` allocation of H033 v1. E044's committed config is never edited.
- **Status:** not a candidate, never NEW, never scored; no holdout access; ledger decision null.
- **Upload:** only after FROZEN, once, by the owner, of the recorded file (S6, S8).
- **S1–S9 of `H031_review_v1.md` bind this run.**

Required acknowledgement path: `research/day-07/acks/H033_ack_v1.md`. It references the proposal hash `c908b3bedf691067020bca2bf86c826eae72a0082caad52e49710bef52649adc` and this review's hash, and accepts S1–S9 as binding.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement: not applicable. There is no truth, and nothing is scored.

| Event | P |
|---|---|
| E044 COMPLETE within CLASS-S, given E042 and E043 COMPLETE and route-checked | 0.97 |
| I1–I5 all hold and the file is written, given E044 COMPLETE | 0.95 |
| A submission file exists from tonight's window (whole chain) | 0.85 |
| No sanity flag (a)–(c) in either month | 0.85 |
| 2026-07 mean prediction above 2026-01's | 0.75 |

Expected magnitude:
- **Mean prediction:** 2026-01 960–1,010 s; 2026-07 995–1,050 s.
- **Rounding:** RMS 0.287–0.290 s, maximum 0.5 s.
- **Out of range:**
  - below 0 s: at most 0.03 % of rows in each month;
  - above 3,600 s: 0.03–0.15 %.
- **January D3-C3 rows** (`d_sched` > 3 h, 435 rows): 0–8 predicted above 3,600 s.

Primary expected failure mode:
- **Upstream:** E043 fails on GPU memory, so E044 is deferred.
- **For H033 itself:** an operational slip. Examples: arguments to the formatter that do not name the ids actually blended, or a formatter run while the lock is held. The formatter's own checks are unlikely to fail.
