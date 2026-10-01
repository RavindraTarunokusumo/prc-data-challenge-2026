---
schema: advisor-review-v1
hypothesis_id: H022
proposal_version: 3
proposal_sha256: 43526f13c690193fe06fcc65b6fd32de6247d83a40178cdf81a0c6c9ccc9d95b
exchange_id: X-D05-S04-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.90
created_utc: 2026-10-01T20:35:39Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.90).**
- v3 meets both required revisions of `H022_review_v2.md`.
- The comparability check is now closed, evidenced and decisive, and the freeze is anchored to the commit that contains the code.
- The v2-to-v3 diff changes nothing else.

**v2 required revisions:**

| v2 item | v3 | Verdict |
|---|---|---|
| 1. Comparability check | A closed exempt set of 13 keys under option (i), with a rationale. Evidence: `cb_param_diff.json`. Any other difference means not matched, and H021's clause 1 is INCONCLUSIVE | **Met** (verified below) |
| 2. Tools freeze | As H021 v3 | **Met.** Anchor `803ceeb` (`H021_review_v3.md`) |

**Verified here.** All checks are read-only: no real target read, no fit, no metric.

**The closed set equals the recorded difference, key for key.** In `cb_param_diff.json`:
- **Differing:** `cat_mode`; `data_partition` (FeatureParallel against DocParallel); `n_cat_features` (9 against 0).
- **Only in ctr:** `combinations_ctr`, `counter_calc_method`, `ctr_history_unit`, `ctr_target_border_count`, `fold_permutation_block`, `has_time`, `max_ctr_complexity`, `one_hot_max_size`, `permutation_count`, `simple_ctr`.
- **Only in codes:** none.
- **The other 45 shared keys are equal.** Among them: `random_seed`, `iterations`, `learning_rate` (float32 0.08), `depth`, `max_leaves`, `border_count`, `feature_border_type`, `l2_leaf_reg`, `bootstrap_type`, `bagging_temperature`, `random_strength`, `score_function`, `leaf_estimation_method`, `nan_mode`, `boosting_type`, `grow_policy` and `gpu_ram_part`.
- **Count:** 58 keys resolved in ctr mode, 48 in codes mode. The 13 keys found are the 13 exempt keys.

**The evidence is of the exact pair, and target-free.**
- `scripts/diag_cb_params.py` fits `calibrate_gpu.H021`, which equals H021 v3's table key for key. It runs with `iterations` 20, in both `cat_mode` values, through `routed.routed_catboost` (the worker's path).
- The frame is R3's, with the training target replaced by a permutation of itself (rng seed 0). Validation targets are null in the masked view. No metric is computed.
- The script refuses to run while an experiment holds the lock (INC-0008).

**The codes arm resolves no CTR key,** so the CTR parameters left in its configuration are inert, as the proposal states.

**Non-blocking execution note:**
- **The evidence is one fold at 20 iterations.** Every key outside the set is either set explicitly, or a fixed default that does not depend on fold size or iteration count. I expect the same difference on all 8 folds at 1,000 iterations (P ≈ 0.97).
- **If a fold shows another key,** clause 1 is INCONCLUSIVE by the proposal's own rule. That is the conservative direction.
- **Recording:** the per-fold record of the check is described in `H021_review_v3.md` (execution note 1).

## Scientific Validity

### (a) What the control removes

As in v1 and v2: every CTR, frequency, combination and one-hot encoding. The codes are quantized at 254 borders. What alphabetical order carries is stated.

### (b) The `data_partition` rationale is sufficient for option (i)

`H022_review_v2.md` (b)(i) allowed exempting `data_partition` "with the argument that on one device it selects a data layout, not model capacity". v3 gives that argument, and it holds:
- **CatBoost sets the key from the presence of categorical features.** The recorded pair differs in nothing else that bears on capacity.
- **On one device both layouts hold every document and every feature.** What can differ is the order of float reductions and the consumption of random streams.
- **Both are noise of the kind CatBoost GPU already shows across identical fits.** In `gpu_calibration.json` (verified):
  - 5 of the first 6 CatBoost GPU configurations differ between two identical fits;
  - so do both exact configurations: `h021_exact` (FeatureParallel) and `h022_exact` (DocParallel).
- **Forcing one value** would put one arm in a layout CatBoost does not choose for it. That would make the arms no more alike in capacity.

### (c) The check is decisive

- The set is closed and was written before the run.
- Every exempt key is tied to the treatment.
- Any other key, or a key present in one arm only, makes the pair not matched, and H021's clause 1 is INCONCLUSIVE.
- "Nothing outside this list is exempt" removes the post hoc reading v2 warned about.

### (d) Role and run order

Unchanged: first in the chain, a reference only, never NEW, with no claim of its own.

## Novelty Relative to Existing Research

This is the first within-learner contrast of categorical handling in the project: Missing Control 3's "contrast whose only difference is the categorical handling, at fixed capacity".

## Experimental Isolation

- **One parameter against H021:** `cat_mode`. Verified in code, in the test and in the recorded resolution.
- **Its consequences** are classified before the run, as a closed list.

## Validation Quality

- **Folds.** The frozen folds are used unchanged: all 8, with H predicted only.
- **Reported comparisons** against E029 are family contrasts.
- **No reproduction.** H021's reproduction supplies the noise scale (accepted in v1 and v2).

## Leakage Review

### Target Leakage

PASS

- The codes come from the fold's training vocabulary. Validation-only levels are NaN.
- No target is involved.
- The diagnostic used a permuted training target and computed no metric.

### Temporal Leakage

CONCERN

This is carried, not blocking. FS2's T features are unchanged from H015 v2.

### Competition Availability

PASS

The raw keys are label P. Unseen 2026 levels become NaN; their shares are recorded under H021's rule 2.

## Compute Review

### RAM

PASS

- **Expected:** 5.5–7.0 GB at the H fold, inside CLASS-M's 8 GB.
- **Swap:** recorded (INC-0010).

### Runtime

PASS

8–14 min (CLASS-M).

### Disk

PASS

About 15 MB.

## Weakest Assumption

**That integer codes are information-poor.**
- The naming hierarchy and the 1:1 bins of the low-cardinality keys give the codes arm more than assumed.
- H021's clause 1 is therefore likely decided near its floor.

## Missing Control or Ablation

None beyond what H022 is.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
1. **One allocation,** `gate.py allocate H022 v3`, first in the chain. Config:
   - H021 v3's, with `cat_mode: codes`;
   - every other key identical, the inert CTR keys included;
   - `feature_set: FS2_RAW`, `folds` all 8, `seed: 42`, `job_class: CLASS-M`.
2. **Post-run steps** of the Validation Plan:
   - `route_check.py <H022> - E029`;
   - `compare.py <H022> E029` (reported);
   - `range_check.py <H022> E029 --bands`;
   - swap use;
   - after H021, the comparability check under the closed set.
3. **Preconditions:** as `H021_review_v3.md`, Execution Authorization item 4:
   - anchor `803ceeb` for every path outside the record directories;
   - rule L v2 item 6's environment;
   - a clean tree, and no experiment running.
4. **Not authorized:**
   - a reproduction;
   - any parameter change;
   - a retry after RESOURCE_FAILURE without a new version. Such a failure stops the chain;
   - holdout access;
   - H022 as NEW or as a candidate.

Required acknowledgement path: `research/day-05/acks/H022_ack_v3.md`. It references the proposal hash above and this review's hash.

## Revision

None required.

## Advisor Prediction

These are for this v3 run.

Probability of improvement:

| Event | P |
|---|---|
| H022 − H021 development mean above +3.0 s on `NM_present_excl_LIRF` (the mirror of H021's clause 1 not met) | 0.60 |
| H022's development mean below E029's 442.5 s | 0.03 |
| H022 passes `route_check.py <H022> - E029` on all 8 folds | 0.95 |
| The closed-set check flags a key outside the set, on any fold | 0.03 |
| H022 ends in RESOURCE_FAILURE | 0.03 |

Expected magnitude:
- **H022 − H021, `NM_present_excl_LIRF`:** +1 to +10 s (central +5).
- **H022 − E029, `NM_present_excl_LIRF`:** +5 to +20 s (central +11).
- **Development mean:** 448–468 s (central 456).
- **Runtime:** 8–14 min.
- **Peak RSS:** 5.5–7.0 GB.

Primary expected failure mode: the codes arm recovers part of the keys' signal through the naming hierarchy, and H021's clause 1 is decided near its floor.
