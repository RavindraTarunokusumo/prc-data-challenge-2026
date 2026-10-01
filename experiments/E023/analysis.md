# E023 analysis: H018 v2 primary (routed LightGBM on FS2, LIRF NM-missing rows excluded from training)

**Outcome: "D3-C2 treated, not promoted."** Neither falsification clause is met, so the mechanism holds. Promotion fails frozen criterion 2 against E019 (S1 TIE). No reproduction is due (authorization item 4), and E019 remains the champion in force for H019 v2 (item 7).

## Run

| Item | Value |
|---|---|
| Configuration | E019's, with `hypothesis_id: H018` and `params.route_train_exclude: true` (authorization item 2) |
| Allocation | `gate.py allocate H018 v2` at `da47b81` in D04-S01, clean tree; config written and run in D04-S02 |
| Status | COMPLETE: 925.0 s, peak RSS 5.29 GB (CLASS-M: within class) |
| Development mean | **442.46 s** (E019 444.49). R1 443.39, R2 269.69, R3 395.95, S1 632.30, W1 470.94; S1c 637.23, W1c 486.95 |

**Recording (item 8(a)).**
- **CPU:** Intel(R) Xeon(R) Processor @ 2.80GHz.
- **Container restarts since E022:** yes, several. One also fell between E023's allocation (D04-S01, boot `dd719b28-…`) and its run (D04-S02, boot `f948bf23-…`).
- **INC-0004** open: the process runs `--model claude-opus-5-5 --effort medium`.
- **Launched by** the main session (`claude-opus-5-5`), not delegated (INC-0005).

## Clause 3: integrity (not met)

`route_check.py E023 - E005`: the routed rows equal E005 on all 8 folds (max |Δ| ≤ 1e-6). The routing, with training exclusion, implements E005's model class on the routed subgroup.

## Clause 1: the > 3 h band (not met)

`range_check.py E023 E019 E021 E017 --by-dsched --bands` (`research/comparisons/range_check_E023.json`). These are `NM_missing_other` bulk rows, summed over the 5 development folds; a row counts if its prediction is below 0 s or above 3,600 s.

| Model | < 1 h | 1–3 h | **> 3 h** | Total |
|---|---|---|---|---|
| **E023 (H018 v2)** | 82 | 12 | **5** | 99 |
| E019 (champion) | 83 | 22 | 81 | 186 |
| E021 (no-T reference) | 83 | 17 | 18 | 118 |
| E017 (FS1) | 60 | 18 | 14 | 92 |

- **> 3 h: 5, below the pre-registered limit of 50. Clause 1 is not met.** The increment is removed, consistent with D3-C2.
- **Fraction of the > 3 h increment removed** (item 8(b)): (81 − 5) / 63 = **1.21**. E023 is below even the no-T reference (18), so it removes more than the T-window increment.
- **Pooled > 5 h share, all rows** (item 8(b)): **1/93** (E019: 41/93).
- **Disclosures** (pre-registered readings):
  - **The total, 99, is inside the no-T range (92–125)**, as expected.
  - **< 1 h is 82.** It is neither below 60 (which would be an observation consistent with the stronger claim) nor above 83 (a perturbation). The < 1 h band is unchanged against E019 (83): the exclusion does not act there, consistent with the proposal's "not claimed".

## Clause 2: accuracy on the treated subgroup (not met)

`compare.py E023 E019`, `NM_missing_other.delta_rmse_bulk`, on the four folds where E019 lost to E017:

| Fold | R1 | R2 | R3 | W1 |
|---|---|---|---|---|
| Bulk dRMSE | **−197.85** | **−230.47** | **−105.67** | **−104.99** |

All four are negative, so **clause 2 is not met.** The treated subgroup improves on every fold, including the others (S1 −34.99, S1c −80.74, W1c −133.27).

**Twin cells** (item 8(c)), `NM_missing_other` full and bulk:
- S1 −28.40 / −34.99; S1c −60.35 / −80.74.
- W1 −8.91 / −104.99; W1c +106.33 / −133.27. The full value on W1c is carried by tail rows (share of SSE change −2.64 from the tail, January-only twin).

## Promotion against E019: fails criterion 2

`compare.py E023 E019`: **mean dRMSE −2.04 s** (q95 −1.31).

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| dRMSE | −3.00 | −4.80 | −1.30 | +0.20 | −1.28 | −1.15 | −1.64 |
| Outcome | WIN | WIN | WIN | **TIE** | WIN | WIN | TIE |

- **Criterion 1 passes. Criterion 2 FAILS: S1 is TIE** (S1 must WIN). Criterion 3 passes. `passes_criteria_1_to_3: false`.
- **S1 attribution** (item 8(d); rule 1): S1 is not a WIN, so no margin is attributed. The cell carrying S1's change is **`NM_present_LIRF`** (share of the SSE change +3.84; tail +3.52). The dominant row is **192622644** (LIRF, NM-present, y 87,002 s; E023 7,041 s against E019 8,136 s). `NM_missing_other` moved the other way (−2.58).
- **Rule 6:** dominant rows on S1 (192622644, on a near-zero net change) and on W1 (183910286, LIRF NM-present; top-1 0.61). Both are expected under the rule 6 reading for folds with small net change.
- **Tail share** of the SSE change: 0.058.

## Rule 8: `NM_present_LIRF` against E019 (pre-registered)

| Fold | R1 | R2 | R3 | S1 | W1 |
|---|---|---|---|---|---|
| Full (expected −10 to +15; S1 −5 to +15) | +0.09 | −8.16 | −1.87 | **+7.76** | **−14.93** |
| Bulk (expected ±5) | +0.33 | −0.11 | −1.65 | +1.46 | +0.80 |

- S1 is inside its range (+7.76 against +4 central).
- W1's full value (−14.93) is **below** the expected range (more favourable than expected).
- Every bulk value is inside ±5.

## Perturbation scale: `mechanism_check.py E023 E019 NM_present_excl_LIRF`

- Mean −0.03 s. Every development fold is within ±0.56 s: R2 +0.37 LOSS, the others TIE.
- W1c is −7.75 (WIN).
- Dominant rows appear on R1 and R3, on near-zero net change, as expected.
- The exclusion barely moves the bulk of the model outside the treated rows.

## Against the champion E005 (reported)

`compare.py E023 E005`: **−40.27 s** (q95 −36.96), WIN on 7/7, criteria 1–3 pass. E019 against E005 was −38.23 s.

## Reading

1. **D3-C2's attribution is supported.** Removing the LIRF NM-missing rows from training removes the > 3 h out-of-range increment completely (81 → 5) and improves the treated subgroup by 105–230 s in bulk on every fold where E019 lost.
2. **It is not promotable as a candidate,** because the frozen criteria need an S1 WIN against the champion. S1's change is carried by one LIRF NM-present row (192622644) through the convention mixture, and the treatment does not touch that.
3. **Next:** H019 v2 runs against **E019** as the champion in force (item 7: H018 was not "promoted first in this chain").
