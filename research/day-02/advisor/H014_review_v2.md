---
schema: advisor-review-v1
hypothesis_id: H014
proposal_version: 2
proposal_sha256: 49a8ec9036a62c59850a61c102119c17eb5b136a1941d8b09a63819374b441f4
exchange_id: X-D02-S01-0005
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-09-28T21:47:23Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT, with preconditions and a lapse rule (as for H014 v1).**

**H014 v2 is the matched M1 reference H013 v2 needs.**
- H014 v1's ACCEPT lapsed by its own rule: H013 v2 sets a fourth training parameter. `H014_ack_v1.md` records the lapse and that v1 will never be allocated.
- **The only substantive change from v1** is `bin_construct_sample_cnt: 5000000`. I read both versions in full; everything else is wording, plus the runtime estimate (12–20 min, 1.1–1.5×).

**The match is now stronger than v1's.**
- v1 matched H013 on the bin sample only while both drew it with seed 42 from the same rows.
- With bins built from every training row, the bin mappers of the shared FS0 features are identical **by construction**: the same rows, in the same `MVT_ID_mvt` order, with the same binning parameters.
- The seed-dependent record in `H014_ack_v1.md` is superseded.

**Verified here** (read-only; batch checks in `H013_review_v2.md`).
- **Hash.** The proposal matches the envelope.
- **Code.**
  - The `fs0` body is identical to `866b902` (AST).
  - `src/prc/models/gbm.py` is unchanged since `866b902`, and `uv.lock` is `39df945c…`.
- **E006.**
  - `experiments/E006/config.yaml` carries H009 v3's parameters on FS0. So "E006's parameters with the four changed" equals H013 v2's training configuration on FS0.
  - E006 took 675.7 s at 3.74 GB (`resource-usage.json`).
- **Determinism.** The fold-scale synthetic check in `H013_review_v2.md` applies to H014: the same code path, and FS0's categoricals have low cardinality. H014 v2's procedure has no random component on any fold.

## Scientific Validity

**The M1 contrasts are unchanged in kind.**
- H013 v2 − H014 v2 on `NM_present_excl_LIRF` (clause 2(a)) and on NM-present bulk rows (clause 2(b)) measure the six FS1 keys under the deterministic procedure.
- This is the test H009 v3 ran against E006, with the procedure now matched.

**H014 − E006 (reported) measures the procedure change on FS0.**
- **What it covers:** no bagging, no feature subsampling, and all-row bins for FS0's features.
- **What it misses:** FS0 has no high-cardinality categoricals, and those are the features whose bin maps all-row binning changes most (`stand`, `actype`, `op_prefix`, `ades`).
- **So it is a weak proxy** for the configuration shift on the FS1-family references E013 and E014, which is H013 v2's untested "comparable size" assumption. It should be read with that caveat, if at all.

**The expectations are plausible.**
- A development mean of 370–390 s (E006: 377.87).
- H014 − E006 within ±4 s per development fold on `NM_present_excl_LIRF`.
- H013 − H014 on the same population: −4 to −15 s, with at least three counted WINs including S1. E012 − E006 gave −7.16 s with four counted WINs.

## Novelty Relative to Existing Research

**Not redundant.**
- No completed experiment fits LightGBM on FS0 without subsampling, or with bins built from all rows.
- H014 is a reference, not a hypothesis.

## Experimental Isolation

| Contrast | Change | Status |
|---|---|---|
| H013 v2 − H014 v2 | FS0 → FS1 (the six keys), with identical configuration, rows and shared-feature bin mappers | **Clean** |
| H014 v2 − E006 | The four procedure parameters (subsampling off, bins from all rows) | Attribution only |

**Precision note.** "Identical bins" holds for the per-feature bin mappers.
- LightGBM decides feature grouping (exclusive feature bundling) per dataset, so it can differ between FS0 and FS1.
- As in E012 − E006, that belongs to any feature-set contrast in LightGBM. It is not a confound specific to this design.

**Residual exposures** are those of H009's M1 clause (`H009_ack_v3.md`), and they carry:
- late departures in 2(a);
- W1c sensitivity: a W1c LOSS voids the W1 WIN;
- LIRF late departures in 2(b).

## Validation Quality

- **Folds.** The frozen folds are used unchanged: seven scored folds, with H predicted only.
- **Status.** H014 is not a candidate: there is no reproduction and no promotion comparison.
- **Clauses.** H013's clauses 2(a) and 2(b) are computed against H014 with committed code. This requires `scripts/compare.py`, `scripts/mechanism_check.py` and `src/prc/attribution.py` unchanged from `5ba9230` until they are computed.
- **Twins.** The rule 2 twin expectations (S1c < 0; W1c ≤ 0, LOSS possible) are H013's, and are read on `NM_present_excl_LIRF`. This contrast is matched, so objection T of `H013_review_v2.md` does not apply to it.

## Leakage Review

### Target Leakage

PASS

- The inputs are FS0 (E006). There are no target statistics.
- Bins and vocabularies come from the fold's training rows only. Binning from all rows adds no rows beyond `x_tr`.

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

- 676 s × 1.2–1.5 ≈ 14–17 min. Binning from all rows adds seconds, not minutes (`H013_review_v2.md`). The timeout is 45 min.
- **Compute discipline.** H014 runs only if H013 does not meet its clause 1 (precondition 1(d)).

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

**The assumption.** The H013 version whose clauses 2(a) and 2(b) are computed against H014 is v2, run with exactly its authorized configuration.

**What follows if it does not hold.** If H013 v2 is superseded by a version with a different training configuration, H014 v2 is no longer matched, and it lapses.

## Missing Control or Ablation

None is required for its stated purpose.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions (all must hold before `gate.py allocate H014 v2`).**
   - (a) H013 v2 has decision ACCEPT (`H013_review_v2.md`), and `research/day-02/acks/H013_ack_v2.md` is committed.
   - (b) **H013 v2's primary run used exactly its authorized configuration.** This is checked in that run's `experiments/E###/config.yaml`.
     - `model: lightgbm`.
     - `params`: `objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 1.0`, `bagging_fraction: 1.0`, `bagging_freq: 0`, `bin_construct_sample_cnt: 5000000`, `num_threads: 4`, `num_boost_round: 1000`.
     - `seed: 42`.
     - No other training parameter is set.
   - (c) H013 v2 uses H014 v2 as the reference of its M1 clauses: `mechanism_check.py <H013> <H014> NM_present_excl_LIRF` and `… NM_present`.
   - (d) H013 v2's primary run is COMPLETE, and H013 does not meet its clause 1 (it passes criteria 1–3 against E005).
   - (e) The code and environment are unchanged:
     - the `fs0` body and `gbm.py` are unchanged, `uv.lock` is `39df945c…` and silver is pinned;
     - the clause code is unchanged from `5ba9230` until clauses 2(a) and 2(b) are computed;
     - no other experiment runs concurrently.
2. **Lapse.** If (b) or (c) does not hold, this ACCEPT lapses. An `H014_v3` matched to the H013 version that runs is then required.
3. **One primary run.**
   - `uv run python scripts/gate.py allocate H014 v2`.
   - Config: `hypothesis_id: H014`, `proposal_version: 2`, `purpose: primary`, `model: lightgbm`, `feature_set: FS0`, the `params` in 1(b).
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
   - Then `uv run python scripts/run_experiment.py E###`.
4. **Comparisons** (completed experiments only; no new run):
   - `mechanism_check.py <H013> <H014> NM_present_excl_LIRF` (H013 clause 2(a));
   - `mechanism_check.py <H013> <H014> NM_present` (H013 clause 2(b));
   - `compare.py <H013> <H014>` (rules 1, 6 and 7);
   - `compare.py <H014> E006` (reported; the procedure change on FS0).
5. **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun`, logged.
6. **Not authorized:**
   - a reproduction run;
   - use as a promotion candidate or champion;
   - any change to features, parameters, folds or seed;
   - scoring H.

Required acknowledgement path: `research/day-02/acks/H014_ack_v2.md`.
- It must reference the proposal hash and this review's hash.
- It must adopt preconditions 1(a)–(e) and the lapse rule.
- It must record that H014 v2 matches H013 v2's shared-feature bins by construction (bins from all rows of identical training rows). This supersedes the seed-dependent record in `H014_ack_v1.md`.

## Revision

None required for this version.

**Non-blocking notes:**
- `compare.py <H014> E006` is attribution only. It is a weak proxy for the procedure shift on FS1-family models (Scientific Validity).
- If H013's chain step 1 already rules out Day 2 promotion (`H013_review_v2.md`, compute-discipline note), H014 has no Day 2 decision use. Running it is then the researcher's call, recorded as attribution.

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
| Development mean | 372–386 s |
| H014 − E006 on `NM_present_excl_LIRF` | −2 to +3 s per development fold |
| H013 − H014 on `NM_present_excl_LIRF` | −5 to −10 s (mean) |

Primary expected failure mode (of the reference's role):
- **Primary.** The procedure change interacts with the static keys. All-row binning changes the categorical bin maps of FS1's high-cardinality keys, which have no counterpart in FS0. H013 − H014 then differs from E012 − E006 by a few seconds on one fold, and R1 (−4.71 s in E012 − E006) comes out TIE. Clause 2(a) survives on R2, R3 and S1.
- **Secondary.** A W1c LOSS voids the W1 WIN again, as in E012 − E006.
