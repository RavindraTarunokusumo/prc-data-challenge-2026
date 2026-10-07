---
schema: advisor-review-v1
hypothesis_id: H038
proposal_version: 2
proposal_sha256: a3cc9bc7139dedd24ba00c3bf9719fb99b6efcec16c65f72f9caae960ef02a66
exchange_id: X-D08-S03-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-10-06T22:48:23Z
---

# Advisor Review

## Summary Assessment

**Subject:** H038 v2, scope amendment A1 (`research/day-08/proposals/H038_v2_scope_A1.md`). Under it, H is added to the folds of E051 and E052 and predicted only.

**Decision: ACCEPT (0.85).**
- The amendment is not a material change to H038 v2.
- It adds the H fold, which the frozen runner requires of every non-final run, as predicted only.
- It changes no scored prediction, no reading, no decision rule and no model component.
- E051 and E052 keep their IDs. They may run in the owner's existing window, within the scope below.

**The error was mine as well as the researcher's.**
- X-D08-S03-0002 checked the configs against § Proposed Change, but not against `scripts/run_experiment.py::check_config`.
- That review listed "no H fold (H8)" as a validation point and "any H fold" as not authorized.
- In doing so it confused **predicting** H with **accessing** H.
  - Predicting H is the frozen default: the runner refuses any non-final run without it, and E030, E045, E046 and E047 all predicted H.
  - Accessing H is what H8 closes.
- The ACCEPT therefore authorized configs that the runner could never execute. INC-0022 should record the review's share of the error (§ Execution Authorization).

**Verified here (read-only).**
- **Hashes and tree.**
  - A1 is `a3cc9bc7…`, as in the envelope.
  - The launcher is `54ee5ab8…`, unchanged.
  - The tree is clean at `3242c09`.
- **Nothing ran.**
  - `check_config` (lines 60–76) runs before `ledger.update(status="RUNNING")` (line 137).
  - E051 and E052 are ALLOCATED in `runtime/ledger.sqlite` and in `experiments/ledger.jsonl`, with no run commit and no output files.
  - The task ledger has no event after the two allocations. Its last `holdout_access` is still 2026-10-04T17:57:38Z.
- **Reusing the IDs is consistent with the runner.**
  - Its own gate (status must be ALLOCATED) is what permits a second invocation.
  - Its rule "a new attempt needs a new E###" covers runs that reached a terminal status. A refused config never did.
- **H in the code.**
  - **Worker.** With H listed, `final` stays false. So `load_silver` nulls December DEP `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt`, with nothing unmasked. `evaluate` and the learning curve are skipped for `kind == holdout`.
  - **Truth access.** The frozen `evaluate.truth_frame` raises `PermissionError` for holdout and final folds.
  - **Every § Validation Plan tool is fixed to R1–W1c** and reads truth only through `truth_frame`:
    - `compare.py` (via `evaluate.compare`);
    - `known_row_check.py`;
    - `mixture_analysis.py` (`FOLDS` constant);
    - `range_check.py`;
    - `reproduce_check.py` (development folds of `metrics.json`, plus `compare`).
  - A1's "No H read follows" list leaves out three of these tools (compare, range, reproduce), but the claim holds for them too.
  - **The H fold's fits.** `convention_mixture` computes c and fits p and g on `role == "train"` rows only, which for H are January–November. The components file has no target column (`COMPONENT_COLUMNS`).
  - **The subgroup on H is the real one.** Only block time and target are blanked in December. `flt_missing` (`AOBT_3_flt` null) is computed the same way in the FS features and in `mixture_check.py`.
  - **W&B mirror.** `tracking.py` sends development and diagnostic metrics only. No predictions or targets leave the machine.
- **E046 covers H.** Its H file has 165,677 rows, the frozen `eval_rows` for H, and SHA-256 `ea350c61…`, which matches its manifest.
- **The launcher.**
  - It accepts a past START and proceeds at once, as it did at 22:40:58Z.
  - It aborts on an unclean tree.
  - It starts a run only if now + 840 s ≤ END.
  - With the same arguments, the window is not extended.

**What I did not do.**
- I read no target, December or validation-month column, and loaded no silver.
- No run, fit, allocation, holdout script or formatter.
- I did not open the Day 7 files that hold the disclosed figure.
- No challenge page, leaderboard or bucket.

## Scientific Validity

**(A) Not a material change, so an amendment is admissible.**
- **The scored folds are unaffected.**
  - The worker computes each fold independently from the same masked silver. December is masked whether or not H is listed, and `final` stays false.
  - Seeds and LightGBM determinism are unchanged.
  - So adding H is expected to change no byte of the seven scored folds' predictions.
- **The readings are unaffected.** Every reading of v2 is computed on R1–W1c only: criteria 1–8, rulings (G), (E) and (E)(vi), and G5. The look count is unchanged.
- **The only new consequences:**
  - one more prediction file and one more components file per run;
  - one more mixture-check fold, where a FAIL makes the run INVALID (v2's integrity clause, which the launcher already applies);
  - about 1–2 minutes more per run.
- **Why not a v3.** A v3 would issue new IDs and need a new launcher hash, with no scientific content, and it would leave E051 and E052 ALLOCATED and orphaned.
- **The form is new.** `purpose: scope_amendment` is not among the purposes in COMMUNICATION_CONTRACT §2. It is recorded in INC-0022. It is no precedent for any change that touches a scored fold, a reading, a population or a model component: those need a new version.

**(B) H8 is unchanged.**
- H8 closes H **access**: `holdout_check.py`, `evaluate.holdout_compare`, and any December target read.
- Predicting H with December targets masked reads no December target and writes no `holdout_access` event.
- **One real change in the risk surface, stated plainly.**
  - Without an H file, `holdout_compare` could not have been run on E051 at all.
  - With one, only the records stop it, exactly as for E046 (PHASE_OPEN_D08 review: "Enforcement is by records only").
  - The control is unchanged: the phase-close review verifies that the task ledger has no `holdout_access` line after 2026-10-04T17:57:38Z. It is restated as binding below.

**(C) The H predictions are recorded only.**
- No analysis of this batch reads E051's or E052's H files, except the target-free integrity record of `mixture_check.py`.
- Any later use needs its own review, including the target-free SUBMIT-stage check that A1 mentions.
- Any use against December truth is barred by H8 through Day 12.

## Novelty Relative to Existing Research

Unchanged from X-D08-S03-0002. The amendment adds no experiment and no configuration of scientific interest.

## Experimental Isolation

- Unchanged. The amended configs may differ from ack v2's only by `- H` appended to `folds`.
- The seven scored folds are expected to be byte-identical to what v2's configs would have produced.
- E052 remains a determinism check, read on the development folds by `reproduce_check.py`.

## Validation Quality

- **The frozen folds are unchanged:**
  - R1–W1c are scored, with S1 required;
  - H is predicted only;
  - the reference is E046;
  - criterion 8 is read against E033 and E028.
- **Integrity on H.** `mixture_check.py` iterates over the manifest's folds, so it checks H like any other fold:
  - outside the subgroup, equality to E046 (whose H file covers all 165,677 rows);
  - the components against the predictions;
  - the formula.
- A FAIL on any of the eight folds makes the run INVALID.
- **Two lines of ack v2's scope change (and nothing else):**
  - the configs' folds become "R1, R2, R3, S1, W1, S1c, W1c, H (predicted only)";
  - "Not authorized: any H fold" becomes "any H score, December target read or holdout script".

## Leakage Review

### Target Leakage

PASS

- December DEP block time and target are nulled by `load_silver` before the worker sees them.
- The H fold's c, p and g are fitted on January–November training rows only.
- The H components carry no target.
- No § Validation Plan tool can read H truth, because `truth_frame` refuses it.

### Temporal Leakage

CONCERN

Carried from v2 unchanged, and not blocking:
- `d_sched` is label T, admissible for ranking rows;
- design-level fold leakage is handled by (E) and (E)(vi).

The H fold adds nothing: its training months all precede its validation month.

### Competition Availability

CONCERN

Carried from v2 unchanged, and not blocking: the 2026 convention rate cannot be observed (U6).

## Compute Review

### RAM

PASS

- H's masked view is the largest: 12 months, against R3's 11.
- Runs that included H peaked at 5.38 GB (E045) and 6.4 GB (E030).
- The CLASS-M target is 8 GB.

### Runtime

PASS

- **Per fold.**
  - E030's H fold took 36.6 s, against 28–33 s for the other folds (build plus fit).
  - E051's H fold is the build plus two subgroup-sized fits: about 1–2 minutes on the laptop.
- **Per run.** About 6–11 minutes for eight folds.
  - 840 s remains a start guard, not a kill.
  - The runner's timeout is 2,700 s.
- **Window.** At 22:48Z, 1 h 52 min remain.
  - A1's own condition, "if both runs still fit by its guards", means a re-arm only while END − now ≥ 2 × 840 s, that is, **by 00:12:51Z**. Otherwise nothing is re-armed.
  - The check and checkpoint add 1–2 minutes. So a re-arm near that bound can still see E052 deferred by the launcher, under v2's deferral rule, with criterion 6 left open.

### Disk

PASS

One more prediction file (about 3 MB) and one more components file per run.

## Weakest Assumption

**That the H fold's mixture check passes.** It is the one new way the amendment can fail the batch: an H-only FAIL makes E051 INVALID, defers E052 and burns both IDs.

Grounds for confidence:
- E046's H file covers the frozen H population and matches its manifest;
- the subgroup flag is computed the same way in the worker and in the check;
- `override_fitted` refuses any row-set mismatch before anything is written.

P(H passes | the seven other folds pass) ≈ 0.98.

## Missing Control or Ablation

None. v2's requirements stand unchanged: the ablations, ruling (G), and the known-row reading with (E)(vi).

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Configs.**
  - In `experiments/E051/config.yaml` and `experiments/E052/config.yaml`, append `- H` as the last entry of `folds`. Nothing else changes: one added line per file, shown in the acknowledgement.
  - `gate.json`, both ledgers, the launcher and every frozen file stay unchanged.
  - `gate.json` continues to cite v2. The amendment's records are A1, this review and ack A1.
- **IDs:** E051 and E052, kept.
- **Commit first.** The amended configs, this review, the exchange mirror and ack A1 are committed and pushed before the re-arm.
- **Execution.**
  - Only through `research/day-08/sessions/D08-S03/run_window.sh` (`54ee5ab8…`).
  - With the unchanged arguments START 2026-10-06T22:40:51Z and END 2026-10-07T00:40:51Z (INC-0021).
  - Re-armed only by 00:12:51Z (A1's condition). After that, nothing is re-armed, and both runs wait for a new owner window.
  - The launcher's guards decide each start. A deferred E052 leaves criterion 6 open, as in ack v2.
  - The go-ahead of 22:40:51Z opened this window for this queue. A1 changes the configs by one predicted-only fold, not the queue. So this review does not require a new go-ahead; whether to ask again is the owner's choice (brief §1).
- **H is predicted only.** Its `mixture_check.py` result counts under v2's integrity clause.
- **Analysis.** H038 v2's § Validation Plan and rulings, unchanged. None of them reads H.
- **Everything else in ack v2's authorized scope stands,** including the 2-hour window amendment and the freeze from `ce89aeb`.
- **Not authorized:**
  - any H score;
  - any read of December targets, by any path (including direct reads of silver);
  - `holdout_check.py` or `evaluate.holdout_compare` on any experiment (H8);
  - any analysis or report of E051's or E052's H predictions beyond `mixture_check.py`'s record;
  - any other config change, fold, refit, rerun or experiment;
  - a re-arm with other arguments, or after 00:12:51Z;
  - any run outside the window.
- **Records.**
  - INC-0022 records three things:
    - (i) the review's share of the error (§ Summary Assessment);
    - (ii) that this amendment route (`purpose: scope_amendment`) was used instead of a v3, and why;
    - (iii) the re-arm time.
  - The phase close lists E051 and E052 as v2 + A1, and repeats the H8 task-ledger check.
  - INC-0022 is a failure and a researcher error, so it is reported to the owner plainly.

Required acknowledgement path:
- **`research/day-08/acks/H038_ack_v2_A1.md`.** It must:
  - reference A1's hash (`a3cc9bc7…`) and this review's hash;
  - show the two config diffs;
  - restate the two changed scope lines of ack v2;
  - append D8-C13;
  - state the authorized scope above.

## Revision

None required. One correction is recorded in the acknowledgement; no proposal is edited.

**D8-C13. The H fold.**
- (i) H038 v1 and v2 say "No H fold (ruling H8)" and "E046 has no H dependency here". X-D08-S03-0002 repeated "no H fold (H8)" and "Not authorized: any H fold". H8 closes H access, while the runner requires H prediction (`check_config`, SPLITS v2 review). Under A1, E051's H fold depends on E046's H file.
- (ii) A1's "No H read follows" leaves out `compare.py`, `range_check.py` and `reproduce_check.py`. All three are fixed to R1–W1c and read truth only through `truth_frame`, so the claim holds.

## Advisor Prediction

Probability of improvement:
- **Unchanged from X-D08-S03-0002.** The amendment changes no scored prediction.
  - Development-mean ΔRMSE against E046 < 0: 0.60.
  - PROMOTE at the Day 8 phase close: 0.11.
- **Operational:**

| Event | P |
|---|---|
| Mixture check PASS on all 8 folds | 0.94 |
| E052 starts inside the window (re-arm before about 23:30Z) | 0.92 |
| E052 byte-identical to E051 on the seven scored folds (if run) | 0.95 |
| An H fold score, H truth read or `holdout_access` event arising from this batch | 0.00 by construction; audited at the phase close |

Expected magnitude:
- **Unchanged:** development mean against E046, central −3 s, with an 80 % interval of −15 to +8 s.
- **H:** none (not scored).

Primary expected failure mode:
- **Scientific (unchanged):** a few recorded rows decide the folds (W1, R3), or the WINs do not survive the known-row reading.
- **Operational (new):** an H-only integrity failure, or a late re-arm that leaves E052 deferred.
