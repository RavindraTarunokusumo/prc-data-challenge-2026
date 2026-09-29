Exchange X-D02-S01-0004 is complete: **H013 v1 is REVISE (0.92) and H014 v1 is ACCEPT with conditions (0.80).** Both proposal hashes matched the envelope, so neither review is a HOLD.

**Why H013 is REVISE.** H013 rests on the claim that LightGBM without row and feature subsampling does not use the seed. That is false on seven of its eight folds.
- **The mechanism.** `gbm.py` passes `seed` to LightGBM. LightGBM derives a second seed from it and uses that to pick the rows it builds feature bins from, whenever the training set exceeds 200,000 rows (the library default). Nothing in `src/`, `scripts/` or `config/` overrides either setting.
- **The folds.** Every fold except W1c trains on 1.0–1.9 M rows. W1c trains on January only, 153,706 rows.
- **The check.** I ran synthetic data only, through the unchanged `gbm.lightgbm` with H013's parameters and 4 threads, with no repository writes:
  - at 150,000 training rows, seeds 42 and 43 give identical predictions;
  - at 400,000 rows, all 20,000 predictions differ between the seeds (up to 271 s), while a same-seed rerun is identical;
  - making the bin sample cover every row, or fixing its seed, restores identity. That confirms the mechanism; it is not a recommendation.
- **The cited evidence doesn't reach this regime.** The committed test fits 1,500 rows. The "4-thread, 20,000-row check" cited as commit `f84fea3` is not in that commit, and is below the threshold anyway.
- **Consequences.**
  - The pre-registered reproduction result ("identical predictions, 0.00 s") is false as configured. The seed-43 run would be a real perturbation test with an unknown outcome on R3 and S1.
  - E015's failure can't be pinned on subsampling alone, because E015 also re-drew the bin sample.

**Rulings the envelope asked for** (all binding on H013 v2):
- **Criterion 6.**
  - If the training procedure has no random component at all, the reproduction becomes a determinism check. That satisfies both the rule and its intent, as for ridge (`PHASE_CLOSE_D01_review_v1.md`, line 73).
  - If the seed has no effect only because some random step is fixed independently of it, that does not satisfy the intent, because the reproduction never re-draws that step.
  - Either way, E015's spread (up to 3.5 s on S1, 1.7 s on R3) must be recorded as a standing disclosure if H013 is promoted.
- **Reusing E013 and E014 for clauses 3 and 4.** Both are allowed, with conditions.
  - The "bounds" the proposal cites (E015 − E012 shifts) measure seed spread, not the effect of switching subsampling off. The effect nothing measures is on the E013/E014 side.
  - Clause 4's margins (−33 to −96 s, 7/7 WIN) are too large for that to matter.
  - Clause 3 works as a sign test: four of five margins exceed 1,000 s, and R2 is the thinnest at −314 s.
  - v2 must add `mechanism_check.py H013 E012` on `LIRF_NM_missing` and on `NM_present`, and pre-register per fold what measured shift makes the reuse inadmissible.
- **Criterion 8.** I did not accept widening the bound to +7,000 s.
  - The spread the proposal cites is at most 148 s on any fold (66 s on S1), not 500 s.
  - E015 implies +6,456 s on S1, and E012 was +6,390 s.
  - H009's rule (≤ +6,500 s on every development fold) applies unless v2 gives a rationale the committed evidence supports.

**H014 conditions.** It may run only after an H013 version ≥ 2 is accepted with exactly v1's training configuration, and after H013 passes clause 1. If H013 v2 changes anything else in training, this ACCEPT lapses and H014 needs a v2. The bin-seed finding does not break the H013 − H014 comparison: both use seed 42 on the same rows, so shared features get identical bins.

**Other checks (read-only, nothing in the repository changed except the two reviews):**
- Frozen-file hashes, the Advisor definition hash and `uv.lock` all match. The clause code and `gbm.py` are unchanged, `tests/test_models.py` passes 13/13, and the tree was clean.
- The E015/E016 allocation-order slip has no scientific consequence. The runs were sequential: E016 ran 20:26:02–20:40:44Z and E015 20:40:44–20:55:12Z.
- E015's `git_dirty_at_run: true` is undisclosed in its analysis, but only output files changed around its run commit.
- INC-0003 is still open (not blocking).

Files are in `/home/user/prc-data-challenge-2026/research/day-02/advisor/`:
- H013_review_v1.md
- H014_review_v1.md

Synthetic check script (outside the repository): `/tmp/claude-0/-home-user-prc-data-challenge-2026/0b2147c0-74e1-4b58-965c-6ea22d5b4eaa/scratchpad/seed_check.py`

```yaml
schema: advisor-task-result-v1
exchange_id: X-D02-S01-0004
status: COMPLETE
decisions:
  - proposal_id: H013
    proposal_sha256: e47d382841a5382f6cd5aabf83ea85f4f6c554e93717dcb42b5f28aa420e3290
    decision: REVISE
    review_path: research/day-02/advisor/H013_review_v1.md
    review_sha256: 96f9ed862f16eb67d49d87375fa9ee8c3e2c83f1b18d5b82f7abae8836ab392f
  - proposal_id: H014
    proposal_sha256: bfaadc501f4752e83171c10afff3290b1eb5b6dfa40d817ea21ffbe23ee4eca8
    decision: ACCEPT
    review_path: research/day-02/advisor/H014_review_v1.md
    review_sha256: 479534116888f92aa63fb9d3187625e3569c24869b45816a7656f5111a2c2b09
completed_utc: 2026-09-28T21:19:30Z
```
