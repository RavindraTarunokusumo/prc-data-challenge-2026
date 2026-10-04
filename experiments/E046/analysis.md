# E046 analysis: H035 v1 (candidate): E033 with the LIRF NM-missing subgroup predicted by the unrouted FS2 LightGBM (E045)

**Development reading: criteria 1–4, 6 and the criterion 8 rule all met; objection F (U7) is open.** H035 is **not promotable** until the Day 7 phase-close access `holdout_check.py E046 E033` gives a WIN (U7). Under U6, the development margin below is **not** the submission's expected gain: criteria 1–4 recompute Day 3's recorded contrast on laptop instances, and criterion 6 checks determinism; none of them tests the forward bet.

## Run

| Item | Value |
|---|---|
| Config | `override`, base E033, override E045, subgroup `LIRF_NM_missing`, all 8 folds, seed 42, CLASS-S |
| Status | COMPLETE: 30.8 s, 3.35 GB; started 00:21:55Z, finished 00:22:26Z (INC-0015 window); run commit `e6477be` |
| Integrity | `route_check.py E046 E033 E045`: PASS on all 8 folds (subgroup rows 168/115/52/337/58/337/58/88 equal E045; every other row equals E033 exactly) |
| Tree, unmasking | `git_dirty_at_run: false`; no unmasking event (U4) |
| Freeze | `git diff --stat 76e80f1 3eccc98 -- src scripts config pyproject.toml uv.lock research/day-07/sessions/D07-S01/run_window_2.sh`: empty |
| W&B | sync failed (CommError); not mirrored (INC-0009) |

## Development results (against E033; `research/comparisons/E046_vs_E033.json`)

| | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| E046 | 274.34 | 238.33 | 294.43 | 414.44 | 350.59 | 431.56 | 434.35 | **314.42** |
| E033 | 439.89 | 264.88 | 393.04 | 627.92 | 468.63 | 631.99 | 481.77 | 438.87 |
| ΔRMSE | −165.55 W | −26.55 W | −98.61 W | −213.49 W | −118.04 W | −200.43 W | −47.42 W | **−124.45 (q95 −82.85)** |
| Pre-registered | −165.6 | −26.6 | −98.6 | −213.5 | −118.0 | −200.4 | −47.4 | −124.5 |

- **Criteria 1–3: pass.** 7/7 WIN; the only airport that changes is LIRF (pooled 838.4 against 1,445.5 s); no airport degrades.
- **Rule 14 (point contrasts against each E033 draw):** E034 −124.53 (q95 −82.94), E041 −124.54 (q95 −83.04); both 7/7 WIN. Against E028 (E005's laptop instance): −168.30.
- **Criterion 6: PASS** (`reproduce_check.py E048 E046 --champion E033`; E047 byte-identical to E045).
- **E045 reproduces E020** to 0.000000 s per fold, so the pre-registered derivation held to 0.05 s per fold.

## Criterion 4 (mechanism)

Reading (a) per development fold, from `compare.py`'s rule 7 disclosure for `NM_missing_LIRF`. The total SSE change is negative on every fold, and the tail rows (y ≥ 3,600 s) carry more than the whole gain:

| | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| `share_of_sse_change_tail` | 1.055 | 1.125 | 1.014 | 1.127 | 1.003 | 1.112 | 1.007 |
| subgroup rows (tail) | 168 (74) | 115 (57) | 52 (36) | 337 (119) | 58 (44) | 337 (119) | 58 (44) |

Reading (b): the route check shows every non-subgroup row unchanged (0.0 s). **Criterion 4 holds.**

## Criterion 8 (H009 v3's rule, unchanged)

`NM_missing_LIRF.delta_rmse_bulk` on every development fold:

| | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| against E033 | +2,823.6 | +1,634.1 | +2,333.1 | **+4,292.4** | +1,066.7 | +3,874.6 | +1,163.1 |
| against E028 | +2,823.7 | +1,634.0 | +2,319.4 | +4,292.0 | +1,066.4 | +3,874.6 | +1,163.0 |

Both are ≤ +6,500 s on every development fold. **The rule holds.** (The predicted S1 value was about +4,300 s, against E020's +4,292.)

## Objection F (U7)

**Open.** It is resolved only by a WIN of `holdout_check.py E046 E033` at the Day 7 phase close. A TIE leaves H035 INCONCLUSIVE ("phase-close holdout TIE; forward bet not confirmed"). A LOSS applies the frozen revert. In either case E033 stays champion and E044's file stands.

## U8 disclosures

**(a) Forward support** for the subgroup (target-free; `E046_exposure_U8.json`, `range_check_forward_D07.json`):
- In every month, 81–94 % of subgroup rows are more than 1 h behind schedule.
- Median schedule delay: 2025 months 6,001–6,898 s; **2026-01 7,141 s**; 2026-07 6,897 s.
- q90: 2025 maximum 13,865 s (December 11,642); **2026-01 17,816 s**; 2026-07 14,945 s. Both ranking months lie above every 2025 month at q90.
- LIRF NM-missing rows with `d_sched` > 3 h: 2026-01 21 and 2026-07 53, against a 2025 range of 6–75.

**(b) Exposure** on the subgroup. X_t and X_b are the squared prediction changes on tail and bulk rows; S_t and S_b are the realized SSE changes. λ* is the recording-change break-even; "absent loss" is X_t + S_b.

| | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| λ* = (X_t + S_b)/(X_t − S_t) | 0.47 | 0.57 | 0.27 | 0.54 | 0.27 | 0.50 | 0.20 |
| convention-absent loss / realized gain | 0.90 | 1.30 | 0.37 | 1.19 | 0.37 | 0.99 | 0.25 |
| top-1 / top-10 share of X_t + X_b | 0.17 / 0.84 | 0.19 / 0.70 | 0.34 / 0.88 | 0.08 / 0.63 | 0.57 / 0.89 | 0.08 / 0.61 | 0.14 / 0.85 |

**In plain words (U6):** the candidate keeps an advantage on a fold only if the 2026 convention rate stays above about **20–57 %** of its 2025 level. If the convention disappeared, the loss would be **0.25–1.3 times the 2025 gain**: of the same order, and larger than the gain on R2 and S1. Per ranking month, the target-free exposure Σ(E050 − E044)² is reported when E050 exists (deferred, below).

**(c) Rule 6.** Row 183903219 (W1; y 131,167 s; `d_sched` 131,163 s) carries 0.79 of W1's SSE change and 0.57 of W1c's. Without it, W1 is **−32.92 s** (E046 288.29 against E033 321.21) and W1c −28.66 s. The audit is disclosure only (as D5-C10). The top-10 share of the SSE change is 0.72–0.97 on every fold: the gain lives on a few dozen rows per fold.

**(d) Rule 12** (`range_check_E046.json`). Subgroup bulk rows predicted above 3,600 s / below 0 s: R1 27 / 8 of 94; R2 10 / 4 of 58; R3 7 / 0 of 16; S1 104 / 15 of 218; W1 2 / 3 of 14; S1c 110 / 20 of 218; W1c 3 / 0 of 14 (E033: 0 / 0 on every fold). These are the mechanism's bulk cost, the same rows that make up criterion 8's statistic.

## Missed or corrected

- The forward-risk wording of H035 §Batch, and of the researcher's message to the owner, is corrected by U6 (recorded in `research/day-07/acks/H035_ack_v1.md`).
- E045's runtime was above its forecast and its window guard (above). Together with E047's, it **deferred E049 and E050**: at 00:50:28Z, 572 s remained in the window against E049's 600 s guard. Both remain ALLOCATED with their ids (U10). They need a later owner-set window, recorded in a new incident, and are needed only if H035 is promoted.

## Appended correction (D7-C7, X-D07-S01-0003)

U8 (a) above is corrected. The 2025 maximum subgroup q90 is July 2025's 14,939 s, not 13,865 s. July 2026 (14,945 s) is at the 2025 maximum: above it by 6 s at the nearest rank, below it by linear or lower interpolation. **Only January 2026 lies above every 2025 month** (17,816 s at the nearest rank; 19,592 s linear). The share of subgroup rows more than 1 h late is 81–96 %, not 81–94 %.

## Appended outcome (Day 7 phase close)

Objection F resolved for December only: `holdout_check.py E046 E033` **WIN**, ΔRMSE −124.24 s (q10/q90 −190.37/−42.98); December 2025, E046 against E033, one access (E046 244.94, E033 369.18; P2 instance check exact). **H035 PROMOTED** (ledger E046 and E048 PROMOTE). Per U6 and P8, neither this figure nor the development margin is the submission's expected gain.
