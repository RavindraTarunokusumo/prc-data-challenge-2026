---
schema: advisor-review-v1
hypothesis_id: H003
proposal_version: 1
proposal_sha256: cbb3848e013eeb924ed5815417c1bd32a9517da323d90d7655ebe1316dc16b80
exchange_id: X-D01-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.90
created_utc: 2026-09-27T12:27:44Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**

H003 changes exactly one thing relative to H002: it adds the UTC takeoff hour to the median key. The estimator stays the same, and the fallback threshold `min_cell` = 30 was fixed a priori. The falsification criterion (criteria 1–2 against H002) is decisive, and the frozen folds are used unchanged.

**Verified here.** The batch-level checks recorded in `H001_review_v1.md` also hold for H003:
- hashes, tests (90 of 90), lint and a clean tree;
- fixed parameters unchanged since `866b902`.

In `airport_hour_median`:
- cell and airport medians come from training rows only;
- cells with fewer than 30 rows fall back to the airport median, then to the global median;
- the joins cannot duplicate rows;
- `tests/test_models.py` shows that the output ignores validation targets.

**Two findings** (neither blocks):
1. **A second, unlisted alternative explanation.** The takeoff hour is labelled T. Part of its association with the target is mechanical rather than diurnal demand: a long taxi moves the same pushback into a later takeoff hour, most visibly at the end of departure banks. The proposal lists only the DST blur. The effect is admissible under §6.2. It has two consequences:
   - the diurnal-demand mechanism is not isolated by this design;
   - the causal-only variant for Days 5–7 will need a P-labelled time key.
2. **DST runs in the opposite direction on W1 and W1c** (details under Validation Quality). H003 may therefore score better on W1c than on W1, the reverse of the usual forward-exposure pattern.

## Scientific Validity

**Mechanism.** The queueing view (the runway as a server, and diurnal banks as arrival bursts) is standard and plausible. The design is a legitimate time-conditioned Tier 0 reference, as brief §11 requires.

**Two limits on what it shows.**
- The UTC hour mixes local clock times across DST. The proposal says so, and it makes any hour effect a lower bound.
- The T-label mechanics (finding 1) mean that a gain over H002 does not show *which* diurnal mechanism is at work. It shows only that the time of day carries signal.

That is enough for a Tier 0 reference.

## Novelty Relative to Existing Research

- The journal is empty.
- Brief §11 names this baseline.
- It is unchanged in substance since `866b902`.
- It is not redundant.

## Experimental Isolation

Clean with respect to H002: the same estimator (median), the same fallback chain, and one added key. The ablation (H002) is the right one, and criterion 4 ("H003 passes criteria 1–2 against H002") follows directly from the isolation.

## Validation Quality

**Folds and criteria.**
- The frozen folds are used unchanged. S1 is a required WIN, and the twins are scored.
- The tail rule is pre-registered with no tail mechanism, so a tail share ≥ 0.5 fails criterion 4. That is appropriate for an hour key.

**DST against the folds.**
- In 2025, daylight saving ran from 30 March to 26 October at 9 of the 10 airports. LTFM stays at UTC+3 all year.
- **W1** validates February (standard time) but trains mainly on DST months (April to October), so its UTC-hour cells are offset by an hour from February's local banks.
- **W1c** trains on January (standard time) only and has no offset.
- **S1** (July, DST) trains on a mixture of about five DST months and four standard-time months.

This is informative rather than a defect: the real January 2026 test is trained on all of 2025, mostly DST, so W1 reproduces the blur the test will face. Report the W1-versus-W1c contrast next to the pre-registered S1c and W1c signs.

**W1c coverage.** W1c trains on January only (153,706 DEP rows; at least 9,735 per airport). Night cells will fall back to the airport median, as pre-registered.

**Batch conditions B1–B4** (defined in full in `H001_review_v1.md`) apply:
- B1: criteria 5, 7 and 8 also apply.
- B2: a falsified candidate is not promoted.
- B3: an S1 WIN with an S1c point dRMSE ≥ 0 is an unresolved objection.
- B4: row-concentration reporting (standing rule 6).

## Leakage Review

### Target Leakage

PASS

The medians come from the fold's training DEP targets. `_split` asserts that validation targets are null.

### Temporal Leakage

PASS

- **Admissibility.** The takeoff hour (label T) is known at the prediction timestamp defined in §6.2.
- **Forward exposure.** In S1 and W1 it comes from the frozen design and is handled by standing rule 2 and condition B3. The LFPG runway-regime months (August to November) shift LFPG's hourly medians in S1's training data.

### Competition Availability

PASS

`MVT_TIME_UTC_mvt` and `ADEP_mvt` are complete in ranking.

## Compute Review

### RAM

PASS

- **Measured here.** The FS0 build peaks at 3.45 GB on fold H, which is the largest training fold (1,919,370 rows), not S1.
- **Expected in the worker.** About 3.5–3.7 GB, within CLASS-S (4 GB).

### Runtime

PASS

Under 1 minute.

### Disk

PASS

About 10 MB.

## Weakest Assumption

The assumption is that a UTC-hour key captures a diurnal effect large enough to WIN on at least three development folds, including S1, despite:
- the DST offset on W1 and the DST mixture on S1;
- the heavy July tail on S1.

S1 and W1 are the folds most likely to come out TIE.

## Missing Control or Ablation

None required. An alternative key would separate the diurnal-demand mechanism from the T-label mechanics:
- a local-time hour; or
- a P-labelled hour, such as the hour of the off-block proxy.

That belongs to Day 2 (static and temporal structure), not to this baseline.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Primary run.** One primary run:
  1. `uv run python scripts/gate.py allocate H003 v1`.
  2. Write the config exactly as in the Implementation Plan: `model: airport_hour_median`, `feature_set: FS0`, `params: {min_cell: 30}`, `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-S`.
  3. Run `uv run python scripts/run_experiment.py E###`.
- **Comparisons.**
  - Against its ablation: `scripts/compare.py <H003> <H002>`.
  - Against the current champion, if that differs from H002.
  - Both with the B4 figures.
- **Reproduction, only if H003 passes criteria 1–3 against the current champion.**
  1. `gate.py allocate H003 v1 --purpose reproduction` (seed 43).
  2. `scripts/reproduce_check.py <repro> <primary> --champion <champion>`.
- **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun` is permitted and must be logged.
- **Not authorized:**
  - any change to `min_cell`, the key or the time zone (that needs `H003_v2`);
  - scoring H.

Required acknowledgement path: `research/day-01/acks/H003_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It should record finding 1 (the T-label mechanics as an alternative explanation).
- It should adopt conditions B1–B4.

## Revision

None required.

## Advisor Prediction

Probability of improvement: P = 0.65 that H003 passes criteria 1–3 against H002.

Expected magnitude: the development-fold mean dRMSE against H002 is −5 to −15 s (−1 to −3 %). The largest gains should be at hub airports and in the `high` traffic regime. W1c should gain more than W1, because of the DST offset.

Primary expected failure mode: fewer than three development-fold WINs. W1 (DST-offset cells) and S1 (tail-dominated interval) are the folds most likely to come out TIE.
