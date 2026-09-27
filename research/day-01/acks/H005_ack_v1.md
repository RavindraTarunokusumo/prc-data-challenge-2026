# Acknowledgement — H005 v1 (exchange X-D01-S01-0003)

- proposal: `research/day-01/proposals/H005_v1.md`, sha256 `ab97e4312158b0a5c26d6223423539969308daf39ac1807d3c93c6fcf054ff44`
- review: `research/day-01/advisor/H005_review_v1.md`, sha256 `2b4658c558bd61ee5cca4a87167fa53832e2a16544299c678ead7db8d87b22ea`
- decision received: **ACCEPT**. Both hashes were verified by the researcher.
- acknowledged: 2026-09-27T12:36:01Z

Execution follows the review's Execution Authorization exactly: one primary run with the
config from the Implementation Plan, the comparisons listed there, a reproduction only
under the stated conditions, and at most one logged `rerun` after an infrastructure failure.

## Corrections to the proposal record (appended; the proposal is not edited)
Target-free findings, recorded as the review lists them:
1. **A day-scale anchor in S1's validation month.** One LIRF row in July 2025 has `d_aobt3` = 87,181 s, with its NM and schedule times about 24 h before takeoff. No S1 training month has any `d_aobt3` ≥ 20,000 s, and July 2026 has one similar row (86,340 s). H005 predicts about 87,000 s for it. Whether that is right depends on that row's recorded block time.
2. **Negative anchors.** Validation months hold rows with `d_aobt3` < −600 s (Jul 117, Sep 86, Oct 49, Nov 23; minimum −11,521 s). H005 passes them through as negative predictions.
3. **The January 2026 anchor tail.** 0.375 % of Jan 2026 rows have anchors ≥ 3,600 s, against 0.067–0.132 % in every 2025 month. No fold reproduces this.

H005 stays unguarded: no clip or cap, as authorized.

## Batch conditions adopted (X-D01-S01-0003)
- **B1.** Brief §10 criteria 5 (no leakage), 7 (resources within class) and 8 (Advisor objections resolved) also apply to every promotion in the chain.
- **B2.** A candidate whose own falsification criterion is met is not promoted, even if it beats the current champion.
- **B3.** An S1 WIN with a non-negative S1c point dRMSE is an unresolved Advisor objection, and so blocks promotion under criterion 8.
- **B4 (standing rule 6).** Every comparison used for a promotion or a criterion-4 check reports, per fold, the share of the SSE change carried by the largest single row and by the 10 largest rows. Where one row carries ≥ 50 %, it also reports that row's airport, anchor, target and both predictions. This is attribution only; fold outcomes are unchanged. Implemented in `scripts/compare.py`.
