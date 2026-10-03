---
schema: advisor-review-v1
hypothesis_id: H028
proposal_version: 2
proposal_sha256: 65b8f3fbc816a7bde428c7f39a8c40525dfb1ea4c9595b56444e14d4567d70a2
exchange_id: X-D06-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.87
created_utc: 2026-10-02T18:08:13Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.87).** Delta review against `H028_review_v1.md`.

**The batch's main overclaim is gone.** All three required items are met:

| v1 item | v2 |
|---|---|
| 1. §Batch revisions 1, 2, 3, 5, 6, 7 | Through the pointer to `H024_v2.md` §Batch. Revision 2 is applied here too |
| 2. Research Question and Scientific Value | Rung A measures "the generic-averaging floor at a perturbation twin's disagreement". Only its "carries" outcome would change the record on E033. A LOSS is explicitly "not support for 'a second learner family adds signal'", and "nothing is concluded about learner families" |
| 3. Expected-reading row | Relabelled "the twin does not reproduce the gain (generic-averaging floor at its measured disagreement)", P 0.92. "Carries" is P 0.02 and INCONCLUSIVE P 0.06, under the bounded rule |

- **The gating follows H027 v2.** The runner admits seed 42, so the v1 seed refusal no longer blocks this rung.
- **One phrase in the Research Question drops the 1.0 s bound:** "E033's margin needs no CatBoost". C5 of `H024_review_v2.md` replaces it in the record with "a CatBoost half is not shown to be needed beyond the 1.0 s bound, at equal weight". It is on a P ≈ 0.01–0.02 branch, so it does not block.
- **Conditions C1–C7 of `H024_review_v2.md` apply.**

## Scientific Validity

- **The reading now matches what the construction can show.**
  - The twin's residual correlation with E029 should be 0.996–0.999 on all rows.
  - The exact decomposition then fixes its blend gain at a fraction of a second.
  - The expected LOSS is a floor measurement, and the text records it as one.
- **The Scientific Value sentence is descriptive, not a reading:** "their gains above that floor are what the CatBoost half adds beyond averaging at a small disagreement".
  - It compares rungs; it does not decompose them additively.
  - It refers to "the CatBoost half", the configuration, which stays within H023 v3's accepted scope.
  - The decomposition reports accuracy and disagreement per rung, so the comparison cannot be over-read as an additive split.
- **Rung A's determinism.** It holds no GPU draw. The twin is still one subsampling realization at seed 42 (`H024_review_v2.md`, Scientific Validity (e)). That cannot move a reading expected near D ≈ +3.5 s.

## Novelty Relative to Existing Research

The project's first same-family average. It is not redundant.

## Experimental Isolation

- **Against E029:** exact. At the prediction level, H028 − E029 = ½ (twin − E029).
- **Against E033:** the whole second half is replaced, which v2 now states in the ladder table and the Controlled Variables. No single ingredient is isolated, and none is claimed.

## Validation Quality

- **D(H028) is a direct paired comparison against E033,** on the frozen folds with the frozen bootstrap.
- **No GPU draw is involved.**
- **Gating is status-only:** E038 must be COMPLETE and route-checked. If E038 is deferred, H028 is deferred with it.

## Leakage Review

### Target Leakage

PASS

There is no new input. The blend reads manifest-verified predictions only, and its weights are fixed a priori.

### Temporal Leakage

CONCERN

Inherited and not blocking: FS2's T features, and post-validation training months in S1 and W1. S1c and W1c bound them.

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

**That a twin built to stay close to E029 says anything about averaging beyond its own disagreement level.** It does not, and v2 now says so. The floor is interpretable only beside the measured disagreement of each rung (§Batch diagnostics).

## Missing Control or Ablation

**For any learner-family reading:** a same-family second half on E031's inputs (FS2_RAW's raw keys), or at E031's disagreement level.
- This is named, not required.
- It is D4-C7's open question.
- Without it, rung A speaks only to the generic-averaging floor, and v2 limits it to that.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Exactly one allocation,** `uv run python scripts/gate.py allocate H028 v2` (purpose `primary`).
  - It is made fifth in the batch, so it is expected to be **E039**.
  - The config is the Proposed Change block: components [E029, E038], weights [0.5, 0.5], seed 42, CLASS-S, all 8 folds.
- **It runs only after E038 is COMPLETE and has passed `route_check.py E038 - E029`.**
  - It runs by the pinned launcher, or at a later window under C3 of `H024_review_v2.md`.
  - If E038 does not end COMPLETE and route-checked, E039 is recorded under C2.
- **The reading is the §Batch rung reading on D(H028),** worded under C5. It is a disclosure only: no candidate, no holdout access.
- **Conditions C1–C7 of `H024_review_v2.md` apply.**

Required acknowledgement path:
- `research/day-06/acks/H028_ack_v2.md`, referencing the proposal hash `65b8f3fbc816a7bde428c7f39a8c40525dfb1ea4c9595b56444e14d4567d70a2` and this review's hash.

## Revision

None required.

## Advisor Prediction

Probability of improvement:

| Event (H028 = E039) | P |
|---|---|
| G(H028) < 0 (the twin blend beats E029 on the population; point) | 0.85 |
| "The twin does not reproduce the gain" (D ≥ +1.0 s and LOSS on ≥ 3 development folds) | 0.95 |
| Bounded "rung A carries the gain" (q95 of D's mean < +1.0 s) | 0.01 |
| INCONCLUSIVE | 0.04 |
| Runs in today's window (needs E038 COMPLETE in time) | 0.48 |
| Route check passes | 0.99 |

Expected magnitude:
- **On `NM_present_excl_LIRF`:**
  - G(H028): −0.1 to −1.0 s (central −0.4);
  - **D(H028): +2.9 to +3.9 s (central +3.55).**
- **All rows:**
  - H028 − E029: −0.1 to −1.0 s;
  - H028 − E033: +2.6 to +3.5 s.
- **The twin's disagreement term** (¼ mean squared prediction difference with E029) is 3–12 % of E031's on the population.

Primary expected failure mode:
- **The expected LOSS occurs.** Under v2 and C5 it enters the record as the generic-averaging floor at seed 42's disagreement, not as support for a family claim.
- **Second:** the window defers E038 and E039. They then run at the owner's next window under C3, or are recorded "not run (window)", with nothing inferred.
