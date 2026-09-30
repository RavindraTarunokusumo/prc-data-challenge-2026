---
schema: advisor-review-v1
hypothesis_id: H020
proposal_version: 1
proposal_sha256: 174102191673a5f2343c74bbad3df65f4a27e96e550749deed797b3aad986ff1
exchange_id: X-D04-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REJECT
confidence: 0.80
created_utc: 2026-09-30T17:16:31Z
---

# Advisor Review

## Summary Assessment

**Decision: REJECT. The CLASS-L justification that brief §4 requires is declined.**

This is not a judgement on CatBoost. It is a judgement that this design cannot answer the question it asks, and that its answer is not worth a CLASS-L run.

1. **The stated mechanism is not what the configuration runs.**
   - The installed CatBoost (1.2.10) resolves `boosting_type: Plain` for this parameter set. There is no ordered boosting.
   - For RMSE, its categorical statistics are two:
     - `Borders` CTRs on a target **binarised at one border** (MinEntropy; priors 0, 0.5 and 1);
     - `Counter`, a frequency count.
   - So "a leakage-controlled, smoothed target encoding … the prior mechanism of H019, learned inside the model" is false. The "two routes to priors" contrast with H019 is not like-for-like.
2. **The design cannot isolate categorical handling:**
   - FS2's categoricals are collapsed at 100 training rows (`RARE_MIN`) before any learner sees them. The "sparse levels" the mechanism needs are therefore gone.
   - `max_ctr_complexity: 1` removes the stand × runway combination.
   - Tree capacity (symmetric depth 6 against 255 leaves) is confounded, with no control.
   - Under ruling R, criterion 4 has no matched reference for the stated mechanism.
3. **The expected answer informs no decision.**
   - The pre-registered outcome is a scoped negative: P(improvement) 0.20 and +2 to +15 s, per the proposal.
   - It concerns a configuration that Day 5, the architecture day with GPU, would not use.
4. **CLASS-L is reserved** for feature rebuilds and confirmation runs, with explicit justification (brief §4). This run is neither, and Day 4 runs on the owner's daily limit (INC-0005). The runtime estimate itself is credible.

**Precedent.**
- H007 (XGBoost FS0) was accepted on Day 1 as a CLASS-M configuration reference, which the brief named as a Day 1 baseline, with its result attributed to "configuration" and not "implementation".
- H020 asks for CLASS-L, and its stated mechanism is one the configuration does not implement.

**Verified here.** All checks were read-only or synthetic, and no model was fitted on a real fold.
- **Hash.** The proposal matches the envelope.
- **Resolved CatBoost parameters.** `CatBoostRegressor(loss_function=RMSE, depth=6, learning_rate=0.08, border_count=254, max_ctr_complexity=1, thread_count=4)` was fitted on 20,000 and on 200,000 synthetic rows with a 500-level categorical. Via `get_all_params()`, both resolve to:
  - `boosting_type` Plain, `grow_policy` SymmetricTree;
  - `simple_ctr` and `combinations_ctr` both `Borders:TargetBorderCount=1:TargetBorderType=MinEntropy:Prior=0/1:Prior=0.5/1:Prior=1/1` plus `Counter`;
  - `one_hot_max_size` 2, `l2_leaf_reg` 3, `nan_mode` Min;
  - `bootstrap_type` MVS with `subsample` 0.8, and `random_strength` 1.
- **Calibration arithmetic re-checked.**
  - With the default combinations, depth 6: 0.455 s per iteration at 100 iterations, and 1.093 s per iteration marginal from 100 to 300.
  - With `max_ctr_complexity: 1`: 0.29–0.30 s per iteration, linear. 6.23 R3-equivalents of training rows gives about 31 min of fitting.
  - The addendum's script (scratch `cb_ctr1.py`) is not committed.
- **Code (INC-0005).**
  - `gbm.catboost` reuses LightGBM's vocabulary through `_frames`. Unseen or null levels become `"__NULL__"`.
  - `routed_catboost` shares `_routed` with the LightGBM path.
  - The three CatBoost tests (determinism, routing, exclusion) pass.

## Scientific Validity

### (a) The mechanism against the configuration

**Boosting scheme.**
- "CatBoost uses ordered target statistics and ordered boosting" does not describe this run. Plain boosting is what the library resolves here.
- The CTRs are still computed on permutations of the training rows. That part of "ordered" survives.

**What CatBoost computes for each categorical with more than 2 levels.**
- It computes neither a smoothed mean of y nor anything like H019's m-estimate.
- It computes the permutation-ordered share of rows whose y exceeds **one** MinEntropy border, at three priors, plus the level's frequency.
- Every such categorical is represented only through these statistics, including `ADEP_mvt` and `airport_runway`.
- With a heavy-tailed target (the LIRF NM-present tail alone reaches 87,002 s), a one-border statistic is a coarse "slow versus fast" share.

**The consequences for the record's claims:**
- "This is the prior mechanism of H019, learned inside the model" is false.
- "Two routes to priors, explicit LOMO statistics against in-model ordered statistics" compares a mean encoding of raw-level interaction keys with a one-border share of collapsed single keys.

### (b) The feature set removes what the mechanism acts on

- **What is left after the collapse.**
  - FS1 replaces every level with fewer than 100 training DEP rows by `__RARE__`, fold-locally.
  - After collapse, R3 has 1,343 stand levels, 606 `ades`, 523 `op_prefix` and 120 `actype`. Every one has ≥ 100 training rows, except one `__RARE__` bucket per column.
- **What that leaves for the mechanism.**
  - At n ≥ 100 with a prior weight of 1, ordered and plain statistics agree closely.
  - The mechanism the proposal names ("better … on sparse levels") therefore has nothing to act on except the `__RARE__` buckets.
  - The raw levels are exactly what H019's priors use, and exactly what H020 withholds.

### (c) Capacity is confounded, and criterion 4 cannot be carried

The learner changes at once in:
- tree shape and depth;
- categorical representation;
- NaN handling;
- stochastic row sampling (MVS, 0.8);
- random split noise;
- L2 regularisation;
- border selection.

The proposal concedes that capacity and categorical handling cannot be separated.
- **Ruling R** needs a matched reference that shares the candidate's procedure, so criterion 4 would carry only "this CatBoost configuration".
- **Outcome 1** ("CatBoost ≥ LightGBM here") would be a configuration statement, with no bearing on high-cardinality handling.
- **Outcome 2**, the pre-registered one, would be "this handicapped configuration loses". That is expected from capacity alone.

### (d) Value

- **The expected result is known in advance.** The proposal expects +2 to +15 s. I expect worse (Advisor Prediction).
- **Neither outcome changes a Day 4 decision.**
  - H019 answers the priors question directly.
  - D3-C2 is H018's.
- **Neither outcome informs Day 5.** A Day 5 CatBoost would be configured differently: GPU, combinations, depth, the raw categorical inputs.
- **A Day 1-style reference does not need CLASS-L.**

## Novelty Relative to Existing Research

- **The brief names CatBoost as the natural Day 4 candidate** for high-cardinality categoricals (§11). The item is legitimate.
- **This design repeats the H007 pattern:** an untuned learner-family swap. XGBoost lost to LightGBM by 12.4 %, and the difference was attributed to configuration.
- **It does not add the categorical-handling test** that would make it new.

## Experimental Isolation

- **"Same features, same training rows, same routing" is true at the input.**
- **But the learner never sees a raw category.** Everything with more than two levels becomes CTR and Counter features.
- **The treatment bundles about seven differences** ((c)), and no ablation separates them. The proposal defers that to Day 5.

## Validation Quality

- **The frozen folds, the H018 base and the planned `mechanism_check` and `compare` calls** would measure the contrast correctly.
- **The CatBoost fit is stochastic** (MVS, `random_strength`), although seeded. Its criterion 6 would be a genuine reproducibility test, not the determinism check of the deterministic LightGBM. Any future CatBoost proposal should pre-register what it expects from the seed-43 run.

## Leakage Review

### Target Leakage

PASS

- CatBoost's CTRs are computed on training rows only, with permutation ordering.
- Validation targets are null in the masked view.

### Temporal Leakage

CONCERN

This is not blocking.
- FS2's T features are inherited from H018 and E019.
- The CTR permutation mixes training months. That affects training rows only, and is within the fold's training part.

### Competition Availability

PASS

The same inputs as H018. All are present in the ranking files.

## Compute Review

### RAM

PASS

- The calibration was flat at 3.97 GB.
- The estimate of 5–6 GB, including the frame, is well inside 11 GB.

### Runtime

FAIL

- The estimate of 35–45 min is credible from the calibration, and inside CLASS-L's 90 min (the runner stops at 135 min).
- But CLASS-L requires an explicit Advisor justification, and I decline to give one for this design ((d)). It is not a feature rebuild or a confirmation run, and its result would inform no decision.

### Disk

PASS

About 10 MB.

## Weakest Assumption

**That a learner-family swap with default regression CTRs, on pre-collapsed categoricals and without combinations, tests CatBoost's handling of high-cardinality categoricals.** It tests a configuration.

## Missing Control or Ablation

These are named, not designed, for any new CatBoost proposal (Day 4 or Day 5):
- a contrast whose only difference is the categorical handling, with tree capacity held fixed; or a within-CatBoost contrast that removes the categorical statistics;
- if a sparse-level mechanism is claimed, categorical inputs that still contain sparse levels;
- a correct statement of the CTR type and boosting scheme that will run, checked against `get_all_params()`;
- a CLASS-L rationale tied to a decision the result would change;
- the calibration addendum's script, committed.

## Decision

REJECT

## Execution Authorization

Authorized scope: none. REJECT closes H020 v1.
- **No CatBoost fit with a real target on a frozen fold** under this proposal.
- **Permuted-target timing calibrations** that compute no metric remain allowed as infrastructure. So do synthetic tests.

Required acknowledgement path: none for v1.
- Record the rejection in `research/EXPERIMENT_JOURNAL.md` (negative results are kept).
- If the Day 4 CatBoost item is not re-proposed in a new form, record it as deferred to Day 5 in `research/day-04/DAY_SUMMARY.md` and `docs/reproducibility/HANDOFF_D04.md`.

## Revision

None (REJECT). Record notes for any successor proposal:
- The `created_utc` of v1 (17:55:00Z) post-dates the commit that contains it (`3298cc0`, 16:51:03Z). Use measured times.
- Add INC-0004 to the provenance line.
- Rule 8: "LIRF convention rows are excluded from the Tier 1 training" is false for the LIRF NM-present block-at-schedule tail rows (`H018_review_v1.md` (c)).

## Advisor Prediction

These predictions are for the run as written, had it been authorized.

Probability of improvement:
- P(H020 − H018 on `NM_present_excl_LIRF`, development mean < 0) = 0.08.
- P(outcome 1: criteria 1–2 on that population and all-rows mean < 0) = 0.04.

Expected magnitude:
- **`NM_present_excl_LIRF`:** +5 to +25 s (worse).
- **All rows:** +3 to +20 s.
- **Out-of-range counts on `NM_missing_other`:** below H018's. Symmetric trees with L2 leaves bound the predictions more tightly.

Primary expected failure mode: CatBoost loses to the routed LightGBM through capacity. The record then carries a scoped negative that says nothing about high-cardinality handling (the question asked), nothing about priors (H019's question), and nothing that transfers to a Day 5 CatBoost configuration.
