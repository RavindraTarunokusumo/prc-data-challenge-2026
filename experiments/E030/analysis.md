# E030 analysis: H022 v3 (CatBoost on GPU, categorical columns as integer codes; matched control)

**COMPLETE; route integrity holds.** H022 carries no claim of its own: it is the matched control for H021's clause 1 (`H022_v3.md`), so no decision is recorded here.

## Run

| Item | Value |
|---|---|
| Allocation | `gate.py allocate H022 v3`, committed `d8407e0` (clean tree; nothing outside the record directories differs from the freeze anchor `803ceeb`) |
| Config | as authorized: `routed_catboost`, FS2_RAW, H021 v3's parameters with `cat_mode: codes`, seed 42, all 8 folds, CLASS-M |
| Status | COMPLETE: **224.9 s, peak RSS 6.40 GB, within CLASS-M** |
| GPU | device peak 3,773 MiB, including 853 MiB of desktop use at start (`gpu_mib_peak`) |
| Swap | **0 pages swapped out** during the run (INC-0010) |
| Environment (rule L v2 item 6) | `python` 3.13.15, `polars_threads` 16, lock `efa4fd78…`, no thread variables set: **matches** |
| Resolved parameters | `resolved_params.json`, 8 folds: `cat_mode` codes, 0 categorical features, `data_partition` DocParallel, `boosting_type` Plain |
| Development mean | **446.50 s**: R1 450.10, R2 276.10, R3 398.14, S1 632.05, W1 476.11; S1c 635.91, W1c 494.66 |

The runtime is far below the 8–14 min estimate. The per-fold fit plus feature build took 11–37 s, against the calibration's 36 s for one R3 fit alone (the calibration ran two fits and timed both).

## Post-run steps (H022 v3 Validation Plan)

- **`route_check.py E030 - E029`: passes on all 8 folds.** The routed rows equal E029's bit for bit (168, 115, 52, 337, 58, 337, 58 and 88 rows). The FS2_RAW frame path reproduces the LightGBM path's ridge, as the target-free diagnosis predicted.
- **`compare.py E030 E029`** (reported; a family contrast, not a matched procedure):
  - mean dRMSE **+4.05 s** (q95 +5.68);
  - R1 +6.71 LOSS, R2 +6.40 LOSS, R3 +2.19 LOSS, **S1 −0.25 TIE**, W1 +5.18 LOSS; S1c −1.32 TIE, W1c +7.70 LOSS;
  - airports degraded beyond 3 %: EHAM +8.9 %, EDDF +4.8 %, LEMD +4.7 %, LSZH +4.1 %, EDDM +3.2 %.
  - H022's expectation (+8 to +35 s against E029 on all rows) is **missed on the favourable side**: the codes arm is closer to the LightGBM than expected.
- **`range_check.py E030 --bands`** (rule 12; `NM_missing_other` bulk rows, 5 development folds): < 1 h 25, 1–3 h 5, **> 3 h 4**, total 34. E029: 82, 12, 5, total 99. **Symmetric trees bound extreme predictions**: the generic < 1 h band falls from 82 to 25.
- **Learning curve:** the development-mean validation RMSE is 447.69 s at iteration 800 and 446.50 s at 1,000, still falling (its minimum is at 1,000). Recorded "at this budget".
- **The comparability check** against H021 runs after H021 (H022 v3).
