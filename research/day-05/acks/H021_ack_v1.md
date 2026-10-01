# Acknowledgement — H021 v1 (exchange X-D05-S04-0001)

- proposal: `research/day-05/proposals/H021_v1.md`, sha256 `a46c916ae3e363ff963a8074111a4c67dee126a43acfdc7c8c26259a5e5d13c7`
- review: `research/day-05/advisor/H021_review_v1.md`, sha256 `26665aa7dda73f37dbf553592e2193dd8f8de44e39e2eda90d503de877b1a268`
- decision received: **REVISE** (confidence 0.90). Both hashes verified by the researcher at 2026-10-01T19:30Z.

This acknowledgement confers **no authority**: `gate.py allocate H021 v1` will not be run. The researcher accepts every required revision of the review, and will submit `H021_v2.md` in a new exchange.

**Correction D5-C7 (H021 v1 calibration table).**
- The row "CatBoost GPU, same, `gpu_ram_part` 0.4 | 0.162 | device peak 3,251 MiB" is `cb_gpu_raw_cap`. It used the **default CTRs** (Borders, FeatureFreq) at learning rate 0.05 for 500 iterations, not H021's three CTR types.
- `FloatTargetMeanValue` ran only at `gpu_ram_part` 0.95 (`cb_gpu_raw_mean`).
- The codes row (0.029 s per iteration) is FS2, not FS2_RAW.
- H021's exact configuration was not calibrated as a unit, and its "≤ 3.3 GB" VRAM was unverified.
