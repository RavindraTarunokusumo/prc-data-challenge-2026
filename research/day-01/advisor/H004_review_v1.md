---
schema: advisor-review-v1
hypothesis_id: H004
proposal_version: 1
proposal_sha256: 9eb6270e3a3166890a412c98442d07a8e4607c76e3d0206d12a643de496b2621
exchange_id: X-D01-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-09-27T12:29:29Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**

H004 is a correctly fold-local linear reference:
- every fitted transform comes from the fold's training rows: winsorisation quantiles, median fill with missing-value indicators, standardisation and the one-hot vocabulary;
- `alpha` and the winsorisation bounds were fixed a priori;
- the ridge fit uses only training targets.

The two falsification clauses (criteria 1–2 against H003, and against H005) are decisive.

**Verified here.** The batch-level checks recorded in `H001_review_v1.md` also hold for H004:
- hashes, tests (90 of 90), lint and a clean tree;
- `alpha` and `winsor` unchanged since `866b902`.

**Ridge solver.** With sparse input and an intercept, scikit-learn 1.9.1 resolves `solver="auto"` to `sparse_cg`. The fit is deterministic (`test_model_deterministic` passes). Unseen validation categories get a zero one-hot row.

**Three findings** (none blocks):
1. **Winsorisation is doing two jobs.** Clipping `d_aobt3` at the training 99.5 % quantile has two effects:
   - it makes H004 robust to absurd anchors;
   - it discards the signal in genuine long anchors above the cap.

   Target-free facts make both matter:
   - **Day-scale row.** S1's validation month (July 2025) contains one LIRF row with `d_aobt3` = 87,181 s. All its NM and schedule times sit about 24 h before takeoff, and no S1 training month has any `d_aobt3 ≥ 20,000 s`. July 2026 has one row with the same pattern.
   - **Negative anchors.** July 2025 has 117 rows with `d_aobt3 < −600 s`; the minimum is −10,851 s.
   - **January 2026.** 0.375 % of rows have `d_aobt3 ≥ 3,600 s`, against 0.067–0.132 % in every 2025 month. Most are an EHAM cluster on 3–9 January.

   H004's result against H005 on S1 may be decided largely by the single LIRF row (see Weakest Assumption).
2. **RAM sits on the CLASS-S boundary.** The resource premise that S1 is the largest fold is wrong: fold H trains on 1,919,370 rows, 24.8 % more than S1. See the Compute Review.
3. **The pre-registered ordering may be inverted in the bulk.** The proposal expects H004 at 400–470 s, at or above H005 at 360–420 s. In the bulk, however, `BLOCK − AOBT_3` is plausibly independent of the taxi duration. The least-squares slope on the anchor will then be below 1 (regression dilution), and the airport and runway offsets remove the anchor's bias. On bulk rows H004 should therefore beat the raw anchor. Its fate against H005 is decided in the tail. This is a prediction, not a defect.

## Scientific Validity

**Mechanism.** "Noisy linear proxies plus airport and runway bias correction" is a sound account of what a linear model can extract from FS0. The design is a legitimate linear Tier 0 reference, as brief §11 requires.

**Limitations** (acknowledged or harmless):
- `hour_utc` and `weekday` enter linearly, so the diurnal pattern is represented crudely.
- The null indicators for columns that are never null are constant columns, which the ridge ignores.
- `flt_missing` duplicates the anchor's null indicator.

**What the H005 comparison tests.** It shows whether the fitted combination adds anything over the raw anchor, which is the question §6.3 asks. It does not show which part of the fitted combination helps:
- the slope shrinkage;
- the offsets;
- the other deltas;
- winsorisation acting as robustness.

## Novelty Relative to Existing Research

- The journal is empty.
- Brief §11 names the linear baseline.
- It is unchanged since `866b902`.
- It is not redundant.

## Experimental Isolation

**Against H003.** Many changes at once: the estimator, the features and the fitting. That is acceptable, because the H003 clause is a floor, not a mechanism test.

**Against H005, the mechanism ablation.** Still several changes: fitting, the extra deltas, the offsets and winsorisation. The result attributes a gain to "a fitted linear combination of FS0" as a whole.

**Missing control.** Winsorisation is a robustness mechanism that H005 does not have. If H004's margin over H005 (or its deficit) is concentrated on the few extreme-anchor rows, it measures clipping, not linear bias correction. The B4 figures will show this. An unclipped variant would separate the two (see Missing Control or Ablation).

## Validation Quality

**Folds and criteria.**
- The frozen folds are used unchanged, S1 is a required WIN, and the twins are scored.
- **Forward exposure.** The sign is pre-registered for the runway key `airport_runway`, which is regime-sensitive at LFPG (27R and 27L switched over August to November).
- **S1c and 27R.** S1c trains on January to June, which contain only 62 LFPG_27R departures (against 3,495 in July). At `alpha` = 1, the 27R coefficient in S1c is essentially unregularised and noisy. That is part of what the S1c twin should expose.

**Tail share.** The pre-registered tail mechanism is weaker for H004 than for H005, because the anchor is capped at the training 99.5 % quantile. A tail share ≥ 0.5 against H003 is therefore unlikely.

**Validation limit.** No fold reproduces January 2026's density of long anchors, so the cost of the cap on the January test is not measured by any fold.

**Batch conditions B1–B4** (defined in full in `H001_review_v1.md`) apply. B1 matters for H004 (criterion 7; see the Compute Review).

## Leakage Review

### Target Leakage

PASS

All transforms and the fit use training rows only. `numeric_block` receives the training statistics for the validation rows. No target-derived input is used.

### Temporal Leakage

PASS

- **Admissibility.** The T-labelled deltas and the takeoff hour are admissible under §6.2.
- **Forward exposure.** Exposure on S1 and W1 through `airport_runway` comes from the frozen design and is handled by standing rule 2 and condition B3.

### Competition Availability

PASS

- Every input is present in `ranking.parquet`.
- NM data is missing for 1.61 % (January 2026) and 1.48 % (July 2026) of rows. The training median fill and the indicator handle this.
- No ranking DEP row has a runway unseen in training (audit §5).

## Compute Review

### RAM

PASS

There is a class-boundary risk (below). It cannot cause a run failure.

- **Measured here** (read-only, no model fitted). The FS0 build alone peaks at 3.45 GB on fold H, in a process that has already built S1 and R3. RSS carried over between folds is about 3.22 GB.
- **Calibration.** The calibrated ridge on S1 peaked at 3.28 GB, about 0.15 GB above its FS0 build.
- **Estimate.** Scaled to fold H, with the worker's scikit-learn import, the H004 peak is about 3.6–4.0 GB. The hard limit (11 GB) cannot be reached.
- **Risk.** P ≈ 0.25 that the peak exceeds the 4 GB CLASS-S target. `within_class` would then be false, criterion 7 fails (condition B1), and H004 cannot be promoted. Its reference numbers would remain valid for H006's falsification clause.

### Runtime

PASS

About 2–3 minutes, scaled from the 14.6 s calibration by total training volume (7.1 times S1). The CLASS-S timeout is 7.5 minutes.

### Disk

PASS

About 10 MB.

## Weakest Assumption

The assumption is that H004 against H005 measures the value of a fitted linear combination. In practice S1, and LIRF's pooled RMSE under criterion 3, may be decided by the single day-scale LIRF row.

**If its recorded block time is on the original day (target about 87,000 s):**
- H005 is nearly exact on that row.
- H004, clipped at a few thousand seconds, carries an error of about 84,000 s. That adds about 3.7 × 10⁴ s² to S1's MSE and about 1.1 × 10⁵ s² to LIRF's pooled development MSE (66,051 LIRF rows), i.e. roughly +4 to +11 % of LIRF RMSE.
- In the frozen bootstrap, that row's cluster is drawn at least twice with probability 0.26. H004 would then need an S1 advantage of about 100 s elsewhere to WIN S1.

**If its block time is on the departure day:** the same arithmetic runs in H004's favour.

I did not read the target.

## Missing Control or Ablation

- **B4 (row concentration, standing rule 6)** is required.
- **An unclipped ridge** would separate winsorisation-as-robustness from linear bias correction. It is not required for this baseline. However, if H004's margin (or deficit) against H005 is carried by rows beyond the clip, the linear-combination mechanism cannot be claimed without it.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Primary run.** One primary run:
  1. `uv run python scripts/gate.py allocate H004 v1`.
  2. Write the config exactly as in the Implementation Plan: `model: ridge`, `feature_set: FS0`, `params: {alpha: 1.0, winsor: [0.005, 0.995]}`, `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-S`.
  3. Run `uv run python scripts/run_experiment.py E###`.
- **Comparisons.** Each with the B4 figures:
  - against H003 (falsification clause 1);
  - against H005 (clause 2, the ablation);
  - against the current champion.
- **Reproduction, only if H004 passes criteria 1–3 against the current champion and `within_class` is true.**
  1. `gate.py allocate H004 v1 --purpose reproduction` (seed 43).
  2. `scripts/reproduce_check.py <repro> <primary> --champion <champion>`.
- **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun` is permitted and must be logged.
- **Not authorized:**
  - reclassifying the run as CLASS-M, or changing `alpha`, the winsorisation bounds or the features (any of these needs `H004_v2`);
  - scoring H.

Required acknowledgement path: `research/day-01/acks/H004_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It should record finding 2 (fold H is the largest training fold, and what a RAM overrun means for criterion 7).
- It should adopt conditions B1–B4.

## Revision

None required.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Passes criteria 1–2 against H003 | 0.95 |
| Passes criteria 1–2 against H005 | 0.35 |
| Peak RSS stays within CLASS-S | 0.75 |

Expected magnitude: development-fold mean RMSE of 340–420 s. H004 should be better than H005 on bulk rows and worse on rows beyond the clip.

Primary expected failure mode: against H005, S1 comes out TIE and criterion 3 fails at LIRF. Both would be driven by the single day-scale LIRF row if its recorded block time is on the original day. Secondary: a RAM overrun of the 4 GB class target on fold H, which fails criterion 7.
