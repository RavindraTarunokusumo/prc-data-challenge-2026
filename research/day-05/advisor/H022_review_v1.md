---
schema: advisor-review-v1
hypothesis_id: H022
proposal_version: 1
proposal_sha256: 043f9625010775991ac5a558073867a83dad45696faa8d1fcdf2fb89bfd22121
exchange_id: X-D05-S04-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.90
created_utc: 2026-10-01T19:24:03Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.90).**

H022 is the right control, minimal and correctly implemented. It is Missing Control 3's "contrast whose only difference is the categorical handling, at fixed capacity" (`H020_review_v1.md`). It cannot run as written, for three reasons:

1. **Its integrity clause is unattainable on the laptop** (`LAPTOP_REFS_review_v1.md` (b), D5-C4).
   - On the laptop, the routed path's ridge (E027 = E029) differs from E028 on every routed row of every fold, by up to 190.9 s.
   - `route_check.py <H022> - E028` at 1e-6 s will almost surely be met, and H022 would then be INVALID.
   - **The stated consequence, "and so is H021's clause 1", does not follow.** Clause 1's population, `NM_present_excl_LIRF`, contains no LIRF row, and the routed rows are LIRF NM-missing rows. A routed-row defect cannot move clause 1's statistic.
2. **The comparability check cannot be executed.**
   - It requires H022's resolved `get_all_params()` to equal H021's on every key except the categorical ones.
   - But `gbm.catboost` does not record the resolved parameters. The model is discarded (`allow_writing_files=False`), and nothing in the worker, the curves or the manifest captures them. `gbm.py` is in the frozen-tools list.
   - So "the resolved parameters recorded" has no source in the run.
3. **The resource statements are inconsistent with the evidence.**
   - **RAM.** Peak RAM "4.5–6 GB" comes from a calibration process that does not hold two frames. The worker's `route_train_exclude` path does: `_routed` keeps `feats` and the filtered `gbm_frame` alive together. On the laptop E029 peaked at **6.60 GB**, against E027's 5.19 GB on the same configuration without the exclusion.
   - **Class wording.** "CLASS-M (expected inside CLASS-S's runtime)" contradicts the 8–14 min estimate (CLASS-S is under 5 min).
   - **Calibration fold.** The 0.029 s per iteration figure is `cb_gpu_nocat` on **FS2**, not FS2_RAW.

**Verified here** (beyond `LAPTOP_REFS_review_v1.md`):
- **Code.**
  - `gbm.catboost` with `cat_mode: codes` passes the categorical columns as `cat.codes` of the training vocabulary (sorted levels), with unseen levels as NaN and `cat_features=[]`. The default path is unchanged.
  - The `ed5151f` diff touches only the CatBoost function, `blend.py`, the worker's `needs_fold` path, the runner's GPU sampling and tests.
- **Tests.** `tests/test_models.py::test_catboost_codes_mode_uses_no_categorical_features` passes, within 31/31 synthetic model tests.
- **Calibration.** `cb_gpu_nocat` resolves `simple_ctr`, `combinations_ctr`, `max_ctr_complexity` and `one_hot_max_size` to null, with Plain boosting, SymmetricTree, Bayesian bootstrap, `random_strength` 1, `l2_leaf_reg` 3 and `border_count` 254 (`gpu_calibration.json`).
- **Cardinalities.** R3's FS2_RAW training cardinalities are stand 1,877, op_prefix 2,288, ades 1,507 and actype 264 (calibration record).

## Scientific Validity

### (a) What the control removes

- **Removed.** In `codes` mode no categorical feature is declared. CatBoost therefore builds no CTRs of any type (border share, frequency, target mean), no combinations, and no one-hot encodings.
- **Kept.** The parameters, rows, routing, seed and numeric inputs are the same.
- **Inherent in the representation.** The contrast also carries two properties of integer codes. Both belong to "categorical handling", so they do not break isolation, but **the Mechanism text should state them:**
  1. **Quantization.** With `border_count` 254, a numeric column gets at most 254 borders. Stand (1,877 levels), op_prefix (2,288) and ades (1,507) are therefore binned into runs of adjacent codes, and actype (264) nearly so. Levels inside one bin cannot be separated at all, at any number of splits. "Useful level sets can only be isolated by spending splits" overstates the codes arm.
  2. **Alphabetical order is not arbitrary here.**
     - ICAO destination codes are ordered by region (E…, L…, K…).
     - Aircraft type designators cluster by manufacturer and family (A3…, B7…).
     - Stand names cluster by pier or terminal prefix.
     - Adjacent codes therefore often share operational meaning. "A split groups levels that merely share a name prefix" understates what the codes arm can extract.
- **Effect on the expected contrast.** Both points cut the same way: H022 is likely stronger than the proposal assumes, and the H021 − H022 gap smaller (Advisor Prediction).

### (b) The integrity clause and its consequence

- **The route check.** The routed rows are fitted by the same `_routed` ridge whatever the tier-1 learner. Whether the CatBoost path reproduces E027's routed rows, E028's, or neither, is unknown (LAPTOP_REFS (b)).
- **What a routed-row defect can affect.** All-rows comparisons (`compare.py <H022> E029`, reported) and the criterion 8 statistic.
- **What it cannot affect.** It cannot affect H021's clause 1.
- **What v2 must state.** The consequence should be scoped to what a routed-row defect can affect.

### (c) The comparability check

**The check is the right idea.** It turns "only `cat_mode` differs" from an assertion into a recorded fact.

**It needs a source.** One of:
- the run captures the resolved parameters (for example, per fold, beside the curves);
- or the proposal names a permuted-target fit of the exact configuration as the source, with the reason the resolution cannot depend on the target values.

The choice is the researcher's. The source must exist before the tools freeze.

## Novelty Relative to Existing Research

- **H022 is new.** It is the first within-learner contrast of categorical handling in this project.
- **It is the control the Day 4 review and phase close named** (Missing Control 3).
- **It is not a candidate.** It is never NEW, and rule 10 is not engaged.

## Experimental Isolation

- **One change against H021: `cat_mode`.** This is verified in code and test. The CTR parameters stay in the configuration and are inert without categorical features.
- **The inherent differences in (a)** (quantization, the information in alphabetical order, and the absence of combinations and frequencies) are all part of the categorical-handling treatment. They are not extra treatments.
- **GPU non-determinism and seed.** H022 is not reproduced. The noise scale for the contrast comes from H021's seed-43 reproduction, which is adequate for a control.

## Validation Quality

- **Folds.** The frozen folds are used unchanged, all 8, with H predicted only.
- **Twin rule.** It applies through `mechanism_check.py`.
- **Role.** H022 is the reference side of H021's clause 1 and carries no claim of its own.
- **Reported comparisons.**
  - `compare.py <H022> E029` is a family contrast (learner and feature set differ), not a matched contrast.
  - `range_check.py <H022> E029 --bands` gives rule 12 counts.

## Leakage Review

### Target Leakage

PASS

The codes come from the fold's training vocabulary (`_frames`), with no target. Validation-only levels are NaN.

### Temporal Leakage

CONCERN

This is carried, not blocking: FS2's T features, as disclosed in H015 v2 and carried through E019 and E023. No new temporal input.

### Competition Availability

PASS

- The raw keys are label P and present in the ranking files (DATASET_AUDIT §6.2, as FS1).
- 2026 levels unseen in 2025 become NaN in a submission fold. Their target-free share is recorded under H021's rule 2.

## Compute Review

### RAM

REVISE

- **The estimate.** The proposal's 4.5–6 GB comes from the calibration process.
- **The worker path is heavier.** With `route_train_exclude: true`, `_routed` keeps the full frame and a filtered copy. E029, the same routing path with LightGBM, peaked at 6.60 GB against E027's 5.19 GB.
- **Expected for H022:** about 6.5–7.5 GB at the largest fold (H, 11 training months). That is inside CLASS-M's 8 GB, but close.
- **Swap** (D5-C1). With swap on, RSS can understate the true footprint. The resolution of D5-C1 applies.

### Runtime

PASS

- 8–14 min is credible: E029's 893 s includes about 690 s of LightGBM fitting, which CatBoost codes replaces with about 30 s per R3-equivalent.
- The class is CLASS-M; the "inside CLASS-S's runtime" wording must go.

### Disk

PASS

About 15 MB of predictions and curves, covered by the manifest.

## Weakest Assumption

**That integer codes are an information-poor representation of these keys.**
- Destination, aircraft type and stand names are hierarchical.
- A depth-8 symmetric tree can combine an airport split with a code range and recover much of a stand's pier, or a destination's region.
- If that is so, H022 sits closer to H021 than the expected +6 to +25 s, and H021's clause 1 is decided near its −3.0 s floor.

## Missing Control or Ablation

None beyond what H022 is. It is the control.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- There is no allocation of H022 v1.
- No CatBoost fit with a real target on a frozen fold.
- Still allowed:
  - synthetic tests;
  - target-free checks;
  - permuted-target calibrations that compute no metric.

Required acknowledgement path: none for v1. Submit `research/day-05/proposals/H022_v2.md` in a new exchange, together with H021 v2 and LAPTOP_REFS v2.

## Revision

**Required (minimal):**

1. **Integrity clause** (b).
   - Adopt the route-integrity reference and tolerance settled in LAPTOP_REFS v2, which a correctly routed laptop run on this code path can meet.
   - Scope the consequence of a failure to the comparisons a routed-row defect can affect. It does not reach H021's clause 1.
2. **Comparability check** (c). Name the source of the resolved `get_all_params()` for both arms, and make it exist before the tools freeze.
3. **Resources.**
   - Re-estimate peak RAM from the worker path: E029 6.60 GB is the evidence, plus CatBoost's own overhead.
   - Remove "expected inside CLASS-S's runtime".
   - State that the 0.029 s per iteration calibration is on FS2, not FS2_RAW.
4. **Mechanism text** (a). State the 254-border quantization of the high-cardinality codes and the information carried by alphabetical order. This changes no parameter.

**Acceptable as is:**
- the single change (`cat_mode: codes`) and its test;
- the role (reference only, never NEW) and the run order;
- the reported comparisons;
- the leakage statements.

## Advisor Prediction

These are for a v2 run of the same design.

Probability of improvement:
- P(H022 − H021 on `NM_present_excl_LIRF`, development mean > +3.0 s) = 0.60. This is the mirror of H021's clause 1 not met.
- P(H022 development mean below E029's 442.5 s) = 0.03.

Expected magnitude:
- **H022 − H021, `NM_present_excl_LIRF`:** +1 to +10 s (central +5). This is below the proposal's +6 to +25 s, for the reasons in (a).
- **H022 − E029, `NM_present_excl_LIRF`:** +5 to +20 s (central +11).
- **Development mean:** 448–468 s (central 456).
- **Rule 12, > 3 h band** (5 development folds): ≤ 10 with P 0.80.
- **Peak RSS:** 6.5–7.5 GB.

Primary expected failure mode:
- **As written.** The integrity clause is met on routed rows that do not enter clause 1. H022 is recorded INVALID, and H021's clause 1 with it, for no scientific reason.
- **After revision.** The codes arm recovers a good part of the keys' signal through naming hierarchy. H021's clause 1 is then decided within about 2 s of its floor.
