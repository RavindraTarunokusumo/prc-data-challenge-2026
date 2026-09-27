# E002: H002 airport median

- **Hypothesis:** H002 v1. Review: ACCEPT (X-D01-S01-0003). Purpose: primary. Seed 42.
- **Reproduction:** E007 (seed 43).
- **Comparison:** `research/comparisons/E002_vs_E001.json`.

## Results

**E002** (H002): status COMPLETE, 8.6 s, peak 3.459 GB, within class True (CLASS-S).

| Fold | RMSE | MAE | Bias |
|---|---|---|---|
| R1 | 529.97 | 256.2 | -64.2 |
| R2 | 397.52 | 251.5 | -60.7 |
| R3 | 507.31 | 260.9 | -59.8 |
| S1 | 723.86 | 283.5 | -97.2 |
| W1 | 610.02 | 284.2 | -62.1 |
| S1c | 725.04 | 284.7 | -106.1 |
| W1c | 612.09 | 282.7 | -93.3 |
| **dev mean** (R1–R3, S1, W1) | **553.74** | | |

RMSE by airport (all rows / bulk y < 3,600 s):

| Airport | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| EDDF | 317 / 315 | 304 / 301 | 370 / 356 | 339 / 327 | 329 / 329 | 340 / 328 | 330 / 330 |
| EDDM | 267 / 242 | 252 / 250 | 343 / 338 | 274 / 254 | 375 / 373 | 282 / 262 | 384 / 383 |
| EGLL | 442 / 394 | 410 / 363 | 387 / 361 | 539 / 417 | 384 / 358 | 540 / 418 | 389 / 362 |
| EHAM | 277 / 270 | 265 / 263 | 337 / 329 | 312 / 300 | 370 / 369 | 310 / 297 | 371 / 370 |
| LEBL | 377 / 377 | 354 / 354 | 297 / 297 | 394 / 394 | 277 / 277 | 395 / 395 | 285 / 285 |
| LEMD | 331 / 331 | 320 / 320 | 294 / 294 | 325 / 325 | 291 / 291 | 326 / 326 | 292 / 292 |
| LFPG | 395 / 370 | 372 / 340 | 511 / 454 | 400 / 349 | 440 / 414 | 413 / 362 | 448 / 422 |
| LIRF | 1480 / 454 | 816 / 465 | 1350 / 385 | 2200 / 581 | 1468 / 365 | 2200 / 581 | 1469 / 365 |
| LSZH | 265 / 263 | 257 / 256 | 348 / 346 | 304 / 287 | 383 / 333 | 304 / 287 | 384 / 334 |
| LTFM | 318 / 316 | 422 / 401 | 385 / 380 | 453 / 433 | 917 / 590 | 453 / 434 | 917 / 590 |

RMSE by taxi band (true target):

| Band | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| <300 | 567 | 562 | 560 | 565 | 571 | 567 | 556 |
| 300-600 | 337 | 335 | 338 | 341 | 345 | 336 | 320 |
| 600-900 | 176 | 180 | 190 | 180 | 198 | 173 | 175 |
| 900-1200 | 190 | 185 | 185 | 192 | 190 | 197 | 197 |
| 1200-1800 | 430 | 418 | 433 | 438 | 424 | 446 | 451 |
| 1800-3600 | 1099 | 1130 | 1198 | 1219 | 1343 | 1226 | 1364 |
| >=3600 | 10011 | 5104 | 9668 | 10552 | 6474 | 10553 | 6478 |

## Promotion test against the champion E001 (H001), which is also H002's ablation

| Fold | dRMSE (s) | q10…q90 | Outcome | Bulk dRMSE |
|---|---|---|---|---|
| R1 | −30.36 | −36.56…−25.08 | WIN | −44.46 |
| R2 | −39.55 | −44.72…−34.38 | WIN | −44.64 |
| R3 | −24.74 | −31.84…−19.71 | WIN | −33.69 |
| S1 | −22.20 | −27.43…−18.22 | WIN | −37.73 |
| W1 | −18.39 | −24.90…−13.74 | WIN | −28.72 |
| S1c | −21.21 | −26.27…−17.30 | WIN | |
| W1c | −16.28 | −22.62…−11.95 | WIN | |

- **Criterion 1:** mean dRMSE **−27.05 s**, q95 −24.51 s. Pass.
- **Criterion 2:** 5 of 5 development folds WIN, and both twins WIN. Pass.
- **Criterion 3:** no airport degrades beyond 3 %. Pass.
- **Tail attribution (standing rule 1):** the tail's share of the SSE change is **0.037**. The gain is in the bulk.
- **Row concentration (B4):** the largest row carries ≤ 0.5 % of each fold's SSE change, and the 10 largest rows ≤ 1 %.
- **Forward exposure (standing rule 2, B3):** the pre-registered signs hold (S1c −21.21 s and W1c −16.28 s, both < 0).
  - The LFPG contrast the review asked for: RMSE is 400.5 on S1 against 412.6 on S1c, and bias −76.6 s against −125.6 s.
  - S1's post-July training months (the higher LFPG regime) help S1 at LFPG by about 12 s, as the review predicted.
  - LFPG is slightly worse than under the global mean (395.2 on S1), consistent with the review's criterion-3 note (+0.8 %).
- **Reproduction (criterion 6):** E007 is bit-identical (dRMSE 0.0 on every fold), and criteria 1–3 hold for it against E001 (`research/comparisons/repro_E007_of_E002.json`).
- **Criterion 4:** the ablation is H001, and the comparison above passes. The mean-vs-median confound works against H002 (review finding 1), so the pass is conservative evidence for the airport mechanism.
- **Criterion 5:** no leakage (medians come from training rows only). **Criterion 7:** within CLASS-S (8.6 s, 3.46 GB). **Criterion 8:** no open objection (B3 satisfied).
- **Falsification** ("does not pass criteria 1–2 against H001"): **not met**.

## Decision

**PROMOTE.** H002 becomes the champion (step 1 of the pre-registered chain).
