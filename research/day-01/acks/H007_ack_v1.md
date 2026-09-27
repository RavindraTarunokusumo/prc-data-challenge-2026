# Acknowledgement — H007 v1 (exchange X-D01-S01-0003)

- proposal: `research/day-01/proposals/H007_v1.md`, sha256 `541ea19a3b65c253a019b629f23a7a4b6fd727d51841bbdb062d0dcd1e011706`
- review: `research/day-01/advisor/H007_review_v1.md`, sha256 `044e888b56166adddfb6c261afda87a4ccbc8fc24e95aaee5a8fdd5ddeeaa162`
- decision received: **ACCEPT**. Both hashes were verified by the researcher.
- acknowledged: 2026-09-27T12:36:01Z

Execution follows the review's Execution Authorization exactly: one primary run with the
config from the Implementation Plan, the comparisons listed there, a reproduction only
under the stated conditions, and at most one logged `rerun` after an infrastructure failure.

## Corrections to the proposal record (appended; the proposal is not edited)
1. **The comparison with H006 is confounded with capacity.** Minimum leaf size differs (about 10 against 100), and so does tree size (up to 1,024 against 255 leaves). A difference from H006 is attributed to the **configuration**, not the implementation.
2. **The criterion-4 check against H008 is cross-implementation**: it changes library and features together. If H007 is promoted over H006, the attributed mechanism is "the XGBoost configuration".
3. **The same single-row exposure as H006.**

## Batch conditions adopted (X-D01-S01-0003)
- **B1.** Brief §10 criteria 5 (no leakage), 7 (resources within class) and 8 (Advisor objections resolved) also apply to every promotion in the chain.
- **B2.** A candidate whose own falsification criterion is met is not promoted, even if it beats the current champion.
- **B3.** An S1 WIN with a non-negative S1c point dRMSE is an unresolved Advisor objection, and so blocks promotion under criterion 8.
- **B4 (standing rule 6).** Every comparison used for a promotion or a criterion-4 check reports, per fold, the share of the SSE change carried by the largest single row and by the 10 largest rows. Where one row carries ≥ 50 %, it also reports that row's airport, anchor, target and both predictions. This is attribution only; fold outcomes are unchanged. Implemented in `scripts/compare.py`.
