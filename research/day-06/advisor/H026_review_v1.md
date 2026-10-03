---
schema: advisor-review-v1
hypothesis_id: H026
proposal_version: 1
proposal_sha256: dbcef1904ffc6ce28c70fecdf6f57d1ebe7323c806707a9ed507e85eebfdcd71
exchange_id: X-D06-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.85
created_utc: 2026-10-02T17:45:27Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.85).**

- **H026 is the batch's most decisive rung.** It is the control H023 v3 named and did not run (revision 6). `H023_review_v3.md` listed it under Missing Control and excluded it from that chain's authorization (item 6). It costs no training: E029 and E030 are COMPLETE, and 16 of 16 of their prediction files match their manifests.
- **Its own design is sound.**
- **It adopts H024 §Batch unchanged.** So it carries §Batch revisions 1, 3, 4, 5, 6 and 7 of `H024_review_v1.md`, and the binding ruling there, plus:
  - **(a) The mechanism wording.** Its Research Question and Mechanism attribute "ordered boosting" to CatBoost's learner. E030 runs `boosting_type: Plain` (resolved `Plain`, `bootstrap_type: Bayesian`, `random_strength: 1`). What rung B keeps is oblivious trees with plain boosting and Bayesian bootstrap, on FS2_RAW integer codes (revision 4).
  - **(b) The pointer and the reading probabilities.** Point at the revised §Batch. Restate "part" P 0.55, "carries" P 0.25, INCONCLUSIVE P 0.20 under the bounded "carries" rule.

## Scientific Validity

### (a) What rung B decides

- **The question.** Rung B decides whether Day 5 finding 1 explains E033's gain at E033's construction. Finding 1 is "within CatBoost at fixed capacity, the categorical statistics carry signal" (−4.91 s on the population).
- **If rung B carries the gain:** finding 1 stays true within CatBoost but does not explain the champion's margin.
- **If it does not:** the statistics carry part of the gain at equal weight.

### (b) The scope is "at equal weight"

- **The weight penalises a weaker second half.** A fixed 0.5 weight costs a less accurate component more than its best weight would. E030 is +4.05 s against E029 on all rows.
- **So a LOSS has a precise meaning:** "at E033's construction, the codes CatBoost is no substitute". That includes its weaker accuracy, as Alternative explanation 1 says.
- **This is the right question for attributing E033, and the reading should say so.** Revision 5 (the diversity diagnostic on the readings' population) and the recommended ambiguity decomposition separate the accuracy channel from the disagreement channel.

### (c) The pre-registration can be checked only by attestation

- **H026's outcome is a deterministic function of existing artifacts:** E029's and E030's stored predictions, plus development truth.
- **The repository shows no E029/E030 blend, ambiguity or residual-correlation figure.** Searched: `research/`, the E030 and E031 analyses, the journal and the Day 5 eda.
- **The acknowledgement should attest that none was computed before the run.** That keeps the pre-registered expectations meaningful. Non-blocking.

### (d) The direction is credible

- **CTR statistics are target-driven,** as are LightGBM's gradient-sorted categorical splits. Integer codes are not.
- **So E030 may disagree with E029 at least as much as E031 does.** That would partly offset its accuracy deficit.
- **This is why "carries" is not negligible,** and why its reading must be bounded (revision 1).

## Novelty Relative to Existing Research

- **New as an experiment.** The named control was never run.
- **Not redundant:** E030 was a within-CatBoost control, never blended.

## Experimental Isolation

- **Against E033:** E030 and E031 differ only in `cat_mode`, inside H022 v3's closed exempt set (`cat_mode`, `n_cat_features`, `data_partition`). Each is one GPU draw.
- **E030's re-draw is unmeasured.** The proxy is the blend re-draw, +0.26 s on the 5-fold mean and +1.28 s on W1 (revision 3).

## Validation Quality

- **D(H026) is a direct paired comparison against E033,** on the frozen folds.
- **There is no gating** beyond allocation (E030 is COMPLETE).
- **Rule 12 band disclosure** of E030's < 1 h band (25, against 86 and 82) is planned.
- **The gaps are the §Batch ones.**

## Leakage Review

### Target Leakage

PASS

The blend adds no input. It reads manifest-verified predictions only, and its weight is fixed a priori.

### Temporal Leakage

CONCERN

Inherited and not blocking: FS2's T features in E029, FS2_RAW in E030, and post-validation training months in S1 and W1. The twins bound them.

### Competition Availability

PASS

Both components can predict SUBMIT_JAN and SUBMIT_JUL.

## Compute Review

### RAM

PASS

About 3.4 GB, inside CLASS-S's 4 GB.

### Runtime

PASS

About 8–60 s.

### Disk

PASS

About 60 MB.

## Weakest Assumption

**That E030's single GPU draw represents the codes arm.** Its re-draw was never measured; only E031's was.

## Missing Control or Ablation

- **None beyond the brackets** E029 and E033.
- **The within-CatBoost contrast** (E031 against E030, Day 5) supplies the scale.

## Decision

REVISE

## Execution Authorization

Authorized scope:
- **None.** REVISE never permits execution.

Required acknowledgement path:
- None for v1.
- After an ACCEPT of v2, it is `research/day-06/acks/H026_ack_v2.md`.

## Revision

**Required.**
1. **The §Batch revisions** 1, 3, 4, 5, 6 and 7 of `H024_review_v1.md`, through a pointer to the revised §Batch.
2. **Plain boosting.** Replace "ordered boosting" in the Research Question and Mechanism with plain boosting, Bayesian bootstrap and oblivious trees on FS2_RAW codes.
3. **Restated reading probabilities** under the bounded "carries" rule.
4. **Scope.** State that the reading is at equal weight (Scientific Validity (b)).

**Requested in the acknowledgement (non-blocking):** the attestation of Scientific Validity (c).

**Binding:** the ruling in `H024_review_v1.md`.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| G(H026) < 0 (the codes blend beats E029 on the population; point) | 0.93 |
| "Statistics carry part" (D ≥ +1.0 s and LOSS on ≥ 3 development folds) | 0.60 |
| v1 "carries the gain" (D < +1.0 s; point) | 0.20 |
| Bounded "carries" (bootstrap q95 of D's mean < +1.0 s) | 0.08 |
| H026 − E029 < 0 on all rows | 0.85 |
| Route check passes | 0.99 |

Expected magnitude:
- **On `NM_present_excl_LIRF`:**
  - G(H026): −0.8 to −3.0 s (central −1.9);
  - **D(H026): +0.9 to +3.2 s (central +2.05).**
- **All rows:**
  - H026 − E029: −0.3 to −2.6 s (central −1.4);
  - H026 − E033: +1.0 to +3.3 s.
- **Residual correlation, E029 against E030, bulk rows:** 0.83–0.92 (central 0.88; E031: 0.84–0.92).

Primary expected failure mode:
- **"Part" is met, but mostly through E030's accuracy deficit.** Its disagreement with E029 is about E031's.
- **The reading is right as an attribution of the ingredient at equal weight.** Without the population-matched diagnostic it would be read too strongly, as "the statistics decorrelate".
