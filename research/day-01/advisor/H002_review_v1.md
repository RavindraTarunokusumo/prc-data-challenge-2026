---
schema: advisor-review-v1
hypothesis_id: H002
proposal_version: 1
proposal_sha256: 83e85637037e74215694d0656639f9047fe823903a7f2f17758de544d74be77d
exchange_id: X-D01-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.90
created_utc: 2026-09-27T12:27:02Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**

H002 is a valid Tier 0 reference:
- fold-local airport medians computed from training rows only;
- no leakage path;
- the frozen folds, unchanged;
- a decisive falsification criterion (criteria 1–2 against H001).

**Verified here.** The batch-level checks recorded in `H001_review_v1.md` also hold for H002:
- hashes: proposal, frozen files and advisor definition;
- 90 of 90 tests pass and ruff is clean;
- the working tree is clean;
- fixed parameters are unchanged since the first draft at `866b902`.

In `airport_median`, the medians come from `role == 'train'` rows only, and the left join cannot duplicate rows.

**Three findings** (none blocks):
1. **The estimator changes together with the key.** H001 predicts a mean and H002 a median, so the comparison changes two things at once (quantified below). The confound works against H002. A pass therefore supports the airport mechanism; a fail would not refute it.
2. **Criterion 3 is not free.** For airports whose median sits further from their mean than the global mean does, the airport median is worse than the global mean. On the audit's all-year moments this holds for:

   | Airport | RMSE change vs the global mean |
   |---|---|
   | LTFM | +1.1 % |
   | LFPG | +0.8 % |
   | LEBL | +0.6 % |
   | LEMD | +0.2 % |

   All are below the 3 % tolerance, but the gap widens in tail-heavy months.
3. **The forward-exposure rationale is inaccurate for LFPG.** The proposal says "airport offsets are stable across 2025". LFPG's median rose from about 900 s (Jan–Jun) to about 1,013 s (Aug–Nov), per DATASET_AUDIT §6.5 and `regime_stats.json`. The pre-registered sign (S1c < 0) should still hold. The LFPG component of S1 versus S1c will show forward exposure.

## Scientific Validity

**Mechanism.** Airport layout and airport-level queueing are the obvious first factor, and the design tests it directly.

**Size of the confound.** On the audit's all-year airport moments (`audit_stats.json`, pre-freeze aggregates already summarised in DATASET_AUDIT §2), computed in-sample:

| Predictor | RMSE (s) |
|---|---|
| Global mean | 546.4 |
| Airport mean | 514.8 |
| Airport median (H002) | 519.5 |

The median gives up about 4.7 s of a roughly 31.6 s airport effect. On a right-skewed target scored by RMSE, the median is a biased estimate of the conditional mean. LIRF's mean exceeds its median by 170 s, and LTFM's by 90 s.

**Why the design is still acceptable.**
- Brief §11 names the airport *median* as the Tier 0 baseline.
- The bias works against H002, so a pass is conservative evidence for the mechanism.

**What must be recorded.** A failure against H001 would be ambiguous: either no airport signal, or the median penalty. The analysis must say which, using the per-airport `bias` in `metrics.json`.

## Novelty Relative to Existing Research

- The journal is empty.
- Brief §11 names this baseline.
- It duplicates no completed or rejected work.
- It is unchanged in substance since the unsubmitted draft at `866b902`.

## Experimental Isolation

H002 against H001 adds the airport key **and** switches the estimator from mean to median. That is two changes, and the missing control would separate them (see below). For the positive claim ("airport identity explains RMSE"), the confound is conservative, so the isolation is sufficient for promotion. It is not sufficient to quantify the airport effect exactly.

## Validation Quality

**Folds and criteria.**
- The frozen folds are used unchanged. S1 is a required WIN, and the twins are scored.
- The falsification criterion (criteria 1–2 against H001) is decisive and pre-registered.
- The tail rule is pre-registered: with no tail mechanism, criterion 4 fails if the tail share of the SSE change is ≥ 0.5.

**Tail share.** For H002 against H001, the tail share may come out negative:
- Tail rows get worse at airports whose median lies below the global mean (EDDF, EDDM, EHAM, LEBL, LEMD, LFPG, LSZH, LTFM).
- They get better at EGLL and LIRF.

A negative share is still a bulk-driven margin under `scripts/compare.py`'s definition.

**Forward exposure.** The pre-registered S1c and W1c signs (dRMSE < 0 against H001) are the right checks. LFPG's regime shift (finding 3) will favour S1 over S1c for that airport. Report the LFPG row of the S1-versus-S1c contrast.

**Batch conditions B1–B4** (defined in full in `H001_review_v1.md`) apply:
- B1: brief §10 criteria 5, 7 and 8 also apply to the chain.
- B2: a candidate whose own falsification criterion is met is not promoted.
- B3: an S1 WIN together with an S1c point dRMSE ≥ 0 is an unresolved objection under criterion 8.
- B4: row-concentration reporting (standing rule 6).

## Leakage Review

### Target Leakage

PASS

The medians come from the fold's training DEP targets. `_split` asserts that validation targets are null.

### Temporal Leakage

PASS

The key (airport) is known in the ranking file. Post-validation training months in S1 and W1 are frozen design, and standing rule 2 and B3 handle them.

### Competition Availability

PASS

`ADEP_mvt` is complete in ranking. The global fallback is never needed, because every DEP row departs from one of the ten airports.

## Compute Review

### RAM

PASS

The FS0 build was measured here at 3.45 GB on fold H (the largest fold, not S1). Expect about 3.5–3.7 GB in the worker, within CLASS-S (4 GB).

### Runtime

PASS

Under 1 minute.

### Disk

PASS

About 10 MB.

## Weakest Assumption

The assumption is that the airport effect is large enough, on every development fold including tail-heavy S1 (July std 745 s), to clear the median penalty and the airport-day cluster noise. S1's variance is dominated by tail clusters, for example LIRF on 13 and 28 July (`regime_stats.json`), so S1 is the fold most likely to come out TIE.

## Missing Control or Ablation

**Missing control.** A like-for-like estimator control would isolate the airport key: the global median against the airport median, or the global mean against the airport mean.

**Not required**, because the confound is conservative for the claim being promoted. If H002 fails against H001, however, no conclusion about airport signal may be drawn without that control.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Primary run.** One primary run:
  1. `uv run python scripts/gate.py allocate H002 v1`.
  2. Write the config exactly as in the Implementation Plan: `model: airport_median`, `feature_set: FS0`, `params: {}`, `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-S`.
  3. Run `uv run python scripts/run_experiment.py E###`.
- **Comparison.** `uv run python scripts/compare.py <H002 E###> <H001 E###>`, with the B4 row-concentration figures.
- **Reproduction, only if H002 passes criteria 1–3 against H001.**
  1. `gate.py allocate H002 v1 --purpose reproduction` (seed 43, everything else identical).
  2. `scripts/reproduce_check.py <repro> <primary> --champion <H001 E###>`.
- **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun` is permitted and must be logged.
- **Not authorized:**
  - any change to the estimator, key, folds or class (that needs `H002_v2`);
  - scoring H.

Required acknowledgement path: `research/day-01/acks/H002_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It should record findings 1–3 as corrections to the proposal record.
- It should adopt conditions B1–B4.

## Revision

None required.

## Advisor Prediction

Probability of improvement: P = 0.80 that H002 passes criteria 1–3 against H001.

Expected magnitude: the development-fold mean dRMSE against H001 is −20 to −30 s (−3.5 to −5 %). About 4–5 s of the attainable airport gain is lost to using the median.

Primary expected failure mode:
- **Most likely:** S1 comes out TIE because July's tail clusters widen the paired interval, which fails criterion 2 because S1 must WIN.
- **Less likely:** criterion 3 fails at LTFM, whose mean exceeds its median by about 90 s (P ≈ 0.1).
