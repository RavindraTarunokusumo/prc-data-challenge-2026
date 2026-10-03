# E041 analysis: H030 v1 (E033's construction on the seed-42 re-draw: blend of E029 and E040)

**Reading (N5): "robust to one further fixed-seed (GPU-only) draw".** `compare.py E041 E026`: `passes_criteria_1_to_3` **True**: mean −5.52 s (q95 −4.67), **WIN on all 7 folds**, no airport beyond +3 %. Tolerance: |`fold_delta_rmse`| of `compare.py E041 E033` ≤ 0.40 s on every development fold (limit 1.0 s). Criterion 6, E033's PROMOTE and ruling H5 are not reopened (N5).

## Run

| Item | Value |
|---|---|
| Config | `blend`, [E029, E040], [0.5, 0.5], seed 42, all 8 folds, CLASS-S |
| Status | COMPLETE: 8.7 s, 3.42 GB; run commit `b7f896e` |
| Development mean | **438.97 s** (E033 438.87; E034 438.95) |
| Integrity | `route_check.py E041 - E029`: PASS |
| Gating | status only: E040 COMPLETE and route-checked |

- **Started by a direct `run_experiment.py` call** on the owner's instruction "No, run now." (INC-0012 amendment, 2026-10-03; N2/C3 route). No run window applied; no INC-0012 deviation.
- **Freeze:** `git diff --stat 9d245c0 <run commit> -- src scripts pyproject.toml uv.lock config research/day-06/eda/d06_diagnostics.py research/day-06/sessions/D06-S01/run_window_2.sh` is **empty**.
- **Environment (rule L v2 item 6):** manifest `python` 3.13.15, `polars_threads` 16; clean tree; no swap pages. GPU: RTX 5060 Laptop, driver 591.91, CUDA 13.1; 688 MiB in use at the start of E040.
- **Role:** control (batch X-D06-S01-0003); no candidate; never NEW; no holdout; ledger decision null. **N4:** E040/E041 are one further draw of E031's / E033's configuration; they are not the Day 7 SUBMIT draw, and no WIN/TIE/LOSS between draws is read as an effect.

## The reading

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| E041 − E026 (s) | −6.44 W | −9.65 W | −4.17 W | −4.17 W | −3.19 W | −6.59 W | −6.75 W |
| E033 − E026 (s), for reference | −6.51 W | −9.61 W | −4.21 W | −4.17 W | −3.59 W | −6.39 W | −6.82 W |

## Rule 13 quantities and the three-draw record (N5, N7; labelled by pair type)

| All rows (s) | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| E041 − E033 (fixed-seed) | +0.08 | −0.05 | +0.04 | −0.00 | +0.40 | −0.20 | +0.07 |
| E034 − E033 (seed + GPU) | +0.48 | −0.25 | +0.09 | +0.27 | −0.20 | +0.14 | −1.28 |
| E041 − E034 (seed + GPU) | −0.40 | +0.20 | −0.05 | −0.27 | +0.60 | −0.34 | +1.35 |
| RMS prediction change E041 vs E033 | 12.7 | 12.9 | 10.6 | 0.0 | 16.7 | 15.5 | 3.1 |
| RMS prediction change E034 vs E033 | 21.2 | 17.5 | 15.2 | 19.8 | 19.0 | 23.3 | 36.6 |
| RMS change E041 vs E033, `NM_present_excl_LIRF` | 10.5 | 10.4 | 9.2 | 0.0 | 13.2 | 11.8 | 3.0 |

- `NM_present_excl_LIRF`: E041 − E033 mean +0.36 s (q95 +0.58); E034 − E033 +0.26 s; E041 − E034 +0.10 s.
- **Blend three-draw spread** (max − min over E033, E034, E041; development folds, all rows): R1 0.48, R2 0.25, R3 0.09, S1 0.27, **W1 0.60** s. All three draws meet criteria 1–3 against E026 with 7/7 WIN.
- **D5-C10 rows:** row 192622644 (S1): E033 9,008, E034 8,639, **E041 9,008** s (inside the 7,900–14,100 s band the review computed for S1's tolerance). Row 183910286 (W1): E033 15,086, E034 13,272, **E041 13,576** s.
- Rule 12 bands: < 1 h 79, 1–3 h 4, > 3 h 3 (E033: 82, 4, 3).
- **Scope (review finding 3):** this test had almost no power to show E033 wrong; it is a reproducibility measurement. The untested part of the Day 7 claim is the 12-month composite SUBMIT procedure.
- Predictions met: reading "draw-robust" (researcher P 0.85; Advisor 0.93); E041 − E026 −5.52 (expected −5.0 to −6.0; Advisor ≈ −5.6); |E041 − E033| ≤ 0.6 s on all five (realised ≤ 0.40). RMS change 11–17 s on four folds (expected 13–25), 0 on S1.

## Appended correction (D6-C11; rule 13 on the mechanism population)

*Appended at the Day 6 phase close (X-D06-S01-0004; `research/day-06/acks/PHASE_CLOSE_D06_ack_v1.md`). The text above is unchanged.*

Clause 1's gain over E029 on `NM_present_excl_LIRF`, by draw (s):

| Draw | R1 | R2 | R3 | S1 | **W1** | S1c | W1c | 5-fold mean |
|---|---|---|---|---|---|---|---|---|
| E033 | −3.90 | −4.47 | −4.03 | −5.81 | **−1.59** | −7.29 | −8.29 | −3.96 |
| E034 | −3.66 | −4.54 | −4.10 | −5.87 | **−0.31** | −7.70 | −8.45 | −3.70 |
| E041 | −3.84 | −4.65 | −4.09 | −5.81 | **+0.40** | −7.43 | −8.21 | −3.60 |
| Spread | 0.24 | 0.18 | 0.08 | 0.07 | **2.00** | 0.41 | 0.24 | 0.36 |

- On W1 (February 2025, the January analogue) the gain on normal taxis is present in one draw, near zero in one, reversed in one. On all rows W1 improves over E029 in all three draws (−2.31, −2.51, −1.91 s), and 69 % of E033's W1 gain sits outside normal taxis (8.2 % of W1 rows). W1 is WIN against E026 in all three draws. Updates D5-C9.
