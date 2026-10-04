## Advisor result: X-D07-S01-0002 (H034–H037 v1)

**I accepted all four proposals, with binding conditions U1–U10, but the main finding is a correction: the forward risk is much larger than the proposal (and my own Day 3 wording) states.** The conditions are in `H035_review_v1.md`; the H034, H036 and H037 reviews adopt them by reference. Nothing is a HOLD: the four proposal hashes and the launcher hash (`f76db6fa15abf5c8a3712cea39e6454f1f4290295a25b3a109505076ada05eed`) match the envelope.

**Checks I ran, all read-only:**
- **Tests and lint:** the full suite passed (165) and ruff is clean. The experiment lock was free.
- **Code:** I reviewed the new override combiner, the worker dispatch and the formatter's override mode and `--tag`. The existing three-argument `route_check.py E046 E033 E045` already performs the override integrity check correctly; no script change is needed.
- **Combiner on real files:** run on stored predictions (R1, S1, W1c, W1), it reproduced the base exactly off the subgroup and swapped exactly the subgroup rows (168, 337 and 58).
- **Recorded figures:** the proposal's expectation table recomputes to 0.1 s (development mean 314.4).
- **Fresh holdout:** the earlier holdout records hold aggregates only, so December's subgroup is a fresh test.
- **What I did not touch:** no target or block-time column, no December row, no feature build, fit or score. E044's file is unchanged (`d57ff7db…`). The only tree changes are the four review files.

**Main findings:**
1. **The forward risk is understated (U6).**
   - All seven Day 3 break-even rates (0.009–0.099) reproduce exactly as mixture weights, with each row's 2025 gain or loss held fixed. They describe a change in which rows the subgroup contains, not a change in how block times are recorded.
   - For a fit calibrated to 2025, a row predicted at T + a(D − T) loses once its 2026 convention probability falls below a/2, i.e. about half its 2025 value. It does not take a fall to "a sixth of the lowest month".
   - If the convention were absent, the loss is of the same order as the 2025 gain. On S1 that is roughly half to all of it in squared-error terms.
   - The wording that produced the understatement is the Advisor's own, at Day 3 (e). U6 corrects that record too.
2. **The development folds cannot test the candidate.** Criteria 1–4 recompute Day 3's recorded contrast, and criterion 6 only checks determinism. December is the only fresh evidence.
   - So I pre-registered **objection F** (U7): a WIN on December resolves it, for December only. A TIE leaves H035 INCONCLUSIVE and E044's file stands. A LOSS triggers the frozen revert. Without an access, H035 is not promotable.
   - This is stricter than the frozen phase-close rule, which lets a promotion stand on a TIE.
3. **The rule 12 forward-support table for this subgroup was missing; I computed it (target-free).**
   - In every month, 81–96 % of subgroup rows are more than an hour behind schedule.
   - January 2026 sits above every 2025 month: median 7,141 s and q90 17,816 s against a 2025 maximum of 14,939 s. Its per-row stakes are the largest in both directions.
4. **Row concentration is known in advance.** Row 183903219 carried 79 % of W1's and 57 % of W1c's subgroup gain on Day 3. U8 requires W1 and W1c reported without it, plus exposure figures that measure the real downside.
5. **Allocation ids:** the proposal's "the ack records the mapping" conflicts with the pinned queue. The ids must be E045–E050 in the U1 order, or do not arm.
6. **Submission file:** the earlier rule on which file is uploaded (S8 of X-D07-S01-0001) is replaced only if H035 is promoted. `--tag E050` formatting runs only after that promotion (U9).

**Correction to my own work:** my first draft of the H035 review contained three launcher hash strings I had not taken from any tool output. I replaced them with the verified pin before hashing, and checked that every 64-character hash in all four reviews is a verified value.

**What the owner must decide:** the gain is a bet that LIRF keeps recording block times at schedule in 2026, with a downside of similar size. U9 requires this to be stated plainly to the owner before any upload decision.

**Window timing:** the queue fits the 00:00–01:00Z window. The expected end is about 00:45Z. Failed W&B syncs added about 100 s per run last time, and the guards do not count it. E049 and E050 are deferred only if E045 and E047 each run about 40 % longer than E029.

Files are in /home/rvindra/Projects/prc-data-challenge-2026/research/day-07/advisor/:
- H035_review_v1.md
- H034_review_v1.md
- H036_review_v1.md
- H037_review_v1.md

```yaml
schema: advisor-task-result-v1
exchange_id: X-D07-S01-0002
status: COMPLETE
decisions:
  - proposal_id: H034
    proposal_sha256: 2ccb7401113d8f4dad356978d95720cae08cd47e1f7c30dada5fa3f0b070a62f
    decision: ACCEPT
    review_path: research/day-07/advisor/H034_review_v1.md
    review_sha256: be24cbc1e4ad11a8e783d58840c4c3b8464d5aa3644081108ca882c92d826a59
  - proposal_id: H035
    proposal_sha256: ece127cbbec41fa96bc91950add8d6604be548e9607cf85522ef91f095cfff81
    decision: ACCEPT
    review_path: research/day-07/advisor/H035_review_v1.md
    review_sha256: 4f1c428d6995fc316ab8efba0df789e39ee4bf80307f531f95851b3b7b22afd7
  - proposal_id: H036
    proposal_sha256: 413475f20b4a404a73134ea5bc73867d86ddb4bdb6d13c3cc17bc19251adb698
    decision: ACCEPT
    review_path: research/day-07/advisor/H036_review_v1.md
    review_sha256: 547b2ebefc74f5ef9215e227c3d9f7b12ce837b444ca63f47a2e0e9968fa2f3d
  - proposal_id: H037
    proposal_sha256: 8e9c3f39082af5e613ef2b25715a6c884b4235463928769f14004d99ab2c3966
    decision: ACCEPT
    review_path: research/day-07/advisor/H037_review_v1.md
    review_sha256: 36b766bf8a239d1a0b8bd6ba7ffccc05449bcd3462f2ae6a424c7239731d7fa7
completed_utc: 2026-10-03T20:52:43Z
```
