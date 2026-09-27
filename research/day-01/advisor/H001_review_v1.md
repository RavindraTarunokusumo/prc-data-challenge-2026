---
schema: advisor-review-v1
hypothesis_id: H001
proposal_version: 1
proposal_sha256: 38225fb0d6b274cf6904445b2fe0b38de5c2267bee7d140c65e1c07d09dd2d84
exchange_id: X-D01-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.95
created_utc: 2026-09-27T12:26:24Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**

H001 is a correctly specified constant reference:
- one fitted scalar per fold (the mean of the training-row targets);
- no features;
- the frozen folds, unchanged;
- H predicted but not scored.

It is also the incumbent of the pre-registered initial-champion chain and the phase-opening champion of the Day 1 holdout check. Its correctness therefore matters more than its RMSE.

**Verified here.** All checks were read-only. No December target was read, and no model was fitted or scored.
- **Hashes.**
  - The proposal SHA-256 matches the envelope (8 of 8 in this batch).
  - The six frozen files, and the SPLITS v2 proposal, review and ack, match `config/frozen.json`.
  - `.claude/agents/advisor.md` matches `config/agents.yaml`.
  - The working tree is clean at `01b2f2f`.
- **Tests and lint.** `pytest -p no:cacheprovider` passes 90 of 90, and `ruff` is clean.
- **Model and runner code.**
  - `global_mean` uses only rows with `role == 'train'`.
  - `_split` asserts that validation targets are null.
  - The worker predicts H and never evaluates it.
  - `run_experiment.check_config` enforces the seed by purpose (42 or 43) and requires all seven scored folds plus H.
- **Expected values.** They reproduce from the audit's monthly moments (`audit_stats.json`, December not displayed).
  - Validation std: Sep 560.3, Oct 437.1, Nov 532.0, Jul 745.0, Feb 628.3 s.
  - The shift between training and validation means is at most 43 s on every fold. It is largest on S1 and S1c: the July mean is 1,025.7 s against about 983–986 s in training.

**Record defects** (neither blocks):
1. **Stale label.** Controlled Variables calls FS0 "(DATASET_AUDIT §6.2 label: static)". §6.2 defines only the labels P, T and F. The Leakage Analysis section labels the features correctly. The same stale term appears in the docstring of `src/prc/features.py`.
2. **Wrong calibration premise.** The resource estimates rest on "calibration … on the largest fold, S1". That is false for the frozen v2 folds. Counted from `month` with no target read:

   | Fold | Training DEP rows |
   |---|---|
   | R1 | 1,387,414 |
   | R2 | 1,571,364 |
   | R3 | 1,757,038 |
   | S1 | 1,537,475 |
   | W1 | 1,611,189 |
   | S1c | 1,005,519 |
   | W1c | 153,706 |
   | H | 1,919,370 |

   S1 is the fifth largest. H is 24.8 % larger than S1.

## Scientific Validity

Sound as a reference.

The falsification criterion (any fold RMSE more than 40 s above the fold's validation std means INVALID) is a pipeline sanity check. It is loose:
- For a constant predictor, RMSE² = std² + shift².
- At R2's std of 437 s, the criterion tolerates a mean shift of about 190 s.
- The observed shifts are at most 43 s. On R1–R3 and W1, an excess of more than about 3 s over the std would already be surprising.

That is acceptable. The check only has to catch gross defects (wrong fold, wrong join, unit error), and those produce excesses far larger than 40 s.

## Novelty Relative to Existing Research

- The experiment journal is empty. No earlier hypothesis has been reviewed, completed or rejected.
- Brief §11 names the mean baseline explicitly.
- **Drafts.** The drafts committed at `866b902` and `312fb1d` were never submitted.
  - Diffing `866b902..HEAD` shows no change to any fixed parameter or expected result in the batch, only to timestamps and the standing-rule sections.
  - `866b902` is also the resource-calibration commit, and the calibration computes no metric.
  - I found no sign that anything was tuned on scores.

## Experimental Isolation

Not applicable: H001 is a reference. It is the comparator for H002 and for the phase-close holdout check.

## Validation Quality

**Folds.**
- The frozen folds are used unchanged, including S1 (seasonal) and W1 (winter).
- The causal twins are scored.
- H is predicted only.

**Chain.** H001's role is correct. It is the incumbent and never needs promotion. It is also the phase-opening champion for `splits.yaml: phase_close`.

**Batch conditions.** The chain that starts from H001 is governed by the following conditions, which apply to every promotion in H001–H008:
- **B1. Criteria 5, 7 and 8 still apply.** The chain names criteria 1–3, 4 and 6. Brief §10 criteria 5 (no leakage), 7 (resource use within class, i.e. `within_class` in `resource-usage.json`) and 8 (Advisor objections resolved) are also required.
- **B2. A falsified candidate is not promoted.** If a candidate's own pre-registered falsification criterion is met, it is not promoted, even if it passes against the current champion.
- **B3. Standing rule 2 inside the chain.** Suppose a candidate's S1 WIN comes with an S1c point dRMSE ≥ 0 against the same comparator. That is an unresolved Advisor objection (criterion 8), and the candidate is not promoted without a further review.
- **B4. Row concentration (standing rule 6, from this exchange).** Standing rule 1 splits rows by the target. It cannot see a single absurd prediction on a bulk row. Every comparison used for a promotion or a criterion-4 check therefore also reports, per development fold and twin:
  - the share of the fold's SSE change carried by its single largest row, and by its 10 largest rows (ranked by absolute change in squared error);
  - where one row carries ≥ 50 % of a fold's SSE change: that row's `ADEP_mvt`, `d_aobt3`, target and both predictions.

  This is attribution only. It never changes the frozen evaluation population or any fold outcome.

## Leakage Review

### Target Leakage

PASS

The only input is the fold's training DEP targets. Validation targets are null in the masked view, which is tested on real silver for all ten folds.

### Temporal Leakage

PASS

There are no features. The S1 and W1 training means include post-validation months by frozen design. For a constant this is not regime-sensitive, and it moves the prediction by less than 45 s.

### Competition Availability

PASS

Nothing is used except the training target.

## Compute Review

### RAM

PASS

- **Measured here** (read-only: `load_silver` plus `fs0`, no model). In one process, with RSS carried over between folds, the FS0 build peaks at:
  - 2.75 GB on S1;
  - 3.14 GB on R3;
  - 3.45 GB on H.
- **Expected in the worker.** The worker also imports scikit-learn, so expect about 3.5–3.7 GB. That is slightly above the proposal's "< 3.5 GB" but inside the 4 GB CLASS-S target.

### Runtime

PASS

Expected under 1 minute. The CLASS-S timeout is 7.5 minutes.

### Disk

PASS

About 10 MB of predictions, covered by the experiment manifest.

## Weakest Assumption

The assumption is that the runner, the masking and the evaluator behave on real folds exactly as they do in the synthetic tests. H001 is the first real exercise of the whole path.

The per-fold `bias` in `metrics.json` (training mean minus validation mean) is the direct check. It must match the monthly means in the audit to within a few seconds.

## Missing Control or Ablation

None for H001. The missing control at batch level is row concentration (B4).

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Primary run.** One primary run:
  1. `uv run python scripts/gate.py allocate H001 v1`.
  2. Write `experiments/E###/config.yaml` exactly as in the Implementation Plan: `model: global_mean`, `feature_set: FS0`, `params: {}`, `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-S`.
  3. Run `uv run python scripts/run_experiment.py E###`.
- **No reproduction run.** H001 is the incumbent, so the chain needs no reproduction run for it.
- **Uses of its predictions.**
  - As the comparator in `scripts/compare.py`.
  - Once, as the reference in the Day 1 phase-close `scripts/holdout_check.py <final chain champion E###> <H001 E###>`, after the chain completes.
- **Re-run after an infrastructure failure.** One identical re-run is permitted, with `--purpose rerun`, a new E### and nothing changed. It must be logged.
- **Not authorized:**
  - any change to model, features, folds, seed or class (that needs `H001_v2`);
  - scoring H;
  - any read of H truth outside `holdout_check.py`.

Required acknowledgement path: `research/day-01/acks/H001_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It should append the two record corrections above (the "static" label and the S1-largest premise).
- It should adopt conditions B1–B4.

## Revision

None required.

## Advisor Prediction

Probability of improvement: not applicable, because H001 is the reference. P = 0.98 that no fold triggers the INVALID criterion.

Expected magnitude: RMSE of about R1 560, R2 437, R3 532, S1 746, W1 628, S1c 746 and W1c 628 s. Development-fold mean about 581 s (±2 s).

Primary expected failure mode: none scientific. The only plausible failure is an infrastructure defect on the first real run (a join or coverage error). The evaluator's coverage check would surface it as INVALID.
