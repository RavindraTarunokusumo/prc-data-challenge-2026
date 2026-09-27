---
schema: advisor-review-v1
hypothesis_id: H005
proposal_version: 1
proposal_sha256: ab97e4312158b0a5c26d6223423539969308daf39ac1807d3c93c6fcf054ff44
exchange_id: X-D01-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-09-27T12:28:35Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**

H005 is the reference that DATASET_AUDIT §6.3 and §7 item 4 require:
- the raw admissible anchor `d_aobt3 = MVT − AOBT_3_flt`;
- a fold-local airport-median fallback for the rows without NM data;
- nothing else fitted.

The falsification criterion (criteria 1–2 against H003) is decisive. The ablation (H002, which is the fallback everywhere) isolates the anchor cleanly.

**Verified here.** The batch-level checks recorded in `H001_review_v1.md` also hold for H005:
- hashes, tests (90 of 90), lint and a clean tree;
- fixed parameters unchanged since `866b902`.

`anchor_aobt3` coalesces `d_aobt3`, then the training airport median, then the training global median. `d_aobt3` is null exactly when `AOBT_3_flt` is null, so every prediction is finite.

**The main finding: the unguarded anchor has target-free extremes that can decide single folds.** All counts below come from covariates only. No target was read, and December was excluded throughout.

1. **A day-scale anchor sits in S1's validation month.**
   - Exactly one DEP row in January–November 2025 has `d_aobt3 ≥ 20,000 s`. It is at LIRF, in July 2025, which is the validation month of S1 and S1c. It is also in the training data of R1–R3 and H.
   - Its `d_aobt3` is 87,181 s. `EOBT_1`, `SCHED`, `LOBT` and `IOBT` are all about 87,001 s before its takeoff. The flight took off about 24 h late, and NM recorded its off-block on the original day.
   - The ranking month July 2026 has one row with the same pattern (LIRF, 86,340 s).
   - No S1 training month contains any `d_aobt3 ≥ 20,000 s`.

   H005 will predict about 87,000 s for this row. That prediction is nearly exact if the recorded block time is also on the original day. It is off by about 86,000 s if the block time is on the departure day. I did not read the target.
2. **Negative anchors.** Some validation-month rows have `d_aobt3 < −600 s`, and H005 will predict those negative taxi times as they are:

   | Month | Rows below −600 s | Minimum (s) |
   |---|---|---|
   | Jul 2025 | 117 | −10,851 |
   | Sep 2025 | 86 | −11,521 |
   | Oct 2025 | 49 | −8,999 |
   | Nov 2025 | 23 | −8,275 |
   | Feb 2025 | 15 | −5,522 |

3. **January 2026 has an anchor tail no fold reproduces.**
   - In January 2026, 0.375 % of DEP rows (564) have `d_aobt3 ≥ 3,600 s`. That is 2.9 times the highest 2025 month; the 2025 months range from 0.067 % to 0.132 %.
   - 342 of the 564 are at EHAM, concentrated on 3–9 January, and 79 are at LFPG. That concentration points to an event cluster rather than a pipeline shift. The 2025 monthly anchor medians are 926–965 s, against 1,001 s in January 2026.
   - July 2026 (0.181 %) resembles July 2025 (0.132 %).

**Effect on H005's own test.**
- **S1.** On S1 (190,713 rows), an error of about 86,000 s on one row adds about 3.9 × 10⁴ s² to the MSE, i.e. +40–45 s of RMSE at a base of about 400 s. The anchor's expected advantage over H003 on S1 is roughly 150–250 s. Even with the row's cluster drawn three times in the bootstrap, the S1 WIN against H003 holds either way.
- **Chain comparisons.** The same row decides a large part of every later comparison between H005 and a bounded model (H004, H006, H007). See those reviews. This makes H005 a plausible Day 1 champion for a reason unrelated to its bulk accuracy.

## Scientific Validity

**Mechanism.** It is correct as a measurement argument: the anchor's error is exactly `BLOCK − AOBT_3`. The audit puts its median at +51 s, so the anchor over-predicts at the median, with an IQR of −122 to +183 s.

**Tail share.** The pre-registered expectation that the tail share of the SSE change against H003 stays below 0.5 is uncertain.
- The audit implies that the anchor removes a large part of the constant model's extreme-tail SSE:
  - Under the constant mean, the top 0.1 % of rows carry 46.6 % of the SSE, about 1.39 × 10⁵ s² of the 2.99 × 10⁵ s² MSE.
  - The anchor's total MSE is 1.48 × 10⁵ s².
  - Its errors on the other 99.9 % of rows (IQR about 305 s; 1–99 % range −1,194 to +803 s) plausibly account for at least about 4 × 10⁴ s². This is an estimate, not a strict bound.
  - If so, the anchor removes at least about a quarter of that tail SSE.
- A tail share of 0.3–0.6 is plausible. If it reaches 0.5 or more, criterion 4 rests on the pre-registered tail mechanism (long holds after NM's off-block).
- The B4 figures must then show whether the tail gain is broad, or carried by a few physically implausible records such as the day-scale row.

**Alternative explanation.** The proposal notes that NM's AOBT may embed its own taxi model. That is fair, and it does not affect admissibility.

## Novelty Relative to Existing Research

- The journal is empty.
- The audit explicitly calls for this reference.
- It duplicates no other work and is unchanged since `866b902`.

## Experimental Isolation

Clean. H005 against H002 changes only the prediction on rows with an anchor: the anchor instead of the airport median. The fallback is identical. The chain comparison against H003 is also valid, but it changes more than one thing (the anchor, and the hour key being dropped). That is why H002 is the right mechanism ablation.

## Validation Quality

**Folds.** The frozen folds are used unchanged, S1 is a required WIN, the twins are scored, and H is predicted only.

**Forward exposure.** H005's S1 and S1c predictions are identical except for the fallback rows (about 2 % in July 2025). The twin contrast will therefore mostly measure the comparator. The pre-registered sign (S1c < 0 against H003) is right.

**Validation limit.** No development fold reproduces January 2026's anchor-tail density. W1 (February 2025) has 0.067 %. The fold results will understate how much the treatment of large anchors matters in January.

**Batch conditions B1–B4** (defined in full in `H001_review_v1.md`) apply. B4 (row concentration) is essential for H005: it is the only model in the batch whose predictions are unbounded.

## Leakage Review

### Target Leakage

PASS

- **Not a copy of the target.** `AOBT_3_flt` is not a copy of the withheld block time (§6.3: within 1 s in only 2.0 % or 0.5 % of rows). It is a strong admissible proxy, not a leak.
- **Fallback.** The fallback medians come from training rows only.

### Temporal Leakage

PASS

- **Admissibility.** `d_aobt3` is labelled T and is admissible under §6.2.
- **Forward exposure.** The model is not regime-sensitive, apart from the 1–2 % fallback.

### Competition Availability

PASS

`AOBT_3_flt` is present for 98.4 % (January 2026) and 98.5 % (July 2026) of ranking DEP rows; the rest use the fallback.

## Compute Review

### RAM

PASS

The FS0 build was measured here at 3.45 GB on fold H, the largest training fold (not S1). Expect about 3.5–3.7 GB in the worker, within CLASS-S (4 GB).

### Runtime

PASS

Under 1 minute.

### Disk

PASS

About 10 MB.

## Weakest Assumption

The assumption is that the anchor's error, `BLOCK − AOBT_3`, is well behaved on the validation months. It is not guaranteed: day-scale and multi-hour negative anchors exist in S1's validation month and in the July 2026 test month. Whether the target echoes them is unknown. That single fact may decide which model family is the Day 1 champion.

## Missing Control or Ablation

- The mechanism ablation (H002) is adequate.
- The missing control is batch condition B4 (row concentration, standing rule 6). Standing rule 1 splits rows by the target. If the day-scale row's target is ordinary, H005's error on it falls in the **bulk**, and the tail/bulk split alone would misattribute it.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Primary run.** One primary run:
  1. `uv run python scripts/gate.py allocate H005 v1`.
  2. Write the config exactly as in the Implementation Plan: `model: anchor_aobt3`, `feature_set: FS0`, `params: {}`, `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-S`.
  3. Run `uv run python scripts/run_experiment.py E###`.
- **Comparisons.** Each with the B4 figures, and for the day-scale LIRF row its target and both predictions:
  - against H003 (falsification);
  - against H002 (ablation);
  - against the current champion.
- **Reproduction, only if H005 passes criteria 1–3 against the current champion.**
  1. `gate.py allocate H005 v1 --purpose reproduction` (seed 43; deterministic, so the predictions should be identical).
  2. `scripts/reproduce_check.py <repro> <primary> --champion <champion>`.
- **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun` is permitted and must be logged.
- **Not authorized:**
  - any guard, clip or cap on the anchor (that is a modelling change and needs a new version or hypothesis);
  - scoring H.

Required acknowledgement path: `research/day-01/acks/H005_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It should record the three target-free findings above.
- It should adopt conditions B1–B4.

## Revision

None required.

## Advisor Prediction

Probability of improvement: P = 0.90 that H005 passes criteria 1–3 against H003. P = 0.97 that it passes criteria 1–2 against H002.

Expected magnitude: development-fold mean RMSE of 380–450 s, about 15–30 % below H003. S1 carries a ±40–45 s swing from the single day-scale LIRF row. Tail share of the margin over H003: 0.3–0.6, so P ≈ 0.4 that it is ≥ 0.5.

Primary expected failure mode: not a failure of criteria 1–3. The failure mode is attribution. H005's standing in the chain, and P ≈ 0.45 that it ends Day 1 as champion, may rest on one July 2025 row whose recorded block time decides whether the unguarded anchor is exactly right or wrong by a day.
