# E021 analysis: H017 v2 primary (LightGBM on FS2_P; P/T decomposition of C)

**Role:** a decomposition reference. It is not a candidate, not reproduced, and never NEW (H017 v2, ACCEPT X-D03-S01-0002).

## Run

| Item | Value |
|---|---|
| Configuration | `lightgbm` on FS2_P (FS1 + the 10 P congestion features of `63923e2`), E017's parameters, seed 42 |
| Status | COMPLETE: 1,071.3 s, peak RSS 4.86 GB (CLASS-M: within class) |
| Development mean | **372.14 s** (pre-registered 370–385). R1 353.80, R2 257.44, R3 302.73, S1 543.00, W1 403.73; S1c 547.48, W1c 431.03 |

**Provenance (item 8).**
- **CPU:** Intel(R) Xeon(R) Processor @ 2.10GHz.
- **Container restart since E020: no** (same kernel boot id).
- **INC-0004** open.
- **Clause 3 dependency** (ack): H015 v2's clause 3(b) was **not met**, since E019 and E020 were bit-identical outside the routed rows across containers. Reading 1 therefore carries no cross-process caveat.

## Pre-registered readings (all on `NM_present_excl_LIRF`)

| Reading | Contrast | Mean dRMSE (q95) | Criteria 1–2 | Folds | Floor −6.0 s | Result |
|---|---|---|---|---|---|---|
| **1. T carries C** (T on top of P) | E020 − E021 | **−3.28** (−2.82) | pass | 7/7 WIN | not reached | **Not supported** |
| **2. P beyond E017** | E021 − E017 | **−3.47** (−2.93) | pass | 7/7 WIN | not reached | **"P effect not distinguishable from training noise"** (pre-registered wording) |
| **3. Rule 11, all rows** | E021 − E017 | **−6.68** (q95 −1.26) | criterion 1 pass, **criterion 2 fail** (3 WIN, 4 TIE), criterion 3 pass | — | — | Reported |

**Per fold:**

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| Reading 2: P (E021 − E017) | −3.04 | −3.11 | −3.28 | −2.01 | −5.91 | −3.04 | −2.80 |
| Reading 1: T given P (E020 − E021) | −2.84 | −3.56 | −3.03 | −3.34 | −3.61 | −2.68 | −4.86 |
| Sum = C (E020 − E017) | −5.88 | −6.67 | −6.31 | −5.35 | −9.52 | −5.72 | −7.66 |

- **The decomposition adds exactly per fold,** as the review noted (the same rows). The sums match E019/E020 − E017 on this population to 0.01 s.
- **Rule 6 on reading 1.** No dominant row: |top-1| ≤ 0.15 on every fold, and there are no "not decisive" folds, as pre-registered. The top-10 shares are 0.32–0.46 on R2, R3, S1, S1c and W1c. That is concentrated, but below 0.5.
- **Rule 6 on reading 2.** |top-1| ≤ 0.05 on every fold.

**Against the forecasts.**

| | Proposal | Outcome |
|---|---|---|
| P (reading 2) | −1 to −4 s | −3.47 s: inside |
| T given P (reading 1) | −4 to −12 s; WIN on ≥ 3 of 5 dev folds | −3.28 s: **below the range**; 5 of 5 WIN |
| Development mean | 370–385 s | 372.14 s: inside |

## What this says (bounded as the review required)

1. **Neither half reaches the floor on its own.** Both are very consistent: every fold is a WIN, and each fold's q90 is below 0. But each is about half of C.
   - The −6.0 s floor was set at about three times the largest development-fold perturbation on this population (1.96 s).
   - Each half is about 1.7 times that perturbation.
2. **The split is ordered** ("P without T", then "T given P"). There is no T-only arm, so P may be credited with information that T also carries. The data do not say that P matters more than T, only that, in this order, the two parts are about equal.
3. **The EDA expectation that T dominates is not borne out beyond the anchor.**
   - The univariate after-anchor EDA showed the T counts at 10–12 s, against P features at 0.3–1.7 s.
   - In the model, with `d_aobt3` present, the T part adds about 3.3 s, and the P part about 3.5 s.
   - This is consistent with the v1 review's point (g): the after-anchor EDA partly re-measured the anchor.
4. **For Days 5–7.** About half of the congestion block's gain on the clause population, **−3.47 s, is available at the off-block proxy (P)**. This is an estimate of the congestion component only: FS1's own T inputs (`d_*` and the rest) are present in both arms. It is not the causal-only model.

## Rule 11: all rows (reading 3)

- **E021 − E017 is −6.68 s on all rows** (q95 −1.26): 3 WIN (R1, W1, W1c) and 4 TIE. Criterion 2 fails on too few WINs, not on losses.
- Tail share of the SSE change is 0.165. Dominant or near-dominant rows appear on TIE folds with small net change (R2 −0.93, R3 +0.96, S1 −1.05, S1c +0.88).
- No airport is degraded.
- The all-rows figure is about twice the clause-population figure, because the P features also move the LIRF NM-missing rows (not routed in H017).

## Next

The chain has three primaries done. **The reproduction of H015 v2 is due:** clauses 1–4 are all not met (Validation Plan step 4). One `reproduction` allocation of H015 v2 with seed 43, everything else identical; then `reproduce_check.py <repro> E019 --champion E005` and the prediction-file SHA-256 comparison on all 8 folds.
