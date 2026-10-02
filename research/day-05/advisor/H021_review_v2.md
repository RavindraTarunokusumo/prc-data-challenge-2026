---
schema: advisor-review-v1
hypothesis_id: H021
proposal_version: 2
proposal_sha256: c97b36b34eeda65400d861381722f0a339d8edd5e1114f88cfddbeeb57d7acde
exchange_id: X-D05-S04-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.85
created_utc: 2026-10-01T20:16:40Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.85).** v2 meets all seven required revisions of `H021_review_v1.md`, and **the CLASS-L request is justified** (ruling under Compute Review). It cannot be accepted as written, for three reasons; the first two are new findings from checks run here.

1. **The comparability check that clause 1 is read through will fire by construction.**
   - H021 cites H022's check: "`resolved_params.json` against H022's". H022 v2 defines it: every resolved key must be equal except the listed categorical ones, or "the pair is not matched … H021's clause 1 is read as INCONCLUSIVE".
   - **Verified here** on a synthetic GPU fit through `gbm.catboost`, with H021's CTR settings in both `cat_mode` values. The resolved parameters also differ on keys outside H022's list:
     - **`data_partition`**: FeatureParallel (ctr) against DocParallel (codes);
     - present in ctr mode only: `permutation_count` 4, `fold_permutation_block` 64, `has_time` false, `counter_calc_method` SkipTest, `ctr_history_unit` Sample, `ctr_target_border_count` 1.
   - As written, clause 1 would be INCONCLUSIVE with near certainty, or would need a post hoc reading of which keys count as categorical.
   - The fix may change both arms' configurations, so it belongs to the matched pair: H021 and H022 are revised together (`H022_review_v2.md`).
2. **The tools freeze is anchored to a commit after which the frozen tools changed, and its list is incomplete.**
   - The anchor is "frozen from the X-D05-S04-0001 submission commit" (`503763b`). After it, `60365dd` changed `gbm.py`, `curves.py`, `worker.py`, `scripts/run_experiment.py` and `models/__init__.py`, added `prc/blending.py` and deleted `models/blend.py`, as v1 required. Read literally, the freeze is already broken.
   - The list omits:
     - the routed ridge `src/prc/models/linear.py`, whose bits are the integrity reference;
     - the clause population definitions in `src/prc/attribution.py`;
     - the data loader;
     - `uv.lock` and `pyproject.toml`.
3. **The reproduction's routed rows are unchecked.**
   - H023r is ½ E029 + ½ H021r.
   - The plan runs `route_check.py` on H021 only.

**v1 required revisions:**

| v1 item | v2 | Verdict |
|---|---|---|
| 1. Integrity clause | `route_check.py <H021> - E029`; failure scoped to all-rows comparisons and H023; clause 1 still read | **Met.** The reference is attainable: P ≈ 0.95 (`LAPTOP_REFS_review_v2.md` (a)). Clause 1's population excludes LIRF (`prc.attribution`: `~nm_missing & ADEP != LIRF`) |
| 2. Resolved parameters | `resolved_params.json`, per fold, from `get_all_params()` | **Met.** `note_params` runs inside every fold, H included (curves are active in every fold). The test passes, and the capture works on GPU (synthetic) |
| 3. Calibration | Table corrected (D5-C7); `h021_exact` and `h022_exact` through the routed path | **Met.** 248.5 / 248.8 s per R3 fit; peak RSS 4.66 GB; device peak 3,788 MiB including 869 MiB of desktop use. Its `resolved` field is null, so the run's own `resolved_params.json` is the first record of the exact resolved configuration |
| 4. RAM and class | 6–7.5 GB; CLASS-L on runtime | **Met.** Ruled below |
| 5. Clause 1 WIN count | `fold_outcome_counted` among R1, R2, R3, S1, W1 | **Met.** The field is produced by the frozen `promotion_check` |
| 6. Failure recording | `gpu_failure` gives RESOURCE_FAILURE; no retry; the chain stops | **Met.** The regex and its test pass. A kernel OOM or the RSS guard gives RESOURCE_FAILURE as before |
| 7. Alternative explanations | Tail contamination added | **Met** |
| Recording | Curves and the 800–1,000 slopes, `gpu_mib_peak`, swap, unseen-level shares, S1c/W1c | **Met** |

**Verified here** (beyond `LAPTOP_REFS_review_v2.md`):
- **Code:**
  - `curves.note_params` precedes `curves.record` in `gbm.catboost`;
  - the worker writes `resolved_params.json` with `default=str`;
  - `reproduce_check.py`'s `--champion` is optional, so H021's reproduction call is valid.
- **Synthetic GPU:** both `data_partition` values are accepted in both `cat_mode` values on this build, so equalizing the arms by configuration is feasible.
- **Provenance:** the session runs `--effort high` with `claude-opus-5-5` (process arguments), as the proposal states.

## Scientific Validity

### (a) The science is unchanged and sound

The research question, the mechanism (with `FloatTargetMeanValue` verified in v1 to average the raw target), FS2_RAW, the single a-priori configuration, H022 as the control, clause 1's floor and readings, and the noise condition all stand as accepted in v1.

### (b) The comparability check must be decisive before the run

**The check's purpose is right:** it turns "only `cat_mode` differs" into a recorded fact.

**Its exempt set must be complete and closed before any run.** Otherwise, one of two things happens:
- it fires on keys that are consequences of the treatment itself (no categorical feature means no CTR permutations, and CatBoost then picks a different data partition);
- or the researcher decides after the run which keys "are categorical". That is the post hoc flexibility pre-registration exists to prevent (rule 10's spirit).

**`data_partition`:**
- It is not a CTR setting.
- On one device, I expect it to select a data layout, not model capacity. But that is a claim the proposal must make and support, or make moot by equalizing the arms.

**The options are named in `H022_review_v2.md`; the choice is the researcher's.**

### (c) The freeze must name the code reviewed here

- The code reviewed in this exchange is `60365dd`.
- A freeze that starts earlier than the code it protects is not a freeze.
- One that omits the ridge, the populations or the lock leaves the integrity reference, clause 1's population and item 6's environment unprotected.
- The Day 4 precedent (`H018_review_v2.md`, authorized scope 1(e)) is the model: no change under `src/` or `scripts/`, in `pyproject.toml` or in `uv.lock`, from a named commit to the chain's last comparison. Run commits may differ only in records.

### (d) The reproduction feeds H023r

- H021r's routed rows enter H023r at half weight.
- They should meet the same integrity check as H021's, and its consequence for H023r should be stated.

## Novelty Relative to Existing Research

- **This is the first CatBoost run, with the matched control** that the Day 4 review and phase close asked for (Missing Control 3).
- **It is not redundant with H019** (explicit fold-local priors) **or H020** (rejected; its objections are answered).

## Experimental Isolation

- **Against H022: one parameter,** `cat_mode`, plus what the representation entails: the CTR features, combinations and frequencies; quantization of the codes; and alphabetical order.
- **The resolved-key differences in (b) belong to the treatment** if the researcher shows they follow from declaring no categorical feature. `data_partition` is the one that needs an argument or an equalized configuration.
- **Against E029: not isolated,** and not claimed to be.

## Validation Quality

**The frozen folds are used unchanged:** all 8 predicted, H predicted only.

**Clause 1:**
- It runs through `mechanism_check.py`, which is the frozen `promotion_check` on the population, with counted WINs.
- It is read "at this budget", with both arms' slopes recorded.

**Noise and reproduction.**
- The noise condition is decisive: INCONCLUSIVE when the H021r−H021 mean exceeds 1.5 s.
- The unconditional seed-43 reproduction is the right noise scale.

## Leakage Review

### Target Leakage

PASS

- The CTRs come from training rows only, over permutations.
- Validation rows have null targets in the masked view and take the training statistics.
- FS2_RAW uses no target, and no validation row.

### Temporal Leakage

CONCERN

This is carried, not blocking.
- FS2's T features are unchanged.
- In S1 and W1, the CTR statistics include post-validation training months, by the frozen fold design. The S1c and W1c cells are reported beside them.

### Competition Availability

PASS

- The raw keys are label P and present in the ranking files.
- Levels unseen in a fold's training rows become `__NULL__`. The 2026 shares are recorded target-free (rule 2).

## Compute Review

### RAM

PASS

**The estimate is credible:** 6–7.5 GB. My estimate is 6.0–7.5 GB, from:
- `h021_exact`, 4.66 GB with silver released;
- silver resident, about 1–2 GB;
- the H fold, with 9 % more training rows than R3;
- E029's 6.60 GB on the LightGBM path.

**Swap.** `swap_out_pages_during_run` is recorded. Under INC-0010, a run that swaps is not called within class on RSS alone.

### Runtime

PASS

**CLASS-L ruling (brief §4): justified, for H021 and its seed-43 reproduction only.**

**Evidence.**
- `h021_exact` took 248.5 and 248.8 s per R3 fit on the routed path, including the ridge and the string conversion.
- The folds' training months sum to 63, or 6.3 R3-equivalents, which gives about 26 min of fitting.
- Eight FS2_RAW builds, staged curve predictions and scoring add 3–8 min.
- My estimate is 28–35 min, with P(> 30 min) ≈ 0.65.
- Under CLASS-M, `within_class` would be a coin flip on an a-priori configuration the v1 review accepted. Through H023's criterion 7, the coin flip would decide a promotion criterion.
- Cutting iterations to fit CLASS-M would change both the configuration and the budget at which clause 1 is read.

**Why it is not H020's refusal.**
- H020's CLASS-L was declined because that design could not answer its question, and its result informed no decision (`H020_review_v1.md`).
- Missing Control 3 asked for "a CLASS-L or GPU rationale tied to a decision". H021 now has:
  - a matched control and a decisive clause;
  - two decisions: H023's component, and whether CatBoost goes into Days 6–7;
  - an unconditional reproduction, which is a confirmation run, one of brief §4's examples.
- The overrun is marginal (≤ about 15 %), on one fixed configuration with no search.

**Conditions** (carry into v3 unchanged):
1. CLASS-L covers H021 and H021r. H022 stays CLASS-M, and H023 CLASS-S.
2. No parameter changes to fit any class.
3. The analysis reports, beside `within_class`, whether the run would also have been within CLASS-M (≤ 30 min and ≤ 8 GB).
4. The RAM side was not part of the justification. A peak RSS above 8 GB, or any swap-out, is disclosed beside criterion 7.
5. For H023's criterion 7, H021's class is CLASS-L.

The runner's CLASS-L timeout is 135 min.

### Disk

PASS

About 15 MB of predictions, curves and resolved parameters, covered by the manifest.

## Weakest Assumption

**That integer codes are an information-poor control** (as in v1).
- Destination, aircraft type and stand names are hierarchical.
- A depth-8 symmetric tree can recover part of that structure from code ranges, even at 254 borders.
- Clause 1 is then decided near its −3.0 s floor.

## Missing Control or Ablation

None for clause 1: H022 is the control. The H023-level control (the E029 + H022 blend) is named in `H023_review_v1.md` and is not required for a claim scoped to this configuration.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- There is no allocation of H021 v2 or of its reproduction.
- No CatBoost fit with a real target on a frozen fold.
- **Still allowed:**
  - synthetic tests;
  - target-free checks;
  - permuted-target GPU fits of both exact configurations that compute no metric. One example is establishing the resolved-key difference of the exact pair on R3.

Required acknowledgement path: `research/day-05/acks/H021_ack_v2.md`.
- It references both hashes and confers no authority.
- Submit `H021_v3.md` with H022 v3 and H023 v3 in one exchange. LAPTOP_REFS v2 stands.

## Revision

**Required (minimal):**

1. **Comparability, jointly with H022 v3.**
   - Adopt H022 v3's closed definition of the comparability check.
   - If the researcher equalizes `data_partition` (or any other key) by configuration, set it identically in H021's parameter table.
   - Clause 1 is read INCONCLUSIVE only under that closed definition.
2. **Tools freeze.**
   - Anchor it to the commit that contains the code submitted with v3. If the code is unchanged, that is `60365dd` or later.
   - Freeze, until the chain's last comparison, all code under `src/` and `scripts/`, plus `pyproject.toml` and `uv.lock`. This includes `src/prc/models/linear.py`, `src/prc/attribution.py` and `src/prc/data.py`.
   - Run commits may differ only in records (`research/`, `experiments/`, `orchestration/`, `docs/`).
3. **Reproduction integrity.**
   - Add `route_check.py <H021r> - E029` to the reproduction step.
   - State its consequence: H021r INVALID for all-rows comparisons and as H023r's component. The noise condition is unaffected, because its population excludes LIRF.

**Acceptable as is (carry into v3 unchanged):**
- the research question, mechanism and configuration table;
- FS2_RAW; the routing and `route_train_exclude`;
- clause 1, its floor, the counted-WIN rule and "at this budget";
- the noise condition and the unconditional reproduction;
- the integrity clause and its scope;
- the failure recording;
- the recording items; "Not claimed"; the alternative explanations; rules 1–12;
- **CLASS-L, with the conditions above;**
- the RAM, VRAM and disk estimates.

## Advisor Prediction

These are for a v3 run of the same design.

Probability of improvement:

| Event | P |
|---|---|
| Clause 1 not met (H021 − H022 ≤ −3.0 s with ≥ 3 counted WINs) | 0.60 |
| The v2 comparability check, as written, flags a key outside its list | 0.97 |
| H021 passes `route_check.py <H021> - E029` on all 8 folds | 0.95 |
| The noise condition triggers (reproduction differs by > 1.5 s) | 0.12 |
| H021 − E029 below 0 on `NM_present_excl_LIRF` | 0.10 |
| Development-mean validation curve still falling by ≥ 0.5 s over iterations 800–1,000 | 0.65 |
| Prediction on row 192622644 below E029's 7,041 s | 0.60 |
| Runtime above 30 min | 0.65 |
| Runtime above 90 min | < 0.01 |
| Peak RSS above 8 GB | 0.08 |
| Any swap-out during the run | 0.10 |

Expected magnitude:
- **H021 − H022, `NM_present_excl_LIRF`:** −1 to −10 s (central −5).
- **H021 − E029, `NM_present_excl_LIRF`:** +3 to +14 s (central +7).
- **Development mean:** 446–458 s (central 450).
- **Runtime:** 28–35 min.
- **Peak RSS:** 6.0–7.5 GB.

Primary expected failure mode:
- **As written.** Clause 1 is read INCONCLUSIVE through the comparability check, on `data_partition` and the CTR-only keys, for no scientific reason.
- **After revision.** The statistics help by less than pre-registered, because the codes arm recovers part of the naming hierarchy. Clause 1 is decided within about 2 s of −3.0 s.
