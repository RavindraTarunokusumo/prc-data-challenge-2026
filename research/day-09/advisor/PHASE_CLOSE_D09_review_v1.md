---
schema: advisor-review-v1
hypothesis_id: PHASE_CLOSE_D09
proposal_version: 1
proposal_sha256: 6068b608c8e123efc7b9b8f83be2ebc98ecd4ab039dc3ab19e9aed28ebf355bd
exchange_id: X-D09-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-10-08T18:02:28Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.80), with binding conditions R1–R6 and corrections D9-C1 to D9-C14.**
- Day 9 closes and the project refreezes. There is no new upload, and E050 stands.
- The final-report section and the project summary become final only with the corrections applied, and before the `frozen` event (R1).

**What stands.**
- **The pilot decision.** The pre-registered rule was not met: +2.90 / −3.10 s, against ≤ −1.0 s required in both pilots. H039 was correctly not written. The commit order, the design-month footprint and the block's inputs all check out (Verified, below).
- **The INC-0024 re-run is clean.**
  - Code, parameters and rule are unchanged since `0969550`.
  - The re-run's log was created six seconds after the go-ahead record was committed.
  - The pilot is deterministic.
  - So nothing the stopped run did could have changed the re-run's numbers or its rule.
- **The refreeze.** It is the owner's decision, on the one question Q3 allows. Under G7 there is no new upload, and E050 stands. No SUBMIT run exists to select among.
- **B5.** H: closed (H8), verified below. Look count 2. G1 waived. No delegated work.

**What this review adds: four findings, all settled by corrections.**
1. **The pilot tells us nothing about the mechanism in the form a candidate would have taken (D9-C1).** Its rule was set on all rows, with unrouted training. Q5 B2 bound any candidate to keep E046's LIRF NM-missing predictions (the override from E045) and to refit the routed halves. The LIRF rows set the sign in both months: in P1, their SSE increase alone exceeds the whole result. The decision stands as the rule's output. The idea is untested, not refuted.
2. **INC-0024's "no figure was seen" rests on the researcher's word alone (D9-C2).** The stopped run's log was deleted, which is not append-only. This does not affect the result.
3. **The §9 draft repeats a corrected statement and contradicts itself (D9-C4 to D9-C8).**
   - It repeats "no object name ... recorded", which INC-0020 §2 corrected.
   - It places D08-S01 and D08-S02 on the laptop; they were cloud sessions.
   - It says "owner-approved runs" without the INC-0024 exception.
   - It omits INC-0020's own reading.
4. **The project summary repeats overclaims already corrected (D9-C9 to D9-C14).**
   - It repeats D7-C8 (Day 3's gain credited to congestion), D7-C10 (provenance) and D8-C19 ("none found").
   - It states the unverified upload as fact.
   - This is the Branch A failure mode the Day 8 review predicted: "an overclaim corrected here being repeated".

**The champion, adversarially.** Day 9 adds no objection to E046. One observation, consistent with U6 and rule 6:
- Adding seven columns to E045's configuration moved LIRF's RMSE by +18.21 s in June and −17.05 s in May (P-only: +10.46 / −5.42 s). E045's configuration is the model whose stored predictions E046 uses for the subgroup.
- The pilot note attributes the swing to a few hundred tail and NM-missing rows, mostly at LIRF.
- So the subgroup component is high-variance under small input changes. U6's "tens to hundreds of seconds, in either direction" already covers this.

**Verified here (read-only).**
- **Hashes and tree.**
  - The proposal is `6068b608…55bd`, as in the envelope.
  - The Advisor definition is `30fff5dd…0d19`, as in `config/agents.yaml`.
  - The six frozen files match `config/frozen.json`, and so do the SPLITS v2 proposal, review and acknowledgement.
  - The tree is clean at `0039358`.
- **Day 9 changes are append-only.** `git diff --numstat 3e85b4c HEAD` shows additions only. The one exception is `src/prc/features.py`, where `NUMERIC` gains the seven taxi-state names. `NUMERIC` is only a membership filter (`features.columns`), so the FS2 reference's columns are unchanged.
- **Pre-registration order** (file and commit times, UTC):
  - block, tests, parameters and script written 22:19:07–22:20:39 on 7 October;
  - full test suite: the pytest cache was last written at 22:21:52, with no new failure;
  - rule committed (`0969550`) at 22:21:58;
  - INC-0024, with the owner's "Go", committed at 00:16:55 on 8 October;
  - re-run log created at 00:17:00.9; JSON written at 00:21:49; results committed (`bd3c73e`) at 00:22:18.
  - `git diff 0969550 HEAD` over `src`, `scripts`, `tests`, `config` and the parameters file is empty.
  - The JSON records the parameters' hash `bbdb9079…`, which matches the file.
- **Pilot JSON internal checks.** The NM-missing plus NM-present SSE changes equal the all-rows change, and so do tail plus bulk and the sum over airports (to within 1e-5 s²). The row counts add up.
- **Design-month footprint.**
  - The script builds features from `masked_view` on folds made of design months only. That view drops every other month, and blanks the predicted month's DEP block time and target.
  - The truth join is filtered to the predicted month's DEP rows.
  - 2025-01, 04, 05 and 06 are exactly the intersection of the training months of R1–R3, S1 and W1, and none of them is a validation month of any fold, H included.
- **The block uses no blanked column.**
  - `prc.taxistate` reads ARR `BLOCK_TIME_UTC_mvt` and `MVT_TIME_UTC_mvt`, and DEP `MVT_TIME_UTC_mvt`, `AOBT_3_flt`, `EOBT_1_flt`, `SCHED_TIME_UTC_mvt` and `RUNWAY_mvt`.
  - `BLANKED_DEP_COLS` is DEP `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt` only.
  - `test_invariant_to_dep_block_and_target` asserts the invariance.
  - The P features remove the row's own takeoff exactly, tested at nine offsets. There are 14 tests in the file.
- **Holdout (H8).**
  - The task ledger has 94 lines. Its last `holdout_access` is 2026-10-04T17:57:38Z (Day 7).
  - Its last unmasking event is E050's, at 2026-10-04T22:01:39Z.
  - After `reopened` (2026-10-05T14:15:05Z) there are only the E051 and E052 allocations, and there is no Day 9 line.
  - `experiments/ledger.jsonl` and `runtime/ledger.sqlite` (opened read-only) each hold 52 experiments. E051 and E052 are labelled REJECT, and there is no E053.
- **Upload and champion.**
  - `predictions/final/E050/submitting.parquet` is `f0dc2c7c…06e8`, recomputed here.
  - `CURRENT.json` names E046.
  - No commit has touched `models/` or `predictions/final/` since 2026-10-05.
- **Counts used by the drafts.**
  - 33 exchange directories: 27 for Days 1–7 and 6 for Days 8–12.
  - 26 incident files under 24 numbers.
  - The summary's figures match the ledgers and holdout records: 580.79 / 514.74 (E001), 482.73 / 411.29, 444.49 / 375.93, 438.87 / 369.18, 314.42 / 244.94, and 294.32.
- **Sessions (registry).**
  - D08-S01 ran in the cloud and D08-S02 in the cloud (governance and text only).
  - D08-S03 and D09-S01 ran on the owner's laptop.
  - D08-S02 has no `SESSION_START.md`, and its served model and end time are not recorded.
- **Secrets.** No credential pattern appears in the Day 9 diff.

**What I did not do.**
- I read no target of any month, design months included. The pilot was checked from its stored aggregates only.
- No run, fit, allocation, test-suite run, holdout script or formatter.
- No challenge page, leaderboard or bucket.
- I did not open INC-0018 (D7), INC-0017 (D7), `UPLOAD_RECORD.md`, `HANDOFF_D07.md` or the post-freeze session-registry note. From the registry I printed only selected fields.
- **The disclosed leaderboard figure did not reach the Advisor's context in this exchange.**

## Scientific Validity

### (a) The pilot decision and its reading (request 1; "case against" 1)

- **The decision stands.** The rule is pre-registered and its output is mechanical: P1 is +2.898 s. Restricting the population after seeing the result would be a post-hoc population change (rule 10), and the researcher rightly did not do it.
- **The rule's population did not match the candidate's construction.**
  - Q5 B2 and HANDOFF_D08 §4.1 bound any candidate to keep the LIRF NM-missing subgroup's predictions from E045's stored file, and to refit the routed halves (E029, E031).
  - The pilot measured the block with an unrouted LightGBM, on all rows, including the subgroup a candidate could not change.
  - From the stored aggregates (the SSE change divided by 2·n·RMSE_ref, i.e. in all-rows seconds; first-order, within about 0.01 s):

| Rows | P1 (June) | P2 (May) |
|---|---|---|
| All rows (the rule; exact) | +2.90 | −3.10 |
| LIRF, all rows | +4.14 | −2.20 |
| NM-missing, all airports | +3.55 | −2.31 |
| Tail, y ≥ 3,600 s (395 / 219 rows) | +2.50 | −1.88 |
| Nine non-LIRF airports, all rows | −1.23 | −0.88 |
| NM-present, all airports | −0.64 | −0.77 |

  - **In P1 the LIRF rows' increase exceeds the whole result. In P2 they carry about 70 % of it.**
  - The candidate's analogue is the non-LIRF rows plus LIRF's NM-present rows, under routed training.
    - The LIRF NM-present term cannot be separated from the stored aggregates, and no row-level prediction was stored.
    - Meeting −1.0 s in both pilots would need that term to contribute at most +0.23 s in P1 and at most −0.12 s in P2.
    - The record cannot say whether that holds, and the pilot did not use the routed training population.
- **Reading.** The decision stands as the rule's output. But the pilot tells us nothing about the mechanism in the candidate's form. No record may say that the block was shown not to help, or that it would have passed (D9-C1).
  - The table is for this review only. It is a post-hoc population (rule 10), and no figure from it enters the final report or the summary.
- **Precision.** NM-present in P1 is −0.996 s, which is not ≤ −1.0 s. The "−1.00" in the pilot note and in DAY_SUMMARY is rounding (D9-C3).

### (b) INC-0024 (request 1; "case against" 2)

- **Order.** The re-run started after the go-ahead was recorded: log created at 00:17:00.9Z, INC-0024 committed at 00:16:55Z. The rule, code and parameters were unchanged (Verified).
- **Determinism.** LightGBM ran with `deterministic`, row-wise, seed 42, no bagging and the same thread count. A figure from the stopped run, had there been one, would have equalled the re-run's, and the rule was already fixed. **The re-run is clean.**
- **What is weak.**
  - The stopped run left no trace: the empty log was deleted, which is not append-only.
  - "About two minutes" appears only in this proposal, not in INC-0024. The re-run's P1 took 157.4 s after loading, so the margin is narrow.
  - "No figure was seen" therefore rests on the researcher's statement. That is a gap in the record, not in the validity (D9-C2).

### (c) The block (request 1, last bullet)

- **No blanked column is used** (Verified).
- **Admissibility.** All inputs are in the ranking information set (DATASET_AUDIT §6.1–6.2). The P labels depend on the `AOBT_3` proxy for t_off, which the audit allows.
- **A design change from the plan.** HANDOFF_D08 §4.1 named medians and counts; the block uses means and no counts. This was fixed in code before any target was read, so it is a design choice, not tuning.

### (d) The refreeze (request 2)

- **The owner's words.** They are verbatim in the INC-0017 amendment, with the time bounded: after `bd3c73e` (00:22:18Z), before the entry (17:41:53Z). No commit lies in between.
- **Reading.** "Wrap up the experiment" reads as the refreeze, and it matches HANDOFF_D08 §4.3's stop rule. Asking "continue or refreeze" after the stop rule fired is the question Q3 allows.
- **G7.** No candidate was promoted, so there is no new upload and E050 stands. There is no SUBMIT run to select among. Q6's records apply, with "closed at Day 9".
- **G2** needs "no upload" recorded, so the `frozen` event must say it (R2).
- **P7 (c)** allows only appended files after FROZEN, so the drafts must be corrected first (R1).

### (e) The final-report section (request 4)

Checked against INC-0017, INC-0020, INC-0023, the Day 8 records, both ledgers and the session registry.
- **Accurate:**
  - the Day 8 rows, as corrected by D8-C17 to D8-C22;
  - the rules'-asymmetry sentence;
  - four H reads;
  - 52 experiments and 33 exchanges;
  - the incident count;
  - both Advisor-context exposures.
- **Errors:** D9-C4 to D9-C8.

### (f) The project summary (request 5)

Every figure matches the records. The problems are interpretations and omissions.
- **D7-C8 repeated.** The Day 3 row credits the 444 s champion to congestion. In fact 95 % of E019's margin over E005 was routed FS1 structure (D3-C1), and congestion as served was −1.90 s on all rows.
- **D7-C10 repeated.** The roles section:
  - omits the Sonnet delegation (INC-0005, INC-0013);
  - calls the launch-argument discrepancies (INC-0003, INC-0004) "run settings";
  - omits the owner's Day 7 choice (INC-0015), which led to the final champion;
  - says the Advisor reviewed "every step" and "every proposal before anything ran". The design pilots and looks ran without per-item review.
- **D8-C19 repeated** ("none found").
- **The owner's role.** "The project owner made the key decisions" replaces FINAL_REPORT §1's precise statement ("The owner did no feature selection, tuning or interpretation", plus INC-0015) with an interpretation.
- **The upload.** It is stated as fact three times. But every Day 8–12 record must disclose it as unverified, and after the waiver of G1 (a) (iii)–(iv) no record establishes "once".
- **"Process errors are all recorded, and none affected a submitted result"** is not in the records.

### (g) "Case against" 4 (`test_evaluator`)

- It scores random predictions against R3 truth to test determinism, and it checks row counts. On a pass it displays no figure and scores no model or feature.
- It is not a look under G5 (a). No disclosure is needed beyond the acknowledgement.

## Novelty Relative to Existing Research

- The block measures durations, where Day 3 counted movements. It is not redundant with any rejected or completed work. H017's caveat ("`d_aobt3` already encodes the realised waiting") was the known risk.
- Because of finding 1, the records describe the idea as untested in the candidate's form, not refuted. No Days 8–12 work remains to test it.

## Experimental Isolation

- **Isolation was adequate.** The pilot changed one thing, the 7-column block, against a fixed reference with the same learner, seed and months, and it reported a P-only variant.
- **The flaw is elsewhere.** It is in the evaluation population and the training population (finding 1), not in the isolation.

## Validation Quality

- **No frozen fold was used.** The footprint is design months only (Verified). W1c trains on January only, which does not affect the footprint.
- **The rule was pre-registered and decisive as written.** No review checked its population before the run: Q5 B2 required a committed rule, not a reviewed one.
- **G5 (a): 2 looks (E051, E052).** Day 9 adds none.

## Leakage Review
### Target Leakage
PASS
- No blanked column or target enters the block.
- The P features exclude the row's own takeoff exactly.
- The truth join is limited to the predicted design month's DEP rows.

### Temporal Leakage
PASS
- The P features use events before the t_off proxy.
- The T features use the row's own taxi interval, labelled T and admissible (§6.2).
- The 1 July 2026 month edge is the audit's known asymmetry (§6.5).
- No candidate exists, so nothing reaches a submission.

### Competition Availability
PASS
- ARR rows are complete in ranking. Other departures' takeoff times and `AOBT_3` are present (§6.1).

## Compute Review
### RAM
PASS
- This is a read-only review. No run is proposed.

### Runtime
PASS
- The pilot took about 277 s on the laptop CPU (P1 157.4 s, P2 119.3 s): CLASS-S scale.

### Disk
PASS
- Three small tracked outputs.

## Weakest Assumption

- **The main one:** that the pilot's all-rows rule measured the block's value for the candidate it gated. It did not. The LIRF rows, which a candidate could not change, set the sign in both months. The decision is valid as a rule outcome; it is not evidence against the mechanism.
- **A second:** that no figure was seen in the stopped run. This rests on the researcher's statement, because the log was deleted. It does not affect the result.

## Missing Control or Ablation

- **Named, not recommended:** the pilot's matched control. That is the same comparison with the LIRF NM-missing predictions held at the reference in both arms, and with the routed training population.
- The refreeze makes it moot. It is named so that the records describe the pilot correctly.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

**Records only.** No allocation, run, fit, test-suite run, holdout script, formatter, SUBMIT fit or upload is authorized by this review.

**R1. Order.**
1. Apply D9-C1 to D9-C14.
   - Corrections to drafts are applied in place, as with D7-C1 to D7-C13 and D8-C14 to D8-C22. The drafts are the Day 9 DAY_SUMMARY, the §9 draft and PROJECT_SUMMARY.
   - Corrections to completed records are appended. These are the pilot note, the incidents and STATE's history.
2. Append §9 to `FINAL_REPORT.md`; §§1–8 stay unchanged.
3. Mark DAY_SUMMARY and PROJECT_SUMMARY FINAL.
4. Close the incidents (R3).
5. Only then write the `frozen` event. After FROZEN, P7 (c) allows only appended files.

**R2. The `frozen` task-ledger event.** It names:
- E050's path and SHA-256 (`f0dc2c7c…06e8`);
- the champion, E046;
- the basis: "INC-0017 (refreeze amendment, 2026-10-08T17:41:53Z); X-D09-S01-0001";
- **explicitly, no upload in Days 8–12 (G7).** This is G2's "no upload is recorded".

**R3. Incidents.**
- **INC-0017** closes with its final upload record:
  - no new upload in Days 8–12;
  - E050 stands;
  - E050's upload remains the owner's report, unverified (INC-0020 §2).
- **INC-0018 (D8)** closes with the delegated-work list: none in Day 8 or Day 9.
- **INC-0023** closes once §9.4, with D9-C7, is appended.
- **INC-0024** closes with D9-C2 recorded in its closure section.
- **INC-0004, INC-0009 and INC-0010** stay open.

**R4. STATE** records:
- "Phase: FROZEN (Days 8–12 closed at Day 9)";
- champion E046; E050 stands; H: closed (H8);
- open incidents INC-0004, INC-0009 and INC-0010; next free INC-0025;
- E053 unused; last exchange X-D09-S01-0001.

Re-stamp "Updated" and the Days 8–12 section stamp. The 2026-10-07 stamp currently precedes a Day 9 line, as in D8-C22.

**R5. Then:**
- the D09-S01 session-end line;
- the content-neutral merge of `day-9` into `main` (P7 (b));
- enforcement by records only (P7 (f)).

**R6. No further exchange is needed** if the applied texts add no figure, interpretation or decision beyond the records and D9-C1 to D9-C14.
- D9-C1 must not turn into a claim that the block helps or would have passed.
- No figure from this review's table in Scientific Validity (a) enters the report or the summary.
- Anything more needs review.

**Not authorized:**
- any pilot, experiment or test-suite run;
- any edit of the Day 7 files that hold the disclosed figure;
- any edit of a completed record other than by an appended correction.

Required acknowledgement path: `research/day-09/acks/PHASE_CLOSE_D09_ack_v1.md`
- It references the proposal hash (`6068b608…55bd`) and this review's hash.
- It adopts R1–R6.
- It lists D9-C1 to D9-C14, with where each was applied.
- It records the B5 items: the H8 check, look count 2, G1 waived, delegation none.

## Revision

None to the proposal. The corrections below bind the records (R1). Each states the fact the text must carry; the wording is the researcher's.

**Day 9 records**
- **D9-C1. The pilot's reading.**
  - The rule's population (all rows, unrouted training) did not match the construction Q5 B2 binds a candidate to: the LIRF NM-missing subgroup overridden from E045, with routed halves.
  - In P1 the LIRF rows' SSE increase exceeds the whole result.
  - The decision stands as the rule's output (rule 10; no re-adjudication).
  - The mechanism is untested in the candidate's form. No record may say it was shown not to help, or that it would have passed.
  - Recorded in the acknowledgement. DAY_SUMMARY §1 and the pilot note are read with it.
- **D9-C2. INC-0024's evidence.**
  - The stopped run's empty log was deleted, which is not append-only.
  - "No figure was seen" and the run's duration rest on the researcher's statement.
  - This does not affect the result: code, parameters and rule are unchanged since `0969550`, the re-run is deterministic, and its log was created after the go-ahead was recorded.
  - Recorded in INC-0024's closure section and in DAY_SUMMARY §5.
- **D9-C3. Clerical.**
  - The pilot note: P2's EDDF (−0.13 s) is also about 0, and P1's LSZH (−4.30 s) lies outside "−1 to −4 s".
  - NM-present in P1 is −0.996 s, shown as −1.00.
  - DAY_SUMMARY's G3 line: "continue or refreeze" was the only research-direction question. The pilot's "Go" was a run decision (INC-0024).
  - STATE's stamps and IDs (R4).

**The final-report section (§9 draft)**
- **D9-C4. §9.1.** D08-S01 and D08-S02 ran in the cloud, governance only. Only D08-S03 and D09-S01 ran on the laptop. As written, §9.1 contradicts §9.6 and the session registry.
- **D9-C5. §9.2.**
  - The Day 9 row carries D9-C1 in one clause.
  - The weather row's "No restriction reaches the rule" is limited to the tested restrictions, including an oracle one (D8-C20).
- **D9-C6. §9.3.** "No object name, time or recomputed hash was recorded" is the statement INC-0020 §2 corrected.
  - The `day-7` upload record names the object and the expected hash.
  - The researcher did not observe the hash recomputed at upload.
  - The upload is the owner's report, and it is unverified.
- **D9-C7. §9.4.**
  - Add INC-0020's disclosure and reading:
    - the Day 8 records written before the merge wrongly stated that no figure had been seen;
    - leaderboard isolation did not hold at the reopening;
    - the owner's aspiration was stated after the disclosure.
  - The "Researcher errors" list is a selection. Say so, and point to the full lists (D8-C1 to D8-C22; D9-C1 to D9-C14).
  - Add D8-C18 (named by Q7) and D9-C2.
- **D9-C8. §9.6.**
  - "In owner-approved runs" needs the INC-0024 exception: the first start of the Day 9 pilot.
  - D08-S02 has no session-start record, and the registry holds neither its served model nor its end time. State this beside the governance-session line.
  - The external-data line also notes that the IEM licence fit is unsettled, and that the data is kept and unused (INC-0019 closure).

**The project summary**
- **D9-C9. The upload and the standing disclosures.**
  - Each statement of the upload states it as the owner's report, unverified: "submitted once", "uploaded by the owner once", "1 upload" and "its file was submitted".
  - After the G1 waiver, no record establishes "once".
  - Add the missing standing disclosure: what was known at the reopening is not stated.
  - Add that the disclosed figure also reached the Advisor's context twice.
- **D9-C10. Roles (D7-C10 repeated).**
  - Use FINAL_REPORT §1's statement of the owner's role, in place of "made the key decisions" and "every owner intervention is logged as an incident". Owner decisions are recorded in incidents, acknowledgements and day summaries.
  - State the owner's Day 7 choice that led to the final champion (INC-0015), and the Day 8 choices (INC-0023).
  - State the delegation (INC-0005, INC-0013).
  - Describe INC-0003 and INC-0004 as the researcher's own model and effort settings, with Day 3's still undetermined.
  - Scope the Advisor as reviewing every proposal before its runs, and every phase close. The design pilots and looks ran under committed rules, without per-item review.
- **D9-C11. Day 3 (D7-C8 repeated).** The 483 → 444 s step is not credited to congestion. 95 % of E019's margin over E005 was routed FS1 structure (D3-C1), and congestion as served was −1.90 s on all rows.
- **D9-C12. The bet and the figures.**
  - The opening paragraph's "largest single step" carries U6: it depends on Rome's recording quirk persisting in 2026, with a downside of similar size.
  - Directly under the result table, carry FINAL_REPORT §4's caveat. The figures belong to the evaluated models, not to the submitted file. Neither the development margin nor the December ΔRMSE is the file's expected gain.
- **D9-C13. Errors.** "Process errors are all recorded" and "none affected a submitted result" are not in the records. Keep only statements the records support, for example D7-C14: no output was affected.
- **D9-C14. The Day 8 and Day 9 rows.**
  - "Recording quirks ... (none found)" repeats what D8-C19 corrected. None of the 18 tested patterns explained the non-LIRF tail, and the look does not show what those rows are.
  - The Day 9 row and the extension paragraph must not imply that the taxi-state idea was shown not to work (D9-C1).

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| D9-C1 to D9-C14 applied before the `frozen` event | 0.85 |
| A further appended correction to §9 or the summary is needed after FROZEN | 0.30 |
| A G1–G3 breach incident before the challenge closes | 0.05 |
| A further reopening | not predicted (owner's decision) |

Expected magnitude:
- No change to the champion (E046) or the submission (E050's file). Days 8–12 end with no promotion.
- No leaderboard figure, and no expectation of one, is given (G3).

Primary expected failure mode:
- **The opposite overclaim, introduced while applying the corrections.** D9-C1 gets rewritten as "the taxi-state block helps ordinary flights" or "would have passed", or this review's segment table gets quoted.
- **Second:** the summary's lay simplifications drift away from the records' wording again (D9-C10 to D9-C12).
