---
schema: advisor-review-v1
hypothesis_id: H032
proposal_version: 1
proposal_sha256: 139205d4964a47720b9032ad58ef147a7f83821dfa1220fb3f1e3dca2376657c
exchange_id: X-D07-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.83
created_utc: 2026-10-03T17:18:57Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.83).** The shared findings and the binding conditions S1–S9 are in `H031_review_v1.md`. They apply here unchanged. **S5 is specific to this proposal.**

**What H032 is.** E031's configuration fitted on the two final folds: the CatBoost half of the submission.
- **Parsed-YAML comparison:** the `params` block equals `experiments/E031/config.yaml` exactly. Only `hypothesis_id`, `proposal_version` and `folds` differ, as the proposal states.
- Seed 42 and CLASS-L are unchanged from E031.
- The proposal hash matches the envelope.

**Three points are specific to H032.**
1. **The resolved-parameter clause is too lenient (S5).**
   - The proposal discloses only differences "other than those caused by the training set".
   - E031's and E040's resolved parameters are identical on all 8 folds, from W1c (1 training month, about 154,000 DEP rows) to H (11 months, 1,919,370). `data_partition` is FeatureParallel throughout.
   - Training-set size has therefore never changed a resolved key in this configuration.
   - A difference at 12 months is a sanity flag, named key by key, not a footnote. `data_partition` is the key that matters, because it is confounded with E031's advantage (D6-C7).
2. **GPU memory is this batch's main operational risk.** The details are under Compute Review.
3. **E043 is one further draw, and the only stochastic part of the submission.** E043 against E031 differs in two ways at once: the training set (12 months) and GPU run-to-run variation. No twin exists, so neither part can be measured. Records say "one draw of E031's configuration on 12 months" and nothing more (rule 13; N4 of `H029_review_v1.md` carried).

## Scientific Validity

- The SUBMIT fit of the champion's CatBoost half is the procedure STATE names ("SUBMIT predictions will be a further draw, and SUBMIT trains on 12 months").
- No parameter changes. The 1,000-iteration budget stays a standing disclosure, not a reason to change the fit: any change of iterations is a new configuration.
- **The draw record carried into the analysis:**
  - on all rows, the blend spread over three draws is ≤ 0.60 s per development fold;
  - on W1 normal taxis it is 2.00 s;
  - CatBoost alone spreads up to 1.57 s on W1 (D6-C11).

  The submission inherits a draw of this size. It cannot be measured on the ranking months.

## Novelty Relative to Existing Research

- **No SUBMIT fit of E031's configuration exists.** E031, E032 and E040 are development-fold draws, and none is the SUBMIT draw (N4).
- **Rule 10 is not engaged.** This is the champion's own component, not a candidate.

## Experimental Isolation

- **Against E031:** the folds, and with them the training set, are the only change in configuration. GPU run-to-run variation is unavoidable and disclosed.
- **The route check against E042** isolates the routed rows, which take the same fold-local ridge in both halves. E031 matched E029 within tolerance on every development fold.

## Validation Quality

- H031 §Batch's integrity readings apply, with S4.
- **Integrity item 2 is H032's own check:** `route_check.py E043 - E042` must pass on both final folds. It is a cross-check between two runs that share the ridge path, not an external reference (H031 review, Weakest Assumption).
- **S5's comparison** runs before the submission is formatted. Any difference is a flag, not a block.
- **CLASS-L reporting** (as `H021_review_v2.md`):
  - beside `within_class`, state whether E043 also stayed within CLASS-M (≤ 30 min and ≤ 8 GB);
  - disclose any peak RSS above 8 GB and any swap-out.

## Leakage Review

### Target Leakage

PASS

- CatBoost builds its categorical statistics (CTRs) from the training rows only, as in E031. Here those rows are all 2025 DEP rows.
- The predicted month's rows carry a null target into the model frame. Their categorical levels are mapped to the training vocabulary; unseen levels become `__NULL__`.
- No new input is added.

### Temporal Leakage

PASS

- As H031: `masked_view` gives the §6.2 information set, with one ranking month per view.
- The CTR concern about post-validation months (S1, W1) does not arise, because every training month precedes both ranking months.

### Competition Availability

PASS

FS2_RAW is available at prediction time, as on the development folds. The §6.5 asymmetries are disclosed under S9.

## Compute Review

### RAM

PASS

- Peak RSS was 7.01 GB for E031 and 7.13 GB for E040 over 8 folds.
- With +8.6 % training rows, the expected peak is 7.1–7.7 GB. That is under CLASS-L's 11 GB and probably under 8 GB as well.

### Runtime

PASS

- On the H fold, E031 took 257 s and E040 273 s.
- At 12 months, each fold should take about 280–300 s. Two folds plus loading and curves come to about 9–12 minutes.
- The 1,100 s guard and the 8,100 s CLASS-L timeout are generous.

### Disk

PASS

About 10 MB, covered by manifests.

**GPU memory, the main risk.**
- **Device and external use:** the device has 8,151 MiB. A process outside WSL held 2,864–2,883 MiB at idle on 2026-10-03.
- **CatBoost's own use at `gpu_ram_part` 0.4:**
  - Day 5's calibration measured about 2.9 GB;
  - the device-wide deltas were 3,103 MiB for E031 and 2,872 MiB for E040, both with under 0.9 GB of external use.
- **Expected device-wide peak:** about 5.7–6.4 GB, if external use stays near 2.9 GB.
- **What the record does not settle:**
  - whether CatBoost sizes its pool from total or from free memory;
  - a complexity-4 run has never started with a large external holder (E036, at complexity 1, ran with 5,150 MiB held externally).
- **Why the risk is acceptable:**
  - a GPU memory or device error is classified RESOURCE_FAILURE, and S7's rerun path covers it;
  - GPU memory is re-measured at arming (S2).

## Weakest Assumption

**That the external GPU holder stays near its idle size during the window.**
- On 2026-10-02 the same holder used 4.3–5.2 GB. At that level, a complexity-4 fit's roughly 3 GB may not fit in 8,151 MiB.
- The shared final-fold path (H031 review) is the second assumption.

## Missing Control or Ablation

- None required.
- Named, not required: an E031-configuration twin on the final folds would allow rule 13's draw quantities to be computed. As §Batch says, averaging two draws for submission would be a new configuration (rule 10). The twin would serve as disclosure only, and it is not needed for the submission.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **H032 v1: exactly one `primary` allocation,** `uv run python scripts/gate.py allocate H032 v1`, made second in the batch (expected **E043**).
  - **Config:** the Proposed Change block (folds `SUBMIT_JAN` and `SUBMIT_JUL`, seed 42, CLASS-L, GPU).
  - **When:** second in the queue of the pinned `run_window.sh`, in the 2026-10-03 19:00–20:00Z window, or later under S7.
- **Route check:** `route_check.py E043 - E042`, run by the launcher after E043 is COMPLETE.
- **CLASS-L** stands on H021 v3's accepted justification, unchanged.
- **Status:** not a candidate, never NEW, never scored; no holdout access; ledger decision null.
- **S1–S9 of `H031_review_v1.md` bind this run.** Under S5, the resolved-parameter comparison is H032's.

Required acknowledgement path: `research/day-07/acks/H032_ack_v1.md`. It references the proposal hash `139205d4964a47720b9032ad58ef147a7f83821dfa1220fb3f1e3dca2376657c` and this review's hash, and accepts S1–S9 as binding.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement: not applicable. There is no truth, and nothing is scored.

| Event | P |
|---|---|
| E043 COMPLETE, within CLASS-L, in tonight's window | 0.91 |
| E043 fails on GPU memory or device (RESOURCE_FAILURE) | 0.06 |
| E043 also within CLASS-M (≤ 30 min, ≤ 8 GB) | 0.88 |
| Resolved parameters identical to E031's on both final folds (S5) | 0.95 |
| `route_check.py E043 - E042` PASS on both folds, given both COMPLETE | 0.97 |
| Reading (c), RMS(E042 − E043), above the 205 s flag in either month | 0.03 |

Expected magnitude:
- **Resources:** runtime 540–780 s (central 640 s); peak RSS 7.1–7.7 GB; device-wide GPU peak 5.7–6.4 GB at the idle external level.
- **RMS(E042 − E043):** 2026-01 80–115 s; 2026-07 95–135 s. This is beside H 86.4 s and S1 107.8 s.

Primary expected failure mode:
- A GPU memory failure at the start of training, if the external holder has grown. That is RESOURCE_FAILURE: E044 is deferred, and the rerun follows S7 in another owner window.
