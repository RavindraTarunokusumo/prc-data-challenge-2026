# Acknowledgement — SPLITS v2 (exchange X-D01-S01-0002)

- proposal: `research/day-01/proposals/SPLITS_v2.md`, sha256 `827e0319241fb5da37aa9eb956ca7073c5323756439212a03567e9af2d65d561`
- review: `research/day-01/advisor/SPLITS_review_v2.md`, sha256 `7d42b7a0538db68d719e0a750bc56333b7c51e8d2a52206eb9b2a7d41ce587dc`
- decision received: **ACCEPT** (confidence 0.80). Both hashes and all six pinned freeze hashes were re-verified by the researcher before the freeze.
- acknowledged: 2026-09-27T11:59:57Z

Authorized scope: `scripts/gate.py freeze` over exactly the six pinned files, then the
§13 checkpoint. No experiment is authorized.

## Corrections to the proposal record (appended; the proposal itself is not edited)

1. **Role of the 1.0 s floor.** SPLITS_v2 said the 1.0 s criterion-1 minimum "sits at the
   tail-only sensitivity measured in the review". That is wrong for the v2 folds. W1 alone
   moves by 2.09 s under a +60 s tail-only change, and a tail-only predictor passes
   criteria 1–3. The floor is a **minimum effect size**, not a guard against tail-only
   gains. The guard is the Advisor's standing rule 1: per-fold bulk/tail attribution, and a
   pre-registered tail mechanism when most of the margin comes from y ≥ 3,600 s.
2. **Timestamp.** The proposal's `created_utc` (12:20:00Z) was typed, not measured. It is
   later than both the envelope (created 11:3x Z) and the review. From now on every
   `created_utc` is taken from `date -u` when the file is written. The same applies to the
   unsubmitted H001–H008 drafts, which are regenerated with measured timestamps before
   submission.

## Standing review rules

The five standing rules in the review's Revision section (tail attribution, forward
exposure, holdout use, calendar-month identity, fold coverage) are adopted, and every
subsequent proposal pre-registers against them.
