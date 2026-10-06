---
schema: advisor-review-v1
hypothesis_id: H038
proposal_version: 2
proposal_sha256: 3104c018121e46b1a7ba7aafcd453b5781ebe0da41d538ac38ffe9b50cfc294c
exchange_id: X-D08-S03-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-10-06T20:08:54Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.80).** v2 makes all six revisions of X-D08-S03-0001. The one unrequested launcher change is operational and sound. E051 and E052 may be allocated and run as written, within the scope below.

**Two rulings bind the analysis and the phase close.** Neither changes the run, the tooling or the launcher.
- **(G) Criterion 4's decisive reading is the proposal's sign test.**
  - The frozen tool and its test use the name "criterion 4 reading (a)" for a different rule: the convention rows must carry at least half of the gain.
  - On the pilot the two rules disagree in one split of two (P1, share 0.22). The proposal governs.
- **(E)(vi) The known-row reading also covers criterion 2's no-LOSS condition.**
  - Ruling (E) left one case open: a fold that is not a LOSS as frozen, but is a LOSS once its known rows are reverted.
  - W1's single dominant row makes this the natural failure pattern under the paired cluster bootstrap. If it occurs, the candidate carries G5's consequence.

**Two corrections** (D8-C11, D8-C12) are appended in the acknowledgement. No new version is needed.

**The six revisions.**

| # | Required by X-D08-S03-0001 | v2 | Verdict |
|---|---|---|---|
| 1 | Rule 8: tail and bulk per fold and twin; S1 at July's rate | Band table for all seven folds; S1 statement (tail −5 to −10 s; bulk +5 to −9 s, sign uncertain) | Met. Every cell recomputes |
| 2 | Criterion 4: a decisive share reading, **or** the claim restated so that reading (a) tests it; large-`d_sched` non-convention rows under Alternative Explanations | Claim restated (the second option); the alternative listed; c = 0 rows split by `d_sched`, reported as unattributed | Met in the proposal. The frozen tool labels the first option as reading (a): ruling (G) |
| 3 | Footprint with D8-C7 to D8-C9; whether the design used a known row | Restated; "No" | Met, consistent with the commit order |
| 4 | The known-row reading in tooling committed before the envelope | `known_row_check.py` at `a977bef`, with a synthetic test | Met. The implementation is correct |
| 5 | A tracked manifest for the component files | `mixture_check.py` records path, size and SHA-256; the launcher commits that JSON | Met |
| 6 | Restated probabilities; W1 consistent with its concentration | Restated and coherent (0.20 + 0.15 = 0.35); W1 decided by one row | Met |

**The launcher change (guards 1,500 s → 840 s) is acceptable** (Compute Review).
- The diff against the reviewed version (`903b5a48…`, `e310996`) is the two queue values only.
- The start rule, deferral, never-kill rule and checkpoints are unchanged.
- It answers an owner constraint, INC-0021, created after v1's envelope.

**Verified here (read-only).**
- **Hashes.**
  - The proposal (`3104c018…`), the launcher (`54ee5ab8…`) and the params file (`b22c02c1…`) match the envelope.
  - The tree is clean at `ce89aeb`.
  - The six frozen files match `config/frozen.json`. `.claude/agents/advisor.md` is `30fff5dd…0d19`, as in `config/agents.yaml`.
  - X-D08-S03-0001's mirror checksums verify.
- **What changed since `3c23aab`.**
  - Code: `scripts/known_row_check.py` (new), `scripts/mixture_analysis.py` (+12 lines), `scripts/mixture_check.py` (+10 lines), `tests/test_known_rows.py` (new).
  - Nothing under `src/` or `config/`. `pyproject.toml` and `uv.lock` (`efa4fd78…`) are unchanged.
  - The params file and the pilot script are unchanged since `9f653a9`.
  - INC-0020 is closed by an appended section and its status field, as earlier incidents were.
- **Tests and lint.**
  - The seven synthetic tests pass (`tests/test_known_rows.py` 2, `tests/test_mixture.py` 5). `ruff` is clean on the five changed files.
  - The full suite was not run: `test_evaluator` reads development-fold truth.
- **Stored files and ledgers.**
  - E046's eight prediction files match its manifest.
  - `runtime/ledger.sqlite` holds 50 rows, E001–E050, as does `experiments/ledger.jsonl` (G6).
  - The task ledger ends at `reopened`. Its last `holdout_access` is at 2026-10-04T17:57:38Z.
  - No E051 or E052 output exists.
- **Figures.**
  - The band table recomputes on all seven folds, from E046's fold SSE and the pilot's per-band SSE changes.
  - The W1 arithmetic recomputes:
    - E046's error on row 183903219 is about 75,640 s;
    - the break-even p is 0.423;
    - p = 0.3 / 0.5 / 0.8 gives +25.9 / −14.4 / −54.1 s.
  - The bulk and tail counts and the rule 12 counts match E046's analysis.
- **Code paths.**
  - FS2 holds departure rows only, so g's `ADEP_mvt == LIRF` filter selects LIRF departures.
  - `gbm.lightgbm` sets `deterministic=True` and `force_row_wise=True`.
  - `override_fitted` refuses any row-set mismatch.
- **Environment:** CPython 3.13.15 and `uv.lock` `efa4fd78…`, as in D08-S03's SESSION_START (rule L v2 item 6).
- **Secrets.** No credential pattern appears in the diff since `3c23aab`.

**What I did not do.**
- I read no target, block-time or December column, and loaded no silver.
- No feature build, fit, run, score, allocation, holdout script or formatter.
- I did not open the Day 7 files that hold the disclosed figure. No leaderboard figure entered this exchange.
- No challenge page, leaderboard or bucket.

**Governance note.**
- INC-0021 records that the researcher offered the owner a review waiver for an exploratory run, and that the owner declined (option 1).
- Policy is the owner's to set (G3), so asking was not a breach. Any waiver would itself have been a protocol deviation needing its own incident.
- No action is needed.

## Scientific Validity

### (A) Rule 8 (revision 1)

**The band table is right.**
- The pilot's per-row SSE changes are:
  - −1.32e7 (P1) and −0.17e7 s² (P2) per bulk row;
  - −2.61e7 and −1.19e7 s² per tail row.
- Applied at half strength to E046's fold SSE at the recorded counts, they give for example:
  - R1: bulk −0.8 to −6.2 s, tail −4.4 to −9.8 s;
  - S1: tail −4.5 to −10.0 s;
  - W1 without its dominant row: tail −2.6 to −5.8 s. That matches v2's "0 to −6 s" after the reversion.

**The S1 statement is reasonable, and it correctly calls the bulk sign uncertain.**
- The bias argument treats July's lower convention share as unexplained by x.
- Part of it will be explained, because `d_sched` is a feature: fewer late departures mean fewer convention rows. To that extent p falls on its own, and the bulk cost is below the estimate of +700 s per row.
- Either way, S1's WIN rests on the tail, as v2 says.

**One slip (D8-C12).** After W1's only known row (a tail row) is reverted, W1 rests on 14 bulk and 43 tail rows, not "13 bulk".

### (B) Criterion 4 (revision 2) and ruling (G)

**v2's choice is admissible.**
- Revision 2 offered two options, and v2 took the second.
  - The claim becomes "the convention component contributes a gain on the convention rows".
  - v2 states that the claim is *not* that the convention rows carry most of the gain.
- The reason is P1's convention share of 0.22. It comes from design months, which are legitimate design data.

**What the restated claim can and cannot show.**
- It is weaker than v1's claim.
- Reading (a) can still fail. Where E045 already predicts a convention row well, the mixture's error there, about (1 − p)(g − `d_sched`), can exceed E045's.
- But the pilot's convention-row RMSE fell by 29 % (P1) and 40 % (P2) under the mixture. A pass is therefore likely, and it shows only that the convention component helps where the convention holds. It does not show that the convention carries the gain.
- v2 commits to reporting `convention_share_of_gain` and, as unattributed, the non-convention change split by `d_sched`. A promotion record must carry both beside the result.

**The defect: the frozen tooling registers a different reading (a).**
- **`scripts/mixture_analysis.py` (`a977bef`):**
  - `CONV_SHARE = 0.5`;
  - `criterion4_reading_a` is true only if the convention-row SSE change is at most 0.5 × the subgroup SSE change;
  - its docstring calls this "H038 v2 criterion 4 reading (a)".
- **`tests/test_known_rows.py::test_mixture_analysis_convention_share_reading`** describes the same rule as "Criterion 4 (a) of H038 v2 … must carry at least half of the gain".
- **The v1 acknowledgement** lists revision 2 as "a decisive convention-row reading". That is the first option, which v2 did not take.
- **The two rules disagree whenever the convention rows gain but carry less than half of the gain.**
  - On the pilot they disagree in P1 (share 0.22: the sign test passes, the share test fails) and agree in P2 (0.93).
  - A conflict on at least one development fold is therefore likely (my estimate: about 0.4).
- **The run is unaffected; only the reading is.** Under the freeze, the tool cannot change for this version.

**Ruling (G), binding on the analysis and the phase close.**
- **Decisive (the proposal's text).**
  - Take every development fold (R1, R2, R3, S1, W1) whose `subgroup_sse_change` in `E051_vs_E046_mixture_analysis.json` is negative.
  - On each of them, `subgroup_sse_change_convention` must also be negative.
  - If it is not, on any one of them, the candidate is INCONCLUSIVE.
- **Not decisive.** The boolean `criterion4_reading_a` in that file is reported as **the majority-share reading**, beside `convention_share_of_gain`. It decides nothing.
- **No other criterion 4 statistic is decisive.**
- **Why the proposal governs.**
  - It is the hashed pre-registration, and it is unambiguous on this point.
  - The frozen tool's fields compute its reading exactly.
  - Choosing between the two rules after the run would be a forking path.

### (C) Ruling (E)(vi): the known-row reading and criterion 2's no-LOSS condition

**The gap.**
- Ruling (E) removed confirmatory weight from WINs that rest on known rows.
- It said nothing about a fold that avoids a LOSS only because of known rows.
- `known_row_check.py` implements (E) as written, so its `g5_consequence` flag does not cover this case.

**Why it matters here (W1).**
- The paired cluster bootstrap resamples about 300 airport-days per fold. Any one cluster is absent from about 37 % of the resamples, and present twice or more in about 26 %.
- Suppose the mixture gains tens of seconds on row 183903219 (p > 0.42) and loses on W1's other 57 rows:
  - q0.10 falls among resamples that contain the row's cluster, so it is strongly negative and the fold cannot be a LOSS;
  - q0.90 falls among resamples without it, so it is positive and the fold is not a WIN;
  - the frozen outcome is a TIE.
- Reverting the row can turn the same fold into a LOSS. While a dominant row gains, the frozen computation cannot declare that LOSS.
- R3's known row 200300302 can do the same, with smaller stakes.

**Clarification, binding (pre-registered before any run).**
- **The rule.** Suppose criteria 1–3 pass as frozen, and some development fold's counted outcome is LOSS in the reverted computation (`reverted.fold_outcome_counted` in `E051_vs_E046_known_rows.json`). Then criterion 2's no-LOSS condition rests on known rows.
- **The consequence is G5's:** an objection of objection F's type; INCONCLUSIVE; never uploaded.
- **Where it is read.** The phase close reads it from the same file, because the tool's `g5_consequence` flag does not compute it.
- **Unchanged:**
  - a frozen LOSS stays a LOSS;
  - criteria 1 and 3 are read as frozen;
  - the population is fixed.
- **Reported, not decisive:** the five-fold mean of `reverted.fold_delta_rmse`, beside the frozen mean.
- **Expected to bite rarely** (about 0.03). It is closed now so that it cannot be argued after the run.

### (D) Footprint (revision 3)

- **"Did the design use any known row? No."** The record agrees:
  - the params were committed at `9f653a9`, before the pilot;
  - `mixture.py` has changed since then only by two diagnostic columns (`e310996`);
  - nothing under `src/` has changed since `3c23aab`.
- **v2's expectations read E046's recorded figures for row 183903219 and the status of row 200300302.** These are expectations, not design inputs. Under (E)(v) they extend nothing.

## Novelty Relative to Existing Research

- **Unchanged from v1: not redundant.** No experiment fits a convention classifier or uses `d_sched` as a prediction component (rule 10: a new configuration).
- **New readings.**
  - The convention-row split (`subgroup_sse_change_convention`) runs for the first time.
  - v2 adds the split of the non-convention rows by `d_sched`.

## Experimental Isolation

- **Off the subgroup, the change is exact.** The mixture check requires max |Δ| = 0 against E046.
- **On the subgroup, three things change together:** the structure, g's training population (LIRF c = 0 rows), and the a-priori parameters.
  - The stored-component ablations separate the classifier from the structure.
  - On convention rows, a gain is attributable to the `d_sched` component, because the mixture's error there is about (1 − p)(g − `d_sched`).
  - On non-convention rows, nothing separates the structure from g's population. v2 now says so under Alternative Explanations and reports that gain as unattributed. That is the correct handling.
- **E052 is a determinism check.** LightGBM is deterministic here, with no subsampling, so the seed is unused. E047's byte-identity with E045 is the precedent.

## Validation Quality

- **The frozen folds are used unchanged:**
  - R1–W1 with the twins, and S1 required;
  - no H fold (H8);
  - the reference is E046;
  - criterion 8 is read against E033 and E028 (ruling B).
- **G5:**
  - (a) E051 and E052 are the first and second Day 8–12 looks, against a baseline of 44;
  - (b) the draw spread is unchanged and correct, and the subgroup spread is 0;
  - (c) is ruled in (E) and extended by (E)(vi).
- **`known_row_check.py` implements (E) correctly.**
  - `KNOWN_ROWS` equals (E)'s table: 14 rows, with the twins taking their fold's rows.
  - Predictions are read through the manifest-verified `_predictions`.
  - It raises an error if a known row is missing from a fold.
  - It runs the frozen `promotion_check` on reverted frames, so the twin rule applies to the reverted twins.
  - A fold has weight only if it is a WIN in both computations, and `g5_consequence` follows (E)'s two conditions.
- **The integrity check and the manifest are sound.** `mixture_check.py` writes its JSON even on a FAIL, and the launcher stages that JSON in the run's own checkpoint.
- **The expectations and probabilities are coherent,** with one slip (D8-C12).

## Leakage Review

### Target Leakage

PASS

- c is computed from y on training rows only. Validation labels are never computed, and a test checks this.
- p and g are fitted on `role == "train"` rows only.
- FS2 holds departure rows only, so g's LIRF filter cannot admit arrival rows.
- The labels computed on validation rows after the run (`mixture_analysis.py`) are evaluation, not inputs.

### Temporal Leakage

CONCERN

Not blocking. Unchanged from v1:
- `d_sched` is label T: admissible for ranking rows (DATASET_AUDIT §6.2), and outside the causal-only variant.
- Design-level fold leakage is handled by (E) and (E)(vi).

### Competition Availability

CONCERN

Not blocking. Unchanged from v1:
- every input exists for ranking DEP rows (107 subgroup rows in 2026-01 and 276 in 2026-07);
- the 2026 convention rate cannot be observed (U6);
- January 2026 carries the largest per-row stakes;
- (F)'s exposure requirement binds any SUBMIT proposal.

## Compute Review

### RAM

PASS

- The FS2 build dominates, as in E045 (5.38 GB peak, with a fit on all rows). The component fits here are smaller.
- The laptop has 10 GiB of RAM plus 4 GiB of swap. The CLASS-M target is 8 GB.

### Runtime

PASS

**v2's basis is weak, but its conclusion holds for other reasons.**
- The pilot's 72–75 s per split covered four months of data. The folds cover 2–11 months, so the pilot timings do not scale to them directly.
- The record supports 5–9 min per run on other grounds:
  - E030's laptop folds took 28–33 s each, including the FS2_RAW build and a fit. That bounds the build at about 25–30 s per fold.
  - g fits on LIRF c = 0 rows, about 7–8 % of a fold's rows, instead of E045's fit on all rows (E045: 92–190 s per fold).
  - No learning curves are recorded.
- So 840 s is about 1.5 to 3 times the expected time per run.

**The laptop is the risk.** The same computation has taken twice as long on one fold (E045 R1 92 s; E047 R1 195 s).

**Window arithmetic** (30 min = 1,800 s).
- E051 starts at START.
- E052 starts only if E051, its check and its checkpoint end by about START + 960 s. Otherwise it is DEFERRED.
- E052 can end after the window only if E051 took about 880–920 s and E052 took as long.
- I put P(E052 deferred) at about 0.1, and P(an overrun) at about 0.03.

**The consequences are bounded by the unchanged logic.**
- Nothing is killed, and the runner's CLASS-M timeout (2,700 s) still applies.
- An overrun is recorded under INC-0021 with its end time, as INC-0014 did for Day 7.
- A deferred E052 stays ALLOCATED and needs another owner window. Until it runs, criterion 6 is open and nothing can be promoted.
- The comparisons are analysis of stored files, run after the queue (INC-0014's reading).

### Disk

PASS

- About 30 MB: seven prediction files and seven component files per run, plus JSON.

## Weakest Assumption

- **That the pilot's gain carries over to folds decided by a few day-scale rows.**
  - On those rows, p comes from one or two classifier leaves.
  - The reference, E045, trained on two to three times as many months as the pilot's direct model.
- **S1 adds a second assumption:** p's upward bias at July's lower convention share must not, on S1's 218 bulk rows, overturn the tail gain.

## Missing Control or Ablation

- **Required:** nothing beyond what v2 registers:
  - the ablations (constant p, the convention component alone, g alone);
  - reading (a) as ruled in (G);
  - the known-row reading, with (E)(vi).
- **Named, not required (as in v1):** a direct LightGBM on LIRF training rows with E045's parameters. It would separate g's population from the structure on non-convention rows.
- **Reported, not required:** the reverted five-fold mean ((C)).

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Allocation.**
  - `gate.py allocate H038 v2` (primary), then the same with `--purpose reproduction`.
  - The pinned launcher hard-codes **E051** and **E052**, so the allocation must yield those IDs. Any other ID needs a new launcher, and with it a new version.
- **Configs:** exactly § Proposed Change.
  - `model: convention_mixture`, `feature_set: FS2`.
  - Params identical to the `mixture` section of `H038_params.yaml` (`b22c02c1…`): `base: E046`, `subgroup: LIRF_NM_missing`, tolerance 120 s, the classifier and normal parameters.
  - Folds R1, R2, R3, S1, W1, S1c, W1c; `job_class: CLASS-M`.
  - Seed 42 for E051. Seed 43 with `purpose: reproduction` for E052.
  - `proposal_version: 2` (D8-C12).
- **Execution.**
  - Only through `research/day-08/sessions/D08-S03/run_window.sh` (`54ee5ab8…`).
  - Armed only on the owner's go-ahead (INC-0021), with END = START + 30 min.
  - Queue E051 then E052, guards 840 s, one run at a time.
  - The launcher runs `mixture_check.py EID E046` after each run. A FAIL makes the run INVALID.
- **Analysis**, after the queue and from a clean tree:
  - § Validation Plan as listed, on development and diagnostic folds only;
  - the readings under rulings (G) and (E)(vi);
  - the rule 15 (G5) tables;
  - the INC-0017 and INC-0020 disclosure lines.
- **Freeze from `ce89aeb`:** no change under `src/`, `scripts/` or `config/`, and none to `pyproject.toml`, `uv.lock` or the launcher, until the batch's last comparison.
- **Not authorized:**
  - any H fold, holdout script or December target read;
  - any refit, rerun with changed parameters, added fold or other experiment;
  - any SUBMIT fit, formatter or upload;
  - any run outside the owner's window;
  - any change to a model component after results are seen.

Required acknowledgement path:
- **`research/day-08/acks/H038_ack_v2.md`.** It must:
  - reference the proposal hash (`3104c018…`) and this review's hash;
  - adopt rulings (G) and (E)(vi) as binding;
  - append D8-C11 and D8-C12;
  - state the authorized scope.

## Revision

None required. The corrections below are recorded in the acknowledgement; no proposal is edited.

- **D8-C11. Criterion 4 reading (a) in the tooling.**
  - `scripts/mixture_analysis.py` (`a977bef`) and `tests/test_known_rows.py` label a majority-share test (`CONV_SHARE = 0.5`, `criterion4_reading_a`) as "H038 v2 criterion 4 reading (a)". H038 v2 registers the sign test.
  - The v1 acknowledgement's "a decisive convention-row reading" describes the option v2 did not take.
  - Ruling (G) governs.
- **D8-C12. H038 v2, minor.**
  - (i) After the known-row reversion, W1 rests on 14 bulk and 43 tail rows, not 13 and 43.
  - (ii) The components are written to `predictions/validation/<EID>/components/`, not `predictions/val/`.
  - (iii) `proposal_version: 1` in § Proposed Change is carried over from v1. The configs carry 2.
  - (iv) The launcher's header still says "batch H038 v1". It is pinned and runs v2's queue; no change.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Mixture check PASS on all 7 folds | 0.95 |
| E052 starts inside the window | 0.90 |
| E052 byte-identical to E051 (if run) | 0.95 |
| Development-mean ΔRMSE against E046 < 0 | 0.60 |
| S1 WIN (frozen) | 0.45 |
| Criteria 1–3 hold (frozen) | 0.30 |
| … and they keep confirmatory weight under (E) and (E)(vi) | 0.17 |
| Reading (a) as ruled in (G) holds on every gaining development fold | 0.70 |
| The majority-share reading holds on every gaining development fold (reported) | 0.35 |
| Criterion 8 holds against E033 and E028 | 0.85 |
| The classifier beats constant p on at least 3 of 5 folds | 0.30 |
| PROMOTE at the Day 8 phase close | 0.11 |

Expected magnitude:
- **Development mean against E046:** central −3 s; 80 % interval −15 to +8 s.
- **R1 and R2:** −2 to −12 s.
- **S1:** −20 to +12 s.
- **W1:** set by p on row 183903219, from +26 s (p = 0.3) to −54 s (p = 0.8). After the reversion, 0 to −6 s.
- **R3:** small, of either sign.
- No leaderboard figure, and no expectation of one, is given (G3).

Primary expected failure mode:
- **Primary: a few recorded rows decide the folds.** W1 or R3 is a LOSS, or a TIE that turns into a LOSS once its known row is reverted ((E)(vi)). Or the WINs do not survive the known-row reading. Either way the candidate is INCONCLUSIVE.
- **Secondary: S1.** At July's lower convention share, S1's bulk rows turn it into a TIE.
- **Tertiary: reading (a) fails on a fold.** The convention rows lose while the subgroup gains, so the gain is not the convention's.
