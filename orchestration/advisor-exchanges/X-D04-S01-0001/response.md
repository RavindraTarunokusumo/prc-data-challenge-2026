The batch review for X-D04-S01-0001 is done. No proposal can run: **H018 v1 and H019 v1 are REVISE** and **H020 v1 is REJECT**, and I decline the CLASS-L justification for H020.

All three proposal hashes match the envelope. I only wrote the three review files. Every check was read-only, target-free or synthetic: I read no December target and fitted or scored no model on a real fold.

**H018 v1 — REVISE (0.88).** The treatment itself is sound and correctly implemented. The two blocking problems are in what it pre-registers:
- **Clause 1 does not test the claim it names.** On `NM_missing_other` bulk rows (5 development folds), every LightGBM fit has 60–83 out-of-range predictions below 1 h of schedule delay, with or without T windows. The congestion increment D3-C2 explains sits above 3 h: against E021, the matched fit without T windows (118 in total), E019 adds +63 of its +68 there.
  - If the exclusion removes exactly that increment, the count lands near 118, above the 93 threshold.
  - The record would then say "falsified, D3-C2 needs correcting", which is the opposite of what the data would show. Under rule B2 that would also bar promotion.
- **The rule 8 statement is false.** "The LightGBM no longer learns the convention from LIRF" does not hold: 932 LIRF block-at-schedule tail rows that have NM data stay in training.
  - On S1 they carry 10.4 % of E019's error. The treated subgroup carries 1.9 %.
  - In existing fits, those rows alone move S1's all-rows RMSE by −1.96 to +2.44 s. That is the size of H018's whole expected effect, and S1 is the WIN promotion needs.
- Record items:
  - "About 8 times" should be about 4.2 times.
  - The E006/E012/E015/E018 counts are not in any committed file (they re-derive exactly).
  - Nothing says the chain stops if H018 is INVALID.

**H019 v1 — REVISE (0.82).** The priors code is correct. The −3.0 s floor is decisive: at least 12× the development-mean shifts of the committed perturbation pairs.
- **The prior block does nothing on W1c.** W1c has one training month, so all 153,706 training rows get null or constant priors (checked on the real view). A synthetic LightGBM fit with such columns gives byte-identical predictions.
  - W1c will therefore equal H018 exactly, a TIE, not "LOSS with probability 0.5".
  - So the W1 causal twin is vacuous. 8 of the 9 months behind W1's priors come after February, and no fold checks them causally.
- **No contingency is stated for H018's outcome.** It must say what happens if H018 is INVALID, and how criterion 4 and B2 treat H018's change when it is carried into H019's promotion.
- The same rule 8 error appears here.
- The joint-key figures that justify the choice of priors are not committed, and the rule that picked the five priors is not stated. The EDA also has no control for the NM off-block anchor, so its +0.19 R² is a loose upper bound.

**H020 v1 — REJECT (0.80).**
- **The stated mechanism is not what would run.** The installed CatBoost 1.2.10 resolves to plain boosting, not ordered. Its categorical statistics for RMSE are a share of rows above one target border plus a frequency count, not a smoothed mean. "The prior mechanism of H019, learned inside the model" is therefore false.
- **The design cannot test categorical handling:**
  - FS1 has already collapsed levels under 100 rows, so the sparse levels the mechanism needs are gone.
  - `max_ctr_complexity: 1` removes the stand × runway combination.
  - Tree capacity is confounded with no control.
- The pre-registered result is a scoped negative that changes no Day 4 or Day 5 decision, so CLASS-L is not justified.

Also:
- **Timestamps.** All three proposals' `created_utc` values (17:05, 17:25 and 17:55Z) are later than the commit that contains them (`3298cc0`, 16:51:03Z).
- **Verified.** Tests 141/141 pass, `ruff` is clean, and `fs1` is identical before and after the Day 4 refactor on all 8 folds. The exclusion counts match the proposal and remove no categorical level.
- **INC-0004 not re-measured.** Reading the researcher process's launch arguments was denied by the permission classifier, and I did not pursue it.

Files are in /home/user/prc-data-challenge-2026/research/day-04/advisor:
- H018_review_v1.md
- H019_review_v1.md
- H020_review_v1.md

```yaml
schema: advisor-task-result-v1
exchange_id: X-D04-S01-0001
status: COMPLETE
decisions:
  - proposal_id: H018
    proposal_sha256: 2234bfb839a0ba2eaefe1e55ee2a63353d07c5b4f24abb9aced98886b8af485c
    decision: REVISE
    review_path: research/day-04/advisor/H018_review_v1.md
    review_sha256: 223da8d9dca4fe1a3d7ccb84a0e389edf4118de1eb3a526d1ac7b3d0da72d280
  - proposal_id: H019
    proposal_sha256: 0d2535d466bf00ff28a5004fb0168aa6a8b1bb461b0a62502d5b60716e2bef0c
    decision: REVISE
    review_path: research/day-04/advisor/H019_review_v1.md
    review_sha256: 701e7b23df645f94d4a61d8f3207967fdf1ca19b414f87f0e55977886e2dc396
  - proposal_id: H020
    proposal_sha256: 174102191673a5f2343c74bbad3df65f4a27e96e550749deed797b3aad986ff1
    decision: REJECT
    review_path: research/day-04/advisor/H020_review_v1.md
    review_sha256: 4de9e54f564e7b83e0fc1e5a3592a7fd6db8eba5036eb41492052abd203ee8c8
completed_utc: 2026-09-30T17:17:48Z
```
