---
schema: advisor-review-v1
hypothesis_id: H021
proposal_version: 3
proposal_sha256: b8618266bf2cd259415ab3879435d5f016f8dee780a50c798d1b6cba68a19716
exchange_id: X-D05-S04-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.88
created_utc: 2026-10-01T20:35:39Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.88).**
- v3 meets the three required revisions of `H021_review_v2.md`.
- It carries the CLASS-L ruling and its five conditions unchanged.
- The v2-to-v3 diff changes nothing else: only the revisions, the version fields and references.

**v2 required revisions:**

| v2 item | v3 | Verdict |
|---|---|---|
| 1. Comparability, jointly with H022 v3 | H022 v3's closed exempt set is adopted. No key is equalized, so the parameter table is unchanged. Clause 1 is INCONCLUSIVE only under that set (besides the noise condition) | **Met.** The set equals the recorded key difference of the exact pair, key for key (`H022_review_v3.md`) |
| 2. Tools freeze | Anchored to the X-D05-S04-0003 submission commit. `src/`, `scripts/`, `pyproject.toml` and `uv.lock` are frozen, with `linear.py`, `attribution.py` and `data.py` named. Run commits differ only in records, and each analysis states the diff | **Met.** The anchor is `803ceeb` (below) |
| 3. Reproduction integrity | `route_check.py <H021r> - E029`. A failure makes H021r INVALID for all-rows comparisons and as H023r's component. The noise condition is unaffected | **Met** |
| CLASS-L conditions 1–5 | No parameter changes; the CLASS-M comparison and swap use beside criterion 7; H023 reads CLASS-L | **Met** |

**Verified here.** All checks are read-only: no real target read, no fit, no metric.
- **Hashes.**
  - All three v3 proposals match the envelope.
  - The v2 reviews, acks and proposals match the X-D05-S04-0002 result.
- **Lock.** `runtime/experiment.lock` (content `E029`) is held by no process (`/proc/locks`), and no experiment is running.
- **Anchor.** `803ceeba5965bd7c0d415eb44a13d6921854f6eb` adds this envelope and the three v3 proposals, and HEAD is that commit with a clean tree. Since `60365dd` (the code reviewed in v2), it changes two pieces of code:
  - `scripts/diag_cb_params.py` (new; it generated the comparability evidence);
  - `prc.worker.environment()` (+20 lines), which writes the lock hash, eight library versions and the `*_THREADS` variables into each manifest.
- **The worker change is record-only.**
  - It runs after every fit, and after `metrics.json`, `curves.json` and `resolved_params.json` are written. It cannot change a prediction.
  - `tests/test_worker.py::test_worker_end_to_end` passes (synthetic data; 0.3 GB).
  - In this venv the record reads CPython 3.13.15, polars 1.44.2 (16 threads), numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, LightGBM 4.7.0, CatBoost 1.2.10 and lock `efa4fd78eaa6…`. That is rule L v2 item 6.
  - Its imports add about 37 MB at the end of a run.
  - It records no secret: versions, a hash and thread variables only.
- **`uv.lock`** is unchanged since `261477c`.
- **No allocation since E029** (task ledger). No v2 proposal was run.

**Non-blocking execution notes (not revisions):**
1. **No frozen tool performs the comparability check.** No script compares two runs' `resolved_params.json`.
   - Under a closed set the check is mechanical, so an ad hoc comparison is acceptable.
   - The analysis must record its full output, in `cb_param_diff.json`'s form: per fold, for all 8 folds, the differing keys and the keys present in one arm only.
2. **The freeze's verification is narrower than its rule.**
   - The rule lets run commits differ from the anchor only in `research/`, `experiments/`, `orchestration/` and `docs/`.
   - The stated `git diff --stat` covers `src scripts pyproject.toml uv.lock` only.
   - The runner reads `config/resources.yaml` (class limits, and so criterion 7).
   - The rule binds as written (Execution Authorization 4). A diff over everything outside the four record directories would verify it.
3. **Edge case.** If H021r ends in RESOURCE_FAILURE, the noise condition has no input. Clause 1 is then reported without a verdict (neither met nor not met), and the chain stops, as the proposal states.

## Scientific Validity

### (a) The science is unchanged and sound

All of these stand as accepted in v1 and v2:
- the research question and mechanism;
- FS2_RAW and the single a-priori configuration;
- H022 as the control;
- clause 1's floor, its readings and "at this budget";
- the noise condition and the integrity clause.

### (b) The comparability check is now decisive

- **The exempt set** is 13 keys, closed and fixed before the run. Each key is tied to the treatment (ruled in `H022_review_v3.md`):
  - the treatment itself: `cat_mode`, `n_cat_features`;
  - the CTR machinery's own settings: 10 keys that CatBoost resolves only when categorical features are declared;
  - one layout choice CatBoost makes from the presence of categorical features: `data_partition`.
- **Any other difference** (a differing key, or a key in one arm only) means not matched, and clause 1 is INCONCLUSIVE. The researcher has no choice to make after the run.
- **The parameter table is untouched.** The CLASS-L evidence (`h021_exact`) still describes this configuration.

### (c) The freeze protects the reviewed code

- The anchor contains all the code the chain runs (verified).
- It names the ridge, the clause populations and the loader, which v2 found missing.
- Together with rule L v2 item 6's environment, it fixes for the whole chain:
  - the integrity reference (E029's routed rows);
  - clause 1's population;
  - the instances.

### (d) The reproduction feeds H023r cleanly

- The reproduction now has its own integrity check, with a scoped consequence.
- The noise condition reads `NM_present_excl_LIRF`, which has no LIRF rows, so a routed-row failure in H021r cannot touch it.

## Novelty Relative to Existing Research

Unchanged.
- **This is the first CatBoost run with the matched control** the Day 4 review asked for (Missing Control 3).
- **It is not redundant with H019** (explicit fold-local priors) **or H020** (rejected; its objections are answered).

## Experimental Isolation

- **Against H022: one parameter,** `cat_mode`, plus what it entails, now a closed list of resolved keys.
- **`data_partition`** follows from declaring categorical features.
  - On one device it changes the data layout, and with it the order of float reductions and random draws.
  - It does not change the tree family, depth, borders, leaf estimation or regularization. All of those are equal in the recorded pair.
  - A random-stream effect is noise of the kind the seed-43 reproduction measures for this arm.
- **Against E029: not isolated,** and not claimed to be.

## Validation Quality

- **Folds.** The frozen folds are used unchanged: all 8 predicted, H predicted only, no holdout use.
- **Clause 1** runs through `mechanism_check.py`: the frozen `promotion_check` on the population, with counted WINs among R1, R2, R3, S1 and W1. It is read at this budget, with both arms' 800–1,000 slopes recorded.
- **INCONCLUSIVE has exactly two sources,** both closed before the run:
  - the noise condition (the H021r − H021 mean beyond 1.5 s);
  - the closed comparability set.
- **The unconditional reproduction** gives the noise scale.

## Leakage Review

### Target Leakage

PASS

- The CTRs come from training rows only, over permutations. Validation rows have null targets in the masked view.
- FS2_RAW uses no target, and no validation row.
- The new diagnostic used a permuted training target (rng seed 0) and computed no metric.

### Temporal Leakage

CONCERN

This is carried, not blocking.
- FS2's T features are as disclosed in H015 v2.
- In S1 and W1, the CTR statistics include post-validation training months, by the frozen fold design. The S1c and W1c cells are reported beside them.

### Competition Availability

PASS

- The raw keys are label P and present in the ranking files.
- Levels unseen in a fold's training rows become `__NULL__`. The 2026 shares are recorded target-free (rule 2).

## Compute Review

### RAM

PASS

- **Estimate:** 6.0–7.5 GB, as in v2. The environment record adds about 37 MB at the end of the run.
- **Swap:** recorded. Under INC-0010, a run that swaps is not called within class on RSS alone.

### Runtime

PASS

**CLASS-L, as ruled in `H021_review_v2.md`, for H021 and H021r only.**
- **Expected:** 28–35 min, with P(> 30 min) ≈ 0.65. The runner's CLASS-L timeout is 135 min.
- **Conditions:** the ruling's conditions 1–5 apply unchanged.

### Disk

PASS

About 15 MB, covered by the manifest.

## Weakest Assumption

**That integer codes are an information-poor control** (unchanged).
- The naming hierarchy, and the 1:1 bins of the low-cardinality keys, give the codes arm more than assumed.
- Clause 1 is therefore likely decided near its −3.0 s floor.

## Missing Control or Ablation

- **None for clause 1:** H022 is the control.
- **The E029 + H022 blend** is the H023-level control. It is named there, and not required under H023's scoped claim.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
1. **Primary run.** One allocation, `gate.py allocate H021 v3`, after H022 v3's run has completed (not RESOURCE_FAILURE). Config:
   - `model: routed_catboost`, `feature_set: FS2_RAW`, `folds` all 8, `seed: 42`, `job_class: CLASS-L`;
   - the parameters exactly as in the proposal's table:
     - `loss_function` RMSE, `task_type` GPU, `devices` "0";
     - `depth` 8, `iterations` 1000, `learning_rate` 0.08, `border_count` 254, `l2_leaf_reg` 3, `boosting_type` Plain;
     - `simple_ctr` and `combinations_ctr` [Borders, FeatureFreq, FloatTargetMeanValue], `max_ctr_complexity` 4;
     - `gpu_ram_part` 0.4, `thread_count` 4, `cat_mode` ctr;
     - `route_ridge_params` {alpha 1.0, winsor [0.005, 0.995]}, `route_train_exclude` true;
   - unlisted GPU defaults stay at default.
2. **Reproduction, unconditional.** One allocation, `gate.py allocate H021 v3 --purpose reproduction`: the same config with `seed: 43`, CLASS-L.
3. **Post-run steps:** exactly those of the Validation Plan, including:
   - the comparability check under H022 v3's closed set, recorded per fold for all 8 folds (execution note 1);
   - `route_check.py <H021r> - E029`.
4. **Preconditions for each run:**
   - a clean tree; no experiment running; nothing memory-heavy beside the run (INC-0008);
   - every path outside `research/`, `experiments/`, `orchestration/` and `docs/` equal to `803ceeb`, `config/` and `tests/` included. A difference there puts the run outside this authorization;
   - rule L v2 item 6's environment, confirmed from the manifest's `python`, `polars_threads` and `environment`.
5. **The CLASS-L conditions** of `H021_review_v2.md` (1–5) apply.
6. **Not authorized:**
   - any change of parameters or iterations, or early stopping;
   - a retry after RESOURCE_FAILURE (`gpu_failure`, a kernel OOM or the RSS guard) without a new version. Such a failure stops the chain;
   - any further fit of this configuration on a real fold;
   - holdout access;
   - H021 as NEW or as a promotion candidate.

Required acknowledgement path: `research/day-05/acks/H021_ack_v3.md`. It references the proposal hash above and this review's hash.

## Revision

None required. The execution notes in the Summary are not revisions.

## Advisor Prediction

These are for this v3 run.

Probability of improvement:

| Event | P |
|---|---|
| Clause 1 not met (H021 − H022 ≤ −3.0 s with ≥ 3 counted WINs) | 0.60 |
| The closed-set check flags a key outside the set, on any of the 8 folds | 0.03 |
| Clause 1 INCONCLUSIVE, for either reason | 0.15 |
| The noise condition triggers (reproduction differs by > 1.5 s) | 0.12 |
| H021 passes `route_check.py <H021> - E029` on all 8 folds | 0.95 |
| H021r passes its own route check, given that H021 passes | 0.98 |
| H021 − E029 below 0 on `NM_present_excl_LIRF` | 0.10 |
| Development-mean validation curve still falling by ≥ 0.5 s over iterations 800–1,000 | 0.65 |
| Prediction on row 192622644 below E029's 7,041 s | 0.60 |
| Runtime above 30 min | 0.65 |
| Runtime above 90 min | < 0.01 |
| Peak RSS above 8 GB | 0.08 |
| Any swap-out during the run | 0.10 |

Expected magnitude:
- **H021 − H022, `NM_present_excl_LIRF`:** −1 to −10 s (central −5).
- **H021 − E029, `NM_present_excl_LIRF`:** +3 to +14 s (central +7).
- **Development mean:** 446–458 s (central 450).
- **Runtime:** 28–35 min.
- **Peak RSS:** 6.0–7.5 GB.

Primary expected failure mode:
- The statistics help, but by less than pre-registered, because the codes arm recovers part of the naming hierarchy.
- Clause 1 is decided within about 2 s of −3.0 s.
