# Day 8 summary: the first reopened phase (DRAFT for the phase close X-D08-S03-0004)

*Written 2026-10-07T21:44:22Z (measured with `date -u`), D08-S03, owner's laptop, branch `day-8`.*

**Sessions:**
- D08-S01 (cloud): phase-open request, ACCEPT.
- D08-S02 (cloud): G1 waiver, `reopened` event, INC-0019.
- D08-S03 (laptop): all research below.

**Provenance:**
- The researcher is `claude-opus-5-5`. The Advisor is the `advisor` subagent (definition `30fff5dd3c54`).
- **No delegation** (G11; INC-0018). The delegated-work list is empty.
- Owner interventions:
  - INC-0017: the reopening, G1 (a)–(c) waived;
  - INC-0019: the weather approval, and the fetch the owner ran from the owner's terminal;
  - INC-0021: H038's run window;
  - the owner's choices in chat on 2026-10-07: drop weather and look at item 1 ("Option 1, go ahead with the recording quirks look"), then close Day 8 ("Option 1, close Day 8").
- Environment: rule L v2 item 6 throughout (manifests).

**Standing disclosures (every Day 8–12 record):**
- Leaderboard isolation for Days 8–12 rests on no recorded commitment (the owner waived G1 (a)–(c)).
- What was known at the reopening is not stated.
- E050's upload is unverified (INC-0017).
- The Day 8 records written before the merge of `origin/day-7` stated that no leaderboard figure had been seen. That was wrong: one had been disclosed to the researcher on 2026-10-04 (INC-0020). It is not used.

**G1 status:** waived by the owner (INC-0017 amendment). No G2 or G3 breach is recorded in Day 8. No challenge page was opened in D08-S03.

## 1. The Day 8 question and its answer

**Question (owner, INC-0017):** can the champion's development error be lowered materially in Days 8–12?

**Answer for Day 8: no candidate is promotable.** E046 stays champion, and there is no new upload (G7 default).

The phase tested three ideas:

| Idea | How it was tested | Outcome |
|---|---|---|
| **H038 v2:** a convention mixture for LIRF's NM-missing subgroup (agenda item 2) | Design pilot, then E051 (candidate) and E052 (reproduction), on the frozen development folds | Development mean 294.32 against 314.42 (−20.10 s, q95 −2.98). **Criterion 2 not met:** one WIN (R3, carried by its known rows); S1 TIE. Not promotable. |
| **External weather** (agenda item 3; INC-0019) | Coverage check, then a design-month pilot with a pre-registered rule | LTFM snow is almost all in W1's validation month, so a snow mechanism cannot be learned on any fold. All-airport pilot: +1.43 / −0.48 s. **The rule (≤ −1.0 s in both pilots) is not met.** Not pursued. |
| **Recording conventions beyond LIRF** (agenda item 1) | Design-month look at 15 signatures, with a pre-registered rule | **No signature meets the rule at any of the nine airports.** Closed with no lead. |

Agenda item 4 (the CatBoost iteration budget) was not attempted. The phase-open review judged it "unlikely to be worth a phase" (G9).

## 2. What was built

| Component | Where | Notes |
|---|---|---|
| Convention mixture | `prc.models.mixture`, worker override, `scripts/mixture_check.py`, `mixture_analysis.py`, `known_row_check.py`, tests | H038 v2 |
| Weather fetch | `scripts/fetch_weather.py` | IEM ASOS archive, monthly bronze files, tracked manifests. Run by the owner. |
| Weather block | `prc.weather`, `scripts/build_weather.py`, `tests/test_weather.py` (6 tests) | 16 P-labelled columns. Latest report observed at or before t_off − 10 min, maximum age 3 h. Pure functions; nothing reads a target. |
| Pilots and looks | `scripts/pilot_mixture_D08.py`, `pilot_weather_D08.py`, `eda_conventions_D08.py` | Design months only (2025-01, 04, 05, 06). Parameters and reading rules committed before each run. |

Tests: 180 pass. Lint clean.

## 3. Experiments

| Run | Proposal | Role | Outcome |
|---|---|---|---|
| E051 | H038 v2 | candidate | COMPLETE, 121.5 s. Dev 294.32. Criteria 1, 3, 4 (decisive reading), 6 and 8 met; **criterion 2 not met**. Not promotable. |
| E052 | H038 v2 | reproduction (seed 43) | COMPLETE; byte-identical to E051; criterion 6 PASS |

**Rule 15 (G5) (a), the look count:** E051 is look 1, E052 look 2 (Days 1–7 baseline: 44). No other Day 8 analysis read a validation-month target. The weather pilot and the item 1 look read design months only.

**Rule 15 (b) and (c):** in `experiments/E051/analysis.md` § Rule 15. Every |ΔRMSE| exceeds the fold's draw spread by a factor of 6 or more. The footprint is as H038 v2 § Rule 15 (c), with D8-C7 to D8-C9.

## 4. Analyses without an experiment ID (design months only)

| Analysis | Pre-registration | Targets read | Outcome |
|---|---|---|---|
| H038 design pilot | `H038_params.yaml` (9f653a9) | 2025-01, 04, 05, 06, row level | supported the proposal (X-D08-S03-0001) |
| LTFM weather coverage | none needed (weather only) | none | snow: 258 reports in February 2025 (W1 validation) and 2 in W1's training months |
| Weather design pilot | `WX_pilot_params.yaml` (d506516) | 2025-01, 04, 05, 06, row level | rule not met (+1.43 / −0.48 s) |
| Item 1 conventions look | rule in the script's docstring (a37f95e) | 2025-01, 04, 05, 06, row level | no finding |

Weather pilot segment readings, reported only:
- bulk −1.27 / −1.17 s;
- tail +71.61 / +12.72 s;
- EHAM −10.62 / −6.09 s.

A restricted weather candidate would choose its population after seeing these readings (rule 10). None is proposed.

## 5. Champion: E046 (unchanged)

- Development mean 314.42. Its standing disclosures are unchanged (STATE): U6 (the convention bet), U7 (December only), rules 6 and 12, D7-C7 and the H exposure.
- **The submission stays E050's file,** SHA-256 `f0dc2c7c…06e8`. No Day 8 SUBMIT fit exists.

## 6. Holdout

**H: closed (H8).** No `holdout_check.py` run and no December target read. E051's H fold was predicted only (amendment A1).

## 7. Missed or corrected predictions, and errors (kept)

- **H038's misses** (E051 analysis): R2 gained nothing (+1.39 s, against −5 to −13 central); S1 was a TIE; the classifier was much better on the folds than in the pilot.
- **INC-0022:** E051's first arming was refused, because the configuration had no H fold. This was the researcher's error and the review's. Amendment A1 fixed it, and nothing ran.
- **D8-C14 (new). The weather-host diagnosis was wrong.**
  - Commit 930b788 and INC-0019's first D08-S03 amendment blamed the Claude Code sandbox for the TLS resets.
  - The session's shell has no sandbox. The resets are in the laptop's network path.
  - The owner reported that the script did not work for the owner either. The owner then changed something on the owner's side (not recorded here), and the owner's runs succeeded.
  - The researcher also asked to run one probe outside the sandbox, which the harness refused.
  - Corrected in INC-0019 (appended).
- **D8-C15 (new). The wind mechanism was overstated to the owner.**
  - In chat, the researcher said that wind sets the runway configuration, and that this made wind "the best use of the weather approval".
  - The departure runway is already a model input (`airport_runway`, FS0), and so is the realised taxi interval (`d_aobt3`, the T congestion block). Wind's runway channel was therefore largely represented already. The researcher noticed this while the owner's nine-airport fetch was running, and did not tell the owner until this record.
  - The pilot's outcome is consistent with this.
- **D8-C16 (new). Clerical.**
  - `prc.weather.reports` was fixed after the weather pilot's parameters were committed (d506516) and before the pilot ran. The fix was a polars ShapeError in the ceiling expression, plus stripping sky codes. Feature definitions did not change.
  - `weather_reports_manifest.json` records `code_dirty: true`, because the manifest file itself was untracked when the table was built.
  - `conventions.md` cites its pre-registration commit by message only; the commit is a37f95e.

## 8. Delegated work (G11; INC-0018)

None.

## 9. Open questions

1. **Whether Days 9–12 continue.** This is the owner's decision. The remaining agenda is thin:
   - item 2's variants are bounded by criterion 2 on few rows;
   - item 4 was judged unlikely to clear criterion 1.
2. **E051's reverted-known-row reading** (R1 and S1 WINs) cannot be credited under the frozen rules. Any follow-up is a new proposal that states this footprint.
3. **Weather:** the data is fetched and tested. The only lead is post hoc (bulk only).

## 10. Phase close

Requested in `research/day-08/proposals/PHASE_CLOSE_D08_v1.md` (X-D08-S03-0004).
