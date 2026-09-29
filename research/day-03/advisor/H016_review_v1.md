---
schema: advisor-review-v1
hypothesis_id: H016
proposal_version: 1
proposal_sha256: 604801ba34586a34965db0d669cec12a63c47de590b20a92241b39f8ab17902e
exchange_id: X-D03-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.80
created_utc: 2026-09-29T15:53:21Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE.** The revision is needed because of coupling to H015, not because of a scientific defect of H016's own.

**H016's content is sound.**
- It gives an exact ablation of R. `routed_lightgbm` calls the same `gbm.lightgbm` on the same FS2 frame through the same worker path. There is no feature cache, and `deterministic=True`, `force_row_wise=True` and 4 threads are pinned.
- It gives the all-rows congestion contrast that standing rule 11 requires.
- It discloses the unrouted criterion 8 statistic at July's rate.
- It adds a cross-process determinism check: H015 against H016 outside the subgroup.

**It is not executable as written.**
- Its chain position, preconditions and comparison populations are H015 v1's, and H015 v1 is REVISED (`H015_review_v1.md`).
- **Outside the routed subgroup, H016's predictions are H015's by construction.** Any H016 run before H015's clause 2 is re-registered would reveal H015's congestion outcome on every candidate population. H009 v2 raised the same hazard: no FS1-family run until the M1 clause was fixed.

**Verified here.**
- The proposal hash matches the envelope.
- The code path identity holds (`models/routed.py`, `models/gbm.py`, `worker.py`).
- The H015 review lists the shared checks.

## Scientific Validity

- **Mechanism.** "Congestion inputs may shift that mixture" is right.
  - For a row without `AOBT_3`, *t_off* = SCHED. The T counts then run over (SCHED, *t_to*) and grow with `d_sched`: M3 in another form.
- **This is not confined to LIRF.** Of the 1,086 S1 training rows with more than 100 takeoffs during taxi, 1,082 are NM-missing, and 1,020 of those are at the other nine airports (target-free).
  - The all-rows contrast H016 − E017 will therefore mix queueing with a re-encoding of schedule delay on NM-missing rows.
  - The "whatever its sign" reporting rule is the right protection.
- **The criterion 8 disclosure** (+6,000 to +8,000 s on S1) is consistent with the phase-close forecast (+6,400 to +7,800 s) and the measured S1 sensitivities (static keys +608/+717 s, procedure +605/+714 s).
- **The R-effect expectations are well founded.** Every Day 2 Tier 1 fit beat E005 on the subgroup's full RMSE through the convention tail and lost on its bulk (S1 +5,782 to +7,104 s). Positive full and negative bulk for H015 − H016 is the expected pattern.
- **The Observation defers to H015's forward-risk figures,** which are wrong (`H015_review_v1.md` (b)). It inherits the correction.

## Novelty Relative to Existing Research

- **New configuration:** FS2 has no precedent.
- **Rule 10 is not engaged:** H016 is a reference, never a candidate.

## Experimental Isolation

| Contrast | Population | Only difference | Status |
|---|---|---|---|
| H015 − H016 | `LIRF_NM_missing` | The routing | Exact |
| H015 against H016 | All other rows | None (identity check) | Exact; `max \|Δ\| == 0` by `route_check.py` |
| H016 − E017 | All rows (rule 11) | + 15 congestion columns | Isolated. Dominated by LIRF NM-missing rows (see Weakest Assumption) |
| H016 − E017 | `excl_LIRF_NM_missing` | Same | Equal to H015 − E017 there. Inherits H015's S1 exposure to row 192622644 |

## Validation Quality

- **Folds.** The frozen folds are used unchanged, H is predicted only, and H016 is never NEW.
- **Reproduction.** Not reproducing a reference is consistent with Day 2 practice.
- **Rule 11.** "Comparisons between contrasts use one population." The reported C check (`mechanism_check.py <H016> E017 excl_LIRF_NM_missing`) must use the population that H015's revised clause 2 uses. It may keep `excl_LIRF_NM_missing` as an additional disclosure.

## Leakage Review

### Target Leakage

PASS

The inputs are FS2's, as in `H015_review_v1.md`. No input reads a DEP block time or target.

### Temporal Leakage

CONCERN

- **As in H015.** The T features are admissible.
- **Five P-labelled features** carry the row's own takeoff time on 0.086 % of DEP rows (`H015_review_v1.md` (e)).

### Competition Availability

PASS

Every input is present for ranking DEP rows.

## Compute Review

### RAM

PASS

Under 7 GB, as H015's LightGBM part, without the ridge.

### Runtime

PASS

About 15–23 min. E017 took 668 s, with about 1.65 times the histogram cost for 38 inputs against 23.

### Disk

PASS

About 10 MB.

## Weakest Assumption

That H016 − E017 on all rows says something about congestion.
- On all rows, LIRF NM-missing rows (≤ 0.18 % of rows) carried 0.17–0.73 of each Day 2 fold's SSE change against E005.
- The congestion inputs re-encode `d_sched` on exactly those rows.
- The all-rows sign will likely be set by a few convention records. The proposal already commits to reporting it whatever its sign.

## Missing Control or Ablation

None beyond H015's. H016 is itself the R ablation.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- No allocation of H016 v1.
- No FS2 model may be fitted on a frozen fold before an H015 version ≥ 2 is ACCEPTED and acknowledged (`H015_review_v1.md`).

Required acknowledgement path: none for v1. Submit `research/day-03/proposals/H016_v2.md` in the same exchange as H015 v2.

## Revision

**Required (minimal):**
1. **Re-point to H015's revised version.**
   - Its chain step, preconditions and the FS2 definition must be H015's.
   - If H015 v2 re-implements the P features, H016 uses that FS2.
2. **One population.** Run the reported C check against E017 on the population that H015's revised clause 2 uses. `excl_LIRF_NM_missing` may remain as an extra disclosure.
3. **Carry H015 v2's corrected forward-risk figures** in the Observation.

**Acceptable as is:**
- the role (not a candidate, not reproduced, never NEW);
- the run order after H015's primary;
- `route_check.py` as the R integrity check;
- the R-effect and criterion 8 disclosure expectations;
- the "whatever its sign" rule 11 statement.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| H015 − H016 on `LIRF_NM_missing`: full dRMSE > 0 on at least 3 of 5 development folds | 0.90 |
| H015 − H016 on `LIRF_NM_missing`: bulk dRMSE < 0 on S1 | 0.95 |
| H015 and H016 identical outside the subgroup on all 8 folds | 0.95 |
| H016 − E017 on all rows: development mean < 0 (point estimate) | 0.50 |
| Criterion 8 statistic against E005 on S1 within +6,000 to +8,000 s | 0.55 |

Expected magnitude:
- **H016 − E017 on all rows:** −10 to +10 s development mean, sign undetermined. Per fold, the LIRF NM-missing subgroup can move it by tens of seconds.
- **On H015's clause population:** identical to H015 − E017.

Primary expected failure mode:
- The rule 11 all-rows figure is set by the LIRF NM-missing convention records, through the T counts' re-encoding of `d_sched`. It is then uninformative about congestion in either direction. That is a reading hazard, not a defect: the proposal reports it whatever its sign.
