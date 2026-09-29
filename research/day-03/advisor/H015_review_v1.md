---
schema: advisor-review-v1
hypothesis_id: H015
proposal_version: 1
proposal_sha256: 2218b3eec778fbd4961c194bf2f0b0db32e31ee0d98efec0b02f7a77bc142334
exchange_id: X-D03-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.88
created_utc: 2026-09-29T15:53:21Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE.**

**The structure is sound.**
- C is tested against the matched deterministic reference E017 (ruling R).
- R is isolated exactly by H016.
- The frozen folds are used unchanged.
- No input reads a DEP block time or target.
- Routing the subgroup to the champion's model class is the kind of structural resolution that ruling B admits.

**Two defects block execution as written.**
1. **R's forward-risk rationale rests on false figures.**
   - The Observation says LIRF NM-missing DEP rows run "52–115 in Jan–Nov 2025", and that July 2026's 276 rows are "2.4 to 5.3 times any 2025 month".
   - Silver (a target-free count) gives 185, **337**, 197 and 168 for June–September 2025. July 2025 has *more* such rows than July 2026.
   - The Day 1 phase-close review had already recorded that "July has both the most such rows (337)". H015 itself cites "S1's 337 subgroup rows".
   - Ruling B makes the forward-risk rationale a condition of the alternative resolution, so the figures must be right.
2. **Clause 2 can be decided by one known record.** This is the defect that made H009 v2 REVISE.
   - The record is row 192622644: S1, LIRF, NM-present, y 87,002 s.
   - On `excl_LIRF_NM_missing` at S1, its signed share of the SSE change had magnitude ≥ 0.5 in **all four** Day 2 Tier 1 contrasts.
   - E017 − E018 on S1 is +1.59 s with the row and **−18.50 s without it**.
   - FS2 gives this row T counts of 486, 466 and 473, against a fold q99 of 33.

**Three smaller defects.**
3. The noise scale is quoted on the wrong population. On the clause population, the procedure shift E018 − E006 is −5.73 s on S1, the size of the −6.0 s floor, and all of it comes from that row.
4. Five of the ten "P" features read the row's own takeoff time on 0.086 % of DEP rows. The leakage section's claim that they do not is false.
5. Clause 3 does not say what its failure means for H015's decision.

**Verified here.** All checks were read-only or synthetic. No December target was read, no model was fitted or scored on real data (the test suite fits synthetic data only), and I wrote only the three review files.
- **Hashes.** The three proposal hashes match the envelope. `frozen.json` (`32c41c0f…`) and its six frozen files, `.claude/agents/advisor.md` (`30fff5dd…`, matching `config/agents.yaml`), `uv.lock` (`39df945c…`) and silver (`efde4262…`) are intact.
- **Code.**
  - Unchanged since E017's run commit `6e135de`: `gbm.py`, `linear.py`, `worker.py`, `run_experiment.py`, `data.py`, `splits.py`, `evaluate.py`, `metrics.py` and `pyproject.toml`.
  - `features.py` only appends FS2 and FS2_P.
  - Unchanged since `5ba9230`: `compare.py`, `mechanism_check.py`, `attribution.py`, `reproduce_check.py` and `gate.py`.
- **Predictions.** The prediction files of E005, E006, E012, E017 and E018 match their manifests (8 of 8 each).
- **Arithmetic.** The routed-E017 margins verify exactly.
- **EDA.** Its figures match `congestion.json`, and its target hygiene holds.
- **Tree, tests and lint.** `pytest` passes 113/113 and `ruff` is clean. The working tree is clean, and the task ledger holds no Day 3 allocation.
- **Secrets.** No credential value appears in the 394 tracked files.
- **Retry.** This is attempt 2 after a container restart with no `response.md`, which is legitimate under COMMUNICATION_CONTRACT §6.

## Scientific Validity

### (a) What holds

- **Mechanism C** is the standard runway-queue account. E017 already contains `d_aobt3`, so the C contrast measures what the counts add beyond the length of the interval (Alternative Explanation 1 is handled correctly).
- **Mechanism R is structural.**
  - The candidate's predictions on the subgroup are E005's, so the criterion 8 statistic is 0.0 by construction.
  - Routing also removes the subgroup from criterion 6's exposure: the ridge is a closed-form, deterministic fit, and E009 reproduced E005 exactly.
- **Rule 8 pre-registration for S1** (Missing Control 3) is present: H015 − H016 is expected positive on the full subgroup and negative on its bulk.
- **Fold-local fitting** is present, and H016 is the isolating ablation.
- **The routed-E017 margins** (E017 on non-routed rows, E005 on the subgroup, against E005) reproduce exactly by SSE arithmetic from `E017_vs_E005.json` and the metrics files: −31.69, −49.00, −32.60, −33.85 and −34.50 s; S1c −29.96 s; W1c −10.55 s.
- **The EDA.**
  - Targets were read only for Jan, Mar–Jun and Aug, which are never validation months.
  - Masking invariance holds on 1,919,370 rows. The code never selects a DEP block or taxi column.
  - The ranking-month quantiles match 2025.
  - The congestion block takes 5.7 s on S1's view, with a peak of 2.86 GB including silver.

### (b) R's forward-risk rationale (Revision 1)

LIRF DEP rows without `AOBT_3`, from silver (target-free):

| 2025 | Jan | Feb | Mar | Apr | May | Jun | **Jul** | Aug | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rows | 60 | 58 | 59 | 70 | 99 | 185 | **337** | 197 | 168 | 115 | 52 | 88 |

| 2026 | Jan | Jul |
|---|---|---|
| Rows | 107 | 276 |
| Share of LIRF DEP rows (same 2025 month) | 0.97 % (0.53 %) | 1.74 % (2.22 %) |

- **Both ranking months lie inside the 2025 monthly range (52–337).**
  - July 2026 has 0.82 times July 2025's count.
  - January 2026 has 1.8 times January 2025's count.
- **The "0.35–0.83" range is the Day 1 tail rate of this subgroup:** July 2025 (337 rows) at 0.35 and March 2025 (59 rows) at 0.83. The month with the most rows had the lowest rate.
- **What survives.**
  - The 2026 rate cannot be estimated without targets, and R removes the candidate's dependence on it.
  - Ruling B's own example ("276 … in July 2026 … and 2025 monthly convention rates of 0.35–0.83") is a rationale of exactly this kind.
- **What does not survive:** the claim that the ranking months carry an unprecedented count, which appears in the Observation and in Mechanism R.
- The next review judges the restated rationale.

### (c) Clause 2 and row 192622644 (Revision 2)

**The row.** 192622644 is in July 2025 (S1 and S1c validation), at LIRF, NM-present.
- y is 87,002 s, `d_aobt3` 87,181 s and `d_sched` 87,001 s.
- It is inside `excl_LIRF_NM_missing`.

**Evidence.** S1 on `excl_LIRF_NM_missing`, derived exactly from committed comparison JSONs and metrics.
- The derivation reproduces `E016_vs_E010_mech_excl_LIRF_NM_missing.json` to 0.001 s on all seven folds.
- The row's target is the committed `dominant_row` value, and its predictions come from the prediction files.

| Contrast | S1 dRMSE | Predictions on the row (candidate / reference) | Row's share of the S1 change | S1 without the row |
|---|---|---|---|---|
| E017 − E018 (static keys, deterministic) | +1.59 | 6,471 / 22,473 | **+11.13** | **−18.50** |
| E012 − E006 (static keys, bagged) | −2.99 | 5,912 / 16,545 | **−4.07** | **−17.57** |
| E018 − E006 (procedure, FS0) | −5.73 | 22,473 / 16,545 | **+1.06** | +0.39 |
| E017 − E012 (procedure, FS1) | −1.14 | 6,471 / 5,912 | +0.60 | −0.54 |

- **S1c shares:** +28.56, +2.47, −0.73 and −0.01.
- **The other folds.** On R1–R3 the static-key contrast E017 − E018 is −13.9, −13.2 and −12.4 s, and on W1 −8.0 s. S1 is the outlier only because of this row.
- **S1's RMSE on this population is about 343–349 s.** Moving the row's prediction from E017's value to E018's shifts S1 by about 20 s. The expected C effect is −8 to −25 s.

**FS2 makes the row more extreme,** with target-free values computed on S1's view:
- `cg_dep_to_during` is 486, `cg_dep_to_rwy_during` 466 and `cg_arr_land_during` 473. The view's q99, q99.99 and maximum of `cg_dep_to_during` are 33, 199 and 1,058.
- In S1's training months, only **4 NM-present rows** exceed 100 takeoffs during taxi (largest `d_aobt3` 16,622 s).
- **1,082 of the 1,086 training rows above 100 are NM-missing,** with *t_off* = SCHED: 1,020 at the other nine airports and 62 at LIRF.
- The FS2 prediction on this row is therefore an extrapolation with no NM-present support, and its direction is unknowable.

**Consequence.**
- Clause 2(a)'s required S1 WIN, its S1c twin and about a fifth of clause 2(b)'s mean can be set by one record. That could produce a spurious confirmation or a spurious falsification.
- The proposal names the row under rule 6 but pre-registers nothing that neutralises it. This is item 1 of `H009_review_v2.md` on the same row.
- **A second volatile block sits in the same population:** NM-missing rows at the other nine airports. They hold 15.6 % of E010's SSE in this population on W1, which is ±5 s per ±15 % (`H011_review_v2.md`). They are exactly the rows whose T windows start at SCHED.
- Clause 2(c) (`NM_present` bulk) is insulated from both blocks; clauses 2(a) and 2(b) are not.

### (d) Noise scale (Revision 3)

- **The procedure figure is on the wrong population.** The proposal's 2.11 s is on `NM_present`, not on the clause population.
- **On `excl_LIRF_NM_missing` (development folds R1, R2, R3, S1, W1; twins S1c, W1c):**
  - **Seed** (E015 − E012): +0.04, +0.33, +0.23, +1.33, −1.94. Committed.
  - **Procedure, FS1** (E017 − E012): −1.71, +0.35, +0.23, −1.14, +0.93; S1c −2.09, W1c +1.48. Derived.
  - **Procedure, FS0** (E018 − E006): +0.29, −0.78, +0.17, **−5.73**, −2.62; S1c +1.40, **W1c +5.92**. Derived.
- **The −6.0 s floor** survives the first two. It does not survive the third on S1, where the whole shift is row 192622644 (+0.39 s without it).
- **"Both deterministic, so seed noise should be zero."**
  - Determinism removes re-run noise. It does not remove perturbation sensitivity: adding 15 uninformative columns would still change the trees.
  - The floor's logic (three times the perturbation proxies) is right. That sentence cannot be used to argue that smaller effects are decisive.

### (e) The P labels (Revision 4)

**A synthetic check** varied only the row's own `MVT_TIME` and held its *t_off* proxy fixed. It shows which "P" features depend on the row's own takeoff:
- `cg_dep_taxiing` and `cg_dep_taxiing_rwy`: −1 when *t_to* ≤ *t_off*. The unconditional −1 assumes the row counted itself, which it does only when *t_to* > *t_off*.
- `cg_dep_to_p15` and `cg_dep_to_rwy_p15`: +1, the row counting itself, when *t_to* is in [*t_off* − 15 min, *t_off*).
- `cg_dep_to_p30`: +1 when *t_to* is in [*t_off* − 30 min, *t_off*).

**Rows affected** (target-free), where the row takes off at or before its *t_off* proxy:
- 2,091 DEP rows (0.086 %): 1,235 NM-present (0.051 %) and 856 NM-missing (3.1 %; 835 at the other nine airports).
- Ranking months: 119 rows in January 2026 and 168 in July 2026.

**What follows.**
- **It is not a leakage violation.** T is admissible (§6.2). The bits are functions of `flt_missing`, `d_aobt3` and `d_sched`, which FS1 already contains (no row has `AOBT_3` missing with `EOBT_1` present), so neither C nor H017's P/T split is confounded in information.
- **But two statements are false:**
  - "The self term is excluded without reading the row's own takeoff time";
  - the `congestion.py` docstring's "a P feature never reads the row's own takeoff time".
- The labels exist for the Days 5–7 causal-only variant.

### (f) Clause 3 (Revision 5)

- **The consequence is ambiguous.** Clause 3 sits under "H015 is falsified if any of the following holds", yet says a failure makes the run "INVALID as a test of R". Its decision consequence is undefined: B2 (falsified, not promoted), the brief's INVALID, or an R test that is void while promotion is decided on the other clauses.
- **The risk is low.**
  - `gbm.lightgbm` pins `deterministic=True`, `force_row_wise=True` and 4 threads.
  - The worker calls the same feature function and the same `gbm.lightgbm` for `routed_lightgbm` and `lightgbm`, and there is no feature cache.
- **A 3(b) failure matters beyond R.** It would also be a cross-process determinism failure, which bears on criterion 6's premise.

### (g) The expected size of C (not a defect)

- **What the EDA's residual measures.** The after-anchor residual is `r_anch` = y − `d_aobt3` − c = AOBT_3 − BLOCK − c, the anchor's own error.
- **Why the counts partly re-fit the anchor.** The T counts over (*t_off*, *t_to*) scale with `d_aobt3`. Their binned means therefore partly re-fit the anchor non-linearly, and the three in-taxi counts' Spearman correlations with `r_anch` are negative (−0.04 to −0.09). E017's trees already do that fit.
- **No control.** The EDA has no binned-`d_aobt3` baseline for comparison.
- **Consequence.** The −8 to −25 s expectation is probably optimistic.
- **Internal inconsistency.**
  - The development mean equals 482.73 plus the mean dRMSE against E005. So "−35 to −65 s" implies 417.7–447.7 s, not 405–445 s.
  - The routed-E017 baseline alone is 446.4 s.

## Novelty Relative to Existing Research

- **Congestion reconstruction** is the Day 3 priority (brief §11), and **routing** is new. Neither repeats completed work.
- **Rule 10 is not engaged.** H015 adds new features and a new structure, changes no threshold, population or counting rule, and re-submits no completed configuration.

## Experimental Isolation

| Claim | Contrast | Population | Only difference | Status |
|---|---|---|---|---|
| C | H015 − E017 | `excl_LIRF_NM_missing` | + 15 congestion columns (the routing plays no part) | Isolated. **Not decisive on S1 and S1c** (row 192622644) |
| C, bulk | H015 − E017 | `NM_present`, y < 3,600 s | Same | Insulated. A sign test |
| R | H015 − H016 | `LIRF_NM_missing` | Routing only (identical fits elsewhere, checked by `route_check.py`) | Exact |
| P against T | H017, H016 | See `H017_review_v1.md` | The five T columns | See that review |

**R's "zero relative risk, by construction" holds on the routed subgroup only.**
- The LightGBM's convention mixture still acts on LIRF NM-present rows.
- Example: W1c row 183908048 has an anchor of 721 s and y of 722 s. E017 predicted 3,801 s on it and E018 10,067 s (`E017_vs_E018_mech_NM_present.json`).
- Rule 8 requires this residual exposure to be disclosed.

## Validation Quality

- **Folds.** The frozen folds are used unchanged. S1 is a required WIN, the twin rule applies, and H is predicted only.
- **The E017 reuse conditions hold** (Summary, "Verified here").
- **Clause 1 is decisive.** On the development folds, the routed baseline alone is −31.7 to −49.0 s. S1c is −29.96 s and W1c −10.55 s before C.
- **Clause 4** is 0.0 by construction, and `route_check.py` (3(a)) verifies it.
- **Clause 2** is not decisive as written; see (c) and (d).
- **Criterion 6** carries the prediction-file SHA-256 comparison (Missing Control 2).
- **Rule 6 against E005.** On S1 and S1c, E005 predicts 2,513 and 2,548 s on row 192622644. If FS2 moves H015's prediction toward E018's 22,473 s, the row would carry about a third of the routed S1 change. It should be named as the likely top row.
- **The unchanged-tools precondition** omits `scripts/route_check.py` (the clause 3 tool), `scripts/reproduce_check.py` and the `fs2`/`fs2_p` bodies.
- **Uncommitted evidence.** The real-data byte-identity check of the routed ridge (W1c, R2) has no committed artifact; only the proposal and STATE assert it. `route_check.py` will check this on every fold at run time, so it does not block.

## Leakage Review

### Target Leakage

PASS

- **No input reads a DEP block time or target.** This holds by code, by unit test, and by real-data masking invariance.
- **No target statistic** is used.
- **The ridge's quantile clips, fill values, scaling and vocabulary** come from the fold's training rows.

### Temporal Leakage

CONCERN

- **The T features are admissible** (§6.2), but they reveal the target through the interval length. The C contrast against E017, which contains `d_aobt3`, measures what they add.
- **Five P features carry T bits** on rows that take off before their proxy ((e)).
- **Windows** reach only months in the fold's view. Embargo and holdout months are absent. A validation month always has its previous month available, and SUBMIT_JUL does not (§6.5; 0.008 % of rows).
- **The routing key** (`ADEP_mvt`, `AOBT_3` missing) is label P.

### Competition Availability

PASS

- **Every input is present for ranking DEP rows,** and ranking ARR rows are complete.
- **Forward exposure to disclose under rule 2.** NM-missing rows at the other nine airports, which are not routed, are **1.66 % of those airports' January 2026 DEP rows against 0.97 % in January 2025** (July: 1.45 % against 2.05 %). The model's handling of them comes from 2025.
- **This is not a convention bet.** Day 1 found block-at-schedule at those airports at or below the base rates.

## Compute Review

### RAM

PASS

- **Baselines.** E017 peaked at 4.18 GB. The congestion build peaks at 2.86 GB including silver.
- **Additions.** FS2 adds 15 float columns. The ridge runs after the LightGBM fit returns; E005's whole process peaked at 3.76 GB.
- **Expected peak:** 5–6.5 GB, below 8 GB.

### Runtime

PASS

- **Baselines.** E017 took 668 s. The congestion block takes about 6 s per fold, and the ridge about 12 s per fold (E005: 94 s for 8 folds).
- **Row-wise histograms** cost about 1.65 times as much with 38 inputs as with 23.
- **Expected:** 17–25 min, below 30 min.
- **The chain** (three primaries and one reproduction) runs sequentially in about 75–100 min.

### Disk

PASS

About 10 MB of predictions per experiment, covered by manifests.

## Weakest Assumption

**That clause 2's S1 outcome on `excl_LIRF_NM_missing` measures congestion.**
- In every Day 2 Tier 1 contrast on this population, one record's signed share of S1's change had magnitude ≥ 0.5.
- FS2 gives that record the most extreme inputs in the fold.

**Second: the size of C beyond the anchor.** The EDA's after-anchor figures partly re-measure the anchor ((g)).

## Missing Control or Ablation

- **The ablations are complete:** E017 for C, H016 for R and H017 for P against T.
- **What is missing:**
  - protection of the decisive C clause against a known single record (Revision 2);
  - the noise scale on the clause population (Revision 3).
- **An EDA control that is not required:** a binned-`d_aobt3` baseline on `r_anch`. It would show how much of the T counts' after-anchor figure is interval length.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- No allocation of H015 v1, H016 v1 or H017 v1.
- No FS2 or FS2_P model may be fitted on a frozen fold before an H015 version ≥ 2 is ACCEPTED and acknowledged. Outside the routed subgroup, any FS2 outcome is H015's outcome, and it would reveal the congestion effect before clause 2 is fixed.
- Still allowed:
  - target-free checks;
  - EDA on never-validation months under the Day 2/3 hygiene;
  - synthetic tests;
  - comparisons of existing prediction files without truth.

Required acknowledgement path: none for v1. Submit `research/day-03/proposals/H015_v2.md` in a new exchange.

## Revision

**Required (minimal):**

1. **Forward-risk figures** (Observation, Mechanism R, Scientific Value).
   - Replace "52–115 in Jan–Nov 2025" and "2.4 to 5.3 times any 2025 month" with the target-free monthly counts in (b), against the same 2025 month and against the 2025 range.
   - Restate R's rationale on those figures. It must still not rest on E006–E018 outcomes.
2. **Clause 2 must not be decidable by one known record.**
   - Re-specify clauses 2(a) and 2(b) so that neither the S1 and S1c outcomes nor the mean can be decided by row 192622644. The population, statistic or decision rule is the researcher's choice.
   - State the chosen population's exposure to NM-missing rows whose T windows start at SCHED.
   - Pre-register the expected rule 6 dominant rows per fold and twin.
   - Define any new population in committed code with a test before allocation, and add it to the unchanged-tools precondition.
3. **Noise scale on the chosen population.**
   - Give E015 − E012, E017 − E012 and E018 − E006 on that population, per development fold.
   - If any exceeds a third of the floor, say why the clause is still decisive (Missing Control 4).
4. **P labels.**
   - Either relabel the five features (T on rows whose takeoff precedes their *t_off* proxy), or re-implement them so that they never use the row's own takeoff time. The choice is the researcher's.
   - Either way, add a unit test of the stated property, and correct the proposal's leakage notes and the `congestion.py` docstring.
   - If the code changes, re-verify masking invariance on real data before allocation.
5. **Clause 3.**
   - State the decision consequence of a 3(a) failure and of a 3(b) failure separately.
   - State how a 3(b) failure bears on criterion 6's determinism premise.
6. **Record items.**
   - Add `route_check.py`, `reproduce_check.py` and the `fs2`/`fs2_p` bodies to the unchanged-tools precondition.
   - Name row 192622644 as a possible top row against E005 on S1 and S1c.
   - Disclose R's residual exposure on LIRF NM-present rows (Experimental Isolation).
   - Commit the routed-ridge real-data check, or call it uncommitted.
   - Make the development-mean expectation consistent with the dRMSE range.

**Acceptable as is:**
- FS2's fifteen features (subject to item 4), E017's LightGBM parameters, the routing rule and E005's ridge parameters, the folds, the seed and the class;
- clauses 1, 2(c) and 4;
- the criterion 6 handling;
- the chain order and the conditional reproduction;
- the rule 8 pre-registration for S1;
- rule 11 reporting through H016.

**Process notes (non-blocking):**
- **INC-0004 is open.** The proposal discloses it, and it is not a block here, as with INC-0003.
- **Standing rule 11.** The C headline next to H016 − E017 on all rows is the right pairing.

## Advisor Prediction

Probability of improvement:

| Event (for the v1 design, if it were run) | P |
|---|---|
| Clause 1: criteria 1–3 against E005 pass | 0.92 |
| H015 − E005 development mean within −35 to −65 s | 0.75 |
| C: H015 − E017 mean on `excl_LIRF_NM_missing` ≤ −6.0 s | 0.35 |
| C: clause 2(a) passes (criteria 1–2, S1 WIN included) | 0.40 |
| C: `NM_present` bulk < 0 on at least 4 of 5 development folds (2(c) not met) | 0.75 |
| Row 192622644 carries \|share\| ≥ 0.5 of S1's change in H015 − E017 on `excl_LIRF_NM_missing` | 0.80 |
| Removing that row would change S1's 2(a) outcome | 0.45 |
| `route_check.py` passes, 3(a) and 3(b) | 0.95 |
| The reproduction is byte-identical on all 8 folds | 0.93 |
| H015 v1 would be promotable at the end of its chain | 0.25 |

Expected magnitude:
- **H015 − E005:** development mean −37 to −47 s (the routed baseline is −36.33 s, plus C). W1c −8 to −20 s.
- **C on `excl_LIRF_NM_missing`:** −2 to −10 s on R1–R3 and W1. S1 is set by row 192622644, within about ±20 s.
- **C on the `NM_present` bulk:** −1 to −6 s per fold.
- **H015 − E017 on all rows:** about +58 to +66 s development mean. The routed baseline is 446.4 s against E017's 378.8 s (+67.6 s), and C then subtracts 2–10 s. H015's development mean: 436–445 s.

Primary expected failure mode:
- **Primary.** C's decisive clause measures something else.
  - As written, S1 in clause 2(a) is set by row 192622644.
  - Once that is fixed, C on the clause population may land between −6 s and 0, because the anchor already carries the in-taxi information.
  - Clause 1 and criterion 8 pass either way. The likely outcome is H015 falsified on clause 2, with its margin over E005 intact.
- **Secondary.** W1c, trained on January alone, is LOSS for C. That voids W1's WIN and leaves S1 to carry criterion 2.
