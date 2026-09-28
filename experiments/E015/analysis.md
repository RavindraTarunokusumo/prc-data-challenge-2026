# E015 — H009 v3 reproduction (seed 43) · COMPLETE → criterion 6 FAILS

**Run.** 868.2 s, peak 4.195 GB, CLASS-M, `within_class: true`. The config is identical to E012 except `purpose: reproduction` and `seed: 43` (the frozen reproduction seed).
- **Allocation order.** E015 was allocated before E016 (H011), a researcher slip recorded in the journal.
- **Run order.** It ran after E016, as the registered chain requires (step 4 before step 5).

## Frozen reproduction rule (`research/comparisons/repro_E015_of_E012.json`)

| Fold | E012 (seed 42) | E015 (seed 43) | \|Δ\| | Within 1.0 s |
|---|---|---|---|---|
| R1 | 362.74 | 362.39 | 0.35 | yes |
| R2 | 262.64 | 263.55 | 0.91 | yes |
| R3 | 311.89 | 313.62 | **1.73** | **no** |
| S1 | 538.09 | 541.59 | **3.50** | **no** |
| W1 | 405.37 | 405.30 | 0.07 | yes |

- `within_tolerance: false`.
- `criteria_hold: true`: E015 against E005 passes criteria 1–3, 7/7 WIN.
- **`passes: false`, so criterion 6 fails.**

## Where the seed variance lives (attribution only; `E015_vs_E012_mech_*.json`)

| Population | R3 \|Δ\| | S1 \|Δ\| |
|---|---|---|
| All rows | 1.73 | 3.50 |
| Excluding LIRF NM-missing (~99.8 % of rows) | 0.23 | 1.33 |
| NM-present rows outside LIRF | 0.21 | 0.91 |
| LIRF NM-missing only (52 and 337 rows) | 124 | 82 |

- **The static-structure and anchor part of the model is seed-stable to within the tolerance** on NM-present rows outside LIRF, on both folds.
- **The failure is carried by the bagged mixture predictions on LIRF convention records.**
  - On R3, row 200300302 (y = 87,598 s, no NM data) is predicted at 16,148 s with seed 42 and 13,746 s with seed 43.
  - On S1, the 337 LIRF NM-missing rows move by +82 s RMSE, and row 192622644 (NM-present, y = 87,002 s) adds the residual 1.33 − 0.91 s.
- With `bagging_fraction` 0.8 and `feature_fraction` 0.9, which rows and features each tree sees depends on the seed. On a handful of day-scale records the L2 mixture prediction swings by thousands of seconds, and at a fold RMSE of ~300–540 s one such swing exceeds the 1.0 s tolerance.

## Consequence

H009 v3 **cannot be promoted**: criterion 6 fails, and the frozen rule gives no discretion. **E005 remains champion.**
- H009 is not falsified: all its clauses 1–4 hold.
- The decision is **INCONCLUSIVE**, the Day 1 category for a candidate that is not falsified but not promotable.
- No re-run with another seed. That would be seed selection, and a re-run is authorized only after an infrastructure failure.

**Implication for every Tier 1 candidate.** Any bagged tree model that uses `d_sched` on LIRF NM-missing rows will face the same criterion 6 exposure. This is a Day 2 finding for the phase-close review, to be addressed by a pre-registered design, not by tuning.
