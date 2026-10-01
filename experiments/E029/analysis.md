# E029 analysis: H018 v2 reproduction (laptop instance of E023)

**PASS** (`reproduce_check.py E029 E023`: every development fold within 0.0072 s; R1 +0.0001, R2 −0.0004, R3 −0.0036, S1 −0.0072, W1 +0.0007). 893.1 s, **peak RSS 6.60 GB** (E023: 5.29 GB; E027 with curves: 5.19 GB; cause not established), CLASS-M within class. Learning curves recorded.

- **Not byte-identical** to E023 (0 of 8 files), as for E026, E027 and E028. The per-fold differences are almost exactly E026's against E019, which fits a common CPU-architecture effect on the shared LightGBM path.
- **Single rows on the laptop** (instances): row 192622644 (S1, y 87,002 s): E027 8,136 s, E029 7,041 s (cloud: 8,136 and 7,041). Row 183910286 (W1, LIRF, y 13,865 s): E027 1,979 s, E029 7,938 s.
- **Purpose:** E023's prediction files are not on the laptop. E029 is proposed as E023's laptop instance and as H023's LightGBM component (`research/day-05/proposals/LAPTOP_REFS_v1.md`).
