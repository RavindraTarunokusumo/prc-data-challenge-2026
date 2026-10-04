# Day 7 summary: final synthesis, submission, freeze (DRAFT for phase close X-D07-S01-0003)

**Session:** D07-S01, on branch `day-7`, on the owner's laptop.

**Provenance:**
- The researcher is `claude-opus-5-5` (`--effort high`). The Advisor is the `advisor` subagent (definition `30fff5dd3c54`). No delegation.
- Owner interventions: INC-0014 (run window 21:00–22:00 CEST on 2026-10-03) and INC-0015 (the decision to test the routing candidate; window 02:00–03:00 CEST on 2026-10-04).
- Environment: rule L v2 item 6 throughout (manifests).

## 1. The Day 7 question and its answer

**Question (brief §3):** produce the submission from the champion's procedure, synthesise the project, and freeze.

**Answer so far:**
- **The champion's SUBMIT procedure works and gives a complete submission** (E042–E044). The file passes every blocking check and raises no sanity flag (§3). SHA-256: `d57ff7db7dfa34e13934aa524464ea13dbe9f5f904fae400a85f87e62c95af73`.
- **A routing candidate (H035, E046) meets every development criterion** at a development mean of 314.42 s, against E033's 438.87. Its gain is **a bet that LIRF's block-at-schedule recording convention persists in 2026**, with a downside of similar size (U6). It is promotable only through a WIN on the Day 7 holdout access (objection F, U7). Its outcome is decided at this phase close.

## 2. What was built

| Component | Where | Notes |
|---|---|---|
| Submission formatter | `scripts/make_submission.py`, `tests/test_make_submission.py` | Target-free. I1–I5 integrity checks; template order and dtypes; nearest-integer rounding only. `override` mode and `--tag` (a second file never overwrites the first). |
| Override combiner | `prc.blending.override`; worker `model: override`; `tests/test_worker.py` | One target-free subgroup's rows come from a second experiment's stored predictions. Fits nothing. |
| Launchers | `research/day-07/sessions/D07-S01/run_window.sh`, `run_window_2.sh` | INC-0012's pinned logic; the second takes a two-argument route check. |

## 3. Experiments

| Run | Proposal | Role | Outcome |
|---|---|---|---|
| E042 | H031 v1 | SUBMIT fit, E029's config (LightGBM half) | COMPLETE, 280 s |
| E043 | H032 v1 | SUBMIT fit, E031's config (CatBoost GPU half; one draw) | COMPLETE, 419 s; route check PASS; resolved parameters equal E031's |
| E044 | H033 v1 | SUBMIT blend 0.5/0.5 | COMPLETE; I1–I5 pass; no flag; **the submission (unless H035 is promoted)** |
| E045 | H034 v1 | E020's config, laptop instance | reproduces E020 to 0.0 s per fold |
| **E046** | **H035 v1** | **candidate** | **dev 314.42; −124.45 s against E033, 7/7 WIN; criteria 1–4, 6 and the criterion 8 rule met; objection F open** |
| E047 | H034 v1 repro | criterion 6 component | byte-identical to E045 |
| E048 | H035 v1 repro | criterion 6 | PASS |
| E049, E050 | H036, H037 v1 | the candidate's SUBMIT fits | **DEFERRED** (572 s left against a 600 s guard); ALLOCATED |

**SUBMIT sanity (E044):**
- January 2026 sits close to two pre-registered limits without crossing either: the mean prediction is 1,062.8 s against a limit of 1,070; 0.219 % of predictions are above 3,600 s against a limit of 0.25 %.
- Both halves agree on that level (1,062.7 and 1,062.9 s).
- January 2026's inputs are unlike any 2025 winter month: mean schedule delay 36.4 min against January 2025's 30.0, and 13.5 % of departures more than 1 h late against 9.1 %.
- July's per-airport means sit within 69 s of S1's.
- The D3-C3 rows (435 above 3 h, 92 above 5 h): none is predicted above 3,600 s.

## 4. The routing candidate in plain words

- E033 sends the 383 ranking-month rows of LIRF departures without an NM match to a ridge fitted on a winsorised target. On 2025, most such rows with long taxi-out values are block-at-schedule records: the "taxi-out" is takeoff minus scheduled time.
- The unrouted LightGBM learns that convention; the ridge cannot. On every development fold this is worth 27–213 s of all-rows RMSE, and the whole gain sits on a few dozen tail rows per fold.
- **The bet (U6, corrected):**
  - the candidate keeps its advantage only if the 2026 convention rate stays above about 20–57 % of its 2025 level (λ*, by fold);
  - if the convention vanished, it would lose 0.25–1.3 times its 2025 gain;
  - Day 3's wording ("would lose only if the convention nearly vanished") understated this; so did the researcher's message to the owner.
- **The development folds cannot test the bet:** they recompute Day 3's recorded contrast. December (H) is the only fresh month, and both ranking months' subgroup delay tails lie above every 2025 month.

## 5. Champion

E033 at the phase opening. The phase close decides between E033 (E044's file) and H035 (E046; E050's file), under U7.

## 6. Holdout

Day 7 has one access. Requested: `holdout_check.py E046 E033` (U7's statistic), named by this phase close.

## 7. Missed or corrected predictions (kept)

- **D7-C1:** H031 §Batch's "2026-07's mean prediction above 2026-01's" and H033's mean ranges (Jan 975–1,000, Jul 1,010–1,040) were all missed (1,062.8; 1,002.0). The Advisor's E042 range was missed as well.
- **D7-C2:** the created times of H031–H033 (17:20:00Z) were written ahead of the commit that contains them (17:00:11Z) (S9). The H034–H037 headers carry the measured time.
- **D7-C3:** the forward-risk wording, corrected by U6:
  - H035 §Batch, INC-0015's context, and the researcher's question to the owner ("it would only lose if the quirk nearly vanished");
  - Day 3 (e) carries the same error, and the Advisor corrected its own record.
- **D7-C4:** E045 (1,196 s) and E047 (1,339 s) ran past their 1,100 s guards (forecast 13–17 min). This deferred E049 and E050.
- **D7-C5:** in chat, the researcher first told the owner that January 2026 had "the longest schedule delays of any month in the data". That is wrong: July 2025 is higher (38.5 against 36.4 min). The records state it correctly (E044 analysis).

## 8. Open questions (none blocks the freeze)

1. The convention rate in 2026 (unobservable: block time is blanked in the ranking months).
2. The SUBMIT procedure's accuracy (untestable without truth).
3. D3-C3's January exposure; the 1,000-iteration budget; neural models (not attempted); a causal-only variant (not built).

## 9. Phase close

Pending (X-D07-S01-0003).
