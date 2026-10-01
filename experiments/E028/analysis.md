# E028 analysis: H004 v1 reproduction (laptop instance of E005)

**PASS** (`reproduce_check.py E028 E005`: every development fold within 0.012 s; max |Δ| 0.011 s on W1). 72.7 s, 3.50 GB, CLASS-S.

- **Not byte-identical:** all 8 prediction files differ from E005's hashes, as for E026 (LightGBM). The ridge's linear algebra (numpy/BLAS) also gives different low-order bits on the AMD laptop than on the Intel cloud host.
- **Purpose:** E005's prediction files are not on the laptop. `route_check.py` (routed rows against E005) and the criterion 8 statistic (`NM_missing_LIRF` bulk against E005) need them. E028 is proposed as E005's laptop instance (ruling requested in the first Day 5 exchange).
