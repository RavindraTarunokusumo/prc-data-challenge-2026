# E026 analysis: H015 v2 reproduction on the owner's laptop (Day 5 compute check)

**PASS under the frozen reproduction rule** (`reproduce_check.py E026 E019`: every development fold within 1.0 s). **No prediction file is byte-identical to E019's.**

| Item | Value |
|---|---|
| Allocation | `gate.py allocate H015 v2 --purpose reproduction` (replaces E025, RESOURCE_FAILURE, INC-0008), committed `3b38a90` |
| Config | identical to E022 (E019's configuration, seed 43, `num_threads: 4`, 8 folds) |
| Host | owner laptop: AMD Ryzen 7 260 (16 threads), WSL2 11 GB, swap 0. The cloud runs were Intel Xeon. Nothing else ran during the experiment (experiment lock held) |
| Status | COMPLETE: **668.7 s, peak RSS 5.22 GB** (CLASS-M, within class). E019 took 954 s / 4.76 GB, E022 1,339 s / 4.63 GB |

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| E026 | 446.40 | 274.49 | 397.25 | 632.09 | 472.22 | 638.38 | 488.59 |
| E026 − E019 (s) | +0.0001 | −0.0004 | −0.0035 | −0.0072 | +0.0007 | n/a | n/a |

- **Byte identity:** E022 was byte-identical to E019 on the cloud, across two Intel CPU model strings. On this AMD laptop, **all 8 prediction files differ** from E019's manifest hashes (including H, which is not scored here). The largest development-fold difference is 0.007 s. The likely cause is CPU-architecture-dependent floating-point paths in the same LightGBM build (unverified; E019's files are not on the laptop, so no row-level comparison is possible).
- **Consequence for Day 5 comparisons.** `prc.evaluate` loads stored predictions and checks them against the experiment's manifest. **E019's, E005's and E023's prediction files are not on the laptop** (git-ignored, cloud only), so `compare.py`, `mechanism_check.py` and `holdout_check.py` cannot run against them. E026's files cannot stand in under E019's name. A Day 5 comparison against the champion therefore needs an Advisor ruling, either on E026 as the laptop instance of E019, or on another route. The request goes into the first Day 5 exchange. `reproduce_check.py --champion E005` was not run for the same reason (E005's files are absent).
- **Laptop timing:** about 80–90 s per full fold on 4 threads, 30 % faster than the cloud.
