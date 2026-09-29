---
schema: advisor-review-v1
hypothesis_id: H013
proposal_version: 1
proposal_sha256: e47d382841a5382f6cd5aabf83ea85f4f6c554e93717dcb42b5f28aa420e3290
exchange_id: X-D02-S01-0004
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.92
created_utc: 2026-09-28T21:17:37Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE.**

The design rests on one claim: without row and feature subsampling, the LightGBM path does not consume the seed. **That claim is false on seven of the eight folds H013 fits.** Its reproduction expectation ("identical predictions; |Δ| = 0.00 s on every fold") is therefore false as configured, and so is the criterion 6 framing built on it.

**The finding (verified here, read-only).**

- **The mechanism.** `src/prc/models/gbm.py` passes `seed=seed` to LightGBM, and LightGBM derives `data_random_seed` from `seed`.
  - That seed draws the rows used to construct the feature bins whenever the training set exceeds `bin_construct_sample_cnt` (library default 200,000). This applies to numeric boundaries and to categorical bin maps.
  - Nothing in `src/`, `scripts/`, `config/` or `tests/` sets either parameter (grep). The worker passes `cfg["params"]` and `cfg["seed"]` unchanged.
- **The folds.** Training DEP rows per fold, from `research/day-01/audit/audit_stats.json` (`dep_by_month_airport`):

  | Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | H |
  |---|---|---|---|---|---|---|---|---|
  | Training rows | 1,387,414 | 1,571,364 | 1,757,038 | 1,537,475 | 1,611,189 | 1,005,519 | 153,706 | 1,919,370 |

  S1 equals the calibration figure in `config/resources.yaml`. **Every fold except W1c is above 200,000.**
- **The check.** Synthetic data only, through the unchanged `prc.models.gbm.lightgbm`. H013's parameters (no subsampling, `num_leaves` 255, `min_data_in_leaf` 100, `learning_rate` 0.05, 4 threads), 60 rounds, 20,000 validation rows. Nothing was written to the repository.

  | Training rows | Seed 42 against seed 43 | Seed 42 rerun |
  |---|---|---|
  | 150,000 | identical | identical |
  | **400,000** | **all 20,000 predictions differ** (max 271 s) | identical |
  | 400,000, bin sample covering every row | identical | identical |
  | 400,000, bin-sample seed fixed | identical | identical |

  The last two rows are diagnostics that locate the mechanism. They are not a recommendation (see the criterion 6 ruling).
- **The cited evidence does not reach this regime.**
  - `test_lightgbm_without_subsampling_is_seed_invariant` fits 1,500 training rows on one thread. It passes here (`tests/test_models.py`, 13/13), but it is correct only below the threshold.
  - The Observation cites "a 4-thread check on 20,000 synthetic rows … (commit `f84fea3`)". That commit adds only the 1,500-row, 1-thread test. The 20,000-row check is not committed, and it is below the threshold as well.

**Consequences.**
1. **The reproduction.** Run as written, the seed-43 reproduction would re-draw the bin sample on R1–W1, S1c and H. It would be a genuine perturbation test with an unknown outcome on R3 and S1, not a determinism check.
2. **E015's failure is not established as a subsampling effect.** E015 re-drew the bagging subsets, the feature subsets **and** the bin sample. Which of them moved the LIRF day-scale records is unknown. Removing subsampling may not remove the instability.
3. **The Disclosure on criterion 6 does not apply to v1.** It asks me to rule on a determinism check that v1's configuration does not produce. I rule on the question anyway (below), because v2 needs it.

**Rulings requested by the envelope (binding on v2).**
- **Criterion 6.** Full ruling in Validation Quality.
  - A configuration with **no random component** satisfies criterion 6 through a determinism check, as ridge did.
  - A configuration made seed-invariant by **fixing a random component outside the reproduction seed's reach** does not satisfy its intent.
  - In both cases, the E015 procedure spread must be carried as a disclosure.
- **E013 and E014 reuse (clauses 3 and 4).** Admissible, but the stated "bounds" measure the wrong quantity. Conditions are in Experimental Isolation and Revision item 3.
- **Criterion 8.** The widening to +7,000 s is **not accepted** on its stated rationale. The H009 rule (+6,500 s) applies to H013 unless v2 gives a rationale the committed evidence supports.

**What is sound:**
- the question, and its value for every later Tier 1 candidate;
- FS1 and the inputs (unchanged);
- the matched M1 reference H014;
- clauses 1, 2(a) and 2(b);
- the frozen folds, leakage and resources;
- the chain order.

**Verified here** (read-only). No December target was read, no model was fitted or scored on real data, and I wrote only the two review files.
- **Hashes.**
  - Both proposals match the envelope.
  - The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json`.
  - `.claude/agents/advisor.md` is `30fff5dd…`, matching `config/agents.yaml`.
  - `uv.lock` is `39df945c…` (LightGBM 4.7.0).
- **Code.**
  - `scripts/compare.py`, `scripts/mechanism_check.py`, `src/prc/attribution.py`, `src/prc/features.py` and `src/prc/models/gbm.py` are unchanged since `5ba9230`.
  - `gbm.py` is unchanged since `866b902`.
- **Tree and timestamps.**
  - The tree is clean at `ba15ca0`.
  - `created_utc` 21:00:14Z equals the file time and precedes the commit (21:00:33Z).
  - STATE.md's header time equals its commit time.
- **Ordering note (envelope).**
  - E015 was allocated at 20:25:34Z and E016 at 20:25:50Z.
  - From runtimes and finish times, E016 ran from 20:26:02 to 20:40:44Z and E015 from 20:40:44 to 20:55:12Z, so there was no concurrency.
  - H011 v2's preconditions needed only E012–E014. The reproduction's condition (clauses 1–4 not met) was settled when E014 completed (20:24:41Z).
  - The allocation slip has no scientific consequence.

## Scientific Validity

**The question is worth answering.** Can the H009 model class, fitted without procedure randomness, keep its margin and its three mechanisms?
- STATE.md is right that every bagged Tier 1 model that uses `d_sched` on LIRF NM-missing rows is exposed to criterion 6.
- A deterministic configuration is the cheapest principled route to certification. Seed averaging (k ≈ 13–16 fits) is correctly ruled out on cost.

**The Mechanism fails as stated.** "Removing subsampling removes the model's dependence on the seed" holds only on W1c, whose January-only training set (153,706 rows) is below the bin-construction sample.

**The E015 attribution is partial.**
- `experiments/E015/analysis.md` and STATE.md attribute the seed variance to "the bagged mixture predictions".
- The seed also re-drew the 200,000-row bin sample, which is about 11–14 % of each development fold's training rows. That sample fixes the upper-tail bin boundaries of `d_sched` and the categorical bin maps of `stand`, `op_prefix` and `ades`.
- For day-scale records (y ≈ 87,000 s, residual ≈ 70,000 s), a leaf-composition change of a few hundred seconds is worth tenths of a second of fold RMSE. A few such records can reach the 1.0 s tolerance.
- v2 must not rely on the subsampling-only attribution. Whether to append a correction to the E015 record is the researcher's call.

**An alternative the proposal does not name: bin-sample sensitivity.**
- Suppose the day-scale LIRF predictions move with the bin sample. Then a no-subsampling fit with a seed-driven bin sample is still one draw of a sensitive function, and v1's reproduction would measure that.
- With a configuration that has no random component, nothing measures it. That is the reason for the disclosure in ruling 5 below.

**Carried unchanged from H009 v3:**
- "M1–M3 unchanged because the inputs are unchanged" is a sound prior, and the clauses re-test it.
- Alternative Explanation 1 (bagging regularised the day-scale predictions) is correctly named. It is exactly what the criterion 8 cap exists to catch (Validation Quality).

## Novelty Relative to Existing Research

**Not redundant.**
- No completed experiment trains LightGBM without subsampling.
- It follows directly from E015 and re-earns every H009 clause for itself.
- It is not a search: the three values are the unique "off" setting.

## Experimental Isolation

**H013 against E012.** One conceptual change (subsampling off, three parameters). Adequate for the attribution-only comparison.

**H013 against H014 (M1).** Clean.
- Both use seed 42 on the same training rows, sorted by `MVT_ID_mvt`. Their bin-sample indices are therefore identical by construction, and every shared feature gets identical bins.
- The only difference is the six FS1 keys. This holds whichever option v2 takes for the seed (Revision item 1), provided H014 matches.

**Ruling on the E013 and E014 reuse.** On the same rows, RMSE differences add exactly:
- H013 − E013 = (H013 − E012) + (E012 − E013);
- H013 − E014 = (H013 − E012) + (E012 − E014).

What each term is:
- E012 − E013 and E012 − E014 are measured.
- H013 − E012 is the configuration change on the full-feature model, and the chain can measure it.
- **The unmeasured term is on the reference side:** the configuration change on FS1 − `d_sched` and on FS1 − anchor.

The proposal's "bound" is neither term.
- The E015 − E012 shift is the draw-to-draw spread of the *bagged* FS1 model, and it includes the bin-sample draw. It does not bound the effect of switching subsampling off.
- The proposal also quotes only S1 and R3. On LIRF NM-missing rows, the shifts across the development folds were:

  | Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
  |---|---|---|---|---|---|---|---|
  | Full dRMSE (s) | −16.9 | +56.7 | +124.4 | +82.2 | +93.5 | −133.5 | +0.4 |

  (`E015_vs_E012_mech_LIRF_NM_missing.json`)

**Clause 4 (E014) is admissible.**
- The E012 − E014 margins on NM-present rows are R1 −33.2, R2 −36.6, R3 −59.1, S1 −43.9, W1 −83.8, S1c −42.3 and W1c −95.9 s. All are WIN.
- The proposal expects the configuration effect on `NM_present_excl_LIRF` within ±4 s. Row 192622644 adds about ±10–15 s on S1 and S1c (`H009_review_v3.md`).
- No plausible configuration effect flips criterion 1 or 2 here.

**Clause 3 (E013) is admissible as a sign test.**
- The E012 − E013 margins are R1 −1,088.6, R2 −314.2, R3 −2,492.9, S1 −1,976.3 and W1 −2,475.2 s.
- Falsification needs three of five folds ≥ 0, and four folds have margins above 1,000 s. The thinnest is R2, at −314 s.
- "M3 supported for H013" is attributable to `d_sched` only if the configuration change is small against these margins. The chain can check that on its own side (H013 − E012 on the subgroup), but not on E013's.

The conditions are in Revision item 3.

## Validation Quality

**Folds.** The frozen folds are used unchanged: seven scored folds, with H predicted only. S1 is a required WIN, and B1–B4 carry.

**Clauses 1, 2(a) and 2(b)** are decisive, for the reasons given in `H009_review_v3.md`: the same populations and committed code, with the reference now matched.

**The clause code is not frozen.** Clauses 1–4 need `scripts/compare.py`, `scripts/mechanism_check.py` and `src/prc/attribution.py` unchanged from `5ba9230` until they are computed (Revision item 5).

### Ruling on criterion 6 (requested)

1. **The frozen rule** (`splits.yaml: promotion.reproduction`):
   - a gate-allocated reproduction with seed 43 and everything else identical;
   - every development-fold RMSE within 1.0 s;
   - criteria 1–3 re-checked against the champion.

   **Its intent:** the promoted result is reproducible, and it is not the product of one particular draw of the training procedure's randomness.
2. **No random component.** Suppose the fitted model is a deterministic function of the fold's training data. Then the rule reduces to a determinism check, and **that satisfies both its letter and its intent.**
   - The ridge precedent binds: "criterion 6 is a determinism check only for this model. That is inherent in the frozen rule, and not a defect" (`PHASE_CLOSE_D01_review_v1.md`, line 73).
   - A deterministic LightGBM is treated as ridge was.
3. **Randomness taken out of the seed's reach does not qualify.** A configuration that is seed-invariant because a random component is fixed independently of `seed` passes the letter and fails the intent: the reproduction would not re-draw that component. **I will not accept a criterion 6 pass on that basis.**
4. **Randomness still driven by `seed` (v1 as configured).**
   - Criterion 6 is then a genuine perturbation test under the frozen 1.0 s tolerance.
   - That is legitimate, but the expectation must be stated as such.
5. **In every case, E015 stays on the record.**
   - On a handful of LIRF day-scale convention records, this model class's fold RMSE moves with the draw: by up to 3.50 s on S1 and 1.73 s on R3.
   - A deterministic fit fixes one such function. It does not make it stable.
   - **If H013 is promoted,** the three-fit spread (E012, E015, H013) is a standing disclosure. A later margin over H013 of that order on R3, S1 or S1c, carried by LIRF NM-missing rows, is not mechanism evidence.
   - The promotion claim itself is robust to the draw: both H009-class fits pass criteria 1–3 against E005, 7/7 WIN (`repro_E015_of_E012.json`).
6. **Scope.** Determinism shown in this container (same binary, same `num_threads`) says nothing about the Days 5–7 laptop. The hand-off reproduction is a separate matter.

### Ruling on criterion 8 (the LIRF bulk trade)

**The statistic.** `NM_missing_LIRF.delta_rmse_bulk` against E005. Bulk is y < 3,600 s (`prc.attribution.BULK_MAX_S`), so differences on the same rows add exactly.

| Fold | R1 | R2 | R3 | S1 | W1 |
|---|---|---|---|---|---|
| E012 (s) | +5,045 | +2,279 | +1,835 | **+6,390** | +2,349 |
| E015 − E012 (s) | +144 | +148 | +8 | +66 | −40 |
| E015 (s, implied) | +5,189 | +2,427 | +1,843 | **+6,456** | +2,308 |

**Why the widening is not accepted.**
- **The rationale does not hold.** "A single deterministic draw can differ by the measured seed shifts" supports at most about 150 s on any development fold, and 66 s on S1. It does not support 500 s.
- **It was set after the observation.** It came after both fits of the class landed within 110 s (E012) and 44 s (E015) of the old bound on S1.
- **It weakens a guard in the candidate's favour.** The cap exists to catch a systematic worsening of the trade by the configuration change, which is Alternative Explanation 1.

**The rule for H013.** The expectation band (+1,500 to +7,000 s) is the researcher's. The resolution threshold is the Advisor's. For H013 it is H009's, unchanged:
- clause 3 not met;
- `NM_missing_LIRF.delta_rmse_bulk` against E005 ≤ +6,500 s on every development fold.

A different bound needs a rationale that the committed evidence supports.

## Leakage Review

### Target Leakage

PASS

- The inputs are FS1, unchanged. There are no target statistics.
- Bins, vocabularies and the rare-level collapse come from the fold's training rows only. Validation rows never enter bin construction, because the Dataset is built from `x_tr`.

### Temporal Leakage

CONCERN

These are label notes, as for H009 v3. They do not affect admissibility:
- `ades` is F on diversions (~0.03 % of rows);
- the takeoff hour and weekday, the `d_*` deltas and the hour-resolution schedule-delay proxy are T;
- stand is P on an assumption.

### Competition Availability

PASS

Same as H009 v3. Unseen levels map to `__RARE__`.

## Compute Review

### RAM

PASS

Below 5.5 GB expected (E012: 4.14 GB). Subsampling does not reduce the resident dataset.

### Runtime

PASS

- E012 took 906 s. At 1.1–1.4× (all rows and all features per tree), H013 needs about 17–21 min. The timeout is 45 min.
- The sequential chain (H013, H014, conditional reproduction) takes about 50–60 min.
- If v2 changes how the bins are built, re-estimate on fold H (1.92 M training rows).

### Disk

PASS

About 10 MB of predictions per run, covered by the manifest.

## Weakest Assumption

**The assumption.** The seed enters LightGBM only through subsampling. It is false above 200,000 training rows, which covers all five development folds.

**The assumption behind it.** The E015 instability is caused by subsampling. This is not established, because E015 also re-drew the bin sample.

## Missing Control or Ablation

- **Evidence of seed invariance at the development folds' scale** (1.0–1.9 M training rows), if v2 claims invariance.
  - The seed-43 reproduction is the only real-data evidence, and it comes last in the chain.
  - It should not be the first place where the premise is tested.
- **The measured confound for clauses 3 and 4.** H013 − E012 on `LIRF_NM_missing` and on `NM_present`, reported per fold (Revision item 3).

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- No allocation of H013 v1.
- H014 v1 (conditional ACCEPT, `H014_review_v1.md`) may not run before an H013 version ≥ 2 is ACCEPTED and acknowledged, and H013's primary run is COMPLETE.

Required acknowledgement path: none for v1. Submit `research/day-02/proposals/H013_v2.md` in a new exchange.

## Revision

**Required (minimal):**

1. **The seed-invariance premise.** Correct the Research Question, Observation, Mechanism, Expected Result and the Disclosure on criterion 6. The choice between the two options is the researcher's:
   - **(a) No random component on any scored fold.** Back the claim with committed evidence at a training size above LightGBM's bin-construction sample. Under the criterion 6 ruling, a configuration that fixes a random component independently of `seed` does **not** qualify.
   - **(b) Keep v1's configuration.** Re-register the seed-43 reproduction as what it is: a perturbation of the bin sample under the frozen 1.0 s rule. Give an expectation, and state what a pass or a fail would show about E015's attribution.

   Any training-parameter change beyond v1's three also changes H014's matched configuration (`H014_review_v1.md`, lapse rule).
2. **Evidence corrections.**
   - "The model code consumes the seed only through subsampling" is false above 200,000 training rows.
   - E015's instability cannot be attributed to subsampling alone.
   - The "4-thread check on 20,000 synthetic rows (commit `f84fea3`)" is not in that commit. Commit it or drop the citation. Either way, it is below the threshold.
3. **Clauses 3 and 4 (reuse of E013 and E014).**
   - Replace the E015 − E012 "bounds" with a correct statement of what is and is not measured (Experimental Isolation).
   - Add `mechanism_check.py <H013> E012 LIRF_NM_missing` and `mechanism_check.py <H013> E012 NM_present` to chain step 1, as reported figures.
   - Pre-register, per development fold, which measured configuration shift makes the reuse inadmissible on that fold, and how such a fold is then counted in the clause. The rule is the researcher's.
4. **Criterion 8.** Withdraw the widening to +7,000 s, or justify a bound with a quantity that measures what it claims. Otherwise H009's resolution rule applies to H013 unchanged (Validation Quality).
5. **Preconditions.** State them, carried from H009 v3:
   - `scripts/compare.py`, `scripts/mechanism_check.py` and `src/prc/attribution.py` stay unchanged from `5ba9230` until clauses 1–4 are computed;
   - `uv.lock` (`39df945c…`), `gbm.py`, the `fs1`-family feature functions of E012–E014 and silver stay unchanged, as the reuse of E012–E014 requires;
   - no experiment runs concurrently.

**Acceptable as is:**
- FS1, the three-parameter change, seed 42, the folds and the class;
- clause 1, and clauses 2(a) and 2(b) against H014;
- the chain order: H013, then H014, then clauses 3–4 from existing runs, then the conditional reproduction;
- the standing rules section and the rule 6 pre-registrations;
- the supplementary three-fit spread (attribution only). Criterion 6 ruling 5 turns it into a standing disclosure if H013 is promoted.

**Process notes (non-blocking):**
- **E015's dirty tree.** E015 ran from a dirty tree (`git_dirty_at_run: true`, run commit `6b84350`).
  - Between that commit and `924c2fa`, only outputs changed: the E015 and E016 records, the ledger, the journal and the comparisons. No code changed. That is consistent with E016's uncommitted outputs at launch.
  - The E015 analysis does not disclose it. Append a note.
- **The rule 8 tail-share band** (0.2–1.2, from H009's 0.3–1.1) was widened after E012's R2 came in at 0.25. It is an expectation, not a clause, but the proposal should say that it was set after E012.
- **INC-0003** is still `open`. Not blocking.

## Advisor Prediction

Probability of improvement, for v1's configuration as written:

| Event | P |
|---|---|
| The seed-43 reproduction gives identical predictions on every development fold (as pre-registered) | 0.02 |
| The seed-43 reproduction is within 1.0 s on every development fold (criterion 6) | 0.45 |
| Passes criteria 1–3 against E005 (clause 1 not met) | 0.92 |
| Clause 2(a) not met against H014 | 0.72 |
| Clause 2(b) not met against H014 | 0.88 |
| Clause 3 not met (E013 reuse) | 0.93 |
| Clause 4 not met (E014 reuse) | 0.96 |
| `NM_missing_LIRF.delta_rmse_bulk` against E005 ≤ +6,500 s on every development fold | 0.50 |

Expected magnitude:

| Quantity | Expected |
|---|---|
| Development mean | 372–384 s |
| H013 − E012 on `NM_present_excl_LIRF` | −2 to +3 s per development fold |
| Against E005 (mean dRMSE) | −100 to −112 s |
| H013 − H014 on `NM_present_excl_LIRF` | −5 to −10 s (mean) |

Primary expected failure mode:
- **Primary.** As configured, the reproduction re-draws the bin sample. R3 or S1 then moves by more than 1.0 s through the same LIRF day-scale records, and criterion 6 fails again.
- **Secondary.** Without bagging, S1's LIRF NM-missing bulk trade exceeds +6,500 s, and the criterion 8 objection stays unresolved.
