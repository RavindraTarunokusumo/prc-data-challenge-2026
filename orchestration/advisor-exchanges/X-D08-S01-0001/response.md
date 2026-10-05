## Advisor result: X-D08-S01-0001, PHASE_OPEN_D08 v1

**Decision: ACCEPT (0.80).** The acceptance carries binding conditions G1–G12, a new holdout ruling H8, rule 15 as amended (G5), and corrections D8-C2 to D8-C6.

- Reopening for Days 8–12 is admissible as an owner-decided deviation (INC-0017).
- Research resumes only after the G1 preconditions are committed. Until then, no `reopened` event is written and nothing is allocated.
- This review authorizes no allocation, run, holdout access or upload.

The proposal hash, recomputed, is `6c91822f…4ee1a3b`, which matches the envelope. The review is at `/home/user/prc-data-challenge-2026/research/day-08/advisor/PHASE_OPEN_D08_review_v1.md` (SHA-256 `21b8391f0bc874f704cafe10afaeeea36e7f2ab581d3c63e13745aa9428de1b6`).

### Answers to your three questions
- **(c) Hedges are inadmissible, whatever the ranking rule (G2).**
  - At most one new file is uploaded: the refreeze's file, and only if a candidate is promoted.
  - E050's file is already in the bucket. So under a "best submission" rule, even that single upload means the ranked figure may be the better of two files. This is disclosed in the external evaluation.
  - No Day 8–12 decision depends on the ranking rule, so nobody confirms it before the final upload. Confirming it means visiting the page that also shows the leaderboard, which would break the owner's own blindness.
  - If a counted submission must be designated: the final file if one is uploaded, otherwise E050's file.
- **(d) The holdout H stays closed for all of Days 8–12 (ruling H8).**
  - No access is granted now, and no later Day 8–12 review may grant one; ruling H7 stands.
  - Closure is enforced by records only. The gate takes the phase from the proposal's directory, so the holdout code would allow one access in each of `day-08` to `day-12`.
  - An objection that only H could resolve (like Day 7's objection F) therefore cannot be resolved. A candidate carrying one ends INCONCLUSIVE and is not uploaded.
- **(e) Rule 15 is adopted, amended (G5).** Each Day 8–12 candidate reports:
  - (a) every development-fold look, meaning every scored run of any purpose plus every analysis that read validation-month targets. Days 1–7 baseline: 44 scored experiments.
  - (b) its all-rows and mechanism-population ΔRMSE against the spread of E046's draw analogues. This needs no new run.
  - (c) a discovery footprint in the proposal: which months' targets were read, and at what granularity.
  - The consequence is pre-registered now. A design that read a fold's validation-month targets at row, flight or airport-day level, or that re-measures a contrast already recorded on the same folds, gets no confirmatory weight on that fold. If that leaves S1, or criterion 2's third WIN, without weight, the candidate ends INCONCLUSIVE.

### Preconditions you must arrange with the owner (G1)
All of these must be committed before the `reopened` event.
- **(a) The owner's commitments, in the owner's own words** (appended to INC-0017), not in your acknowledgement:
  - read no leaderboard content, through any channel including organiser e-mail, until the challenge closes. At minimum, until the refreeze's upload decision has been executed.
  - relay nothing about the board, including rank, direction or distance from 250 s.
  - make no upload before the refreeze, then carry out exactly the refreeze's decision.
  - after that, no further upload and no further reopening, whatever any figure shows.
- **(b) The owner's statement of what they knew at reopening:** whether any leaderboard content has been viewed since FROZEN, whether any E050 figure was seen, and where the 250 s figure came from. "No score yet" does not settle these. If an E050 figure was seen, a new review is needed first.
- **(c) The owner's completed upload line, which P7 (d) of the Day 7 phase close required and which is still missing:**
  - the object name, the upload time, the path uploaded and its SHA-256, and whether the hash was recomputed before upload.
  - this matters because E044's file at `predictions/final/` and E050's at `predictions/final/E050/` are both named `submitting.parquet`.
  - a hash mismatch, a wrong file or a non-conforming name sends it to a recovery review.
- **(d) The deviation from the leaderboard policy's "submit once"** is recorded as the owner's decision.

### Other main conditions
- **G3: the owner's target and role.**
  - No record and no message to the owner relates a development, H or segment figure to 250 s or to the leaderboard, including by juxtaposition.
  - Proposals cite INC-0017, not the number.
  - Do not put choices between candidates or files to the owner (the INC-0015 type).
  - Neither you nor workers open challenge pages. Your acknowledgement states what the 2026-10-05 index-page read showed.
- **G6: sessions and compute.**
  - Sessions do not overlap: D08-S01 ends and pushes before the laptop session allocates.
  - Before its first allocation, the laptop session records the environment (rule L v2 item 6) and confirms its ledger holds E001–E050.
  - Phase-close reviews run where the stored predictions are.
- **G7: the final-file rule.**
  - Only one branch uploads: the latest Day 8–12 champion's checked SUBMIT file, complete before 2026-10-11T12:00:00Z.
  - Every other branch is "no new upload; E050 stands".
  - No branch uploads E044's file or E050's file again.
- **G8: final report.** The Days 1–7 content is unchanged and Days 8–12 are appended. The external evaluation is recorded per file after the challenge closes.
- **G9: agenda notes, binding on later proposals.**
  - Item 1 must cite the Day 1 phase-close finding (c): outside LIRF, block-at-schedule is at or below base rates.
  - Item 2 cannot be promoted on "downside"; trading development RMSE for lower forward exposure re-adjudicates the Day 7 decision (rule 10).
  - Item 4: −0.73 s on the CatBoost half alone is below criterion 1's 1.0 s minimum before blending.
- **G10: breaches.** Any breach leads to an incident and a recovery review, and nothing is uploaded meanwhile.

### Corrections to append (the proposal is not edited)
- **D8-C2.**
  - Non-LIRF bulk RMSE is 149–309 s, not "about 180–310".
  - LIRF bulk is 279–710 s, not 297–710.
  - E046's LIRF bulk is largely its own subgroup's cost: 45/19/16/72/5 % of its LIRF bulk SSE on R1/R2/R3/S1/W1. E033's LIRF bulk was 273–374 s.
- **D8-C3.** The convention is specific to LIRF. LIRF holds only 12–68 % of each fold's rows at or above 3,600 s; in W1, LTFM holds 615 of 763.
- **D8-C4.** 44 experiments have development-fold scores, not 50.
- **D8-C5.** §3's heading "What this means for the owner's aspiration" is withdrawn.
- **D8-C6.** Clerical: four records share the session start's timestamp (09:31:17Z).

### Verified (read-only)
- **Hashes and tree.**
  - The six frozen files and the advisor definition (`30fff5dd…`) match their pins.
  - The merged `main` (`88cdb22`) equals the FROZEN tree (`4c21eff`).
  - `66e8296` adds records only.
- **Ledgers.**
  - The task ledger has four H accesses, and nothing after the `frozen` event.
  - The cloud SQLite ledger holds E001–E024 only, so an allocation here would reissue E025. E051 is correct on the laptop.
- **§3 table.** Every cell reproduces from E046's `metrics.json`.
- **Not checkable here.** E050's file is not in this container, so its hash could not be verified.
- **Not touched.** No target, block-time or December data was read; no fit, holdout script, web page, leaderboard or bucket.

I did not write `response.md`. Store this message verbatim there, as before.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D08-S01-0001
status: COMPLETE
decisions:
  - proposal_id: PHASE_OPEN_D08
    proposal_sha256: 6c91822f5a6d5456575f3f65f83b8a4b06a2078e909852aa934dba4db4ee1a3b
    decision: ACCEPT
    review_path: research/day-08/advisor/PHASE_OPEN_D08_review_v1.md
    review_sha256: 21b8391f0bc874f704cafe10afaeeea36e7f2ab581d3c63e13745aa9428de1b6
completed_utc: 2026-10-05T09:54:15Z
```
