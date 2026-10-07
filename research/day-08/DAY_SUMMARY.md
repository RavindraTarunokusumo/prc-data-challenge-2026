# Day 8 summary: the first reopened phase (FINAL; phase close X-D08-S03-0004 ACCEPT; H closed (H8); E046 remains champion; no Day 8 upload)

*Written 2026-10-07T21:44:22Z (measured with `date -u`), D08-S03, owner's laptop, branch `day-8`. Marked FINAL after the phase close, with D8-C14 to D8-C22 applied in place; the acknowledgement holds their full text.*

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

**G1 status:** waived by the owner (INC-0017 amendment). No G2 breach is recorded in Day 8, and no challenge page was opened in D08-S03. **G3: INC-0023** records the owner's choices among researcher-written research options, including one option that offered a route around a pre-registered rule (Q3).

## 1. The Day 8 question and its answer

**Question (owner, INC-0017):** can the champion's development error be lowered materially in Days 8–12?

**Answer for Day 8: no candidate is promotable.** E046 stays champion, and there is no new upload (G7 default).

The phase tested three ideas:

| Idea | How it was tested | Outcome |
|---|---|---|
| **H038 v2:** a convention mixture for LIRF's NM-missing subgroup (agenda item 2) | Design pilot, then E051 (candidate) and E052 (reproduction), on the frozen development folds | Development mean 294.32 against 314.42 (−20.10 s, q95 −2.98). **Criterion 2 not met:** one WIN (R3, carried by its known rows); S1 TIE. Not promotable. |
| **External weather** (agenda item 3; INC-0019) | Coverage check, then a design-month pilot with a pre-registered rule | LTFM snow is almost all in February and March 2025, so no fold can both learn and score a snow effect (D8-C17). All-airport pilot: +1.43 / −0.48 s. **The rule (≤ −1.0 s in both pilots) is not met.** Not pursued. |
| **Recording conventions beyond LIRF** (agenda item 1) | Design-month look at 18 signatures (D8-C19), with a pre-registered rule | **No signature meets the rule at any of the nine airports.** Closed with no lead. |

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
| E051 | H038 v2 | candidate | COMPLETE, 121.5 s. Dev 294.32. Criteria 1, 3, 4 (decisive reading), 6 and 8 met; **criterion 2 not met**. **REJECT** (Q1). |
| E052 | H038 v2 | reproduction (seed 43) | COMPLETE; byte-identical to E051; criterion 6 PASS. **REJECT** (as the reproduction). |

**Rule 15 (G5) (a), the look count:** E051 is look 1, E052 look 2 (Days 1–7 baseline: 44). No other Day 8 analysis read a validation-month target. The weather pilot and the item 1 look read design months only.

**Rule 15 (b) and (c):** in `experiments/E051/analysis.md` § Rule 15. Every |ΔRMSE| exceeds the fold's draw spread by a factor of 5.6 or more (D8-C22). The mechanism-population ΔRMSE is in D8-C21. The footprint is as H038 v2 § Rule 15 (c), with D8-C7 to D8-C9.

## 4. Analyses without an experiment ID (design months only)

| Analysis | Pre-registration | Targets read | Outcome |
|---|---|---|---|
| H038 design pilot | `H038_params.yaml` (9f653a9) | 2025-01, 04, 05, 06, row level | supported the proposal (X-D08-S03-0001) |
| LTFM weather coverage | none needed (weather only) | none | snow: 258 reports in February 2025 (W1 validation), 2 in W1's training months, 270 in the training months of R1–R3, S1 and S1c (D8-C17) |
| Weather design pilot | `WX_pilot_params.yaml` (d506516) | 2025-01, 04, 05, 06, row level | rule not met (+1.43 / −0.48 s) |
| Item 1 conventions look | rule in the script's docstring (a37f95e) | 2025-01, 04, 05, 06, row level | no finding |

Weather pilot segment readings, reported only:
- bulk −1.27 / −1.17 s;
- tail +71.61 / +12.72 s;
- EHAM −10.62 / −6.09 s.

A restricted weather candidate would choose its population after seeing these readings (rule 10). **No implementable or oracle restriction reaches −1.0 s in both pilots** (D8-C20; the review's finding 2), so weather is not a lead.

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
- **D8-C17 to D8-C22 (the phase-close review).** Their full text is in `research/day-08/acks/PHASE_CLOSE_D08_ack_v1.md`.
  - **D8-C17:** snow (above).
  - **D8-C18:** E051's reverted known-row reading is weaker than the analysis said. On R2 the known rows favour the candidate, and the reverted computation fails criterion 2 by itself. No computation on record passes H038 v2.
  - **D8-C19:** the item 1 look tested 18 signatures, and its ratio test is vacuous for the shift signatures.
  - **D8-C20:** weather is not a lead.
  - **D8-C21:** E051's labels, the missing `range_check.py E051` output, and the mechanism-population ΔRMSE.
  - **D8-C22:** clerical items.
- **D8-C16 (new). Clerical.**
  - `prc.weather.reports` was fixed after the weather pilot's parameters were committed (d506516) and before the pilot ran. The fix was a polars ShapeError in the ceiling expression, plus stripping sky codes. Feature definitions did not change.
  - `weather_reports_manifest.json` records `code_dirty: true`, because the manifest file itself was untracked when the table was built.
  - `conventions.md` cites its pre-registration commit by message only; the commit is a37f95e.

## 8. Delegated work (G11; INC-0018)

None.

## 9. Open questions

1. **Whether Days 9–12 continue or the project refreezes.** This is the owner's decision, and the only question put to the owner (Q3).
   - **If Days 9–12 continue (Q5),** no Day 8-motivated candidate is admissible:
     - no change to the LIRF NM-missing subgroup's predictions;
     - no weather;
     - no non-LIRF convention candidate.
   - **Any other candidate** is designed on design months only, with its rule committed before its pilot. It leaves E046's subgroup unchanged or carries the extended known-row reading, and finishes its SUBMIT path before 2026-10-11T12:00:00Z.
   - **The Advisor's estimate:** P(promotion) ≈ 0.06.
2. **E051's reverted-known-row reading** is not a lead (D8-C18).
3. **Weather** is not a lead (D8-C20). The data is kept. Any later use needs the IEM licence settled, a new owner decision and a reviewed proposal (INC-0019 closure).

## 10. Phase close

**X-D08-S03-0004: ACCEPT (0.85).**
- Review: `research/day-08/advisor/PHASE_CLOSE_D08_review_v1.md`.
- Acknowledgement: `research/day-08/acks/PHASE_CLOSE_D08_ack_v1.md`, which adopts Q1–Q8.

| | |
|---|---|
| Champion | **E046** (unchanged); development mean 314.42 s |
| Best Day 8 run | E051, development mean 294.32 s (REJECT: criterion 2) |
| Previous champion | E033, development mean 438.87 s |
| H | closed (H8) |
| Upload | none in Day 8; **E050 stands** (`f0dc2c7c…06e8`) |
| Incidents | INC-0019 closed; INC-0018 (D7) closed (Q4); INC-0023 opened (Q3) |

**Owner's branch decision (continue or refreeze):** pending. It is appended to the acknowledgement when made.
