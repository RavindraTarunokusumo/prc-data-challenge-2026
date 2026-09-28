# E012 — H009 v3 (LightGBM on FS1), primary · COMPLETE

**Run.** 905.9 s, peak 4.142 GB, CLASS-M, `within_class: true`. Allocated from a clean tree (`gate.json`: `git_dirty_at_allocation: false`). `uv_lock_sha256` `39df945cddc4…`, the E006/E010 reuse condition (c). The config is identical to E006 except `feature_set: FS1`.

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| E012 | 362.74 | 262.64 | 311.89 | 538.09 | 405.37 | 545.52 | 444.21 | **376.15** |
| E006 | 375.3 | 277.8 | 306.2 | 524.5 | 405.5 | — | — | 377.87 |

H: predicted only.

## Chain step 1 (pre-registered; `H009_v3.md`)

### Clause 1 — promotion against E005 (`research/comparisons/E012_vs_E005.json`): passes

- Mean dRMSE **−106.58 s** (q95 −84.41). **7/7 WIN**, including S1 (−131.9) and both twins (S1c −125.5, W1c −65.7). Predicted: −110 to −130 s, 7/7.
- **Criterion 3 passes:** no airport is degraded beyond tolerance. Pooled bulk dRMSE is −24 to −69 s at nine airports, and **+198.3 s at LIRF** (the convention trade).
- **Tail share** 0.940 (predicted > 0.9).
- **Rule 7:** NM-present bulk dRMSE is −41.0, −42.1, −47.7, −45.9 and −49.7 s (R1–W1). E006 had −31 to −40 s.
- **Rule 8, LIRF NM-missing:**

  | | R1 | R2 | R3 | S1 | W1 | Predicted |
  |---|---|---|---|---|---|---|
  | Tail share of the SSE change | 0.88 | 0.25 | 0.70 | 1.09 | 0.65 | 0.3–1.1 |
  | Bulk dRMSE (s) | +5,045 | +2,279 | +1,835 | +6,390 | +2,349 | +1,500 to +6,500 |

  - R2's tail share, 0.25, is below the 0.3 bound, a small miss. Every other fold is in range.
  - The S1 bulk loss is the largest (predicted > +4,000), and S1 still has a net gain.
- **Criterion 8 rule, part 2:** `NM_missing_LIRF.delta_rmse_bulk` ≤ +6,500 s on every development fold. It **holds**, but narrowly on S1 (+6,390). Part 1 (clause 3) is pending H010.
- **Rule 6:** top-1 share ≤ 0.49 on every fold. There is no dominant row, including on W1 and W1c, where 183903219 was expected to dominate.

### Clause 2(a) — M1 on `NM_present_excl_LIRF` (`E012_vs_E006_mech_NM_present_excl_LIRF.json`): passes

- Mean dRMSE **−7.16 s** (q95 −6.25); criterion 1 is True (predicted −5 to −20 s).
- **Folds:** R1 −4.71, R2 −6.83, R3 −6.93, S1 −6.96 and W1 −10.35 are all WIN. S1c −5.13 is WIN. **W1c +6.91 is LOSS.**
- Under the frozen twin rule the W1 WIN counts as a TIE. The counted WINs are R1, R2, R3 and S1 (4 ≥ 3), S1 is WIN, and there is no counted loss, so criterion 2 is True.
- Predicted "WIN on ≥ 4 of 5": met on the raw outcomes (5/5) and on the counted outcomes (4/5).
- **Residual exposure 2 materialised as flagged.** W1c (January-only training) is LOSS, which voids the W1 WIN.
- **Rule 6 (pre-registered: no row with |top-1| ≥ 0.5):** the top-1 shares are −0.08 to +0.07 on every fold. As predicted.

### Clause 2(b) — NM-present bulk (`E012_vs_E006_mech_NM_present.json`): passes

- Bulk dRMSE is −8.12, −10.07, −8.35, −14.47 and −9.48 s (R1–W1), all < 0. The clause is not met.
- **The v2 defect, observed.** On `NM_present` rows (full), S1 is a **TIE** (−1.43 s). Row **192622644** carries the change (top-1 share −8.93): E012 predicts 5,912 s for it and E006 16,545 s (y = 87,002).
  - S1c is also TIE. Criterion 2 is False on this population.
  - v2's clause 2(a) (this population) would have falsified H009 through one record, despite a −14.5 s bulk gain on S1. The v3 re-specification is what separates these.

### Rules 1, 6 and 7 for M1, all rows (`compare.py`, `E012_vs_E006.json`): reported

- Mean −1.72 s (q95 +9.39). Folds: R1 −12.5, R2 −15.2, R3 +5.7, S1 +13.6, W1 −0.1, S1c +2.0 and W1c +26.1 (LOSS).
- On all rows, **the static-key effect is swamped by LIRF NM-missing day-scale records.** The dominant rows are 200300302 (R3, y = 87,598), 192626268 (S1 and S1c, y = 88,132) and 183903219 (W1 and W1c, y = 131,167). E012 predicts 3,000–17,000 s lower than E006 on them.
- **Rule 7, NM-present LIRF bulk:** −17.6 to −58.5 s on every fold. Static keys help at LIRF too.

### Alternative Explanation 2 — LIRF NM-missing (`E012_vs_E006_mech_LIRF_NM_missing.json`): reported

- **Bulk:** −469, −1,311, −150 and −413 s (R1, R2, R3, W1), and **+608 s on S1**.
- **Full:** −203, −201, +1,237, +487 and +605 s. The rows are few (52–337 per fold), and one day-scale row decides each fold.
- **Reading.** FS1's static keys move LIRF NM-missing predictions toward normal taxi time. That recovers bulk on most folds and loses on day-scale convention records.
  - This is not the "identifier" direction feared in Alternative Explanation 2, where keys would flag convention rows and push predictions up. It is the reverse: the static prior dilutes the `d_sched` signal.
  - It cannot decide an M1 clause, because these rows are outside 2(a) and are tail rows for 2(b).

## Status

Clauses 1, 2(a) and 2(b) are **not met**. H009 is not falsified so far.
- Clause 3 needs H010, which is next.
- Clause 4 needs H012.
- The criterion 8 rule, part 1, needs clause 3.
- The reproduction is conditional on clauses 1–4.
