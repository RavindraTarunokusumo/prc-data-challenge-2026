---
schema: advisor-review-v1
hypothesis_id: H015
proposal_version: 2
proposal_sha256: 468b442de9f20b3d16e676d1e3584fd0fec0e3efa442b83f7133e9c975ecf499
exchange_id: X-D03-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-09-29T16:26:59Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT**, with the preconditions and the scope limit under Execution Authorization.

v2 resolves all six required revisions of `H015_review_v1.md`, and I found no new blocking defect.
- **The v1 "acceptable as is" items are unchanged.** A diff against v1 shows the Proposed Change table, clauses 1, 2(c) and 4, the criterion 6 handling, the chain order, the conditional reproduction and the rule 8 S1 pre-registration are unchanged. Only wording differs.
- **E017's parameters are reproduced exactly**, checked against `experiments/E017/config.yaml`.

| v1 required revision | Status in v2 | How it was verified |
|---|---|---|
| 1. Forward-risk figures | **Done** | Every monthly count and share matches `fs2_v2_checks.json` (silver, target-free). The rationale now rests on the Day 1 rate range (0.35 in July, 0.83 in March; `PHASE_CLOSE_D01_review_v1.md`) and on the fact that the 2026 rate cannot be estimated. It no longer rests on a count claim |
| 2. Clause 2 not decidable by one known record | **Done** | `NM_present_excl_LIRF` (`64c165b`, tested) excludes row 192622644. By construction it contains no SCHED-anchored T window. Target-free, the clause population's largest in-taxi count is 93–129 per fold; v1's row had 486. See (a) |
| 3. Noise scale on the chosen population | **Done** | All 21 table cells match the three committed JSONs to 0.01 s. The largest development-fold shift is 1.957 s (W1, E018 − E006). The W1c argument holds |
| 4. P labels | **Done** | See (e): the diff, the tests on old and new code, a brute-force recomputation on real data and a real-data perturbation |
| 5. Clause 3 consequences | **Done** | 3(a) and 3(b) are stated separately, and 3(b)'s bearing on criterion 6 is stated |
| 6. Record items | **Done** | The tools list is extended. Row 192622644 is named against E005. The residual exposure is disclosed. The routed-ridge check is declared uncommitted. The development mean equals 482.73 plus the dRMSE range (432.7–446.7 s) |

**Verified here.** All checks were read-only, target-free or synthetic.
- No December target was read.
- No model was fitted or scored on real data; the test suite fits synthetic data only. DEP block and taxi columns were nulled for every month before any real-data feature computation.
- I wrote only the three review files.

The checks:
- **Hashes.**
  - The three proposals match the envelope.
  - The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json` (`32c41c0f…`).
  - `.claude/agents/advisor.md` is `30fff5dd…`, matching `config/agents.yaml`.
  - `uv.lock` is `39df945c…`, the value in the gate records of E005, E009, E017 and E018.
  - Silver is `efde4262…`, matching its manifest.
  - The X-D03-S01-0001 mirror checksums verify (6/6).
- **Predictions.** The prediction files of E005, E006, E012, E015, E017 and E018 match their manifests (8/8 each).
- **Code.**
  - Unchanged since E017's run commit `6e135de`: `gbm.py`, `linear.py`, `worker.py`, `run_experiment.py`, `data.py`, `paths.py`, `ledger.py`, `pyproject.toml` and `uv.lock`.
  - `features.py` only appends `CONGESTION_NUMERIC` to `NUMERIC` and adds `fs2`, `fs2_p` and their registry entries. `models/__init__.py` only registers `routed`.
  - Unchanged since `5ba9230`: `compare.py`, `mechanism_check.py`, `attribution.py`, `reproduce_check.py` and `gate.py`.
- **Frames** (target-free, real W1c and S1 views).
  - The FS2 frame's FS0 and FS1 columns equal `fs0()` and `fs1()` exactly.
  - The LightGBM input order is E017's 17 inputs followed by the 15 congestion columns.
  - FS2_P is FS2 minus the five T columns, and no congestion value is null.
  - The routed validation rows (58 on W1c, 337 on S1) equal silver's LIRF NM-missing counts for February and July.
- **Tree, tests and lint.**
  - The tree is clean at `2671dd3`.
  - `pytest` passes 123/123 with caches disabled, and `ruff` is clean.
  - The task ledger has no Day 3 allocation. There is no FS2 or FS2_P artifact in `predictions/` or `research/comparisons/`.
- **Secrets.**
  - No credential value appears in the 410 tracked files.
  - The OpenSky username occurs once, inside the public repository owner's name in the brief. The Day 2 phase close recorded the same, and DATA_POLICY §1 does not list the username as a credential.

## Scientific Validity

### (a) Clause 2 on `NM_present_excl_LIRF` cannot be decided by a known record

The clause population, target-free, computed on each fold's masked view with every DEP block and taxi value nulled:

| Fold | Clause rows | Max `cg_dep_to_during` | Rows > 100 | Max `d_aobt3` (s) | NM-present training rows > 100 |
|---|---|---|---|---|---|
| R1 | 166,986 | 99 | 0 | 5,396 | 2 |
| R2 | 169,734 | 129 | 2 | 10,094 | 2 |
| R3 | 149,700 | 124 | 1 | 7,363 | 4 |
| S1 | 171,901 | 100 | 0 | 8,163 | 4 |
| W1 | 131,977 | 93 | 0 | 7,915 | 4 |
| S1c | 171,901 | 100 | 0 | 8,163 | 1 |
| W1c | 131,977 | 93 | 0 | 7,915 | 0 |

- **The distribution is ordinary.** q99 is 28–29 and q99.9 is 41–46 on every fold. The largest-count rows are long LTFM taxis, plus one EHAM and one EGLL row.
- **The existing fits agree on those rows.** On the clause rows with `d_aobt3` > 3,600 s, the four existing Tier 1 fits (E006, E012, E017, E018) differ by at most 1,262–3,380 s per fold. In v1 the fits differed by 6,471 against 22,473 s on one row.
- **What one row can do.**
  - RMSE on this population is about 211–269 s per fold, derived from the committed E017 − E018 SSE.
  - Half of a −6 s fold change is 1.9–2.6 × 10⁸ s² of squared error. A single-row change of 10⁸ s² moves a fold by only 1.1–1.6 s.
  - Across the 35 fold and twin cells of the five committed contrasts on this population, the top row's change is 0.3–4.5 × 10⁷ s² (largest: E017 − E018 on R3). The dominant rows reported in the noise contrasts are ordinary tail and late-departure rows (y 1,264–10,972 s).
  - H009 v3's review established that no row in this population has y ≥ 20,000 s.
- **Consequence.** Even a 10⁸ s² single-row change, twice the largest seen, moves the five-fold mean by about 0.3 s at most. Clause 2(b) could be decided by a single record only if the true mean sat within that distance of −6.0 s. The S1 WIN and the S1c twin are likewise not decided by any known record.

### (b) Reading rule 6 on the clause (attribution only; not a defect)

"No row is expected to carry ≥ 0.5 of any fold's change" holds for folds with a real effect: the Day 2 static-key contrasts had |top-1| ≤ 0.11. It does not hold for folds with a near-zero net change.
- In the three noise contrasts on this population, whose development-fold net changes are all within ±2 s, 7 of the 15 cells have |top-1| ≥ 0.5.
- **A dominant row on a fold with |dRMSE| below about 1.5 s is therefore expected.** It is not evidence against the clause.
- On a fold with |dRMSE| ≥ 4 s it would be unexpected. It must then be reported with its details (B4).
- This changes no fold outcome.

### (c) R: the restated rationale and the residual exposure

**The rationale is admissible under ruling B.**
- It is pre-registered and is not a threshold.
- It rests on the Day 1 tail rate (0.35–0.83), not on E006–E018 outcomes.
- The "decided criterion 8" bullet cites the Day 2 record as motivation. The rationale does not depend on it.
- Both 2026 counts (107 and 276) lie inside the 2025 range, and v2 says so.

**The residual exposure on LIRF NM-present rows is small.** From the committed rule 7 figures of E017 − E005:
- On every development fold, E017 beats E005 on those rows, both over the full subgroup (−79.8 to −115.7 s) and on its bulk (−50.8 to −65.2 s).
- The NM-missing pathology (a bulk loss larger than the NM-present gain) does not appear. W1c's bulk (+8.6 s) is the only positive cell.

**Criterion 3 at LIRF is not at risk.**
- For routed E017 (E017 outside the subgroup, E005 on it), derived exactly from `E017_vs_E005.json`, LIRF's pooled development RMSE is 1,450.9 s against E005's 1,485.8 s: a ratio of 0.977 against a tolerance of 1.03.
- To breach it, FS2 would have to add 1.6 × 10¹⁰ s² of LIRF SSE. Row 192622644 could contribute under a tenth of that (at most about 1.1 × 10⁹ s²).

### (d) C: expected size, and an unlisted reading

**The EDA supports review v1 (g).**
- The large after-anchor figures come from the three counts that scale with the interval length (9.7–11.8 s each).
- The two T features that do not scale with it add much less: `cg_rwy_gap_prev` 0.98 s and `cg_dep_to_rwy_m15` 0.90 s.
- The ten P features add 0.28–1.74 s.
- v2's reduced range (−4 to −15 s) is still optimistic in my estimate (Advisor Prediction).

**An alternative mechanism, for the record.** Given `d_aobt3`, the in-taxi counts can act as a plausibility check on the anchor: a long interval with few takeoffs suggests an early `AOBT_3` (a gate hold) rather than a runway queue.
- This is still traffic-state information, it is admissible, and it does not affect clause 2's validity.
- It bears on the Mechanism's reading ("waiting time … set by the departure queue"), not on the C claim as worded in the Research Question.

### (e) The P-label re-implementation (commit `63923e2`)

- **The diff.** It is exactly the stated fix. The five counts subtract `1{t_to > t_off}` or `1{t_to ∈ [t_off − w, t_off)}` instead of a constant 1, and the clip at 0 is gone. No other feature changes.
- **The tests.** On a scratch copy with the v1 `congestion.py`, `test_p_features_invariant_to_own_takeoff` fails at five of its nine positions and `test_p_counts_exclude_self_when_takeoff_precedes_proxy` fails: 6 failures in all. On v2 they pass.
- **Brute force on real data.** I recomputed all ten P features independently, excluding row i explicitly, on 3,262 real July 2025 DEP rows. The sample includes all 266 July rows that take off at or before their proxy. It matches the code exactly (0 mismatches).
- **Perturbation on real data.** Moving the own takeoff of 60 real EGLL rows to four positions around the proxy changes no P feature.
- **Masking invariance** holds on 1,919,370 rows (`fs2_v2_checks.json`), and structurally: `_dep_frame` never selects a DEP block or taxi column. The docstring is corrected.

### (f) Clause 3 and determinism

- **The code path is identical.**
  - `routed_lightgbm` calls `gbm.lightgbm` with the parameters minus `route_ridge_params`, through the same worker path.
  - `deterministic`, `force_row_wise` and 4 threads are pinned.
  - `bin_construct_sample_cnt` (5,000,000) exceeds every training set (at most 1.54 M rows).
- **3(a) is low-risk.** E005 and its exact reproduction E009 ran on the current `uv.lock`. The ridge's FS0 inputs are identical to E005's (see Summary, "Frames").
- **Hardware.**
  - The container restarted once in D03-S01 (retry record, 15:30Z).
  - Byte identity across processes is expected on one host. Across a restart onto another host it is likely but not guaranteed.
  - The pre-registered consequence of a 3(b) failure (INVALID) applies either way. The record must say whether a restart intervened (Execution Authorization, item 8).

## Novelty Relative to Existing Research

- **The congestion block and the routing structure are new.**
- **Standing rule 10 is not engaged.**
  - FS2 with routing is a new configuration.
  - The clause population changes before any run, in answer to a review finding. The new population is an existing one that H009 v3 used for the same row.
  - No FS2 outcome exists: I checked the ledger, `predictions/` and `research/comparisons/`.

## Experimental Isolation

| Claim | Contrast | Population | Only difference | Status |
|---|---|---|---|---|
| C | H015 − E017 | `NM_present_excl_LIRF` | + 15 congestion columns (routing plays no part) | **Isolated and decisive against known records** ((a)) |
| C, bulk | H015 − E017 | `NM_present`, y < 3,600 s | Same | Insulated sign test |
| R | H015 − H016 | `LIRF_NM_missing` | Routing only | Exact, given `route_check.py` 3(b) |
| P against T | H017, H016 | `NM_present_excl_LIRF` | The five T columns | See `H017_review_v2.md` |

**Residual exposures, all disclosed:**
- the learned convention mixture on LIRF NM-present rows ((c));
- NM-missing rows at the nine other airports, whose T windows start at SCHED. They are outside the clause population and reported under rule 7.

## Validation Quality

**Folds and references.**
- The frozen folds are used unchanged. S1 is a required WIN, the twin rule applies, and H is predicted only.
- E017's reuse conditions hold (ruling R).

| Clause | Verdict |
|---|---|
| 1 (criteria 1–3 against E005, all rows) | Decisive. The routed baseline alone is −31.7 to −49.0 s on the development folds, S1c −30.0 s and W1c −10.6 s. Criterion 3 has a 5-point margin at LIRF |
| 2(a) (criteria 1–2 on `NM_present_excl_LIRF`) | Decisive ((a)). W1c enters only through the twin rule |
| 2(b) (mean > −6.0 s) | Decisive. The noise-contrast means are −0.24, −0.12 and +0.25 s against a −6.0 s floor |
| 2(c) (`NM_present` bulk sign) | Insulated, as accepted in v1 |
| 3 (integrity) | Exact checks with a defined consequence |
| 4 (criterion 8) | 0.0 by construction, verified by 3(a) |

**Records** (non-blocking):
- **STATE.md is stale.** Its header is 14:03:03Z, and it still lists X-D03-S01-0001 as pending. The proposal's own allocation precondition requires it to be current, so this does not block.
- **The unchanged-tools list has gaps.** It omits `worker.py`, `run_experiment.py`, `data.py`, `models/__init__.py` and the helpers of `features.py` (`columns()`, `collapse_rare`, the column lists). All of them affect the run. The scope limit below closes the gap.

## Leakage Review

### Target Leakage

PASS

- **No input reads a DEP block time or target.** This holds by code, by unit test, by real-data masking invariance, and in my own real-data checks, which ran with every DEP block and taxi value nulled.
- **No target statistic is used.**
- **Both fits are fold-local.** The ridge's clips, fills, scaling and vocabulary come from the fold's training rows.

### Temporal Leakage

CONCERN

These are label notes, not blocking.
- **The five T features are admissible** (§6.2), but they reveal the target through the interval length. The contrast against E017, which contains `d_aobt3`, measures only their increment.
- **The ten P features are now P,** as verified ((e)). Their labels are relative to the proxy for *t_off*, and the runway is P by assumption.
- **Windows** reach only months in the fold's view. Embargo and holdout months are absent. SUBMIT_JUL has no June context (0.008 % of rows).

### Competition Availability

PASS

- Every input is present for ranking DEP rows.
- The ranking-month feature distributions match 2025.
- The increase in NM-missing rows at the nine other airports in January 2026 is disclosed under rule 2.

## Compute Review

### RAM

PASS

5–6.5 GB expected: E017 peaked at 4.18 GB, and the congestion build at 2.86 GB including silver. CLASS-M allows 8 GB.

### Runtime

PASS

- **Inputs.** FS2 has 32 model inputs against FS1's 17. The v1 review's "38 against 23" was wrong; this is an Advisor record correction.
- **Scaling.** E018 (11 inputs) took 418 s and E017 (17 inputs) 658 s. The 15 added inputs are low-cardinality counts. Congestion adds about 6 s per fold and the ridge up to 18 s per fold (E005: 1–18 s).
- **Estimate:** 17–25 min, under the 30 min class limit. Criterion 7 needs `within_class`, and the margin is about 5 min.

### Disk

PASS

About 10 MB of predictions per experiment, covered by manifests.

## Weakest Assumption

**That C beyond E017 reaches 6 s on NM-present rows at the nine other airports.**
- E017 already fits `d_aobt3` non-linearly.
- The EDA's after-anchor signal is carried by the counts that scale with the interval.
- The −6.0 s floor is conservative: about 3 times the largest perturbation.
- A real congestion effect of 3–5 s would therefore be recorded as a falsification. That is the accepted cost of a decisive clause, and it is the most likely outcome.

## Missing Control or Ablation

**None required.** The ablations are complete: E017 for C, H016 for R, and H017 for P against T.

**Named, not required:**
- A descriptive split of C by anchor-length band. It would separate the queue reading from the anchor-plausibility reading ((d)).
- A control with permuted congestion columns. It would measure the perturbation of adding 15 uninformative columns directly. The procedure and seed contrasts are the accepted proxies.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions** before `gate.py allocate H015 v2`:
   - (a) `research/day-03/acks/H015_ack_v2.md`, `H016_ack_v2.md` and `H017_ack_v2.md` are committed.
   - (b) `research/STATE.md` is current, with a measured header time. It records:
     - X-D03-S01-0001 (three REVISE decisions);
     - commit `63923e2`;
     - this exchange's result;
     - INC-0004 open;
     - the next action.
   - (c) The working tree is clean at allocation, and no other experiment runs.
   - (d) The proposal's unchanged-tools list holds from `2671dd3` until the last comparison of the chain.
2. **One primary run.**
   - `model: routed_lightgbm`, `feature_set: FS2`.
   - `params`: E017's exactly (`objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 1.0`, `bagging_fraction: 1.0`, `bagging_freq: 0`, `bin_construct_sample_cnt: 5000000`, `num_threads: 4`, `num_boost_round: 1000`), plus `route_ridge_params: {alpha: 1.0, winsor: [0.005, 0.995]}`.
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
3. **Comparisons,** in the chain order of the Validation Plan:
   - step 1: `compare.py <H015> E005`; `mechanism_check.py <H015> E017` on `NM_present_excl_LIRF`, `NM_present` and `excl_LIRF_NM_missing` (disclosure); `compare.py <H015> E017`;
   - step 2, after H016 v2 runs under its own ACCEPT: `route_check.py <H015> <H016> E005` and `mechanism_check.py <H015> <H016> LIRF_NM_missing`;
   - step 3: H017 v2 runs under its own ACCEPT.
4. **Conditional reproduction.** Only if clauses 1, 2 and 4 are not met and clause 3 is not met:
   - one `reproduction` allocation of H015 v2, with seed 43 and everything else identical;
   - then `reproduce_check.py <repro> <H015> --champion E005`, plus the prediction-file SHA-256 comparison on all 8 folds.
5. **Infrastructure failure.** One identical re-run with `--purpose rerun`, logged, only after an infrastructure failure (for example, a process killed by a container restart). A RESOURCE_FAILURE or TIMEOUT is recorded and not retried (brief §4).
6. **Promotion.**
   - Only if criteria 1–8 hold (B1–B4), with clause 3 not met.
   - Subject to the Day 3 phase-close review.
   - The holdout access is only as that review names it (rule 9).
7. **Advisor objections for criterion 8.** This review raises none beyond the pre-registered clauses and B3.
8. **Recording.** The analysis of each chain experiment (H015, H016, H017, the reproduction) records:
   - the CPU model string;
   - whether a container restart occurred since the previous chain experiment;
   - INC-0004 in its provenance.

   A 3(b) failure, or a byte difference in the reproduction, is still judged under the proposal's pre-registered rules. If a restart intervened, the determinism finding is recorded as cross-container.
9. **Not authorized:**
   - any change to features, parameters, folds, seed, routing rule, populations or clause code;
   - any search or early stopping;
   - scoring H outside the Day 3 phase-close check;
   - H016 or H017 as a candidate or as NEW;
   - **any change to code under `src/` or `scripts/`, to `pyproject.toml` or to `uv.lock`** between the H015 allocation and the last comparison of the chain. The run commits of the chain experiments may differ only in records (`research/`, `experiments/`, `orchestration/`).

Required acknowledgement path: `research/day-03/acks/H015_ack_v2.md`.
- It references the proposal hash (`468b442d…`) and this review's hash.
- It adopts preconditions 1(a)–(d), the scope limit in item 9 and the recording condition in item 8.
- It records the rule 6 reading in (b).

## Revision

None required for this version.

**Process notes (non-blocking):**
- **STATE.md** was last written at 14:03:03Z (precondition 1(b)).
- **Timestamps.** The proposals' `created_utc` (16:02:50Z) precedes their final file times (16:04:35–16:05:53Z).
- **Advisor record correction.** In `H015_review_v1.md` (Runtime), "38 inputs as with 23" should read 32 and 17.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Clause 1 not met (criteria 1–3 against E005 pass) | 0.93 |
| H015 − E005 development mean within −36 to −50 s | 0.78 |
| C: H015 − E017 mean on `NM_present_excl_LIRF` ≤ −6.0 s (2(b) not met) | 0.30 |
| C: criteria 1–2 pass on that population (2(a) not met) | 0.45 |
| C: `NM_present` bulk < 0 on at least 4 of 5 development folds (2(c) not met) | 0.78 |
| Clause 2 not met as a whole | 0.25 |
| No development-fold or twin cell with \|top-1\| ≥ 0.5 in H015 − E017 on the clause population | 0.65 |
| `route_check.py` passes, 3(a) and 3(b) | 0.95 |
| Reproduction byte-identical on all 8 folds (if run) | 0.92 |
| H015 within class (criterion 7) | 0.93 |
| H015 v2 promotable at the end of its chain | 0.20 |

Expected magnitude:
- **C on `NM_present_excl_LIRF`:** a mean of −2 to −7 s (central −4 s). Per development fold −1 to −9 s. W1c −3 to +6 s.
- **H015 − E005:** a development mean of −37 to −45 s (the development mean itself 437.7–445.7 s). W1c −5 to −14 s (the routed baseline's −10.6 s plus C).
- **H015 − E017 on all rows:** about +59 to +66 s development mean. The routing forgoes the tail gain.
- **C on the `NM_present` bulk:** −1 to −6 s per fold.

Primary expected failure mode:
- **Primary.** Clause 2(b) is met: the C mean lands between −6 s and −1 s, most likely −3 to −5 s, because E017's anchor already carries most of the in-taxi information. H015 is then falsified with its 37–45 s margin over E005 intact, and E005 stays champion by rule.
- **Secondary.** At small effects, one development fold (R2 or W1) comes out TIE or LOSS in 2(a), or a W1c LOSS voids W1's WIN.
