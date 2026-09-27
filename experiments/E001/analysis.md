# E001: H001 global-mean reference (incumbent)

- **Hypothesis:** H001 v1 (`research/day-01/proposals/H001_v1.md`). Review: ACCEPT (X-D01-S01-0003). Purpose: primary. Seed 42.
- **Config:** `global_mean`, FS0, all seven scored folds, with H predicted only.

## Results

**E001** (H001): status COMPLETE, 8.8 s, peak 3.431 GB, within class True (CLASS-S).

| Fold | RMSE | MAE | Bias |
|---|---|---|---|
| R1 | 560.33 | 301.6 | +0.4 |
| R2 | 437.07 | 298.6 | -1.9 |
| R3 | 532.05 | 302.8 | -6.7 |
| S1 | 746.06 | 324.2 | -39.5 |
| W1 | 628.41 | 324.0 | -10.6 |
| S1c | 746.25 | 323.9 | -43.0 |
| W1c | 628.36 | 324.7 | -7.1 |
| **dev mean** (R1–R3, S1, W1) | **580.79** | | |

RMSE by airport (all rows / bulk y < 3,600 s):

| Airport | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| EDDF | 335 / 334 | 327 / 324 | 377 / 364 | 358 / 347 | 360 / 360 | 356 / 345 | 361 / 361 |
| EDDM | 320 / 302 | 313 / 311 | 369 / 365 | 327 / 312 | 402 / 401 | 325 / 310 | 404 / 403 |
| EGLL | 601 / 561 | 561 / 522 | 531 / 508 | 689 / 582 | 505 / 482 | 692 / 585 | 503 / 480 |
| EHAM | 377 / 372 | 376 / 375 | 403 / 397 | 368 / 358 | 400 / 399 | 366 / 356 | 401 / 400 |
| LEBL | 369 / 369 | 348 / 347 | 307 / 307 | 380 / 380 | 289 / 289 | 380 / 380 | 290 / 290 |
| LEMD | 330 / 330 | 320 / 320 | 294 / 294 | 324 / 324 | 291 / 291 | 325 / 325 | 291 / 291 |
| LFPG | 372 / 347 | 363 / 331 | 501 / 444 | 395 / 344 | 439 / 413 | 396 / 345 | 439 / 413 |
| LIRF | 1485 / 464 | 825 / 476 | 1352 / 387 | 2207 / 595 | 1470 / 366 | 2208 / 596 | 1469 / 366 |
| LSZH | 374 / 372 | 371 / 371 | 415 / 413 | 388 / 376 | 455 / 416 | 386 / 374 | 457 / 418 |
| LTFM | 317 / 315 | 415 / 394 | 379 / 373 | 447 / 427 | 909 / 583 | 448 / 428 | 908 / 582 |

RMSE by taxi band (true target):

| Band | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| <300 | 770 | 769 | 773 | 771 | 776 | 767 | 779 |
| 300-600 | 495 | 496 | 494 | 495 | 496 | 492 | 499 |
| 600-900 | 249 | 249 | 250 | 244 | 251 | 240 | 254 |
| 900-1200 | 98 | 98 | 98 | 100 | 97 | 102 | 95 |
| 1200-1800 | 450 | 448 | 452 | 458 | 446 | 461 | 443 |
| 1800-3600 | 1195 | 1206 | 1226 | 1292 | 1347 | 1295 | 1343 |
| >=3600 | 10044 | 5155 | 9683 | 10592 | 6471 | 10594 | 6469 |

## Pre-registered check

- **Expected:** each fold's RMSE ≈ its validation std (R1 560.3, R2 437.1, R3 532.0, S1 745.0, W1 628.3; development mean ≈ 580).
- **Observed:** 560.33, 437.07, 532.05, 746.06, 628.41; development mean **580.79**.
- **Falsification** (any fold more than 40 s above its std): **not met**. The largest excess is S1 at +1.1 s, which is the train/validation mean shift (bias −39.5 s: July runs longer than the training months).
- **Conclusion:** the runner, masking, evaluator and population pins behave as designed on real data.

## Observations (descriptive; not claims)

- **Tails decide the metric.** The ≥ 3,600 s band has RMSE 5,155–10,594 s, while the 900–1,200 s band sits near 100 s.
- **LIRF dominates.** Its all-row RMSE is 1,352–2,208 s against a bulk (y < 3,600 s) RMSE of 366–596 s. The Advisor's bulk diagnostic is necessary: without it, LIRF masks everything else.
- **Winter tail at LTFM.** On W1 LTFM reaches 909 s (583 s bulk), against 317–447 s on the other folds. This is consistent with the winter-tail evidence in DATASET_AUDIT §6.5.
- **Twins match their folds.** S1 ≈ S1c and W1 ≈ W1c. A constant has no forward exposure; the small differences come from different training means.

## Decision

**Incumbent by pre-registration** (initial-champion rule: H001 is the incumbent, not a tested candidate). Ledger decision: PROMOTE (incumbent). Criteria 1–4 are not applicable. Criterion 7: within class.
