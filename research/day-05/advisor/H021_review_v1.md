---
schema: advisor-review-v1
hypothesis_id: H021
proposal_version: 1
proposal_sha256: a46c916ae3e363ff963a8074111a4c67dee126a43acfdc7c8c26259a5e5d13c7
exchange_id: X-D05-S04-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.90
created_utc: 2026-10-01T19:25:16Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.90).**

**The science is now sound.** H021 answers every objection of `H020_review_v1.md` and Missing Control 3 of X-D04-S02-0001:
- the boosting scheme is stated (Plain) and resolved;
- the CTR types are named and resolved, and the target-mean statement is **verified here** ((a));
- the raw levels are kept (FS2_RAW);
- combinations are kept (complexity 4);
- the capacity control is a one-parameter twin (H022);
- the GPU rationale is tied to a decision (H023, and whether CatBoost goes to Days 6–7);
- the calibration script is committed.

**It cannot run as written, for six reasons:**
1. **The integrity clause is unattainable** (D5-C4; `LAPTOP_REFS_review_v1.md` (b)). The laptop's routed-path ridge differs from E028 on every routed row of every fold, by up to 190.9 s. `route_check.py <H021> - E028` at 1e-6 s will almost surely make H021 INVALID. That would remove H023's component on routed rows that do not enter clause 1.
2. **"The resolved `get_all_params()` (recorded in the analysis)" has no source.** `gbm.catboost` discards the model and records no parameters, and `gbm.py` is frozen for the chain.
3. **The calibration table misattributes a row** (D5-C7).
   - "CatBoost GPU, same, `gpu_ram_part` 0.4 | 0.162 | device peak 3,251 MiB" is `cb_gpu_raw_cap`. That run used the **default CTRs** (Borders, FeatureFreq), at learning rate 0.05 for 500 iterations.
   - FloatTargetMeanValue was run only at `gpu_ram_part` 0.95 (`cb_gpu_raw_mean`, device peak 7,112 MiB).
   - So H021's configuration (three CTR types, complexity 4, `gpu_ram_part` 0.4) has **not been calibrated as a unit**, and "≤ 3.3 GB" VRAM is unverified.
   - The codes row (0.029 s per iteration) is FS2, not FS2_RAW.
4. **Peak RAM "5–6 GB" is underestimated.**
   - The worker's `route_train_exclude` path holds the full frame and a filtered copy at once. E029 peaked at **6.60 GB**, against E027's 5.19 GB on the same configuration without the exclusion.
   - CatBoost added 0.47 GB over LightGBM in the calibration (5.18 against 4.71 GB), before its string conversion of nine categorical columns.
   - Expect about 7–8 GB at the largest fold. That is the CLASS-M target, and **H023's criterion 7 inherits H021's class**.
5. **Clause 1's WIN count is undefined.** It does not say whether WINs are read from `fold_outcome_counted` (the frozen twin rule, adopted for H019 v2) or from raw `fold_outcome`, nor among which folds.
6. **A GPU failure would be mis-recorded.** The runner records a non-zero worker exit as INVALID. A CUDA out-of-memory or device error is a resource failure, and its recording must be pre-registered.

**Verified here** (beyond `LAPTOP_REFS_review_v1.md`):
- **FloatTargetMeanValue averages the raw target.** The test was a synthetic GPU fit, with no project data, `gpu_ram_part` 0.05 and the lock free.
  - Design: three levels share the same 50 % zero / 50 % positive split, with positive values 10, 100 and 1,000, so the raw means are 5, 50 and 500.
  - `simple_ctr=[FloatTargetMeanValue]` predicts **6.9 / 50.3 / 500.0**.
  - `[Borders]` predicts **117.9 for all three**: its one-border share cannot tell the levels apart.
  - The resolved string's `TargetBorderCount=1` is therefore inert for this type.
  - `[FeatureFreq]` also separated the three levels, but only because their counts differ, which makes a frequency a level identifier. With thousands of levels, 15 frequency borders group levels by frequency, not by target.
- **Calibration** (`gpu_calibration.json`).
  - Plain, SymmetricTree, three CTR types at complexity 4, Bayesian bootstrap, `random_strength` 1, `l2_leaf_reg` 3, `border_count` 254 and `one_hot_max_size` 2.
  - 0.17–0.20 s per iteration on GPU (CPU at Day 4: 0.88–1.13). LightGBM 0.111.
  - 5 of 6 CatBoost GPU configurations were non-deterministic. `cb_gpu_raw` repeated, and the second `cb_gpu_raw_cap` draw has the same hash as `cb_gpu_raw`.
- **Cardinalities.** R3 FS2_RAW: stand 1,877, op_prefix 2,288, ades 1,507, actype 264. That is 1.40–4.37 times FS2's.
- **Code.**
  - `gbm.catboost` in `ctr` mode passes strings, with unseen levels as `__NULL__` and `cat_features` set.
  - The staged curves take `predict(ntree_end=1)` plus `staged_predict(eval_period=10)`, and the learn RMSE comes from `get_evals_result()`.
  - `routed_catboost` shares `_routed` with the LightGBM path.
  - `tests/test_models.py` passes 31/31 (synthetic).
- **E027's curves** support "flat from about 500 iterations" for the LightGBM.
- **E029 on the clause population** (re-scoring of its existing predictions, development folds, through `truth_frame`): RMSE 213.4, 208.3, 201.5, 243.3 and 230.1 s on R1–W1, about 219 s on average. The −3.0 s floor is about 1.4 % of it.

## Scientific Validity

### (a) The mechanism now matches the configuration

The three H020 defects are resolved:
- **Boosting.** Plain is stated, and no ordered-boosting claim is made. The CTRs are still computed on permutations of the training rows.
- **Statistics.** A border share, a frequency and a **raw-target mean** (verified). The mechanism ("statistics order levels by target behaviour") is true at least of the target-mean and border-share CTRs.
- **Inputs.** Raw levels, and combinations at complexity 4.

**"Not claimed" is correctly scoped:** no CTR type is isolated, combinations are not isolated, and ordered boosting is not run.

### (b) Clause 1 is decisive

- **The size of the test.** The population has 132,000–172,000 rows per development fold. The frozen cluster bootstrap resolves differences of about 1 s there.
- **The floor, −3.0 s, is meaningful in both directions:**
  - not met: the statistics add at least 1.4 % of the population's RMSE;
  - met: they add less.
- **The noise condition.** It reads clause 1 as INCONCLUSIVE when a single seed and GPU re-draw moves the population mean by more than 1.5 s. That is sound: a two-arm difference then carries noise comparable to half the floor.
- **Gap: the WIN count is undefined** (Summary, item 5).
  - Precedent: `H019_review_v2.md` adopted `fold_outcome_counted`, the frozen twin rule.
  - Here S1c and W1c can check the CTR effect, because their own training months give their own statistics. The counted reading is natural, but it must be stated.

### (c) The budget is part of the treatment contrast

- **The budget.** Both arms run 1,000 iterations at learning rate 0.08, at depth 8. CatBoost's own default for 1.7 million rows would be a larger rate, and the proposal expects under-convergence.
- **Why it matters.** The codes arm needs more splits than the CTR arm to isolate the same level sets. Part of the clause 1 gap can therefore be convergence speed rather than information.
- **This is acceptable,** because "at fixed capacity" includes the budget. But:
  - the reading must say "at this budget";
  - the analysis must report both arms' development-mean validation curves, including their slopes over iterations 800–1,000;
  - no iteration count may be chosen from those curves later without saying so (INC-0009 addendum).

### (d) A heavy-tailed target and a target-mean statistic

- **The tail stays in training.** The LIRF NM-present block-at-schedule tail rows remain in the CatBoost's training set (rule 8), with targets up to day scale. A single 87,000 s record shifts a 200-row level's mean by about 435 s.
- **The CTRs are noisy where it matters.** Ordered statistics on permutations make the training-row CTRs of such levels noisy. A symmetric tree may split on that noise.
- **Consequence for clause 1.** If clause 1 is met, "the target-mean statistic is tail-contaminated" is an explanation beside "too coarse" and "the high-traffic levels dominate". These explanations cannot be told apart here. Add it to the Alternative Explanations.

### (e) The integrity clause

- **The test.** Routed rows must equal E028 within 1e-6 s. That is unattainable on the laptop (D5-C4).
- **Its consequence is mis-scoped.**
  - Routed rows are LIRF NM-missing rows. Clause 1's population excludes LIRF, so routed-row integrity cannot move clause 1.
  - It can move the all-rows comparisons (reported), the criterion 8 statistic, and H023's routed rows.
- **What v2 must do.** Adopt the reference settled in LAPTOP_REFS v2, and scope the INVALID consequence to what a routed-row defect can affect.

### (f) Against E029

- **This is a family contrast:** a different learner on a different feature set. It is reported only, as the proposal says.
- **The expectation is consistent with the record.**
  - H007 (XGBoost) lost to LightGBM by 12.4 % on Day 1.
  - Symmetric depth-8 trees at this budget are expected to trail 255-leaf leaf-wise trees.

## Novelty Relative to Existing Research

- **It is the project's first CatBoost run,** and the first designed to answer the Day 4 categorical-handling question with a matched control.
- **It is not redundant with H019** (explicit fold-local priors in LightGBM), and it uses a different statistic family.

## Experimental Isolation

- **Against H022: one parameter.** Inherent to the representation, and part of the treatment (`H022_review_v1.md` (a)):
  - the CTR feature set, its combinations and frequencies;
  - quantization of the codes at 254 borders;
  - the information carried by alphabetical order.
- **Against E029: not isolated,** and not claimed to be.

## Validation Quality

- **Folds.** The frozen folds, unchanged, with all 8 predicted and H predicted only.
- **Clause 1** runs through `mechanism_check.py`, which is the frozen `promotion_check` on the population, with the twin rule.
- **Reproduction.** The seed-43 reproduction is unconditional, and it is the right noise scale for a stochastic learner (`H020_review_v1.md`, Validation Quality).
- **Rule 12 and the single-row predictions** are pre-registered. They are disclosures.

## Leakage Review

### Target Leakage

PASS

- **CTRs** are computed by CatBoost from training rows only. Training rows are taken on permutations. Validation rows use statistics of all training rows, and their targets are null in the masked view.
- **The FS2_RAW change** (no collapse) uses neither the target nor validation rows.

### Temporal Leakage

CONCERN

This is carried, not blocking.
- **FS2's T features are unchanged.**
- **In S1 and W1,** CTR statistics include post-validation training months. That is the frozen fold design, as for H019's priors.
- **Raw levels sharpen per-level statistics,** so the twins matter more here. Report the S1c and W1c cells beside S1 and W1.

### Competition Availability

PASS

- Stand, aircraft type, operator prefix and destination are label P and present in the ranking files.
- 2026 levels unseen in 2025 become `__NULL__` and take the CTR prior. Their target-free share is recorded (rule 2).

## Compute Review

### RAM

REVISE

- **Estimate the worker path, not the calibration process.** E029, the same routing and exclusion path, peaked at 6.60 GB. CatBoost's overhead and the H fold (11 training months) add to that.
- **The class must be chosen against an evidenced estimate.** About 7–8 GB sits at the CLASS-M target.
  - If v2 keeps CLASS-M, it states what follows if the run exceeds 8 GB without reaching the 11 GB guard. Criterion 7 then fails for H021, and through H023's criterion 7 for H023.
  - CLASS-L needs the explicit justification of brief §4.
- **Swap.** D5-C1 must be resolved first, because swapped pages escape the RSS guard.

### Runtime

PASS

- **20–30 min is credible.**
  - E029, the same path with curves, took 893 s with LightGBM at 0.111 s per iteration.
  - At 0.17 s per iteration, CatBoost adds about 400–450 s over the 6.2 R3-equivalents plus H. String preparation and staged predictions add more.
  - Estimate: about 22–27 min.
- **The upper end touches the CLASS-M target.** Exceeding 30 min without reaching the 45-min timeout is the same criterion 7 question as RAM.

### Disk

PASS

About 15 MB of predictions and curves, covered by the manifest.

## Weakest Assumption

**That integer codes are an information-poor control.**
- Destination, aircraft type and stand names are hierarchical (`H022_review_v1.md` (a)).
- A depth-8 symmetric tree can recover pier and region structure from code ranges.
- The expected −12 s central effect is therefore optimistic, and clause 1 may be decided near its floor.

## Missing Control or Ablation

None for clause 1: H022 is the control. The H023-level control (a blend of E029 with H022) is named in `H023_review_v1.md`.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- There is no allocation of H021 v1 or of its reproduction.
- No CatBoost fit with a real target on a frozen fold.
- Still allowed:
  - permuted-target calibrations that compute no metric (for example, of the exact H021 configuration);
  - synthetic tests;
  - target-free checks.

Required acknowledgement path: none for v1. Submit `research/day-05/proposals/H021_v2.md` with H022 v2, H023 v2 and LAPTOP_REFS v2.

## Revision

**Required (minimal):**

1. **Integrity clause** ((e)).
   - Use the route-integrity reference and tolerance settled in LAPTOP_REFS v2, attainable on this code path.
   - Scope the INVALID consequence to what a routed-row defect can affect. Clause 1 is not affected.
2. **Resolved parameters.**
   - Name and create the source of `get_all_params()` for H021, H022 and H021's reproduction, before the tools freeze.
   - The Validation Plan and H022's comparability check depend on it.
3. **Calibration evidence** (D5-C7).
   - Correct the table: the 0.4 row is default CTRs, at learning rate 0.05 for 500 iterations, and the codes row is FS2.
   - Either calibrate the exact configuration (permuted target, no metric) or mark the VRAM figure unverified.
4. **RAM and class** (Compute Review). Re-estimate from the worker path, and justify the class against the estimate, with H023's criterion 7 in view.
5. **Clause 1 WIN count.** State the outcome field (counted or raw) and the folds among which WINs are counted.
6. **Failure recording.**
   - Pre-register that a GPU memory or device error is recorded as RESOURCE_FAILURE, beside the runner's INVALID status.
   - It is not retried with changed parameters without a new version.
   - It stops the chain until a new version is accepted.
7. **Alternative Explanations.** Add tail contamination of the target-mean CTR ((d)).

**Carry into v2 as recording** (no design change):
- both arms' validation curves and their 800–1,000 slopes, with clause 1 read "at this budget";
- the runner's `gpu_mib_peak`;
- the 2026 unseen-level shares (rule 2);
- the S1c and W1c cells beside S1 and W1.

**Acceptable as is:**
- the research question and the mechanism (verified);
- FS2_RAW;
- the single a-priori configuration: Plain; three CTR types; complexity 4; depth 8; 1,000 iterations; learning rate 0.08; `border_count` 254; `l2_leaf_reg` 3; 4 threads; seed 42 and 43;
- H022 as the control;
- clause 1's floor and readings;
- the noise condition and its INCONCLUSIVE reading;
- the unconditional reproduction;
- "Not claimed";
- the rules 1–12 statements;
- the provenance line.

## Advisor Prediction

These are for a v2 run of the same design.

Probability of improvement:

| Event | P |
|---|---|
| Clause 1 not met (H021 − H022 ≤ −3.0 s with ≥ 3 counted WINs) | 0.60 |
| H021 − E029 on `NM_present_excl_LIRF` below 0 | 0.10 |
| The noise condition triggers (reproduction differs by > 1.5 s) | 0.15 |
| H021's prediction on row 192622644 is below E029's 7,041 s | 0.60 |
| Rule 12, > 3 h band ≤ 10 (5 development folds) | 0.80 |
| Validation curve still falling by ≥ 0.5 s over iterations 800–1,000 (development mean) | 0.65 |
| Runtime above 30 min | 0.15 |
| Peak RSS above 8 GB | 0.25 |

Expected magnitude:
- **H021 − H022, `NM_present_excl_LIRF`:** −1 to −10 s (central −5). This is below the proposal's −12 s central.
- **H021 − E029, `NM_present_excl_LIRF`:** +3 to +14 s (central +7).
- **H021 − E029, all rows:** +2 to +16 s.
- **Development mean:** 446–458 s (central 450).
- **Row 192622644:** 2,000–9,000 s.

Primary expected failure mode:
- **As written.** INVALID on the E028 route check, for routed rows that do not enter clause 1. The chain then loses H023's component.
- **After revision.** The categorical statistics help, but by less than pre-registered, because the codes arm recovers naming hierarchy and the budget limits both arms. Clause 1 is decided within about 2 s of −3.0 s, and the noise condition matters.
