---
schema: advisor-review-v1
hypothesis_id: PHASE_CLOSE_D08
proposal_version: 1
proposal_sha256: 501a5881d1beba663ff54f85fe16343a67b3d1d56f2ca27e5ea5aa2b637d4a19
exchange_id: X-D08-S03-0004
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-10-07T22:07:00Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.85), with binding conditions Q1–Q8 and corrections D8-C17 to D8-C22.** The three Day 8 decisions stand. The holdout and upload statements are verified. No Day 8 reading may motivate a promotable Day 9 candidate (Q5). `DAY_SUMMARY.md` is marked FINAL only once D8-C14 to D8-C22 are applied.

**What stands.**
- **E046 remains champion.** E051 fails criterion 2 as frozen: one WIN (R3), with S1 a TIE (q90 +11.50 s). The ledgers have no decision label for E051 or E052. Under H038 v2's own falsification criterion (criteria 1–3 against E046) and the project's precedent (E011, E023, E024: criterion 2 not met on an S1 TIE), **H038 v2 is REJECT** (Q1).
- **Weather is not pursued.** The pre-registered rule is not met, and the verdict is robust to the "too blunt" objection. No restricted variant reaches −1.0 s on all rows in both pilots, even with an oracle (target-defined) bulk restriction (finding 2).
- **Item 1 is closed with no lead.** The reading is the rule's own output. The note's last sentence claims more than the look shows (D8-C19).
- **H: closed (H8).** Verified below.
- **No Day 8 upload; E050 stands.** Its file's hash was recomputed and is unchanged.

**The adversarial result on the champion.** Nothing in Day 8 contradicts E046's promotion or its standing disclosures.
- The item 1 look finds LIRF's block-at-schedule tail share at 0.84 (bulk 0.25) in all four design months. That is consistent with Day 1's 83.3 %, so the U6 bet is unchanged.
- Day 8 does add one fact against E046's *optimality* on the development folds. E051's development mean is 20.10 s lower (q95 −2.98), carried mostly by three known rows.
- E046 therefore stands by the frozen rules' asymmetry, not because it was shown better. The records must not imply that E051 is the worse subgroup predictor (Weakest Assumption). This changes no decision.

**What this review adds: seven findings, all settled by conditions and corrections.**

1. **The reverted known-row reading is weaker than presented, and one sign is misread (D8-C18).**
   - Credited in full, the reverted computation still fails criterion 2: 2 WINs of 5, with a minimum of 3.
   - Its R1 and S1 WINs arise because reversion deletes the candidate's own losses on those folds' known rows: +4.2 × 10⁸ and +5.5 × 10⁸ s².
   - On R2, the known rows *favour* the candidate. Reverting them moves R2 to +3.90 s with q10 −0.08 s, a hair from LOSS. The E051 analysis says the opposite ("on R1, R2 and S1, the known rows go against the candidate").
   - The reading is not evidence that "the structure may be right". The proposal's "case against" 5 should be stated more strongly in the other direction.
2. **The weather objection "the rule is too blunt" fails on the pilot's own numbers.** If only one segment takes the candidate's predictions, the all-rows change is:

   | Segment that takes the candidate | P1 (June) | P2 (May) |
   |---|---|---|
   | Bulk rows (y < 3,600 s; oracle, not implementable) | −0.91 s | −0.80 s |
   | NM-present rows (an implementable proxy) | +0.17 s | −0.63 s |
   | EHAM only | −0.61 s | −0.36 s |
   | The four airports that gained in both pilots (selected in-sample) | −1.28 s | −0.59 s |

   No restriction clears −1.0 s in both pilots, so the "bulk-only" reading is not a lead (D8-C20).
3. **"A snow mechanism cannot be learned on any fold" is wrong as stated (D8-C17).**
   - R1–R3, S1 and S1c all train on February and March 2025, which hold 270 LTFM snow reports.
   - What is true: no fold can both learn a snow effect and be scored on one. The conclusion for criterion 2 is unchanged.
4. **The item 1 look's count and closing sentence (D8-C19).**
   - It tested 18 signatures, not 15.
   - Its ratio test is vacuous for the hour- and day-shift signatures. A block time recorded k hours early forces the row into the tail, so the bulk share is about 0 by construction.
   - Pooled across the nine airports, "block 1 h before AOBT_3" covers 30 of the 554 non-LIRF tail rows. Even if those rows were identified perfectly, the stake is about 0.8 s of all-rows RMSE, and no input flags them. "No lead" stands.
   - The note's "looks like real long taxi-outs" goes beyond what was tested.
5. **The E051 record has gaps (D8-C21).**
   - There is no decision label.
   - `range_check.py E051` was pre-registered, but no output was recorded.
   - The G5 (b) mechanism-population ΔRMSE is not tabulated.
6. **Governance (Q3, Q4, Q7).**
   - Two owner answers to numbered options are recorded, but the options are not. If an option was a research item, G3 makes the choice an incident.
   - INC-0019's closure needs the owner's words.
   - INC-0018 (D7) is omitted. Its own closure condition has been met.
   - D8-C15 has not yet been told to the owner.
7. **My own exposure, stated plainly (Q8).**
   - To rule on INC-0018 (D7)'s status, I opened that file. It holds the leaderboard figure disclosed on 2026-10-04 (INC-0020). I had first tried to mask figures in the output, and the mask failed.
   - The Advisor's context therefore received the figure again in this exchange (first: X-D08-S03-0001, 2026-10-06).
   - It is not repeated here, and no ruling below uses it. It is another team's figure, not one of the project's own files, so ruling (D)'s G10 trigger does not apply.

**Verified here (read-only).**
- **Hashes and tree.**
  - The proposal is `501a5881…4a19`, as in the envelope.
  - The Advisor definition is `30fff5dd…0d19`, as in `config/agents.yaml`.
  - The six frozen files match `config/frozen.json`, and so do the SPLITS v2 proposal, review and acknowledgement.
  - The tree is clean at `0e09457`.
- **The H038 freeze held.** `git diff ce89aeb 7cb6ffd` is empty under `src`, `scripts`, `config`, `tests`, `pyproject.toml`, `uv.lock` and the launcher.
  - Code changed after the batch: the weather block, the two Day 8 scripts and `prc.features.NUMERIC`.
  - `NUMERIC` is used only as a membership filter (`features.columns`), so FS2's columns and their order are unchanged.
- **Holdout (H8).**
  - The task ledger's last `holdout_access` is 2026-10-04T17:57:38Z.
  - The last unmasking event is E050's, at 2026-10-04T22:01:39Z.
  - After the `reopened` event there are only the E051 and E052 allocations.
  - No E051 comparison file holds an H key. Each run's mixture check passes on H (88 rows) with no truth read.
- **Upload.**
  - `predictions/final/E050/submitting.parquet` is `f0dc2c7c…06e8`, recomputed here.
  - No commit has touched `models/` or `predictions/final/` since 2026-10-05.
  - `CURRENT.json` names E046.
- **Stored files.** The eight prediction files each of E046, E051 and E052 match their manifests.
- **E051's figures, from the comparison JSONs:**
  - fold outcomes and quantiles, the frozen mean −20.104 (q95 −2.98) and the reverted mean −3.71;
  - criterion 8 against E033 and E028 (worst: S1 +4,263.3 and +4,262.9 s);
  - the criterion 4 sign test on R1, R3, S1 and W1;
  - the rule 12 counts, the classifier AUCs, and `repro_E052_of_E051.json` (0.0 s on every fold).
- **Pre-registration order** (file times against commits):
  - weather: parameters and rule committed at `d506516` (19:32:01Z); then the parser fix `bdcbb83` (21:26:56Z); the table (21:27:03Z); the pilot outputs (21:34:05Z);
  - item 1 look: rule committed at `a37f95e` (21:41:44Z; script last written 0.4 s earlier); outputs at 21:41:52Z.
  - Both scripts and the parameters file are unchanged since their commits. The pilot JSON records the parameters' hash, `9cc6cb20…`, which matches.
- **The weather table rebuilds byte for byte.**
  - I ran `prc.weather.reports` on the hash-verified bronze files, with output to the session scratchpad, not the repository.
  - The result is SHA-256 `bf5c256d…6314`, 277,489 reports, equal to the stored table.
  - So `code_dirty: true` (D8-C16) has no effect on the pilot's input.
- **LTFM events recount exactly from bronze:** snow, fog, visibility < 0.5 mi, thunderstorms and ≤ 0 °C, for all 19 months.
- **Pilot JSON internal checks.**
  - Bulk plus tail SSE changes equal the all-rows change, and so do NM-missing plus NM-present.
  - Coverage is 1.0 at all ten airports.
- **Design months only.**
  - The pilot uses `masked_view` on folds made of design months only. Its truth join is filtered to the predicted design month.
  - The look filters to the design months and asserts it.
  - None of 2025-01, 04, 05 or 06 is a validation month of any fold, H included. G5 (a)'s count stays at 2.
- **Tests and lint.**
  - The 13 synthetic tests for weather (6), the mixture (5) and the known rows (2) pass. They were run without cache writes.
  - `ruff` is clean.
  - I did not run the full suite: `test_evaluator` reads development-fold truth.
- **Secrets.** No credential pattern appears in the diff since `7cb6ffd`. The run log names `WANDB_API_KEY` but not its value.

**What I did not do.**
- I read no target of any month, and no block-time column.
- No fit, run, allocation, holdout script or formatter.
- No challenge page, leaderboard or bucket.
- Apart from INC-0018 (D7) (finding 7), I did not open the Day 7 files that hold the disclosed figure.

## Scientific Validity

### (a) E051 (H038 v2): the reading and its label

- **The frozen reading is correct.** Criterion 2 needs ≥ 3 WINs among R1–W1, an S1 WIN and no LOSS (`config/splits.yaml`). E051 has one WIN, R3 (q90 −5.40).
  - R1: q90 +3.28.
  - S1: q90 +11.50.
  - W1: q90 +1.51 (a single row).
  - R2: TIE.
- **The label.** H038 v2's "Falsification Criterion" lists criteria 1–3 against E046 first, and criterion 2 fails.
  - The project has recorded this pattern as REJECT three times: E011 (S1 TIE), E023 ("mechanism supported", S1 TIE) and E024.
  - INCONCLUSIVE has been used for "not falsified" outcomes (E017) and for attribution failures (E006). Neither applies here.
  - So E051 is REJECT. E052, its reproduction, takes the same label, as E022, E034 and E048 did. Rule 10 then covers E051's configuration.
- **The classifier's AUC gap is a training-size effect, not a leak.**
  - The AUC rises with training months: W1c (1 month) 0.61, the pilots (3) 0.67–0.68, S1c (6) 0.78, the development folds (8–10) 0.84–0.93.
  - The code path is as audited in X-D08-S03-0002: c is computed from y on training rows only, and validation y is null.
  - The researcher's "miss" is real, but it has a benign explanation.

### (b) The reverted known-row reading ("case against" 5)

| | R1 | R2 | R3 | S1 | W1 | Mean |
|---|---|---|---|---|---|---|
| Frozen ΔRMSE (q10 / q90) | −3.88 (−10.98 / +3.28) TIE | +1.39 (−3.65 / +6.59) TIE | −30.38 (−47.51 / −5.40) WIN | −7.94 (−26.65 / +11.50) TIE | −59.72 (−122.92 / +1.51) TIE | −20.10 |
| Known rows' SSE change, candidate minus E046 (s²) | **+4.2e8** (candidate loses) | **−2.2e8** (candidate gains) | −2.5e9 (gains) | **+5.5e8** (loses) | −5.5e9 (gains) | |
| Reverted ΔRMSE (q10 / q90) | −8.10 (−13.66 / −1.97) WIN | +3.90 (**−0.08** / +8.08) TIE | −2.42 (−5.92 / **+0.15**) TIE | −11.50 (−21.39 / −0.67) WIN | −0.45 (−3.92 / +3.02) TIE | −3.71 |

- **The reverted computation fails criterion 2 by itself:** 2 WINs, against a minimum of 3. No computation on record passes the candidate.
- **The reversion edits both ways.**
  - It turns R1 and S1 into WINs by deleting the candidate's largest losses: real errors on real validation rows.
  - It removes R3's and W1's gains, and R2's gain on its known rows.
  - That leaves R2 0.08 s from a LOSS at q10, and R3 0.15 s from a WIN at q90.
  - What remains is fold heterogeneity, not a signal the bootstrap "cannot see".
- **The misreading.** The E051 analysis groups R2 with R1 and S1 as folds where "the known rows go against the candidate (negative shares)".
  - On R2, the fold total is a loss (+1.24e8 s²), so a negative share means the known rows favour the candidate.
  - The same sentence (D8-C18) appears, in substance, in DAY_SUMMARY §9.2 and the proposal's "case against" 5.
- **The reversion is a weight test, not an estimate.** DATA_POLICY §10 fixes the evaluation population. Ruling (E) uses the reversion only to remove confirmatory weight from WINs. Using it to credit TIEs would be a post-hoc population change (rule 10).

### (c) The weather pilot ("case against" 1–3)

- **The pre-registration is sound.**
  - The rule and the parameters (`d506516`) predate any weather table, because the first build failed with a ShapeError.
  - The later parser fix (`bdcbb83`) changed parsing only (VV layers and stripped sky codes) and matches the docstring's definition.
  - The table the pilot read is reproduced byte for byte by the committed code.
  - Even if an unrecorded earlier pilot run existed, it could not have shaped the rule.
- **"Too blunt" (case 2).** Finding 2's table settles it.
  - The bulk gain is real in both pilots, about 1.2 s of bulk RMSE. Diluted to all rows, it is −0.91 and −0.80 s, so it cannot reach criterion 1's −1.0 s minimum even before the tail's losses.
  - The implementable proxy (NM-present) is +0.17 s in P1.
  - The tail sets P1's sign (+2.33 s on all rows), as the proposal says. Ignoring the tail does not rescue the block.
  - The rule was the right bar for a feature block whose purpose is a criterion-1-sized gain.
- **One learner (case 1).** The pilot's learner is E045's configuration: exactly the model E046 uses on the subgroup, and the model family of E046's LightGBM half.
  - A CatBoost response could differ, but nothing suggests a larger effect.
  - FS2 already carries the departure runway and the realised NM taxi interval (`d_aobt3`, label T). That bounds what weather can add (D8-C15).
- **Four design months (case 3).** Correct, and it is the price of G5 (c). Reading any other month would cost the corresponding fold its weight.

### (d) LTFM coverage (D8-C17)

- **The recount from bronze is exact.** Snow reports: February 2025, 258 (12 days); March, 12; April, 2; December, 17; January 2026, 147 (9 days).
- **The statement is wrong; the conclusion holds.**
  - "No development fold can learn a snow or freezing effect from its training months" is false. R1, R2, R3, S1 and S1c all train on February and March (270 snow reports; 135 reports at or below 0 °C).
  - The correct statement: W1 and W1c are the only folds whose validation month has snow, and their training months hold 2 and 0 snow reports.
  - The folds that train on the snow months validate on snow-free months (July and September–November).
  - So no fold can both learn and score a snow effect, and a snow-only candidate cannot meet criterion 2.
- **Already covered for E046.** E046 uses no weather input. W1 already scores it on a snowy month without snow in training, which is the January 2026 situation without the SUBMIT fit's February months. No new disclosure is needed.

### (e) The item 1 look ("case against" 4)

- **The rule and its output agree.** `findings: []`, and LIRF's check reproduces Day 1 (0.84 against 0.25).
- **The count.** There are 18 signatures, not 15:
  - five anchor equalities, including Day 1's block = SCHED;
  - nine hour shifts;
  - two day shifts;
  - round hour;
  - repeated block.
- **The rule's power.**
  - For the shift signatures, "tail share ≥ 2 × bulk share" is automatic: a block recorded k hours before AOBT_3 gives y ≈ `d_aobt3` + k · 3,600 s. Only the 30-row floor bites.
  - Only EGLL, LFPG, EHAM and LTFM have 30 or more tail rows at all.
  - Pooled across the nine airports, "block 1 h before AOBT_3" has 30 tail rows (EGLL 16, EDDM 5, LFPG 5, EDDF 3, LTFM 1), and "1 h before EOBT_1" has 12.
  - With perfect identification, the 30 rows are worth about 30 × 3,600² / 697,338 ≈ 560 s² of MSE, roughly 0.8 s of all-rows RMSE.
  - BLOCK is withheld, and `d_aobt3` looks normal on such rows, so no input can flag them.
- **The reading "no lead" is robust.** "Looks like real long taxi-outs or unrecorded causes" is not: the look tested 18 signatures, not the nature of the remaining 554 tail rows.

### (f) The champion, adversarially

- **E046's promotion rests on development evidence plus one H WIN** (December, −124.24 s). Day 8 changes neither.
- **E051 shows that the subgroup predictor can be improved on the mean,** but not on folds that the frozen bootstrap can call.
- **Under H8, the mixture can never receive the out-of-sample check E046 had.** This asymmetry is the intended design of the governance, not a defect.
- **Forward risk.** E051 would have deepened E046's U6 bet. Not promoting it leaves the submission's forward exposure where Day 7 left it.

### (g) Days 9–12: the scientific bounds (request item 6)

**Neither Day 8 reading may motivate a promotable Day 9 candidate.**

1. **The E051 follow-ups, and every LIRF NM-missing subgroup mechanism.**
   - Ruled now under G5 (c), both limbs:
     - E051's records read every development fold's subgroup validation rows at row level: the dominant rows, the known rows, and per-row predictions against y.
     - Any subgroup candidate re-measures a recorded contrast (subgroup against E046 on the same rows).
   - So no fold carries confirmatory weight. S1 and the third WIN lack it, and the candidate ends INCONCLUSIVE and is never uploaded.
   - On top of that, rule 10 bars:
     - crediting the reverted reading;
     - choosing any population, tolerance or threshold from E051's per-fold or per-row results.
   - Such a run has no decision value in Days 9–12. A proposal of this kind will be rejected as not worth the compute or the look.
2. **Weather.**
   - The researcher's pre-registered rule says no weather proposal is written in Days 8–12, and that segment readings do not override it.
   - Finding 2 shows no restriction that would have met it anyway.
   - Reopening weather would be a deviation from a pre-registration, and it will be rejected.
3. **Item 1:** no lead.

**What remains admissible (Q5).** A genuinely new mechanism, designed on design months only, that leaves the subgroup alone or carries the extended known-row reading, and whose SUBMIT path can finish before G7's cutoff.
- **Item 4** is still subject to X-D08-S01-0001 (f): an expected all-rows effect below criterion 1's minimum, and G5 (c) if the iteration count is read off validation curves.

**My assessment.**
- If Days 9–12 continue, P(a promotion) is about 0.06.
- Each look adds fold reuse, and H8 leaves no out-of-sample check.
- Refreezing now is the scientifically cleaner course. Continuing is admissible only within Q5.
- Whether to continue is the owner's decision (brief §1). It is put to the owner as continue or refreeze, not as a menu of research items (G3; Q3).

## Novelty Relative to Existing Research

- **E051** was the first test of an explicit convention mixture, and it is now closed (REJECT, rule 10).
- **The weather block** was the first use of external data. Its pilot is a negative screen, recorded.
- **The item 1 look** extends PHASE_CLOSE_D01 (c) from one anchor to 18 signatures. It is the first systematic check of time-shift recording errors outside LIRF: absent at the 30-row floor, and below 1 s even when pooled.
- **None duplicates** a rejected or completed record.

## Experimental Isolation

- **E051** is exact off the subgroup: max |Δ| = 0.0 on all eight folds, H included.
  - On the subgroup, structure, g's training population and parameters change together, as X-D08-S03-0002 recorded.
  - The ablations attribute the convention-row gain to the `d_sched` component.
- **The weather pilot** changes one thing: 16 columns on an otherwise identical E045-configuration fit, with the same seed and folds. Its segment readings are diagnostics, not separate tests.
- **The item 1 look** fits nothing.

## Validation Quality

- **The frozen folds are unchanged and were used unchanged.**
  - R1–W1 and the twins scored, with S1 required.
  - H predicted only.
  - Reference E046.
  - Criterion 8 read against E033 and E028.
- **Rule 15 (G5).**
  - (a) Look count 2: E051, then E052.
  - (b) Every |ΔRMSE| exceeds the all-rows draw spread by a factor of 5.6 or more (R2: 1.39 against 0.25). The subgroup spread is 0. The per-fold mechanism-population ΔRMSE is not yet tabulated (D8-C21).
  - (c) As ruled in X-D08-S03-0001 and -0002.
- **Pre-registration.** Both Day 8 analyses committed their rules before running (Summary). Neither result depends on a post-hoc choice.

## Leakage Review

### Target Leakage

PASS

- E051: c comes from training rows only, validation y is null, and the components hold no target (re-read here in `prc.models.mixture`).
- Weather pilot: fits on the pilot fold's training rows (`masked_view`); truth joins only to the predicted design month.
- Item 1 look: no fit.
- No December target was read by any path.

### Temporal Leakage

CONCERN

Not blocking.
- **Weather features** take the latest report observed at or before t_off − 10 min, with t_off = coalesce(AOBT_3, EOBT_1, SCHED).
  - They are label P with the proxy caveat (DATASET_AUDIT §6.2; runway labelled P by assumption).
  - Nothing is admitted for any model.
- **`d_sched`** (label T) is carried from H038.
- **The live risk for Days 9–12 is design-level fold leakage.** Q5 rules it in advance for every subgroup mechanism.

### Competition Availability

CONCERN

Not blocking.
- U6 is carried, and the 2026 convention rate stays unobservable.
- The IEM licence fit (competition permission) was never settled. That is moot for Day 8, because no model or file uses weather, and it binds any reuse (Q4).

## Compute Review

### RAM

PASS

A read-only review. The Day 8 runs were within class (E051: 4.55 GB; E052: 4.42 GB).

### Runtime

PASS

E051 and E052 took 121.5 s and 125.4 s, inside the owner's window. The pilot took 235 s and 164 s, design months only.

### Disk

PASS

The weather bronze files are git-ignored with tracked manifests. The table is 2.3 MB.

## Weakest Assumption

**That "not promotable" means "not better".** On the development folds, the mean favours E051 (−20.10 s, q95 −2.98). Even after reversion it is −3.71 s.
- E046 stays because the frozen criteria require fold-level WINs that a few hundred subgroup rows rarely deliver.
- That is the right rule for promotion, but the records must say "not promotable under the frozen criteria", never "E046 predicts the subgroup better".
- The phase close's other readings rest on firmer ground: weather is bounded by the oracle analysis, and item 1 by the stake bound.

## Missing Control or Ablation

- **Required:** none for the close.
- **Named, not recommended:** X-D08-S03-0002's direct-LightGBM-on-LIRF control. Under Q5 it has no decision value in Days 9–12.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

**Records only.** No allocation, run, fit, holdout script, formatter, SUBMIT fit or upload is authorized by this review.

**Q1. Decisions and labels.**
- E046 remains champion. `CURRENT.json` stays unchanged, with no `champion_change` event.
- **H038 v2: REJECT.**
  - E051's decision is REJECT in `runtime/ledger.sqlite` and `experiments/ledger.jsonl`, noted "criterion 2 not met: one WIN (R3), S1 TIE; X-D08-S03-0004".
  - E052's decision is REJECT, noted "reproduction of E051; byte-identical; criterion 6 PASS".
- Rule 10's list gains E051's configuration.

**Q2. Holdout and upload.**
- "H: closed (H8)" is recorded, together with the task-ledger check above.
- "No Day 8 upload; E050 stands (`f0dc2c7c…06e8`)."

**Q3. Owner choices (G3).**
- Append to the D08-S03 records, verbatim and with UTC times:
  - the options the researcher offered;
  - the owner's answers ("Option 1, go ahead with the recording quirks look"; "Option 1, close Day 8").
- Closing Day 8 and dropping external data are the owner's decisions.
- If any offered option was a research item, the choice is an incident of INC-0015's type: INC-0023, disclosed in the final report.
  - Research items here include item 1, a restricted weather candidate and item 4.
  - DAY_SUMMARY's "No G2 or G3 breach is recorded in Day 8" is then amended.
- If a restricted weather candidate was among the options, the record says so: it offered the owner a route around a pre-registered rule.
- **From now on,** the question put to the owner is only "continue or refreeze", with this review's bounds stated.

**Q4. Incidents.**
- **INC-0019 closes once its closure section records:**
  - the owner's words with UTC, and the researcher's reading of them;
  - tested on design months, rule not met, and no weather proposal in Days 8–12 (Q5);
  - bronze and manifests kept, with the table reproducible byte for byte (this review);
  - the owner's unrecorded network change, which does not affect integrity (hashes verified);
  - **the IEM licence fit unsettled:** any later use needs it settled, a new owner decision recorded as an incident, and a reviewed proposal;
  - that INC-0019 §3's "any use needs its own H proposal" was read as covering experiments, not design pilots, as with H038's pilot.
- **INC-0018 (D7):** its own closure condition, "when the extension's governance review records its own rules", was met by X-D08-S01-0001 and X-D08-S03-0001 (D).
  - It is recorded as closed in the acknowledgement and in STATE.
  - The file itself stays unedited (ruling (D)).
- **INC-0017 and INC-0018 (D8)** stay open until the last Day 8–12 phase close.
- **INC-0004, INC-0009 and INC-0010** stay open. For INC-0009, E051 and E052 were never mirrored (CommError).

**Q5. If Days 9–12 continue (Branch B), these bounds bind every Day 9–12 proposal.**
- **B1. No Day 8-motivated candidate.**
  - (a) Any candidate whose mechanism changes the LIRF NM-missing subgroup's predictions carries G5's consequence, ruled now (Scientific Validity (g)). This covers:
    - the mixture or any variant of it: other p, tolerance or components, known-row exclusions, population restrictions;
    - any other model for the subgroup.

    Such a proposal will be rejected.
  - (b) No weather proposal: the pilot's own rule.
  - (c) No non-LIRF convention candidate from the item 1 look.
- **B2. Any other candidate:**
  - is designed, and piloted if at all, on 2025-01, 04, 05 and 06 only, with its parameters and decision rule committed before the pilot runs;
  - states its G5 (c) footprint and relies on no row-level validation-month record, including the Day 8 comparison files;
  - either leaves E046's subgroup predictions exactly unchanged (an override check), or carries ruling (E)'s known-row reading. In that case the known-row set is extended to every subgroup validation row named at row level in a tracked file at the proposal's commit;
  - is judged against E046 by criteria 1–8 and rules 1–15, with rule 13 if stochastic.
- **B3. Item 4 additionally:**
  - its iteration count is not read off validation curves;
  - it gives a reason to expect ≥ 1.0 s on the development mean, despite X-D08-S01-0001 (f).
- **B4. G7.**
  - A promotion leads to an upload only if its SUBMIT file is complete and checked before 2026-10-11T12:00:00Z, through its own reviewed SUBMIT proposals.
  - The phase close that promotes pre-registers the final-file rule before any SUBMIT run.
  - Otherwise: no new upload; E050 stands.
- **B5.** Each Day 9–12 phase close repeats the H8 ledger check, the look count, G1's status and the delegated-work list.
- **Branches.** Day 9 opens on `day-9` from `main`, after a content-neutral merge of `day-8`.

**Q6. If the owner ends Days 8–12 now (Branch A, the refreeze), this review is the last Day 8–12 phase close.**
- **G7's rule, pre-registered here:** no candidate was promoted in Days 8–12, so there is no new upload and E050 stands. No SUBMIT run exists to select among.
- **Records:**
  - the owner's words, with UTC, in INC-0017;
  - STATE "Phase: FROZEN (Days 8–12 closed at Day 8)";
  - a `frozen` task-ledger event citing INC-0017 and this exchange, with E050's path and hash.
- **The FINAL_REPORT Days 8–12 section** is appended per G8; Days 1–7 stay unchanged. It contains:
  - the reopening, with the stated aspiration cited by INC-0017 only (G3);
  - the seven-phase result unchanged;
  - H: four reads in total, Days 8–12 closed (H8);
  - uploads: E050's file only;
  - the INC-0017 and INC-0020 disclosures, including the Advisor-context exposures of 2026-10-06 and 2026-10-07 (Q8);
  - the Day 8 results as corrected here;
  - brief §15 verbatim, plus the Days 8–12 facts;
  - delegated work: none.
- **Incidents:** INC-0017 and INC-0018 (D8) close.
- **P7 (b), (c) and (f) apply:** a content-neutral merge into `main`; only appended files afterwards; enforcement by records only. P7 (a) and (d) add nothing new.
- **The external evaluation** follows G2 after the challenge closes.
- **No further Advisor exchange is needed for Branch A** if these records add no figure, interpretation or decision beyond those reviewed. Anything more needs review.

**Q7. The owner report.** The end-of-phase report to the owner states plainly:
- no promotion; E050 stands;
- INC-0022, D8-C14, D8-C15 (not yet told to the owner) and D8-C18;
- the decision needed: continue (within Q5) or refreeze, with this review's assessment (P(promotion) ≈ 0.06).

No figure is related to the leaderboard or the owner's target (G3).

**Q8. Disclosure.** The acknowledgement records finding 7. The external evaluation lists this exchange beside X-D08-S03-0001 as an Advisor-context exposure (ruling (D)).

**Not authorized:**
- anything in Branch B before the owner's decision is recorded;
- any weather proposal in Days 8–12;
- any change to frozen files, reviews or completed records (corrections are appended);
- any edit of the Day 7 files that hold the disclosed figure.

Required acknowledgement path: `research/day-08/acks/PHASE_CLOSE_D08_ack_v1.md`
- It references the proposal hash (`501a5881…`) and this review's hash.
- It adopts Q1–Q8 as binding and appends D8-C17 to D8-C22.
- It records the owner's branch decision when it is made.

## Revision

None required. The following corrections are appended in the acknowledgement; no proposal or completed record is edited.

- **D8-C17. Snow.** The proposal's step 3, DAY_SUMMARY §1 and `weather_LTFM_coverage.md` (Consequence 1) say a snow mechanism "cannot be learned on any fold". Correct reading:
  - R1–R3, S1 and S1c train on February and March 2025 (270 LTFM snow reports);
  - W1 and W1c, the only folds whose validation month has snow, have 2 and 0 snow reports in training;
  - so no fold can both learn and score a snow effect. The consequence for criterion 2 is unchanged.
- **D8-C18. The reverted known-row reading.**
  - (i) E051 analysis § Ruling (E): the known rows go against the candidate on R1 and S1 only. On R2 they favour it (fold +1.24e8 s², known rows −2.24e8 s²). Reverting them moves R2 to +3.90 s, with q10 −0.08 s.
  - (ii) The reverted computation fails criterion 2 by itself (2 WINs). Its R1 and S1 WINs come from deleting the candidate's losses on known rows.
  - (iii) DAY_SUMMARY §9.2, the proposal's "case against" 5 and the journal's "R1 and S1 would be WINs" are read with (i) and (ii). No computation on record passes H038 v2.
- **D8-C19. The item 1 look.**
  - It tested 18 signatures, not 15 (DAY_SUMMARY §1, the proposal).
  - The ratio test is vacuous for the shift signatures.
  - Pooled "block 1 h before AOBT_3": 30 of 554 non-LIRF tail rows; oracle stake about 0.8 s.
  - `conventions.md`'s last sentence reads: "No tested signature explains the non-LIRF tail; the look does not show what those rows are."
- **D8-C20. Weather is not a lead.** DAY_SUMMARY §9.3 and the coverage note's restricted-candidate sentence are corrected by finding 2's table: no implementable or oracle restriction reaches −1.0 s in both pilots.
- **D8-C21. The E051 records.**
  - The decision labels (Q1).
  - `range_check.py E051` (pre-registered) has no recorded output. The analysis used `mixture_analysis.py`'s subgroup counts instead, and by the mixture check the other rule-7 cells equal `range_check_E046.json`. Commit `7cb6ffd`'s message lists "range".
  - G5 (b) mechanism-population ΔRMSE (subgroup RMSE, E051 minus E046), with spread 0: R1 −237.8, R2 +177.5, R3 −2,619.0, S1 −315.1, W1 −6,510.1, S1c −669.7, W1c −9,586.4 s.
- **D8-C22. Clerical.**
  - DAY_SUMMARY §3: "a factor of 6 or more" reads "5.6 or more" (R2).
  - STATE's "Updated" and Days 8–12 section stamps (2026-10-06T18:57:28Z) precede content dated 2026-10-07.
  - The synthetic weather tests do not cover the `bdcbb83` fix (trailing-space sky codes, VV).

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Q1–Q8 and D8-C17 to D8-C22 recorded before any Day 9 allocation or the refreeze | 0.90 |
| The owner refreezes at this phase close (Branch A) | not predicted (owner's decision) |
| Under Branch B: at least one Day 9–12 candidate promoted | 0.06 |
| Under Branch B: a new upload before 2026-10-11T12:00:00Z | 0.04 |
| Under Branch B: a Day 9–12 proposal rejected or ruled under G5's consequence before allocation | 0.40 |
| A G1–G3 breach incident before the challenge closes (Q3 excluded) | 0.10 |

Expected magnitude:
- **Day 8:** no change to the champion or the submission.
- **Under Branch B, if a promotion occurs:** development mean −1 to −3 s against E046, central −1.5 s.
- **No leaderboard figure, and no expectation of one, is given (G3).**

Primary expected failure mode:
- **Branch B.** Looks without decision value: fold reuse with H closed, on a thin agenda.
  - Then a cutoff squeeze, in which a late promotion cannot complete its SUBMIT path. Records get rushed, as in D7-C14.
- **Branch A.** Records errors in the FINAL_REPORT's Days 8–12 section.
  - The usual case is an overclaim corrected here being repeated, as in D7-C8 to D7-C13.
