---
schema: advisor-review-v1
hypothesis_id: H014
proposal_version: 1
proposal_sha256: bfaadc501f4752e83171c10afff3290b1eb5b6dfa40d817ea21ffbe23ee4eca8
exchange_id: X-D02-S01-0004
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-09-28T21:17:37Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT, with preconditions and a lapse rule (as for H010 and H012).**

**H014 is the control H013's M1 claim needs.**
- E006 differs from H013 in both the feature set and the three subsampling parameters.
- The effect M1 must isolate is small: E012 − E006 on `NM_present_excl_LIRF` was −7.16 s. A configuration change could produce an effect of the same order.
- H014 holds the configuration fixed, so H013 − H014 changes one thing: the six FS1 keys.

**Why conditions.**
- H014 has meaning only as the M1 reference of an accepted H013, and H013 v1 is REVISE (`H013_review_v1.md`).
- The H013 revision may change the training configuration, in which case H014 v1 is no longer matched. The ACCEPT therefore lapses unless the accepted H013 version keeps v1's configuration.

**The finding in `H013_review_v1.md` does not break this contrast.**
- The seed also draws LightGBM's 200,000-row bin sample on every fold except W1c.
- H013 and H014 both use seed 42 on the same training DEP rows, sorted by `MVT_ID_mvt`, so their bin-sample indices are identical by construction. Every feature they share gets identical bins.
- H014 makes no seed-invariance claim, so nothing in its text depends on the false premise.

**Verified here** (read-only; batch checks in `H013_review_v1.md`).
- **Hash.** The proposal matches the envelope.
- **Code.**
  - The `fs0` function body is byte-identical to `866b902` (AST comparison).
  - `src/prc/models/gbm.py` is unchanged since `866b902`.
- **E006.**
  - `experiments/E006/config.yaml` has H009 v3's parameters on FS0. So "E006's parameters with the three subsampling values changed" equals "H013 v1's parameters on FS0".
  - E006 took 675.7 s at 3.74 GB (`resource-usage.json`), as H014 cites.
- **Tree.** The tree is clean, and `tests/test_models.py` passes (13/13).

## Scientific Validity

**The M1 contrasts.**
- H013 − H014 on `NM_present_excl_LIRF` (H013 clause 2(a)) and on NM-present bulk rows (clause 2(b)) measure the six keys under the no-subsampling configuration.
- This is the same test that H009 v3 ran against E006, now with the training configuration matched.

**H014 − E006 (reported) is useful beyond attribution.**
- It measures the configuration change on a second feature set (FS0), next to H013 − E012 on FS1.
- Reusing E013 and E014 for H013's clauses 3 and 4 implicitly assumes that the configuration effect does not depend strongly on the feature set.
- These two measurements are the only evidence on that assumption. How to use them in H013 v2's admissibility rule is the researcher's call.

**The expectations are plausible.**
- A development mean of 370–390 s (E006: 377.87).
- H014 − E006 within ±4 s per development fold on `NM_present_excl_LIRF`.
- H013 − H014 on the same population: −4 to −15 s, with at least three counted WINs including S1. E012 − E006 gave −7.16 s with four counted WINs.

## Novelty Relative to Existing Research

**Not redundant.** No completed experiment fits LightGBM on FS0 without subsampling. H014 is a reference, not a hypothesis.

## Experimental Isolation

| Contrast | Change | Status |
|---|---|---|
| H013 − H014 | FS0 → FS1 (the six keys), with identical configuration, seed, rows and shared-feature bins | **Clean** |
| H014 − E006 | The three subsampling parameters (plus the subsampling draws that go with them) | Attribution only |

Residual exposures are those of H009's M1 clause, recorded in `H009_ack_v3.md`:
- late departures in 2(a);
- W1c sensitivity: E012 − E006 was a W1c LOSS, which voided the W1 WIN;
- LIRF late departures in 2(b).

## Validation Quality

- **Folds.** The frozen folds are used unchanged: seven scored folds, with H predicted only.
- **Status.** H014 is not a candidate: there is no reproduction and no promotion comparison.
- **Clauses.** H013's clauses 2(a) and 2(b) are computed against H014 with committed code. This requires `scripts/compare.py`, `scripts/mechanism_check.py` and `src/prc/attribution.py` unchanged from `5ba9230` until they are computed.
- **Twins.** The rule 2 twin expectations (S1c < 0; W1c ≤ 0, LOSS possible) are H013's and are read on `NM_present_excl_LIRF`.

## Leakage Review

### Target Leakage

PASS

- The inputs are FS0 (E006). There are no target statistics.
- Bins and vocabularies come from training rows only.

### Temporal Leakage

CONCERN

These are label notes, as for E006, and are not blocking: `hour_utc`, `weekday` and the `d_*` deltas are T.

### Competition Availability

PASS

Same as E006.

## Compute Review

### RAM

PASS

Below 5 GB expected (E006: 3.74 GB; CLASS-M: 8 GB).

### Runtime

PASS

- 676 s × 1.1–1.4 ≈ 12–16 min. The timeout is 45 min.
- **Compute discipline.** If H013 fails its clause 1 (promotion against E005), its M1 clauses have no decision use, and H014 is not worth running (precondition 1(d)).

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

**The assumption.** The accepted H013 version keeps v1's training configuration: the three subsampling parameters and nothing else.

**What follows if it does not.** If H013 v2 changes how the model is trained (`H013_review_v1.md`, Revision item 1(a)), H014 v1 is no longer matched, and it lapses.

## Missing Control or Ablation

None is required for its stated purpose.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions (all must hold before `gate.py allocate H014 v1`).**
   - (a) An H013 version ≥ 2 has decision ACCEPT, and its acknowledgement is committed.
   - (b) **That version's training configuration is H014 v1's, except for the feature set.**
     - `model: lightgbm`.
     - `params`: `objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 1.0`, `bagging_fraction: 1.0`, `bagging_freq: 0`, `num_threads: 4`, `num_boost_round: 1000`.
     - `seed: 42`.
     - No other training parameter is set.
   - (c) That version uses H014 as the reference of its M1 clauses: `mechanism_check.py <H013> <H014> NM_present_excl_LIRF` and `… NM_present`.
   - (d) H013's primary run is COMPLETE, and H013 does not meet its clause 1 (it passes criteria 1–3 against E005).
   - (e) The code and environment are unchanged:
     - the `fs0` body and `gbm.py` are unchanged (as verified here), `uv.lock` is `39df945c…` and silver is pinned;
     - the clause code is unchanged from `5ba9230` until H013's clauses 2(a) and 2(b) are computed;
     - no other experiment runs concurrently.
2. **Lapse.** If (b) or (c) does not hold, this ACCEPT lapses. An `H014_v2` matched to the accepted H013 version is then required.
3. **One primary run.**
   - `uv run python scripts/gate.py allocate H014 v1`.
   - Config: `hypothesis_id: H014`, `proposal_version: 1`, `model: lightgbm`, `feature_set: FS0`, the `params` in 1(b).
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
   - Then `uv run python scripts/run_experiment.py E###`.
4. **Comparisons** (completed experiments only; no new run):
   - `mechanism_check.py <H013> <H014> NM_present_excl_LIRF` (H013 clause 2(a));
   - `mechanism_check.py <H013> <H014> NM_present` (H013 clause 2(b));
   - `compare.py <H013> <H014>` (rules 1, 6 and 7);
   - `compare.py <H014> E006` (reported; the configuration change on FS0).
5. **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun`, logged.
6. **Not authorized:**
   - a reproduction run;
   - use as a promotion candidate or champion;
   - any change to features, parameters, folds or seed;
   - scoring H.

Required acknowledgement path: `research/day-02/acks/H014_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It must adopt preconditions 1(a)–(e) and the lapse rule.
- It must record that H014 matches H013 on the bin sample only while both use seed 42 on the same training rows.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Development mean within 370–390 s | 0.85 |
| H014 − E006 within ±4 s on `NM_present_excl_LIRF` on every development fold | 0.70 |
| H013 − H014 passes criteria 1 and 2 on `NM_present_excl_LIRF` (H013 clause 2(a) not met) | 0.72 |
| H013 − H014 NM-present bulk dRMSE < 0 on at least 4 of 5 development folds (clause 2(b) not met) | 0.88 |
| W1c comes out LOSS for H013 − H014 on `NM_present_excl_LIRF` | 0.30 |

Expected magnitude:

| Quantity | Expected |
|---|---|
| Development mean | 372–385 s |
| H014 − E006 on `NM_present_excl_LIRF` | −2 to +3 s per development fold |
| H013 − H014 on `NM_present_excl_LIRF` | −5 to −10 s (mean) |

Primary expected failure mode (of the reference's role):
- **Primary.** The configuration change interacts with the static keys, so H013 − H014 differs from E012 − E006 by a few seconds on one fold. R1, the smallest M1 margin in E012 − E006 (−4.71 s), then comes out TIE. Clause 2(a) survives on R2, R3 and S1.
- **Secondary.** A W1c LOSS voids the W1 WIN again (as in E012 − E006).
