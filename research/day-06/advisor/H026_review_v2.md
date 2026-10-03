---
schema: advisor-review-v1
hypothesis_id: H026
proposal_version: 2
proposal_sha256: a4a9ae5000626b1eb92b110ddb4a0f6d3813729b012b8a89352cf78ebc5d6bbc
exchange_id: X-D06-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.90
created_utc: 2026-10-02T18:08:13Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.90).** Delta review against `H026_review_v1.md`.

**All four required items are met:**

| v1 item | v2 |
|---|---|
| 1. §Batch revisions 1, 3, 4, 5, 6, 7 | Through the pointer to `H024_v2.md` §Batch |
| 2. Plain boosting | The Research Question and Mechanism now read: oblivious trees, plain boosting, Bayesian bootstrap (`boosting_type: Plain`, `bootstrap_type: Bayesian`), on FS2_RAW integer codes. No "ordered" remains in H026 v2 |
| 3. Reading probabilities | Restated under the bounded rule: "part" 0.60, "carries" 0.12, INCONCLUSIVE 0.28 |
| 4. Scope | "At equal weight" is stated in the Research Question and the Falsification Criterion. A LOSS includes E030's weaker accuracy. The decomposition is reported "for the record" and does not change the reading |

- **The attestation I recommended is now planned in the acknowledgement:** no E029 + E030 blend, ambiguity or residual-correlation figure was computed before the run.
  - The repository still holds no such figure. There are no E035+ comparisons, and `research/comparisons/` has no E030-blend file.
- **Rung B is the batch's most decisive rung, and now runs first (E035).**
  - It needs no training and has no dependency.
  - Both components are COMPLETE, and all 16 of their prediction files match their manifests.
  - E030's route check passes on all 8 folds.
- **Conditions C1–C7 of `H024_review_v2.md` apply.**

## Scientific Validity

- **What rung B decides.** At E033's construction (equal weight), rung B shows whether Day 5 finding 1, "the categorical statistics carry signal within CatBoost", explains the champion's margin.
  - **"Part" (likely):** at equal weight, the codes CatBoost is no substitute. Removing the statistics, which also costs E030 its accuracy, loses part of the gain.
  - **"Carries" (unlikely):** finding 1 stays true within CatBoost but does not explain E033. C5 then requires "a substitute within the 1.0 s bound".
- **The decomposition is the right companion.** MSE_blend = ½ MSE₁ + ½ MSE₂ − ¼ mean((p₁ − p₂)²) is an identity on the same rows. It separates E030's accuracy channel from its disagreement channel, which is exactly the over-reading risk named in v1 ("the statistics decorrelate").
- **The scope is stated correctly.** E030 and E031 differ only in `cat_mode` inside H022 v3's closed comparability set (`resolved_params_E031_vs_E030.json`: `cat_mode`, `data_partition` and `n_cat_features` differ; nothing outside the set). So at equal weight, "the statistics" and "the statistics plus the accuracy they buy" are the same ingredient.

## Novelty Relative to Existing Research

New as an experiment. This is the control named in `H023_review_v3.md` and never run. E030 was a within-CatBoost control and was never blended.

## Experimental Isolation

- **Against E033:** the second half's `cat_mode` (inside the closed set), plus the difference between E030's and E031's GPU draws.
- **E030's re-draw has never been measured.** The proxy is the blend re-draw, +0.26 s on the mean and +1.28 s on W1. The expected D (about +2 s) is far enough from both thresholds that one draw is unlikely to decide the reading.

## Validation Quality

- **D(H026) is a direct paired comparison against E033,** on the frozen folds with the frozen bootstrap.
- **No gating** beyond allocation is needed (E029 and E030 are COMPLETE).
- **Rule 12 band disclosure** is planned: E030's < 1 h band is 25, against E031's 86.
- **The integrity clause** runs through `route_check.py E035 - E029`.

## Leakage Review

### Target Leakage

PASS

There is no new input. The blend reads manifest-verified predictions only, and its weights are fixed a priori.

### Temporal Leakage

CONCERN

Inherited and not blocking: FS2's T features (E029), FS2_RAW (E030), and post-validation training months in S1 and W1. S1c and W1c bound them.

### Competition Availability

PASS

Both components predict SUBMIT_JAN and SUBMIT_JUL.

## Compute Review

### RAM

PASS

About 3.4 GB, inside CLASS-S's 4 GB.

### Runtime

PASS

About 8–60 s. The CLASS-S timeout is 450 s.

### Disk

PASS

About 60 MB.

## Weakest Assumption

**That E030's single GPU draw represents the codes arm.**
- Its re-draw is unmeasured.
- A large draw effect would be needed to move D from about +2 s across either threshold.

## Missing Control or Ablation

- **None beyond the brackets** E029 and E033.
- **The within-CatBoost contrast** (E031 against E030: −4.915 s, q95 −4.283) gives the scale.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Exactly one allocation,** `uv run python scripts/gate.py allocate H026 v2` (purpose `primary`).
  - It is made **first** in the batch, so it is expected to be **E035**.
  - The config is the Proposed Change block: components [E029, E030], weights [0.5, 0.5], seed 42, CLASS-S, all 8 folds.
- **It runs first in the INC-0012 window by the pinned launcher,** or at a later window under C3 of `H024_review_v2.md`.
- **The reading is the §Batch rung reading on D(H026), at equal weight,** worded under C5. It is a disclosure only: no candidate, no holdout access.
- **The acknowledgement must carry the attestation** that no E029 + E030 blend, ambiguity or residual-correlation figure was computed before the run.
- **Conditions C1–C7 of `H024_review_v2.md` apply.**

Required acknowledgement path:
- `research/day-06/acks/H026_ack_v2.md`, referencing the proposal hash `a4a9ae5000626b1eb92b110ddb4a0f6d3813729b012b8a89352cf78ebc5d6bbc` and this review's hash.

## Revision

None required.

## Advisor Prediction

Probability of improvement:

| Event (H026 = E035) | P |
|---|---|
| G(H026) < 0 (the codes blend beats E029 on the population; point) | 0.94 |
| "Statistics carry part" (D ≥ +1.0 s and LOSS on ≥ 3 development folds) | 0.72 |
| Bounded "rung B carries the gain" (q95 of D's mean < +1.0 s) | 0.05 |
| INCONCLUSIVE | 0.23 |
| H026 − E029 < 0 on all rows | 0.88 |
| Runs in today's window | 0.98 |
| Route check passes | 0.99 |

Expected magnitude:
- **On `NM_present_excl_LIRF`:**
  - G(H026): −0.7 to −3.0 s (central −1.85);
  - **D(H026): +0.95 to +3.25 s (central +2.1); q95 − mean about 0.3 s.**
- **All rows:**
  - H026 − E029: −0.3 to −2.6 s (central −1.4);
  - H026 − E033: +1.0 to +3.3 s.
- **Residual correlation, E029 against E030:** bulk 0.83–0.92 (central 0.88), and about the same on `NM_present_excl_LIRF`.
- **Decomposition:** E030's disagreement term is within ±25 % of E031's. Its accuracy term is clearly worse.

Primary expected failure mode:
- **"Part" is met, mostly through E030's accuracy deficit,** with a disagreement close to E031's.
- **The reading is correct as stated, at equal weight.** The decomposition stops the record from turning it into "the statistics decorrelate the halves".
