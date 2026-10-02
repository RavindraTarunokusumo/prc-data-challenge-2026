# E028 analysis: H004 v1 reproduction (laptop instance of E005)

**PASS** (`reproduce_check.py E028 E005`: every development fold within 0.012 s; max |Δ| 0.011 s on W1). 72.7 s, 3.50 GB, CLASS-S.

- **Not byte-identical:** all 8 prediction files differ from E005's hashes, as for E026 (LightGBM). The ridge's linear algebra (numpy/BLAS) also gives different low-order bits on the AMD laptop than on the Intel cloud host.
- **Purpose:** E005's prediction files are not on the laptop. `route_check.py` (routed rows against E005) and the criterion 8 statistic (`NM_missing_LIRF` bulk against E005) need them. E028 is proposed as E005's laptop instance (ruling requested in the first Day 5 exchange).

## Corrections (appended 2026-10-01T19:35Z; D5-C2 to D5-C5)

- "low-order bits" is wrong. E028 differs from E005 at every airport. W1c: +0.339 s on all rows, LTFM +1.94 s; the development folds are within 0.0113 s.
- E028's routed-row predictions differ from the routed path's ridge (E027, E029) on every routed row, by up to 190.9 s (R3).
- E028 was allocated outside H004 v1's review scope (D5-C5).
