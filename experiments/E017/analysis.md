# E017 — H013 v2 (LightGBM on FS1, no random component), primary · COMPLETE

**Run.** 668.0 s (faster than E012's 906 s), peak 4.183 GB, CLASS-M, `within_class: true`.
- The config is exactly the authorized one: E012's with `bagging_fraction` 1.0, `bagging_freq` 0, `feature_fraction` 1.0 and `bin_construct_sample_cnt` 5,000,000.
- The preconditions (a)–(e) of `H013_review_v2.md` were verified before allocation. The clause code, `gbm.py` and `features.py` were unchanged since `5ba9230`, `uv.lock` was `39df945c`, the tree was clean, and nothing ran concurrently.

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| E017 | 364.65 | 258.37 | 310.59 | 548.94 | 411.57 | 545.07 | 435.91 | **378.82** |
| E012 | 362.74 | 262.64 | 311.89 | 538.09 | 405.37 | 545.52 | 444.21 | 376.15 |

The development mean is inside the predicted 368–388 s.

## Chain step 1

### Clause 1 — promotion against E005 (`E017_vs_E005.json`): not met (passes)

- Mean **−103.90 s** (q95 −80.35), **7/7 WIN**, criterion 3 passes with no airport degraded (predicted −95 to −120 s, 7/7).
- Tail share 0.968 (predicted > 0.9).
- NM-present bulk dRMSE against E005: −42.4 to −50.1 s on the development folds.

### Criterion 8 (the LIRF bulk trade): NOT RESOLVED, so H013 is not promotable

`NM_missing_LIRF.delta_rmse_bulk` against E005:

| R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|
| +5,456.4 | +1,863.1 | +2,036.7 | **+7,104.4** | +2,555.8 | +5,520.3 | +1,225.3 |

- **S1 exceeds the registered bound of +6,500 s** (H009 v3's rule, applied unchanged per `H013_ack_v2.md`). Whatever clauses 2–4 show, **the criterion 8 objection is not resolved and H013 v2 cannot be promoted.**
- The Advisor predicted this as the main live risk (P ≈ 0.45 of staying under). It also realises **Alternative Explanation 1**: without bagging, predictions on LIRF convention rows are more extreme. On S1 the LIRF NM-missing bulk dRMSE against E012 is +714 s.
- The v1 widening to +7,000 s, withdrawn in v2, would not have covered S1 either.
- **Rule 8 tail share** (band 0.3–1.1): 0.90, **0.28**, 0.71, **1.17** and 0.64. R2 is below the band, as anticipated in the proposal, and S1 is above it.

### Configuration effect against E012 (`E017_vs_E012*.json`): the inputs to the admissibility rule and objection T

**All rows.** Mean +2.67 s (q95 +6.95). R1 TIE, R2 WIN (−4.3), R3 TIE, **S1 LOSS (+10.9)**, **W1 LOSS (+6.2)**, S1c TIE, W1c TIE.

**NM-present rows.** Mean **−0.75 s** (q95 −0.29).

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| Full dRMSE (s) | −2.11 | +0.46 | +0.04 | −1.39 | −0.75 | −1.68 | +2.38 |

- **On 98–99 % of rows, the deterministic configuration is practically equivalent to the bagged one.**

**LIRF NM-missing rows** (full dRMSE):

| R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|
| +134.8 | −453.5 | −117.1 | +356.2 | +392.9 | +28.4 | −700.2 |

- All the material difference is here: a different draw of the convention mixture.

**Objection T.** |S1c| = 1.68 < 21.153 and |W1c| = 2.38 < 47.966, so it **does not stand**. The twins are covered.

**Admissibility for clause 4** (`NM_present`, threshold ½ |E012 − E014|). |Δ| is 2.11, 0.46, 0.04, 1.39 and 0.75 against 16.585, 18.318, 29.549, 21.926 and 41.882. **All five development folds are admissible.**

**Admissibility for clause 3** (`LIRF_NM_missing`, threshold ½ |E012 − E013|):

| Fold | \|Δ\| (s) | Threshold (s) | Admissible |
|---|---|---|---|
| R1 | 134.78 | 544.320 | yes |
| **R2** | **453.45** | **157.101** | **no** |
| R3 | 117.05 | 1,246.470 | yes |
| S1 | 356.18 | 988.123 | yes |
| W1 | 392.85 | 1,237.579 | yes |

R2 is inadmissible, as the review predicted, and counts as a failing fold under the conservative rule. Clause 3 is computed after step 3.

## Status

- **Not promotable** (criterion 8 unresolved). The reproduction is therefore **not run**: it is conditional on criterion 8 being resolved.
- Clauses 2–4 are computed as registered, with H014 v2 next, for the record and for the Day 3–4 training-procedure question.

## Chain steps 2–3 (after E018)

| Clause | Source | Result | Verdict |
|---|---|---|---|
| **2(a)** | `mechanism_check.py E017 E018 NM_present_excl_LIRF` | −7.27 s (q95 −6.49), criteria 1–2 True, 4 counted WINs (W1c LOSS voids W1) | **not met** |
| **2(b)** | `… E017 E018 NM_present` | Bulk < 0 on all five development folds (−9.0 to −16.4 s) | **not met** |
| **3** | `… E017 E013 LIRF_NM_missing` | Full dRMSE −953.9, −767.7, −2,610.0, −1,620.1 and −2,082.3 s: none ≥ 0. R2 is inadmissible and counts as failing, so 1 failing fold < 3 | **not met**; M3 re-established on four admissible folds |
| **4** | `… E017 E014 NM_present` | −52.05 s (q95 −48.24), 7/7 WIN; all development folds admissible | **not met**; M2 re-established |

**Objection T** does not stand (S1c 1.68 s, W1c 2.38 s).

**Disclosure comparisons** (`compare.py`): E017 against E013, −36.21 s; against E014, −34.58 s; against E018, −2.13 s.

## Decision: H013 v2 **INCONCLUSIVE** (not promoted; E005 remains champion)

- Clauses 1–4 are not met and objection T does not stand, so H013 v2 is **not falsified**. Criteria 1–3 pass against E005.
- **Criterion 8 is not resolved:** `NM_missing_LIRF.delta_rmse_bulk` on S1 is +7,104.4 s, above +6,500 s. That alone blocks promotion.
- **The reproduction is not run.** It is conditional on criterion 8.
- **Mechanism replication across training procedures** (bagged → deterministic): M1 −7.16 → −7.27 s; M2 −51.30 → −52.05 s. M3 holds on every admissible fold.
