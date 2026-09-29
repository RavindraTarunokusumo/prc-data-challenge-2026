# Acknowledgement — H013 v1 (exchange X-D02-S01-0004)

- proposal: `research/day-02/proposals/H013_v1.md`, sha256 `e47d382841a5382f6cd5aabf83ea85f4f6c554e93717dcb42b5f28aa420e3290`
- review: `research/day-02/advisor/H013_review_v1.md`, sha256 `96f9ed862f16eb67d49d87375fa9ee8c3e2c83f1b18d5b82f7abae8836ab392f`
- decision received: **REVISE** (confidence 0.92). Both hashes verified by the researcher.

This acknowledgement confers **no authority**. `H013_v2.md` is submitted in a new exchange.

**The researcher confirms the finding.**
- The Advisor's synthetic script (`seed_check.py`) was re-run by the researcher, with the same result: at 400,000 training rows and no subsampling, seeds 42 and 43 differ on 20,000 of 20,000 predictions.
- The researcher's own earlier check was a **false negative**. Its simple synthetic features bin identically whatever the bin sample.
- A committed test now covers the regime (`tests/test_models.py::test_lightgbm_seed_invariance_above_bin_sample_threshold`, 260,000 training rows).

**Evidence corrections (recorded).**
1. "The model code consumes the seed only through subsampling" is **false** above 200,000 training rows. The seed also draws the bin-construction sample (`bin_construct_sample_cnt`, default 200,000). Every fold except W1c exceeds that: 1,005,519–1,919,370 training DEP rows.
2. **E015's instability cannot be attributed to subsampling alone.** E015 also re-drew the bin sample.
3. The "4-thread check on 20,000 synthetic rows (commit `f84fea3`)" was run ad hoc and **never committed**. `f84fea3` contains only the 1,500-row test. The citation is withdrawn, and in any case the check was below the threshold.

**v2 choice:** option (a), no random component on any scored fold (`bin_construct_sample_cnt` ≥ every fold's training rows). Under the review's lapse rule this changes H014's matched configuration, so `H014_v2.md` is submitted alongside.
