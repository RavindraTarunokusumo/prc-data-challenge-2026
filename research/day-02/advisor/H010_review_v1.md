---
schema: advisor-review-v1
hypothesis_id: H010
proposal_version: 1
proposal_sha256: 3e273bd053d99337e6877ed2b2a2212461feb620bb525c26697372a9790a3a4a
exchange_id: X-D02-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.75
created_utc: 2026-09-28T18:42:37Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT, with sequencing and lapse conditions.**

**H010 is a clean one-column ablation.**
- FS1 minus `d_sched`, with the same model, parameters, seed, folds and rare collapse as H009.
- It is the ablation X-D01-S01-0004 named as missing: nothing on Day 1 separated the anchor correction from the `d_sched` / LIRF convention behaviour.
- Its test is well defined and pre-registered: the sign of H010 − H009 full dRMSE on the LIRF NM-missing subgroup, on at least 3 of the 5 development folds.
- It makes no promotion claim.

**Why conditions.** H010 has meaning only inside H009's chain, and H009 v1 is REVISE (`H009_review_v1.md`).
- H010 differs from H009 only by `d_sched`. The proposal itself expects NM-present bulk differences within [−3, +8] s.
- Running H010 before an H009 version is accepted would therefore reveal H009's M1 outcome while the M1 clause is being rewritten.
- H010 must wait for the accepted H009 version. It lapses if that version changes anything H010 depends on.

**One correction to the record.** The Mechanism says that without `d_sched` "the model cannot scale its prediction with the time between schedule and takeoff". For FS1_NO_DSCHED that is not correct.
- `hour_utc` and `weekday` (takeoff, T) against `sched_hour_local` and `sched_weekday_local` (P) give the delay at hour resolution (mod 24 h) plus a day-crossing bit.
- On LIRF NM-missing rows (FIT months → August), this proxy cuts the out-of-time RMSE of shrunken cell means from 9,289 to 8,855 s; exact `d_sched` in 1-hour bins reaches 8,758 s (details in `H009_review_v1.md`).
- The proposal's own Alternative Explanation 2 anticipates this and calls the measured M3 effect a lower bound. That reading is correct and is the one that stands: **H010 − H009 measures what exact `d_sched` adds beyond an hour-resolution proxy.**

**Verified here.** The batch checks in `H009_review_v1.md` (hashes, frozen files, tests 96/96, lint, code, rule 7 instrument, secrets) cover H010.
- `fs1_no_dsched` drops exactly `{d_sched}` (asserted in `tests/test_features_fs1.py` on real silver, R1 and W1c).
- `columns()` keeps the remaining columns in FS1 order, so the ablation changes one input and nothing else.

## Scientific Validity

**The mechanism test is valid for what it isolates.** On LIRF NM-missing rows `d_aobt3` and `d_eobt1` are null. Removing `d_sched` there leaves `flt_missing`, the static keys and the hour-resolution proxy.

**Expected Result.**
- The directions are right:
  - LIRF NM-missing full dRMSE > 0;
  - LIRF NM-missing bulk < 0;
  - NM-present bulk close to 0.
- The development mean of 395–440 s is probably too high, because the proxy keeps part of the convention signal.
- The "bulk loss recovered" expectation (−1,500 to −6,000 s) assumes the model reverts to a static prior on these rows. The proxy moves predictions on the same rows, so part of the bulk loss can persist.

**The alternative explanation on NM-present rows is well posed.** A bulk loss beyond +8 s would show that `d_sched` carries genuine delay information there. At LIRF, 79 % of NM-present tail rows are block-at-schedule records, so expect the NM-present effect to concentrate in the LIRF tail, not in the bulk.

## Novelty Relative to Existing Research

This is new. H008 (E010) removed all four deltas together. No completed experiment removes `d_sched` alone.

## Experimental Isolation

**Good: one column.** The contrast is H009 against H010, with the same code path, seed, folds and rare collapse.

**Residual confound (acknowledged in the proposal).** The convention stays partly reachable through the takeoff-hour × scheduled-hour interaction. H010 therefore gives a lower bound on M3's contribution, not its size.

**Named, not required.** An ablation that removes the channel entirely would need the proxy removed as well.

## Validation Quality

**Folds.**
- The frozen folds are used unchanged: seven scored folds plus H, with H predicted only.
- Twin signs are pre-registered: H010 − H009 > 0 on S1c and W1c.

**Rows that decide the clause.** On the development folds, the LIRF NM-missing subgroup has:

| Fold | R1 | R2 | R3 | S1 | W1 |
|---|---|---|---|---|---|
| Bulk rows | 94 | 58 | 16 | 218 | 14 |
| Tail rows | 74 | 57 | 36 | 119 | 44 |

- On R3 and W1 a few long rows decide the fold's sign.
- Row concentration (rule 6) is reported at fold level. Because H010 − H009 concentrates on this subgroup, the fold-level figures effectively describe it.

**Reuse.** None: H010 is compared only with the Day 2 H009 run.

## Leakage Review

### Target Leakage

PASS

- It uses the same inputs as H009 minus one column.
- There are no target statistics. The collapse and vocabularies are counts from training rows only.

### Temporal Leakage

CONCERN

- Every input is admissible under §6.2.
- The label notes of `H009_review_v1.md` apply:
  - `ades` is F for diverted flights whose `ADES_mvt` records the flown destination (641 of 2,070 diversions, about 0.03 % of rows);
  - the takeoff × scheduled time-key proxy is label T by precedence.
- Not blocking.

### Competition Availability

PASS

Every input is present for ranking DEP rows. Unseen levels (0.005–0.26 %) map to `__RARE__`.

## Compute Review

### RAM

PASS

About 4–5 GB on fold H, as for H009 (CLASS-M: 8 GB).

### Runtime

PASS

11–18 minutes (16 features). The timeout is 45 minutes.

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

That removing `d_sched` removes the convention channel. It removes one of two channels, so the effect measured is the marginal value of exact `d_sched` given the hour-resolution proxy.

## Missing Control or Ablation

None is required for its stated purpose. A complete removal of the convention channel (`d_sched` plus the proxy) is named above for the record.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions (all must hold before allocation).**
   - (a) An H009 version ≥ 2 has decision ACCEPT, and its acknowledgement is committed.
   - (b) That version keeps FS1 exactly (`src/prc/features.py` as at `cba278d`, or byte-identical output), with the same model, parameters, folds and seed as H009 v1.
   - (c) That version keeps its M3 clause, with the same subgroup (LIRF NM-missing), statistic (full dRMSE) and 3-of-5 rule.
   - (d) The H009 primary run is COMPLETE.
   - (e) No other experiment runs concurrently.
2. **Lapse.** If (b) or (c) does not hold, this ACCEPT lapses and `H010_v2` is required.
3. **One primary run.**
   - `uv run python scripts/gate.py allocate H010 v1`.
   - Config: `model: lightgbm`, `feature_set: FS1_NO_DSCHED`.
   - `params`: `objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 0.9`, `bagging_fraction: 0.8`, `bagging_freq: 1`, `num_threads: 4`, `num_boost_round: 1000`.
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
   - Then `uv run python scripts/run_experiment.py E###`.
4. **Comparisons.**
   - `scripts/compare.py <H009 primary> <H010>`, with the rule 1, 6 and 7 disclosures.
   - Any contrast that the accepted H009 version pre-registers using H010. These compare completed experiments and need no new run.
5. **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun`, logged.
6. **Not authorized:**
   - a reproduction run (H010 is not a candidate);
   - any change to features, parameters, folds or seed;
   - use as a promotion candidate or champion;
   - scoring H.

Required acknowledgement path: `research/day-02/acks/H010_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It must adopt preconditions 1(a)–(e) and the lapse rule.
- It must record the Mechanism correction above.
- It must record the evidence corrections shared with H009 that apply here:
  - the ranking-unseen shares are not 0 %;
  - `created_utc` is not a measured time.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| H010 − H009 full dRMSE on LIRF NM-missing rows > 0 on ≥ 3 of 5 development folds (M3 supported) | 0.80 |
| H010 − H009 NM-present bulk dRMSE within [−3, +8] s on every development fold | 0.75 |
| H010 − H009 > 0 on both S1c and W1c (full population) | 0.70 |

Expected magnitude: development mean 375–415 s, i.e. H009 + 10 to +40 s. That is below the pre-registered 395–440 s, because the proxy keeps part of the convention.

Primary expected failure mode: on R3 and W1, which have about 50–60 LIRF NM-missing rows each, the proxy and the static keys recover enough of the convention that the subgroup sign is decided by one to three long records. The 3-of-5 rule then rests on R1, R2 and S1.
