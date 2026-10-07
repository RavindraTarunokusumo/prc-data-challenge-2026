---
schema: advisor-review-v1
hypothesis_id: H038
proposal_version: 1
proposal_sha256: 36747a9357e54fd36618908ae2eaa4daeccecbbe6d3230b1b22ec4244c3d68ad
exchange_id: X-D08-S03-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.82
created_utc: 2026-10-06T19:42:56Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.82).** The candidate is sound, cheap, free of leakage and exactly isolated off the subgroup. v1 cannot run as written, for three reasons the Advisor cannot fix on the researcher's behalf:

1. **Rule 8 is not met.** v1 pre-registers no per-fold expectation for the subgroup's tail and bulk against E046, and no S1 statement at July's rate.
2. **Criterion 4 cannot fail when the stated claim fails.**
   - The research question says the gain is "carried by the convention rows".
   - Reading (a) only asks that the convention rows' SSE change be negative, at any share.
   - A gain that sits on non-convention rows with large `d_sched` passes it.
3. **The G5 (c) footprint is understated in three places** (D8-C7 to D8-C9).

**The two rulings the envelope asks for are made here. They bind v2.**
- **INC-0020 (G10):** not a breach of G1–G3. No recovery review is needed, and conditions are attached ((D)).
- **G5 (c):** no development fold loses confirmatory weight outright.
  - A fold's WIN carries weight only if it survives reverting the candidate to E046 on that fold's **known rows**.
  - The known rows are the 14 subgroup validation rows that the record already names at row level ((E)).

**What v1 gets right.**
- **Parameters were fixed before the pilot.** They were committed at `9f653a9`, the pilot script asserts design months only, and nothing was tuned.
- **The construction is exact off the subgroup,** with a strict integrity check. v1 reports a smoke test that fails on a one-row change.
- **The fits are deterministic,** so E052 is a determinism check (as D3-C4).
- **It is honest.** The footprint is declared, and so is the case in which the candidate would be INCONCLUSIVE by construction.
- **The caveats are frank:** the weak classifier, P1's near-tie with the convention component alone, and a pilot trained on three months.

**Verified here (read-only).**
- **Hashes.**
  - The proposal (`36747a93…`), the launcher (`903b5a48…`) and the params file (`b22c02c1…`) match the envelope.
  - The tree is clean at `3c23aab`.
  - The six frozen files match `config/frozen.json`.
  - `.claude/agents/advisor.md` is `30fff5dd…0d19`, as in `config/agents.yaml`.
- **Order of commits.**
  - The params file and `pilot_mixture_D08.py` are unchanged since `9f653a9` (19:09:36Z). The pilot output followed at `e310996` (19:15:30Z).
  - The only later change to `mixture.py` adds two diagnostic columns. The prediction formula is unchanged.
- **The launcher.**
  - Its diff against Day 7's pinned `run_window_2.sh` (`f76db6fa…`) is exactly what v1 lists: window arguments, queue, `mixture_check.py` in place of the route check, no start after a failure, branch `day-8`, UTC logging.
  - The start rule, deferral, never-kill and own-path checkpoints are unchanged.
- **The code.**
  - `convention_mixture` fits p on the subgroup's training rows and g on LIRF training rows with c = 0.
  - `gbm.lightgbm` trains on `role == "train"` rows only, with category vocabularies from those rows.
  - Validation labels are never computed; a test checks this.
  - `override_fitted` refuses a row-set mismatch.
  - `mixture_check.py` requires max |Δ| = 0 off the subgroup, and agreement with the components and the formula within 1e-6 s.
- **Tests and lint.**
  - The five synthetic tests in `tests/test_mixture.py` pass, and `ruff` is clean on the eight changed files.
  - **The full suite was not run.** `test_evaluator` reads development-fold truth frames, which the envelope forbids.
- **Stored predictions.** E046's eight prediction files match its manifest (SHA-256).
- **Ledgers.**
  - `experiments/ledger.jsonl` ends at E050.
  - The last `holdout_access` is at 2026-10-04T17:57:38Z.
  - Nothing has been allocated since `reopened`.
- **Figures.**
  - v1's draw-spread table recomputes exactly (0.48 / 0.25 / 0.09 / 0.27 / 0.60 / 0.34 / 1.35 s).
  - Its expectation table recomputes to 0.1 s.
- **Secrets.** No credential pattern appears in any file changed since `88cdb22`.

**What I did not do.**
- No target, block-time or December column was read.
- From silver I read four target-free columns only (`MVT_ID_mvt`, `ADEP_mvt`, whether `AOBT_3_flt` is null, `month`), to place the rows the record names by fold and population.
- No fit, run, score, allocation, holdout script or formatter.
- No challenge page, leaderboard or bucket.

**Exposure, disclosed.** The envelope lists INC-0018 (D7) and HANDOFF_D07, and both hold the disclosed leaderboard figure. I read them, so the figure has entered the Advisor's context in this exchange. It is not repeated here and not used.

## Scientific Validity

### (A) The mechanism and what the pilot shows

**The structure is right in principle.**
- Under squared loss, E[y | x] = P(c | x) · E[y | c = 1, x] + (1 − P(c | x)) · E[y | c = 0, x].
- By the label's definition, E[y | c = 1, x] is `d_sched` to within 120 s.
- g estimates E[y | c = 0, x] on every LIRF c = 0 training row, almost all of them NM-present. That choice of population is part of the intervention (Experimental Isolation).

**The pilot supports the structure more than the classifier.**
- P1's Brier score (0.251) is no better than a constant 0.5 (0.250). P2's is 0.243.
- In P1, the convention component alone comes within 1 % of the mixture's subgroup SSE (9.79 against 9.73 × 10⁹ s²).
- So the secondary classifier claim (the candidate below constant p on at least 3 of 5 folds) is unlikely to hold. v1 already makes it non-decisive, which is right.

**The per-row scaling does not describe how the folds will be decided.**
- The expectations assume the same effect on every subgroup row.
- The record shows heavy concentration:
  - the last subgroup contrast on these folds (E046 against E033) had top-10 shares of 0.72–0.97, and W1's top-1 share was 0.79;
  - from E046's analysis (c), one W1 row holds 0.32 of E046's whole W1 SSE (350.59 s with it, 288.29 s without).
- The folds' dominant subgroup rows sit at the top of the `d_sched` range. There, p comes from one or two classifier leaves of at least 20 training rows each.
- Day 1 (c) already shows that day-scale subgroup rows are not all convention records: its "exception" row has y and `d_sched` hours apart.
- The development outcome therefore turns on p in a region that the three-month pilot barely samples. It is also measured against an E045 that saw 8–10 months of day-scale rows.
- **"Up to 36 hours"** matches the 2025 subgroup maximum of `d_sched` (131,163 s; target-free, from the H035 review). At that scale, the identity y = `d_sched` is evidenced in the record by one row only, W1's ((E)).

### (B) Rule 8 (standing): not met

Rule 8 has three parts. v1 meets the first two:
- it names the mechanism (the convention);
- it labels `d_sched` T.

It misses the third: the expected effect **separately on the tail and the bulk** of the subpopulation, with an **S1 expectation in view of July's low tail rate**.
- v1 has only criterion 8's bulk statistic against E033 ("values below E046's"). There is no tail expectation against E046 and no S1 statement.
- **The S1 statement matters more here than it did for H035:**
  - p learns the training months' convention rate (about 0.46–0.49 in the pilot months);
  - July's tail rate is the lowest of 2025 (0.35);
  - S1 has the most subgroup bulk rows (218 of 337);
  - E046's S1 bulk cost is already the largest (+4,292 s against E033).
- H035 v1 met this item. These are the researcher's predictions, so the Advisor cannot supply them (Revision 1).

### (C) Criterion 4: the falsification test does not test the stated claim

- **The claim.** The research question says the gain is "carried by the convention rows". The mechanism section says it "must appear on the convention rows".
- **What reading (a) tests.** It requires `subgroup_sse_change_convention` < 0 on every fold whose subgroup change is negative. It passes at any share: 5 % of the gain on convention rows and 95 % elsewhere would pass.
- **Why that gap matters.**
  - On convention rows, the mixture's error is about (1 − p)(g − `d_sched`).
  - On non-convention rows with large `d_sched`, raising the prediction toward `d_sched` lowers the error whenever y lies above the reference's prediction. That has nothing to do with the convention.
  - Rows of that kind are in this population. Day 1 (c)'s exception is one, and D8-C10 corrects a journal entry that called another one a "convention record".
- **The ablations do not close it.** Constant p, the convention component alone and g alone are reported, but none is a decision rule for the convention attribution.
- **What v2 needs:** a reading that can fail when the convention rows do not carry the gain, or a restated claim (Revision 2). The operationalisation and any threshold are the researcher's to choose.

### (D) Ruling on INC-0020 (G10)

1. **It is not a breach of G1–G3, so G10's recovery review is not triggered.**
   - The figure was disclosed at 2026-10-04T22:35Z (INC-0018 (D7)). That is before the reopening, and before X-D08-S01-0001 (09:51Z on 2026-10-05) created G1–G3.
   - At `3c23aab`, the figure appears only in three Day 7-lineage texts, all written before G3:
     - INC-0018 (D7);
     - HANDOFF_D07;
     - the Day 7 section of UPLOAD_RECORD.
   - No Day 8 record repeats it or relates any figure to it.
   - v1 cites INC-0017 as the reason for the phase. It does not quote the target and uses no board content.
2. **It falsifies a premise of X-D08-S01-0001, but it would not have changed that decision.**
   - That review already doubted "No score yet" (finding 5).
   - Its only isolation trigger was a figure for **E050** (G1 (b)). The disclosed figure is another team's.
   - INC-0020 does settle part of G1 (b):
     - board content was viewed after FROZEN and before the reopening;
     - the owner's target was set after that, so it may rest on board content.

     G3 already bars the target from every decision.
   - Whether any figure for the project's own file has been seen remains unrecorded, because G1 was waived.
3. **It has no bearing on H038's substance.**
   - The mixture form has been on record since Day 2 (H009 v1–v3).
   - It was agenda item 2 of PHASE_OPEN_D08_v1. That proposal was written by a cloud session whose branch lacked the Day 7 post-freeze commits.
   - Its parameters were fixed before the pilot.
   - A score level on the test months cannot rank one development-fold design above another.
   - **The live channel is motivational.** A threshold target rewards variance (X-D08-S01-0001 (a)), and H038 deepens the U6 bet. G3, G5 and the default of no new upload remain the defences.
4. **Conditions, binding on Days 8–12.**
   - **Disclosure.**
     - INC-0020's disclosure line stands beside INC-0017's in every Day 8–12 record and in the final report's Days 8–12 section (G8).
     - The external evaluation (G2) records that a leaderboard figure entered the researcher's context on 2026-10-04 and the Advisor's on 2026-10-06, in this exchange.
   - **The figure is not repeated.**
     - It appears in no new record, envelope, proposal, message or worker prompt.
     - The Day 7 files that hold it stay unedited.
     - Proposal-review envelopes cite INC-0020 rather than list those files, unless a ruling needs them.
   - **It is not used.** No proposal, expectation, criterion, threshold, stopping rule or upload decision may refer to it (G2, G3).
   - **The G10 trigger.** If any record or statement shows that a figure for one of the project's own files was seen or relayed, G10 applies at once: an incident, a recovery review, and no upload until it rules.
   - **Closure.** INC-0020 may close when the H038 v1 acknowledgement records this ruling.

### (E) Ruling on G5 (c): confirmatory weight per development fold

**(i) Prong 2 (a contrast already recorded): not engaged.** No record holds the mixture, the convention component, or a fitted p against E045 or E046 on these folds.

**(ii) Prong 1 (row-level reads by the design): no fold is stripped outright.**
- The design's own analysis read design months only.
- What it takes from earlier records is segment- or fold-level:
  - Day 1 (c)'s convention rate and definition, which X-D08-S01-0001 (d) classes as legitimate aggregate analysis;
  - E046's criterion 8 statistic and tail shares;
  - HANDOFF_D07 §2.

**(iii) The footprint is wider than v1 states.**
- **Day 1 (c)'s row table** names three rows of this population, in W1, S1 and R2. Row 192622644, which v1 cites, is NM-present and outside the subgroup.
- **E046's analysis (c), with `E046_vs_E033.json`,** gives W1's decisive row at row level: its target, its `d_sched`, E046's prediction there, and W1 without it.
- **The tracked record at `3c23aab` names 14 subgroup validation rows across all five development folds.** Most are rule 6 dominant rows from the Day 1–3 comparisons. v1 states that they are in the researcher's context.
- **The candidate's effect concentrates on rows of exactly this kind** (rule 6). The cluster bootstrap cannot see whether a WIN rests on them.

**(iv) Consequence, pre-registered now.**

*Known rows.* These are the LIRF NM-missing validation rows of the development folds whose `MVT_ID` appears in any tracked file at `3c23aab`. They were located with target-free columns only.

| Fold (twin) | Known rows | Where the record holds them | Reference prediction in the record |
|---|---|---|---|
| R1 | 196123310, 196129531 | Day 2–3 comparison files | no |
| R2 | 198934338, 198939290, 198939422, 198941714 | Day 1 (c); Day 1–3 comparison files | no |
| R3 | 200297323, 200300302 | Day 2–3 comparison files | yes for 200300302, through E045 = E020 |
| S1 (S1c) | 192615553, 192615662, 192621162, 192626268, 192628959 | Day 1 (c); Day 1–3 comparison files | no |
| W1 (W1c) | 183903219 | Day 1 (c); H035 U8 (c); E046 analysis (c); 24 comparison files | yes (`E046_vs_E033.json`) |

*Reading.* For each development fold and twin, the candidate's predictions on that fold's known rows are set equal to E046's. The fold outcome against E046 is then recomputed with the frozen bootstrap on the full fold. The population does not change.

*Rules.*
- A WIN carries confirmatory weight only if it remains a WIN under this reading.
- The twin rule is applied to the reverted twin.
- If S1's WIN, or the third WIN of criterion 2, lacks weight under this reading, G5's consequence applies: an objection of objection F's type; INCONCLUSIVE; never uploaded.
- A LOSS in the frozen computation stays a LOSS. The reading cannot rescue it.
- Criteria 1 and 3 are read as frozen.

The reading changes no fold outcome, criterion or population. It rules only on confirmatory weight, as G5 (c) delegates to this review.

**(v) Later changes.**
- A change in v2 that is motivated by row-level facts in the record, including those this review names, extends the footprint. It strips the affected folds outright.
- The revisions required below change no model component.

### (F) G9 item 2 and forward exposure

- **G9's notes are respected.** v1 is judged against E046, aims at development RMSE, and does not argue from 2026 downside.
- **It reverses PHASE_OPEN_D08_v1's framing.** The phase-open proposal framed item 2 as "a mechanism that lowers the downside"; H038 deepens the U6 bet instead. That is admissible, and v1 says so plainly.
- **Where the extra exposure lies.** The exposure beyond E046's sits on the largest-`d_sched` rows. There the convention component is unbounded, while E045's leaves are bounded by its training targets.
  - July 2026's subgroup maximum `d_sched` is 111,654 s.
  - January 2026 has the heaviest subgroup delay tail on record (q90 17,816 s; D7-C7).
- **Required of a SUBMIT proposal, if one follows.** Before any upload decision, it carries the target-free per-ranking-month exposure of U8 (b)'s type: Σ(candidate − E050)² on the subgroup, with its top-1 and top-10 shares. It is named here so that it is pre-registered.

## Novelty Relative to Existing Research

- **Not redundant.**
  - The mixture form has been written down since Day 2 (H009 v1–v3: "roughly p · `d_sched` + (1 − p) · (normal taxi time)"), and it recurs in H015 and H016.
  - The trees of Days 2–7 learned it only implicitly.
  - No experiment fits a convention classifier or uses `d_sched` as a prediction component. Under rule 10 this is a new configuration.
- **It finally runs the convention split.** The H035 review and X-D08-S01-0001 named that split, and it has not been done. `mixture_analysis.py` computes it (`subgroup_sse_change_convention`), which is a genuine gain for the record.

## Experimental Isolation

- **Off the subgroup, the change is exact.** The mixture check passes only at max |Δ| = 0, and rule R holds: E046 is the matched reference.
- **On the subgroup, three things change at once:**
  - the structure: an explicit mixture instead of a direct fit;
  - the training populations: p on subgroup rows, g on LIRF c = 0 rows, against E045 on all rows at every airport;
  - the parameters, all set a priori.
- **What the ablations separate, and what they leave open.**
  - The stored-component ablations separate the classifier from the structure.
  - Nothing separates the structure from g's LIRF-only training population.
  - On convention rows that matters little: the mixture's error there is about (1 − p)(g − `d_sched`). A decisive convention-row reading (Revision 2) therefore attributes a convention-row gain to the `d_sched` component.
  - A gain on non-convention rows stays unattributed (Missing Control).
- **Rules 13 and 14.**
  - No stochastic component is added.
  - LightGBM runs deterministically with no subsampling, so the seed is not used.
  - E052 is therefore a determinism check.

## Validation Quality

- **The frozen folds are used unchanged:**
  - R1–W1 and the twins, with S1 required to WIN;
  - no H fold (H8);
  - the reference is E046;
  - criterion 8 is read against E033 and E028 (ruling B).
- **G5 (a):** E051 is the first Day 8–12 look and E052 the second. The baseline of 44 is correct.
- **G5 (b):** the spread verifies. On the subgroup, E046's draw analogues are identical, because E045 is deterministic and E047 is byte-identical. The subgroup spread is therefore 0.
- **G5 (c):** ruled in (E). v1's case of "S1 removed" does not arise. S1 keeps confirmatory weight, subject to the known-row reading.
- **Expectations.**
  - The arithmetic verifies.
  - The construction ignores the recorded concentration: W1's −2 to −6 s cannot describe a fold whose subgroup SSE is a third one row.
  - Under (E), the probabilities for criteria 1–3 need restating (Revision 6).
- **Twins.** W1c trains on January only (60 subgroup rows), so its classifier has at most 3 leaves.
- **Manifest gap.**
  - The component files (`predictions/validation/<EID>/components/`) are git-ignored, and no tracked manifest lists them.
  - Criterion 4 and the integrity check rest on them, so DATA_POLICY §3 requires one (Revision 5).

## Leakage Review

### Target Leakage

PASS

- **c** is computed from y on training rows only. Validation rows are masked, and a test checks that their label is never true.
- **p and g** are fitted on the fold's `role == "train"` rows only.
- **The 120 s tolerance** is Day 1's constant, taken from segment aggregates over January–November; its derivation is unrecorded.
  - In the pilot, the RMSE of |y − `d_sched`| on convention rows is 3–7 s, far inside 120 s.
  - So the labels are insensitive to the tolerance, and no sensitivity run is needed.

### Temporal Leakage

CONCERN

Not blocking.
- **`d_sched` is label T:** it uses the row's own takeoff time.
  - It is admissible for ranking rows (DATASET_AUDIT §6.2).
  - It falls outside the causal-only variant (rule 8).
- **The remaining risk is design-level fold leakage,** ruled in (E).

### Competition Availability

CONCERN

Not blocking.
- **Inputs:** every input exists for ranking DEP rows. There are 107 subgroup rows in January 2026 and 276 in July 2026.
- **The 2026 convention rate cannot be observed** (U6).
- **January 2026 carries the largest stakes.** Its subgroup delay tail lies above every 2025 month, so an unbounded convention component carries the largest per-row stakes there, in both directions.
- **INC-0020:** ruled in (D).

## Compute Review

### RAM

PASS

- The FS2 build dominates, as in E045 (5.38 GB peak). The component fits are smaller.
- The CLASS-M target is 8 GB and the hard limit 11 GB. The laptop has 10 GiB of RAM plus 4 GiB of swap.

### Runtime

PASS

- E045 took 92–190 s per development fold, including a 1,000-round fit on all rows. Here g fits LIRF rows only.
- The pilot took 72–75 s per split.
- 1,500 s pessimistic per run is within the CLASS-M target and the 2,700 s timeout.
- The window needs at least about 3,000 s plus the checks.

### Disk

PASS

- About 30 MB: seven prediction files and seven component files per run, plus a JSON.

## Weakest Assumption

**That the pilot's gain carries over to the development folds.** The pilot trained on three months against a direct model that was also trained on three months. The folds differ in three ways:
- **A few rows decide them.** Their outcomes are set by a few dozen rows at the top of the `d_sched` range.
- **p is thinly estimated there.** It comes from one or two classifier leaves trained on a handful of day-scale rows of mixed convention status.
- **The reference is stronger.** E045 has seen two to three times as many training months as the pilot's direct model.

If p is low at the top of the range, two things follow:
- the mixture under-predicts the one recorded 36-hour convention row;
- it over-weights the normal component on day-scale rows that are not convention records.

The pilot cannot show either.

## Missing Control or Ablation

- **Required:**
  - a decisive convention-row reading (Revision 2);
  - the known-row reading of (E), implemented before the run (Revision 4).
- **Named, not required if Revision 2 is decisive:** a direct LightGBM on LIRF training rows with E045's parameters. It would separate g's training population from the structure.
- **Not needed:** a tolerance sensitivity run (Target Leakage).

## Decision

REVISE

## Execution Authorization

Authorized scope:
- **None.** REVISE never permits execution.
- No `gate.py allocate` for H038 v1, no E051 or E052, no launcher run, and no fit or score on any development fold.

Required acknowledgement path:
- **`research/day-08/acks/H038_ack_v1.md`.**
  - It records both hashes, the INC-0020 ruling (D) and the G5 (c) ruling (E), with the known-row table in full.
  - It appends D8-C7 to D8-C10.
  - It authorizes nothing. INC-0020 may close on it.
- **After an ACCEPT of v2:** `research/day-08/acks/H038_ack_v2.md`.

**Corrections** (appended in the v1 acknowledgement; no proposal is edited):
- **D8-C7. Day 1 (c)'s rows.** The dominant-row table of Day 1 (c) names three subgroup rows: 183903219 (W1), 192628959 (S1) and 198941714 (R2). Row 192622644, which H038 v1 cites, is NM-present and outside the subgroup.
- **D8-C8. E046's analysis is also row-level.**
  - It is not only fold × segment aggregates.
  - Its section (c), together with `E046_vs_E033.json`, holds W1's row 183903219 at row level: its target, its `d_sched`, E046's prediction, and W1 without the row.
- **D8-C9. The record's row-level subgroup rows.**
  - The tracked record at `3c23aab` names 14 subgroup validation rows on all five development folds (listed in (E)).
  - H038 v1's "D5-C10 and the Day 7 rule 6 / U8 row audits: S1, W1 and others" understates this.
- **D8-C10. Journal, E015.**
  - The entry calls 200300302 one of the "day-scale LIRF convention records".
  - By Day 1's definition it is not one: its recorded target and its `d_sched` differ by hours (Day 2–3 comparison files).

## Revision

Six changes are required for v2. They are minimal: the model, its parameters, the folds, the seeds and the launcher's run logic all stay as they are.

1. **Rule 8.** For each development fold and twin, pre-register:
   - the expected effect against E046 on the subgroup's tail and on its bulk, separately: direction and rough size, stating the band or label used;
   - an S1 statement at July's rate, which is below the training rate that p learns.
2. **Criterion 4.** Do one of the following:
   - pre-register a convention-row reading that fails when the convention rows do not carry the subgroup's gain, with its consequence (the operationalisation and threshold are yours);
   - restate the research question and the claim so that reading (a), as written, tests them.

   In either case, list "non-convention rows with large `d_sched`" under Alternative Explanations, and state how the reading separates them.
3. **Footprint.** Restate rule 15 (c) with D8-C7 to D8-C9, and state whether the design used any of the 14 known rows.
4. **The known-row reading of (E).**
   - Implement it in tooling committed before v2's envelope, so that it falls under the freeze.
   - Per fold and twin, it reports:
     - the frozen outcome and the reverted outcome;
     - the known rows' share of the subgroup SSE change;
     - the verdict on confirmatory weight.
5. **Component files.** Cover them with a tracked manifest (path, size, SHA-256). One way is to have the integrity check, which the launcher already commits, record them.
6. **Restated probabilities.** Give probabilities for:
   - criteria 1–3 against E046;
   - each fold's WIN surviving the known-row reading;
   - G5's consequence.

   W1's expectation must be consistent with its recorded row concentration.

**Binding on v2:** the rulings in (D) and (E), and (F)'s exposure requirement for the SUBMIT stage.

**Not required:** any change to p, g, the tolerance, the folds or the queue.

## Advisor Prediction

Probability of improvement (v2 as required, with the same model):

| Event | P |
|---|---|
| Mixture check PASS on all 7 folds | 0.95 |
| E052 byte-identical to E051 | 0.95 |
| Development-mean ΔRMSE against E046 < 0 | 0.60 |
| Criteria 1–3 against E046 hold (frozen computation) | 0.30 |
| … and S1 plus a third WIN survive the known-row reading | 0.18 |
| S1 WIN | 0.45 |
| At least one development-fold LOSS (W1 or R3 most likely) | 0.30 |
| The criterion 8 rule holds against E033 and E028 | 0.90 |
| The classifier beats constant p on at least 3 of 5 folds | 0.30 |
| Promoted at the Day 8 phase close | 0.12 |

Expected magnitude:
- **Development mean against E046:** central −3 s; 80 % interval −15 to +8 s.
- **W1:** decided by one recorded row. Its ΔRMSE can be tens of seconds of either sign, set by p on that row.
- **R3:** similar, with smaller stakes.
- **S1:** −20 to +12 s.
- **The known-row reading** removes most of W1's and R3's movement.
- No leaderboard figure, and no expectation of one, is given (G3).

Primary expected failure mode:
- **Primary: a few recorded rows decide the folds.** The fold outcomes are set by p at the top of the `d_sched` range. The result is either a LOSS on W1 or R3, or WINs that do not survive the known-row reading. Either way the candidate is INCONCLUSIVE under G5.
- **Secondary: S1.** At July's lower convention rate, S1's subgroup bulk rows turn S1 into a TIE or LOSS.
- **Tertiary: the gain is not the convention.** It sits mostly on non-convention rows, and a decisive criterion 4 fails.
