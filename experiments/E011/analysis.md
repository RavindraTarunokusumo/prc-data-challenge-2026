# E011: H007 XGBoost on FS0

- **Hypothesis:** H007 v1. Review: ACCEPT (X-D01-S01-0003). Purpose: primary. Seed 42.
- **Comparisons:** `research/comparisons/E011_vs_{E005,E006,E010}.json` and `E011_vs_E005_tail_mechanism.json`.

## Results

**E011** (H007): status COMPLETE, 1137.8 s, peak 3.853 GB, within class True (CLASS-M).

| Fold | RMSE | MAE | Bias |
|---|---|---|---|
| R1 | 413.15 | 169.5 | +5.7 |
| R2 | 293.68 | 161.9 | -2.1 |
| R3 | 350.25 | 156.6 | -7.1 |
| S1 | 627.95 | 192.7 | +3.7 |
| W1 | 438.31 | 165.3 | -18.3 |
| S1c | 625.24 | 195.3 | +1.4 |
| W1c | 459.13 | 173.0 | -16.7 |
| **dev mean** (R1–R3, S1, W1) | **424.67** | | |

RMSE by airport (all rows / bulk y < 3,600 s):

| Airport | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| EDDF | 193 / 191 | 181 / 178 | 214 / 205 | 224 / 211 | 174 / 174 | 227 / 214 | 178 / 178 |
| EDDM | 199 / 172 | 172 / 169 | 181 / 177 | 205 / 185 | 174 / 172 | 208 / 185 | 176 / 172 |
| EGLL | 281 / 261 | 254 / 231 | 232 / 225 | 347 / 281 | 227 / 215 | 357 / 287 | 240 / 230 |
| EHAM | 191 / 187 | 181 / 181 | 185 / 183 | 202 / 188 | 200 / 200 | 209 / 194 | 295 / 295 |
| LEBL | 296 / 296 | 231 / 231 | 181 / 181 | 287 / 287 | 162 / 162 | 292 / 292 | 172 / 172 |
| LEMD | 198 / 198 | 206 / 206 | 188 / 188 | 216 / 216 | 164 / 164 | 220 / 220 | 177 / 177 |
| LFPG | 288 / 263 | 286 / 257 | 351 / 315 | 323 / 287 | 242 / 231 | 345 / 307 | 380 / 368 |
| LIRF | 1218 / 698 | 702 / 424 | 1026 / 322 | 2021 / 1148 | 1219 / 312 | 1979 / 913 | 1079 / 325 |
| LSZH | 198 / 195 | 198 / 197 | 210 / 208 | 230 / 213 | 269 / 207 | 379 / 370 | 262 / 195 |
| LTFM | 256 / 254 | 287 / 272 | 237 / 234 | 328 / 310 | 615 / 352 | 337 / 319 | 760 / 528 |

RMSE by taxi band (true target):

| Band | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| <300 | 337 | 344 | 310 | 361 | 294 | 808 | 777 |
| 300-600 | 220 | 197 | 217 | 253 | 182 | 262 | 261 |
| 600-900 | 212 | 189 | 184 | 389 | 164 | 302 | 216 |
| 900-1200 | 341 | 197 | 181 | 411 | 176 | 340 | 211 |
| 1200-1800 | 287 | 254 | 244 | 353 | 247 | 351 | 298 |
| 1800-3600 | 659 | 691 | 592 | 783 | 660 | 800 | 824 |
| >=3600 | 7106 | 4100 | 7156 | 8256 | 5128 | 8683 | 4791 |

## Against the champion E005 (ridge), which is also falsification clause 1

- **Result.** Mean −58.06 s (q95 −32.46). R1, R2, R3 and W1 WIN; **S1 TIE** (−42.06, q10…q90 −113.76…+31.05); S1c WIN; W1c TIE. **Criterion 2 fails** (S1 must WIN).
- **Bulk dRMSE:** S1 +98.45 s, R1 +22.76 s (worse than ridge in the bulk).
- **Tail attribution.** Tail share 1.19. On R1, R3, S1 and W1 the gain comes mostly from tail rows without NM data, the same pattern as H006.
- **Dominant rows (B4):**

  | Fold | MVT_ID | Airport | Anchor | Target | H007 | Ridge |
  |---|---|---|---|---|---|---|
  | R2 | 198941714 | LIRF | none | 11,349 | 54,135 | 1,870 |
  | S1 | 192628959 | LIRF | none | **87,186** | 63,623 | 1,783 |
  | W1c | 183903219 | LIRF | none | 131,167 | 38,872 | 1,762 |

  S1's dominant row is a **second day-scale LIRF record, and this one has no NM data**.

## Other checks

- **Clause 2 (more than 5 % from H006):** 424.67 against 377.87 is **+12.4 %**, so the clause is met. Per the review, the difference is attributed to the configuration (minimum leaf size 10 against 100, depth-wise growth), not to the library.
- **Against H006:** fails 1–3 (mean +46.80 s).
- **Against H008:** criterion 2 fails (cross-implementation check, recorded as such).

## Decision

**REJECT.** Falsification clauses 1 and 2 are both met (B2), and criteria 1–2 fail against the champion. Criterion 7: CLASS-M, 1,138 s, 3.85 GB.
