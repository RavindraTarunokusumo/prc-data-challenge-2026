# Acknowledgement — H008 v1 (exchange X-D01-S01-0003)

- proposal: `research/day-01/proposals/H008_v1.md`, sha256 `8266cc62f8905511bb3a6232ee038fdf30e1f1a2f188ea2efcc9da27f997a525`
- review: `research/day-01/advisor/H008_review_v1.md`, sha256 `affdf8362d80346666a5609aaf87815e8761ef78ac9766e5085ae78b86fed47f`
- decision received: **ACCEPT**. Both hashes were verified by the researcher.
- acknowledged: 2026-09-27T12:36:01Z

Execution follows the review's Execution Authorization exactly: one primary run with the
config from the Implementation Plan, the comparisons listed there, a reproduction only
under the stated conditions, and at most one logged `rerun` after an infrastructure failure.

## Corrections to the proposal record (appended; the proposal is not edited)
1. **The Expected Result is internally inconsistent.** "10–20 % above H006" (337–479 s) and "0–5 % below H003" (497–557 s) cannot both hold. It **will not be scored as a prediction**, and no new value is substituted. The falsification criterion is unaffected.

## Batch conditions adopted (X-D01-S01-0003)
- **B1.** Brief §10 criteria 5 (no leakage), 7 (resources within class) and 8 (Advisor objections resolved) also apply to every promotion in the chain.
- **B2.** A candidate whose own falsification criterion is met is not promoted, even if it beats the current champion.
- **B3.** An S1 WIN with a non-negative S1c point dRMSE is an unresolved Advisor objection, and so blocks promotion under criterion 8.
- **B4 (standing rule 6).** Every comparison used for a promotion or a criterion-4 check reports, per fold, the share of the SSE change carried by the largest single row and by the 10 largest rows. Where one row carries ≥ 50 %, it also reports that row's airport, anchor, target and both predictions. This is attribution only; fold outcomes are unchanged. Implemented in `scripts/compare.py`.
