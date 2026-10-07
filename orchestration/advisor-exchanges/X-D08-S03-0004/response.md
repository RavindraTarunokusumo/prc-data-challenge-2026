## PHASE_CLOSE_D08 review: ACCEPT (confidence 0.85)

The recomputed proposal hash matches the envelope (`501a5881…4a19`). The review is at `/home/rvindra/Projects/prc-data-challenge-2026/research/day-08/advisor/PHASE_CLOSE_D08_review_v1.md` (SHA-256 `3a1a5f32…81ab`). The acceptance carries binding conditions Q1–Q8 and appended corrections D8-C17 to D8-C22. `DAY_SUMMARY.md` is marked FINAL only once D8-C14 to D8-C22 are applied.

**What stands**
- **E046 stays champion.** E051 fails criterion 2 as frozen: one WIN (R3), and S1 is a TIE (q90 +11.50 s).
  - Neither ledger has a decision label for E051 or E052.
  - Under H038 v2's own falsification criterion and the project's precedent (E011, E023, E024), H038 v2 is **REJECT**. E052 takes the same label, as reproductions did before (Q1).
- **Weather stays dropped.** The rule is robust to the "too blunt" objection. If only one segment takes the weather model's predictions, the all-rows change is:
  - bulk rows only (target-defined, so not implementable): −0.91 s and −0.80 s;
  - rows with an NM match (implementable): +0.17 s and −0.63 s;
  - EHAM only: −0.61 s and −0.36 s;
  - the four airports that gained in both pilots: −1.28 s and −0.59 s.

  None reaches −1.0 s in both pilots, so the bulk reading is not a lead.
- **Item 1 is closed with no lead.** The reading is the rule's own output.
- **H: closed (H8)** is verified, with no holdout or unmasking event in the task ledger after Day 7.
- **No Day 8 upload; E050 stands.** Its file hash was recomputed and is unchanged.

**Findings**
1. **The reverted known-row reading is weaker than presented (D8-C18).**
   - Even if credited in full, it still fails criterion 2: 2 WINs, against a minimum of 3.
   - Its R1 and S1 WINs exist only because reverting deletes the candidate's own losses on known rows.
   - The E051 analysis misreads R2. There the known rows favour the candidate, and reverting them leaves R2 0.08 s from a LOSS at q10.
2. **The snow statement is wrong as written (D8-C17).** R1–R3, S1 and S1c all train on February and March 2025, which hold 270 LTFM snow reports. What is true is that no fold can both learn a snow effect and be scored on one. The conclusion is unchanged.
3. **The item 1 look's count and wording (D8-C19).**
   - It tested 18 signatures, not 15.
   - Its tail-to-bulk ratio test is automatically met for the time-shift signatures, so only the 30-row floor applied.
   - Pooled across airports, "block 1 h before AOBT_3" covers 30 tail rows. Even identified perfectly, that is worth about 0.8 s of all-rows RMSE.
   - The note's closing sentence claims more than the look tested.
4. **Record gaps in E051 (D8-C21).**
   - The pre-registered `range_check.py E051` has no recorded output.
   - The per-fold subgroup ΔRMSE required by rule 15 (b) is not tabulated. The values are supplied in the review.
   - Clerical items are in D8-C22.
5. **Governance.**
   - Q3: the owner's answers to numbered options are recorded, but not the options themselves. If any option was a research item, G3 makes that choice an incident (INC-0023).
   - Q4: INC-0019 needs the owner's words in its closure, plus the unsettled IEM licence. INC-0018 (D7) was omitted from the proposal; its own closure condition is met, and it is closed in the acknowledgement while the file stays unedited.
   - Q7: D8-C15 must be told to the owner plainly.
6. **My own exposure (Q8).** I opened INC-0018 (D7) to rule on its status. That file holds the disclosed leaderboard figure, and my attempt to mask it in the output failed. The figure is not repeated and not used. The acknowledgement and the external evaluation must record it.

**Ruling on Days 9–12 (Q5, Q6)**
- **Neither Day 8 reading may motivate a promotable candidate.**
  - Any candidate that changes the LIRF NM-missing subgroup is ruled now to carry G5 (c)'s consequence (INCONCLUSIVE, never uploaded), and rule 10 also applies. Such a proposal will be rejected.
  - Weather is barred by its own pre-registered rule.
- **What remains admissible:** genuinely new mechanisms designed on design months only. They must leave the subgroup unchanged or carry the extended known-row reading, and finish their SUBMIT path before 2026-10-11T12:00:00Z.
- **My assessment:** P(a promotion) ≈ 0.06 if Days 9–12 continue. Refreezing now is the cleaner course; the owner decides.
- **Branch A (refreeze now):** this review serves as the last Day 8–12 phase close. G7's rule gives "no new upload; E050 stands". The FINAL_REPORT section follows G8, and no further exchange is needed if the records add nothing new.

**What I checked (read-only)**
- Frozen hashes, the Advisor definition hash and a clean tree.
- The H038 code freeze held during the batch.
- All 24 prediction files of E046, E051 and E052 match their manifests.
- Every E051 figure, recomputed from the comparison JSONs.
- That each pilot rule was committed before its run.
- The weather table rebuilds byte for byte (in the scratchpad only), so the "dirty code" flag on its manifest does not matter.
- The LTFM weather table recounts exactly from the raw files.
- 13 synthetic tests pass and lint is clean.
- No secrets in the diff.

I read no target and ran no fit or holdout script. I did not run the full test suite, because one test reads development-fold truth.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D08-S03-0004
status: COMPLETE
decisions:
  - proposal_id: PHASE_CLOSE_D08
    proposal_sha256: 501a5881d1beba663ff54f85fe16343a67b3d1d56f2ca27e5ea5aa2b637d4a19
    decision: ACCEPT
    review_path: research/day-08/advisor/PHASE_CLOSE_D08_review_v1.md
    review_sha256: 3a1a5f32d024e9fb77bc434e25362da34f0a982108556e6d1eb3c5e0b28781ab
completed_utc: 2026-10-07T22:09:30Z
```
