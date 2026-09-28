---
schema: advisor-review-v1
hypothesis_id: H011
proposal_version: 2
proposal_sha256: a39d91bad0b4ddb3b88fe101fe70904f4800bf1f06e177724830b8c04adc42b0
exchange_id: X-D02-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-09-28T19:14:10Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT, with sequencing and lapse conditions.**

v2 fixes the three v1 defects, and the diagnostic is now clean enough to answer the brief's Day 2 question.

| v1 item | Status in v2 |
|---|---|
| 1. Schedule-delay proxy | **Removed.** `fs1_static_no_deltas` drops the scheduled local hour and weekday. A test on real silver (R1) asserts that the added columns are exactly `stand`, `actype`, `op_prefix` and `ades`, and that the FS0_NO_DELTAS columns are byte-identical. There are 11 features |
| 2. Falsification insulated from LIRF NM-missing | Done. `excl_LIRF_NM_missing`, from committed code (`prc.attribution.population_mask`, tested; `scripts/mechanism_check.py`) |
| 3. M2 role | Dropped. H012 is the comparator |
| 4. Record corrections | Done: "nearly causal" withdrawn, the takeoff keys labelled T, the runtime for 11 features, the unseen shares, `created_utc`, and E010's dirty-tree flags |

**Residual route to the schedule delay: coarse.**
- Operator prefix and destination together can hint at a flight's scheduled hour, which the takeoff hour (T) could then compare against.
- A target-free check (January–November DEP rows, groups ≥ 100 rows) shows the airport × `op_prefix` × `ades` triple pins the modal scheduled local hour for only:
  - **37 %** of rows overall;
  - **41 %** of LIRF NM-missing rows.
- The removed proxy gave hour resolution on every row. The residual route is not material.

**Residual exposure of the falsification population.** Per fold, with E010 as the reference:

| Subgroup inside `excl_LIRF_NM_missing` | Share of E010's SSE in that population | ±15 % of that subgroup's SSE moves the fold by |
|---|---|---|
| LIRF NM-present tail | 2.0–10.2 % (R1–R3, W1, W1c); **30.4 % on S1** (29.7 % S1c), of which row 192622644 alone is 20.1 % | ±0.6 to ±2.5 s; S1 ±10 s |
| NM-missing rows at the other nine airports | 2.9–4.7 % (R1–R3, S1); **15.6 % on W1** (14.4 % W1c) | ±0.7 to ±1.9 s; W1 ±5 s |

- **Row 192622644 (S1, S1c)** is not a decider here, unlike in H009's M1.
  - Neither model has the anchor or `d_sched`. E010 predicts 1,009 s on it, and H011 has no input that marks it as a day-scale record.
  - A 1,000 s change on that row moves S1 by about 1 s.
  - H011's criterion does not require an S1 WIN.
- **The criterion** (frozen criterion 1 over five folds, plus ≥ 3 WINs among five) cannot be decided by these exposures at the expected −8 to −30 s. The exception is near the bottom of that range, where the rule 1, 6 and 7 disclosures will show it.

**Verified here** (read-only). The batch checks in `H009_review_v2.md` cover H011: hashes, frozen files, tests 98/98, lint, secrets. In addition:
- `fs1_static_no_deltas` = `fs1` minus `DELTAS` and the two scheduled-time keys, and `fs1` is unchanged since `cba278d`.
- **The E010 reuse conditions hold:**
  - `uv.lock` is `39df945c…`;
  - `gbm.py` and the FS0 path are unchanged;
  - silver is verified.

  E010 ran with `git_dirty_at_allocation` and `git_dirty_at_run` both true (recorded in v2).

**Why sequencing matters.** H011's outcome on NM-present rows measures the static keys on the validation folds, while H009's M1 clause is being revised (`H009_review_v2.md`). H011 therefore runs only after an H009 version ≥ 3 is ACCEPTED and acknowledged. That is also where H011's own Validation Plan puts it: last in the chain.

## Scientific Validity

**The mechanism.** Static keys as taxi-duration structure (stand to runway distance, type and operator procedures, destination) is plausible. The EDA supports it in the bulk against the airport median:
- stand 43 s;
- operator prefix 33 s;
- destination 32 s;
- aircraft type 29 s.

**What H011 answers.** It measures "static keys on top of the airport × runway × takeoff-time structure", without the anchor, without `d_sched` and without scheduled time. It keeps the takeoff hour and weekday (T), as E010 does. That is the cleanest form of the Day 2 question available with an existing reference.

**Where the gain will partly come from: NM-missing rows at the other nine airports.**
- Static keys replace `UNK` there: on NM-missing rows, stand, flight number and destination are ≥ 99.7 % present, and aircraft type 93.2 %.
- These rows are inside the falsification population. They carry 15.6 % of E010's population SSE on W1.
- The gain there is P-labelled static structure, but concentrated. The Day 2 answer should report the NM-present figure (`mechanism_check.py <H011> E010 NM_present`, planned) next to the falsification figure.

**Rule 8 disclosures.**
- E010 already predicts the subgroup level on LIRF NM-missing rows: median 5,364–6,125 s per fold, bulk RMSE 5,224–6,257 s on 14–218 bulk rows.
- The pre-registered bulk band (±300 s per fold) is narrow at that scale. Static keys that separate convention-prone from normal flights can exceed it.
- A miss is recorded under rule 8. It does not touch the falsification.

## Novelty Relative to Existing Research

This is new. E010 had none of the four keys, and no completed experiment measures them without the anchor.

## Experimental Isolation

**Good: four columns.** H011 − E010 changes exactly `stand`, `actype`, `op_prefix` and `ades` (tested), with the same model code, parameters, seed and folds.

**Remaining confounds:**
- The rare collapse and LightGBM's per-tree feature sampling change with the column count. That is inherent to adding features.
- The route-identity path to the delay is coarse (above).

## Validation Quality

**Folds.**
- The frozen folds are used unchanged: seven scored folds plus H, with H predicted only.
- Twin signs are pre-registered: S1c < 0, W1c ≤ 0.

**The falsification statistic is named:**
- `criterion_1`;
- `fold_outcome` (raw, not twin-adjusted), with fewer than 3 WINs among five meaning falsified.

It is weaker than criterion 2 (no S1 requirement, no no-LOSS rule). That is acceptable for a diagnostic that is never a candidate.

**Reuse of E010.** Permitted (X-D02-S01-0001), and the conditions hold today.

## Leakage Review

### Target Leakage

PASS

- There are no target statistics.
- The collapse and vocabularies are counts from training rows only.
- Validation `y` is null.

### Temporal Leakage

CONCERN

These are label notes, all stated in v2. Not blocking:
- `ades` is F on diverted flights (~0.03 % of rows);
- the takeoff hour and weekday are T, so the model is not a causal-only variant.

### Competition Availability

PASS

Every input is present for ranking DEP rows. Unseen levels (0.005–0.27 %) map to `__RARE__`.

## Compute Review

### RAM

PASS

- E010 peaked at 3.63 GB, and the FS1 build plus the silver load at 4.27 GB.
- Expect 4.5–5.5 GB on fold H, inside CLASS-M (8 GB).

### Runtime

PASS

- E010 took 444 s with 7 features. H011 has 11, four of them high-cardinality.
- Expect 8–13 minutes. The timeout is 45 minutes.

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

**The assumption.** The static-key gain in `excl_LIRF_NM_missing` is taxi-duration structure of scheduled flights.

**Why it may not be:**
- Part of it will come from NM-missing rows at the other nine airports, where `UNK` is replaced (W1: 15.6 % of the reference SSE).
- On S1, part may come from static priors on LIRF NM-present block-at-schedule rows.

Both are visible in the rule 7 table.

## Missing Control or Ablation

None is required for its stated purpose. The planned `NM_present` report is the interpretive control, and it must be reported next to the falsification figure.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions (all must hold before allocation).**
   - (a) An H009 version ≥ 3 has decision ACCEPT, and its acknowledgement is committed.
   - (b) The primary runs that the accepted H009 version's chain places before H011 are COMPLETE. In the v2 chain these are H009, H010 and H012.
   - (c) No other experiment runs concurrently.
   - (d) The E010 reuse conditions hold at allocation:
     - `uv.lock` is `39df945c…`;
     - `gbm.py` and the FS0 path are unchanged;
     - silver is pinned.

     Record H011's `gate.json` `uv_lock_sha256` in the analysis.
2. **Lapse.** If the output of `fs1_static_no_deltas` changes (through `fs1`, `fs0` or `collapse_rare`), or (d) fails, this ACCEPT lapses and `H011_v3` is required.
3. **One primary run.**
   - `uv run python scripts/gate.py allocate H011 v2`.
   - Config: `model: lightgbm`, `feature_set: FS1_STATIC_NO_DELTAS`.
   - `params`: `objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 0.9`, `bagging_fraction: 0.8`, `bagging_freq: 1`, `num_threads: 4`, `num_boost_round: 1000`.
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
   - Then `uv run python scripts/run_experiment.py E###`.
4. **Comparisons** (completed experiments only; no new run):
   - `scripts/mechanism_check.py <H011> E010 excl_LIRF_NM_missing` is the falsification test (`criterion_1`, `fold_outcome`);
   - `scripts/mechanism_check.py <H011> E010 NM_present` is reported next to it;
   - `scripts/compare.py <H011> E010` gives the rule 1, 6 and 7 disclosures.
5. **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun`, logged.
6. **Not authorized:**
   - a reproduction run;
   - any change to features, parameters, folds or seed;
   - use as a promotion candidate or champion;
   - scoring H.

Required acknowledgement path: `research/day-02/acks/H011_ack_v2.md`.
- It must reference the proposal hash and this review's hash.
- It must adopt preconditions 1(a)–(d) and the lapse rule.
- It must record the residual exposures above. They are not a change of claim.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Falsification not met (criterion 1 and ≥ 3 WINs on `excl_LIRF_NM_missing`) | 0.88 |
| H011 − E010 < 0 on S1c (`excl_LIRF_NM_missing`) | 0.85 |
| W1c comes out WIN | 0.50 |
| \|LIRF NM-missing tail share\| ≤ 0.3 on every development fold (rule 8, pre-registered) | 0.55 |
| LIRF NM-missing bulk dRMSE within ±300 s on every development fold (rule 8, pre-registered) | 0.35 |

Expected magnitude:

| Quantity | Expected |
|---|---|
| Development mean | 470–495 s |
| H011 − E010 on `excl_LIRF_NM_missing` | −10 to −28 s (mean) |
| NM-present bulk dRMSE | −12 to −30 s per fold |

Primary expected failure mode:
- The falsification passes, but the margin is disproportionately carried by NM-missing rows at the other nine airports, where `UNK` is replaced. That is largest on W1 and W1c.
- Read alone, the Day 2 answer would then overstate the static signal on scheduled, NM-present flights.
- Secondary: W1c comes out TIE, because January-only training collapses more levels to `__RARE__`.
