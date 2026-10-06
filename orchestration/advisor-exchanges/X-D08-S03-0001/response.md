## Advisor result: X-D08-S03-0001, H038 v1

**Decision: REVISE (0.82).** H038 v1 cannot run as written. Nothing is authorized, so there is no E051/E052 allocation and no launcher run. The two rulings the envelope asked for are made now and bind v2.

The candidate itself is sound:
- **No leakage.** p, g and c use training rows only, and validation labels are never computed.
- **Parameters fixed in advance.** They were committed at `9f653a9`, before the design-month pilot.
- **Exact isolation off the subgroup**, enforced by an integrity check.
- **Deterministic and cheap.**

It cannot run as written for three reasons the Advisor cannot fix on the researcher's behalf:
1. **Rule 8 is not met.** There is no per-fold tail or bulk expectation for the subgroup against E046, and no S1 statement at July's rate. The S1 point matters most here: p learns the training months' convention rate, and July's is the lowest in 2025.
2. **Criterion 4 cannot fail when the stated claim fails.** The research question says the gain is "carried by the convention rows". Reading (a) only asks that the convention rows' SSE change be negative, at any share. A gain sitting on non-convention rows with large `d_sched` would pass it.
3. **The G5 (c) footprint is understated in three places.**
   - Day 1 (c)'s row table names subgroup rows in W1, S1 and R2. The row v1 cites, 192622644, is NM-present and outside the subgroup.
   - E046's analysis (c) is row-level for W1.
   - The tracked record names 14 subgroup validation rows across all five development folds.

**Ruling on INC-0020 (G10): not a breach of G1–G3, and no recovery review is triggered.**
- The disclosure (2026-10-04T22:35Z) came before the reopening and before G1–G3 existed.
- The figure appears only in three Day 7 texts written before G3. No Day 8 record repeats it, and v1 uses no board content.
- It falsifies a premise of X-D08-S01-0001 without changing that decision. That review's only isolation trigger was a figure for E050, and this was another team's figure.
- Conditions:
  - the disclosure lines stand in every record, the final report and the external evaluation, which also notes that the Advisor's context received the figure in this exchange;
  - the figure is never repeated or used;
  - any sign that a figure for the project's own files was seen triggers G10 at once.
- INC-0020 may close when the H038 v1 acknowledgement records this ruling.

**Ruling on G5 (c): no fold is stripped outright; confirmatory weight is conditional.**
- Neither prong strips a fold. The design's own analysis read design months only, its use of earlier records is aggregate, and no recorded contrast is re-measured.
- Because the record names 14 subgroup validation rows at row level ("known rows", listed in the review), a fold's WIN carries confirmatory weight only if it is still a WIN when the candidate's predictions on that fold's known rows are reverted to E046's.
  - The reverted outcome uses the frozen bootstrap on the full fold.
  - The twin rule is applied to the reverted twin.
  - A frozen LOSS stays a LOSS.
- If S1's WIN or the third WIN fails this reading, G5's consequence applies: INCONCLUSIVE, never uploaded.
- Any v2 change motivated by row-level facts in the record strips the affected folds outright.

**Required for v2.** The model, parameters, folds, seeds and launcher logic all stay unchanged.
1. Rule 8 tail and bulk expectations per fold and twin, plus an S1 statement at July's rate.
2. A decisive convention-row reading for criterion 4, or a restated claim. Either way, the non-convention large-`d_sched` rows go under Alternative Explanations.
3. A footprint restated with corrections D8-C7 to D8-C9.
4. The known-row reading, in tooling committed before v2's envelope.
5. A tracked manifest for the component files (DATA_POLICY §3).
6. Restated probabilities under the ruling.

D8-C10 corrects journal entry E015, which calls row 200300302 a convention record; by Day 1's definition it is not one.

**Verification limits.**
- **Not run:** the full test suite, because `test_evaluator` reads development-fold truth frames, which the envelope forbids.
- **What passed:** the five synthetic mixture tests, and `ruff` on the changed files.
- **Data read:** from silver, four target-free columns only, to place the named rows by fold.
- **Not touched:** targets, December data, fits and leaderboard pages.

My prediction for v2 (same model): criteria 1–3 hold against E046 with P = 0.30, falling to 0.18 once the known-row reading is applied; promotion at the Day 8 phase close is 0.12.

Files:
- Review: `/home/rvindra/Projects/prc-data-challenge-2026/research/day-08/advisor/H038_review_v1.md`
- Acknowledgement to write (records the rulings and D8-C7 to D8-C10; authorizes nothing): `/home/rvindra/Projects/prc-data-challenge-2026/research/day-08/acks/H038_ack_v1.md`

```yaml
schema: advisor-task-result-v1
exchange_id: X-D08-S03-0001
status: COMPLETE
decisions:
  - proposal_id: H038
    proposal_sha256: 36747a9357e54fd36618908ae2eaa4daeccecbbe6d3230b1b22ec4244c3d68ad
    decision: REVISE
    review_path: research/day-08/advisor/H038_review_v1.md
    review_sha256: 60fc1cb960ec426ab778fa2062de89af7b0e05ccbaf4d4452e29e89636d5a684
completed_utc: 2026-10-06T19:44:19Z
```
