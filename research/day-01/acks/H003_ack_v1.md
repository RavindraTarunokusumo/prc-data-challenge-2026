# Acknowledgement — H003 v1 (exchange X-D01-S01-0003)

- proposal: `research/day-01/proposals/H003_v1.md`, sha256 `cbb3848e013eeb924ed5815417c1bd32a9517da323d90d7655ebe1316dc16b80`
- review: `research/day-01/advisor/H003_review_v1.md`, sha256 `493c824e9a4e5e3e45fa9c48e335d7dede87c1fa7dd711ae55d46d87415265f2`
- decision received: **ACCEPT**. Both hashes were verified by the researcher.
- acknowledged: 2026-09-27T12:36:01Z

Execution follows the review's Execution Authorization exactly: one primary run with the
config from the Implementation Plan, the comparisons listed there, a reproduction only
under the stated conditions, and at most one logged `rerun` after an infrastructure failure.

## Corrections to the proposal record (appended; the proposal is not edited)
1. **An unlisted alternative explanation.** The takeoff hour is label T. Part of its association with the target is mechanical: a long taxi pushes the same pushback into a later takeoff hour. The design does not isolate diurnal demand, and a causal-only variant will need a P-labelled time key.
2. **DST runs in opposite directions on W1 and W1c**, so H003 may score better on W1c than on W1.

## Batch conditions adopted (X-D01-S01-0003)
- **B1.** Brief §10 criteria 5 (no leakage), 7 (resources within class) and 8 (Advisor objections resolved) also apply to every promotion in the chain.
- **B2.** A candidate whose own falsification criterion is met is not promoted, even if it beats the current champion.
- **B3.** An S1 WIN with a non-negative S1c point dRMSE is an unresolved Advisor objection, and so blocks promotion under criterion 8.
- **B4 (standing rule 6).** Every comparison used for a promotion or a criterion-4 check reports, per fold, the share of the SSE change carried by the largest single row and by the 10 largest rows. Where one row carries ≥ 50 %, it also reports that row's airport, anchor, target and both predictions. This is attribution only; fold outcomes are unchanged. Implemented in `scripts/compare.py`.
