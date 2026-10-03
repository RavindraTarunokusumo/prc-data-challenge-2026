---
schema: advisor-review-v1
hypothesis_id: H027
proposal_version: 1
proposal_sha256: 361b317e712dde78a59bc32ba62cb1469849f524e5626f3553c4bbc9ebc802bf
exchange_id: X-D06-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.95
created_utc: 2026-10-02T17:45:57Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.95). As written, H027 cannot be executed.**

**The seed is refused.**
- `scripts/run_experiment.py::check_config` requires the seed that the frozen protocol assigns to the run's purpose (`config/splits.yaml`, `promotion.reproduction`):
  - `primary_seed` 42 for `primary` and `rerun`;
  - `reproduction_seed` 43 for `reproduction`.
- **Seed 44 is refused under every purpose.**
- **What would happen.** The Implementation Plan allocates with `gate.py allocate H027 v1`, whose default purpose is `primary`.
  - The runner would exit `refused: E038 (primary) must use seed 42, config has 44` before setting RUNNING.
  - The launcher would log `rc=1 status=ALLOCATED`, and E039 would be deferred.
  - Rung A would not run.

**The fix is one value.** v2 must use a seed the frozen protocol admits for its purpose, and say so.
- **The seed change stays inert for E029.** E029 has no subsampling, and every training fold is below `bin_construct_sample_cnt` (5,000,000; S1, the largest, has 1,537,475 rows). Its seed is therefore inert:
  - E023 at seed 42 equals E029 at seed 43 at the non-LIRF airports;
  - the routed ridge does not depend on the seed (E030 and E031 at seed 42 against E029 at seed 43: 0.0).
- **So the twin's seed drives only its own subsampling.**

**It also carries** §Batch revisions 1, 5, 6 and 7 of `H024_review_v1.md`, and the binding ruling there.

## Scientific Validity

- **The construction is correct for what it is:** a perturbation twin of E029 with Breiman-style row and feature bagging. It keeps the same features, learner, tree shape and routing.
  - `gbm.lightgbm` passes `feature_fraction`, `bagging_fraction` and `bagging_freq`.
  - LightGBM derives its bagging and feature-fraction seeds from `seed`.
  - `deterministic=True` with `force_row_wise=True` keeps it reproducible on the laptop.
- **Its information value is modest and predictable.** The predicted residual correlation with E029 is 0.995–0.999. By the Krogh & Vedelsby identity the batch cites, its blend gain is small by construction.
  - It measures the floor that generic averaging reaches at a perturbation twin's disagreement.
  - It does not test "any decorrelated second model of similar accuracy" (H024 §Batch's own wording). The twin is similar in accuracy and dissimilar in decorrelation.
  - Its reading is restated in H028 (`H024_review_v1.md`, revision 2).
- **Keep it last in the queue,** so it never displaces rungs B and C.
- **The provenance of the subsampling values is uncited.** "LightGBM's conventional subsampling defaults in its documentation examples" has no citation, and LightGBM's own defaults are 1.0, 1.0 and 0. Cite the source, or state 0.8/0.8/1 as a fixed a-priori choice. Non-blocking.
- **Clerical.** The text says "three changes", but four keys change (the three subsampling keys and the seed). Treating them as one perturbation is fine; say so.

## Novelty Relative to Existing Research

- **New:** no subsampled LightGBM and no same-family average exists in the journal.
- **Not redundant** with E026/E027 (byte-identical reproductions) or E029.

## Experimental Isolation

- **Against E029:** one conceptual change (subsampling, with its seed).
- **Same features, learner, shape, rounds, binning, routing and environment.**

## Validation Quality

- **All 8 folds,** with H predicted and never scored.
- **Route check against E029** at 1e-6 s. Exact equality is expected: the same ridge on FS2 in the same environment.
- **`compare.py <H027> E029`** and the residual correlation (revision 5 adds the readings' population).
- **H027 has no reading of its own,** which is correct for a component.

## Leakage Review

### Target Leakage

PASS

There is no new input, and the training rows are the same.

### Temporal Leakage

CONCERN

Inherited and not blocking: FS2's T features, and post-validation training months in S1 and W1. The twins bound them.

### Competition Availability

PASS

As E029 (FS2 at prediction time; SUBMIT folds predictable).

## Compute Review

### RAM

PASS

About 6.6 GB (E029 6.60 GB), inside CLASS-M's 8 GB. Bagging buffers are small.

### Runtime

PASS

- CLASS-M is right: E029 took 893 s, and the timeout is 2,700 s.
- **The window margin is thin.** The 950 s pessimistic figure is 6 % above E029's measured 893 s, and the speed-up from subsampling is assumed. If it overruns, the run can extend past 21:30 (revision 7(b)).

### Disk

PASS

About 60 MB.

## Weakest Assumption

**That a 0.8/0.8 twin is a meaningful averaging partner.** Its disagreement with E029 is expected to be about an order of magnitude below E031's, so its blend's failure is predicted before it runs.

## Missing Control or Ablation

- **For H027 as a component:** none (E029 is its partner).
- **For the family question it feeds:** see `H024_review_v1.md` (a same-family half on E031's inputs or at E031's disagreement). Named, not required.

## Decision

REVISE

## Execution Authorization

Authorized scope:
- **None.** REVISE never permits execution.

Required acknowledgement path:
- None for v1.
- After an ACCEPT of v2, it is `research/day-06/acks/H027_ack_v2.md`.

## Revision

**Required.**
1. **The seed.** Use a seed admitted by `check_config` for the allocation's purpose (frozen `promotion.reproduction`), and state it with its purpose. Seed 44 is refused.
2. **The §Batch revisions** 1, 5, 6 and 7 of `H024_review_v1.md`, through a pointer to the revised §Batch.

**Recommended (non-blocking):**
- cite the subsampling values, or state them as a choice;
- write "four keys, one perturbation" instead of "three changes";
- justify the 950 s pessimistic figure from measured values, or widen it.

**Binding:** the ruling in `H024_review_v1.md`.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| As written (seed 44): the runner refuses the run | 0.99 |
| Revised: H027 − E029 < 0 on all rows (point) | 0.55 |
| Revised: \|H027 − E029\| < 1.0 s on all rows | 0.85 |
| Revised: route check passes | 0.99 |
| Revised: runtime above 950 s | 0.10 |

Expected magnitude:
- **H027 − E029, all rows:** −0.9 to +0.7 s (central −0.1).
- **Development mean:** 441.6–443.2 s.
- **Residual correlation with E029:** all rows 0.996–0.999; bulk 0.985–0.997; `NM_present_excl_LIRF` 0.985–0.997.
- **Runtime:** 650–900 s (central 760 s).

Primary expected failure mode:
- **As written:** the run is refused at start and rung A is lost from the window.
- **Revised:** the twin is nearly identical to E029, so H028's gain is the generic-averaging floor (below 1 s), as constructed.
