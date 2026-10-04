# E050 analysis: H037 v1 (E044 with the LIRF NM-missing subgroup from E049): **the final submission's predictions** (P4 of X-D07-S01-0003)

**Outcome: COMPLETE; every P4 condition holds, so `predictions/final/E050/submitting.parquet` is the final file.**

| Item | Value |
|---|---|
| Config | `override`, base E044, override E049, subgroup `LIRF_NM_missing`, final folds, CLASS-S |
| Status | COMPLETE: 14.7 s, 3.42 GB, within class; run commit `130a211`; started 22:01:29Z, finished 22:01:45Z (INC-0016) |
| Tree (U3) | `git_dirty_at_run: true` (task-ledger append from the final-fold unmasking only; U3). The post-checkpoint WARNING listed only `orchestration/task-ledger.jsonl` |
| Unmasking (U4) | one event, 22:01:39Z, inside the run span; unmasked silver loaded, no target used (override; the FS0 frame supplies row ids and the subgroup key only) |
| Route check | `route_check.py E050 E044 E049`: PASS (subgroup rows 107 / 276 equal E049; every other row equals E044 exactly) |
| Formatter | `make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050`: **I1–I5 pass**; 344,841 rows; rounding RMS 0.288 s |
| **File** | `predictions/final/E050/submitting.parquet`, **SHA-256 `f0dc2c7c40063e238ef57f51d31192008e37c5327afcdc67d563868af17d06e8`**, 1,094,599 bytes (`research/day-07/submission/SUBMISSION_RECORD_E050.json`) |
| W&B | sync failed (INC-0009) |

## P6 flag (non-blocking; bounds fixed by X-D07-S01-0003)

| | SUBMIT_JAN | SUBMIT_JUL | Flag band |
|---|---|---|---|
| Subgroup share predicted above 3,600 s | 0.682 (of 107) | 0.500 (of 276) | flag if < 0.226 or > 0.981 |
| Subgroup mean prediction: E050 / E044 | 7,274 / 1,760 s | 7,073 / 1,760 s | — |

**No flag.** No flag analysis is open. `research/day-07/submission/E050_P6_flag_U8b.json` holds the figures.

## U8 (b) per-month exposure (target-free; disclosure only)

| | SUBMIT_JAN | SUBMIT_JUL |
|---|---|---|
| Σ(E050 − E044)² on the subgroup | 1.15 × 10¹⁰ s² | 4.79 × 10¹⁰ s² |
| RMS change on the subgroup | 10,367 s | 13,167 s |
| top-1 / top-10 share | 0.31 / 0.79 | 0.11 / 0.74 |
| non-subgroup max \|E050 − E044\| | 0.0 s | 0.0 s |

**In plain words (U6):**
- The two files differ only on 383 Rome rows, but there by hours.
- Per month, the squared difference is about 75,000 s² per row of the whole month in January and about 249,000 s² in July. That is of the order of the whole month's squared error at E033's level (about 370² ≈ 137,000 s² per row on December).
- So the choice moves the month's RMSE by tens to hundreds of seconds, in either direction depending on whether LIRF's block-at-schedule convention holds in 2026.
- December 2025 (one access) favoured E046 by −124.24 s. That is not an estimate for January or July.

## Pre-registered expectations

COMPLETE (met), route check PASS (met), I1–I5 (met), shares inside the flag band (met).
