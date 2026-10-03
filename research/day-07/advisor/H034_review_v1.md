---
schema: advisor-review-v1
hypothesis_id: H034
proposal_version: 1
proposal_sha256: 2ccb7401113d8f4dad356978d95720cae08cd47e1f7c30dada5fa3f0b070a62f
exchange_id: X-D07-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.90
created_utc: 2026-10-03T20:50:26Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.90).** The shared findings and binding conditions U1–U10 are in `H035_review_v1.md` and apply here unchanged. **U1 (order and ids), U5 (status) and U10 (deferral and reruns) bear most directly on this proposal.**

**What H034 is.** It re-runs E020's configuration (H016 v2: deterministic LightGBM on FS2, unrouted) on the laptop. It has two roles:
- **E045** supplies H035's subgroup predictions;
- **E047**, a seed-43 reproduction, is H035's criterion 6 component.

It is a component, not a candidate.

**Verified here.**
- The proposal hash matches the envelope.
- **Parsed-YAML comparison:** `params`, `model`, `feature_set`, `folds`, `seed` and `job_class` equal `experiments/E020/config.yaml` exactly. Only `hypothesis_id` and `proposal_version` differ, as stated.
- **A laptop instance is needed.** E020's prediction files are absent on the laptop (stored predictions begin at E025).
- **The seed is inert, so E047 should be byte-identical to E045:**
  - `prc.models.gbm.lightgbm` sets `deterministic=True` and `force_row_wise=True`;
  - bagging and feature fractions are 1.0;
  - `bin_construct_sample_cnt` (5,000,000) exceeds every fold's training rows (largest: H, 1,919,370);
  - Day 3 found byte identity across seeds, restarts and two CPU strings (E022 against E019; D3-C4).
- **Cloud to laptop.**
  - Rule L v2 found laptop runs equal to the cloud except on the routed ridge rows, where polars' thread pool changes the last bits.
  - The closest evidence is E026, E019's laptop instance. Its LightGBM is E020's fit: the same configuration on the same training rows, because routing acts only at prediction. E026 equals the cloud off the routed rows.
  - E045 has no ridge, so identity with E020 on every row is expected.

**One reading to strengthen** (non-blocking).
- Identity with E020 can only be read from metrics, because no E020 file is on the laptop.
- `rmse_by_fold` alone is seven numbers. `experiments/E020/metrics.json` also holds every RMSE and bias by airport, airport bulk, month, traffic regime and wake class on each scored fold.
- The E045 analysis should compare the whole `scores` block key by key, not only the fold RMSEs. Any difference above 0.01 s is reported as a rule L v2 boundary event.

## Scientific Validity

- **A reproduction of a recorded configuration, with no mechanism claimed.**
- **Its falsification rule is adequate for a component.**
  - A per-fold difference above 1.0 s from E020 is disclosed, and it blocks H035's derivation table.
  - It does not block H035's readings, which use E045 directly.
- **The subgroup is where a silent difference would matter.** E045's subgroup rows carry H035's whole contrast, and they are the day-scale records a procedural change moves most (`H013_review_v2.md`).
- **The scores-block comparison above is the check.**

## Novelty Relative to Existing Research

- **Not a new experiment in substance:** it is E020's configuration on the current environment.
- **Rule 10 is not engaged,** because H034 is not a candidate.
- **Rule 10 bars E020's configuration and its backend-only re-draws as candidates** (X-D04-S02-0001 (e)). E045 and E047 are such re-draws, and U5 binds them.

## Experimental Isolation

- Against E020, only the environment differs (rule L v2 item 6). The configuration and silver are unchanged.
- E047 differs from E045 only in `purpose` and `seed`.

## Validation Quality

- **Folds.** The frozen folds are used unchanged: seven scored folds and H, with H predicted only.
- **Readings:**
  - E045's `scores` against E020's;
  - E047's eight prediction-file SHA-256s against E045's, from the two manifests.
- **No comparison against the champion is a reading of H034** (U5).

## Leakage Review

### Target Leakage

PASS

As H016 v2, reviewed on Day 3:
- training rows of each fold only, with validation targets masked;
- no target statistics.

### Temporal Leakage

CONCERN

Label notes, as H016 v2; not blocking.
- `d_sched`, the in-taxi counts and the SCHED-anchored windows are T.
- The convention channel is admissible and lies outside the causal-only variant (rule 8).

### Competition Availability

PASS

Every FS2 input is present for ranking DEP rows (DATASET_AUDIT §6). H034 itself predicts no ranking month.

## Compute Review

### RAM

PASS

- E029 (the same learner and frame on the laptop, plus a ridge) peaked at 6.60 GB.
- E020 peaked at 4.62 GB in the cloud; the laptop's 16-thread polars pool raises the peak.
- Expected 6.3–6.8 GB, under CLASS-M's 8 GB.

### Runtime

PASS

- E029 took 893 s. Expected 850–1,000 s, plus about 100 s of W&B sync if the mirror fails, as in the first window.
- The 1,100 s guard governs only the start. The CLASS-M timeout is 2,700 s.

### Disk

PASS

About 60 MB of predictions per run, covered by the manifests.

## Weakest Assumption

**That the laptop reproduces E020 on every row, the subgroup included.**
- The evidence is strong. E026 fits E020's LightGBM on the laptop and equals the cloud off the routed rows.
- But E026's subgroup outputs were replaced by the ridge. The unrouted fit's predictions on the subgroup, which carry H035's whole contrast, have not yet been observed on the laptop.

## Missing Control or Ablation

None required. The scores-block comparison (Summary) is the check to report.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

**Allocations:**
- exactly one `primary` allocation, `uv run python scripts/gate.py allocate H034 v1`, made first in the batch (expected **E045**);
- exactly one `uv run python scripts/gate.py allocate H034 v1 --purpose reproduction`, made third (expected **E047**).

Both follow U1's order and id rule.

**Config:**
- E045: the Proposed Change block.
- E047: identical except `purpose: reproduction` and `seed: 43`.

**When:** first and third in the queue of the pinned `research/day-07/sessions/D07-S01/run_window_2.sh`, in the 2026-10-04 00:00–01:00Z window (INC-0015), or later under U10.

**Readings:**
- E045's `scores` against `experiments/E020/metrics.json`;
- E047's prediction-file SHA-256s against E045's.

**Status (U5):**
- not a candidate, and never NEW, in any phase;
- no `compare.py`, `mechanism_check.py` or `holdout_check.py` run with E045 or E047 as the candidate.

**Not authorized:** any other allocation, and any change to the configuration.

Required acknowledgement path: `research/day-07/acks/H034_ack_v1.md`.
- It references the proposal hash `2ccb7401113d8f4dad356978d95720cae08cd47e1f7c30dada5fa3f0b070a62f` and this review's hash.
- It adopts U1–U10 of `H035_review_v1.md` as binding.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement: not applicable. This is a reproduction, and no candidate claim is made.

| Event | P |
|---|---|
| E045 COMPLETE within CLASS-M | 0.97 |
| E045 equals E020 within 0.01 s on every fold RMSE | 0.92 |
| … within 1.0 s on every fold (the frozen tolerance) | 0.97 |
| E047's eight prediction files byte-identical to E045's | 0.95 |

Expected magnitude:
- **Fold RMSE as E020:** R1 284.67, R2 248.97, R3 300.02, S1 420.73, W1 355.37, S1c 440.87, W1c 441.90; development mean 321.95 s.
- **Resources:** runtime 850–1,000 s; peak RSS 6.4–6.8 GB.

Primary expected failure mode:
- **Primary:** an undetected environment difference moves only the day-scale subgroup predictions. The fold RMSEs then differ from E020's by more than 0.01 s, mostly on folds with dominant subgroup rows (W1, W1c, R3). This blocks H035's derivation table, not its readings.
- **Secondary:** E045 runs long enough to defer E049 and E050 (H035 review, Runtime).
