Exchange X-D02-S01-0005 is complete: **H013 v2 is ACCEPT (0.80) and H014 v2 is ACCEPT (0.85), both with conditions.** Both proposal hashes matched the envelope, so neither is a HOLD.

**H013 v2.** It meets all five required items from the v1 review. The premise is correct: with no subsampling and bins built from every training row, LightGBM makes no random draw. That falls under ruling 2 (it qualifies for criterion 6), not ruling 3. Pinning `data_random_seed` was rightly rejected.

I checked this at fold scale on synthetic data only. The frame had 1,919,370 training rows shaped like FS1: four categoricals with 160–1,800 levels, and rare records with day-scale targets. The fits ran with H013's parameters through the unchanged `gbm.lightgbm`, 60 rounds, 4 threads:

| Configuration | Seed 42 against seed 43 |
|---|---|
| All-row bins (v2) | identical (0 of 60,000 differ); a same-seed rerun is identical too |
| Default bin sample (v1) | all 60,000 differ (max 17,640 s) |
| v2 against v1, both seed 42 | all 60,000 differ (max 16,719 s) |

The third row matters: binning from all rows also changes the model, and moves day-scale predictions by thousands of seconds. So H013 − E012 on LIRF NM-missing rows may be large, and the admissibility rule will probably bite on R2 (threshold 157 s).

**What the ACCEPT adds** (the ack must record all of it):
- **Objection T (new, under criterion 8).** Clause 4's admissibility rule checks only the five development folds. But criterion 2 reads the twins: an S1c LOSS voids the S1 WIN, and S1 must win. The E015 − E012 shifts also differed in sign between S1 and S1c, so an admissible S1 says nothing about S1c.
  - The statistic is H013 − E012 on NM-present rows for S1c and W1c, which chain step 1 already produces.
  - The objection stands if it reaches half the twin margin: S1c ≥ 21.153 s or W1c ≥ 47.966 s.
  - If it stands, the proposal's own consequence applies: not promotable on Day 2 without a separately reviewed matched M2 ablation, no reproduction, and decision INCONCLUSIVE.
  - My v1 review asked for the rule "per development fold", so the gap is partly mine.
- **Reading 1: clauses 3 and 4 are carry-over tests.**
  - Every clause 3 fold that would fail is automatically inadmissible, so clause 3 is met exactly when three or more development folds are inadmissible.
  - Clause 4 can fail with every fold admissible only in an unlikely case: a fold's bootstrap wider than its margin.
  - A clause met through inadmissible folds therefore means the mechanism was not re-established by reuse. It blocks promotion, is not evidence against M2 or M3, and gives INCONCLUSIVE, not REJECT.
- **Reading 2: "identical predictions" needs a check.**
  - `reproduce_check.py` compares fold RMSEs only. Prediction identity should come from the per-fold prediction SHA-256s in the two manifests; E005/E009 are byte-identical this way.
  - If any fold differs, the "no random component" premise is falsified and must be reported. Criterion 6 then becomes a perturbation test under the frozen 1.0 s tolerance (ruling 4).
- **Reading 3: admissibility thresholds use full precision.** For example, clause 4's R3 threshold is 29.549 s, not the table's 29.6.

**Preconditions before allocation.**
- The ack is committed.
- STATE.md is refreshed: its header (20:57:38Z) predates X-D02-S01-0004.
- The clause code stays unchanged from `5ba9230` until clauses 1–4 and objection T are computed.
- The lock file, `gbm.py`, the feature-set functions and silver are unchanged.
- Nothing runs concurrently.

**H014 v2.** The only change from v1 is `bin_construct_sample_cnt`. The shared FS0 features now get identical bins by construction, not just because both runs used seed 42.
- The conditions are those of v1: H013 v2 ran with exactly its authorized parameters, H013 passes clause 1, and nothing concurrent.
- It lapses if H013 v2 is superseded by a version with a different training configuration.
- H014 − E006 is only a weak proxy for how much the new training setup shifts E013 and E014 (H013's untested "comparable size" assumption). FS0 lacks the high-cardinality keys whose bins change most.

**Prediction.** The biggest risk to promoting H013 is the S1 LIRF bulk trade, which must stay at or below +6,500 s on every development fold (P about 0.45; E012 was at +6,390 s). Overall promotion is about 0.20. The accuracy margin over E005 should hold (P 0.93).

**What I checked (read-only).**
- Frozen-file, Advisor-definition and `uv.lock` hashes all match.
- The clause code and `src/prc` are unchanged since `5ba9230`. The feature-set functions are identical to the commits the proposals cite (compared by syntax tree).
- The runner passes the new parameter through to LightGBM unchanged, and stored predictions are checked against their manifests before reuse.
- Training-row counts per fold (largest 1,919,370) and every cited margin match the committed files. The final submission folds (2,085,047 rows) are also under 5,000,000.
- The E015 notes were appended without altering earlier text.
- `tests/test_models.py` passes 14/14.
- No December targets were read, and no model was fitted or scored on real data.

**Erratum to my v1 review.** I wrote that the older seed-invariance test fits "1,500 training rows"; it fits 300. H013_ack_v1 repeats the figure. The conclusion is unchanged, since 300 is also below the threshold.

I wrote only the two review files. `response.md` and `checksums.sha256` are left for your mirror.

Files:
- /home/user/prc-data-challenge-2026/research/day-02/advisor/H013_review_v2.md
- /home/user/prc-data-challenge-2026/research/day-02/advisor/H014_review_v2.md
- Synthetic check script (outside the repository): /tmp/claude-0/-home-user-prc-data-challenge-2026/0b2147c0-74e1-4b58-965c-6ea22d5b4eaa/scratchpad/scale_check.py

```yaml
schema: advisor-task-result-v1
exchange_id: X-D02-S01-0005
status: COMPLETE
decisions:
  - proposal_id: H013
    proposal_sha256: 13fc73618aba0d9a3e8ce9832e0896fa79bac6a177112714e9f2ebe09f7d20e9
    decision: ACCEPT
    review_path: research/day-02/advisor/H013_review_v2.md
    review_sha256: d46b89761a5047b80d0060b83dba5f92b22c49cc8fb9cb6c9ec00e1e501b4091
  - proposal_id: H014
    proposal_sha256: 49a8ec9036a62c59850a61c102119c17eb5b136a1941d8b09a63819374b441f4
    decision: ACCEPT
    review_path: research/day-02/advisor/H014_review_v2.md
    review_sha256: 4d6395c87af7c72effa2a6e4eaa854524519b85300e954b069fb0b8e57bb1c9a
completed_utc: 2026-09-28T21:48:08Z
```
