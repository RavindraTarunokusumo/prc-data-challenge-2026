---
schema: advisor-review-v1
hypothesis_id: H022
proposal_version: 2
proposal_sha256: 363b736693175f9224ea5cd2d5fcd6d4806a40522c2a8a7b05eabd1bbeafb920
exchange_id: X-D05-S04-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.92
created_utc: 2026-10-01T20:16:40Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.92).** v2 meets all four required revisions of `H022_review_v1.md`. One new defect, verified here, blocks it: **the comparability check fires by construction.** The tools freeze also inherits H021's wrong anchor.

**The check as written:** H022's resolved `get_all_params()` must equal H021's on every key except:
- `simple_ctr`, `combinations_ctr`, `max_ctr_complexity` and `one_hot_max_size`;
- "any per-feature CTR key";
- `cat_mode` and `n_cat_features`.

Any other difference makes the pair "not matched", and H021's clause 1 is then INCONCLUSIVE.

**What the resolution gives.** A synthetic GPU fit through `gbm.catboost` used H021's CTR settings, 300,000 training rows, 9 categorical columns in ctr mode against 0 in codes mode, and no project data. It resolved 58 keys in ctr mode against 48 in codes mode. Besides the listed keys, the arms differ on:

| Key | ctr (H021) | codes (H022) |
|---|---|---|
| `data_partition` | FeatureParallel | DocParallel |
| `permutation_count` | 4 | absent |
| `fold_permutation_block` | 64 | absent |
| `has_time` | false | absent |
| `counter_calc_method` | SkipTest | absent |
| `ctr_history_unit` | Sample | absent |
| `ctr_target_border_count` | 1 | absent |

Three of these are arguably "CTR settings" by name. `permutation_count`, `fold_permutation_block` and `has_time` are permutation settings that, under Plain boosting, serve the CTRs; the proposal does not say so. **`data_partition` is not a categorical setting at all.**

As written, the check therefore reads clause 1 INCONCLUSIVE with near certainty, or invites a post hoc decision about which keys count. Both defeat its purpose.

**v1 required revisions:**

| v1 item | v2 | Verdict |
|---|---|---|
| 1. Integrity clause | `route_check.py <H022> - E029`, scoped; does not reach clause 1 | **Met.** Attainable: P ≈ 0.95 (`LAPTOP_REFS_review_v2.md` (a)) |
| 2. Comparability source | `resolved_params.json`, per fold | **Met** as a source. Its comparison rule is the new defect above |
| 3. Resources | `h022_exact` measured; CLASS-S wording removed; FS2 noted | **Met.** 37.0 / 35.8 s per R3 fit; peak RSS 3.97 GB with silver released; device peak 3,881 MiB including 954 MiB of desktop use. My RAM estimate is a little higher than the proposal's 5–6 GB (5.5–7.0 GB), and inside CLASS-M either way |
| 4. Mechanism text | Quantization at 254 borders; alphabetical order | **Met** |

**Verified here:**
- **Both `data_partition` values are accepted in both `cat_mode` values** on this CatBoost build (synthetic GPU fits).
- `tests/test_models.py::test_catboost_codes_mode_uses_no_categorical_features` passes. In codes mode, `n_cat_features` resolves to 0.

## Scientific Validity

### (a) What the control removes

As in v1:
- **Removed:** every CTR, frequency, combination and one-hot encoding. The codes are quantized at 254 borders, so the high-cardinality keys cannot be isolated level by level.
- **What alphabetical order carries:** part of the naming hierarchy. The v2 Mechanism text states both.

### (b) The check must be closed before the run

A matched-pair check is only decisive if its exempt set is fixed in advance and is exactly what the treatment entails.

**Options** (named, not chosen):
- **(i) Exempt by rule, with an argument.** Exempt the keys that CatBoost resolves only when categorical features are declared, listed as a closed set from a fit of both exact configurations. Exempt `data_partition` too, with the argument that on one device it selects a data layout, not model capacity.
- **(ii) Equalize by configuration.** Set `data_partition` to the same value in both arms (feasible: verified above), and exempt the CTR-only keys.
  - This changes both arms' parameter tables, so H021 changes with it.
  - Under (ii), the researcher should also say whether a forced partition alters H021's or H022's fit beyond float order.

**Either way:**
- record the key difference of the two exact configurations, from a synthetic or permuted-target GPU fit, before submission;
- write the exempt set as a closed list.

### (c) Role and run order

H022 runs first and is never NEW. It is the reference side of H021's clause 1, and carries no claim of its own. All of this is unchanged.

## Novelty Relative to Existing Research

This is the first within-learner contrast of categorical handling in the project: Missing Control 3's "contrast whose only difference is the categorical handling, at fixed capacity".

## Experimental Isolation

- **One parameter against H021:** `cat_mode`. Verified in code and test.
- **The resolved-key differences** (b) are consequences of that parameter, except possibly `data_partition`. Isolation holds once the check classifies them before the run.

## Validation Quality

- **Folds.** The frozen folds are used unchanged, all 8, with H predicted only.
- **Reported comparisons** against E029 are family contrasts.
- **No reproduction.** H021's reproduction supplies the noise scale. Accepted in v1.

## Leakage Review

### Target Leakage

PASS

The codes come from the fold's training vocabulary, and validation-only levels are NaN. No target is involved.

### Temporal Leakage

CONCERN

This is carried, not blocking. FS2's T features are unchanged from H015 v2.

### Competition Availability

PASS

The raw keys are label P. Unseen 2026 levels become NaN; their shares are recorded under H021's rule 2.

## Compute Review

### RAM

PASS

5.5–7.0 GB expected at the H fold, inside CLASS-M's 8 GB. Swap use is recorded (INC-0010).

### Runtime

PASS

8–14 min (CLASS-M). About 4 min of fitting, from the measured 0.037 s per iteration, plus the frame builds and curves.

### Disk

PASS

About 15 MB.

## Weakest Assumption

**That integer codes are information-poor.** The naming hierarchy and the 1:1 bins of the low-cardinality keys give the codes arm more than the proposal assumes, so H021's clause 1 is likely decided near its floor.

## Missing Control or Ablation

None beyond what H022 is.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- There is no allocation of H022 v2.
- No CatBoost fit with a real target on a frozen fold.
- **Still allowed:**
  - synthetic tests;
  - target-free checks;
  - permuted-target GPU fits of both exact configurations that compute no metric, to record the resolved-key difference.

Required acknowledgement path: `research/day-05/acks/H022_ack_v2.md`.
- It references both hashes and confers no authority.
- Submit `H022_v3.md` with H021 v3 and H023 v3.

## Revision

**Required (minimal):**

1. **Comparability check.**
   - Replace the exempt list with a closed set fixed before the run, covering every key that differs between the two exact configurations.
   - Choose option (i) or (ii) of (b), or another that makes the check decisive, and state its rationale.
   - Attach the recorded key difference of the exact pair as evidence (synthetic or permuted-target GPU fit; no metric).
   - Keep "any other difference makes the pair not matched, and H021's clause 1 is INCONCLUSIVE" for keys outside the closed set.
2. **Tools freeze.** As in `H021_review_v2.md`, Revision item 2:
   - the anchor commit contains the submitted code;
   - all code under `src/` and `scripts/`, plus `pyproject.toml` and `uv.lock`, is frozen until the chain's last comparison.

**Acceptable as is:**
- the single change (`cat_mode: codes`) and its test;
- the role (reference only, never NEW) and the run order (first);
- the integrity clause and its scope;
- the reported comparisons;
- the leakage statements;
- the mechanism text;
- CLASS-M and the runtime and VRAM figures.

## Advisor Prediction

These are for a v3 run of the same design.

Probability of improvement:

| Event | P |
|---|---|
| H022 − H021, `NM_present_excl_LIRF` development mean above +3.0 s (the mirror of H021's clause 1 not met) | 0.60 |
| H022's development mean below E029's 442.5 s | 0.03 |
| H022 passes `route_check.py <H022> - E029` on all 8 folds | 0.95 |
| The v2 check, as written, flags a key outside its list | 0.97 |

Expected magnitude:
- **H022 − H021, `NM_present_excl_LIRF`:** +1 to +10 s (central +5).
- **H022 − E029, `NM_present_excl_LIRF`:** +5 to +20 s (central +11).
- **Development mean:** 448–468 s (central 456).
- **Runtime:** 8–14 min.
- **Peak RSS:** 5.5–7.0 GB.

Primary expected failure mode:
- **As written.** The check fires on `data_partition` and the CTR-only keys, and H021's clause 1 is INCONCLUSIVE by the proposal's own rule.
- **After revision.** The codes arm recovers part of the keys' signal through the naming hierarchy, and clause 1 is decided near its floor.
