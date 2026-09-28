# E016 — H011 v2 (LightGBM on FS1_STATIC_NO_DELTAS) · COMPLETE — the Day 2 question

**Run.** 882.4 s, peak 4.054 GB, CLASS-M, `within_class: true`. Preconditions 1(a)–(d) of `H011_review_v2.md` held:
- H009 v3 ACCEPT;
- E012, E013 and E014 COMPLETE;
- no concurrency;
- `uv.lock` `39df945cddc4` (`gate.json`), `gbm.py` unchanged since `866b902`, the `fs0` body unchanged, silver pinned.

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| E016 | 433.93 | 321.03 | 426.72 | 659.42 | 530.56 | 660.68 | 581.23 | **474.33** |
| E010 | 455.0 | 356.6 | 468.0 | 667.6 | 564.6 | — | — | 502.34 |

The development mean is inside the predicted 470–495 s.

## Falsification test (`E016_vs_E010_mech_excl_LIRF_NM_missing.json`): not falsified

- Mean dRMSE **−30.03 s** (q95 −28.46), criterion 1 True.
- **Development folds:** R1 −32.3, R2 −32.5, R3 −28.8, S1 −29.2, W1 −27.3, all WIN (5 counted WINs).
- **Twins:** S1c −26.7 (WIN) and W1c −1.8 (TIE). The expected sign held: S1c < 0, W1c ≤ 0, TIE possible.
- **Magnitude:** predicted −8 to −30 s. The observed −30.03 is at the edge of the range, marginally beyond it.
- **Bulk:** −27 to −31 s on every development fold. No row concentration (|top-1| ≤ 0.02, except W1c at −1.23 on a near-zero total).
- **On `NM_present` alone** (reported): mean −29.57 s, the same picture.

## The Day 2 answer

On its own, without NM or schedule deltas and without any route to the schedule delay, the four static keys (stand, aircraft type, operator prefix, destination) reduce RMSE by **about 30 s** on 99.8 % of rows.
- On top of the full anchor set, the six FS1 keys are worth **about 7 s** (H009 clause 2(a)).
- The anchor therefore absorbs roughly three-quarters of the static signal. Most of what stand, type and operator "know" about a flight's taxi time is already reflected in NM's off-block estimate relative to takeoff.

## Missed pre-registration: standing rule 8 on LIRF NM-missing rows (`compare.py`, `E016_vs_E010.json`)

Pre-registered: `share_of_sse_change_tail` within ±0.3 per fold, `delta_rmse_bulk` within ±300 s per fold.

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| Tail share | −0.03 | −0.07 | **0.51** | −0.05 | **0.50** | 0.14 | **−0.51** |
| Bulk dRMSE (s) | +85 | **−1,683** | **+704** | **+946** | **+3,082** | **−460** | **−3,687** |

- **Missed** on three development folds for tail share or bulk, and on both twins.
- **Reading.** Without `d_sched` or the scheduled-hour proxy, the static keys still reach the LIRF convention, most likely through the residual operator × destination × takeoff-hour route. The review flagged that route; it pins the scheduled hour for ~37 % of rows.
- The claim is unaffected, because the falsification population excludes these rows. The prediction that "the convention is out of reach" of this model was wrong in magnitude.

**All rows** (attribution): mean −28.01 s (q95 −19.01).
- Folds: R1, R2, R3 and W1 WIN; **S1 TIE** (−8.1); twins S1c WIN and W1c TIE.
- The S1 TIE comes from the LIRF NM-missing subgroup (+946 s bulk on S1). The static signal outside it is −29 s.
