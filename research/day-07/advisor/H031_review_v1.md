---
schema: advisor-review-v1
hypothesis_id: H031
proposal_version: 1
proposal_sha256: 560ee530f3c2e1adeb18beb1e4ab6b9602d22e9bab8188a4fb29c2cc01815cf6
exchange_id: X-D07-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-10-03T17:17:40Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.85), with binding conditions S1–S9.** This file also holds the shared batch findings for H031–H033. `H032_review_v1.md` and `H033_review_v1.md` adopt S1–S9 by reference.

**The batch is the right procedure, built as stated.**
- It applies E033's construction to the frozen final folds. This is the refit-on-all-training-data step of brief §3's Day 7 theme, and the procedure STATE already names. The final folds and their training months were frozen on Day 1; nothing is chosen now.
- **Parsed-YAML comparison:** H031's `params` block equals `experiments/E029/config.yaml` exactly.
  - Only the header fields, `purpose`, `seed` (42 for 43) and `folds` differ.
  - The proposal's "identical except `purpose`, `seed` and `folds`" leaves out `hypothesis_id` and `proposal_version`, which are header fields (clerical, S9).
- **The seed change is inert:**
  - `prc.models.gbm.lightgbm` sets `deterministic=True` and `force_row_wise=True`; this is code, not config;
  - bagging and feature fraction are 1.0;
  - `bin_construct_sample_cnt` (5,000,000) is above the 2,085,047 twelve-month DEP training rows, so binning takes no sample;
  - E023 at seed 42 already equals E029 at seed 43, except for the routed rows' last bits (rule L v2).
- Nothing is a candidate, nothing is scored, and there is no holdout access. Rule 10 is not engaged.

**Facts verified read-only.** These checks are target-free: no target or block-time column was read, and no model was fitted.
- **Hashes:**
  - the three proposal hashes match the envelope;
  - the pinned files are unchanged at the freeze anchor `eedcd47` (committed 2026-10-03T17:00:11Z): launcher `1975bbba…f5872`, `make_submission.py` `c99fdaba…c290c1`, test `d11c773c…14bc49`;
  - the working tree is clean.
- **Tests and lint:**
  - `uv run pytest -q tests/test_make_submission.py`: 4 passed;
  - `ruff check .`: clean;
  - the 162-test full-suite claim was not re-run here; the envelope allowed only the formatter tests.
- **The experiment lock is free.** The inode of `runtime/experiment.lock` is absent from `/proc/locks`. Its `E041` text is the stale stamp disclosed in D6-C14 (c).
- **Template:**
  - its SHA-256 matches the raw manifest (`0d383408…`; one manifest entry);
  - 344,841 rows; `MVT_ID_mvt` Float64; `TAXITIME_SEC_mvt` Int32, all null;
  - its ID set equals silver's DEP rows of 2026-01 (152,719) plus 2026-07 (192,122) exactly.
- **Silver and the final views:**
  - silver holds 2025-01 to 2025-12, 2026-01 and 2026-07 only;
  - `masked_view` keeps the training months plus the one predicted month, so each final view holds a single ranking month (DATASET_AUDIT §6.2).
- **Row counts:**
  - routed rows (LIRF, `AOBT_3` missing): 107 in 2026-01 and 276 in 2026-07, as stated;
  - twelve-month training has 2,085,047 DEP rows, against H's 1,919,370 (+8.6 %), consistent with "about 9 %".

**Six findings.** Conditions S1–S9 settle them. None changes a configuration, threshold, population or fold.

1. **The launcher will leave the tree dirty after E042's checkpoint, so E043 and E044 will record `git_dirty_at_run: true`.**
   - **Cause:** inside each final-fold run, `prc.data.load_silver(unmask_holdout_for=…)` appends the unmasking event to `orchestration/task-ledger.jsonl`, a tracked file. `checkpoint()` stages only `experiments/<E###>`, `experiments/ledger.jsonl` and the route-check JSON.
   - **Effect:**
     - the launcher logs a WARNING and continues;
     - `run_experiment.py` records `git_dirty()` (`git status --porcelain`) at each start;
     - the launcher header's "so the next run records a clean tree" is false for E043 and E044.
   - **Why this is acceptable:**
     - it is harmless to the science: the file is an append-only, non-code log, and code identity is `run_commit`;
     - it is auditable, because the WARNING lines print the porcelain entries;
     - I do not require a launcher change: the launcher is pinned, and a v2 cycle risks the only window.

   S3 pre-registers the state and how it is checked.
2. **Integrity reading 4 contradicts itself.** It says "for E042 and E043 only", then adds that E044 "unmasks as well and logs it". Read literally, this blocking criterion fails by design. S4 restates it.
3. **H032's resolved-parameter clause exempts "differences caused by the training set". The exemption has no basis.**
   - E031's and E040's resolved parameters are identical on all 8 folds, from W1c (1 training month) to H (11). `data_partition` is FeatureParallel throughout; E036 has DocParallel.
   - D6-C7 found `data_partition` confounded with E031's advantage.
   - A difference at 12 months is therefore informative, not explained by the training set. S5 removes the exemption.
4. **"A flag never changes the predictions" needs its limit stated.** A flag whose written analysis finds a code or data defect is not a fact about the ranking months. Under §Batch's own failure handling, such a run is INVALID (S6).
5. **The requested rerun allowance has no bounds.** It does not separate deferral from failure, or say how the blend takes a re-run id. S7 grants it narrowly.
6. **Clerical.** All three proposals carry `created_utc: 2026-10-03T17:20:00Z`. That is 20 minutes after the commit that contains them (`eedcd47`, 17:00:11Z), and after the envelope (17:00:07Z). The hashes stand; S9 records the correction.

**What the batch cannot show.** Stated here so that no record claims more.
- No frozen fold trains on 12 months, so no development-fold analogue of the SUBMIT fit exists.
- H cannot test the SUBMIT fit (ruling H6 (f)).
- The Day 6 phase close named "a pre-registered check of the SUBMIT procedure". The target-free integrity and sanity readings are the only feasible form of that check. They test completeness and consistency, not accuracy.

## Scientific Validity

- **Procedure.** Selecting on development folds and then refitting the selected procedure on all training months is standard (ESL §7.10).
- **No new selection.** Iterations and weights are fixed, and nothing stops early or is fitted on predictions. The 12-month fit adds no selection step.
- **What differs from the evaluated components:**
  1. one more training month (December; +8.6 % rows);
  2. a fresh GPU draw of the CatBoost half (H032);
  3. the ranking months themselves.

  Items 1 and 3 are the purpose of the batch. Item 2 is disclosed under rule 13.
- **Known asymmetries the SUBMIT fit meets untested** (DATASET_AUDIT §6.5; disclosure under S9):
  - **The July gap.** July 2026 is predicted across a six-month gap; no 2025 fold reproduces this.
  - **The month edge.**
    - 1 July 2026 rows have no 30 June context, because June 2026 is not in silver. Every development fold has its previous month in view.
    - The windows affected are short: the `cg_*` look-backs reach at most 30 minutes plus taxi intervals, and `cg_rwy_gap_prev` is capped at 3,600 s. They fall in the night (UTC).
  - **The NM match rate.**
    - The DEP NM-missing share is 1.61 % in 2026-01 (2,453 rows) and 1.48 % in 2026-07 (2,837). By 2025 month it ranges from 0.62 % to 2.06 % (pooled 1.08 %).
    - January 2026 is about 1.7 times January 2025 (0.93 %), and above both winter analogues, H (1.00 %) and W1 (0.77 %).
    - NM-missing rows carry 14–66 % of the development SSE (STATE). January's exposure to the champion's weakest population is therefore higher than in any winter analogue. This complements D3-C3.
- **Format.**
  - Rounding to Int32 (half to even) is forced by the template's dtype. It moves a row by at most 0.5 s, about 0.29 s RMS, which is negligible against an RMSE of about 440 s.
  - Declining a floor or clip is correct: the submitted predictor stays the evaluated one.

## Novelty Relative to Existing Research

- **No SUBMIT fit exists.**
  - The final-fold path has never run on real data (HANDOFF_D04 §10: "not yet written or tested").
  - No test calls `load_silver(unmask_holdout_for=…)`.
- **Not redundant with E040 and E041.** Those are development-fold draws, and N4 of `H029_review_v1.md` already separated them from the SUBMIT draw.
- **Rule 10 is not engaged:** no candidate, no promotion, no ledger decision.

## Experimental Isolation

- Against E029, H031 changes only the folds. The seed change is inert (Summary).
- No ablation is needed, because no mechanism is claimed.
- The route check between the halves isolates the routing path. It cannot see a defect common to both halves (Weakest Assumption).

## Validation Quality

- **Frozen folds are used unchanged.** `SUBMIT_JAN` and `SUBMIT_JUL` run as frozen. No development fold, diagnostic fold or H is touched.
- **The pre-registration fits a run with no truth:**
  - integrity readings 1–4 are blocking (4 as restated in S4);
  - the sanity flags are non-blocking;
  - their thresholds are anchored to reference values measured on E033's 8 folds on 2026-10-03;
  - S6 states when a flag becomes a defect.
- **Integrity 1 makes "within class" blocking.** The margins are adequate: E042 is expected at ≤ 7.3 GB against 8 GB, and E044 at about 3.4 GB against 4 GB. I accept this conservative choice as written.
- **Rule 13 is correctly limited.** Final folds have no twin and no truth. Reading (c), the halves' disagreement, is a different quantity from a draw change and is labelled as such (S9).

## Leakage Review

### Target Leakage

PASS

- Inputs are as E029 (FS2), already reviewed. FS2 carries no fold-local target priors.
- The ridge and LightGBM fit on the final folds' training rows only (`role == 'train'`, all in 2025).
- **December's targets** enter only as training labels of a final fold, through the logged Day 1 unmasking path.
- **No artifact of the run shows a December figure:**
  - `metrics.json` is empty for final folds;
  - `learning_curve` returns training loss only for final folds;
  - the worker prints "saved".

### Temporal Leakage

PASS

- `masked_view` gives the ranking information set of DATASET_AUDIT §6.2:
  - it nulls the predicted month's DEP block time and target;
  - it keeps that month's ARR rows complete;
  - it excludes every other month.
- Verified on silver: the only 2026 months are 2026-01 and 2026-07, and each final view contains one of them.
- All training months precede both ranking months.

### Competition Availability

PASS

- The admissible information set is the same as in every development fold.
- The July month edge and the six-month gap are §6.5 asymmetries of the ranking data, not availability violations (disclosed under S9).

## Compute Review

### RAM

PASS

- E029 peaked at 6.60 GB over 8 folds; its largest fold, H, has 11 training months.
- With +8.6 % training rows, the expected peak is 6.7–7.3 GB: under CLASS-M's 8 GB, and the hard limit is 11 GB.
- Any swap-out is recorded beside RSS (INC-0010).

### Runtime

PASS

- E029's H fold took 146 s. Two 12-month folds plus loading come to about 5–7 minutes.
- The 700 s guard and the 2,700 s CLASS-M timeout are generous.
- **Window arithmetic:** the pessimistic queue is 1,860 s of the window's 3,600 s. The expected queue ends by about 19:25Z.

### Disk

PASS

About 10 MB of predictions and records, covered by manifests.

## Weakest Assumption

**That the final-fold path, never exercised, builds the intended 12-month training set for both halves.**
- No test calls the unmasking branch, and it runs on real data for the first time tonight.
- **After the run, the evidence is structural only:** the task-ledger event (S4), the frozen `masked_view`, and the code at `run_commit`. No record counts training rows per fold.
- **A defect shared by both halves would go unseen by the integrity checks.**
  - Both halves use the same `load_silver`, `masked_view`, FS1 and congestion builders, and ridge.
  - I1–I5 and the route check only compare outputs with each other, so they cannot see such a defect.
  - Only the sanity readings (b) and (c) and the per-airport means could reveal it, and only if it is gross.

## Missing Control or Ablation

None is required: this is a procedure run with no mechanism claim.

Named, not required:
- **An external reference for the routed rows on the final folds.** The route check compares two runs that share the ridge path. It is not an independent reference, the role E029 played on the development folds.
- **A target-free feature-path check.** Comparing per-column null rates and ranges of the SUBMIT validation frames with H's validation frame would cheaply check for a defect common to both halves.
- **The Day 6 phase close's "pre-registered check of the SUBMIT procedure"** exists here only in target-free form. No frozen fold trains on 12 months, so an accuracy analogue would need a change to frozen splits. The final report says so (S9).

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **H031 v1: exactly one `primary` allocation,** `uv run python scripts/gate.py allocate H031 v1`, made first in the batch (expected **E042**).
  - **Config:** the Proposed Change block (folds `SUBMIT_JAN` and `SUBMIT_JUL`, seed 42, CLASS-M).
  - **When:** first in the queue of `research/day-07/sessions/D07-S01/run_window.sh` (SHA-256 `1975bbba9a458d5b68016a7b2edaa256999f45b28cb18c410c8923cf042f5872`), in the 2026-10-03 19:00–20:00Z window (INC-0014), or later under S7.
- **The batch as a whole:**
  - one `primary` allocation each of H031 v1, H032 v1 and H033 v1, in that order;
  - the route check `route_check.py E043 - E042`;
  - one `make_submission.py` invocation under S8;
  - reruns only under S7. Nothing else.
- **The status of every run in the batch.** This covers E042–E044 and any rerun allowed under S7:
  - none is a candidate, none is ever NEW, and none is scored;
  - there is no holdout access, and the ledger decision is null;
  - no `holdout_check.py` and no `compare.py` runs with any of them.
- **S1–S9 bind every run of the batch.** `H032_review_v1.md` and `H033_review_v1.md` adopt them.

**S1. Allocation, ids and config identity.**
- **Order:** allocate H031 v1, then H032 v1, then H033 v1, with one `primary` allocation each. The expected ids are E042, E043 and E044.
- **Before arming, verify and record:**
  - each `gate.json` names its hypothesis, `v1` and purpose `primary`;
  - each `config.yaml` equals its proposal's block (parsed YAML);
  - E044's components are `[<H031 id>, <H032 id>]`, in that order.
- **The launcher hard-codes E042, E043 and E044.** If the allocated ids differ, do not arm it, because the pinned queue would run the wrong ids. The batch would then need a new launcher, and that means a new proposal version: the launcher's hash is pinned in H031 §Batch.

**S2. Pre-arming record.** It is written and committed before arming. From then until the window opens, nothing in the tree changes. It states:
- the S1 checks;
- the launcher hash and its diff against `run_window_2.sh`;
- the freeze diff from `eedcd47` over `src/`, `scripts/`, `config/`, `pyproject.toml`, `uv.lock` and the launcher (expected empty);
- the rule L v2 item 6 environment;
- the GPU name, driver, total memory and **memory in use at arming**;
- **the overrun bounds:**
  - the class timeouts: 2,700 s for E042 (CLASS-M), 8,100 s for E043 (CLASS-L), 450 s for E044 (CLASS-S);
  - the launcher never kills a run;
  - a run still executing after 20:00Z is an INC-0014 deviation.

**S3. The task-ledger append and the dirty tree.** This state is pre-registered. Within the bounds below it is not a deviation.
- **Expected:**
  - after E042's checkpoint, the launcher logs `WARNING: tree not clean … M orchestration/task-ledger.jsonl`;
  - E043 and E044 record `git_dirty_at_run: true`;
  - the same WARNING follows E043's and E044's checkpoints.
- **When it becomes a deviation.** The state is acceptable only if every such WARNING lists `orchestration/task-ledger.jsonl` as its only entry. Any other entry is an INC-0014 deviation and is reported.
- **During the window:**
  - nothing is edited, staged or committed by hand;
  - the launcher is not edited;
  - the three unmasking lines go into the first commit after the queue ends.
- **How the records describe it.**
  - For E043 and E044 they say "`git_dirty_at_run: true` (task-ledger append from the final-fold unmasking only; S3)".
  - No record claims "clean tree at each run" for this batch.

**S4. How integrity reading 4 is read.**
- The task ledger shows `holdout_targets_unmasked_for_final_training` exactly once for each of E042, E043 and E044, and for each S7 rerun that ran.
- Each event is timestamped between that run's start and end.
- No other experiment has the event.
- E044's event is recorded as "unmasked silver loaded; no target used (blend; the FS0 frame supplies row ids only)".

**S5. Resolved parameters (H032).**
- Before the submission is formatted, compare E043's `resolved_params.json` with E031's on both final folds, key by key. A key present in only one of them counts as a difference.
- E031 and E040 resolved identically on all 8 folds, from 1 to 11 training months. The exemption "other than those caused by the training set" therefore does not apply.
- Any difference is named key by key, and `data_partition` is checked explicitly. It is a sanity flag under S6.
- Expected: none.

**S6. Flags, defects and upload.**
- The sanity flags (a)–(c) and any S5 difference are non-blocking, and they never change a prediction.
- **When a flag finds a defect:** if its written analysis identifies a code or data defect, the affected run is INVALID under §Batch's failure handling.
  - Its predictions are not submitted.
  - The remedy is a new proposal version: no rerun and no post-hoc fix.
- **Upload:**
  - it happens after FROZEN, once, by the owner's decision (LEADERBOARD_POLICY);
  - it does not happen while any flag analysis is open;
  - the owner receives every flag analysis before deciding.

**S7. Deferral, failure and the rerun allowance (granted narrowly).**
- **Deferral.**
  - This covers a run DEFERRED by the launcher and a run refused before RUNNING.
  - The run keeps its E### (still ALLOCATED) and runs unchanged in the next owner-set window.
  - It runs either by a direct `run_experiment.py` call or by a new launcher recorded before that window (as C3 of `H024_review_v2.md`).
  - No new allocation is made.
- **RESOURCE_FAILURE or TIMEOUT.**
  - At most one `gate.py allocate H03x v1 --purpose rerun` per hypothesis, run in an owner-set window.
  - Its config equals the failed run's `config.yaml` (parsed YAML), except for the blend, below.
  - The runner already requires seed 42.
- **Blend substitution, the allowance §Batch requests.**
  - If a component was re-run, the blend is a new allocation, `gate.py allocate H033 v1 --purpose rerun`. Its config equals E044's, except that the re-run id replaces the failed id in the same position.
  - E044's committed config is never edited. E044 stays ALLOCATED and is recorded "superseded; never run".
  - At most one H033 rerun allocation is made in total.
- **Before any blend runs:**
  - the pair it uses passes `route_check.py <CatBoost half> - <LightGBM half>`;
  - `make_submission.py` is then called with the ids actually blended.
- **INVALID.** This covers a code defect, a failed route check or a failed I1–I5. There is no rerun; a fix needs a new proposal version.
- **A GPU memory or device failure** is RESOURCE_FAILURE, and its record states `gpu_mib_at_start`.

**S8. Formatting the submission.**
- **When:** `make_submission.py` (SHA-256 `c99fdaba8067ff5b98fd0ab93762561c3639b58d44b3e02752fa8aa2ebd290c1`) runs only after:
  - E044 is COMPLETE and the route check has passed;
  - the window has closed (INC-0014's reading);
  - no process holds the experiment lock.
- **Arguments:** `E044 E042 E043 --ref E033 E029 E031`, or the ids actually used under S7.
- **If it refuses:** no submission file exists, the refusal is recorded, and a fix needs a new proposal version.
- **The uploaded file.** After FROZEN, the file uploaded is `predictions/final/submitting.parquet`, unmodified, with the SHA-256 recorded in `SUBMISSION_RECORD.json`. Any re-run of the formatter must reproduce that hash.

**S9. Records and disclosures (non-blocking).** The batch analysis states:
- **What the submission is:**
  - E033's construction refit on 12 months, carrying one draw of the CatBoost half;
  - its accuracy is not measured by any fold or by H (ruling H6 (f));
  - no figure is quoted as the submission's expected error, other than E033's development and H figures labelled as such.
- **What reading (c) is:** the halves' disagreement, not a draw change. Rule 13's quantities cannot be computed here.
- **The §6.5 asymmetries, with today's counts:**
  - the July gap;
  - the 1 July month edge;
  - the NM-missing share: 1.61 % (Jan) and 1.48 % (Jul), against 0.62–2.06 % by 2025 month (January 2025 0.93 %, H 1.00 %, W1 0.77 %).
- **The outcomes of S3, S4 and S5.**
- **Clerical corrections, recorded in the ack:**
  - the proposals' `created_utc` (17:20:00Z) is later than `eedcd47` (17:00:11Z);
  - H031's "identical except" sentence leaves out the header fields;
  - `deterministic: true` comes from `prc.models.gbm`, not from the config.
- **Operations:** the launcher log is copied into the session record, and any run ending after 20:00Z is reported under INC-0014 with its end time.

Required acknowledgement path: `research/day-07/acks/H031_ack_v1.md`. It references the proposal hash `560ee530f3c2e1adeb18beb1e4ab6b9602d22e9bab8188a4fb29c2cc01815cf6` and this review's hash, and accepts S1–S9 as binding.

## Revision

None required for this version. S1–S9 are execution and record conditions under ACCEPT.

## Advisor Prediction

Probability of improvement: not applicable. There is no truth, and nothing is scored.

| Event | P |
|---|---|
| E042 COMPLETE, within CLASS-M | 0.95 |
| Batch integrity readings 1–4 all hold (S4 reading), all three runs in tonight's window | 0.88 |
| S3: the dirty-tree WARNING appears, with the task ledger as its only entry | 0.95 |
| `route_check.py E043 - E042` PASS on both folds, given both COMPLETE | 0.97 |
| A first-use defect of the final-fold path surfaces (run INVALID or flag analysis finds a defect) | 0.04 |

Expected magnitude:
- **E042 resources:** runtime 300–480 s (central 370 s); peak RSS 6.7–7.3 GB (central 7.0).
- **E042 mean prediction:** 2026-01 960–1,010 s; 2026-07 990–1,050 s.

Primary expected failure mode:
- **First:** E043 fails on GPU memory, if the external holder grows before or during the window (RESOURCE_FAILURE under S7). E044 is then deferred to another owner window.
- **Second:** an operational slip at arming: the tree is not clean at window open, or the allocated ids are not E042–E044 (S1).
