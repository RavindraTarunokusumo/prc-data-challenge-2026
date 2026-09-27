# Acknowledgement — H001 v1 (exchange X-D01-S01-0003)

- proposal: `research/day-01/proposals/H001_v1.md`, sha256 `38225fb0d6b274cf6904445b2fe0b38de5c2267bee7d140c65e1c07d09dd2d84`
- review: `research/day-01/advisor/H001_review_v1.md`, sha256 `11ee34242ff190108963443877937e7111e7b819806407ec2ce746c074778945`
- decision received: **ACCEPT**. Both hashes were verified by the researcher.
- acknowledged: 2026-09-27T12:36:01Z

Execution follows the review's Execution Authorization exactly: one primary run with the
config from the Implementation Plan, the comparisons listed there, a reproduction only
under the stated conditions, and at most one logged `rerun` after an infrastructure failure.

## Corrections to the proposal record (appended; the proposal is not edited)
1. **Stale label.** Controlled Variables calls FS0 "static". DATASET_AUDIT §6.2 defines only P, T and F. The correct labels are those in the Leakage Analysis section. The stale term in the `src/prc/features.py` docstring is corrected in code, which is not frozen.
2. **Wrong calibration premise.** "The largest fold, S1" is false. Fold H trains on 1,919,370 DEP rows, 24.8 % more than S1 (1,537,475). The order is H > R3 > W1 > R2 > S1 > R1 > S1c > W1c.

## Batch conditions adopted (X-D01-S01-0003)
- **B1.** Brief §10 criteria 5 (no leakage), 7 (resources within class) and 8 (Advisor objections resolved) also apply to every promotion in the chain.
- **B2.** A candidate whose own falsification criterion is met is not promoted, even if it beats the current champion.
- **B3.** An S1 WIN with a non-negative S1c point dRMSE is an unresolved Advisor objection, and so blocks promotion under criterion 8.
- **B4 (standing rule 6).** Every comparison used for a promotion or a criterion-4 check reports, per fold, the share of the SSE change carried by the largest single row and by the 10 largest rows. Where one row carries ≥ 50 %, it also reports that row's airport, anchor, target and both predictions. This is attribution only; fold outcomes are unchanged. Implemented in `scripts/compare.py`.
