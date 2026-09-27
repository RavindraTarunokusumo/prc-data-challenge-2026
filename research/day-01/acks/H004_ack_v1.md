# Acknowledgement — H004 v1 (exchange X-D01-S01-0003)

- proposal: `research/day-01/proposals/H004_v1.md`, sha256 `9eb6270e3a3166890a412c98442d07a8e4607c76e3d0206d12a643de496b2621`
- review: `research/day-01/advisor/H004_review_v1.md`, sha256 `918535aab12f1fbc227ff3ebe7e4969736b4ffd27d1a2c1424016428b519fe01`
- decision received: **ACCEPT**. Both hashes were verified by the researcher.
- acknowledged: 2026-09-27T12:36:01Z

Execution follows the review's Execution Authorization exactly: one primary run with the
config from the Implementation Plan, the comparisons listed there, a reproduction only
under the stated conditions, and at most one logged `rerun` after an infrastructure failure.

## Corrections to the proposal record (appended; the proposal is not edited)
1. **Fold H is the largest training fold** (1,919,370 rows). The FS0 build alone measured 3.45 GB on it. If H004's peak exceeds the CLASS-S 4 GB target, `within_class` is false and criterion 7 fails. H004 then cannot be promoted, but its reference numbers remain valid. It is not reclassified.
2. **Missing control.** If H004's margin (or deficit) against H005 is carried by rows beyond the winsorisation clip, it measures clipping, not linear bias correction. The B4 figures report this, and the linear-combination mechanism is not claimed in that case.

## Batch conditions adopted (X-D01-S01-0003)
- **B1.** Brief §10 criteria 5 (no leakage), 7 (resources within class) and 8 (Advisor objections resolved) also apply to every promotion in the chain.
- **B2.** A candidate whose own falsification criterion is met is not promoted, even if it beats the current champion.
- **B3.** An S1 WIN with a non-negative S1c point dRMSE is an unresolved Advisor objection, and so blocks promotion under criterion 8.
- **B4 (standing rule 6).** Every comparison used for a promotion or a criterion-4 check reports, per fold, the share of the SSE change carried by the largest single row and by the 10 largest rows. Where one row carries ≥ 50 %, it also reports that row's airport, anchor, target and both predictions. This is attribution only; fold outcomes are unchanged. Implemented in `scripts/compare.py`.
