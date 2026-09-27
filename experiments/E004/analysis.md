# E004: H005 unfitted anchor `MVT − AOBT_3` (airport-median fallback)

- **Hypothesis:** H005 v1. Review: ACCEPT (X-D01-S01-0003). Purpose: primary. Seed 42.
- **Comparisons:**
  - `research/comparisons/E004_vs_E003.json` (champion and falsification);
  - `research/comparisons/E004_vs_E002.json` (ablation).

## Results

**E004** (H005): status COMPLETE, 7.4 s, peak 3.473 GB, within class True (CLASS-S).

| Fold | RMSE | MAE | Bias |
|---|---|---|---|
| R1 | 556.83 | 248.0 | -1.9 |
| R2 | 419.82 | 242.4 | +8.2 |
| R3 | 496.48 | 239.3 | +30.3 |
| S1 | 720.65 | 273.0 | -31.7 |
| W1 | 559.45 | 243.8 | +27.1 |
| S1c | 720.73 | 273.0 | -31.9 |
| W1c | 559.58 | 243.8 | +27.0 |
| **dev mean** (R1–R3, S1, W1) | **550.65** | | |

RMSE by airport (all rows / bulk y < 3,600 s):

| Airport | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| EDDF | 248 / 246 | 230 / 226 | 261 / 247 | 298 / 282 | 221 / 221 | 298 / 282 | 221 / 221 |
| EDDM | 318 / 297 | 319 / 317 | 405 / 400 | 337 / 319 | 393 / 392 | 337 / 319 | 394 / 392 |
| EGLL | 455 / 400 | 412 / 351 | 347 / 318 | 608 / 482 | 332 / 310 | 608 / 482 | 332 / 310 |
| EHAM | 400 / 400 | 337 / 337 | 286 / 286 | 393 / 389 | 267 / 267 | 393 / 389 | 267 / 267 |
| LEBL | 363 / 363 | 352 / 351 | 257 / 257 | 401 / 401 | 237 / 237 | 401 / 401 | 237 / 237 |
| LEMD | 307 / 307 | 306 / 306 | 243 / 243 | 309 / 309 | 235 / 235 | 309 / 309 | 235 / 235 |
| LFPG | 407 / 384 | 393 / 365 | 432 / 395 | 458 / 416 | 322 / 299 | 458 / 416 | 322 / 299 |
| LIRF | 1477 / 450 | 803 / 469 | 1350 / 384 | 2080 / 570 | 1466 / 376 | 2080 / 570 | 1467 / 376 |
| LSZH | 250 / 248 | 254 / 252 | 264 / 262 | 296 / 279 | 317 / 253 | 296 / 279 | 316 / 253 |
| LTFM | 522 / 521 | 545 / 531 | 523 / 519 | 572 / 555 | 816 / 581 | 572 / 555 | 816 / 581 |

RMSE by taxi band (true target):

| Band | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| <300 | 518 | 489 | 469 | 520 | 449 | 521 | 448 |
| 300-600 | 342 | 309 | 295 | 348 | 300 | 348 | 300 |
| 600-900 | 319 | 298 | 290 | 314 | 277 | 314 | 277 |
| 900-1200 | 313 | 316 | 296 | 332 | 286 | 332 | 286 |
| 1200-1800 | 383 | 375 | 373 | 419 | 361 | 419 | 361 |
| 1800-3600 | 1023 | 996 | 860 | 1158 | 806 | 1158 | 806 |
| >=3600 | 10012 | 5025 | 9525 | 10011 | 6117 | 10011 | 6119 |

## Against the champion E003 (H003), which is also the falsification test

| Fold | dRMSE (s) | q10…q90 | Outcome | Bulk dRMSE |
|---|---|---|---|---|
| R1 | +35.20 | +28.21…+43.37 | **LOSS** | +53.22 |
| R2 | +31.41 | +24.87…+38.05 | **LOSS** | +37.74 |
| R3 | −7.55 | −16.50…+1.08 | TIE | −6.01 |
| S1 | +2.32 | −33.98…+33.23 | TIE | +51.77 |
| W1 | −50.26 | −70.64…−34.59 | WIN | −47.05 |
| S1c | +1.10 | −32.55…+32.06 | TIE | |
| W1c | −48.48 | −68.36…−32.62 | WIN | |

- **Criterion 1:** mean dRMSE +2.22 s. **Fail.**
- **Criterion 2:** two development LOSSes. **Fail.**
- **Criterion 3:** EDDM +18.1 %, LTFM +15.9 %, EHAM +11.6 % and EGLL +4.6 % exceed the tolerance. **Fail.**
- **Falsification** ("does not pass criteria 1–2 against H003"): **met**.
- **Ablation against H002 (E002):** it also fails criteria 1–3. Mean −3.09 s, q95 +6.16; R1 and R2 LOSS, R3 and W1 WIN, S1 TIE.

## The day-scale LIRF row (review finding; B4 dominant-row report)

| MVT_ID | Airport | `d_aobt3` | Target | H005 prediction | H003 prediction |
|---|---|---|---|---|---|
| 192622644 | LIRF | 87,181 s | **87,002 s** | 87,181 s | 1,020 s |

- **What the row shows.** The recorded block time is on the original day, so the unguarded anchor is almost exact (error 179 s), while any bounded model is off by about 86,000 s.
- **Share of the S1 change.** That one row carries −11.6× the net S1 SSE change (−24.5× on S1c). S1's bulk dRMSE is **+51.8 s**, so without this row H005 is clearly worse on S1 as well.
- **Consequence.** The S1 TIE is an artefact of a single record. The "tail share" figures (−4.2, and +4.8 against H002) exceed 1 in magnitude because the tail and bulk changes have opposite signs. They are reported as computed.

## Observations (for Day 2+, not claims)

- **Winter.** The anchor helps strongly in winter (W1 −50 s, W1c −48 s, bulk −47 s). This is consistent with the pre-registered tail mechanism (de-icing and queues after NM's recorded off-block). Elsewhere, the raw anchor's noise (negative values, NM rounding) makes it worse than a median in the bulk (R1 +53 s, R2 +38 s).
- **Airport-specific anchor quality.** Criterion 3 fails at EDDM, LTFM and EHAM.
- **Day-scale anchors carry information.** The one validated case has a day-scale target. July 2026 contains one similar row (LIRF, anchor 86,340 s; review finding). Whether bounded models should defer to extreme anchors is a candidate question for a later, pre-registered hypothesis. With n = 1 in training data, no rule can be claimed from it.

## Decision

**REJECT** (falsification met; criteria 1–3 fail against the champion). The champion remains E003. Criterion 7: within CLASS-S (7.4 s, 3.47 GB).
