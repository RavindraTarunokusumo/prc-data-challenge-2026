# Acknowledgement: PHASE_CLOSE_D09 v1 (exchange X-D09-S01-0001)

*Written 2026-10-08T18:08:41Z (measured with `date -u`).*

- **Proposal:** `research/day-09/proposals/PHASE_CLOSE_D09_v1.md`, SHA-256 `6068b608c8e123efc7b9b8f83be2ebc98ecd4ab039dc3ab19e9aed28ebf355bd`.
- **Review:** `research/day-09/advisor/PHASE_CLOSE_D09_review_v1.md`, SHA-256 `e27d4fc3e7e3094250384c20296a21eba3f0a0f9e7fb4acde2a41586a50ea7ee`.
- **Decision received: ACCEPT (0.80).** The researcher verified both hashes with `sha256sum`.
- **Mirror:** `orchestration/advisor-exchanges/X-D09-S01-0001/` (`envelope.yaml`, `response.md` verbatim, `checksums.sha256`).

**The researcher adopts R1–R6 as binding.** This is the last Day 8–12 phase close: the project refreezes, with **no new upload, and E050 stands.**

## B5 items

- **H8 ledger check** (verified by the Advisor):
  - the last `holdout_access` is 2026-10-04T17:57:38Z;
  - the last unmasking event is E050's;
  - after `reopened`, the ledger has only the E051 and E052 allocations.
- **Look count:** 2 (E051, E052).
- **G1:** waived (INC-0017).
- **Delegation:** none.

## D9-C1 to D9-C14: where each was applied

| Correction | Applied in |
|---|---|
| D9-C1: the pilot is untested in a candidate's form, not refuted | DAY_SUMMARY D9 §1 (in place); `research/day-09/eda/pilot_taxistate.md` (appended); FINAL_REPORT §9.2; PROJECT_SUMMARY (Day 9 row, extension paragraph) |
| D9-C2: INC-0024's evidence rests on the researcher's statement | DAY_SUMMARY D9 §5 (in place); INC-0024 closure (appended); FINAL_REPORT §9.4; PROJECT_SUMMARY ("Things that went wrong") |
| D9-C3: clerical (pilot note, the G3 line, STATE) | pilot note (appended); DAY_SUMMARY D9 G1 line (in place); STATE (R4) |
| D9-C4: §9.1, cloud and laptop sessions | FINAL_REPORT §9.1 |
| D9-C5: §9.2, the Day 9 row and the weather row | FINAL_REPORT §9.2 |
| D9-C6: §9.3, the upload as the owner's report | FINAL_REPORT §9.3 |
| D9-C7: §9.4, INC-0020's reading, the error list as a selection, D8-C18 and D9-C2 | FINAL_REPORT §9.4 |
| D9-C8: §9.6, the INC-0024 exception, D08-S02's missing records, IEM licence | FINAL_REPORT §9.6 |
| D9-C9: the upload as the owner's report, and the standing disclosures | PROJECT_SUMMARY ("The result"; "Things that went wrong"; "By the numbers") |
| D9-C10: roles (FINAL_REPORT §1 wording; INC-0015, INC-0023; delegation; INC-0003/0004; the Advisor's scope) | PROJECT_SUMMARY ("How the work was organised") |
| D9-C11: Day 3 not credited to congestion (D3-C1) | PROJECT_SUMMARY (Day 3 row) |
| D9-C12: U6 in the opening; the "models, not the file" caveat under the table | PROJECT_SUMMARY ("In one paragraph"; "The result") |
| D9-C13: only record-supported statements about errors | PROJECT_SUMMARY ("Things that went wrong") |
| D9-C14: the Day 8 and Day 9 rows | PROJECT_SUMMARY (the Day 8 and Day 9 rows) |

## Records under R1

1. **Drafts, corrected in place:** DAY_SUMMARY D9, the §9 draft and PROJECT_SUMMARY.
   - The §9 draft was appended unchanged as `FINAL_REPORT.md` §9, and the draft file was removed.
   - §§1–8 are unchanged: the diff against the previous commit has no removed line.
2. **Completed records, appended:** the pilot note, the incidents and STATE.
3. **DAY_SUMMARY D9 and PROJECT_SUMMARY are marked FINAL.**
4. **Incidents (R3):**
   - closed: INC-0017 (final upload record), INC-0018 (D8) (delegation: none), INC-0023 and INC-0024 (with D9-C2);
   - open: INC-0004, INC-0009 and INC-0010.
5. **The `frozen` event (R2)** is written after this acknowledgement, in the same commit.
6. **R6.** The applied texts add no figure from the review's table in Scientific Validity (a). D9-C1 is not turned into a claim that the block helps or would have passed.
