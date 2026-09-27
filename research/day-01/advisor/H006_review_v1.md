---
schema: advisor-review-v1
hypothesis_id: H006
proposal_version: 1
proposal_sha256: 435a63b783e3a09fef51c92b5608af48941680ca8966cab4303e6639a1a964a8
exchange_id: X-D01-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-09-27T12:30:41Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**

H006 is a properly constrained Tier 1 baseline:
- one LightGBM configuration, fixed a priori;
- 1,000 rounds, with no early stopping on validation data and no search;
- the categorical vocabulary taken from training rows (a polars `Enum`; unseen levels become missing);
- a deterministic build (`deterministic=True`, `force_row_wise=True`, seeded).

Its falsification clause (criteria 1–2 against the better of H004 and H005) tests the nonlinear mechanism directly. H008 tests that the deltas carry the signal.

**Verified here.** The batch-level checks recorded in `H001_review_v1.md` also hold for H006:
- hashes, tests (90 of 90), lint and a clean tree;
- hyperparameters unchanged since `866b902`, which is also the commit of the calibration. The calibration trained this configuration for 50 and 200 rounds on S1 and computed no metric.

**Library and code checks.**
- LightGBM 4.7.0 re-maps pandas categoricals to the training categories at prediction time.
- `test_model_deterministic` and `test_gbm_uses_only_present_columns` pass.

**Findings:**
1. **The Day 1 champion question may be decided by one row.** Target-free facts:
   - S1's validation month (July 2025) contains one LIRF row with `d_aobt3` = 87,181 s. All its NM and schedule times sit about 24 h before takeoff.
   - No S1 training month contains any `d_aobt3 ≥ 20,000 s`.
   - LightGBM will therefore predict a bounded leaf value (the top anchor bin) for that row, while H005 predicts about 87,000 s.

   If the recorded block time is on the original day, H006 carries an error of about 80,000 s on S1:
   - S1 is at risk of TIE against H005;
   - LIRF's pooled RMSE rises by about 4–11 %, which exceeds criterion 3's tolerance;
   - H006's own falsification clause may be met, so under B2 it is not promoted.

   If the block time is on the departure day, the same row hands H006 an easy S1 WIN. See Weakest Assumption. I did not read the target.
2. **What H008 tests.** The ablation is almost certain to pass (P ≈ 0.97), because it removes the anchor that the audit already shows to be dominant. It supports "the deltas are used", not "trees learn interactions". The interaction claim is carried by the falsification clause against H004, which has the same inputs in linear form. That combination is adequate. The Alternative Explanations section is wrong, though, to say H008 can show gains from "correcting the anchor's airport bias": H008 has no anchor. H004 is the relevant control for that.
3. **Record inconsistencies.**
   - Required Ablation says H008 is "minus the three time-delta features". H008 removes four: `d_aobt3`, `d_eobt1`, `d_sched` and `flt_missing`, as H008 itself states.
   - The runtime premise ("largest fold, S1") is wrong: fold H trains on 24.8 % more rows. The total estimate remains valid (see the Compute Review).

## Scientific Validity

**Mechanism.** Trees can learn airport × runway × delay-regime corrections to a noisy anchor, and the hypothesis is sound. The hyperparameters are conventional for about 1.5 million rows and 11 features.

**Expected behaviour.**
- **Tail.** L2 boosting on a target with extreme records (up to 131,167 s) will chase leaves that contain them. `min_data_in_leaf` = 100 limits this, and the metric is RMSE, so a conditional mean is the right estimand.
- **Tail share.** The pre-registered tail mechanism is appropriate. Against H005 the tail share may even be negative: H006 gains in the bulk and gives back tail rows where the raw anchor was right.

## Novelty Relative to Existing Research

- The journal is empty.
- Brief §11 names LightGBM as the Day 1 Tier 1 baseline.
- It is unchanged since `866b902`.
- It is not redundant.

## Experimental Isolation

**Against H004.** The same FS0 inputs; only the linear model is replaced by trees. That isolates nonlinearity, up to the ridge's winsorisation and linear hour and weekday terms.

**Against H005.** Fitting and nonlinearity together.

**Against H008.** Four features removed as a group. That is acceptable, because the claim is about the group (NM and schedule deltas).

Taken together the three comparisons attribute the effect adequately for a baseline. The B4 figures are needed to tell a broad bulk gain from a gain carried by a few extreme-anchor rows.

## Validation Quality

**Folds and criteria.**
- The frozen folds are used unchanged, S1 is a required WIN, and the twins are scored.
- **Forward exposure.** The sign is pre-registered for the runway key and the hour: S1c and W1c < 0 against H004 and H005. Read it as against each of them.
- **W1c.** W1c trains on one month (153,706 rows) with 1,000 rounds and 255 leaves. A W1c LOSS through overfitting would demote a W1 WIN under the twin rule. This is conservative, because W1 is not a required WIN.

**Reproduction.** With bagging (0.8) and feature sampling (0.9), seed 43 changes the ensemble. I expect per-fold RMSE differences of about 0.1–0.5 s, which is inside the frozen 1.0 s tolerance.

**Validation limit.** No fold reproduces January 2026's density of long anchors: 0.375 % of rows with `d_aobt3 ≥ 3,600 s`, mostly an EHAM cluster on 3–9 January, against at most 0.132 % in any 2025 month. How the trees map long anchors will matter more on the January test than on any fold.

**Batch conditions B1–B4** (defined in full in `H001_review_v1.md`) apply. B2 and B4 are the ones that bind here.

## Leakage Review

### Target Leakage

PASS

- No target-derived input is used.
- The vocabulary and the trees come from training rows.
- There is no early stopping on validation data.

### Temporal Leakage

PASS

- **Admissibility.** The T-labelled inputs are admissible under §6.2.
- **Forward exposure.** Exposure on S1 and W1 through `airport_runway` comes from the frozen design and is handled by standing rule 2 and condition B3.

### Competition Availability

PASS

Every input is present in `ranking.parquet`. NM data is missing for 1.61 % (January 2026) and 1.48 % (July 2026) of rows; LightGBM handles that natively, together with the `UNK` categoricals.

## Compute Review

### RAM

PASS

The FS0 build was measured here at 3.45 GB on fold H, the largest fold. LightGBM adds the pandas copy and the binned dataset (about 0.3–0.6 GB at 1.9 million rows). Expect a peak of about 3.8–4.5 GB, inside "< 5 GB" and CLASS-M (8 GB).

### Runtime

PASS

- **Training.** 0.070 s per round (calibrated on S1) × 1,000 rounds × total training volume (7.12 times S1 across the eight folds) ≈ 8.3 minutes.
- **Total.** With data loading, prediction and evaluation, about 9–10 minutes. The CLASS-M target is 30 minutes and the timeout 45 minutes.
- A reproduction run costs the same again.

### Disk

PASS

About 10 MB.

## Weakest Assumption

The assumption is that the frozen comparison with the better of H004 and H005 measures bulk accuracy. The single day-scale LIRF row in S1 can dominate it:
- One error of about 86,000 s on S1 is about 3.9 × 10⁴ s² of MSE, i.e. +40–45 s of RMSE.
- In the frozen bootstrap, that row's cluster is drawn at least twice with probability 0.26.
- If H005 is right on that row, H006 needs about 100 s of S1 advantage elsewhere to WIN S1. It would also add about 1.1 × 10⁵ s² to LIRF's pooled development MSE (66,051 rows).

The same pattern recurs in July 2026 (one LIRF row, 86,340 s), so this is not only a validation artefact.

## Missing Control or Ablation

- The named ablation (H008) is adequate for its claim.
- Condition B4 (row concentration) is required for every comparison that decides H006's promotion or falsification.
- No further control is needed before execution.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Primary run.** One primary run:
  1. `uv run python scripts/gate.py allocate H006 v1`.
  2. Write the config exactly as in the Implementation Plan: `model: lightgbm`, `feature_set: FS0`, `params` as listed (`objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 0.9`, `bagging_fraction: 0.8`, `bagging_freq: 1`, `num_threads: 4`, `num_boost_round: 1000`), `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
  3. Run `uv run python scripts/run_experiment.py E###`.
- **Comparisons.** Each with the B4 figures:
  - against the better of H004 and H005 by development-fold mean RMSE (falsification);
  - against H008 (ablation);
  - against the current champion.
- **Reproduction, only if H006 passes criteria 1–3 against the current champion, is not falsified, and passes against H008.**
  1. `gate.py allocate H006 v1 --purpose reproduction` (seed 43).
  2. `scripts/reproduce_check.py <repro> <primary> --champion <champion>`.
- **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun` is permitted and must be logged.
- **Not authorized:**
  - any hyperparameter, round-count, feature or objective change, including early stopping, robust losses or clipping (a new version or hypothesis);
  - scoring H.

Required acknowledgement path: `research/day-01/acks/H006_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It should record finding 3 (four features removed in H008; fold H is the largest fold).
- It should adopt conditions B1–B4.

## Revision

None required.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Passes criteria 1–2 against the better of H004 and H005 | 0.55 |
| Passes against H008 | 0.97 |
| Reproduction within 1.0 s | 0.90 |
| Ends Day 1 as champion | 0.40 |

The first figure is about 0.9 if the LIRF row's block time is on the departure day, and about 0.25 if it is on the original day.

Expected magnitude: development-fold mean RMSE of 300–370 s, which is 10–20 % below H004 and H005 on bulk rows. The ≥ 3,600 s band stays poorly predicted.

Primary expected failure mode: S1 comes out TIE against H005, and LIRF fails criterion 3, both driven by the single day-scale LIRF row in July 2025. Criterion 2 then fails, the falsification clause is met, and H006 is not promoted even though it is better on almost every row.
