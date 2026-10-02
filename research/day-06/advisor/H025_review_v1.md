---
schema: advisor-review-v1
hypothesis_id: H025
proposal_version: 1
proposal_sha256: de55d6af78decf148b089518b3815c33af91cf3ec2121378016931997354395f
exchange_id: X-D06-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.86
created_utc: 2026-10-02T17:44:56Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.86).**

- **H025's own design is sound.** It is a fixed 0.5/0.5 blend that differs from E033 only in the CatBoost half's `max_ctr_complexity` (4 → 1), plus that half's GPU draw. Its gating is by status only, and its class is CLASS-S.
- **It adopts H024 §Batch unchanged.** So it carries §Batch revisions 1, 3, 5, 6 and 7 of `H024_review_v1.md`, and the binding ruling there, plus two items of its own:
  - **(a) The pointer.** It names `research/day-06/proposals/H024_v1.md`, so v2 must point at the revised §Batch.
  - **(b) The reading probabilities.** "Carries" P 0.60, "part" P 0.20, INCONCLUSIVE P 0.20 were stated under v1's point rule. Restate them under revision 1's bounded rule.

The verified facts, the reproduced figures and the launcher findings are in `H024_review_v1.md`, Summary Assessment.

## Scientific Validity

- **Rung C is the attribution question with the most practical weight.** It asks whether the champion's −3.96 s needs the complexity-4 combinations, which are the reason E031 is CLASS-L (1,523 s).
- **It is also the rung most exposed to v1's asymmetric reading.**
  - The expected D(H025) (+0.1 to +1.4 s, central +0.6) sits under the +1.0 s point threshold.
  - The paired bootstrap spread of a half-blend difference is likely 0.3–0.5 s. E033 against E029 has a q95 − mean of 0.44 s on this population.
  - So a point rule would usually say "carries" here, while a bounded rule would often say INCONCLUSIVE. That gap is what revision 1 closes.
- **Its Day 7 motive is a conjecture and a selection motive.** Scientific Value says "fewer CTR features exposed to January's distribution shift". The binding ruling in `H024_review_v1.md` covers it: rule 10 applies, and the selection is stated.
- **Alternative explanation 2 is handled correctly.** A complexity effect confined to LIRF NM-present tail rows is visible through rule 11's two populations.

## Novelty Relative to Existing Research

New: no blend with a complexity-1 CatBoost half exists. It is not redundant with E033, E034 or any rejected work.

## Experimental Isolation

- **Against E033, the change is single:** the second half's complexity.
- **Two caveats remain:**
  - the GPU draw. The measured blend re-draw is +0.26 s on the 5-fold mean and +1.28 s on W1 (revision 3);
  - any resolved-parameter difference beyond complexity (H024 revision 8). If H024's closed set is violated, H025's reading carries that disclosure.

## Validation Quality

- **D(H025) compares H025 with E033 directly,** on the frozen folds and the bootstrap.
- **The identity with G is exact.**
- **Gating is by status only:** H024 COMPLETE and route-checked, whatever H024's accuracy.
- **Rules 1, 6, 7, 11 and 12 go through the stated scripts.**
- **The gaps are the §Batch ones,** chiefly the bounded reading (revision 1).

## Leakage Review

### Target Leakage

PASS

The blend adds no input. It reads manifest-verified predictions only, and its weight is fixed before the component exists.

### Temporal Leakage

CONCERN

Inherited from its components and not blocking: FS2's T features, and CTRs over post-validation months in S1 and W1. The twins bound them.

### Competition Availability

PASS

Both components can predict SUBMIT_JAN and SUBMIT_JUL.

## Compute Review

### RAM

PASS

About 3.4 GB (E033 3.38 GB, E034 3.40 GB), inside CLASS-S's 4 GB. The margin is small but measured.

### Runtime

PASS

About 8–60 s (E033 took 8.3 s).

### Disk

PASS

About 60 MB.

## Weakest Assumption

**That one GPU draw of the complexity-1 half represents it.** In a blend re-draw, W1 alone moved 1.28 s, which is enough to change a per-fold outcome.

## Missing Control or Ablation

- **None beyond the stated brackets:** E029 (no second half) and E033 (complexity 4).
- **H024's closed exempt set** (`H024_review_v1.md`, revision 8) is the isolation check this rung inherits.

## Decision

REVISE

## Execution Authorization

Authorized scope:
- **None.** REVISE never permits execution.

Required acknowledgement path:
- None for v1.
- After an ACCEPT of v2, it is `research/day-06/acks/H025_ack_v2.md`.

## Revision

**Required.**
1. **The §Batch revisions** 1, 3, 5, 6 and 7 of `H024_review_v1.md`, through a pointer to the revised §Batch.
2. **Restated reading probabilities** under the bounded "carries" rule.

**Binding:** the ruling in `H024_review_v1.md` (never NEW; rule 10 covers the configuration; selection stated on Day 7).

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| D(H025) < 0 (rung C beats E033; point) | 0.15 |
| v1 "carries the gain" (D < +1.0 s; point) | 0.62 |
| Bounded "carries" (bootstrap q95 of D's mean < +1.0 s) | 0.38 |
| "Combinations carry part" (D ≥ +1.0 s and LOSS on ≥ 3 development folds) | 0.18 |
| "Rung C beats E033" (D ≤ −1.0 s and q95 < 0) | 0.01 |
| Route check passes | 0.99 |

Expected magnitude:
- **On `NM_present_excl_LIRF`:**
  - G(H025): −2.4 to −4.0 s (central −3.3);
  - **D(H025): −0.1 to +1.5 s (central +0.65).**
- **All rows:**
  - H025 − E033: −0.2 to +1.3 s (central +0.5);
  - H025 − E029: −2.3 to −3.8 s.

Primary expected failure mode:
- **D(H025) lands between +0.4 and +1.0 s.** A point rule then calls it "carries", but the bounded rule cannot.
- **The honest reading is INCONCLUSIVE.** Under v1 the record would instead have said "the combinations are not needed for the champion's margin" on one draw.
