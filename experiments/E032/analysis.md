# E032 analysis: H021 v3 reproduction (seed 43; unconditional)

**COMPLETE; route integrity holds; the noise condition is not met, so H021's clause 1 has its final verdict: NOT MET (mechanism supported).** The frozen 1.0 s reproduction tolerance fails on R1 (+1.056 s). H021 is not a candidate, so the tolerance decides nothing for H021. It bears on H023's criterion 6 through the blend.

## Run

| Item | Value |
|---|---|
| Allocation | `gate.py allocate H021 v3 --purpose reproduction`, committed `636dc8d` (D05-S05; clean; freeze anchor `803ceeb` holds outside the record directories) |
| Config | E031's with `purpose: reproduction` and `seed: 43` (CLASS-L) |
| Status | COMPLETE: **1,130.5 s (18.8 min), peak RSS 7.08 GB**, within CLASS-L. CLASS-M comparison: runtime inside 30 min; RAM inside 8 GB |
| GPU / swap | device peak 3,820 MiB (desktop included); **0 pages swapped** |
| Environment | 3.13.15, 16 polars threads, lock `efa4fd78…`, no thread variables: **matches** rule L v2 item 6 |
| Development mean | **440.91 s**: R1 442.93, R2 267.18, R3 394.95, S1 628.80, W1 470.67; S1c 633.04, W1c 482.05 |

## Steps (H021 v3 Validation Plan, reproduction)

- **`route_check.py E032 - E029`: passes on all 8 folds.**
- **`reproduce_check.py E032 E031`:**
  - R1 **+1.056**, R2 −0.393, R3 +0.144, S1 +0.649, W1 −0.725 s;
  - `within_tolerance: false` (R1 exceeds 1.0 s by 0.056 s).
  - CatBoost on GPU is a genuine re-draw (seed and non-deterministic kernels), unlike the deterministic LightGBM. The development mean moves by +0.15 s.
- **The noise condition** (`mechanism_check.py E032 E031 NM_present_excl_LIRF`):
  - **m = +0.683 s** (q95 +1.075); per fold R1 +0.65, R2 −0.05, R3 −0.07, S1 +0.13, W1 +2.77, S1c −0.87, W1c −0.72.
  - **|m| = 0.68 ≤ 1.5 s, so clause 1 is not INCONCLUSIVE.**
- **H021's clause 1, final:** −4.91 s with 5/5 counted WINs (E031 against E030) is **not met**. The categorical statistics carry signal on normal taxis at fixed capacity, at this budget.
  - Reported: the re-draw alone gives −4.23 s with 5/5 WINs against E030.
- **H023's noise condition** (half-size): |m| / 2 = 0.34 ≤ 0.5 s, so it is not INCONCLUSIVE on that ground.
- **H023's chain gating** (status only): H021 is COMPLETE and passed integrity, and H021r has run and passed integrity. **H023 is due.**
- **For H023r (if due):** the blend of [E029, E032] against [E029, E031] moves by half of E032 − E031 at the prediction level. That is about 0.53 s on R1 by RMSE scale (unverified until run).
