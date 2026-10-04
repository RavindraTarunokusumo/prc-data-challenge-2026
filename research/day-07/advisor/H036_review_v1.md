---
schema: advisor-review-v1
hypothesis_id: H036
proposal_version: 1
proposal_sha256: 413475f20b4a404a73134ea5bc73867d86ddb4bdb6d13c3cc17bc19251adb698
exchange_id: X-D07-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.88
created_utc: 2026-10-03T20:50:26Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.88).** The shared findings and binding conditions U1–U10 are in `H035_review_v1.md` and apply here unchanged. **U3 (dirty tree), U4 (unmasking event), U5 (status) and U10 bear most directly.**

**Conditions carried from the previous batch.** The proposal says "procedure as H031 §Batch and its review's conditions S3–S8 where they apply". For this batch:
- S3, S4, S7 and S8 are replaced by U3, U4, U10 and U9;
- S6 applies as U9 states.

**What H036 is.** It fits E020's configuration on the frozen final folds `SUBMIT_JAN` and `SUBMIT_JUL`:
- 12 training months, including December, unmasked through the logged path;
- no truth and no score.

Its only use is the subgroup rows that H037 takes.

**Verified here.**
- The proposal hash matches the envelope.
- **Parsed-YAML comparison:** `params`, `model` and `feature_set` equal E020's, and `folds` are the two frozen final folds.
- **The final-fold path has run on real data without defect.** E042 used the same learner and feature set (routed), taking 280 s and 7.02 GB, with one unmasking event and empty final-fold metrics.
- **E049 differs from E042 in two ways only:**
  - no ridge;
  - the subgroup's training rows are kept, so the fit learns the convention, which is H035's mechanism.
- **The fit is deterministic.** It has 2,085,047 training rows, under the 5,000,000 bin sample, so the procedure takes no draw (as H034).
- **The subgroup holds 107 and 276 rows in the ranking months, verified.** January 2026's subgroup has the heaviest schedule-delay tail of any month (`H035_review_v1.md`, table), so E049's subgroup predictions will sit higher there than on any development fold.

**E049's predictions outside the subgroup are never used.** They carry D3-C2 untreated: E020's out-of-range predictions on non-LIRF NM-missing rows. They are never submitted, blended or quoted as a submission quantity.

## Scientific Validity

- **A procedure run, with no mechanism claimed.**
- **The refit-on-all-training-months step is the one H031 used,** with no new selection: the configuration, iterations and features are fixed.
- **One more training month matters here.** December adds a month of convention rows that no development fold trained on. Its effect on the subgroup predictions is unmeasurable, as for E042 (ruling H6 (f)).

## Novelty Relative to Existing Research

- **No unrouted SUBMIT fit exists.**
- **Rule 10 is not engaged:** H036 is not a candidate.

## Experimental Isolation

- Against E045, only the folds differ.
- No ablation is needed.

## Validation Quality

- **Integrity, blocking:**
  - COMPLETE within class;
  - exactly one `holdout_targets_unmasked_for_final_training` event inside its run span (U4).
- **The H037 route check** (`route_check.py E050 E044 E049`) then checks the rows taken from it.
- **Sanity, non-blocking:** H035 §Batch's subgroup flag (U9).

## Leakage Review

### Target Leakage

PASS

- **December targets enter only as final-fold training labels,** through the logged path (U4).
- **No December figure appears in any artifact:**
  - `metrics.json` is empty for final folds;
  - `learning_curve` returns training loss only;
  - the worker prints "saved".

### Temporal Leakage

CONCERN

Label notes, as H016 v2; not blocking.
- `masked_view` gives the ranking information set: one ranking month per view, with its own DEP block times and targets nulled.
- All training months precede both ranking months.
- The convention channel is T (H035 review).

### Competition Availability

PASS

- Every FS2 input is present for ranking DEP rows.
- **Ranking-data asymmetries, not availability failures:**
  - the July month edge;
  - the six-month gap (S9).

## Compute Review

### RAM

PASS

- E042 peaked at 7.02 GB, including a ridge. E049 has no ridge but about 1,500 more training rows (the subgroup's, which E042 excluded).
- Expected 6.8–7.3 GB, under CLASS-M's 8 GB. The hard limit is 11 GB.

### Runtime

PASS

- E042 took 280 s. Expected 260–360 s, plus W&B sync time.
- The 600 s guard requires a start by 00:50:00Z. The CLASS-M timeout is 2,700 s.

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

**That E049's subgroup predictions behave like E045's on the development folds.**
- They come from a 12-month fit.
- They are made on a January subgroup whose schedule delays exceed every 2025 month in median and q90.
- The bet's per-row stakes are therefore largest exactly where no fold has measured them (U6).

## Missing Control or Ablation

None required. U8 (b)'s ranking-month exposure figures are computed from E050 against E044, which compares E049's subgroup rows with the routed ridge's.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

**Allocation:** exactly one `primary` allocation, `uv run python scripts/gate.py allocate H036 v1`, made fifth in the batch (expected **E049**, U1).

**Config:** the Proposed Change block:
- folds `SUBMIT_JAN` and `SUBMIT_JUL`;
- seed 42;
- CLASS-M.

**When:** fifth in the queue of the pinned `research/day-07/sessions/D07-S01/run_window_2.sh`, in the 2026-10-04 00:00–01:00Z window (INC-0015), or later under U10.

**Status (U5):**
- a component: not a candidate, never NEW, never scored;
- no holdout access, and the ledger decision is null;
- only its subgroup rows are used, through H037.

**Not authorized:** any other allocation, any change to the configuration, or any use of its non-subgroup predictions.

Required acknowledgement path: `research/day-07/acks/H036_ack_v1.md`.
- It references the proposal hash `413475f20b4a404a73134ea5bc73867d86ddb4bdb6d13c3cc17bc19251adb698` and this review's hash.
- It adopts U1–U10 of `H035_review_v1.md` as binding.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement: not applicable. There is no truth, and nothing is scored.

| Event | P |
|---|---|
| E049 COMPLETE within CLASS-M, inside the window | 0.90 |
| Exactly one unmasking event, inside its span (U4) | 0.97 |
| Each ranking month's share of subgroup predictions above 3,600 s lies inside H035 §Batch's flag band | 0.80 |

Expected magnitude:
- **Resources:** runtime 260–360 s; peak RSS 6.8–7.3 GB.
- **Subgroup predictions:**
  - most of the 107 and 276 rows lie far above the routed ridge's predictions, which are about 1,760 s on average and never above 2,263 s;
  - January's subgroup mean is the higher of the two ranking months.

Primary expected failure mode:
- **Primary: deferral.** E045 and E047 run long enough to leave less than 600 s before 01:00Z. E049 and E050 are then deferred to another owner window (U10).
- **Secondary: a first-use defect.** The unrouted final-fold fit hits a defect shared with nothing tested so far. This is unlikely, since E042 exercised the same path.
