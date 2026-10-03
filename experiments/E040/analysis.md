# E040 analysis: H029 v1 (seed-42 GPU refit of E031's exact configuration)

**Byte-identity: no** (all 8 prediction files differ from E031's). **Resolved parameters (N6): identical to E031's on every fold** (58 keys, none in one arm only, none differing; `research/day-06/eda/closed_set_E040_vs_E031.json`). So E040 is a pure fixed-seed re-draw.

## Run

| Item | Value |
|---|---|
| Config | `experiments/E031/config.yaml` unchanged (header aside); seed 42; all 8 folds; CLASS-L (ruled for H029 alone) |
| Status | COMPLETE: 1,497.4 s, 7.13 GB; run commit `641abe2`. **Also within CLASS-M** (≤ 30 min, ≤ 8 GB); no swap |
| GPU | device-wide peak 3,560 MiB (688 at start) |
| Development mean | **440.97 s** (E031 440.76; E032 440.91): R1 442.05, R2 267.49, R3 394.90, S1 628.15, W1 472.24; S1c 632.27, W1c 486.40 |
| Integrity | `route_check.py E040 - E029`: PASS |

- **Started by a direct `run_experiment.py` call** on the owner's instruction "No, run now." (INC-0012 amendment, 2026-10-03; N2/C3 route). No run window applied; no INC-0012 deviation.
- **Freeze:** `git diff --stat 9d245c0 <run commit> -- src scripts pyproject.toml uv.lock config research/day-06/eda/d06_diagnostics.py research/day-06/sessions/D06-S01/run_window_2.sh` is **empty**.
- **Environment (rule L v2 item 6):** manifest `python` 3.13.15, `polars_threads` 16; clean tree; no swap pages. GPU: RTX 5060 Laptop, driver 591.91, CUDA 13.1; 688 MiB in use at the start of E040.
- **Role:** control (batch X-D06-S01-0003); no candidate; never NEW; no holdout; ledger decision null. **N4:** E040/E041 are one further draw of E031's / E033's configuration; they are not the Day 7 SUBMIT draw, and no WIN/TIE/LOSS between draws is read as an effect.

## Rule 13 quantities (full size; same scripts and populations for E032, N7)

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| E040 − E031, all rows (s) | +0.18 | −0.08 | +0.10 | −0.00 | +0.84 | −0.41 | +0.16 |
| E032 − E031, all rows (s) | +1.06 | −0.39 | +0.14 | +0.65 | −0.73 | +0.36 | −4.19 |
| RMS prediction change E040 vs E031, all rows (s) | 25.4 | 25.8 | 21.3 | **0.0** | 33.3 | 30.9 | 6.1 |
| RMS prediction change E032 vs E031, all rows (s) | 42.4 | 34.9 | 30.5 | 39.5 | 38.0 | 46.6 | 73.2 |
| RMS change E040 vs E031, `NM_present_excl_LIRF` (s) | 21.1 | 20.8 | 18.5 | 0.0 | 26.4 | 23.7 | 5.9 |

- `NM_present_excl_LIRF`, E040 − E031: mean +0.74 s (q95 +1.18); E032 − E031: +0.68 s.
- **S1 reproduced to floating point:** max |diff| 5.7e-7 s, on 17,176 of 190,713 rows. W1c nearly (max 316 s on single rows; RMS 6.1 s). The other folds differ fully (max |diff| 1.3–3.8 thousand s on single rows). Recorded as observed; no seed/GPU split is drawn from it (N4).
- **CatBoost alone, three-draw spread** (max − min of all-rows RMSE over E031, E032, E040; development folds): R1 1.06, R2 0.39, R3 0.14, S1 0.65, W1 1.57 s.
- **D5-C10 rows:** row 192622644 (S1): E031 10,976, E032 10,237, **E040 10,976** s. Row 183910286 (W1): E031 22,233, E032 18,605, **E040 19,213** s.
- Rule 12 bands (5 development folds, `NM_missing_other` bulk): < 1 h 85, 1–3 h 4, > 3 h 1.
- **Missed predictions:** byte-identity P 0.10 (researcher) / 0.01 (Advisor): not byte-identical, as the Advisor expected. Development mean 440.97 (expected 440.3–441.3; Advisor ≈ 440.8). Largest development-fold change 0.84 s (Advisor ≈ 0.6). RMS change 21–33 s on four folds (expected 25–45), 0 on S1.
