# E031 analysis: H021 v3 (CatBoost on GPU, categorical statistics on raw keys)

**COMPLETE; route integrity holds; clause 1 provisionally NOT MET (mechanism supported), pending the noise condition.** H021 is a component and mechanism experiment, **not a promotion candidate** (pre-registered), whatever its accuracy.

**Paused after this run (INC-0011).** The unconditional seed-43 reproduction (H021r) has not run, so clause 1's noise condition has no value yet, and **clause 1 has no final verdict.**

## Run

| Item | Value |
|---|---|
| Allocation | `gate.py allocate H021 v3`, committed `0a5512a` (clean; nothing outside the record directories differs from `803ceeb`) |
| Config | as authorized: `routed_catboost`, FS2_RAW, H021 v3's table, `cat_mode: ctr`, seed 42, all 8 folds, CLASS-L |
| Status | COMPLETE: **1,522.9 s (25.4 min), peak RSS 7.01 GB**, within CLASS-L |
| CLASS-M comparison (CLASS-L condition) | runtime 25.4 min against 30 min: **inside**. RAM 7.01 GB against 8 GB: **inside** |
| GPU | device peak 3,956 MiB, including 853 MiB of desktop use |
| Swap | **0 pages** (INC-0010) |
| Environment (rule L v2 item 6) | 3.13.15, 16 polars threads, lock `efa4fd78…`, no thread variables: **matches** |
| Development mean | **440.76 s**: R1 441.87, R2 267.57, R3 394.81, S1 628.15, W1 471.40; S1c 632.68, W1c 486.24 |

## Post-run steps (H021 v3 Validation Plan)

- **Integrity:** `route_check.py E031 - E029` passes on all 8 folds; the routed rows are bit-identical.
- **Clause 1:** `mechanism_check.py E031 E030 NM_present_excl_LIRF` gives **mean −4.91 s** (q95 −4.28).

  | Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
  |---|---|---|---|---|---|---|---|
  | dRMSE (s) | −4.32 | −5.99 | −4.40 | −4.06 | −5.80 | −2.30 | −7.20 |
  | Outcome | WIN | WIN | WIN | WIN | WIN | WIN | WIN |

  - The counted WINs (twin rule) are 5 of 5, and the mean is below −3.0 s. **Clause 1 is not met: the categorical statistics carry signal on normal taxis at fixed capacity, at this budget.**
  - **Provisional.** The noise condition (|H021r − H021| > 1.5 s on this population means INCONCLUSIVE) needs H021r, which is paused.
- **Comparability** (H022 v3's closed set; per fold for all 8 folds, `research/comparisons/resolved_params_E031_vs_E030.json`): every differing key is inside the closed set on every fold, so **the pair is matched.** Differing keys: `cat_mode`, `data_partition` and `n_cat_features`. Present in the CTR arm only: the 10 CTR keys.
- **Reported, all rows:**
  - against **E030 (H022): −5.74 s** (q95 −4.95), WIN on all 7 folds, no airport degraded;
  - against **E029 (E023's instance, LightGBM): −1.69 s** (q95 −0.74). R1 −1.52 WIN, R2 −2.12 WIN, R3 −1.14 WIN, **S1 −4.14 WIN**, W1 +0.46 TIE; S1c −4.55 WIN, W1c −0.71 TIE. No airport degraded.
- **Rule 12** (`NM_missing_other` bulk, 5 development folds): < 1 h 86, 1–3 h 4, **> 3 h 0**, total 90 (E029: 82, 12, 5 and 99; E030: 25, 5, 4 and 34).
- **Single rows:**
  - row 192622644 (S1, y 87,002 s): **E031 10,976 s**. E026 8,136, E029 7,041, E030 11,554;
  - row 183910286 (W1, y 13,865 s): **E031 22,233 s**. E026 1,979, E029 7,938, E030 21,259.
- **Learning curves** (development mean): E031 441.49 at iteration 800 against 440.76 at 1,000 (−0.73 s); E030 447.69 against 446.50 (−1.19 s). Both are still falling at 1,000; clause 1 is read at this budget.
- **2026 unseen levels** (rule 2; target-free; `research/day-05/eda/unseen_levels_2026.json`): the share of ranking rows with a raw level never seen in 2025 is January 0.02–0.04 % and July 0.00–0.43 % (op_prefix highest).

## Pre-registered expectations against outcomes (kept)

| Expectation (H021 v3) | Outcome |
|---|---|
| H021 − H022, `NM_present_excl_LIRF`: −6 to −25 s, central −12; ≥ 4 WINs | **−4.91 s: outside (smaller effect)**; 5 WINs |
| H021 − E029 on `NM_present_excl_LIRF`: +2 to +15 s (CatBoost worse); P(< 0) 0.20 | not computed here. **All rows: −1.69 s, CatBoost better** |
| H021 − E029, all rows: 0 to +15 s | **−1.69 s: outside (better)** |
| Development mean 443–458 s | **440.76: outside (better)** |
| > 3 h band ≤ 10 | 0: inside |
| Row 192622644 **lower** than E029 (1,500–7,000 s) | **10,976 s: wrong direction** |
| Row 183910286 lower than E029 | **22,233 s: wrong direction** |
| Validation still falling over 800–1,000 by 0.5–3 s | −0.73 s: inside |

- **The symmetric-tree "bounded extreme predictions" reasoning was wrong for the day-scale rows.** Both CatBoost arms predict *higher* than the LightGBM on the two LIRF NM-present tail rows. The H020 review's prediction (that CatBoost bounds predictions more tightly) holds for the `NM_missing_other` out-of-range counts, but not for these rows.
- **Consequence for H023 (recorded, not acted on).** H023's Missing Control 1 pre-registered that the blend would lower the S1 row's prediction. With E031 at 10,976 s, the blend would be about 9,000 s, above E026's 8,136 s, so moving towards y. The pre-registration stands as written, and its miss will be recorded if H023 runs.

## Clause 1 final verdict (appended 2026-10-02, D05-S05)

H021r (E032) gives m = +0.683 s on `NM_present_excl_LIRF`, inside the 1.5 s noise limit. **Clause 1 is NOT MET, a final verdict: the mechanism is supported.** E032's own reproduction tolerance fails on R1 (+1.056 s), which does not bear on H021 (not a candidate). See the E032 analysis.
