# E010: H008 ablation of H006 (LightGBM, FS0 without the four time-delta features)

- **Hypothesis:** H008 v1. Review: ACCEPT (X-D01-S01-0003). Purpose: primary. Seed 42.
- **Role:** ablation only, never a candidate.

## Results

**E010** (H008): status COMPLETE, 443.8 s, peak 3.626 GB, within class True (CLASS-M).

| Fold | RMSE | MAE | Bias |
|---|---|---|---|
| R1 | 454.97 | 221.8 | -15.1 |
| R2 | 356.55 | 219.4 | -7.4 |
| R3 | 467.98 | 235.1 | +10.2 |
| S1 | 667.56 | 249.4 | -39.2 |
| W1 | 564.63 | 259.6 | +3.1 |
| S1c | 685.86 | 253.3 | -45.2 |
| W1c | 583.95 | 273.9 | -6.2 |
| **dev mean** (R1–R3, S1, W1) | **502.34** | | |

RMSE by airport (all rows / bulk y < 3,600 s):

| Airport | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| EDDF | 280 / 278 | 264 / 261 | 336 / 321 | 303 / 290 | 297 / 297 | 305 / 292 | 307 / 307 |
| EDDM | 237 / 211 | 226 / 224 | 313 / 308 | 249 / 227 | 344 / 343 | 250 / 228 | 381 / 379 |
| EGLL | 412 / 363 | 383 / 335 | 366 / 341 | 514 / 392 | 367 / 340 | 519 / 397 | 380 / 355 |
| EHAM | 201 / 193 | 201 / 199 | 264 / 256 | 210 / 192 | 290 / 289 | 212 / 193 | 323 / 322 |
| LEBL | 352 / 352 | 328 / 328 | 282 / 282 | 369 / 369 | 269 / 269 | 372 / 372 | 262 / 262 |
| LEMD | 284 / 284 | 283 / 283 | 270 / 270 | 285 / 285 | 270 / 270 | 287 / 287 | 273 / 273 |
| LFPG | 334 / 306 | 323 / 290 | 455 / 398 | 368 / 317 | 411 / 387 | 400 / 353 | 519 / 502 |
| LIRF | 1246 / 621 | 751 / 569 | 1285 / 453 | 2037 / 857 | 1412 / 445 | 2097 / 898 | 1403 / 422 |
| LSZH | 232 / 230 | 241 / 240 | 314 / 312 | 270 / 252 | 362 / 306 | 277 / 259 | 361 / 309 |
| LTFM | 295 / 293 | 369 / 349 | 332 / 327 | 436 / 417 | 809 / 497 | 442 / 424 | 839 / 535 |

RMSE by taxi band (true target):

| Band | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| <300 | 478 | 503 | 445 | 469 | 474 | 503 | 461 |
| 300-600 | 296 | 295 | 313 | 329 | 322 | 334 | 342 |
| 600-900 | 249 | 229 | 241 | 282 | 246 | 295 | 283 |
| 900-1200 | 245 | 232 | 219 | 286 | 221 | 304 | 262 |
| 1200-1800 | 357 | 344 | 342 | 420 | 337 | 434 | 367 |
| 1800-3600 | 937 | 957 | 1008 | 1073 | 1139 | 1088 | 1176 |
| >=3600 | 7810 | 4013 | 8998 | 9268 | 6043 | 9494 | 6052 |

## Use

- **H006 against H008:** H006 passes criteria 1–3 (mean −124.47 s, all 7 WIN, tail share 0.605). Removing `d_aobt3`, `d_eobt1`, `d_sched` and `flt_missing` costs about 124 s of development RMSE. The deltas are used.
- **Expected Result:** internally inconsistent, as recorded in the ack. It is not scored as a prediction.
- **The row-level-only signal** (no NM or schedule deltas) reaches a development mean of 502.34. That is below H003 (548.42) and above ridge with the deltas (482.73).

## Decision

No promotion decision by design (ablation). Criterion 7: CLASS-M, 444 s, 3.63 GB.
