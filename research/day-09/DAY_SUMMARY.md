# Day 9 summary: the last reopened phase (DRAFT for the phase close X-D09-S01-0001; refreeze)

*D09-S01, owner's laptop, branch `day-9` (from `main` `3e85b4c`, the content-neutral merge of `day-8`).*

**Provenance:**
- The researcher is `claude-opus-5-5`. The Advisor is the `advisor` subagent (definition `30fff5dd3c54`).
- **No delegation** (G11; INC-0018). The delegated-work list is empty.
- Owner interventions:
  - "Merged, start Day 9";
  - "I didn't tell you to run yet. Cancel run and wait." and then "Go" (INC-0024);
  - the refreeze: "Alright, let's wrap up the experiment. [...]" (INC-0017 amendment).
- Environment: rule L v2 item 6 (SESSION_START). Another process held 2,973 MiB of GPU memory at the start; no GPU work ran.

**Standing disclosures (every Day 8–12 record):**
- Leaderboard isolation for Days 8–12 rests on no recorded commitment (G1 (a)–(c) waived).
- What was known at reopening is not stated.
- E050's upload is unverified (INC-0017).
- A leaderboard figure was disclosed to the researcher on 2026-10-04, and it is not used (INC-0020). It also reached the Advisor's context in X-D08-S03-0001 and X-D08-S03-0004.

**G1 status:** waived (INC-0017). No G2 breach. No challenge page was opened. G3: INC-0023 (Day 8) stands. In Day 9 the owner was asked only "continue or refreeze" (Q3).

## 1. The Day 9 question and its answer

**Question (HANDOFF_D08 §4.1):** does the airport's recent realised taxi state add information beyond the row's own `d_aobt3` and the congestion counts? The state is measured by:
- the mean taxi-in of recently in-blocked arrivals;
- the mean `MVT − AOBT_3` of other recent departures.

**Answer: not by the pre-registered rule.**

| Pilot | Predicted month | Reference RMSE | With taxi state | Difference | P features only (reported) |
|---|---|---|---|---|---|
| P1 | 2025-06 | 373.26 | 376.15 | **+2.90** | +2.21 |
| P2 | 2025-05 | 327.05 | 323.96 | **−3.10** | −0.93 |

- The rule needed at least 1.0 s better in both pilots. **H039 was not written.**
- Segments, reported only: NM-present −1.00 / −1.15 s; LIRF +18.21 / −17.05 s; tail +76.34 / −75.39 s.
- HANDOFF_D08 §4.3's stop rule applied, and **the owner chose to refreeze.**

## 2. What was built

| Component | Where | Notes |
|---|---|---|
| Taxi-state block | `prc.taxistate`, `prc.features.TAXISTATE_NUMERIC`, `tests/test_taxistate.py` (14 tests) | 5 P and 2 T columns. The own row is removed exactly, and P features are invariant to the row's own takeoff. No DEP block time or target is used. |
| Design pilot | `scripts/pilot_taxistate_D09.py`, `research/day-09/proposals/TX_pilot_params.yaml` | Design months only. Parameters and rule committed at `0969550`, before the run. |

Tests: 194 pass. Lint clean.

## 3. Experiments

**None.** No E### was allocated in Day 9. Days 8–12 looks (G5 (a)): **2** (E051, E052). The pilot read design months only.

## 4. Champion, holdout, upload

- **Champion: E046** (unchanged; development mean 314.42 s).
- **H: closed (H8).** No holdout access and no unmasking event after Day 7. To be verified by the phase close.
- **Upload (G7): none.** No candidate was promoted in Days 8–12. **E050 stands** (`f0dc2c7c…06e8`).

## 5. Errors and corrections (kept)

- **INC-0024: the researcher started the pilot without the owner's go-ahead.**
  - The owner stopped it. It ended during the first split, with no output, and no figure was seen.
  - The pilot then ran unchanged on the owner's "Go".
  - From then on, no run starts without the owner's explicit go-ahead.
- No other correction yet; the phase close may add some.

## 6. Delegated work (G11)

None.

## 7. Phase close

Requested in `research/day-09/proposals/PHASE_CLOSE_D09_v1.md` (X-D09-S01-0001), as the last Day 8–12 phase close (refreeze).
