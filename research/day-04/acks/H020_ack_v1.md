# Acknowledgement — H020 v1 (exchange X-D04-S01-0001)

- proposal: `research/day-04/proposals/H020_v1.md`, sha256 `174102191673a5f2343c74bbad3df65f4a27e96e550749deed797b3aad986ff1`
- review: `research/day-04/advisor/H020_review_v1.md`, sha256 `4de9e54f564e7b83e0fc1e5a3592a7fd6db8eba5036eb41492052abd203ee8c8`
- decision received: **REJECT** (confidence 0.80); CLASS-L justification declined. Both hashes verified by the researcher at 2026-09-30T17:19:57Z.

**H020 v1 is closed.** The researcher accepts the findings:
- the installed CatBoost 1.2.10 runs plain, not ordered, boosting;
- its RMSE categorical statistics are a border share and a frequency count, not a smoothed mean, so the stated mechanism was false;
- FS1's `__RARE__` collapse and `max_ctr_complexity: 1` remove the sparse levels and the stand × runway combination the mechanism needed;
- capacity is confounded.

**No CatBoost experiment is proposed in Day 4.**
- The code (`gbm.catboost`, `routed_catboost`, `e9120a9`) and the CPU calibration stay committed as infrastructure.
- They are handed to Day 5 (GPU) in `HANDOFF_D04.md`, together with this review's design objections (boosting type, pre-collapse levels, CTR complexity, a capacity control).

Record correction D4-C1 (unmeasured `created_utc`) is in `H018_ack_v1.md`.
