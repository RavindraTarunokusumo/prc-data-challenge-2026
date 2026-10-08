---
schema: phase-close-proposal-v1
proposal_id: PHASE_CLOSE_D09
proposal_version: 1
day: 9
session: D09-S01
exchange_id: X-D09-S01-0001
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-10-08T17:43:53Z
---

# Day 9 phase close and refreeze (the last Day 8–12 phase close)

**Standing disclosures:**
- Leaderboard isolation for Days 8–12 rests on no recorded commitment (G1 (a)–(c) waived).
- What was known at reopening is not stated.
- E050's upload is unverified (INC-0017).
- A leaderboard figure was disclosed to the researcher on 2026-10-04 and is not used (INC-0020). Envelopes cite INC-0020 instead of the files that hold it.

## Request

1. **Adversarial review of the Day 9 decision.** The taxi-state design pilot did not meet its pre-registered rule (+2.90 / −3.10 s), so H039 was not written. Check:
   - the pilot's design-month footprint;
   - the commit order: the rule at `0969550` before the run;
   - INC-0024, the first start without the owner's go-ahead, stopped with no output: whether the re-run under the same rule is clean;
   - that the block uses no blanked column.
2. **The refreeze (Q6 of X-D08-S03-0004, applied at Day 9).**
   - The owner ended Days 8–12 (INC-0017 amendment, verbatim).
   - **G7's rule:** no candidate was promoted in Days 8–12, so there is no new upload and **E050 stands.** No SUBMIT run exists to select among.
   - **Records after this review:**
     - a `frozen` task-ledger event citing INC-0017 and this exchange, with E050's path and hash;
     - STATE "Phase: FROZEN (Days 8–12 closed at Day 9)";
     - the session end;
     - the content-neutral merge of `day-9` into `main` (P7 (b)).
3. **H: closed (H8).** Please repeat the ledger check (B5).
4. **The final-report section** `docs/reports/FINAL_REPORT_D08_D12_draft.md` (G8, Q6). It is appended as §9 of `FINAL_REPORT.md` once accepted; §§1–8 stay unchanged. Please check it for overclaims, as Q6's failure mode warns.
5. **The owner's project summary** `docs/reports/PROJECT_SUMMARY.md`, which the owner asked for. It is plain-language and restates reviewed records. Please check that it adds no figure, interpretation or decision beyond them, and that it does not overstate.
6. **Incidents:**
   - **Close:** INC-0017 (the refreeze), INC-0018 (D8) (no delegation used), INC-0023 (disclosed in §9.4) and INC-0024 (practice adopted; disclosed).
   - **Stay open:** INC-0004, INC-0009 and INC-0010.
7. **B5 items:** the look count stays at 2; G1 is waived; no delegated work.

## Evidence

| Item | Path |
|---|---|
| Day 9 summary (draft) | `research/day-09/DAY_SUMMARY.md` |
| Pilot parameters and rule | `research/day-09/proposals/TX_pilot_params.yaml` (`0969550`) |
| Pilot script and output | `scripts/pilot_taxistate_D09.py`; `research/day-09/eda/pilot_taxistate.json`, `.log`, `.md` |
| Block and tests | `src/prc/taxistate.py`; `tests/test_taxistate.py` |
| Incidents | INC-0017 (amendment), INC-0023, INC-0024 |
| Hand-over plan | `docs/reproducibility/HANDOFF_D08.md` (§4.3, the stop rule) |
| Session start | `research/day-09/sessions/D09-S01/SESSION_START.md` |

## Case for the decisions

- **The pilot followed its committed rule.** The same rule shape decided the weather pilot in Day 8.
- **The stop rule was written before the pilot** (HANDOFF_D08 §4.3, at `a7e5026`).
- **The refreeze is the owner's decision,** taken on the only question allowed (Q3).

## Case against: where I may be wrong

1. **The pilot is a single-learner check on two months.** The NM-present gain (about −1 s in both pilots) is consistent. The all-rows sign is set by a few hundred LIRF tail and NM-missing rows. Since a full candidate would override the LIRF NM-missing subgroup from E045, those rows would not have taken the block's predictions. The rule was set on all rows, and I did not restrict it after seeing this (rule 10; INC-0023). The Advisor may say the rule's population did not match the eventual candidate's construction.
2. **The INC-0024 stop.**
   - The first process loaded silver, which contains design-month targets, and started fitting before it was stopped.
   - I claim that no figure was produced or seen: the log was empty, the truth join comes after the fits, and the process ran for about two minutes against P1's roughly two and a half.
   - I deleted the empty log before the re-run. Its contents were nothing, but deleting it was not append-only.
3. **The project summary is written for a lay reader.** Simplifications such as "constant guess" and "the largest single step" may lose the qualifications the records carry.
4. **The 194-test suite includes a test that reads development-fold truth** (`test_evaluator`). I ran the full suite during Day 9, as in earlier days. It is not an analysis, and it is not counted as a look.

## Resource Estimate

Read-only review. No run, fit, holdout access or upload is proposed.

## Decision Requested From Advisor

ACCEPT (Day 9 closed; refreeze; no new upload; E050 stands; §9 and the summary as corrected) | REVISE | REJECT | HOLD
