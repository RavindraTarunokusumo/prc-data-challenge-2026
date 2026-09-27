# Acknowledgement — H006 v1 (exchange X-D01-S01-0003)

- proposal: `research/day-01/proposals/H006_v1.md`, sha256 `435a63b783e3a09fef51c92b5608af48941680ca8966cab4303e6639a1a964a8`
- review: `research/day-01/advisor/H006_review_v1.md`, sha256 `0ea1a1375c58a3dbecd363305f045a46860789ce50828596824aef7ac588a2d1`
- decision received: **ACCEPT**. Both hashes were verified by the researcher.
- acknowledged: 2026-09-27T12:36:01Z

Execution follows the review's Execution Authorization exactly: one primary run with the
config from the Implementation Plan, the comparisons listed there, a reproduction only
under the stated conditions, and at most one logged `rerun` after an infrastructure failure.

## Corrections to the proposal record (appended; the proposal is not edited)
1. **The single-row exposure** described in H005's acknowledgement applies to H006's S1 comparison with H005 as well.
2. **H008 removes four features**, not "three time-delta features": `d_aobt3`, `d_eobt1`, `d_sched` and `flt_missing`. H008 supports "the deltas are used". The interaction claim rests on the falsification clause against H004, not on H008. The Alternative Explanations sentence that attributes airport-bias correction to H008 is wrong; H004 is the control for that.
3. **Fold H is the largest fold** (24.8 % more training rows than S1). The runtime totals remain valid.

## Batch conditions adopted (X-D01-S01-0003)
- **B1.** Brief §10 criteria 5 (no leakage), 7 (resources within class) and 8 (Advisor objections resolved) also apply to every promotion in the chain.
- **B2.** A candidate whose own falsification criterion is met is not promoted, even if it beats the current champion.
- **B3.** An S1 WIN with a non-negative S1c point dRMSE is an unresolved Advisor objection, and so blocks promotion under criterion 8.
- **B4 (standing rule 6).** Every comparison used for a promotion or a criterion-4 check reports, per fold, the share of the SSE change carried by the largest single row and by the 10 largest rows. Where one row carries ≥ 50 %, it also reports that row's airport, anchor, target and both predictions. This is attribution only; fold outcomes are unchanged. Implemented in `scripts/compare.py`.
