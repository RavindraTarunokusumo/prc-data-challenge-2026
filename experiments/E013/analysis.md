# E013 — H010 v1 (LightGBM on FS1_NO_DSCHED), M3 ablation · COMPLETE

**Run.** 843.1 s, peak 4.176 GB, CLASS-M, `within_class: true`. All preconditions 1(a)–(e) of `H010_review_v1.md` held at allocation:
- the H009 v3 ACCEPT and its ack were committed;
- FS1 was unchanged;
- the M3 clause was identical;
- E012 was COMPLETE;
- nothing else was running.

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| E013 | 391.52 | 274.60 | 349.92 | 608.22 | 450.87 | 635.42 | 493.16 | **415.03** |

The development mean is inside the predicted 395–440 s.

## Clause 3 of H009 v3 (`research/comparisons/E012_vs_E013_mech_LIRF_NM_missing.json`): not met, M3 supported

H009 − H010 full dRMSE on the LIRF NM-missing subgroup:

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| dRMSE (s) | −1,088.6 | −314.2 | −2,492.9 | −1,976.3 | −2,475.2 | −2,561.5 | −2,958.2 |

- All < 0, so clause 3 (≥ 0 on ≥ 3 of 5 development folds) is **not met**.
- On that subgroup, the frozen criteria give mean −1,669 s (q95 −1,032).
- **Reading (as pre-registered).** Exact `d_sched` adds substantially beyond the hour-resolution schedule-delay proxy that FS1_NO_DSCHED keeps. The measured effect is a lower bound on the convention mechanism.
- **Criterion 8 rule for H009** (`H009_ack_v3.md`):
  - part 1 (clause 3 not met) holds;
  - part 2 (`NM_missing_LIRF.delta_rmse_bulk` against E005 ≤ +6,500 s) held in E012's analysis;
  - the LIRF bulk-trade objection is therefore **resolved**.

## Pre-registered H010 expectations against the outcome

Stated as H010 − H009 (`E012_vs_E013.json` gives H009 − H010; the signs are flipped here).

| Expectation | Outcome | Verdict |
|---|---|---|
| Development mean 395–440 s | 415.03 | met |
| LIRF NM-missing full > 0 on ≥ 3 of 5 | > 0 on 5 of 5 | met |
| LIRF NM-missing **bulk < 0 on every fold** (bulk loss recovered) | −613.6 (R1) and −1,199.9 (S1) < 0; **+677.1 (R2), +2,532.0 (R3), +4,302.3 (W1) > 0** | **missed on 3 of 5** |
| NM-present bulk within [−3, +8] s | +1.2 to +7.6 on the development folds | met |
| Tail share > 0.8 | 1.025 | met |
| S1: smallest net loss of the five folds, possibly a gain | S1 full H009 − H010 = −70.1 s, the largest net H010 loss of the five folds | **missed** |

- **The bulk miss.** Without `d_sched`, the model does not simply fall back to a normal-taxi prior on these rows. On R2, R3 and W1 its bulk predictions are further from the truth.
  - A plausible reading is that the hour-resolution proxy is used cruder, with coarse delay bins that over-shoot. That is untested.
  - The recovery of bulk accuracy happens only in July (S1), the month with the lowest convention-tail rate. The mechanism prediction was right only there.

## Rules 1, 6 and 7 (`compare.py`, `E012_vs_E013.json`): reported

- All rows: 7/7 WIN for H009, and criteria 1–3 pass. H010 is not a candidate, so this is attribution only.
- **Tail share** 1.025.
- **Rule 6:** dominant rows on R2 (198939290, y = 18,245, `d_sched` 18,242), W1 and W1c (183903219, y = 131,167). All are LIRF NM-missing convention records.
- **Rule 7:** NM-present bulk is −1.2 to −7.6 s (H009 better), so exact `d_sched` carries a little genuine delay information on NM-present rows too.
