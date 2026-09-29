---
schema: advisor-review-v1
hypothesis_id: H013
proposal_version: 2
proposal_sha256: 13fc73618aba0d9a3e8ce9832e0896fa79bac6a177112714e9f2ebe09f7d20e9
exchange_id: X-D02-S01-0005
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-09-28T21:43:57Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT, with preconditions, one new Advisor objection rule under promotion criterion 8 (objection T), and three recorded readings.**

**v2 meets all five required items of `H013_review_v1.md`.**
1. **The premise now holds.** The training procedure has no random component on any fold, and the committed test covers the regime above the bin-sample threshold.
2. **The evidence corrections are made.** E015's attribution correction and its dirty-tree note were *appended*, and the earlier text is unchanged.
3. **Clauses 3 and 4:**
   - the E015 "bounds" are gone;
   - the candidate-side shift is measured in chain step 1;
   - a per-fold admissibility rule and a conservative counting rule are pre-registered.
4. **Criterion 8** reverts to H009's rule (≤ +6,500 s).
5. **The preconditions are stated.**

**The premise, checked here at fold scale (synthetic data only, nothing written to the repository).**
- **The frame.** 1,919,370 training rows (fold H's count) and 60,000 validation rows, shaped like FS1:
  - 9 categoricals, four of them with 160–1,800 Zipf-distributed levels;
  - 8 numerics, including an anchor with 4 % NaN and day-scale records (0.04 % of rows, y 15,000–130,000 s).
- **The fit.** H013 v2's parameters (255 leaves, `min_data_in_leaf` 100, 4 threads) with 60 rounds, through the unchanged `prc.models.gbm.lightgbm`.

  | Configuration | Seed 42 against seed 43 | Seed 42 rerun |
  |---|---|---|
  | H013 v2 (`bin_construct_sample_cnt` 5,000,000) | **identical** (0 of 60,000 differ) | identical |
  | H013 v1 (default bin sample) | all 60,000 differ (max 17,640 s) | — |
  | H013 v2 against H013 v1, both seed 42 | all 60,000 differ (max 16,719 s) | — |

  - The run took 64 s in total, at a 1.59 GB peak.
  - The script is outside the repository: `/tmp/claude-0/-home-user-prc-data-challenge-2026/0b2147c0-74e1-4b58-965c-6ea22d5b4eaa/scratchpad/scale_check.py`.
- **What this adds to the committed test.** The committed test fits 260,000 rows with categoricals of at most 40 levels. This check reaches the development folds' scale and covers high-cardinality categorical bin maps. Together they settle the "Missing Control" of `H013_review_v1.md`, as far as synthetic data can. The seed-43 reproduction remains the real-data test.
- **The third row matters** (Scientific Validity). Binning from all rows does more than remove a draw: it is a systematic change to the model, and it moves day-scale predictions by thousands of seconds.

**Why ACCEPT rather than REVISE.** The four findings below are either within the Advisor's remit (criterion 8: Advisor objections resolved) or readings of the registered rules. None changes what is run, what is compared, or what is promotable in the candidate's favour.
1. **Clause 4's reuse does not cover the causal twins that criterion 2 reads** (Experimental Isolation).
   - The frozen twin rule voids an S1 WIN when S1c is LOSS, and S1 must WIN.
   - The admissibility table checks only the five development folds. My v1 instruction said "per development fold", so the gap is partly mine.
   - I close it as **objection T** under criterion 8, the same instrument H009 v3 used for the LIRF bulk trade.
2. **Clauses 3 and 4, as designed, are carry-over tests rather than falsification tests.**
   - Under the registered rule, every clause 3 fold that would fail is necessarily inadmissible.
   - Clause 4 can fail with every fold admissible only if a fold's bootstrap is wider than its margin.
   - A "met" outcome reached through inadmissible folds therefore means "not re-established by reuse", not "falsified" (recorded reading 1).
3. **Criterion 6: "identical predictions" needs a stated check and a stated consequence** (recorded reading 2).
4. **The admissibility thresholds are defined at full precision.** The table's rounded values do not govern (recorded reading 3).

**Verified here** (read-only). No December target was read, and no model was fitted or scored on real data.
- **Hashes.**
  - Both proposals match the envelope.
  - The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json`.
  - `.claude/agents/advisor.md` is `30fff5dd…`, matching `config/agents.yaml`.
  - `uv.lock` is `39df945c…` (LightGBM 4.7.0).
- **Code.**
  - `scripts/compare.py`, `mechanism_check.py`, `reproduce_check.py`, `run_experiment.py`, `gate.py` and all of `src/prc/` are unchanged since `5ba9230`. `gbm.py` is unchanged since `866b902`.
  - Function bodies (AST): `fs1` and `collapse_rare` are identical to `cba278d`; `fs0` to `866b902`; `fs1_no_dsched` and `fs1_no_anchor` to `5ba9230`.
- **Plumbing.**
  - The worker passes `params` to `gbm.lightgbm` unchanged, so `bin_construct_sample_cnt` reaches `lgb.train`. There is no parameter whitelist.
  - The Dataset is built from `role == 'train'` rows only.
  - `_predictions` checks every stored prediction file against its manifest SHA-256, so the reuse of E012–E014 is integrity-checked.
- **Numbers.**
  - Training DEP rows per fold (recomputed from `audit_stats.json`, counts only) match the proposal. The maximum is 1,919,370 (H).
  - The final SUBMIT folds train on 2,085,047 rows, also below 5,000,000.
  - Every margin, admissibility figure and E015-shift figure cited in the proposal matches the committed JSONs.
- **Records.**
  - `experiments/E015/analysis.md`: additions only since `924c2fa`.
  - `experiments/ledger.jsonl`: the only other change is the E012 and E015 `decision` fields (None → INCONCLUSIVE, `b03b63a`).
- **Tree and timestamps.**
  - `created_utc` 21:24:47Z equals the file times and commit `23602e6`.
  - The tree is clean, and no experiment is ALLOCATED or RUNNING.
  - `tests/test_models.py` passes (14/14).

## Scientific Validity

**The question is worth answering, and the mechanism now holds.**
- With no row or feature subsampling and bins built from every training row, the fitted model is a deterministic function of the fold's training rows.
- **Ruling 2 of `H013_review_v1.md` applies, not ruling 3.**
  - Binning from all rows makes **no draw**. That is different in kind from pinning `data_random_seed`, which would fix a draw outside the reproduction seed's reach.
  - The proposal rejects the pinned-seed route explicitly and correctly.

**Binning from all rows is also a systematic model change, and the proposal half-says this.**
- It fixes the upper-tail bin boundaries of `d_sched`, and the categorical bin maps (level order and cut-off) of `stand`, `actype`, `op_prefix` and `ades`. Under E012's configuration these depended on a 200,000-row draw, about 11–14 % of each development fold.
- **In the synthetic check, this change alone** (same seed, both unbagged) moved every prediction, and moved day-scale records by up to 16,719 s.
- **Consequences:**
  - **H013 − E012 on `LIRF_NM_missing` may be large:** hundreds to over a thousand seconds of subgroup RMSE on some folds. The admissibility rule is built to catch exactly this. Expect it to bite on R2, whose threshold is 157 s.
  - **Alternative Explanation 1 should read "bagging and sampled binning were regularising the day-scale predictions."** The unchanged +6,500 s criterion 8 cap and clause 1 guard it either way.

**The standing disclosure (ruling 5) is carried correctly, and the check reinforces it.** A deterministic fit selects one function. Its day-scale LIRF predictions are not stable against an arbitrary procedural choice (bagging draws, bin sample). A later margin over H013 of the E015 order (R3 1.73 s, S1 3.50 s), carried by LIRF NM-missing rows, is not mechanism evidence.

## Novelty Relative to Existing Research

**Not redundant.**
- No completed experiment trains LightGBM without subsampling, or with bins built from all rows.
- It is not a search: each of the four values is the unique setting that removes one random component.

## Experimental Isolation

**H013 against E012.** One conceptual change: deterministic training, through four parameters. It is attribution only, and it now feeds the admissibility rule.

**H013 against H014 v2 (M1). Clean.**
- Both bin from all rows of the same training rows, in the same `MVT_ID_mvt` order, so every shared FS0 feature gets identical bin mappers by construction.
- FS1's six keys receive all-row bins as well. That is part of the M1 contrast under this procedure, which is what H013 claims.

**Clauses 3 and 4 are carry-over tests** (reading 1).

Write M_f for the committed margin (E012 − E013, or E012 − E014) on fold f, which is negative on every fold, and Δ_f for the measured candidate-side shift (H013 − E012) on the same population. On the same rows, RMSE differences add exactly, so the computed clause statistic is C_f = Δ_f + M_f.

- **Clause 3.**
  - A failing fold (C_f ≥ 0) has Δ_f ≥ |M_f|, so it is always inadmissible (|Δ_f| ≥ ½|M_f|).
  - An admissible fold has C_f < −½|M_f| < 0, so it always passes.
  - **Clause 3 is therefore met if, and only if, at least three development folds are inadmissible.** The sign test is subsumed.
- **Clause 4.**
  - If every development fold is admissible, each C_f < −½|M_f|, which is −16.6 to −41.9 s.
  - With the E012 − E014 bootstrap half-widths (q10–q90: 2.6–12.6 s), each fold is all but certainly a WIN, and the pooled mean is below −25.6 s.
  - It could still fail with every fold admissible, but only if a fold's cluster bootstrap were wider than its margin: for example, one day-scale row dominating S1. That would be a genuine failure under the registered rule.
  - An inadmissible fold makes the clause undecidable by the registered rule.
- **So the reused ablations can confirm M2 and M3 for H013, or leave them undecided.** Clause 3 cannot falsify M3. Clause 4 can falsify M2 only in the unlikely case above.
  - That is adequate for H013's claim. M2 and M3 were established by matched ablations (E013, E014) on identical inputs, and H013 claims only that they carry over under the deterministic procedure.
  - It is conservative for promotion, because "undecided" blocks promotion.
  - It must not be recorded as evidence against a mechanism.

**The causal twins are not covered in clause 4** (objection T).
- **Criterion 2 reads S1c and W1c** (`promotion.criterion_2.twin_rule`, `prc.metrics.promotion_check`). An S1c LOSS voids the S1 WIN, and S1 must WIN. A W1c LOSS voids the W1 WIN.
- **The rule's own reasoning covers the twins.** It says "criteria 1–2 pool all folds", yet its trigger checks development folds only.
- **An admissible S1 does not imply an admissible S1c.**
  - S1c has a different training set (Jan–Jun, 1,005,519 rows).
  - The E015 − E012 shifts differ in sign between S1 and S1c: on `LIRF_NM_missing` +82.2 against −133.5 s; on `excl_LIRF_NM_missing` +1.33 against −0.59 s.
  - Both twins' NM-present rows include row 192622644 (y 87,002 s). It moves S1 and S1c by about 11 s per 8,000–10,000 s change in its prediction (`H009_ack_v3.md`, exposure 4; `E012_vs_E006_mech_NM_present.json`).
- **The twin margins** (E012 − E014 on `NM_present`) are S1c −42.306 s and W1c −95.932 s. Half of each is 21.153 s and 47.966 s.
- **No new computation is needed.** `mechanism_check.py <H013> E012 NM_present` already reports `per_fold.S1c` and `per_fold.W1c` (it iterates over the development folds and the twins).

## Validation Quality

**Folds.**
- The frozen folds are used unchanged: seven scored folds, with H predicted only.
- S1 is a required WIN. B1–B4 carry, and B3 is restated in the proposal.

**Clauses 1, 2(a) and 2(b)** are decisive, for the reasons given in `H013_review_v1.md`: the same populations and committed code, with the matched reference H014 v2.

**The clause code is not frozen.** Precondition (c) keeps it fixed until clauses 1–4 and the objection T statistic are computed.

**Criterion 6 under ruling 2** (reading 2).
- **What `reproduce_check.py` checks.** It compares development-fold RMSEs only. |Δ| = 0.00 s is necessary for identical predictions, but not sufficient.
- **What prediction identity is checked from.** The per-fold prediction SHA-256s recorded in the two `manifest.json` files.
  - Precedent: E005 and E009 (and E002/E007, E003/E008) have byte-identical prediction files on all eight folds.
  - E012 and E015 differ on all eight, including W1c. W1c is below the bin threshold, so it isolates the subsampling component.
- **If any fold's file differs:**
  - the "no random component" premise is falsified, and that must be reported;
  - "determinism check" may no longer be used;
  - criterion 6 is read as a genuine perturbation test under the frozen 1.0 s tolerance (ruling 4).

**Criterion 8, the LIRF bulk trade.** H009's rule is registered unchanged.
- **The rule:** clause 3 not met, and `NM_missing_LIRF.delta_rmse_bulk` against E005 ≤ +6,500 s on every development fold.
- **It is thin on S1:** E012 +6,390 s, E015 about +6,456 s (implied), against a +6,500 s bound.
- It is the main live risk to promotion, and it is correctly placed before the reproduction in the chain.

**Objection T (new; Advisor objection under promotion criterion 8).**
- **The statistic:** |`per_fold[S1c].delta_rmse_full`| and |`per_fold[W1c].delta_rmse_full`| of `mechanism_check.py <H013> E012 NM_present` (chain step 1).
- **The objection stands if either reaches half the twin margin** (full precision governs): S1c ≥ 21.153 s, or W1c ≥ 47.966 s.
- **Consequence while it stands:** the same as the proposal's own rule for an inadmissible development fold in clause 4.
  - H013 is not promotable on Day 2 without a new, separately reviewed matched M2 ablation.
  - The conditional reproduction is not run.
  - H013's decision is then INCONCLUSIVE (not falsified, not promotable), unless a clause is met on other grounds.
- **Otherwise** the twins are covered, and the objection is resolved.

**Admissibility thresholds** (reading 3). The registered definition governs: "≥ ½ |margin|" at the full precision of the committed JSONs. The proposal's table rounds to one decimal, and the values below are rounded to three.

| Clause | R1 | R2 | R3 | S1 | W1 |
|---|---|---|---|---|---|
| 3: ½ \|E012 − E013\| on `LIRF_NM_missing` (s) | 544.320 | 157.101 | 1,246.470 | 988.123 | 1,237.579 |
| 4: ½ \|E012 − E014\| on `NM_present` (s) | 16.585 | 18.318 | 29.549 | 21.926 | 41.882 |

The table's R3 value for clause 4 (29.6) is 0.05 s above the definition. Where they disagree, the definition applies.

## Leakage Review

### Target Leakage

PASS

- The inputs are FS1, unchanged, and there are no target statistics.
- Bins, category vocabularies and the rare-level collapse come from the fold's training rows only.
- Binning from all rows adds no rows beyond `x_tr`. Validation rows never enter bin construction, and prediction uses the trees' real-valued thresholds.

### Temporal Leakage

CONCERN

These are label notes, as for H009 v3, and they do not affect admissibility:
- `ades` is F on diversions (~0.03 % of rows);
- the takeoff hour and weekday, the `d_*` deltas and the hour-resolution schedule-delay proxy are T;
- stand is P on an assumption.

The procedure change adds no cross-row or cross-month input.

### Competition Availability

PASS

- Same as H009 v3. Unseen levels map to null or `__RARE__`.
- The SUBMIT folds (2,085,047 training rows) are below 5,000,000, so the procedure stays deterministic there.
- Determinism across machines (Days 5–7) is out of scope (ruling 6).

## Compute Review

### RAM

PASS

- The expectation is below 6 GB (E012: 4.14 GB). Subsampling never reduced the resident dataset.
- In the synthetic fold-scale check, the whole process peaked at 1.59 GB, and binning from all rows added only a transient.

### Runtime

PASS

- **H013.** E012 took 906 s, with 101–137 s on each large fold.
  - Without bagging or feature subsampling, 1.2–1.5× gives 18–23 min.
  - Binning from all rows added about 1–2 s per fit in the synthetic check.
  - This is within CLASS-M (30 min). The timeout is 45 min.
- **The chain.** H013, H014 and the conditional reproduction run sequentially, about 55–60 min in all.

### Disk

PASS

About 10 MB of predictions per run, covered by the manifest.

## Weakest Assumption

**The assumption.** The reference-side configuration shift on E013 and E014 (FS1 − `d_sched`, FS1 − anchor) is no larger than the measured candidate-side shift H013 − E012. The proposal states that this is untested.
- **The plausible direction.** The shift is probably smaller for E013, whose LIRF NM-missing predictions lack `d_sched` and are less extreme.
- **H014 − E006 is a weak proxy.** FS0 lacks the high-cardinality keys, whose bin maps change most under all-row binning.

**Second.** The premise holds on real data. The synthetic evidence at fold scale is strong, and the reproduction is the real-data test (reading 2).

## Missing Control or Ablation

- **No new run is required.** The twin coverage is closed by objection T, from a statistic that chain step 1 already produces.
- **The only way to test M2 or M3 for H013, rather than carry them over,** is a matched ablation under the deterministic configuration. The proposal already names that route for an undecidable clause 4. The same applies to clause 3.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions (all must hold before `gate.py allocate H013 v2`).**
   - (a) `research/day-02/acks/H013_ack_v2.md` is committed, with the contents required below.
   - (b) `research/STATE.md` is refreshed, with a measured header time. Its current header (20:57:38Z) predates X-D02-S01-0004.
   - (c) `scripts/compare.py`, `scripts/mechanism_check.py` and `src/prc/attribution.py` stay unchanged from `5ba9230` until clauses 1–4 and the objection T statistic are computed. Any earlier change needs a new exchange.
   - (d) `uv.lock` is `39df945c…`. `src/prc/models/gbm.py` and the `fs0`, `fs1`, `collapse_rare`, `fs1_no_dsched` and `fs1_no_anchor` bodies are unchanged, and silver is pinned.
   - (e) No other experiment runs concurrently.
2. **One primary run.**
   - `uv run python scripts/gate.py allocate H013 v2`.
   - Config: `hypothesis_id: H013`, `proposal_version: 2`, `purpose: primary`, `model: lightgbm`, `feature_set: FS1`.
   - `params` exactly: `objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 1.0`, `bagging_fraction: 1.0`, `bagging_freq: 0`, `bin_construct_sample_cnt: 5000000`, `num_threads: 4`, `num_boost_round: 1000`. No other parameter.
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
   - Then `uv run python scripts/run_experiment.py E###`.
3. **Comparisons, in the registered chain order** (completed experiments only):
   - **step 1:** `compare.py <H013> E005`, `compare.py <H013> E012`, `mechanism_check.py <H013> E012 LIRF_NM_missing`, `mechanism_check.py <H013> E012 NM_present`;
   - **step 2:** after H014 v2, per `H014_review_v2.md`;
   - **step 3:** `mechanism_check.py <H013> E013 LIRF_NM_missing`, `mechanism_check.py <H013> E014 NM_present`, `compare.py <H013> E013`, `compare.py <H013> E014`.
4. **Conditional reproduction.** Only if clauses 1–4 are not met, criterion 8's LIRF rule is resolved, and objection T does not stand:
   - one `reproduction` allocation of H013 v2, with seed 43 and everything else identical;
   - then `reproduce_check.py <repro> <H013> --champion E005`, and the per-fold prediction SHA-256 comparison of the two manifests (reading 2).
5. **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun`, logged.
6. **Not authorized:**
   - any change to features, parameters, folds, seed or clause code;
   - pinning `data_random_seed` or any other random step;
   - any search or early stopping;
   - a second reproduction;
   - scoring H outside the frozen phase-close check;
   - redefining any population, threshold or counting rule after the H013 run.

Required acknowledgement path: `research/day-02/acks/H013_ack_v2.md`.
- It must reference the proposal hash and this review's hash.
- It must adopt preconditions 1(a)–(e).
- It must record **objection T**: the statistic, the thresholds (S1c 21.153 s, W1c 47.966 s) and the consequence.
- It must record **reading 1.**
  - Clauses 3 and 4 are carry-over tests. A clause met through inadmissible folds (for clause 3, the only way it can be met) means that M3 or M2 is not re-established for H013 by reuse.
  - It blocks promotion and the reproduction, as registered.
  - It is not evidence against the mechanism. H013's decision is then INCONCLUSIVE, not REJECT, unless clause 1 or clause 2 is met.
- It must record **reading 2**: prediction identity is checked from the manifests, and a mismatch has the consequence stated in Validation Quality.
- It must record **reading 3**: the thresholds are defined at full precision.

## Revision

None required for this version.

**Non-blocking notes:**
- **Erratum to my own v1 record.** `H013_review_v1.md` describes `test_lightgbm_without_subsampling_is_seed_invariant` as fitting "1,500 training rows". It fits **300** (`synthetic(n=2000)` marks the first 300 rows as training; 1,700 are validation). `H013_ack_v1.md` repeats the figure. The conclusion is unchanged, since 300 is below the threshold as well.
- **That test's docstring** still says LightGBM "does not consume the seed" and calls it "the basis of the H013 design". This is true only below 200,000 training rows. Tests are not frozen, so the researcher may correct it.
- **Compute discipline.** Chain step 1 may already settle Day 2 promotion against H013: at least three clause 3 folds inadmissible, any clause 4 development fold inadmissible, or objection T standing. H014 then has no Day 2 decision use. Running it anyway is the researcher's call, recorded as attribution.
- INC-0003 is still `open`. Not blocking.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| The seed-43 reproduction gives byte-identical predictions on every fold | 0.95 |
| The reproduction is within 1.0 s on every development fold (criterion 6) | 0.97 |
| Passes criteria 1–3 against E005 (clause 1 not met) | 0.93 |
| Clause 2(a) not met against H014 v2 | 0.72 |
| Clause 2(b) not met against H014 v2 | 0.88 |
| Clause 3 not met (at most two development folds inadmissible) | 0.80 |
| Clause 4 not met (in practice, every development fold admissible) | 0.75 |
| Objection T does not stand | 0.86 |
| `NM_missing_LIRF.delta_rmse_bulk` against E005 ≤ +6,500 s on every development fold | 0.45 |
| H013 is promoted on Day 2 (all of the above, correlated) | about 0.20 |

Expected magnitude:

| Quantity | Expected |
|---|---|
| Development mean | 370–385 s |
| H013 − E012 on NM-present rows outside LIRF | −2 to +3 s per development fold |
| H013 − E012 on `LIRF_NM_missing` | \|Δ\| of 100–1,500 s per development fold; R2 above its 157 s threshold more likely than not |
| Against E005 (mean dRMSE) | −95 to −115 s, 7/7 WIN |
| H013 − H014 on `NM_present_excl_LIRF` | −5 to −10 s (mean) |

Primary expected failure mode:
- **Primary.** The procedure change moves the day-scale LIRF predictions well away from E012's. Either S1's LIRF NM-missing bulk trade exceeds +6,500 s (criterion 8), or at least three clause 3 folds become inadmissible. H013 then stays INCONCLUSIVE on Day 2, with its accuracy margin over E005 intact.
- **Secondary.** Row 192622644 moves S1 or S1c by more than about 21 s on NM-present rows. That makes clause 4 undecidable, or objection T stands.
