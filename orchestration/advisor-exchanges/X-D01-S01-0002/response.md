## Advisor result: exchange X-D01-S01-0002 (SPLITS v2 split-freeze review)

**Decision: ACCEPT (confidence 0.80).** You may freeze exactly the six pinned files with one run of `uv run python scripts/gate.py freeze --proposal research/day-01/proposals/SPLITS_v2.md --review research/day-01/advisor/SPLITS_review_v2.md --ack research/day-01/acks/SPLITS_ack_v2.md`, followed by the §13 checkpoint. If any of the six files changes before the freeze, this ACCEPT lapses. No experiment is authorized by this review.

The review is at `/home/user/prc-data-challenge-2026/research/day-01/advisor/SPLITS_review_v2.md`. Its front matter parses the way `gate.py` expects: `decision: ACCEPT`, and `proposal_sha256` matches the proposal.

### What I checked
All six required revisions from v1 are resolved:
- **Hashes:** the proposal hash matches the envelope. The six pinned hashes, the supporting hashes and the v1 review hash all match the files on disk. Silver matches both its pin and its manifest.
- **Tests and lint:** 83 tests pass and ruff is clean.
- **Row counts:** every pinned fold row count reproduces. I counted H by rows only, without reading target columns.
- **LFPG runway shares:** the Jan 2026, Jul 2026 and Dec 2025 facts in the audit reproduce.
- **History:** no commit after the envelope touched a frozen file.
- **Holdout:** no test reads December targets.
- **Secrets:** no secret value appears in any tracked file.

### Three findings that don't block the freeze
I measured these on real development-fold truth with constant or oracle predictors. No December data was used and no feature was evaluated.

1. **The rule tells you a gain is real, not where it comes from.**
   - A test predictor that differs from a constant only by +60 s on rows with y > 3,600 s WINs all seven folds and passes criteria 1–3: mean −1.30 s, q95 −1.09 s. Those rows are 0.14–0.53 % of each fold.
   - The proposal says the 1.0 s floor sits at the tail-only sensitivity. That is wrong for the v2 folds: W1 alone moves by 2.09 s. The floor works as a minimum effect size, not a guard against tail-only gains.
   - Otherwise the rule behaves well. Under a null (200 runs), per-fold WIN and LOSS rates stay near the nominal 10 % and the full rule never passes. A steady gain of about 1.1 s on the bulk passes 76–100 % of the time.
2. **The twin rule only catches reversals.** A gain that needs the months after validation keeps its S1 WIN whenever S1c comes out TIE.
3. **The holdout "phase" comes from the proposal's day directory.**
   - A promotion that rests on an experiment from an earlier phase cannot be checked at phase close.
   - An access a phase didn't use can be spent later.
   - `holdout_compare` also returns full segment tables for H, which is more than the decision needs.

I handle all three through standing review rules under brief §10 items 4 and 8, listed in the review's Revision section. They cover:
- per-fold bulk versus tail attribution;
- the expected sign on S1c and W1c for regime-sensitive hypotheses;
- citing H only through the phase-close outcome;
- calendar-month identity: no fold can validate it, because each development fold's validation month is absent from its training months, while Jan 2025 and Jul 2025 are both in training for the test;
- coverage of all seven folds plus H.

The review also lists non-frozen hardening you can do at any time without an incident: seed and H enforcement, guarding `load_silver` unmasking, closing the isolation-test gap, a ledger check in `compare.py`, trimming `holdout_check.py` output, and recording the `uv.lock` hash.

**Nits:**
- The proposal's `created_utc` (12:20:00Z) is later than both the envelope and this review, so it is not a measured time.
- The `winter_fold`, `twin_rule` and `reproduction` config keys are not read by any code.

### What you need to do
- Write `research/day-01/acks/SPLITS_ack_v2.md`. It must reference the proposal hash and the review hash below.
- The ack should also note two corrections: finding 1 (the floor's actual role) and the timestamp.
- H001–H008 and the two new CLIs from commit 312fb1d are outside this envelope and were not reviewed.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D01-S01-0002
status: COMPLETE
decisions:
  - proposal_id: SPLITS
    proposal_sha256: 827e0319241fb5da37aa9eb956ca7073c5323756439212a03567e9af2d65d561
    decision: ACCEPT
    review_path: research/day-01/advisor/SPLITS_review_v2.md
    review_sha256: 7d42b7a0538db68d719e0a750bc56333b7c51e8d2a52206eb9b2a7d41ce587dc
completed_utc: 2026-09-27T11:59:04Z
```
