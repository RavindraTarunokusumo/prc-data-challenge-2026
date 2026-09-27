---
schema: advisor-review-v1
hypothesis_id: H008
proposal_version: 1
proposal_sha256: 8266cc62f8905511bb3a6232ee038fdf30e1f1a2f188ea2efcc9da27f997a525
exchange_id: X-D01-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-09-27T12:32:09Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**

H008 is a clean group ablation of H006:
- the same code path, hyperparameters, seed, folds and class;
- only the feature set changes, to `FS0_NO_DELTAS`, which is FS0 minus `d_aobt3`, `d_eobt1`, `d_sched` and `flt_missing`.

`prc.features.columns` passes only the columns present, and `test_gbm_uses_only_present_columns` passes. The decisive criterion is coherent: H006 must pass criteria 1–2 against H008. H008 is correctly excluded from promotion.

**Verified here.** The batch-level checks recorded in `H001_review_v1.md` also hold for H008:
- hashes, tests (90 of 90), lint and a clean tree;
- parameters unchanged since `866b902`.

**Finding: the pre-registered Expected Result contradicts itself.** Take the batch's own pre-registered ranges:

| Model | Pre-registered development-fold mean RMSE (s) |
|---|---|
| H001 | about 580 |
| H002 | 539–563 (3–7 % below H001) |
| H003 | 523–557 (1–3 % below H002) |
| H005 | 360–420 |
| H004 | 400–470 |
| H006 | 306–399 (5–15 % below the better of H004 and H005) |

Against these ranges the two clauses of H008's Expected Result do not overlap:
- "10–20 % above H006" means 337–479 s.
- "0–5 % below H003" means 497–557 s.

One clause must fail. The Mechanism section's own statement, that removing the deltas should push the RMSE "back towards H003 levels", points to the second clause.

**Consequences.**
- The Expected Result cannot be scored as a prediction.
- It does not affect validity, because the falsification criterion alone is decisive.
- The acknowledgement must record the inconsistency. It must not substitute a new expected value after this review.

**Minor.** The proposal's Alternative Explanations correctly notes that `feature_fraction` 0.9 samples 6 of 7 features here, against 10 of 11 in H006. The effect is minor.

## Scientific Validity

**What the ablation supports.** It is sound, and it supports exactly the claim that H006 relies on the NM and schedule deltas as a group. It cannot support the claims that H006 corrects the anchor's airport bias or learns interactions; those rest on H006's falsification clause against H004.

**Day 2 question.** H008 also partly answers how much signal exists without NM operational timestamps. It is **not** a causal-only (P-labelled) variant, because it keeps the takeoff hour and weekday, which are labelled T.

## Novelty Relative to Existing Research

- It is the mechanism ablation required by brief §10 item 4 for H006.
- It is not redundant with H003. H008 uses an L2 conditional mean over airport, runway, wake, market segment, flight type, hour and weekday, whereas H003 uses an airport × hour median.

## Experimental Isolation

- **One change.** Four features are removed as a group, and the group is the object of the claim.
- **`flt_missing`.** Removing it is justified, because it only encodes whether the removed inputs exist.
- **Individual attribution.** A split between `d_aobt3` and the other deltas is not needed for this claim.

## Validation Quality

**Folds and criteria.**
- The frozen folds are used unchanged, and the twins are scored.
- **Forward exposure.** The sign is pre-registered: H006 against H008 < 0 on S1c and W1c.

**The day-scale LIRF row.** It sits in S1's validation month (`d_aobt3` = 87,181 s) and affects H006 and H008 alike, because both predict bounded values. H006 against H008 is therefore not decided by it. This comparison is robust.

**Batch conditions.** B4 (row concentration) still applies, because this comparison is a criterion-4 check for H006. B1–B4 are defined in full in `H001_review_v1.md`.

## Leakage Review

### Target Leakage

PASS

The same pipeline as H006, with fewer inputs. No target-derived input is used.

### Temporal Leakage

PASS

The remaining inputs are labelled P (airport, runway, the NM categoricals) or T (takeoff hour and weekday), and all are admissible under §6.2.

### Competition Availability

PASS

Every remaining input is present in `ranking.parquet`.

## Compute Review

### RAM

PASS

It has the FS0 footprint, measured at 3.45 GB on fold H, plus LightGBM with 7 features. Expect under 4.5 GB, within CLASS-M.

### Runtime

PASS

At most H006's cost: about 9–10 minutes, and less with 7 features. The CLASS-M timeout is 45 minutes.

### Disk

PASS

About 10 MB.

## Weakest Assumption

That a large gap between H006 and H008 shows H006 "relies on the anchor" in a useful sense. The gap is almost certain, because the audit already puts the anchor's proxy RMSE at 385 s against 546 s for the constant. A pass therefore adds little information beyond the audit. Its main value is the H008 RMSE level itself, as the Day 2 reference for FS0 structure without the deltas.

## Missing Control or Ablation

None required for this ablation. Condition B4 applies to the comparison with H006.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Primary run.** One primary run:
  1. `uv run python scripts/gate.py allocate H008 v1`.
  2. Write the config exactly as in the Implementation Plan: `model: lightgbm`, `feature_set: FS0_NO_DELTAS`, `params` identical to H006, `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
  3. Run `uv run python scripts/run_experiment.py E###`.
- **Comparison.** `scripts/compare.py <H006 E###> <H008 E###>`, with the B4 figures.
- **No reproduction run and no promotion.** H008 is an ablation.
- **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun` is permitted and must be logged.
- **Not authorized:**
  - any change to the feature list or the hyperparameters, which would break the pairing with H006;
  - scoring H.

Required acknowledgement path: `research/day-01/acks/H008_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It must record that the Expected Result is internally inconsistent and will not be scored as a prediction, without substituting a new value.
- It should adopt conditions B1–B4.

## Revision

None required. The Expected Result defect is recorded, not revised, because the decisive criterion is unaffected.

## Advisor Prediction

Probability of improvement: not applicable to an ablation. P = 0.97 that H006 passes criteria 1–2 against H008, supporting criterion 4 for H006.

Expected magnitude: H008's development-fold mean RMSE is about 500–540 s. That is 2–8 % below H003 (an L2 mean beats a median, with runway and wake added) and 40–70 % above H006. P ≈ 0.03 that the "10–20 % above H006" clause holds.

Primary expected failure mode: none for the decisive criterion. The realistic defect is interpretive: H008 is read as a causal-only baseline, which it is not, because it keeps the T-labelled takeoff hour and weekday.
