# E006: H006 LightGBM on FS0

- **Hypothesis:** H006 v1. Review: ACCEPT (X-D01-S01-0003). Purpose: primary. Seed 42.
- **Comparisons:**
  - `research/comparisons/E006_vs_E005.json` (champion and falsification: E005 is the better of H004/H005);
  - `research/comparisons/E006_vs_E010.json` (ablation H008);
  - `research/comparisons/E006_vs_E005_tail_mechanism.json` (standing rule 1).

## Results

**E006** (H006): status COMPLETE, 675.7 s, peak 3.744 GB, within class True (CLASS-M).

| Fold | RMSE | MAE | Bias |
|---|---|---|---|
| R1 | 375.28 | 168.7 | +4.9 |
| R2 | 277.79 | 161.8 | -1.8 |
| R3 | 306.24 | 156.1 | -6.9 |
| S1 | 524.53 | 190.9 | +4.1 |
| W1 | 405.50 | 165.0 | -16.8 |
| S1c | 543.51 | 193.5 | +3.9 |
| W1c | 418.15 | 169.6 | -20.1 |
| **dev mean** (R1–R3, S1, W1) | **377.87** | | |

RMSE by airport (all rows / bulk y < 3,600 s):

| Airport | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| EDDF | 192 / 190 | 181 / 177 | 200 / 191 | 223 / 211 | 175 / 175 | 225 / 212 | 178 / 178 |
| EDDM | 198 / 171 | 174 / 171 | 180 / 176 | 205 / 185 | 176 / 173 | 205 / 186 | 174 / 169 |
| EGLL | 278 / 260 | 255 / 232 | 230 / 225 | 348 / 279 | 228 / 216 | 353 / 286 | 237 / 229 |
| EHAM | 188 / 184 | 182 / 181 | 185 / 183 | 201 / 187 | 198 / 198 | 205 / 191 | 194 / 194 |
| LEBL | 261 / 261 | 227 / 227 | 182 / 182 | 288 / 288 | 164 / 164 | 292 / 292 | 170 / 170 |
| LEMD | 197 / 197 | 207 / 207 | 189 / 189 | 221 / 221 | 165 / 165 | 221 / 221 | 173 / 173 |
| LFPG | 282 / 260 | 279 / 249 | 336 / 298 | 304 / 267 | 240 / 228 | 317 / 277 | 291 / 277 |
| LIRF | 1068 / 624 | 620 / 455 | 819 / 323 | 1611 / 907 | 1047 / 329 | 1681 / 954 | 1103 / 389 |
| LSZH | 191 / 188 | 196 / 194 | 196 / 195 | 259 / 240 | 292 / 232 | 243 / 222 | 265 / 197 |
| LTFM | 256 / 254 | 284 / 269 | 236 / 233 | 326 / 309 | 617 / 346 | 333 / 316 | 608 / 394 |

RMSE by taxi band (true target):

| Band | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| <300 | 323 | 337 | 312 | 446 | 288 | 381 | 307 |
| 300-600 | 212 | 198 | 201 | 238 | 182 | 242 | 217 |
| 600-900 | 192 | 177 | 169 | 283 | 182 | 322 | 197 |
| 900-1200 | 303 | 223 | 181 | 344 | 179 | 322 | 199 |
| 1200-1800 | 291 | 256 | 246 | 351 | 245 | 379 | 266 |
| 1800-3600 | 657 | 674 | 596 | 779 | 633 | 787 | 682 |
| >=3600 | 6212 | 3278 | 5637 | 6696 | 4572 | 6950 | 4570 |

Runtime note: E006 shared the CPU with E009 (ridge reproduction) and several comparisons during R3 (R3 took 236 s against 60–96 s for the other folds). Total 676 s, which is within CLASS-M.

## Against the champion E005 (H004 ridge), which is also the falsification test

| Fold | dRMSE (s) | q10…q90 | Outcome | Bulk dRMSE | Top-1 / top-10 share |
|---|---|---|---|---|---|
| R1 | −102.53 | −139.32…−64.30 | WIN | **+5.18** | 0.20 / 0.73 |
| R2 | −45.73 | −57.84…−34.24 | WIN | −19.94 | −0.13 / 0.08 |
| R3 | −125.37 | −164.94…−75.60 | WIN | −35.49 | 0.30 / 0.74 |
| S1 | −145.48 | −203.65…−83.40 | WIN | **+46.25** | 0.14 / 0.83 |
| W1 | −105.17 | −144.46…−58.11 | WIN | −33.18 | **0.52** / 0.66 |
| S1c | −127.48 | −174.68…−73.71 | WIN | | 0.15 / 0.76 |
| W1c | −91.75 | −127.91…−44.60 | WIN | | **0.57** / 0.69 |

- **Criteria 1–3:** pass (mean −104.86 s, q95 −78.86; 5/5 WIN; no airport degraded). **Falsification:** not met.
- **Ablation against H008:** passes criteria 1–3 (mean −124.47 s, all WIN). The deltas are used.
- **Tail attribution (standing rule 1):** the tail's share of the SSE change is **0.991**. The pre-registered expectation was < 0.5, so the prediction failed. In the bulk, H006 is **worse** than ridge on S1 (+46 s) and R1 (+5 s).
- **Row concentration (B4):** 10 rows carry 66–83 % of the change on R1, R3, S1, W1, S1c and W1c. On W1 and W1c a single row carries more than half:

  | MVT_ID | Airport | Anchor | Target | H006 | Ridge |
  |---|---|---|---|---|---|
  | 183903219 | LIRF | none (no NM data) | 131,167 s | 33,406 s | 1,798 s |

### Does the gain run through the pre-registered tail mechanism?

The pre-registered mechanism is that the anchor `MVT − AOBT_3` reflects part of long taxi-outs. The table splits H006's SSE change against ridge by row type (`scripts/tail_mechanism.py`):

| Fold | Bulk | Tail, anchor present | Tail, **no NM data** | H006 closer to the anchor than ridge (tail rows with anchor) |
|---|---|---|---|---|
| R1 | −0.03 | 0.06 | **0.97** | 20 % |
| R2 | 0.37 | 0.24 | 0.40 | 25 % |
| R3 | 0.19 | 0.04 | **0.77** | 41 % |
| S1 | −0.17 | 0.14 | **1.04** | 20 % |
| W1 | 0.17 | 0.08 | **0.75** | 45 % |

**The gain does not run through the pre-registered mechanism.** It comes mostly from long-taxi rows **without NM data**, and on anchor rows H006 is usually not closer to the anchor than ridge. The target-free-of-December context (training months Jan–Nov) explains why: NM-unmatched DEP rows have a tail rate (y ≥ 3,600 s) of **4.9 %**, against 0.15 % for matched rows. At **LIRF** the rate is **49.1 %** (1,400 rows, mean 6,457 s). LightGBM learned "LIRF and no NM data ⇒ very long taxi". That pattern is real and consistent across folds (every fold WINs), but it was not pre-registered.

## Decision

**INCONCLUSIVE, not promoted.**
- Criteria 1–3 pass, the falsification is not met, and the ablation passes.
- **Criterion 4 fails** under standing rule 1: most of the criterion-1 margin comes from rows with y ≥ 3,600 s, and the pre-registered tail mechanism (the anchor) does not account for it.
- The mechanism that does, NM-unmatched movements with a heavy tail concentrated at LIRF, is recorded as a **candidate hypothesis for Day 2**, to be pre-registered on its own terms.
- The champion remains E005. Criterion 7: CLASS-M, 676 s, 3.74 GB.
