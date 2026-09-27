# E005: H004 ridge on FS0

- **Hypothesis:** H004 v1. Review: ACCEPT (X-D01-S01-0003). Purpose: primary. Seed 42.
- **Reproduction:** E009 (seed 43).
- **Comparisons:**
  - `research/comparisons/E005_vs_E003.json` (champion; falsification clause 1);
  - `research/comparisons/E005_vs_E004.json` (clause 2 and ablation);
  - `research/comparisons/E005_vs_E004_clip_attribution.json` (the review's missing control).

## Results

**E005** (H004): status COMPLETE, 94.1 s, peak 3.755 GB, within class True (CLASS-S).

| Fold | RMSE | MAE | Bias |
|---|---|---|---|
| R1 | 477.81 | 202.2 | +13.7 |
| R2 | 323.53 | 192.9 | +2.1 |
| R3 | 431.61 | 191.6 | -10.8 |
| S1 | 670.01 | 226.9 | +10.1 |
| W1 | 510.67 | 200.8 | -27.6 |
| S1c | 670.99 | 229.3 | +14.5 |
| W1c | 509.91 | 197.9 | -19.5 |
| **dev mean** (R1–R3, S1, W1) | **482.73** | | |

RMSE by airport (all rows / bulk y < 3,600 s):

| Airport | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| EDDF | 225 / 223 | 213 / 210 | 245 / 233 | 256 / 244 | 213 / 213 | 257 / 245 | 206 / 206 |
| EDDM | 231 / 209 | 212 / 210 | 271 / 267 | 242 / 225 | 266 / 265 | 243 / 227 | 266 / 265 |
| EGLL | 340 / 289 | 309 / 254 | 273 / 246 | 446 / 321 | 262 / 235 | 447 / 322 | 266 / 243 |
| EHAM | 264 / 260 | 241 / 240 | 227 / 223 | 276 / 266 | 223 / 222 | 285 / 275 | 231 / 231 |
| LEBL | 294 / 294 | 273 / 272 | 219 / 219 | 317 / 317 | 194 / 194 | 320 / 320 | 194 / 194 |
| LEMD | 250 / 250 | 249 / 249 | 226 / 226 | 259 / 259 | 207 / 207 | 262 / 262 | 201 / 201 |
| LFPG | 294 / 268 | 293 / 261 | 350 / 299 | 335 / 288 | 288 / 263 | 337 / 290 | 276 / 253 |
| LIRF | 1412 / 376 | 716 / 382 | 1314 / 349 | 2109 / 443 | 1437 / 340 | 2106 / 442 | 1432 / 314 |
| LSZH | 229 / 227 | 222 / 220 | 241 / 240 | 269 / 253 | 291 / 225 | 274 / 259 | 282 / 216 |
| LTFM | 295 / 293 | 324 / 304 | 288 / 283 | 370 / 351 | 684 / 397 | 380 / 362 | 690 / 401 |

RMSE by taxi band (true target):

| Band | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| <300 | 440 | 414 | 402 | 475 | 385 | 484 | 403 |
| 300-600 | 281 | 262 | 244 | 305 | 238 | 310 | 241 |
| 600-900 | 224 | 211 | 205 | 238 | 193 | 244 | 197 |
| 900-1200 | 208 | 198 | 195 | 217 | 180 | 226 | 187 |
| 1200-1800 | 271 | 262 | 271 | 271 | 269 | 275 | 271 |
| 1800-3600 | 745 | 763 | 709 | 848 | 787 | 840 | 738 |
| >=3600 | 9637 | 4591 | 9308 | 10201 | 5997 | 10186 | 6007 |

## Promotion test against the champion E003 (H003)

| Fold | dRMSE (s) | q10…q90 | Outcome | Bulk dRMSE |
|---|---|---|---|---|
| R1 | −43.82 | −49.10…−39.78 | WIN | −53.75 |
| R2 | −64.89 | −68.49…−61.58 | WIN | −65.04 |
| R3 | −72.42 | −90.88…−61.28 | WIN | −95.78 |
| S1 | −48.33 | −55.30…−43.46 | WIN | −64.71 |
| W1 | −99.05 | −130.80…−76.83 | WIN | −121.10 |
| S1c | −48.64 | −55.59…−43.85 | WIN | |
| W1c | −98.15 | −129.65…−76.76 | WIN | |

- **Criterion 1:** mean **−65.70 s**, q95 −59.56 s. Pass.
- **Criterion 2:** 5 of 5 WIN, twins WIN. Pass.
- **Criterion 3:** pass.
- **Tail share:** 0.254, so most of the margin is in the bulk.
- **Row concentration:** the largest single row carries ≤ 0.02 of each fold's change.
- **Forward exposure:** signs hold (S1c −48.64 s, W1c −98.15 s).

## Falsification clause 2 and ablation: against H005 (E004, the unfitted anchor)

- **Result.** Pass on every fold: mean −67.92 s, all 7 WIN, tail share 0.052.
- **The LIRF day-scale row works against H004** (top-1 share −0.53 on S1). Ridge predicts 2,513 s against a target of 87,002 s, while H005 is exact. H004 wins S1 anyway (bulk −116 s).
- **Missing control (review): does winsorisation carry the margin?** Rows whose `d_aobt3` lies beyond the fold's training clip (0.5 / 99.5 % quantiles, about 298…2,430 s) are about 1 % of rows. They carry this share of H004's SSE advantage over H005:

  | Fold | R1 | R2 | R3 | S1 | W1 |
  |---|---|---|---|---|---|
  | Share | 0.395 | 0.350 | 0.263 | 0.048 | 0.106 |

  The majority (60–95 %) comes from rows inside the clip, so the linear bias-correction mechanism is supported. Clipping is a substantial secondary contributor on R1–R3, and I do not claim otherwise.

## Other criteria

- **Reproduction:** E009 is exact, and criteria 1–3 hold against E003.
- **Criterion 4:** supported, with the clip caveat above.
- **Criterion 5:** all transforms are fold-local.
- **Criterion 7:** CLASS-S, 94 s, **3.76 GB** peak, under the 4 GB target that the review flagged as at risk.
- **Criterion 8:** no open objection (B3: S1c < 0).
- **Pre-registered magnitude** ("mean 400–470 s"): observed **482.73**, above the range. Recorded as a miss of the magnitude prediction.

## Decision

**PROMOTE.** H004 becomes the champion (chain step 4).
