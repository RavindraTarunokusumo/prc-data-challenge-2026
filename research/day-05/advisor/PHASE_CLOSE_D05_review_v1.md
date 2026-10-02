---
schema: advisor-review-v1
hypothesis_id: PHASE_CLOSE_D05
proposal_version: 1
proposal_sha256: ca9fff72ecc60effd757e1df132ae606cf6dfdbca3a29043bf1829073041ee00
exchange_id: X-D05-S05-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.88
created_utc: 2026-10-02T13:09:41Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.88).**
- **The Day 5 decisions stand under the frozen rules:**
  - H023 v3 (E033) meets criteria 1–8 against E019 (instance E026). It is promoted subject to the Day 5 holdout access.
  - H021 v3 (E031): clause 1 not met (mechanism supported), final with E032. Not a candidate.
  - H022 v3 (E030): control, integrity holds.
- **The holdout access is authorized exactly as requested:**
  - one access, E033 (NEW) against E026 (reference; rule L v2 item 5), under the frozen `phase_close` rule (`revert_on: LOSS`);
  - the revert is mechanical, with no substitute comparison;
  - the H figures are recorded only (ruling H5 below).
- **Champion change.** On WIN or TIE, E033 becomes champion and E019 becomes previous, with the disclosures named in Execution Authorization item 3.
- **Corrections.** The acknowledgement appends nine record corrections, D5-C8 to D5-C16, before `DAY_SUMMARY.md` is finalised. None changes a decision. Three change what Day 5 is recorded as having shown:
  - D5-C8: where the margin comes from;
  - D5-C11: CatBoost alone's S1 WIN is one row;
  - D5-C12: attribution statements.
- **Incidents:**
  - INC-0006 may close;
  - INC-0009, INC-0010 and INC-0004 stay open;
  - INC-0007 gets an appended pointer to INC-0010.
- **Standing review rule 13 is added** (disclosure only; Revision).

**Attack on the candidate.** As policy requires, I tried to show that E033 should not be champion. The record's forecasts were wrong in the candidate's favour by a wide margin: the H023 v3 review gave promotion P 0.04. I therefore audited E031 and E033 for any path that could produce a spurious validation gain. I found none.

What the attack did find:
1. **The margin has two sources** (D5-C8).
   - −2.04 s is E029's D3-C2 treatment. That is E023's Day 4 margin, which could not be promoted on its own.
   - −3.58 s is the CatBoost half.
   - S1's WIN is entirely the CatBoost half: +0.20 s, then −4.38 s.
2. **Neither S1 nor criterion 2 depends on a single row** (D5-C10). Without row 192622644, S1 is still −3.76 s. W1's WIN draws 0.29 of its change from row 183910286, but criterion 2 does not need W1.
3. **CatBoost alone would have been single-row carried on S1** (top-1 share 0.62; D5-C11). The blend's gain over E029 is diffuse (top-10 ≤ 0.37). The robust Day 5 effect is the complementarity, not "CatBoost beats LightGBM".
4. **The champion is stochastic** (D5-C9).
   - One GPU re-draw moved CatBoost alone beyond the 1.0 s tolerance on R1.
   - It moved the blend by up to 0.48 s, and flipped clause 1's W1 reading from WIN to TIE.
   - The margins (at least 3.59 s per development fold, and at least 3.79 s on the re-draw) are 7–20 times that spread.

**Verified here.** Every check was read-only.
- **Constraints kept.**
  - The experiment lock was free (last holder E034, finished).
  - No truth was loaded on any fold, development or holdout. No December target was read, and `holdout_check.py` was not run.
  - No model was fitted, and no fold was scored.
  - Scripts and outputs stayed in the session scratchpad. Peak RSS of the largest check was 0.71 GB.
  - The tree was clean before and after.
- **Hashes:**
  - the proposal matches the envelope (`ca9fff72…`);
  - the six frozen files match `config/frozen.json`;
  - `.claude/agents/advisor.md` is `30fff5dd…`, as in `config/agents.yaml`; `scripts/gate.py` is `28e0977c…`, as in every Day 5 gate record;
  - for E030–E034, the proposal, review and ack hashes match their gate records;
  - the X-D05-S04-0001, -0002 and -0003 mirrors verify.
- **Predictions:**
  - all 72 prediction files of E026–E034 match their manifests, and E026 ≡ E027 byte for byte;
  - **E033 = ½ E029 + ½ E031 and E034 = ½ E029 + ½ E032 exactly** (max |Δ| = 0) on all 8 folds, H included;
  - **E026, E029 and E033 are identical on every routed row of every fold** (max |Δ| = 0; 88 rows on H);
  - E026's and E033's H artifacts resolve under the evaluator's path lookup, with 165,677 rows each (the frozen H count).
- **Freeze and environment:**
  - `git diff 803ceeb <run commit>` over `src`, `scripts`, `config`, `pyproject.toml` and `uv.lock` is empty for E030–E034;
  - their manifests all record CPython 3.13.15, 16 polars threads, lock `efa4fd78…`, no thread variables and identical library versions;
  - every one records 0 pages swapped out.
- **Leakage path audit of E031 and E033** (Scientific Validity (c)): it is clean.
- **Tests:** 62 synthetic tests pass (isolation, models, worker, promotion). The suite collects 158 tests, and `ruff` is clean.
- **Task ledger:** no `day-05` `holdout_access` event, and no holdout-unmasking event.
- **Secrets:**
  - No credential value appears in any tracked file. `.env.example` holds names only.
  - `.env`, `runtime/wandb/` and `predictions/validation/` are git-ignored.
  - The only 40-hex strings in prose files are commit hashes.

## Scientific Validity

### (a) The Day 5 decisions re-verify

All figures below are read from committed records or computed target-free.

| Decision | Check | Result |
|---|---|---|
| E033 criteria 1–3 against E026 | `E033_vs_E026.json`: mean −5.618 (q95 −4.787); all 7 folds WIN; the nearest deciding quantile is W1's q90 (−1.98); every airport improves (LIRF worst, ratio 0.9974) | Confirmed |
| Criterion 4 (B2; H018 v2 clauses 1–2) | Clause 1: −3.96 (q95 −3.52), 7/7 WIN. Clause 2: −3.58. Noise \|m\|/2 = 0.34 ≤ 0.5. > 3 h band 3 (limit 50). `NM_missing_other` bulk −317.3, −296.3, −181.4 and −165.9 s on R1, R2, R3 and W1 | Confirmed |
| Criterion 6 | E034 − E033: +0.478, −0.248, +0.093, +0.272 and −0.204 s. E034 against E026 is WIN on 7/7 | Confirmed |
| Criterion 7 | E031: 1,522.9 s and 7.01 GB. E032: 1,130.5 s and 7.08 GB (CLASS-L, and inside CLASS-M's figures). E029 CLASS-M. E033 and E034 CLASS-S. No swap | Confirmed |
| Criterion 8 | `NM_missing_LIRF` bulk against E028: at most +0.06 s (bound +6,500). B3: S1c −6.39 (no objection) | Confirmed |
| Rules 1, 6, 12 | S1 `NM_present_LIRF` share 0.237. Top-1 shares: S1 0.136, W1 0.288. Bands 82 / 4 / 3 | Confirmed |
| Route integrity | E030–E034 against E029: 0.0 on all 8 folds | Confirmed (re-derived from prediction files) |
| H021 clause 1 final | −4.91 (q95 −4.28), 5/5 counted WINs. m = +0.683 | Confirmed |
| Comparability (H022 v3 closed set) | `resolved_params_E031_vs_E030.json`: all 8 folds, nothing outside the set | Confirmed |
| Consistency | The S1 blend RMSE implies an uncentred error correlation of 0.9854, which matches the recorded 0.9854 | Consistent |

### (b) The margin claim on E033's own comparison ("Case against" 1)

**E033 against E019 itself,** from E019's cloud `metrics.json` (point estimates):

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| E033 − E019 | −6.514 | −9.610 | −4.212 | −4.179 | −3.585 | −6.389 | −6.816 |
| E033 − E026 | −6.514 | −9.609 | −4.208 | −4.172 | −3.586 | −6.389 | −6.816 |

- **The development mean is −5.620 against −5.618.** The largest per-fold difference is 0.0072 s (S1).
- **The routed rows contribute exactly 0 to E033 − E026:**
  - the `NM_missing_LIRF` cell is 0.0 on every fold;
  - the predictions are bit-identical.
- **E026 ≡ E019 at the nine non-LIRF airports:** their by-airport RMSEs are equal to full float precision (S1 checked; D5-C3).
- **E029 − E026 reproduces E023 − E019 to 1e-4 s** on every fold.
- **What remains unverified.** The bootstrap quantiles against E019's own files cannot be computed, because those files are absent. No deciding quantile is within 1.98 s of 0, against an instance shift of at most 0.0072 s.
- **The claim is confirmed.**

### (c) Why the result beat every forecast: the extra scrutiny ("Case against" 8)

Every path by which a validation target could reach a learner, or a learner could be tuned on validation data, was checked:

1. **The frozen `masked_view`** nulls `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt` on validation DEP rows. Other months are absent, so embargo months cannot leak.
   - Both components see validation `y` as null.
   - The CatBoost vocabulary is built from training rows only.
2. **CatBoost is fitted on a training `Pool` only.** No `eval_set` is passed. E031's resolved parameters confirm:
   - `use_best_model: False` and `od_type: None`, with a fixed 1,000 iterations;
   - `counter_calc_method: SkipTest`, so no validation data enters a CTR counter;
   - `has_time: False`.
   - Any defect in the training-side CTR estimates could only hurt validation; it cannot create a validation gain.
3. **Curves cannot feed back into the model.** Staged predictions are computed after `pred`. H has no `eval_rmse` in any `curves.json` (E027, E029–E032).
4. **No real-target CatBoost result existed before the blend was registered.**
   - The GPU calibration permuted the training target and computed no metric. That includes the `h021_exact` and `h022_exact` timing rows.
   - H023 v3 was written at 20:24:25Z and ACCEPTed at 20:38:04Z, before E030 (20:39:11Z) and E031 (20:44:22Z) were allocated.
   - The weights are 0.5 / 0.5 as registered. The primary used E031, not the re-draw.
   - The re-draw blend is the slightly worse one (438.95 against 438.87), so nothing was cherry-picked.
5. **The blend is exactly the registered arithmetic:** it is a manifest-verified join on validation ids with a null check (verified bitwise).
6. **The tools freeze and the environment binding hold** for every chain run.

**Where the forecasts went wrong.**
- The H021–H023 reviews (and the researcher) assumed this CatBoost would be 3–14 s worse than E029 on normal taxis (central +7). That assumption was carried over from the H020 reasoning, and it was wrong in sign.
- Given the realised inputs, the blend arithmetic was right. With E031 −1.69 s against E029 and a bulk residual correlation of 0.84–0.92, a −3.6 s blend gain is what the variance-reduction formula gives.
- The surprise is the component, not the blend (D5-C13).

### (d) Where the champion's margin comes from (D5-C8)

E033 − E026 = (E029 − E026) + (E033 − E029), exactly at the level of fold point estimates:

| Fold | R1 | R2 | R3 | S1 | W1 | Dev mean |
|---|---|---|---|---|---|---|
| E029 − E026 (H018 v2's D3-C2 treatment) | −3.00 | −4.80 | −1.30 | **+0.20** | −1.28 | −2.04 |
| E033 − E029 (the CatBoost half) | −3.51 | −4.81 | −2.91 | **−4.38** | −2.31 | −3.58 |
| `NM_missing_other` share of E033 − E026's SSE change | 0.68 | 0.52 | 0.46 | 0.27 | 0.32 | — |

- **36 % of the margin over E019 is E023's Day 4 treatment,** which could not be promoted on its own (S1 TIE).
- **The S1 WIN is entirely the CatBoost half.**
- **This is not a re-adjudication of E023** (rule 10). The S1 outcome that decided Day 4 is now decided by a new mechanism, and B2 required that mechanism to be supported (clause 1 not met).

### (e) Single rows ("Case against" 4; D5-C10, D5-C11)

The table is audit arithmetic on recorded figures only:
- RMSEs from `metrics.json`;
- row counts from `config/splits.yaml`;
- y values as recorded in the E033 analysis;
- stored predictions.

The method reproduces the Day 4 audit's E023 − E019 figures exactly (S1 −0.540, W1 −0.498 without the row). Point estimates only: the bootstrap needs truth, which this exchange does not read.

| Contrast | Fold | With the row | Without the row | Row's share of the SSE change |
|---|---|---|---|---|
| E033 − E026 | S1 (192622644) | −4.17 | **−3.76** | 0.136 |
| E034 − E026 | S1 | −3.90 | −3.73 | 0.084 |
| E033 − E026 | W1 (183910286) | −3.59 | **−2.56** | 0.288 |
| E034 − E026 | W1 | −3.79 | −2.75 | 0.275 |
| E031 − E029 (CatBoost alone) | S1 | −4.14 | **−1.66** | **0.616** |
| E032 − E029 | S1 | −3.50 | −1.47 | 0.596 |

- **S1 is not single-row decided for E033.** D4-C9's constraint did not bind, as the proposal says, and the margin survives the row's removal.
- **W1.** About a third of the W1 advantage is one row. The q90 without the row is not computed here. Criterion 2 is met without W1: R1, R2, R3 and S1 are counted WINs.
- **The W1 row's large prediction rests on post-validation training months.**
  - In W1, with Apr–Nov in training, E031 predicts 22,233 s and the blend 15,086 s (y 13,865 s).
  - In the causal twin W1c, E033 predicts 3,764 s against E026's 4,889 s, so it is further from y.
  - W1c is nevertheless a WIN (−6.82 s, top-1 share 0.04).
  - The twin rule therefore does its job, and the counted W1 WIN is valid. This is the inherited temporal concern made concrete.
- **CatBoost alone against the LightGBM is row-carried.**
  - Its S1 WIN over E029 is 62 % one row (rule 6), and its R1–R3 top-10 shares are 0.64, 0.81 and 0.56.
  - The blend's gain over E029 is diffuse: top-10 shares are at most 0.37 on every fold.

### (f) The stochastic champion ("Case against" 2; D5-C9)

| Re-draw quantity (seed 42 → 43, GPU) | R1 | R2 | R3 | S1 | W1 | S1c | W1c | H |
|---|---|---|---|---|---|---|---|---|
| CatBoost alone, all rows ΔRMSE (s) | +1.06 | −0.39 | +0.14 | +0.65 | −0.73 | +0.36 | −4.19 | — |
| CatBoost alone, `NM_present_excl_LIRF` (s) | +0.65 | −0.05 | −0.07 | +0.13 | **+2.77** | −0.87 | −0.72 | — |
| Blend, all rows ΔRMSE (s) | +0.48 | −0.25 | +0.09 | +0.27 | −0.20 | +0.14 | −1.28 | — |
| RMS prediction change, non-routed rows, CatBoost (s) | 42.5 | 34.9 | 30.5 | 39.6 | 38.0 | 46.7 | 73.3 | 30.1 |
| RMS prediction change, non-routed rows, blend (s) | 21.2 | 17.5 | 15.3 | 19.8 | 19.0 | 23.3 | 36.6 | 15.0 |

**Criterion 6 is satisfied as frozen:** one reproduction, seed + 1, and the 1.0 s tolerance. A second draw is not required, and rule 10 forbids re-reading it.

**The answer to the question asked is a disclosure, not a new test:**
- the evaluated figures (development and H) are one draw;
- clause 1's W1 reading is draw-sensitive: WIN at −1.59 s, then TIE at −0.31 s;
- the SUBMIT predictions will be a further draw, not reproducible bit for bit.

**The decision is robust to the draw.** Both draws are 7/7 WIN against E026. The smallest margin is 3.59 s, against at most 0.48 s of re-draw movement. Standing rule 13 makes this disclosure routine for later candidates.

### (g) The blend against CatBoost alone ("Case against" 3)

**The record should say so, in these terms:**
- **CatBoost alone was never a candidate.** E033 against E031 is not a pre-registered or bootstrapped comparison.
- **By point estimate, the blend is lower on every development fold:**
  - R1 −1.99, R2 −2.69, R3 −1.77, S1 −0.23, W1 −2.77 s;
  - its re-draw spread is about half CatBoost's;
  - CatBoost alone's S1 advantage is 62 % one row (D5-C11).
- **No claim is made that 0.5 / 0.5 is the best combination.**
- **Any Day 6–7 alternative** (CatBoost alone, another weight, another component) is a new configuration. Its weight or selection is chosen with development results in view, so its proposal must state that selection hazard (H023 v3 authorization item 6; INC-0009 addendum).

### (h) Forward risk and budget ("Case against" 5, 6)

**D3-C3 is restated for E033** (D5-C16).
- On development folds, the share of `NM_missing_other` bulk rows with `d_sched` > 3 h that are out of range is:
  - 3 of 528 (0.57 %) for E033;
  - 81 of 528 (15.3 %) for E019.
- Applied naively to January 2026's 435 such rows, that is about 2–3 rows against about 65.
- The count fact stands, and H does not test it. The expected exposure is much reduced, but not measured.

**Bulk out-of-range counts by rule 7 subgroup** (5 development folds):

| Subgroup and count | E019 | E033 |
|---|---|---|
| `NM_present_LIRF`, > 3,600 s | 34 | 19 |
| `NM_missing_other`, < 0 s | 142 | 80 |
| `NM_missing_other`, > 3,600 s | 44 | 9 |
| `NM_present_other`, > 3,600 s | 82 | 85 |
| `NM_present_other`, < 0 s | 8 | 0 |

- The CatBoost half's higher day-scale predictions do not appear as false out-of-range predictions on normal rows.
- Its January effect on genuine day-scale LIRF records can cut either way, as the proposal says.

**Budget.**
- CatBoost was still improving at 1,000 iterations, so the champion is "at this budget".
- A Day 6–7 change of iterations is a new configuration.
- Choosing it from the E031 curves would be validation-guided tuning (INC-0009 addendum). It must be pre-registered as such.

### (i) Process ("Case against" 7): did a slip touch a decision quantity?

**No.** Each slip, checked:

| Slip | Effect on a decision quantity |
|---|---|
| D5-C1 (swap) | None. Boot-wide `pswpin`/`pswpout` were 0 through E029, and each of E030–E034 recorded 0 pages |
| D5-C2 (interpreter) | None for the decisions. Every chain run is in one environment (item 6, verified per manifest), and the instances reproduce the cloud outcomes |
| D5-C3 (attribution) | Records only |
| D5-C4 (E028's ridge path) | Criterion 8 only: at most +0.06 s against +6,500 |
| D5-C5 (scope of E027–E029) | Ratified. E029's files are manifest-verified |
| D5-C6 (E029's manifest commit) | None. `f89dc60..ed5151f` changes only `catboost()`, the v1 blend tooling, the worker's dispatch hook and the runner's GPU polling; the LightGBM path is unchanged |
| D5-C7 (calibration row) | VRAM planning only |
| INC-0008 (E025's OOM) | E025 is recorded as RESOURCE_FAILURE, and E026 is the reproduction |
| Hand-written timestamps | Records only |

**Two further clerical slips found here** (D5-C14, D5-C15):
- the ledger decisions are empty for E026–E034;
- E033's rule 12 call omitted the E029 and E026 arguments of its Validation Plan.

Neither touches a decision quantity.

### (j) What H can and cannot test (proposal item 2)

**The proposal's list is right.** Two additions belong in the record:
1. **H is a joint test.** E033 − E026 on December combines E029's D3-C2 treatment and the CatBoost half. Its outcome cannot be attributed to either.
   - On H, target-free, the two files differ by:
     - RMS 544 s on the 1,561 `NM_missing_other` rows (mean |Δ| 185 s);
     - RMS 45 s on the 152,048 `NM_present_other` rows;
     - RMS 69 s on the 11,980 `NM_present_LIRF` rows.
   - So H exercises both mechanisms, as R1 and R2 do.
2. **H tests one draw** (E031's H fit).
3. **The routed `NM_missing_LIRF` subgroup is excluded by construction:** the 88 routed rows are bit-identical in both files.

## Novelty Relative to Existing Research

- **Day 5 adds the project's first second-family learner and its first ensemble.** H021's CTR mechanism is new against H020 v1's rejection: a mean CTR, raw levels, full combinations and a matched codes control.
- **The blend is not a re-adjudication of E023** (rule 10; (d)). E029 is ratified as its LightGBM component (LAPTOP_REFS v2).
- **Nothing in the chain repeats closed work.**

## Experimental Isolation

- **H023 − E029 = ½ (H021 − E029) exactly.** It was verified bitwise at the prediction level.
- **The attribution is scoped to "this CatBoost configuration".** The control that would attribute it to categorical handling, the E029 + H022 blend, is named and was not run.
- **H021's clause 1 (E031 against E030) isolates the categorical statistics within CatBoost at fixed capacity.** The pair is matched under the closed set.
- **Nothing isolates "CatBoost beats LightGBM"** (D5-C12 (a)).

## Validation Quality

**The development evidence is complete under the frozen procedure:**
- the frozen folds and twins;
- the cluster bootstrap;
- criteria 1–8 with B2, B3, H018 v2's clauses 1–2 and rule L v2 item 4's flags;
- a reproduction with both route checks.

**The holdout design is correct:**
- E033 is a `day-05` gate allocation and a primary (rule 9);
- E026's H file is the reference that rule L v2 item 5 names;
- there are no `day-05` accesses yet, against a limit of 1;
- both experiments are COMPLETE in `experiments/ledger.jsonl`;
- `holdout_compare` takes the phase from E033's gate record (`day-05`);
- the revert rule is frozen (`revert_on: LOSS`; WIN or TIE stands).

**Ruling H5 (recorded with this exchange):**
- the Day 5 access is E033 against E026;
- the H figures are recorded only and inform no Day 6–7 choice (as H3);
- the outcome is a joint test of both mechanisms on one draw, with the routed subgroup excluded by construction;
- no substitute comparison follows any outcome, and an unused or failed access does not carry over (H4).

## Leakage Review

### Target Leakage

PASS
- No new input. The weights are fixed a priori.
- The components are fold-local, and validation `y` is null.
- CatBoost has no eval set, and its counters use `SkipTest`.
- The blend reads only manifest-verified prediction files.
- The calibrations used permuted targets and computed no metric.

### Temporal Leakage

CONCERN

Inherited, not blocking:
- FS2's T features in both components (frozen availability definition, as disclosed in H015 v2);
- post-validation months in S1's and W1's training, for both trees and CTRs.

Row 183910286 shows the second concretely ((e)). The twins bound it: S1c −6.39 and W1c −6.82, both WIN against E026.

### Competition Availability

PASS
- **Both components can predict SUBMIT_JAN and SUBMIT_JUL.**
- **Unseen 2026 raw levels are rare:** at most 0.43 % of rows (July op_prefix; `unseen_levels_2026.json`). They map to a level absent from training, so CatBoost uses its prior.
- **The SUBMIT path for a composite champion does not exist yet.** It needs two component final runs and a blend run, and the CatBoost half will be a fresh draw. Day 7 must pre-register it. This is non-blocking for the promotion.

## Compute Review

### RAM

PASS

E031 7.01 GB and E032 7.08 GB (CLASS-L, 11 GB; also inside CLASS-M's 8 GB). The access itself is light.

### Runtime

PASS

E031 25.4 min and E032 18.8 min (CLASS-L, 90 min). The access takes seconds.

### Disk

PASS

The access writes one JSON file.

## Weakest Assumption

**That the evaluated champion is the one Day 7 will submit.**
- The development and H figures come from one GPU draw, in one laptop environment. The submission will be a fresh draw, trained on 12 months, through a composite SUBMIT procedure that does not yet exist.
- **The draw part is well bounded:** two draws, both 7/7 WIN, with margins at least 7 times the re-draw spread.
- **The procedural part is untested.**

## Missing Control or Ablation

- **The E029 + H022 equal-weight blend.** It is required only to attribute the complementarity to categorical handling. The claim is scoped, so it is not required.
- **A W1 bootstrap without row 183910286.** It was not computed: this exchange reads no truth. It is not required, because criterion 2 is met without W1.
- **E033 against E031 under the criteria.** It was not pre-registered, and it is not required for promotion ((g)).

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **The Day 5 decisions stand as recorded.**
   - H023 v3 is not falsified: clauses 1–2 are not met, and criteria 1–8 hold against E026, with B2, B3 and H018 v2's clauses 1–2.
   - **Criterion 8:** this review raises no unresolved objection. Its findings are resolved by disclosure (item 3).
   - **E033 is the phase-closing champion, subject to item 2.**
   - E031 (H021 v3): clause 1 not met, final; not a candidate. E030 (H022 v3): control. E032 is H021's reproduction; E034 is H023's passing reproduction.
2. **Exactly one protected-holdout access,** under these conditions:
   - the acknowledgement below is committed first;
   - the tree is clean;
   - `runtime/experiment.lock` is free;
   - there is no `day-05` `holdout_access` line in the task ledger;
   - rule L v2 item 6's environment is unchanged.

   ```
   uv run python scripts/holdout_check.py E033 E026 --reason "Day 5 phase close (X-D05-S05-0001): phase-closing champion E033 (H023 v3) vs phase-opening champion E019, laptop instance E026 (rule L v2 item 5)"
   ```

   **Outcomes:**
   - **WIN or TIE:** E033 is champion. H023 v3 is PROMOTE, and E034 is PROMOTE as its reproduction (as E022).
   - **LOSS:** revert. E019 stays champion. H023 v3 (E033, E034) is recorded INCONCLUSIVE ("phase-close holdout LOSS, frozen revert"). No substitute comparison follows.

   **Failure handling:**
   - If the command exits before a `day-05` `holdout_access` line is appended, no access occurred. Record the cause; the identical command may then be issued once more.
   - If the line was appended and no result file was written, stop. There is no re-run; a recovery review decides.

   **Records:**
   - Commit `research/day-05/holdout/holdout_E033_vs_E026.json` and the task-ledger line.
   - Record E026's H RMSE beside E019's recorded 375.9272 s (`holdout_E019_vs_E005.json`), as the instance check on H. This is disclosure only; it changes nothing.
3. **Champion change (WIN or TIE only):**
   - **`models/champion/CURRENT.json`:** a new record, keeping the previous content as history.
     - Champion E033 (H023 v3); previous E019.
     - Components [E029, E031] at [0.5, 0.5].
     - Reproduction E034 (within 0.48 s; not byte-identical: a GPU re-draw).
     - Bound to rule L v2 item 6's environment (INC-0010).
   - **A `champion_change` event** in the task ledger.
   - **Standing disclosures on E033:**
     - D3-C1, as lineage;
     - D3-C3, restated by D5-C16;
     - D5-C8 (margin composition);
     - D5-C9 (stochastic champion);
     - D5-C10 (single rows);
     - the 1,000-iteration budget ((h)).
   - **D3-C2 is retired as a defect of the champion** (treated: > 3 h band 3 against 81), and kept as history.
   - **D4-C9 is superseded for E033 by D5-C10.**
4. **Not authorized:**
   - any other H comparison, including E034 or any of E026–E032 as NEW;
   - any use of the H figures except recording the outcome and the instance check (H5);
   - any further allocation, run or fit in Day 5;
   - E031 alone, any other weight or any other component as a candidate without a new proposal;
   - any change to frozen files, reviews or completed records (corrections are appended).

Required acknowledgement path: `research/day-05/acks/PHASE_CLOSE_D05_ack_v1.md`

**Contents of the acknowledgement:**
- the proposal hash (`ca9fff72…`) and this review's hash;
- corrections D5-C8 to D5-C16 below, appended;
- standing rule 13 and ruling H5, recorded;
- the command in item 2.

**Corrections** (appended; the proposal and completed records are not edited). Figures are in Scientific Validity.

- **D5-C8. Composition of the margin** (DAY_SUMMARY §1, §5; E033 analysis; STATE). Record (d) beside the −5.62 s:
  - −2.04 s is E029's D3-C2 treatment (E023's Day 4 margin);
  - −3.58 s is the CatBoost half;
  - S1 is +0.20 s and −4.38 s respectively;
  - the `NM_missing_other` share of the change is 0.27–0.68.
- **D5-C9. Stochastic champion** (DAY_SUMMARY §5, §9.2). Record (f):
  - the figures are one draw;
  - the blend's re-draw is at most 0.48 s per development fold, with an RMS prediction change of 15–23 s (37 s on W1c);
  - clause 1's W1 reading moves from WIN to TIE;
  - the SUBMIT predictions are a further draw.
- **D5-C10. Single rows** (E033 analysis; DAY_SUMMARY §1):
  - S1 is −3.76 s without row 192622644;
  - W1 is −2.56 s without row 183910286 (q90 not computed; W1 not needed for criterion 2);
  - the W1 row's prediction depends on post-validation months (W1c reverses it).
- **D5-C11. CatBoost alone is single-row carried on S1** (rule 6; E031 analysis; DAY_SUMMARY §1, finding 2).
  - E031 − E029 on S1 has a top-1 share of 0.616: −4.14 s with the row, −1.66 s without it (E032: 0.596).
  - The R1–R3 top-10 shares are 0.64, 0.81 and 0.56.
  - The E031 analysis omits the rule 6 figure.
  - Finding 2 must read: "−1.69 s on all rows (q95 −0.74), W1 TIE; its S1 WIN is 62 % one row; the diffuse effect is the blend's".
- **D5-C12. Attribution and scope** (DAY_SUMMARY; rule 11):
  - (a) §1, "Its categorical statistics are the reason": the −4.91 s is E031 against E030 on `NM_present_excl_LIRF`. It does not attribute E031's all-rows advantage over E029, which is a different contrast and population. Scope it to "within CatBoost at fixed capacity".
  - (b) Finding 3, "better than either half": against E031 this is point estimates only (S1 −0.23 s), neither pre-registered nor bootstrapped.
  - (c) Finding 4, "It holds for the `NM_missing_other` out-of-range counts": this holds for the codes arm only (E030, < 1 h band 25). The CTR arm E031 has 86, E029 82, and the blend 82.
  - (d) Finding 5, "about 5× faster than on CPU": this compares the Day 4 cloud CPU (4 vCPU, 0.88–1.13 s per iteration) with the laptop GPU (0.16–0.25 s). No laptop-CPU run at full combinations exists. State the hosts.
- **D5-C13. Missed forecasts** (DAY_SUMMARY §7; as D3-C8, D4-C10). Add the Advisor's magnitude misses:
  - **H023 v3:**
    - `NM_present_excl_LIRF` −1.8 to +0.3 s → −3.96;
    - all rows −1.5 to +0.5 → −3.58;
    - against E026, −1.5 to −3.5 → −5.62;
    - S1 against E026, −0.3 to +1.8 → −4.17;
    - row 192622644, 4,500–8,000 s → 9,008;
    - H023r due, P 0.05 → due.
  - **H021 v3:**
    - development mean 446–458 s → 440.76;
    - runtime 28–35 min → 25.4;
    - row 192622644 below 7,041 s, P 0.60 → 10,976.
  - **H022 v3:**
    - development mean 448–468 s → 446.50;
    - runtime 8–14 min → 3.7.
  - **Advisor record** (as D3-C9, D4-C16):
    - the H021–H023 reviews carried H020's "CatBoost worse and bounded" premise; it was wrong in sign on both counts;
    - the blend arithmetic was right on the realised inputs.
- **D5-C14. Ledger decisions** (as D4-C11):
  - E026–E034 carry `decision: null`;
  - fill E033 and E034 as item 2 decides;
  - the non-candidates (E026–E032) may stay null, as E020 and E021 do, with their roles in `notes`.
- **D5-C15. Clerical:**
  - (a) E033's rule 12 call held E033 only, while its Validation Plan named `<H023> E029 E026`. The quoted E019 bands (83, 22, 81) come from `range_check_E023.json`. They equal E026's at non-LIRF airports (D5-C3), but the substitution should be stated.
  - (b) `src/prc/tracking.py` hard-codes the W&B champion lineage as {E001, E002, E005, E019}. It omits E003 and lacks E033. This affects the mirror only (INC-0009).
  - (c) "`prc.tracking` reads only `metrics.json`" (proposal) is imprecise. It also reads `gate.json`, `config.yaml`, `resource-usage.json` and `curves.json`. None of them carries an H figure, so the claim that W&B cannot receive H stands.
  - (d) Append to INC-0007 a pointer to INC-0010: its swap-0 closure held only for boot `71605e21`. Add the D05-S04 start line of `orchestration/session-registry.jsonl` ("swap 0") to D5-C1's list by an appended note.
- **D5-C16. D3-C3 restated for E033** (STATE; DAY_SUMMARY §9.3): as (h).
  - The January 2026 count fact and "H does not test it" stand.
  - The development out-of-range share in the > 3 h band is 0.57 % against E019's 15.3 %.

**Conditions on the phase-closing commit:**
- **The acknowledgement** is committed before the access.
- **The holdout result and its task-ledger line** are committed.
- **`research/STATE.md`** is current, with a measured header time. It records:
  - the champion per the outcome, with item 3's disclosures;
  - Day 5 holdout 1 of 1 used;
  - INC-0004, INC-0009 and INC-0010 open, and INC-0006 closed;
  - standing rules 1–13, B1–B4, and rulings H, B, R, H3, H4, H5, rule L v2 and the hand-off base ruling;
  - the next action.
- **`DAY_SUMMARY.md`** is corrected per D5-C8 to D5-C16 and marked final, with the H outcome and the instance check.
- **Journal and ledger.** A Day 5 phase-close journal entry exists, and the ledger decisions follow D5-C14.
- **Mirror.** The exchange is mirrored: `envelope.yaml`, `response.md` and `checksums.sha256`.
- **Session registry.** It has an end event for D05-S05.
- **Incidents:**
  - INC-0006 is closed with "no delegated work". Verified: no provenance line in any Day 5 record, and no record claims delegation.
  - INC-0007 gets its pointer (D5-C15 (d)).

## Revision

None required for this version.

**Standing review rule added from this exchange.** It applies from the next proposal onward.

13. **Stochastic components.**
    - Applies to any candidate or champion with a non-deterministic component (for example, CatBoost on GPU).
    - Beside criterion 6, it reports, per development fold and twin:
      - the reproduction's all-rows ΔRMSE;
      - its ΔRMSE on the mechanism population;
      - the RMS prediction change between the two draws.
    - It states that its evaluated and H figures are one draw.
    - This is disclosure only. It changes no criterion, tolerance or outcome.

## Advisor Prediction

These are for the authorized access.

Probability of improvement:

| Event | P |
|---|---|
| H outcome WIN (E033 against E026) | 0.87 |
| H outcome TIE | 0.11 |
| H outcome LOSS (revert) | 0.02 |
| E033 is champion after the phase close | 0.98 |
| \|RMSE_H(E026) − 375.927\| ≤ 0.02 s (the instance check) | 0.90 |
| The access completes on the first issue | 0.97 |

Expected magnitude:
- **E033 − E026 on H:** −3 to −10 s (central −6). E026 ≈ 375.93 s; E033 ≈ 366–373 s.
- **The q10–q90 width** is 2–4 s, comparable to R1–R3.

Primary expected failure mode:
- **No revert is expected.** The plausible adverse outcome is a TIE. Its likely cause is a few December airport-day clusters:
  - `NM_missing_other` rows the D3-C2 treatment does not reach;
  - LIRF NM-present day-scale records the CatBoost half raises.
- **A TIE leaves the promotion standing.** The record would then say that December did not confirm the margin.
