# Acknowledgement — H002 v1 (exchange X-D01-S01-0003)

- proposal: `research/day-01/proposals/H002_v1.md`, sha256 `83e85637037e74215694d0656639f9047fe823903a7f2f17758de544d74be77d`
- review: `research/day-01/advisor/H002_review_v1.md`, sha256 `600c1de09de900794cc8ddf70514ff1721ab1a356b1f076cb3147b704d9a56e1`
- decision received: **ACCEPT**. Both hashes were verified by the researcher.
- acknowledged: 2026-09-27T12:36:01Z

Execution follows the review's Execution Authorization exactly: one primary run with the
config from the Implementation Plan, the comparisons listed there, a reproduction only
under the stated conditions, and at most one logged `rerun` after an infrastructure failure.

## Corrections to the proposal record (appended; the proposal is not edited)
1. **The estimator changes together with the key.** H001 predicts a mean and H002 a median. In-sample on the audit moments, the median gives up about 4.7 s of a roughly 31.6 s airport effect. A failure against H001 would be ambiguous, and the analysis must resolve it with the per-airport `bias`.
2. **Criterion 3 is not free.** The airport median is worse than the global mean at LTFM (+1.1 %), LFPG (+0.8 %), LEBL (+0.6 %) and LEMD (+0.2 %) on all-year moments.
3. **"Airport offsets are stable across 2025" is inaccurate for LFPG** (median about 900 s in Jan–Jun, about 1,013 s in Aug–Nov). The analysis will report the LFPG row of the S1-versus-S1c contrast.

## Batch conditions adopted (X-D01-S01-0003)
- **B1.** Brief §10 criteria 5 (no leakage), 7 (resources within class) and 8 (Advisor objections resolved) also apply to every promotion in the chain.
- **B2.** A candidate whose own falsification criterion is met is not promoted, even if it beats the current champion.
- **B3.** An S1 WIN with a non-negative S1c point dRMSE is an unresolved Advisor objection, and so blocks promotion under criterion 8.
- **B4 (standing rule 6).** Every comparison used for a promotion or a criterion-4 check reports, per fold, the share of the SSE change carried by the largest single row and by the 10 largest rows. Where one row carries ≥ 50 %, it also reports that row's airport, anchor, target and both predictions. This is attribution only; fold outcomes are unchanged. Implemented in `scripts/compare.py`.
