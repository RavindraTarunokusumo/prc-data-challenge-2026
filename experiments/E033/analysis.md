# E033 analysis: H023 v3 primary (equal-weight blend of E029 and E031): a promotion candidate that meets criteria 1–8

**Outcome: neither falsification clause is met; promotion criteria 1–8 hold against E019 (laptop instance E026) under the pre-registered path; the reproduction E034 passes criterion 6.** Under project practice (Day 3: H015 v2), the champion change is recorded at the Day 5 phase close, with the phase's holdout access. **Recommendation: PROMOTE at the phase close.**

## Run

| Item | Value |
|---|---|
| Allocation | `gate.py allocate H023 v3`, committed `763c64a` (D05-S05; clean; freeze anchor `803ceeb` holds outside the record directories) |
| Gating (status only) | H021 (E031) COMPLETE with integrity passed; H021r (E032) run with integrity passed; chain not stopped |
| Config | `blend`, components [E029, E031], weights [0.5, 0.5], FS0 (ids only), seed 42, all 8 folds, CLASS-S |
| Status | COMPLETE: 8.3 s, 3.38 GB (within CLASS-S) |
| Development mean | **438.87 s**: R1 439.89, R2 264.88, R3 393.04, S1 627.92, W1 468.63; S1c 631.99, W1c 481.77 |

## Integrity and clauses (H023 v3)

- **`route_check.py E033 - E029`: passes** (all 8 folds).
- **Clause 1** (`mechanism_check.py E033 E029 NM_present_excl_LIRF`): **mean −3.96 s, q95 −3.52.** Folds: R1 −3.90, R2 −4.47, R3 −4.03, S1 −5.81, W1 −1.59, S1c −7.29, W1c −8.29, all WIN. **Not met: the CatBoost half carries signal the LightGBM lacks on normal taxis.**
  - Attribution is to this CatBoost configuration as a whole (claim scope, v2).
  - Noise condition: |m| / 2 = 0.34 s ≤ 0.5, so not INCONCLUSIVE. The pair is matched (E031 against E030), so not INCONCLUSIVE on that ground either.
  - Reported on H023r (E034): −3.70 s, q95 −3.19. The two readings agree.
- **Clause 2** (`compare.py E033 E029`): **mean −3.58 s**, q95 −3.07, all 7 folds WIN. **Not met.**
- **Residual correlation** of E029 and E031 (reported; `research/comparisons/residual_corr_E029_E031.json`): 0.945–0.985 on all rows, and 0.84–0.92 on bulk rows (y < 3,600 s). The decorrelation sits in the bulk, as the mechanism stated.

## Promotion against E019 (laptop instance E026; rule L v2)

`compare.py E033 E026`: **mean dRMSE −5.62 s (q95 −4.79).**

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| dRMSE (s) | −6.51 | −9.61 | −4.21 | **−4.17** | −3.59 | −6.39 | −6.82 |
| q10, q90 | −8.54, −4.98 | −11.80, −7.52 | −6.26, −3.16 | −5.35, −3.29 | −6.39, −1.98 | −8.04, −5.19 | −12.08, −3.97 |
| Outcome | WIN | WIN | WIN | **WIN** | WIN | WIN | WIN |

| Criterion | Result |
|---|---|
| 1. Mean improves (≤ −1.0, q95 < 0) | **pass** (−5.62; −4.79) |
| 2. ≥ 3 WINs incl. S1, no LOSS; twin rule | **pass**: 5/5 counted WINs; S1c and W1c WIN |
| 3. No airport > +3 % | **pass**: every airport improves (worst ratio 0.9974, LIRF) |
| 4. Mechanism (B2) | **pass**: clauses 1–2 not met, not INCONCLUSIVE. **H018 v2 clauses 1–2 not met**: > 3 h band 3 (limit 50); `NM_missing_other` bulk against E026 −317.3 / −296.3 / −181.4 / −165.9 s on R1, R2, R3, W1 |
| 5. No leakage | **pass** (as pre-registered: no new input; fixed weight; components fold-local) |
| 6. Reproduction | **pass**: E034 (blend of [E029, E032], seed 43) is within 0.48 s on every development fold, and criteria 1–3 hold against E026 (7/7 WIN) |
| 7. Within class | **pass**: E033 CLASS-S; E029 CLASS-M (893 s, 6.60 GB); E031 CLASS-L (1,523 s, 7.01 GB; also inside CLASS-M's figures); E032 CLASS-L (1,131 s, 7.08 GB). No swap in E030–E034 |
| 8. Advisor objections | **pass**: criterion 8 statistic against E028 ≤ +0.06 s (bound +6,500). **B3** (S1 WIN with S1c point ≥ 0): S1c −6.39, no objection |

- **Rule L v2 item 4 flags:** none fire. No deciding quantile is within 0.02 s of 0 (the nearest is W1's q90, −1.98). Criterion 1's point and q95 are far from their thresholds. Criterion 3's ratios are far from 1.03, and criterion 8 is far from its bound.
- **Rule 1 S1 recording:** `NM_present_LIRF`'s share of the S1 SSE change is 0.24 (< 0.5). **The S1 WIN is not recorded as carried by the convention mixture.**
- **Rule 6:** S1 top-1 share 0.14 (top-10 0.23); W1 top-1 0.29 (top-10 0.49). No row carries ≥ 50 %.
- **Rule 12** (`NM_missing_other` bulk, 5 development folds): < 1 h 82, 1–3 h 4, > 3 h 3 (E019: 83, 22, 81). **D3-C2 is treated in the candidate.**

## Missing Control 1 (pre-registered single-row exposure): MISSED

| Row | y | E026 | E029 | E031 | **E033** | Pre-registered |
|---|---|---|---|---|---|---|
| 192622644 (S1) | 87,002 | 8,136 | 7,041 | 10,976 | **9,008** | below E026's 8,136, central about 5,500 s: **wrong direction** |
| 183910286 (W1) | 13,865 | 1,979 | 7,938 | 22,233 | **15,086** | between 1,979 and 7,938: **outside (above both)** |

- The pre-registration assumed CatBoost would bound day-scale predictions below the LightGBM's (the H020 review's reasoning). It predicted higher on both rows. The S1 cell expectation (`NM_present_LIRF` full +8 to +28 s) was therefore wrong in sign: the cell moved −6.45 s on R1 and is small on S1 (share 0.24).
- These misses are recorded and change no reading.

## Other expectations against outcomes

| Expectation (H023 v3) | Outcome |
|---|---|
| Clause 1: −1.5 to −6 s, central −3; ≥ 3 WINs | −3.96, 7/7: inside |
| Clause 2: −1 to −5 s, central −2.5 | −3.58: inside |
| Residual correlation 0.93–0.98 (all rows) | 0.945–0.985: S1 0.985 just above |
| Against E026: −3 to −7 s, central −4.5; S1 TIE most likely | −5.62: inside; **S1 WIN** (TIE was the expectation) |
| Development mean 437–442 | 438.87: inside |
| > 3 h band ≤ 10 | 3: inside |
| Criterion 8 against E028 small, non-zero | ≤ +0.06: inside |
| Promotion P 0.20 (Advisor 0.04) | criteria 1–8 met |
