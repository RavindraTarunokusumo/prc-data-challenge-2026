# Acknowledgement: H038 v1 (exchange X-D08-S03-0001)

*Written 2026-10-06T19:48:02Z (measured with `date -u`).*

- **Proposal:** `research/day-08/proposals/H038_v1.md`, SHA-256 `36747a9357e54fd36618908ae2eaa4daeccecbbe6d3230b1b22ec4244c3d68ad`.
- **Review:** `research/day-08/advisor/H038_review_v1.md`, SHA-256 `60fc1cb960ec426ab778fa2062de89af7b0e05ccbaf4d4452e29e89636d5a684`.
- **Decision received: REVISE (0.82).** The researcher verified both hashes at 2026-10-06T19:46Z.
- **Mirror:** `orchestration/advisor-exchanges/X-D08-S03-0001/` (`envelope.yaml`, `response.md` verbatim, `checksums.sha256`).
- **This acknowledgement authorizes nothing.** No E051 or E052 is allocated, and no launcher runs. H038 v2 follows.

## Ruling (D): INC-0020 under G10, adopted as binding

- **Not a breach of G1–G3.** No recovery review is triggered. The disclosure (2026-10-04T22:35Z) came before the reopening and before G1–G3 existed.
- **It falsifies a premise of X-D08-S01-0001 without changing that decision.**
- **INC-0020 also settles part of G1 (b):**
  - board content was viewed after FROZEN and before the reopening;
  - the owner's target was set after that.
- **Conditions, binding on Days 8–12:**
  - **Disclosure.**
    - INC-0020's disclosure line stands beside INC-0017's in every Day 8–12 record and in the final report's Days 8–12 section.
    - The external evaluation records that a leaderboard figure entered the researcher's context on 2026-10-04 and the Advisor's on 2026-10-06 (this exchange).
  - **The figure is not repeated** in any new record, envelope, proposal, message or worker prompt. The Day 7 files that hold it stay unedited. Envelopes cite INC-0020 rather than list those files, unless a ruling needs them.
  - **It is not used** by any proposal, expectation, criterion, threshold, stopping rule or upload decision.
  - **The G10 trigger.** Any sign that a figure for one of the project's own files was seen or relayed means: an incident, a recovery review, and no upload until it rules.
- **INC-0020 closes with this acknowledgement** (resolution appended to the incident).

## Ruling (E): G5 (c), adopted as binding

- **No development fold loses confirmatory weight outright.** Neither prong is engaged: the design's own analysis read design months only, its use of earlier records is aggregate, and no recorded contrast is re-measured.
- **The known rows.** These are the LIRF NM-missing validation rows of the development folds whose MVT_ID appears in a tracked file at `3c23aab`:

  | Fold (twin) | Known rows | Where the record holds them | Reference prediction in the record |
  |---|---|---|---|
  | R1 | 196123310, 196129531 | Day 2–3 comparison files | no |
  | R2 | 198934338, 198939290, 198939422, 198941714 | Day 1 (c); Day 1–3 comparison files | no |
  | R3 | 200297323, 200300302 | Day 2–3 comparison files | yes for 200300302, through E045 = E020 |
  | S1 (S1c) | 192615553, 192615662, 192621162, 192626268, 192628959 | Day 1 (c); Day 1–3 comparison files | no |
  | W1 (W1c) | 183903219 | Day 1 (c); H035 U8 (c); E046 analysis (c); 24 comparison files | yes (`E046_vs_E033.json`) |

- **The reading.** For each development fold and twin, the candidate's predictions on that fold's known rows are set equal to E046's. The fold outcome against E046 is then recomputed with the frozen bootstrap on the full fold. The population does not change.
- **The rules.**
  - A WIN carries confirmatory weight only if it remains a WIN under this reading.
  - The twin rule is applied to the reverted twin.
  - If S1's WIN, or the third WIN of criterion 2, lacks weight, G5's consequence applies: an objection of objection F's type; INCONCLUSIVE; never uploaded.
  - A frozen LOSS stays a LOSS.
  - Criteria 1 and 3 are read as frozen.
- **Later changes.** A v2 change motivated by row-level facts in the record strips the affected folds outright.
- **Implementation:** `scripts/known_row_check.py` (committed at `a977bef`, before v2's envelope; synthetic test `tests/test_known_rows.py`).

## (F): the exposure requirement for a SUBMIT proposal, recorded

If a SUBMIT proposal follows, it carries, before any upload decision, the target-free per-ranking-month exposure of U8 (b)'s type: Σ(candidate − E050)² on the subgroup, with its top-1 and top-10 shares.

## Corrections (appended; no proposal is edited)

- **D8-C7. Day 1 (c)'s rows.**
  - The dominant-row table of Day 1 (c) names three subgroup rows: 183903219 (W1), 192628959 (S1) and 198941714 (R2).
  - Row 192622644, which H038 v1 cites, is NM-present and outside the subgroup.
- **D8-C8. E046's analysis is also row-level.**
  - It is not only fold × segment aggregates.
  - Its section (c), with `E046_vs_E033.json`, holds W1's row 183903219 at row level: its target, its `d_sched`, E046's prediction there, and W1 without it.
- **D8-C9. The record's row-level subgroup rows.**
  - The tracked record at `3c23aab` names 14 subgroup validation rows across all five development folds (the table above).
  - H038 v1's "D5-C10 and the Day 7 rule 6 / U8 row audits: S1, W1 and others" understates this.
- **D8-C10. Journal, E015.**
  - The entry calls 200300302 one of the "day-scale LIRF convention records".
  - By Day 1's definition it is not one: its recorded target and its `d_sched` differ by hours.

## Revisions for v2 (all six adopted)

1. Rule 8: tail and bulk expectations per fold and twin, and an S1 statement at July's rate.
2. Criterion 4: a decisive convention-row reading. Non-convention rows with large `d_sched` go under Alternative Explanations.
3. The footprint restated with D8-C7 to D8-C9, stating whether the design used any known row.
4. The known-row reading in tooling committed before v2's envelope (done: `a977bef`).
5. A tracked manifest for the component files (done: `mixture_check.py` records path, size and SHA-256, and the launcher commits its JSON; `a977bef`).
6. Restated probabilities under the ruling.

**Unchanged:** the model, its parameters, the folds, the seeds and the launcher's run logic.
