---
schema: advisor-review-v1
hypothesis_id: H025
proposal_version: 2
proposal_sha256: 44db30f7e22dda4d21d5d6bbcd88e649b234a1b7563cde2033b6e301f2cd26df
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

**Decision: ACCEPT (0.87).** Delta review against `H025_review_v1.md`.

- **Both required items are met:**
  - **The pointer.** It now names `research/day-06/proposals/H024_v2.md` §Batch, which carries §Batch revisions 1, 3, 5, 6 and 7.
  - **The reading probabilities.** They are restated under the bounded rule: "carries" 0.30, "part" 0.25, INCONCLUSIVE 0.45.
- **The only other change is the component id.** H024 is now E036, because rung B runs first. The config, the falsification text and the gating are otherwise unchanged.
- **The design is unchanged:** a fixed 0.5/0.5 blend that differs from E033 only in the second half's `max_ctr_complexity` (4 to 1), plus that half's GPU draw.
- **The batch conditions C1–C7 of `H024_review_v2.md` apply,** with the verification record there. C5 (bounded wording) matters most for this rung: it is the rung most likely to give a "carries" reading next to per-fold LOSSes.

## Scientific Validity

- **Rung C is still the attribution question with the most practical weight.** It asks whether the champion's −3.96 s needs the complexity-4 combinations, which are the reason E031 is CLASS-L.
- **The bounded rule is reachable here, more than either forecast assumed.**
  - D(H025) compares two blends that share E029, so it moves only half the H024 − E031 prediction difference. Its bootstrap q95 − mean should be about 0.2–0.25 s.
  - That is not E033-against-E029's 0.44 s, which my v1 review used as the reference.
  - So "carries" needs D's mean below about +0.75 s, and the expected D (central +0.55 s) often meets it.
  - The researcher's P 0.30 and my v1 P 0.38 both used too wide a spread.
- **A "carries" reading may come with per-fold LOSSes.** The combinations would then carry a measurable part below 1.0 s. C5 makes the record say so.
- **Alternative explanation 1** ("a GPU draw of ≈ ½ × 0.68 s in the blend") is consistent with the measured blend re-draw, +0.26 s on the mean. W1 moved +1.28 s, and a reading resting on W1 is flagged (§Batch).
- **Alternative explanation 2** (an effect confined to LIRF NM-present tail rows) is caught by rule 11's two populations.
- **The Day 7 motive** ("fewer CTR features exposed to January") remains a conjecture. The binding ruling covers it: rule 10 applies, and the selection is stated.

## Novelty Relative to Existing Research

New. No blend with a complexity-1 CatBoost half exists, and the rung is not redundant with E033, E034 or any rejected work.

## Experimental Isolation

- **Against E033:** one change, the second half's complexity, plus that half's GPU draw.
- **A resolved-parameter difference outside H024's closed set** (C6) is disclosed on this rung's reading. This is pre-registered in H024 v2.

## Validation Quality

- **D(H025) is a direct paired comparison against E033,** on the frozen folds with the frozen bootstrap. The identity with G is exact.
- **Gating is status-only:** H024 must be COMPLETE and route-checked, whatever its accuracy (the launcher's `ROUTE_OK` gate).
- **Rules 1, 6, 7, 11 and 12** go through the stated scripts.

## Leakage Review

### Target Leakage

PASS

There is no new input. The blend reads manifest-verified predictions only, and its weights are fixed before the component exists.

### Temporal Leakage

CONCERN

Inherited from the components and not blocking: FS2's T features, and CTRs over post-validation months in S1 and W1. S1c and W1c bound them.

### Competition Availability

PASS

Both components predict SUBMIT_JAN and SUBMIT_JUL.

## Compute Review

### RAM

PASS

About 3.4 GB (E033 3.38 GB, E034 3.40 GB), inside CLASS-S's 4 GB.

### Runtime

PASS

About 8–60 s (E033 took 8.3 s). The CLASS-S timeout is 450 s.

### Disk

PASS

About 60 MB.

## Weakest Assumption

**That one GPU draw of the complexity-1 half represents it.**
- The bounded rule protects against the bootstrap's row noise, not against the draw.
- A blend-level re-draw has moved the mean by 0.26 s, which is comparable to the margin between D's expected value and the effective "carries" boundary.

## Missing Control or Ablation

- **None beyond the brackets:** E029 (no second half) and E033 (complexity 4).
- **H024's closed set (C6)** is the isolation check this rung inherits.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **Exactly one allocation,** `uv run python scripts/gate.py allocate H025 v2` (purpose `primary`).
  - It is made third in the batch, so it is expected to be **E037**.
  - The config is the Proposed Change block: components [E029, E036], weights [0.5, 0.5], seed 42, CLASS-S, all 8 folds.
- **It runs only after E036 is COMPLETE and has passed `route_check.py E036 - E029`.**
  - It runs by the pinned launcher, or at a later window under C3 of `H024_review_v2.md`.
  - If E036 does not end COMPLETE and route-checked, E037 is recorded under C2.
- **The reading is the §Batch rung reading on D(H025),** worded under C5. It is a disclosure only: no candidate, no holdout access.
- **Conditions C1–C7 of `H024_review_v2.md` apply.**

Required acknowledgement path:
- `research/day-06/acks/H025_ack_v2.md`, referencing the proposal hash `44db30f7e22dda4d21d5d6bbcd88e649b234a1b7563cde2033b6e301f2cd26df` and this review's hash.

## Revision

None required.

## Advisor Prediction

Probability of improvement:

| Event (H025 = E037) | P |
|---|---|
| D(H025) < 0 (rung C beats E033; point) | 0.12 |
| Bounded "rung C carries the gain" (q95 of D's mean < +1.0 s) | 0.60 |
| "Combinations carry part" (D ≥ +1.0 s and LOSS on ≥ 3 development folds) | 0.12 |
| INCONCLUSIVE | 0.28 |
| "Rung C beats E033" (D ≤ −1.0 s and q95 < 0) | 0.01 |
| "Carries" with at least one development-fold LOSS (C5's added sentence applies) | 0.30 |
| Runs in today's window (needs E036 COMPLETE in time) | 0.94 |
| Route check passes | 0.99 |

Expected magnitude:
- **On `NM_present_excl_LIRF`:**
  - G(H025): −2.5 to −4.1 s (central −3.4);
  - **D(H025): −0.15 to +1.4 s (central +0.55); q95 − mean 0.2–0.3 s.**
- **All rows:**
  - H025 − E033: −0.2 to +1.2 s (central +0.45);
  - H025 − E029: −2.3 to −3.7 s.

Primary expected failure mode:
- **D's mean lands between about +0.75 and +1.0 s.** Its q95 then crosses +1.0 s while the mean stays below it, so the reading is INCONCLUSIVE.
- **The other risk is a favourable draw.** It would produce "carries" on one draw. That is recorded as such (C5), not as "the combinations are not needed".
