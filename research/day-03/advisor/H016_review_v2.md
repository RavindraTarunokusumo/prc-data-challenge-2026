---
schema: advisor-review-v1
hypothesis_id: H016
proposal_version: 2
proposal_sha256: 7f44ac059e993f55a8a70913d011647737795e1e3a162068366fb574335ff58b
exchange_id: X-D03-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.88
created_utc: 2026-09-29T16:29:06Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.** H016 v2 runs as H015 v2's chain step 2. It is a reference and ablation only: not a candidate, not reproduced, and never NEW in a holdout access.

**The v1 REVISE was coupling, not a defect of H016's own, and the coupling is resolved.**
- H015 v2's clause 2 is now registered on a population that is decisive against known records (`H015_review_v2.md` (a)).
- H016 runs only after H015's primary and its step 1 comparisons. Outside the routed subgroup it reveals nothing that H015's own outputs do not already show.

| v1 required revision | Status in v2 | How it was verified |
|---|---|---|
| 1. Re-point to H015's revision | **Done** | Chain step 2, H015 v2's preconditions and tools list, FS2 at `63923e2` |
| 2. One population | **Done** | The reported C check is `mechanism_check.py <H016> E017 NM_present_excl_LIRF`. `excl_LIRF_NM_missing` stays as an extra disclosure |
| 3. Corrected forward-risk figures | **Done** | 52–337 rows per month in 2025, 107 and 276 in the ranking months, and a rate of 0.35–0.83. They match `fs2_v2_checks.json` and the Day 1 phase close |

- **The "acceptable as is" items are unchanged** (diff against v1): the role, the run order, `route_check.py`, the R-effect and criterion 8 disclosure expectations, and the "whatever its sign" rule 11 statement.
- **Changed expectations.** The all-rows expectation moved from −3 to −20 s to −2 to −15 s, before any run. That is permitted.

**Verified here.**
- The proposal hash matches the envelope.
- **Code-path identity.**
  - `lightgbm` and `routed_lightgbm` call the same `gbm.lightgbm`, with the same parameters (minus `route_ridge_params`), on the same FS2 frame, through the same worker.
  - There is no feature cache.
  - `deterministic`, `force_row_wise` and 4 threads are pinned.
- **FS2 frames** (target-free, real W1c and S1 views): FS1's columns and their order are unchanged, and the 15 congestion columns follow them. The shared checks are listed in `H015_review_v2.md`.

## Scientific Validity

- **The R ablation is exact.** H015 − H016 differs only on LIRF NM-missing rows, provided `route_check.py` 3(b) holds.
- **The R-effect expectations are well founded.** They are unchanged from v1: full subgroup dRMSE > 0 on at least 3 of 5 development folds, and bulk < 0 on S1.
- **The all-rows contrast (rule 11) mixes two things.**
  - For NM-missing rows, the T windows start at SCHED, so the in-taxi counts re-encode the schedule delay.
  - Target-free, NM-missing training rows with more than 100 takeoffs during taxi number 1,137 (R1), 1,365 (R2), 1,512 (R3), 1,082 (S1), 1,492 (W1), 603 (S1c) and 120 (W1c). NM-present training rows above 100 number 0–4 per fold.
  - The all-rows sign can therefore be set by LIRF convention records and by late departures at the nine other airports, not by queueing. The "whatever its sign" rule is the right protection.
- **The criterion 8 disclosure** (+6,000 to +8,000 s on S1) is consistent with the Day 2 sensitivities (static keys +717 s, procedure +714 s on FS1).
- **Record note.** The development-mean expectation (360–380 s) is looser than the stated dRMSE range: −2 to −15 s against E017's 378.82 implies 363.8–376.8 s. The two ranges should coincide, because the development mean equals E017's plus the mean dRMSE. No clause depends on it.

## Novelty Relative to Existing Research

- **FS2 is a new configuration.**
- **Standing rule 10 is not engaged:** H016 is a reference, never a candidate.

## Experimental Isolation

| Contrast | Population | Only difference | Status |
|---|---|---|---|
| H015 − H016 | `LIRF_NM_missing` | The routing | Exact |
| H015 against H016 | All other rows | None (identity check) | Exact: `max \|Δ\| == 0` by `route_check.py` |
| H016 − E017 | `NM_present_excl_LIRF` | + 15 congestion columns | Equal to H015 − E017 there, if 3(b) holds |
| H016 − E017 | All rows (rule 11) | Same | Isolated. The sign may be set by NM-missing rows (above) |
| H016 − E017 | `excl_LIRF_NM_missing` | Same | Disclosure. Row 192622644 may dominate S1 and S1c, as pre-registered |

## Validation Quality

- **Folds.** The frozen folds are used unchanged, H is predicted only, and H016 is never NEW.
- **Reproduction.** Not reproducing a reference is consistent with Day 2 practice.
- **Rule 11 holds.** The C check uses H015 v2's single clause population, and the all-rows figure is reported next to it.
- **The rule 6 expectations are consistent with the evidence.**
  - On all rows, 183903219 (W1, LIRF NM-missing; E017 predicted 29,744 s against E005's 1,798 s) and 192622644 (S1, S1c) may dominate.
  - On `NM_present_excl_LIRF`, dominant rows are expected only on folds with a near-zero net change (`H015_review_v2.md` (b)).

## Leakage Review

### Target Leakage

PASS

The inputs are FS2's, as in `H015_review_v2.md`.
- No input reads a DEP block time or target.
- There is no target statistic.

### Temporal Leakage

CONCERN

These are label notes, not blocking.
- **The five T features are admissible** (§6.2) and target-revealing through the interval length.
- **The ten P features are now P,** as verified in `H015_review_v2.md` (e).

### Competition Availability

PASS

Every input is present for ranking DEP rows.

## Compute Review

### RAM

PASS

5–6.5 GB expected, as H015's LightGBM part without the ridge.

### Runtime

PASS

16–24 min: 32 inputs against E017's 17, with no ridge. That is within CLASS-M.

### Disk

PASS

About 10 MB of predictions.

## Weakest Assumption

**That H016 − E017 on all rows says something about congestion.**
- On all rows, LIRF NM-missing rows carried 0.17–0.73 of each Day 2 fold's SSE change against E005.
- The T counts re-encode `d_sched` on every NM-missing row.
- The all-rows figure is a disclosure, reported whatever its sign. It is not evidence for or against C.

## Missing Control or Ablation

None. H016 is itself the R ablation and the rule 11 reference.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions:** those of `H015_review_v2.md` 1(a)–(d). In addition, H015 v2's primary run is complete and its chain step 1 comparisons are written.
2. **One primary run.**
   - `model: lightgbm`, `feature_set: FS2`.
   - `params`: E017's exactly (`objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 1.0`, `bagging_fraction: 1.0`, `bagging_freq: 0`, `bin_construct_sample_cnt: 5000000`, `num_threads: 4`, `num_boost_round: 1000`).
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
3. **Comparisons:**
   - `compare.py <H016> E017` and `compare.py <H016> E005` (rules 1, 6, 7; criterion 8 disclosure);
   - `mechanism_check.py <H016> E017 NM_present_excl_LIRF`;
   - `mechanism_check.py <H016> E017 excl_LIRF_NM_missing` (disclosure);
   - then `route_check.py <H015> <H016> E005` and `mechanism_check.py <H015> <H016> LIRF_NM_missing`.
4. **Infrastructure failure.** One identical re-run with `--purpose rerun`, logged, only after an infrastructure failure. A RESOURCE_FAILURE or TIMEOUT is recorded and not retried.
5. **Recording:** as in `H015_review_v2.md` item 8 (CPU model, any intervening container restart, INC-0004).
6. **Not authorized:**
   - a reproduction;
   - any use as a promotion candidate or as NEW in a holdout access;
   - scoring H;
   - any change to features, parameters, folds or seed;
   - any code change during the chain (the scope limit in `H015_review_v2.md` item 9).

Required acknowledgement path: `research/day-03/acks/H016_ack_v2.md`.
- It references the proposal hash (`7f44ac05…`) and this review's hash.
- It adopts the preconditions and the scope limit.
- It records the development-mean note under Scientific Validity as a record note.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| H015 − H016 on `LIRF_NM_missing`: full dRMSE > 0 on at least 3 of 5 development folds | 0.90 |
| H015 − H016 on `LIRF_NM_missing`: bulk dRMSE < 0 on S1 | 0.95 |
| H015 and H016 identical outside the subgroup on all 8 folds | 0.95 |
| H016 − E017 on all rows: development mean < 0 (point estimate) | 0.55 |
| Criterion 8 statistic against E005 on S1 within +6,000 to +8,000 s | 0.55 |
| H016 development mean within 360–380 s | 0.75 |

Expected magnitude:
- **H016 − E017 on all rows:** −8 to +6 s development mean, sign undetermined. Per fold, LIRF NM-missing rows can move it by tens of seconds.
- **On `NM_present_excl_LIRF`:** identical to H015 − E017.
- **S1 criterion 8 statistic against E005:** +6,300 to +7,800 s.

Primary expected failure mode:
- The rule 11 all-rows figure is set by convention records and late NM-missing departures, through the T counts' re-encoding of `d_sched`. It is then uninformative about congestion in either direction. That is a reading hazard, not a defect: the proposal reports the figure whatever its sign.
