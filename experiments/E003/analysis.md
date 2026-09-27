# E003: H003 airport × UTC-hour median

- **Hypothesis:** H003 v1. Review: ACCEPT (X-D01-S01-0003). Purpose: primary. Seed 42.
- **Reproduction:** E008 (seed 43).
- **Comparison:** `research/comparisons/E003_vs_E002.json`.

## Results

**E003** (H003): status COMPLETE, 8.8 s, peak 3.493 GB, within class True (CLASS-S).

| Fold | RMSE | MAE | Bias |
|---|---|---|---|
| R1 | 521.63 | 245.8 | -61.9 |
| R2 | 388.41 | 243.4 | -58.8 |
| R3 | 504.03 | 257.7 | -49.2 |
| S1 | 718.34 | 275.6 | -100.8 |
| W1 | 609.71 | 283.5 | -48.3 |
| S1c | 719.63 | 276.9 | -106.6 |
| W1c | 608.06 | 276.1 | -86.8 |
| **dev mean** (R1–R3, S1, W1) | **548.42** | | |

RMSE by airport (all rows / bulk y < 3,600 s):

| Airport | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| EDDF | 311 / 309 | 297 / 294 | 366 / 351 | 333 / 320 | 325 / 325 | 335 / 322 | 323 / 323 |
| EDDM | 264 / 239 | 249 / 247 | 345 / 340 | 272 / 251 | 376 / 375 | 275 / 254 | 369 / 368 |
| EGLL | 428 / 379 | 397 / 348 | 373 / 346 | 530 / 407 | 372 / 345 | 533 / 409 | 375 / 348 |
| EHAM | 270 / 264 | 260 / 259 | 337 / 329 | 310 / 297 | 370 / 368 | 306 / 294 | 368 / 367 |
| LEBL | 368 / 368 | 345 / 345 | 293 / 293 | 386 / 386 | 276 / 276 | 388 / 388 | 277 / 277 |
| LEMD | 327 / 327 | 318 / 318 | 296 / 296 | 320 / 320 | 292 / 292 | 322 / 322 | 290 / 290 |
| LFPG | 370 / 344 | 360 / 328 | 505 / 449 | 393 / 341 | 436 / 410 | 404 / 352 | 433 / 407 |
| LIRF | 1470 / 429 | 800 / 443 | 1350 / 390 | 2191 / 553 | 1471 / 377 | 2191 / 555 | 1470 / 364 |
| LSZH | 258 / 255 | 251 / 249 | 344 / 343 | 299 / 281 | 383 / 333 | 299 / 281 | 374 / 322 |
| LTFM | 305 / 303 | 411 / 390 | 378 / 372 | 444 / 424 | 920 / 588 | 446 / 426 | 918 / 584 |

RMSE by taxi band (true target):

| Band | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| <300 | 553 | 549 | 559 | 552 | 578 | 556 | 544 |
| 300-600 | 324 | 324 | 343 | 325 | 353 | 325 | 316 |
| 600-900 | 174 | 178 | 198 | 174 | 210 | 168 | 179 |
| 900-1200 | 190 | 188 | 186 | 196 | 191 | 197 | 194 |
| 1200-1800 | 407 | 400 | 417 | 426 | 409 | 433 | 431 |
| 1800-3600 | 1057 | 1093 | 1178 | 1188 | 1327 | 1198 | 1341 |
| >=3600 | 9996 | 5070 | 9652 | 10537 | 6488 | 10540 | 6496 |

## Promotion test against the champion E002 (H002), which is also H003's ablation

| Fold | dRMSE (s) | q10…q90 | Outcome | Bulk dRMSE |
|---|---|---|---|---|
| R1 | −8.35 | −9.54…−7.46 | WIN | −12.50 |
| R2 | −9.11 | −9.90…−8.34 | WIN | −9.89 |
| R3 | −3.28 | −4.14…−2.69 | WIN | −4.05 |
| S1 | −5.53 | −6.38…−4.86 | WIN | −9.36 |
| W1 | −0.31 | −1.27…+0.49 | TIE | −1.72 |
| S1c | −5.41 | −6.28…−4.80 | WIN | |
| W1c | −4.03 | −5.88…−2.87 | WIN | |

- **Criterion 1:** mean dRMSE **−5.31 s**, q95 −4.90 s. Pass.
- **Criterion 2:** 4 of 5 development folds WIN (S1 among them), W1 TIE, no LOSS. Pass.
- **Criterion 3:** pass.
- **Tail share of the SSE change:** 0.065.
- **Row concentration (B4):** largest single-row shares ≤ 0.03 on every fold except W1. There, one row carries −0.33 of the (small) net change, i.e. it moves the opposite way. That is below the 0.5 reporting threshold.
- **Forward exposure:** signs hold (S1c −5.41 s, W1c −4.03 s). W1 is a TIE while W1c is a WIN, the reversal the review predicted from daylight saving. W1 trains on DST-shifted summer months, whereas W1c's January training month shares February's UTC offset.
- **Reproduction:** E008 is exact, and criteria 1–3 hold against E002.
- **Criteria 4, 5, 7, 8:** ablation = H002, pass. No leakage. CLASS-S (8.8 s, 3.49 GB). No open objection.
- **Falsification:** not met.
- **Pre-registered magnitude:** "1–3 % below H002". Observed 0.96 %, just **below** the predicted range. Recorded as a near-miss of the prediction; it is not a falsification criterion.

## Interpretation, bounded by the review

The takeoff hour is label T. A long taxi pushes the same pushback into a later takeoff hour, so this design shows that time of day carries signal. It does **not** show that diurnal demand is the mechanism (review finding 1). A causal-only variant needs a P-labelled time key, such as scheduled or EOBT hour.

## Decision

**PROMOTE.** H003 becomes the champion (chain step 2).
