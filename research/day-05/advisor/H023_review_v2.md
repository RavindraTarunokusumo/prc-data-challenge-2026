---
schema: advisor-review-v1
hypothesis_id: H023
proposal_version: 2
proposal_sha256: 05b13cfb32db777fa20fbf4706b3367a158b8604b207005a5f4d978730226a7c
exchange_id: X-D05-S04-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.88
created_utc: 2026-10-01T20:16:40Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.88).**

**The design is sound and its v1 revisions are substantially met:**
- the integrity reference is attainable;
- B3 is against E026;
- the noise condition is pre-registered;
- the gating is status-only;
- the claim is scoped to this CatBoost configuration.

**It cannot be accepted as written.** Two promotion-relevant statements are ambiguous, and it inherits the batch's component and freeze issues:

1. **Criterion 7 is stated in two incompatible ways.**
   - Falsification: "H021 v2 declares its class from measured RAM". But H021 v2 declares **CLASS-L from measured runtime**, and says "RAM is not the reason".
   - Resource Estimate: "the components are in H021 (CLASS-M, GPU)".
   - With P ≈ 0.65 that H021 runs over 30 min, the two readings decide criterion 7 differently.
   - `H021_review_v2.md` rules CLASS-L justified for H021 and its reproduction. v3 must read H021's class as CLASS-L, stated once.
2. **The consequence of an INCONCLUSIVE clause 1 is unstated.**
   - The noise condition makes clause 1 INCONCLUSIVE when |m| / 2 > 0.5 s.
   - Criterion 4 requires "clauses 1–2 above not met". An INCONCLUSIVE clause is neither met nor not met, and under brief §10 criterion 4 it cannot "support the claimed mechanism".
   - v3 must state that an INCONCLUSIVE clause 1 bars promotion, and whether H023r is then due.
3. **The reproduction blend's routed rows are unchecked.**
   - H023r is ½ E029 + ½ H021r.
   - v3 must run `route_check.py <H023r> - E029`, with H021r's own check (`H021_review_v2.md`) as its precondition, and state the consequence.
4. **Tools freeze** "as in H021": wrong anchor and incomplete list (`H021_review_v2.md`, Summary item 2).
5. **Clerical.**
   - Criterion 6 reads "E026 and E026 are byte-identical". It should read E026 and E027 (verified: 8 of 8 manifest hashes).
   - The references to "H021 v2" must follow H021's accepted version.

**v1 required revisions:**

| v1 item | v2 | Verdict |
|---|---|---|
| 1. Integrity clause | `route_check.py <H023> - E029`; "routed rows identical in both components" checked through H021's clause; criterion 8 restated as non-zero | **Met.** If H021's routed rows equal E029's, the blend's are equal bit for bit (0.0 + 0.5x + 0.5x = x; v1). E029 = E026 on every routed row (verified here) |
| 2. B3 | Against E026 | **Met** |
| 3. Noise | H021's re-draw enters at half size | **Met** as a rule. Its consequence for promotion is item 2 above |
| 4. Gating | Only status gates H023 and H023r | **Met** |
| 5. Criterion 7 | Stated | **Inconsistent** (item 1 above) |
| 6. Claim scope | "This CatBoost configuration"; the E029 + H022 blend named, not run | **Met** |
| Tooling | `prc/blending.py`, dispatched by the worker | **Verified.** It imports no truth-reading code (`test_blending_does_not_import_truth`), checks each component's manifest SHA-256 and COMPLETE status, and its tests pass. E029's ledger status is COMPLETE |

## Scientific Validity

### (a) The expected gain is small; clause 1 is a fair test

This is unchanged from v1 (a).
- At a 6 s component gap, an equal-weight blend gains 1 s on normal taxis only if the residual correlation is about 0.92 or less.
- My prior is 0.93–0.96.
- The −1.0 s threshold therefore sits near the expected value, which makes clause 1 decisive in both directions.

### (b) The noise condition is a proxy

- |m| / 2 approximates the blend's re-draw sensitivity. RMSE is not linear in a component's predictions, so it is not exact.
- It is acceptable as pre-registered. H023r's own clause 1 reading is recorded beside it when H023r runs.
- "The primary reading stands" is consistent with criterion 6, which re-checks criteria 1–3 only (frozen).

### (c) S1 and the single row

This is unchanged from v1 (b).
- The S1 outcome against E026 is roughly +0.20 s (E029's TIE), plus 0.66 s per 1,000 s on row 192622644, minus 0.34 × the clause-population gain.
- An S1 LOSS is a real possibility. Missing Control 1's pre-registration covers the direction.

### (d) Criterion 7 with a CLASS-L component

- Reading H021's class as CLASS-L does not weaken criterion 7's purpose: the declared, justified class is honoured. A run over 90 min or 11 GB would still fail.
- The RAM and CLASS-M disclosures of `H021_review_v2.md` (conditions 3–4) appear beside criterion 7 in H023's record.

## Novelty Relative to Existing Research

- **It is the project's first ensemble,** and answers Day 5's architecture question for this configuration.
- **It is not a re-adjudication of E023.** Rule L v2 item 3 applies, and B2 bars promotion on E023's known margin alone.

## Experimental Isolation

**Against E029: exact.** H023 − E029 = ½ (H021 − E029).

**Attribution beyond "this configuration"** would need the named E029 + H022 blend. v2 scopes the claim accordingly.

## Validation Quality

**The validation design is correct:**
- the frozen folds;
- criteria 1–3 against E026, with rule L v2's boundary flags;
- criterion 4 with B2 and H018 v2's clauses 1–2 (the hand-off base ruling);
- criterion 6 through the reproduction blend;
- criterion 8 against E028, with a 200 s margin;
- B3 against E026;
- the rule 1 S1 recording;
- Missing Control 1.

**Gaps:** items 1–3 of the Summary.

## Leakage Review

### Target Leakage

PASS

- The weight is fixed a priori, and nothing is fitted.
- The blend reads only manifest-verified prediction files.
- Both components were fitted on each fold's training rows only.

### Temporal Leakage

CONCERN

This is inherited, not blocking: FS2's T features in both components, and the CTRs over post-validation months in S1 and W1. The twins bound them.

### Competition Availability

PASS

- Both components can predict SUBMIT_JAN and SUBMIT_JUL, and the blend averages stored files.
- A submitted blend needs SUBMIT runs of both components, one of them a stochastic GPU fit. The Day 7 procedure is untested. Non-blocking.

## Compute Review

### RAM

PASS

About 3.5 GB: silver plus FS0, as E028 (3.50 GB with a ridge fit; the blend fits nothing). This is inside CLASS-S's 4 GB, with little margin.

### Runtime

PASS

1–3 min.

### Disk

PASS

About 10 MB.

## Weakest Assumption

**That a CatBoost about 6 s worse on normal taxis is decorrelated enough from E029 for an equal-weight average to gain at least 1 s.** It needs a residual correlation of about 0.92 or less.

## Missing Control or Ablation

**The E029 + H022 equal-weight blend.**
- It is required only if any complementarity is attributed to categorical handling.
- v2 scopes the claim to "this CatBoost configuration", so it is not required.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- There is no allocation of H023 v2.
- No blend of any component on a frozen fold under this proposal.
- Comparisons of existing prediction files under the frozen functions remain allowed, recorded as audit only.

Required acknowledgement path: `research/day-05/acks/H023_ack_v2.md`.
- It references both hashes and confers no authority.
- Submit `H023_v3.md` with H021 v3 and H022 v3.

## Revision

**Required (minimal):**

1. **Criterion 7.**
   - State once that H021's class is CLASS-L (`H021_review_v2.md`).
   - Remove "(CLASS-M, GPU)" and "declares its class from measured RAM".
   - Carry H021's CLASS-M and RAM disclosures beside criterion 7.
2. **INCONCLUSIVE clause 1.** State that it bars promotion (criterion 4 not satisfied), and whether H023r is then due.
3. **H023r integrity.**
   - Add `route_check.py <H023r> - E029`, with H021r passing its own check as the precondition for allocating H023r.
   - State the consequence: H023r INVALID for criterion 6.
4. **Tools freeze.** As in `H021_review_v2.md`, Revision item 2.
5. **Clerical.**
   - "E026 and E026" reads "E026 and E027".
   - The references to H021 follow its accepted version.

**Acceptable as is:**
- the fixed 0.5 weight and its rationale;
- `prc/blending.py` and its tests;
- E029 as the exact ablation;
- clauses 1 and 2;
- the noise condition (|m| / 2 > 0.5 s) and its H023r recording;
- the status-only gating;
- the promotion path against E026, with B2, H018 v2's clauses 1–2, criterion 6 through [E029, H021r], criterion 8 against E028 (200 s margin) and B3 against E026;
- the rule 1 S1 recording;
- Missing Control 1;
- rules 2–12 as stated;
- the claim scope;
- CLASS-S.

## Advisor Prediction

These are for a v3 run of the same design.

Probability of improvement:

| Event | P |
|---|---|
| Clause 1 not met (H023 − E029 ≤ −1.0 s, q95 < 0, `NM_present_excl_LIRF`) | 0.35 |
| H023 − E029 below 0 on `NM_present_excl_LIRF` (point) | 0.75 |
| Clause 2 not met (all rows against E029 < 0) | 0.65 |
| The noise condition triggers (\|m\| / 2 > 0.5 s) | 0.12 |
| Criterion 1 against E026 | 0.95 |
| S1 counted WIN against E026 | 0.07 |
| S1 LOSS against E026 | 0.25 |
| H018 v2 clauses 1–2 not met | 0.93 |
| Criterion 3 (no airport beyond +3 % against E026) | 0.90 |
| Promotion | 0.04 |

Expected magnitude:
- **H023 − E029, `NM_present_excl_LIRF`:** −1.8 to +0.3 s (central −0.7).
- **H023 − E029, all rows:** −1.5 to +0.5 s (central −0.5).
- **H023 − E026, all rows:** −1.5 to −3.5 s (central −2.5).
- **S1 against E026:** −0.3 to +1.8 s (central +0.7).
- **Residual correlation, E029 against H021,** on the clause population: 0.92–0.97.
- **Row 192622644:** 4,500–8,000 s (P 0.85 below E026's 8,136 s).

Primary expected failure mode:
- **As written.** Criterion 7 is decided by which of its two statements is read, because H021 most likely runs over 30 min.
- **After revision.** The complementarity is real but small, and S1 is a TIE or a LOSS. The record reads "complementary (or not), not promoted", and D3-C2 and D3-C3 stay in the champion.
