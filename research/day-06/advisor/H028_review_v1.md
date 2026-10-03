---
schema: advisor-review-v1
hypothesis_id: H028
proposal_version: 1
proposal_sha256: 172b45ad51e788879cf90ccd5187dc3e6cd4972cb96bd30312404d6896622675
exchange_id: X-D06-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.88
created_utc: 2026-10-02T17:46:31Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.88).**

- **The arithmetic and gating are correct.** It is a fixed 0.5/0.5 blend of E029 and its twin, gated by status only, and deferred with H027.
- **Its reading is the batch's main overclaim.** The expected-reading label "the different family carries part" (P 0.90) would record a control that is expected to fail as confirmation of the claim under attack.
- **§Batch revision 2 of `H024_review_v1.md` applies in full.** H028 also carries revisions 1, 3, 5, 6 and 7 and the binding ruling there, plus:
  - **(a) Research Question and Scientific Value.** Replace "the direct adversarial test of the Day 5 mechanism" and "If a same-family twin of E029 gives most of the −3.96 s, … is not the mechanism; otherwise the champion's margin needs a different learner".
    - Rung A measures the floor that generic averaging reaches at a perturbation twin's disagreement.
    - Only its "carries" outcome bears on the family reading. Its LOSS outcome says nothing about family.
  - **(b) The expected-reading row.** Relabel it per revision 2(b), and restate the probabilities under revision 1's bounded rule.
  - **(c) The pointer.** Point at the revised §Batch. Its gating then follows H027 v2: the seed refusal in `H027_review_v1.md` would otherwise defer H028 every time.

## Scientific Validity

### (a) A LOSS here cannot attribute the gain to "family"

The second half changes everything at once:
- the learner;
- the feature set (FS2's `__RARE__` collapse against FS2_RAW's raw keys);
- the categorical statistics and the hyperparameters;
- most of the disagreement.

**What a LOSS can and cannot support:**
- A LOSS is equally consistent with "the raw keys are needed", "the statistics are needed" and "more disagreement is needed".
- It is not evidence for "a second learner family adds signal".
- The accepted Day 5 scope is "this CatBoost configuration as a whole" (H023 v3, revision 6). A rung A LOSS adds nothing to that scope.

### (b) The outcome is fixed by construction

- **The gain follows from accuracy and disagreement.** For a fixed 0.5/0.5 blend, MSE_blend = ½ MSE₁ + ½ MSE₂ − ¼ mean((p₁ − p₂)²) on the same rows.
- **A twin with residual correlation 0.995–0.999** and similar accuracy gains a fraction of a second.
- **The researcher's own forecast says the same:** central G −0.5 s, D +3.4 s, P(carries) 0.03.
- **So the test is informative in one direction only.** A surprise "carries" would be strong evidence for generic averaging. A LOSS is expected and weak.

### (c) Rung A is worth keeping

- **It is cheap:** a CLASS-S blend after a CLASS-M twin, run last.
- **It puts a number on the generic-averaging floor,** which the Day 5 record lacked.
- **With revision 5,** the twin's measured disagreement on the readings' population makes the floor interpretable beside E031's.

## Novelty Relative to Existing Research

The project's first same-family average. It is not redundant.

## Experimental Isolation

- **Against E029:** exact. H028 − E029 = ½ (twin − E029) at the prediction level.
- **Against E033:** the entire second half is replaced, as (a) says. This is not an isolated contrast of any single ingredient.

## Validation Quality

- **D(H028) is a direct paired comparison against E033** on the frozen folds.
- **No GPU draw is involved.** Both halves are deterministic, so the blend-draw caveat (revision 3) does not apply here.
- **The gaps are the §Batch ones,** chiefly revision 2.

## Leakage Review

### Target Leakage

PASS

The blend adds no input. It reads manifest-verified predictions only, and its weight is fixed a priori.

### Temporal Leakage

CONCERN

Inherited and not blocking: FS2's T features, and post-validation training months in S1 and W1. The twins bound them.

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

**That a same-family twin built to be close to E029 can stand in for "any second model of similar accuracy".** It matches the accuracy but not the decorrelation.

## Missing Control or Ablation

**For any "learner family" reading:** a same-family second half on E031's inputs (FS2_RAW's raw keys), or at E031's disagreement level.
- This is named, not required in this batch.
- It is also D4-C7's open question.
- Without it, rung A speaks only to the generic-averaging floor.

## Decision

REVISE

## Execution Authorization

Authorized scope:
- **None.** REVISE never permits execution.

Required acknowledgement path:
- None for v1.
- After an ACCEPT of v2, it is `research/day-06/acks/H028_ack_v2.md`.

## Revision

**Required.**
1. **The §Batch revisions** 1, 2, 3, 5, 6 and 7 of `H024_review_v1.md`, through a pointer to the revised §Batch. Revision 2 is the substantive one.
2. **Research Question and Scientific Value,** restated per Summary item (a).
3. **The expected-reading row,** relabelled and re-estimated per Summary item (b).

**Binding:** the ruling in `H024_review_v1.md`.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| G(H028) < 0 (the twin blend beats E029 on the population; point) | 0.85 |
| Rung A "carries the gain" (any form) | 0.02 |
| LOSS reading (D ≥ +1.0 s and LOSS on ≥ 3 development folds) | 0.93 |
| E038 and E039 both run in today's window, under the v1 order | 0.65 |

Expected magnitude:
- **On `NM_present_excl_LIRF`:**
  - G(H028): −0.1 to −1.1 s (central −0.45);
  - **D(H028): +2.9 to +3.9 s (central +3.5).**
- **All rows:**
  - H028 − E029: −0.1 to −1.0 s;
  - H028 − E033: +2.6 to +3.5 s.
- **The twin's disagreement with E029** (mean squared prediction difference) is about 5–15 % of E031's.

Primary expected failure mode:
- **The expected LOSS occurs.** As v1 is worded, it would be recorded as "the different family carries part", which supports the Day 5 generalization by a test that could not have refuted it.
- **Second:** the window defers the rung. Without revision 6, it might then never be run.
