---
schema: advisor-review-v1
hypothesis_id: H011
proposal_version: 1
proposal_sha256: 3a8b59483923c500b764dc326d0b014a7bc68b0d6689575a0d7e8530f66cbb70
exchange_id: X-D02-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.80
created_utc: 2026-09-28T18:43:40Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE.**

The question H011 asks (how much static signal exists without the anchor) is the brief's literal Day 2 question and worth answering. As specified, H011 does not answer it cleanly. Three defects, all fixable before execution:

1. **The six added columns are not all static.**
   - FS1_NO_DELTAS keeps `hour_utc` and `weekday` (takeoff, label T) and adds `sched_hour_local` and `sched_weekday_local` (label P).
   - Together they encode the delay at hour resolution: (`hour_utc` − `sched_hour_local`) mod 24, offset by the time zone, plus a day-crossing bit. That is a coarse `d_sched`.
   - E010 had the takeoff keys but no schedule time, so H011 − E010 adds this channel along with the static keys.
   - Evidence (shrunken cell means fitted on FIT months, evaluated out of time on August's 197 LIRF NM-missing rows):

     | Proxy bin: (`hour_utc` − `sched_hour_local`) mod 24 | 0 | 1 | 2–3 | 4–12 | 13–23 |
     |---|---|---|---|---|---|
     | Convention-tail rate (FIT) | 0.50 | 0.69 | 0.69 | 1.00 | 0.25 |
     | Mean y (s) | 4,057 | 6,482 | 11,820 | 30,703 | 5,636 |

     - Out-of-time RMSE: 9,289 s for a constant, 8,855 s with the proxy, and 8,758 s with exact `d_sched` in 1-hour bins.
     - Either key alone gives only 9,213 or 9,232 s, so the gain comes from the interaction.
   - The statements "Neither model contains `d_sched`, so the convention is out of reach of both" and "Standing rule 8: not engaged" are therefore wrong in effect. The batch's own H010 Alternative Explanation 2 names this mechanism.
2. **The static-signal claim is not insulated from the LIRF NM-missing subgroup.**
   - E010's LIRF NM-missing subgroup carries **0.15–0.58 of its SSE** per development fold.
   - A ±15 % change in that subgroup's SSE alone moves the fold RMSE by **±3.9 to ±29 s** (S1c ±30 s).
   - The expected H011 − E010 effect is −8 to −35 s.
   - The falsification criterion (criterion 1 and ≥ 3 WINs against E010, full population) can therefore pass through convention capture by the proxy and be recorded as static structure.
3. **"Nearly causal" is incorrect.** Two inputs are T, and their interaction with the P schedule keys reconstructs a T-labelled delay.

**The M2 role is flawed.** H011's role as H009's M2 comparator is defective for a separate reason: the contrast H009 − H011 removes `d_sched` as well as the anchor. See `H009_review_v1.md`.

**Verified here.**
- The batch checks in `H009_review_v1.md` cover H011: hashes, frozen files, tests 96/96, lint, code, secrets.
- `fs1_no_deltas` drops exactly `d_aobt3`, `d_eobt1`, `d_sched` and `flt_missing` (asserted in the tests).
- FS1_NO_DELTAS equals E010's FS0_NO_DELTAS plus the six FS1 columns, as stated.

## Scientific Validity

**Static keys as taxi-duration structure.**
- The mechanism is plausible, and the EDA supports it in the bulk. Against the airport median:
  - stand 43 s;
  - operator prefix 33 s;
  - destination 32 s;
  - aircraft type 29 s.
- E010 is the right reference in principle: identical except the six columns.

**The defect is that two of those six columns are P only on their own.** Next to the retained T takeoff keys they open the convention channel. Hour resolution is enough for this subgroup:
- the convention-tail rate depends on the delay in steps of hours (0.43 for 1–2 h against 0.70 above 2 h);
- the day-crossing bit flags multi-hour and day-scale records (FIT months: 18 rows, tail rate 0.83, mean y 36,315 s).

**Can LightGBM find the interaction?** Probably, partly:
- the LIRF NM-missing subgroup is identifiable through `WK_TBL_CAT_flt` = `UNK`;
- its residuals are extreme, so L2 boosting chases them;
- `min_data_in_leaf` = 100 still allows about 10 leaves on the roughly 1,000–1,300 subgroup rows of a full training fold.

**What the channel does not reach.** On NM-present LIRF rows the proxy does nothing (613 → 608 s out of time).

## Novelty Relative to Existing Research

This is new. E010 had none of the six FS1 keys (only airport, airport × runway, wake, market and flight type), and no completed experiment measures the FS1 keys without the anchor.

## Experimental Isolation

**H011 − E010 changes six columns carrying two mechanisms:**
- static structure: four categoricals plus the P time of day and weekday;
- a T × P schedule-delay proxy: the two schedule keys interacting with the existing takeoff keys.

The design cannot separate them.

**Missing control (named, not designed).** A contrast in which the delay proxy is absent from both sides, or present on both.

**H009 − H011 (M2) confounds the anchor with `d_sched`.** This is the confound X-D01-S01-0004 recorded for H008.

## Validation Quality

**Folds.**
- The frozen folds are used unchanged: seven scored folds plus H, with H predicted only.
- Twin signs are pre-registered.
- The W1c fallback is correctly stated (fold-local collapse, no history features).

**Reusing E010.** Permitted, under the ruling in `H009_review_v1.md`.
- E010's `gate.json` records `uv_lock_sha256` `39df945c…`, equal to the current `uv.lock`.
- The FS0_NO_DELTAS path is unchanged.
- Standing rule 3 is not engaged: H011 is not a candidate, and E010 is not a promotion comparator.
- Record that E010 ran with `git_dirty_at_allocation: true` and `git_dirty_at_run: true`.

**The pre-registered rule 8 expectation is at risk.** The proposal expects the LIRF NM-missing share of the H011 − E010 SSE change below 0.3 on every fold. That is unlikely given the channel (see Advisor Prediction). A pass of the falsification criterion would not reveal the failure, because that criterion is judged on the full population.

## Leakage Review

### Target Leakage

PASS

- There are no target statistics.
- The collapse and vocabularies are row counts from training rows only.
- Validation `y` is null.

### Temporal Leakage

CONCERN

Every input is admissible under §6.2. The concerns are about labels, not admissibility:
- The schedule-delay proxy takes label T by precedence, so the rule 8 disclosure ("not engaged") is wrong.
- `ades` is F for diverted flights whose `ADES_mvt` records the flown destination (641 of 2,070 diversions, about 0.03 % of DEP rows; see `H009_review_v1.md`).

### Competition Availability

PASS

- Every input is present for ranking DEP rows.
- Unseen levels (0.005–0.26 %) map to `__RARE__`.
- The EDA's "0 % unseen" is an artifact of a vocabulary built over the ranking rows themselves (`H009_review_v1.md`). The conclusion is unaffected.

## Compute Review

### RAM

PASS

E010 peaked at 3.63 GB. FS1_NO_DELTAS on fold H should need about 4–5 GB (CLASS-M: 8 GB).

### Runtime

PASS

- E010 took 444 s with 7 features. H011 has 13, four of them high-cardinality.
- Expect 10–15 minutes, above the proposal's 8–12 but well inside CLASS-M (timeout 45 minutes).

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

That without the four deltas nothing in the model identifies the flight's delay. Two of the six added columns reconstruct it at hour resolution when paired with the retained takeoff keys.

## Missing Control or Ablation

- **For the static claim:** a contrast with the delay proxy absent from both sides, or present on both.
- **For the falsification:** a population or statistic insulated from the LIRF NM-missing subgroup.
- **For the M2 role:** a contrast holding `d_sched` fixed (see `H009_review_v1.md`).

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- No FS1-family run may be allocated before an H009 version ≥ 2 is ACCEPTED and acknowledged.

Required acknowledgement path: none for v1. Submit `research/day-02/proposals/H011_v2.md` in a new exchange, together with or after `H009_v2.md`.

## Revision

**Required (minimal).**
1. **Address the schedule-delay proxy.** Either remove it from the design, or keep it and do all of the following (the researcher chooses):
   - (a) correct the rule 8 statement;
   - (b) pre-register separate tail and bulk expectations for LIRF NM-missing rows, plus an S1 expectation;
   - (c) narrow the "static structure" claim so that it excludes what the proxy can carry.
2. **Insulate the static-signal falsification** from the LIRF NM-missing subgroup, as for H009's M1. Commit the producing code before the run.
3. **M2 role.** If H011 remains a comparator in H009's M2 clause, align it with the M2 contrast re-specified in H009 v2 (`d_sched` held fixed).
4. **Record corrections.**
   - "Nearly causal".
   - The runtime estimate (13 features, not 7).
   - The shared evidence corrections: the ranking-unseen shares are not 0 %, and `created_utc` 18:24:00Z postdates the commit and the envelope.
   - E010's dirty-tree flags.

**Acceptable as is:** the E010 reference, the model, parameters, folds, seed and class, the rare collapse, and the twin expectations.

## Advisor Prediction

For the v1 configuration:

| Event | P |
|---|---|
| Passes criterion 1 and ≥ 3 WINs against E010 (the falsification as written) | 0.85 |
| \|LIRF NM-missing share of the H011 − E010 SSE change\| < 0.3 on every development fold (pre-registered) | 0.40 |
| H011 − E010 < 0 on S1c | 0.85 |

Expected magnitude:

| Quantity | Expected |
|---|---|
| Development mean | 460–490 s |
| H011 − E010 mean dRMSE | −12 to −40 s |
| NM-present bulk dRMSE | −15 to −35 s per fold |

Primary expected failure mode: the falsification passes, but part of the margin runs through LIRF NM-missing tail rows via the schedule-delay proxy, largest on S1 and S1c. It is then recorded as static structure, and the Day 2 answer to "how much signal exists without inferred operational state" is overstated.
