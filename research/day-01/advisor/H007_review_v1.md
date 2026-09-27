---
schema: advisor-review-v1
hypothesis_id: H007
proposal_version: 1
proposal_sha256: 541ea19a3b65c253a019b629f23a7a4b6fd727d51841bbdb062d0dcd1e011706
exchange_id: X-D01-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-09-27T12:31:26Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**

H007 is a legitimate second Tier 1 reference:
- XGBoost `hist` with partition-based categorical splits;
- one a-priori configuration, with no search and no early stopping;
- the training-row vocabulary shared with H006 through `_frames`;
- a deterministic build (`test_model_deterministic` passes).

The configuration is the one calibrated at `866b902` (50 and 200 rounds on S1, with no metric computed), and it is unchanged since.

**Verified here.** The batch-level checks recorded in `H001_review_v1.md` also hold for H007: hashes, tests (90 of 90), lint and a clean tree.

**Findings:**
1. **The implementation question is confounded with capacity.** The research question asks whether the result is robust to the boosting implementation. The configurations differ in more than growth policy:

   | Setting | H007 (XGBoost) | H006 (LightGBM) |
   |---|---|---|
   | Minimum leaf size | `min_child_weight` 10, i.e. about 10 rows under squared error | `min_data_in_leaf` 100 |
   | Tree size | depth 10, up to 1,024 leaves | 255 leaves |

   The proposal acknowledges this under Alternative Explanations. The second falsification clause (a difference of more than 5 % from H006) therefore tests robustness **to the configuration**, not to the implementation.
2. **The criterion-4 check is cross-implementation.** "H007 passes criteria 1–2 against H008" compares XGBoost with the deltas against LightGBM without them. That changes the library and the features together.
   - It is informative only by transfer from H006 against H008.
   - If H007 is promoted *over H006*, the attributed mechanism is "the XGBoost configuration", and its ablation is the H006 comparison itself, which the promotion test already runs.
   - Record this. It does not block.
3. **The same single-row exposure as H006.**
   - No S1 training month contains any `d_aobt3 ≥ 20,000 s`.
   - H007 therefore predicts a bounded value for the day-scale LIRF row in S1's validation month (`d_aobt3` = 87,181 s, with all NM and schedule times about 24 h before takeoff).
   - Its S1 comparison with H005 depends on that row's recorded block time, exactly as for H006. I did not read the target.
   - The smaller minimum leaf size lets XGBoost isolate extreme training targets more readily, which matters for R1–R3 and H: the LIRF row is in their training data.

## Scientific Validity

Sound as a robustness reference. The hyperparameters are conventional and fixed.

**Tail sensitivity.** With `min_child_weight` 10 and L2 loss, leaves of 10–20 rows can form around extreme targets (up to 131,167 s). H007 may therefore be more tail-sensitive than H006, in either direction:
- better where extreme targets echo extreme anchors;
- worse where they are noise.

The B4 figures will show which.

**Expected result.** "Within ±3 % of H006" is coherent with the falsification threshold of 5 %.

## Novelty Relative to Existing Research

- The journal is empty.
- Brief §11 names XGBoost as the second Day 1 Tier 1 baseline.
- It is not redundant with H006, because it tests a different configuration family.

## Experimental Isolation

**Against the better of H004 and H005.** Valid in the same way as for H006.

**Against H006.** Two things are confounded:
- the implementation (depth-wise against leaf-wise growth, partition splits, the sampling scheme);
- capacity and regularisation.

Attribution of any H007–H006 difference is to "configuration", not "implementation". That is acceptable for a robustness reference and must be stated that way in the analysis.

## Validation Quality

**Folds and criteria.**
- The frozen folds are used unchanged, S1 is a required WIN, and the twins are scored.
- **Forward exposure.** The sign is pre-registered, "as H006".
- **W1c.** W1c (one training month) with `min_child_weight` 10 and depth 10 is the fold most prone to overfitting. A W1c LOSS would demote a W1 WIN.

**Reproduction.** Row and column subsampling make seed 43 differ from seed 42. Smaller leaves make H007 more seed-sensitive than H006, but per-fold differences above 1.0 s remain unlikely.

**Validation limit.** As for H006, no fold reproduces January 2026's density of long anchors: 0.375 % of rows with `d_aobt3 ≥ 3,600 s` against at most 0.132 % in 2025.

**Batch conditions B1–B4** (defined in full in `H001_review_v1.md`) apply.

## Leakage Review

### Target Leakage

PASS

No target-derived input is used, the vocabulary comes from training rows, and there is no early stopping on validation data.

### Temporal Leakage

PASS

The T-labelled inputs are admissible under §6.2. Forward exposure on S1 and W1 comes from the frozen design and is handled by standing rule 2 and condition B3.

### Competition Availability

PASS

Every input is present in `ranking.parquet`. Missing values are handled natively.

## Compute Review

### RAM

PASS

The FS0 build was measured here at 3.45 GB on fold H, the largest fold. The DMatrix and the quantile index add a few hundred MB. Expect about 4–4.6 GB, inside "< 5 GB" and CLASS-M (8 GB).

### Runtime

PASS

- **Training.** 0.1685 s per round (calibrated on S1) × 1,000 rounds × total training volume (7.12 times S1; fold H alone is 1.25 times S1) ≈ 20.0 minutes.
- **Total.** With DMatrix construction, prediction and evaluation, about 21–23 minutes. That is within the CLASS-M target of 30 minutes; the timeout is 45 minutes.
- **Margin.** It is the thinnest in the batch. A reproduction run costs the same again.

### Disk

PASS

About 10 MB.

## Weakest Assumption

The assumption is that a difference between H006 and H007 reflects the implementation. With unequal capacity controls, it reflects configuration.

For the chain, the binding assumption is the same as for H006: that the S1 comparison with H005 measures bulk accuracy rather than the single day-scale LIRF row.

## Missing Control or Ablation

- **An XGBoost ablation without the deltas** would give H007 a same-implementation criterion-4 check.
  - It is not required if H007 is promoted over H006, because the H006 comparison is then the operative ablation.
  - If H006 is not champion and H007 is promoted against H004 or H005, criterion 4 rests on the cross-implementation comparison with H008. The analysis must state that limitation.
- **Condition B4** is required.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Primary run.** One primary run:
  1. `uv run python scripts/gate.py allocate H007 v1`.
  2. Write the config exactly as in the Implementation Plan: `model: xgboost`, `feature_set: FS0`, `params` as listed (`objective: reg:squarederror`, `eta: 0.05`, `max_depth: 10`, `min_child_weight: 10`, `subsample: 0.8`, `colsample_bytree: 0.9`, `max_cat_to_onehot: 1`, `nthread: 4`, `num_boost_round: 1000`), `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
  3. Run `uv run python scripts/run_experiment.py E###`.
- **Comparisons.** Each with the B4 figures:
  - against the better of H004 and H005 (falsification clause 1);
  - against H006 (clause 2, the 5 % check);
  - against H008;
  - against the current champion.
- **Reproduction, only if H007 passes criteria 1–3 against the current champion and is not falsified.**
  1. `gate.py allocate H007 v1 --purpose reproduction` (seed 43).
  2. `scripts/reproduce_check.py <repro> <primary> --champion <champion>`.
- **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun` is permitted and must be logged. A TIMEOUT is a RESOURCE_FAILURE and is not retried silently.
- **Not authorized:**
  - any hyperparameter, round-count or feature change;
  - early stopping;
  - scoring H.

Required acknowledgement path: `research/day-01/acks/H007_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It should record findings 1–2: the H006 difference is attributed to configuration, and the H008 check is cross-implementation.
- It should adopt conditions B1–B4.

## Revision

None required.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Passes criteria 1–2 against the better of H004 and H005 | 0.50 (same single-row dependence as H006) |
| Development-fold mean RMSE within 5 % of H006 | 0.85 |
| Displaces H006 as champion | 0.10 |
| Ends Day 1 as champion | 0.05 |

Expected magnitude: development-fold mean RMSE within ±4 % of H006. Slightly worse on the tail-heavy folds (S1, W1) because of the smaller minimum leaf size.

Primary expected failure mode: the same as H006. S1 comes out TIE against H005, and LIRF fails criterion 3, if the day-scale LIRF row's block time is on the original day. Secondary: seed sensitivity of the small leaves on tail-heavy folds.
