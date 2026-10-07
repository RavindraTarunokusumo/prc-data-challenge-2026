---
schema: phase-close-proposal-v1
proposal_id: PHASE_CLOSE_D08
proposal_version: 1
day: 8
session: D08-S03
exchange_id: X-D08-S03-0004
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-10-07T21:45:38Z
---

# Day 8 phase close

**Standing disclosures:**
- Leaderboard isolation for Days 8–12 rests on no recorded commitment (G1 (a)–(c) waived).
- What was known at reopening is not stated.
- E050's upload is unverified (INC-0017).
- A leaderboard figure was disclosed to the researcher on 2026-10-04, and it is not used (INC-0020).

## Request

1. **Adversarial review** of the Day 8 decisions. Try to show that the champion is wrong, or that a Day 8 reading was mis-scored.
   - **E046 remains champion.** H038 v2 (E051) fails criterion 2 as frozen: one WIN (R3, carried by its known rows), S1 a TIE.
   - **Weather (agenda item 3) is not pursued.** The design pilot's pre-registered rule is not met.
   - **Agenda item 1 is closed with no lead.** No signature meets the look's pre-registered rule.
2. **Holdout:** "H: closed (H8)". No access and no December target read.
3. **Upload (G7):** none in Day 8. There is no Day 8 champion and no Day 8 SUBMIT fit. E050 stands.
4. **Corrections D8-C14 to D8-C16** (DAY_SUMMARY §7), and any the Advisor finds, appended before `DAY_SUMMARY.md` is finalised.
5. **Incidents:**
   - **INC-0019 closes.** The weather decision is made: tested, rule not met, and the owner accepted dropping it in chat on 2026-10-07. The bronze data and manifests are kept.
   - INC-0017 and INC-0018 stay open: they close at the last Day 8–12 phase close.
   - INC-0004, INC-0009 and INC-0010 stay open. On INC-0009, E051 and E052 were not mirrored.
6. **A ruling on what Days 9–12 may do,** or whether the project should refreeze. The owner decides whether to continue; the Advisor is asked for the scientific bounds:
   - whether any Day 8 reading may motivate a Day 9 proposal (E051's reverted-known-row reading; the weather bulk reading);
   - under which footprint, given G5 (c) and rule 10.

## Decisions under review

| Step | Item | Decision | Evidence |
|---|---|---|---|
| 1 | E051 (H038 v2 candidate) | criterion 2 not met; not promotable | `experiments/E051/analysis.md`; `research/comparisons/E051_vs_E046*.json`, `E051_vs_E033.json`, `E051_vs_E028.json`, `mixture_check_E051.json` |
| 2 | E052 (reproduction) | byte-identical; criterion 6 PASS | `experiments/E052/analysis.md`; `research/comparisons/repro_E052_of_E051.json` |
| 3 | Weather coverage (LTFM) | a snow mechanism cannot be learned on any fold | `research/day-08/eda/weather_LTFM_coverage.md` |
| 4 | Weather design pilot | rule not met (+1.43 / −0.48 s) | `research/day-08/proposals/WX_pilot_params.yaml` (d506516); `scripts/pilot_weather_D08.py`; `research/day-08/eda/pilot_weather.json` |
| 5 | Item 1 conventions look | no finding | `scripts/eda_conventions_D08.py` (a37f95e); `research/day-08/eda/conventions.md`, `conventions.json` |

Summary: `research/day-08/DAY_SUMMARY.md` (draft). Journal: `research/EXPERIMENT_JOURNAL.md` (Day 8 sections). Ledger: `experiments/ledger.jsonl` (E051, E052).

## Case for the decisions

- **E051's reading follows the frozen computation** and rulings (E), (G) and (E)(vi). The known-row reversion is reported only, and no threshold or population moved.
- **Both pilots' rules were committed before their runs** (commit order is in the git log). The readings are the rules' own outputs.
- **The pilots and the look read design months only,** so G5 (a)'s look count stays at 2.
- **The weather pilot's ten-airport coverage is 100 %,** and its availability rule (report observed at or before t_off − 10 min) is conservative for METAR issue times.

## Case against: where I may be wrong

1. **The weather pilot is one learner and one configuration.** It is a plain LightGBM on FS2, not E046's routed blend with CatBoost. CatBoost's handling of 16 extra columns might differ. The rule was set for the pilot learner, and I accepted that risk before running it.
2. **The pilot's tail loss may be noise in a few hundred rows.** P1's +71.61 s on 395 tail rows decides its sign. The bulk gain (about −1.2 s in both pilots) is consistent. A "bulk-only weather" candidate is a post-hoc population choice (rule 10), so I did not propose one. The Advisor may judge the rule too blunt for a feature block.
3. **Four design months are a small and seasonally narrow sample** (no July, no autumn). The weather effect in winter and summer extremes is unsampled. The only winter design month, January 2025, had no LTFM snow.
4. **Item 1's look tests 15 signatures at 9 airports** with a 30-row floor. Small airports' tails (EDDM 19, LSZH 13 tail rows) cannot reach it. It shows the absence of a large convention, not of a small one.
5. **E051:** the reverted reading (R1 and S1 WINs) suggests that the mixture's structure may be right while the frozen bootstrap cannot see it on few rows. The frozen rules govern, but the Advisor may want this stated more strongly for Day 9.
6. **Process errors this phase:** INC-0022 (the missing H fold); D8-C14 (the sandbox misdiagnosis); D8-C15 (the wind mechanism overstated to the owner before a fetch); D8-C16 (clerical).

## Known weaknesses to attack

- `prc.weather` and the pilot scripts were written and reviewed by the researcher only.
- The weather table's `code_dirty` flag (D8-C16).
- The IEM licence fit (INC-0019: "recorded as a check for the proposal, not as settled") was never settled, because no proposal followed.

## Resource Estimate

Read-only review. No holdout access, run or fit is proposed.

## Decision Requested From Advisor

ACCEPT (E046 remains champion; H closed (H8); no Day 8 upload; the readings stand) | REVISE | REJECT | HOLD
