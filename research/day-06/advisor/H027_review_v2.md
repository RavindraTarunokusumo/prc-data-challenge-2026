---
schema: advisor-review-v1
hypothesis_id: H027
proposal_version: 2
proposal_sha256: eb9168eaef588209b22946f6cde4f4b68bcac8ebada5fe1c171ae559912ccc95
exchange_id: X-D06-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.90
created_utc: 2026-10-02T18:08:13Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.90).** Delta review against `H027_review_v1.md`.

**The blocking item is fixed.**
- The seed is now **42**, the frozen `primary_seed`, under purpose `primary`. The Implementation Plan states the purpose.
- `scripts/run_experiment.py::check_config` reads the purpose from `gate.json`. Every purpose except `reproduction` requires 42, and `gate.py allocate` defaults to `primary`. So the runner admits the run.
- Seed 44 would have been refused before RUNNING.

**The other required item is met:** the pointer to `H024_v2.md` §Batch, which carries §Batch revisions 1, 5, 6 and 7.

**All three recommended items are adopted:**
- the 0.8 values are stated as the researcher's a-priori choice;
- the text says "four keys changed, one perturbation";
- the pessimistic runtime is widened to 1,100 s (E029's measured 893 s × 1.23), and the subsampling speed-up is not assumed.

**The config differs from E029's in exactly four keys:** `feature_fraction` 0.8, `bagging_fraction` 0.8, `bagging_freq` 1 and `seed` 42 (was 43). Everything else is identical, compared line by line against `experiments/E029/config.yaml`.

**Conditions C1–C7 of `H024_review_v2.md` apply.**

## Scientific Validity

- **The seed change is inert for E029.**
  - E029 has no subsampling and runs with `deterministic=True` and `force_row_wise=True`.
  - Every training fold is below `bin_construct_sample_cnt` (5,000,000; S1, the largest, has 1,537,475 rows).
  - The routed ridge gives identical rows across seeds: E030 and E031 at seed 42 against E029 at seed 43 show 0.0 on all folds.
- **So in H027, seed 42 drives only the bagging and feature-fraction draws.** `gbm.lightgbm` sets LightGBM's `seed` from the config, and LightGBM derives its bagging and feature-fraction seeds from it.
- **The twin is one realization.** It is reproducible on the laptop at seed 42, but it is one draw of the subsampling. Rung A's floor is recorded "at seed 42" (`H024_review_v2.md`, Scientific Validity (e)). This cannot move rung A's reading.
- **Its information value is modest and stated as such.** The Alternative Explanations entry now says a failure means "this much same-family diversity is not enough", not "no LightGBM could".
- **When curves are recorded,** the training set is passed as its own eval set (`gbm.lightgbm`). This records metrics only and leaves the trees unchanged, with bagging as without it.

## Novelty Relative to Existing Research

New. The journal holds no subsampled LightGBM and no same-family average. The run is not redundant with E026/E027 (byte-identical reproductions) or with E029.

## Experimental Isolation

- **Against E029:** one conceptual perturbation (subsampling with its seed).
- **Unchanged:** features, learner, tree shape, rounds, binning, routing and environment.

## Validation Quality

- **All 8 folds,** with H predicted and never scored.
- **Route check against E029** at 1e-6 s. Exact equality is expected: the same fold-local ridge on bit-identical FS2 inputs.
- **`compare.py E038 E029`, and residual correlations** on `NM_present_excl_LIRF`, all rows and bulk (C4 for the code).
- **H027 has no reading of its own,** which is correct for a component.

## Leakage Review

### Target Leakage

PASS

There is no new input, and the training rows are the same.

### Temporal Leakage

CONCERN

Inherited and not blocking: FS2's T features, and post-validation training months in S1 and W1. S1c and W1c bound them.

### Competition Availability

PASS

As E029: FS2 is available at prediction time, and the SUBMIT folds are predictable.

## Compute Review

### RAM

PASS

About 6.6 GB (E029 6.60 GB), inside CLASS-M's 8 GB. Bagging buffers are small. The run is never concurrent with the GPU run (INC-0012).

### Runtime

PASS

- **CLASS-M is right.** My central estimate is 700 s (600–880 s). The 1,100 s guard is a safe bound, and the timeout is 2,700 s.
- **Fit to the window.** It must start by 21:11:40, so E036 has to finish in about 9.5 min, including overheads. P ≈ 0.5.
- **If deferred, it runs at the owner's next window** under C3. Otherwise it is recorded "not run (window)".

### Disk

PASS

About 60 MB.

## Weakest Assumption

**That a 0.8/0.8 twin is a meaningful averaging partner.**
- Its disagreement with E029 is expected to be about an order of magnitude below E031's.
- The v2 text now treats it as a floor measurement, not as a test of "any decorrelated second model".

## Missing Control or Ablation

- **For H027 as a component:** none (E029 is its partner).
- **For any learner-family question:** a same-family half on E031's inputs, or at E031's disagreement level. This is named, not required, and v2 no longer makes the claim.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Exactly one allocation,** `uv run python scripts/gate.py allocate H027 v2` (purpose `primary`).
  - It is made fourth in the batch, so it is expected to be **E038**.
  - The config is the Proposed Change block: seed 42, CLASS-M, all 8 folds.
- **It runs by the pinned launcher if it fits the start rule.** Otherwise it runs at a later window under C3 of `H024_review_v2.md`.
- **It is a component only.** It has no reading of its own, is not a candidate, and gets no holdout access.
- **Conditions C1–C7 of `H024_review_v2.md` apply.**

Required acknowledgement path:
- `research/day-06/acks/H027_ack_v2.md`, referencing the proposal hash `eb9168eaef588209b22946f6cde4f4b68bcac8ebada5fe1c171ae559912ccc95` and this review's hash.

## Revision

None required.

## Advisor Prediction

Probability of improvement:

| Event (H027 = E038) | P |
|---|---|
| Runner admits the run (seed 42, purpose `primary`) | 0.99 |
| H027 − E029 < 0 on all rows (point) | 0.55 |
| \|H027 − E029\| < 1.0 s on all rows | 0.88 |
| Runs in today's window | 0.50 |
| Runtime above 1,100 s | 0.03 |
| Status other than COMPLETE, if started | 0.02 |
| Route check passes | 0.99 |

Expected magnitude:
- **H027 − E029, all rows:** −0.8 to +0.7 s (central −0.1).
- **Development mean:** 441.7–443.2 s.
- **Residual correlation with E029:** all rows 0.996–0.999; bulk 0.985–0.997; `NM_present_excl_LIRF` 0.985–0.997.
- **Resources:** runtime 600–880 s (central 700 s), peak RAM about 6.6 GB.

Primary expected failure mode:
- **The run misses today's window,** because E036 takes longer than about 9.5 min.
- **It is then deferred.** It runs at the owner's next window under C3, or is recorded "not run (window)", with nothing inferred.
- **If it runs,** the twin is nearly identical to E029, as constructed.
