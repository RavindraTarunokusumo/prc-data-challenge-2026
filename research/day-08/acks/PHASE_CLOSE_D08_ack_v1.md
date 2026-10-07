# Acknowledgement: PHASE_CLOSE_D08 v1 (exchange X-D08-S03-0004)

*Written 2026-10-07T22:12:00Z (measured with `date -u`).*

- **Proposal:** `research/day-08/proposals/PHASE_CLOSE_D08_v1.md`, SHA-256 `501a5881d1beba663ff54f85fe16343a67b3d1d56f2ca27e5ea5aa2b637d4a19`.
- **Review:** `research/day-08/advisor/PHASE_CLOSE_D08_review_v1.md`, SHA-256 `3a1a5f32d024e9fb77bc434e25362da34f0a982108556e6d1eb3c5e0b28781ab`.
- **Decision received: ACCEPT (0.85).** The researcher verified both hashes with `sha256sum`.
- **Mirror:** `orchestration/advisor-exchanges/X-D08-S03-0004/` (`envelope.yaml`, `response.md` verbatim, `checksums.sha256`).

**The researcher adopts Q1–Q8 as binding.** Corrections D8-C17 to D8-C22 are appended below.

## Q1–Q8: what was recorded

- **Q1.**
  - E046 remains champion; `models/champion/CURRENT.json` is unchanged and there is no `champion_change` event.
  - **H038 v2: REJECT.** E051 and E052 are labelled REJECT, with the review's notes, in `runtime/ledger.sqlite` and `experiments/ledger.jsonl`.
  - **Rule 10's list gains E051's configuration** (STATE).
- **Q2.**
  - **H: closed (H8).** The task ledger's last `holdout_access` is 2026-10-04T17:57:38Z, and its last unmasking event is E050's (2026-10-04T22:01:39Z). After the `reopened` event there are only the E051 and E052 allocations.
  - **No Day 8 upload; E050 stands** (`f0dc2c7c…06e8`).
- **Q3.** INC-0023 records the options offered and the owner's answers, verbatim, with bounded UTC times.
  - The choices were among research items, so INC-0023 is open, and DAY_SUMMARY's G3 line is amended.
  - INC-0023 states that one offered option (exchange 3, option 2) was a route around a pre-registered rule.
  - **From now on, the only question put to the owner is "continue or refreeze".**
- **Q4.** Incidents:
  - **INC-0019 is closed,** with the closure section the review requires.
  - **INC-0018 (D7) is recorded as closed here and in STATE.** Its own condition was met by X-D08-S01-0001 and X-D08-S03-0001 (D). The file stays unedited (ruling (D)).
  - INC-0017 and INC-0018 (D8) stay open until the last Day 8–12 phase close.
  - INC-0004, INC-0009 and INC-0010 stay open. On INC-0009, E051 and E052 were never mirrored.
- **Q5 and Q6** are adopted as written. **The owner's branch decision is pending** and is appended here when made.
- **Q7.** The end-of-phase report to the owner states:
  - no promotion; E050 stands;
  - INC-0022, D8-C14, D8-C15 and D8-C18;
  - the decision: continue (within Q5) or refreeze, with P(promotion) ≈ 0.06.

  D8-C15 was first told to the owner in chat after the proposal (2026-10-07, about 21:46Z). The report repeats it plainly.
- **Q8. The Advisor-context exposure, recorded.**
  - In this exchange the Advisor opened INC-0018 (D7). That file holds the leaderboard figure disclosed on 2026-10-04 (INC-0020), and the Advisor's attempt to mask it failed. The figure therefore reached the Advisor's context a second time (first: X-D08-S03-0001, 2026-10-06).
  - It is not repeated in any record and is used by no ruling.
  - **The researcher did not see it in this exchange.** The Advisor's response states that it is not repeated, and the researcher did not open INC-0018 (D7).
  - The external evaluation lists this exchange beside X-D08-S03-0001.

## Corrections (appended; no completed record is edited)

- **D8-C17. Snow.**
  - "Cannot be learned on any fold" (PHASE_CLOSE_D08 step 3; DAY_SUMMARY §1; `weather_LTFM_coverage.md` Consequence 1) is wrong as stated.
  - R1–R3, S1 and S1c train on February and March 2025 (270 LTFM snow reports). W1 and W1c, the only folds whose validation month has snow, have 2 and 0 snow reports in training.
  - So **no fold can both learn and score a snow effect.** The consequence for criterion 2 is unchanged.
- **D8-C18. The reverted known-row reading.**
  - (i) E051 analysis § Ruling (E): the known rows go against the candidate on R1 and S1 only. On R2 they favour it (fold +1.24e8 s², known rows −2.24e8 s²). Reverting them moves R2 to +3.90 s, with q10 −0.08 s.
  - (ii) The reverted computation fails criterion 2 by itself (2 WINs). Its R1 and S1 WINs come from deleting the candidate's losses on known rows.
  - (iii) DAY_SUMMARY §9.2, the proposal's "case against" 5 and the journal's "R1 and S1 would be WINs" are read with (i) and (ii). **No computation on record passes H038 v2.**
- **D8-C19. The item 1 look.**
  - It tested 18 signatures, not 15.
  - The ratio test is vacuous for the hour- and day-shift signatures, so only the 30-row floor applied there.
  - Pooled across the nine airports, "block 1 h before AOBT_3" covers 30 of 554 non-LIRF tail rows. Its oracle stake is about 0.8 s of all-rows RMSE.
  - `conventions.md`'s last sentence reads: "No tested signature explains the non-LIRF tail; the look does not show what those rows are."
- **D8-C20. Weather is not a lead.** DAY_SUMMARY §9.3 and the coverage note's restricted-candidate sentence are corrected by the review's finding 2: no implementable or oracle restriction reaches −1.0 s in both pilots.
- **D8-C21. The E051 records.**
  - The decision labels (Q1).
  - `range_check.py E051` was pre-registered, and its output was never recorded. The analysis used `mixture_analysis.py`'s subgroup counts instead; by the mixture check, the other rule 7 cells equal `range_check_E046.json`. Commit `7cb6ffd`'s message lists "range".
  - G5 (b) mechanism-population ΔRMSE (subgroup RMSE, E051 minus E046), with spread 0: R1 −237.8, R2 +177.5, R3 −2,619.0, S1 −315.1, W1 −6,510.1, S1c −669.7, W1c −9,586.4 s.
- **D8-C22. Clerical.**
  - DAY_SUMMARY §3: "a factor of 6 or more" reads "5.6 or more" (R2).
  - STATE's "Updated" and Days 8–12 section stamps (2026-10-06T18:57:28Z) preceded content dated 2026-10-07. They are re-stamped in this commit.
  - The synthetic weather tests do not cover the `bdcbb83` fix (trailing-space sky codes, VV).

## The owner's branch decision (2026-10-07T22:15:12Z; appended)

- **Owner (verbatim, chat, D08-S03).** The chat UTC was not measured; the reply came after commit `ba14338` (2026-10-07T22:13Z) and before this entry.
  > Continue with Day 9-12 Handoffs
- **Reading: Branch B (Q5).** Days 9–12 continue, within Q5's bounds B1–B5. "Handoffs" is read as a request for the hand-over document that opens Day 9: `docs/reproducibility/HANDOFF_D08.md`.
- **Not authorized by this decision:**
  - any allocation before a Day 9 proposal is reviewed;
  - anything Q5 B1 excludes.
- **Next:**
  - D08-S03 ends.
  - Day 9 opens on `day-9` from `main`, after the content-neutral merge of `day-8` (Q5, Branches).
