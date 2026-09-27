---
schema: advisor-review-v1
hypothesis_id: SPLITS
proposal_version: 1
proposal_sha256: 4cf31a97946c010de04856d82e041c9f3c3755697ea7d467841a31c4bd7dc022
exchange_id: X-D01-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.85
created_utc: 2026-09-27T11:23:26Z
---

# Advisor Review

## Summary Assessment

The package is careful work. The availability audit is evidence-based. Masking is correct on real data. The fold structure satisfies brief §9. The metric is plain, unclipped RMSE over the full population. The gate and freeze mechanics behave as described. I re-verified the following:

- The proposal SHA-256 matches the envelope.
- All five pinned hashes match the files on disk, as do the audit-stats hash and the silver-manifest hash.
- `silver.parquet` matches its manifest.
- `uv run pytest` passes 35/35 tests.
- No tracked file contains a configured secret value.
- Commit `866b902`, landed during this review, touched none of the freeze candidates.

Freezing is one-way. After the freeze, any change needs an incident. The bar is therefore "no known defect in the frozen files", and v1 does not meet it. I found six defects. Each fix is small:

1. **The evaluation population is not actually pinned.** The frozen boundary also leaks through non-frozen modules.
2. **The once-per-phase holdout guard can be bypassed,** and it returns per-row holdout truth.
3. **The promotion rule has no noise floor.** On this metric, a +60 s change on 0.14–0.34 % of rows moves fold RMSE by 0.75–1.62 s.
4. **No development fold validates a winter month,** although 44.3 % of scored rows are January.
5. **S1's post-validation months demonstrably expose a regime that starts in July** (the LFPG runway change).
6. **The backward/forward label cannot support the causal-only variant it exists for.**

Decision: **REVISE.**

## Scientific Validity

These checks were read-only against silver `efde4262…`. December targets were not read, with one exception: H's row count and std were recomputed once to verify the proposal table, which already publishes them.

**Verified claims**
- **Fold table.** Rows and std reproduce exactly. R1 183,950 / 560.3; R2 185,674 / 437.1; R3 162,332 / 532.0; S1 190,713 / 745.0; H 165,677 / 514.7; SUBMIT 344,841.
- **ARR rows add no off-block information.** Of 1,898,589 Jan–Nov DEP rows with a `FLIGHT_ID`, 288,918 link to an ARR row. No ARR timestamp lies within 60 s of the DEP block time. The only coincidences are in flight-plan fields (`LOBT`/`IOBT`/`EOBT_1` within 1 s in 1.2–1.4 % of pairs), at the same rate as the DEP row's own copies of those fields. ARR `AOBT_3_flt` equals DEP `AOBT_3_flt` in 100 % of pairs.
- **`AOBT_3_flt` is not a hidden copy of the target.** It lies within 1 s of the true block time in 2.0 % of rows when it is a whole minute, and in 0.5 % when it carries seconds. Those are coincidences.
- **The ranking file's anchor looks unperturbed.**
  - The whole-minute share of `AOBT_3` is unchanged (Jan 0.966 → 0.958; Jul 0.985 → 0.987).
  - `MVT − AOBT_3` quantiles are nearly identical for July. For January they shift modestly upward across the distribution, consistent with ordinary winter-to-winter variation.
  - The second-resolution share drifts at some airports (EHAM Jan 25 % → 32 %; LEBL and LFPG Jan < 0.4 % → about 3 %). Anchor error barely depends on resolution where volume matters (EHAM 347 vs 330 s RMSE), so this is not blocking.

**Weaknesses in the argument**
1. R1–R3 are analogues of Jan 2026's *temporal structure* (no gap), not of its *season*. See Validation Quality (b).
2. Audit §6.2 says `MVT_ID` "follows schedule order". A median within-day Spearman of 0.34 is only a weak association. The pooled Pearson rank-gap test (−0.008) cannot detect structure within subgroups or non-linear structure. The point is moot because identifiers are excluded, but the sentence should not be frozen as a finding.
3. Every audit target statistic includes December: quantiles, tail shares, the 384.9 s proxy RMSE and per-airport std. At distribution level this is harmless, but H is not pristine, and the protection scope must say so (R2).
4. The metric definition is sound. Plain RMSE over all DEP rows with no clipping matches the competition. Segment definitions are fine. Traffic terciles are computed per evaluation frame, so `seg_traffic` labels are not comparable across folds. This is a nit.

## Novelty Relative to Existing Research

Not applicable. This is the first exchange of the run, the journal is empty, and there is no completed or rejected work to duplicate. Proposals H001–H008, committed during this review, are outside this envelope and were not reviewed.

## Experimental Isolation

For a freeze, the isolation question is whether the frozen boundary contains everything that determines validation outcomes. It does not.

- **Split path.** Frozen `src/prc/splits.py` finds the frozen YAML through `prc.paths.SPLITS`, and `src/prc/paths.py` is not frozen. Editing `paths.py` would redirect every fold without touching a frozen file, and `gate.py check_frozen` would still pass.
- **Evaluation population.**
  - `evaluate()` scores against whatever `silver` frame its caller supplies.
  - The runner (`src/prc/worker.py`) passes manifest-verified silver, which is good. However, the manifest, `src/prc/data.py` and `scripts/build_silver.py` are not frozen, and nothing pins a per-fold population fingerprint.
  - A rebuilt, filtered or capped silver would silently change the population and its truth (DATA_POLICY §10).
  - The eval-row counts in the proposal's own table are not enforced anywhere.
- **Promotion config.** No code reads the `promotion:` block of `splits.yaml`. `promotion_check` hard-codes the folds, the seasonal fold and the tolerance as defaults that callers can override. `reproduction_tolerance_rmse_s` and `max_access_per_phase` are never used. For criteria 1–3 and 6, the frozen config is decorative.

## Validation Quality

**(a) Noise floor.** These figures use development folds only and a fixed fold-median reference; no model was involved.
- **Tail concentration.** The top 0.1 % of rows carry 51.0 % (R1), 20.3 % (R2), 44.0 % (R3) and 63.6 % (S1) of the SSE.
- **Tail-only sensitivity.** Take two predictors that differ only by +60 s on the rows with y > 3,600 s: 306 / 313 / 222 / 656 rows, or 0.14–0.34 % of each fold. Their fold RMSEs differ by 1.02 / 1.02 / 0.75 / 1.62 s.
- **The v1 rule.** It promotes on any positive margin in mean dev RMSE and counts any positive per-fold margin as a win. The most tail-dominated fold, S1, holds a veto.
- **Reproduction tolerance.** The 1.0 s tolerance has no stated rerun protocol. It is either vacuous (a deterministic same-seed rerun, e.g. `deterministic=True` in `gbm.py`) or as large as the effects it would certify.
- **Consequence.** As written, champion changes below about 1 s are indistinguishable from the way a candidate treats a few hundred implausible records.

**(b) Winter coverage.** The development validation months are Jul, Sep, Oct and Nov. January makes up 152,719 of 344,841 scored rows (44.3 %). I compared training data from Jan–Feb 2025 with those four months, excluding December.
- **Medians** are lower in winter at most airports.
- **The upper tail,** which is where RMSE is decided, is heavier. p90 rises by +253 s at EDDM, +166 s at LTFM, +98 s at LSZH, +88 s at EHAM and +66 s at LFPG. January p90 reaches 1,448 s at EDDM, 1,690 s at LFPG and 1,235 s at LSZH; February p90 reaches 2,219 s at LTFM. November comes closest but stays below every one of these.
- **Disrupted days.** I counted airport-days whose median exceeds the airport's typical daily median by more than 300 s. Of 21 such days in Jan–Nov, 12 fall in Jan–Feb; the four development validation months contain 6.
- **Consequence.** Winter-specific behaviour (de-icing, snow, low-visibility operations) cannot influence model selection except through the protected holdout. Note that the brief's own §9 example validates December as a rolling fold.

**(c) S1 post-validation months.** The researcher asked me to weigh this.

| LFPG | Jun 2025 | Jul 2025 | Aug–Nov 2025 |
|---|---|---|---|
| 27L departure share | 30.2 % | 14.2 % | 0 % |
| 09R departure share | 13.6 % | 6.7 % | 0 % |
| 27R departure share | 0.2 % | 16.1 % | 15.1–24.4 % |
| 09L departure share | 0.0 % | 1.1 % | 9.8–17.4 % |
| Median taxi-out | 895 s | 962 s | 1,012–1,015 s |

A regime that starts inside the validation month is visible to S1's training data only through Sep–Nov. Fold-local runway, stand and interaction priors will therefore look better on S1 than on any strictly causal July analogue, and S1 is the veto fold.

I accept the counterpoint: the real Jul 2026 model trains on all of H2-2025, so a July fold trained only on earlier months would be pessimistic about regimes that persist. Neither design is right. The difference between them is the quantity that needs a control.

The August embargo does real work. EHAM's July runway mix is closest to August (total-variation distance 0.063), against 0.239 for June and 0.242 for September. Stand-vocabulary effects are negligible: 0.076 % of July rows have a stand unseen in Jan–Jun.

**(d) Holdout.**
- **Phase bypass.** `holdout_accesses(phase)` counts exact matches of a phase string supplied by the caller. Any new label, such as "D01" versus "day-01", resets the limit. In the runner the phase comes from free-form experiment config.
- **Per-row truth.** `evaluate()` returns the per-row joined truth frame for H. The worker does not persist it, but any caller can use it for error analysis, which turns H into a development fold across the four phases.
- **Unguarded helpers.** `truth_frame()` and `eval_rows()` have no guard.
- **Tests.** `tests/test_evaluator.py::test_holdout_guard` scores real December truth, with random predictions and a monkeypatched ledger, on every `pytest` run. The information leaked is negligible, but the access is unlogged.
- **No ledger check.** `experiment_id` is not verified against the ledger.

## Leakage Review

### Target Leakage

CONCERN

- **Design: sound.** In validation months, masking nulls both withheld DEP columns (tested on real silver for all six folds). Visible ARR rows carry no copy of the DEP block time (verified above). `AOBT_3` is a noisy, admissible proxy, not a copy. Identifiers are excluded.
- **Enforcement: incomplete.** Model code is kept away from truth only by convention.
  - The committed runner passes only `masked_view` output to feature and model code and persists only `[MVT_ID_mvt, pred]`, which is good.
  - However, `load_silver`, `eval_rows` and `truth_frame` can be imported by any module.
  - The evaluator returns per-row holdout truth and trusts the truth frame its caller supplies.
- **Fixes.** R1 and R2 close the frozen-file part. The model-code import check is recommended below, and I will look for it at the first experiment review.

### Temporal Leakage

CONCERN

- **R1–R3 are clean.** They train strictly before validation with no gap. Later months are absent, so month ends match the ranking file.
- **S1 carries forward information.** Its forward training months expose validation-month regimes (LFPG, above). This is acceptable only with a pre-registered control (R5).
- **S1 is optimistic for recency-dependent features.** Features that rely on the freshest available targets get June 2025 data in S1, but the real Jul 2026 test gets December 2025 data (audit §6.5). From Day 3 onward I will require such features to declare their staleness sensitivity.

### Competition Availability

PASS

- **The snapshot definition is faithful.** The ranking file does give each scored row its actual takeoff and withholds only the block time and target, so no single wall-clock instant reproduces it.
- **The premise of §6.4 holds.** The ranking file's admissible columns show no sign of perturbation.
- **The label rules are not yet usable** (R6).
  - "Backward" is defined relative to the row's own takeoff. The row's taxi interval therefore counts as backward. Examples are departures on the same runway between this row's off-block and its takeoff, or the next arrival blocking in at the vacated stand. These are the most target-revealing cross-row quantities, and they are unknown at any operational prediction instant.
  - Separately, §6.2 makes Jul 2026 rows admissible for Jan 2026 predictions and vice versa. `masked_view(SUBMIT)` exposes both months together, but no development fold has two validation months, so any feature that pools the validation period behaves differently at submission than in validation.

## Compute Review

### RAM

PASS

Loading full silver, building the S1 masked view and extracting eval rows peaks at 2.2 GB RSS. That is slightly above the proposal's "< 2 GB" (a nit) and well within CLASS-S.

### Runtime

PASS

Load, view and eval rows take 1.0 s. The full test suite takes 4.8 s.

### Disk

PASS

The freeze creates no new data. Silver is 233 MB.

## Weakest Assumption

The design assumes that selecting models on R1–R3 plus S1 ranks candidates the way the Jan/Jul 2026 test would. It fails in two directions:
- Winter tails, which matter for 44.3 % of scored rows, are absent from every development validation month.
- S1 lets post-validation months inform the validation month's operational regime.

Independently, the promotion rule treats RMSE differences smaller than the tail-driven variation (about 1 s) as real.

## Missing Control or Ablation

1. **A noise control for promotion.** It must apply both to the mean and to each per-fold win, because S1 holds a veto.
2. **A control that isolates S1 gains coming from post-validation training months.**
3. **A winter validation signal inside model selection,** or an explicit, pre-registered decision use of H.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE confers no authority.
- Do not run `scripts/gate.py freeze` against v1.
- No `E###` can be allocated, because the gate refuses allocation until `config/frozen.json` exists.
- Resubmit as `research/day-01/proposals/SPLITS_v2.md` in a new exchange, with every changed file's hash re-pinned.

Required acknowledgement path: `research/day-01/acks/SPLITS_ack_v1.md`. It acknowledges this REVISE, references the proposal hash and this review's hash, and confers no authority.

## Revision

Required. All six must be addressed in SPLITS_v2. The mechanism is the researcher's choice in every case.

- **R1. Pin the evaluation population and close the frozen boundary.**
  - Make each fold's evaluation population verifiable from the frozen artifacts, for example by frozen per-fold row counts plus a content fingerprint of (`MVT_ID_mvt`, target) that `evaluate()` checks before scoring. Letting the evaluator load and verify silver itself would be an alternative.
  - Frozen modules must not depend on non-frozen modules to decide which config or data they read (`src/prc/paths.py`, and `src/prc/data.py` if the evaluator uses it). Either freeze those modules or remove the dependency.
- **R2. Make the holdout guard real and state its scope.**
  1. The once-per-phase limit must not depend on a free-form caller string, and the enforced limit must be the frozen `max_access_per_phase`.
  2. An access to fold H must not hand per-row truth to the caller. Alternatively, v2 must justify per-row holdout error analysis given that H is re-used in later phases.
  3. State the protection scope honestly. The Day 1 audit already read December's target distribution. From the freeze onward, no EDA, audit or test may read December targets outside a logged access, and that includes `test_holdout_guard`.
- **R3. Pre-register a noise-aware promotion rule and make it binding.**
  1. Criteria 1–2 must require an improvement that exceeds a pre-registered noise floor or passes a pre-registered paired test. It must apply to the mean and to each per-fold win. The method and threshold are yours, but they must be fixed before any baseline is scored.
  2. Specify the brief §10 item-6 rerun protocol: the seed policy, which quantity must reproduce within 1.0 s, and whether criteria 1–3 must also hold on the rerun.
  3. `promotion_check` must take its parameters from the frozen config, with no overridable folds, seasonal fold or tolerance.
- **R4. Address winter in model selection.** Do one of the following, and justify the choice with training-data evidence (not December):
  - add winter coverage to the development folds;
  - re-assign roles among the months;
  - keep the current design and pre-register what an H result at phase close does, i.e. when it blocks or reverses a promotion.
- **R5. Control S1's forward exposure.**
  - Record the LFPG evidence in DATASET_AUDIT §6.5.
  - Pre-register a control that isolates S1 improvements coming from post-validation months. It must at least cover hypotheses built on fold-local priors or regime-sensitive keys (runway, stand, operator, airport × time).
  - The form is yours: a non-promotion diagnostic fold or a mandatory ablation rule. A diagnostic fold must be frozen now, though, or adding it later will need an incident.
- **R6. Make the availability labels usable** (DATASET_AUDIT §6.2).
  1. State the reference instant of backward/forward explicitly. Then either add a label for events inside the row's own taxi interval, or define an operational reference instant, so that the causal-only variant is actually definable.
  2. State whether information from the other ranking month (Jan ↔ Jul 2026) is admissible. If it is, require it to be labelled, because no development fold can validate it.

Recommended (non-blocking):
- **Import check.** Add a test that forbids `prc.data`, `eval_rows` and `truth_frame` imports in `src/prc/features.py` and `src/prc/models/`.
- **Gate hash.** Record the hash of `scripts/gate.py` in each allocation record.
- **Holdout ID.** Verify the holdout `experiment_id` against the ledger.
- **Covariate comparison.** Add a target-free ranking-vs-training comparison of admissible columns (resolution, missingness, `MVT − AOBT_3` quantiles by airport-month) to the audit.
- **LIRF diagnostic.** Report per-airport RMSE on rows with y < 3,600 s as a diagnostic. LIRF's tail (std 1,332 s) makes the +3 % airport rule insensitive to degradation in the bulk.
- **Identifier wording.** State that identifiers may serve as join keys but not as model inputs.
- **Nits.**
  - It is `AOBT_3`, not `BLOCK − AOBT_3`, that is whole-minute in 97.7 % of rows.
  - The claim that `MVT_ID` "follows schedule order" is overstated (see above).
  - The proposal's `created_utc` (11:07:30Z) is later than the envelope's (11:07:28Z), yet the envelope pins the proposal's hash.
  - Peak RAM is about 2.2 GB.

## Advisor Prediction

Probability of improvement: Not applicable, because no model experiment is proposed. I estimate P = 0.75 that a v2 addressing R1–R6 without new defects is accepted on first resubmission.

Expected magnitude: No direct effect on RMSE. If v1 were frozen as written, I would expect at least one Day 1–4 promotion to be decided by a mean dev-RMSE margin below 1 s, which is the size of a tail-only +60 s change. I would also expect S1 to cause most promotion vetoes.

Primary expected failure mode: Selection on autumn folds, plus a July fold that sees post-July regimes, rewards same-year regime memorisation and autumn-typical tails. The resulting dev-fold gains then fail to transfer to January 2026, the winter half of the score (44.3 % of rows), where the upper tail at de-icing airports is heaviest.
