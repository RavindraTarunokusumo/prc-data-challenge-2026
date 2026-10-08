**Phase close X-D09-S01-0001: ACCEPT (0.80), with conditions R1–R6 and 14 required corrections (D9-C1 to D9-C14).** Day 9 closes, the project refreezes, there is no new upload, and E050 stands. The final-report section and the project summary may only be made final once the corrections are in, and before the `frozen` event.

Review: `/home/rvindra/Projects/prc-data-challenge-2026/research/day-09/advisor/PHASE_CLOSE_D09_review_v1.md` (SHA-256 `e27d4fc3e7e3094250384c20296a21eba3f0a0f9e7fb4acde2a41586a50ea7ee`). The proposal hash matches the envelope. That review file is the only thing I wrote.

**Checked and holding:**
- **Pilot decision.** The rule was committed at `0969550`, and code, parameters and tests are unchanged since. The JSON's parameter hash matches the file. The pilot read design months only and used no blanked column.
- **INC-0024 re-run is clean.** Its log was created at 00:17:00.9Z, six seconds after the go-ahead record was committed at 00:16:55Z. The run is deterministic, so the stopped run could not have changed its numbers or its rule.
- **H8.** The last `holdout_access` is 2026-10-04T17:57:38Z and the last unmasking event is E050's. After `reopened` the ledger has only the E051 and E052 allocations.
- **Integrity.** Both ledgers hold 52 experiments. The frozen files, the Advisor definition and E050's file hash (`f0dc2c7c…06e8`) all verify. `CURRENT.json` names E046. No secrets appear in the Day 9 diff.
- **B5.** Look count stays at 2, G1 is waived, and there was no delegated work.
- **Exposure.** The disclosed leaderboard figure did not reach my context in this exchange. I did not open INC-0018 (D7), INC-0017 (D7), `UPLOAD_RECORD.md` or `HANDOFF_D07.md`.

**Findings:**
1. **The pilot says nothing about the idea in the form a candidate would have taken (D9-C1).** The rule was set on all rows, with an unrouted learner. A real candidate would have kept E046's LIRF NM-missing predictions and refit the routed halves. The LIRF rows decided the sign in both months: in June their SSE increase alone (+4.14 s in all-rows terms) exceeds the whole +2.90 s result. Your decision stands as the rule's output, but the records must call the idea untested, not refuted, and must not say it would have passed. The segment table in my review is for the review only and must not be quoted.
2. **INC-0024's "no figure was seen" rests on your word alone (D9-C2).** The stopped run's empty log was deleted, which is not append-only. This does not affect the result.
3. **The §9 draft has errors:**
   - It repeats "no object name ... recorded", which INC-0020 §2 had corrected.
   - It places D08-S01 and D08-S02 on the laptop; they were cloud sessions.
   - "Owner-approved runs" needs the INC-0024 exception.
   - It omits INC-0020's reading that leaderboard isolation did not hold at the reopening.
   - D08-S02's served model and end time were never recorded, and §9.6 should say so.
4. **The project summary repeats overclaims already corrected:**
   - Day 3's gain is credited to congestion (D7-C8).
   - The roles section omits the delegation, calls the launch-argument discrepancies "run settings", drops the owner's INC-0015 choice and over-scopes the Advisor (D7-C10).
   - "None found" for the other airports' recording quirks (D8-C19).
   - It states the unverified upload as fact ("submitted once", "1 upload").
   - "The owner made the key decisions" replaces the final report's wording.
   - The first paragraph leaves out the Rome bet, and the results table lacks the "models, not the submission" caveat.

**Conditions you must follow:**
- **R1, order.** Corrections to drafts go in place; corrections to completed records are appended. Then append §9 to `FINAL_REPORT.md`, mark both documents FINAL and close the incidents. Only then write the `frozen` event.
- **R2, the `frozen` event.** It must state explicitly that there was no upload in Days 8–12.
- **R3, incidents.** Close INC-0017, INC-0018 (D8), INC-0023 and INC-0024 (with D9-C2). Keep INC-0004, INC-0009 and INC-0010 open.
- **R4, STATE.** Set the FROZEN phase, re-stamp it, and record the next free incident as INC-0025.
- **R5, finish.** Write the session end, then merge `day-9` into `main`.
- **R6, no new content.** The applied texts may add nothing beyond the records and D9-C1 to D9-C14, or another exchange is needed.

The acknowledgement goes at `research/day-09/acks/PHASE_CLOSE_D09_ack_v1.md`.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D09-S01-0001
status: COMPLETE
decisions:
  - proposal_id: PHASE_CLOSE_D09
    proposal_sha256: 6068b608c8e123efc7b9b8f83be2ebc98ecd4ab039dc3ab19e9aed28ebf355bd
    decision: ACCEPT
    review_path: research/day-09/advisor/PHASE_CLOSE_D09_review_v1.md
    review_sha256: e27d4fc3e7e3094250384c20296a21eba3f0a0f9e7fb4acde2a41586a50ea7ee
completed_utc: 2026-10-08T18:05:47Z
```
