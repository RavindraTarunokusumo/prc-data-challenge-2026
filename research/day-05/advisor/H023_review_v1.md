---
schema: advisor-review-v1
hypothesis_id: H023
proposal_version: 1
proposal_sha256: 2e79f8b1f18bc4039428aded8a0e847742ec04d41dbc738a99c7439fc7beccb8
exchange_id: X-D05-S04-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.93
created_utc: 2026-10-01T19:26:55Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.93).**

**The design is sound.** H023 is a legitimate Day 5 candidate:
- a fixed equal-weight blend, with no fitted weight;
- E029 as the exact ablation;
- decisive complementarity clauses under B2;
- the hand-off base ruling's H018 clauses in criterion 4;
- the single-row exposure pre-registered (Missing Control 1);
- CLASS-S.

**As written, it is certain to be INVALID, and five more items need fixing:**
1. **The integrity clause is certain to be met** (D5-C4).
   - H023's routed rows are ½ E029 + ½ H021.
   - E029's routed rows differ from E028's on every routed row of every fold, by up to 190.9 s (`LAPTOP_REFS_review_v1.md` (b)).
   - For `route_check.py <H023> - E028` to pass at 1e-6 s, H021's routed rows would have to equal 2·E028 − E029 on every row, to 2e-6 s.
2. **Three premises are false or unverified on the laptop:**
   - "Routed rows are identical in both components" is unverified: whether the CatBoost path reproduces E029's routed rows is unknown.
   - "The blend's routed rows are the ridge's prediction" holds only if they are.
   - "Criterion 8 statistic against E028: 0.0 on every fold" is false: it will be small and non-zero.
3. **B3 is misapplied.** The proposal applies "B3 against E028". B3 is defined against **the comparator of the S1 WIN** (`H001_review_v1.md`: "an S1c point dRMSE ≥ 0 against the same comparator"). Here that comparator is E027, E019's instance.
4. **The CatBoost half's noise is not in clause 1.**
   - H023 − E029 = ½ (H021 − E029), so H023 inherits half of every re-draw difference of H021.
   - H021's noise condition (1.5 s) covers H021's clause only. A 1.5 s re-draw difference becomes 0.75 s here, close to clause 1's −1.0 s threshold.
5. **The gating and criterion 7 must be explicit.**
   - H021, its reproduction and H022 complete before H023 is allocated, so their validation results are known first. v2 must state that only status (COMPLETE, and not INVALID under the revised integrity rule) gates H023 and H023r. No accuracy result may gate them.
   - Criterion 7 is extended to "both components". H021's RAM is expected at about 7–8 GB against the CLASS-M target of 8 GB (`H021_review_v1.md`). v2 must state this rule knowing that.
6. **The research question claims more than the clauses test.**
   - "Two learners that use the same keys differently" attributes complementarity to categorical handling. Clause 1 tests only "adding this CatBoost half helps".
   - Either scope the claim, or pre-register the named control below.

**Verified here** (beyond `LAPTOP_REFS_review_v1.md`):
- **`blend.py`.**
  - The weights are fixed and must sum to 1, with at least 2 components.
  - It refuses a component that is not COMPLETE, and reads each component through the manifest-checked `prc.evaluate._predictions`.
  - The worker passes the fold, and final-fold predictions are written under `predictions/validation/<E###>/`. So the same code can read SUBMIT folds. The Day 7 procedure is still untested (HANDOFF §10).
  - `test_blend_fixed_weights_of_stored_components` passes.
- **Routed rows, as arithmetic.** 0.0 + 0.5·x + 0.5·x = x exactly in float64. So if both components' routed rows were equal, the blend's would equal them bit for bit.
- **Single rows** (existing files). E027: 8,136.5 s on row 192622644 and 1,979.5 s on row 183910286. E029: 7,040.9 and 7,938.4 s.
- **"0.66 s of S1 RMSE per 1,000 s"** is correct. It is ΔSSE / (2 · RMSE · n), with 632.1 s and 190,713 rows.
- **E029 on the clause population.** RMSE is 201.5–243.3 s per development fold (about 219 s). On S1 it is 243.3 s on 171,901 rows, against 632.3 s on all 190,713 rows.

## Scientific Validity

### (a) The blend's expected gain is small, and clause 1 is a fair test

- **The arithmetic.** On the clause population, take E029 at about 219 s. If H021 is 6 s worse, the equal-weight blend's RMSE depends on the residual correlation ρ:

| ρ | Blend − E029 |
|---|---|
| 0.89 | −3.0 s (the proposal's central) |
| 0.93 | −0.9 s |
| 0.95 | +0.2 s |

- **What the proposal assumes.** Its central −3 s therefore assumes ρ of about 0.89 on normal taxis. Its own expectation is "0.93–0.98 on all rows, lower on bulk rows".
- **My prior.** For two boosted learners on largely shared inputs with a large irreducible component, ρ is about 0.93–0.96. That implies a gain of 0 to −1 s.
- **Reading.** The −1.0 s threshold (q95 < 0) sits near the expected value, so clause 1 is decisive in both directions. That is a strength.
- **Clause 2 (all rows < 0 against E029)** is a weak sanity bound. It is acceptable as such.

### (b) S1 dilutes the gain and the single row taxes it

- **Dilution.** A 1 s gain on S1's clause population is about **0.34 s** of S1's all-rows RMSE (243.3 s on 171,901 rows, against 632.3 s on 190,713).
- **The single row.** On row 192622644, every 1,000 s the blend's prediction falls below E027's costs about 0.66 s.
- **The S1 outcome against E027 is then roughly** +0.20 s (E029's TIE) + 0.66 s per 1,000 s on that row − 0.34 × the clause-population gain.
  - At a blend prediction of about 5,500 s and a 1 s clause gain, that is about **+0.8 s**.
  - With the S1 band about 2 s wide (E023 − E019: q10 −0.69, q90 +1.26), **an S1 LOSS is a real possibility**, not only a TIE.
- **What the proposal covers.** Missing Control 1 pre-registers the direction; "S1 TIE most likely" understates the LOSS risk. This changes no clause. It is recorded in the Advisor Prediction.

### (c) The integrity clause, the routed rows and criterion 8

- **Under the revised reference** (LAPTOP_REFS v2), H023's routed rows are the mean of its components'.
- **If H021's routed rows equal E029's,** H023's equal E027's bit for bit. All routed-row terms then vanish from every comparison against E027 or E029.
- **If not,** they differ by half the component difference. That is at most about 95 s on single rows, judging from (b) of the LAPTOP_REFS review, and of the order of 0.001 s in fold RMSE. It must then be stated, not assumed away.
- **Criterion 8** (≤ +6,500 s) is unaffected in practice; only its expectation changes.

### (d) Mechanism attribution

- **What is exact.** H023 − E029 = ½ (H021 − E029), at the prediction level.
- **What is not isolated.** H021 differs from E029 in learner, tree shape, feature set (raw against collapsed levels), categorical representation and random streams. So a complementarity gain is attributable to "this CatBoost configuration", not to "using the same keys differently".
- **The control that would attribute it** is the equal-weight blend of E029 and H022 (named below). H022 shares H021's learner, budget, rows and random procedure, but has no categorical statistics.

### (e) Noise

- **What the frozen cluster bootstrap does not see.** The CatBoost half is a GPU and seed draw.
- **The data that will exist.** H021's unconditional reproduction gives a second draw at no extra fit cost. A blend H023r is CLASS-S.
- **What v2 must do.** State how that second draw enters clause 1. One option is H021's noise condition carried at half size; another is the clause evaluated on H023r as well. The choice is the researcher's.

## Novelty Relative to Existing Research

- **It is the project's first ensemble,** and it answers Day 5's architecture question: is part of the LightGBM's error learner-specific?
- **It is not a re-adjudication of E023** (rule 10).
  - The configuration is new.
  - B2 bars promotion unless the CatBoost half adds at least 1.0 s on normal taxis and improves all rows against E029.
  - So E023's known margin cannot carry H023 alone.
  - This agrees with LAPTOP_REFS item 3.

## Experimental Isolation

- **Against E029: exact** (one added component, fixed weight).
- **The mechanism's attribution beyond "this configuration"** needs the named control ((d)).

## Validation Quality

**The validation design is correct:**
- the frozen folds;
- promotion against E019 through E027 under the revised rule L;
- criterion 4 with H018 v2's clauses 1–2 (the hand-off base ruling);
- criterion 6 through a blend of E029 and H021's reproduction;
- B2;
- the rule 1 S1 recording;
- the Missing Control 1 pre-registration.

**Criterion 6.** E029 is not re-drawn, and that is acceptable. The LightGBM half is deterministic on the laptop (E026 ≡ E027 byte for byte), so the stochastic part is re-drawn in full. The condition is that the environment stays fixed (LAPTOP_REFS revision item 4).

**Fix B3** (Summary, item 3): an S1 WIN with an S1c point dRMSE ≥ 0 **against E027** is an unresolved objection.

## Leakage Review

### Target Leakage

PASS

- The blend fits nothing, and its weight was fixed before any component existed.
- It reads only prediction files, through the manifest-checked loader. Both components were fitted on each fold's training rows.

### Temporal Leakage

CONCERN

This is inherited and not blocking: FS2's T features in both components, and the CTRs of post-validation training months in S1 and W1. That is the frozen fold design, which the twins bound.

### Competition Availability

PASS

- Both components can predict SUBMIT_JAN and SUBMIT_JUL, and the blend code can read those files.
- A submitted blend would need SUBMIT runs of both components, one of them a stochastic GPU fit. The Day 7 procedure is untested (HANDOFF §10). Non-blocking.

## Compute Review

### RAM

PASS

- Silver plus FS0 per fold comes to about 3.0–3.5 GB. E028, the FS0 ridge, peaked at 3.50 GB.
- That is inside CLASS-S's 4 GB, with little margin.

### Runtime

PASS

1–3 min.

### Disk

PASS

About 10 MB.

## Weakest Assumption

**That a CatBoost expected to be about 6 s worse on normal taxis is decorrelated enough from E029 for an equal-weight average to gain at least 1 s.**
- At that gap, it needs a residual correlation of about 0.92 or less.
- Two boosted learners on shared inputs with a large irreducible component typically sit at 0.93–0.96.

## Missing Control or Ablation

Named, not designed:
- **The equal-weight blend of E029 and H022.** It is needed if any complementarity is attributed to categorical handling.
  - It shares H021's learner, budget, rows and random procedure, without categorical statistics.
  - It is CLASS-S, and both components will exist.
  - Without it, the record scopes the claim to "this CatBoost configuration".

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- There is no allocation of H023 v1.
- No blend of any component on a frozen fold under this proposal.
- Comparisons of existing prediction files under the frozen functions remain allowed, recorded as audit only.

Required acknowledgement path: none for v1. Submit `research/day-05/proposals/H023_v2.md` in the same exchange as LAPTOP_REFS v2, H021 v2 and H022 v2.

## Revision

**Required (minimal):**

1. **Integrity clause** ((c)).
   - Adopt the route-integrity reference settled in LAPTOP_REFS v2.
   - Make the clause consistent with H023's routed rows being the mean of its components'.
   - Restate "routed rows identical in both components" and the criterion 8 expectation, as facts to be checked or as stated differences.
2. **B3.** Evaluate it against E027, the comparator of the S1 WIN.
3. **Noise** ((e)). Pre-register how the CatBoost half's re-draw (H021's reproduction) enters clause 1.
4. **Gating.**
   - State that H023 is allocated once H021 has completed and passed the revised integrity rule, whatever the accuracy of H021 or H022.
   - State that H023r is due by its stated rule, whatever the interim results.
   - No other condition gates either run.
5. **Criterion 7.** State the component-class rule knowing H021's RAM estimate (`H021_review_v1.md`). Keep it, or justify a different reading.
6. **Claim scope** ((d)). Restrict the research question's attribution to "this CatBoost configuration", or pre-register the named control as a reported contrast.

**Acceptable as is:**
- the fixed 0.5 weight and its rationale;
- `blend.py` and its test;
- E029 as the exact ablation;
- clause 1 (−1.0 s and q95 < 0 on `NM_present_excl_LIRF`) and clause 2;
- the promotion path: criteria 1–3 against E027 with rule L's disclosures; criterion 4 with H018 v2's clauses 1–2; criterion 6 through the reproduction blend; rule 1 S1 recording;
- the Missing Control 1 pre-registration;
- rules 2–12 as stated;
- CLASS-S.

## Advisor Prediction

These are for a v2 run of the same design.

Probability of improvement:

| Event | P |
|---|---|
| Clause 1 not met (H023 − E029 ≤ −1.0 s, q95 < 0, `NM_present_excl_LIRF`) | 0.35 |
| H023 − E029 below 0 on `NM_present_excl_LIRF` (point) | 0.75 |
| Clause 2 not met (all rows against E029 < 0) | 0.65 |
| Criterion 1 against E027 | 0.95 |
| S1 counted WIN against E027 | 0.07 |
| S1 LOSS against E027 | 0.25 |
| H018 v2 clauses 1–2 not met (> 3 h band ≤ 50; bulk < 0 on ≥ 3 of R1, R2, R3, W1) | 0.93 |
| Criterion 3 (no airport beyond +3 % against E027) | 0.90 |
| Promotion | 0.04 |

Expected magnitude:
- **H023 − E029, `NM_present_excl_LIRF`:** −1.8 to +0.3 s (central −0.7).
- **H023 − E029, all rows:** −1.5 to +0.5 s (central −0.5).
- **H023 − E027, all rows:** −1.5 to −3.5 s (central −2.5): E029's −2.04 s plus the blend's own effect.
- **S1 against E027:** −0.3 to +1.8 s (central +0.7).
- **Residual correlation, E029 against H021,** on the clause population: 0.92–0.97.
- **Row 192622644:** 4,500–8,000 s (P 0.85 below E027's 8,136 s).
- **Row 183910286:** 5,000–8,000 s.

Primary expected failure mode:
- **As written.** INVALID on the E028 route check, with certainty.
- **After revision.** The complementarity is real but small, about −1 s or less on normal taxis. That is about −0.3 s on S1's all-rows RMSE, and the lower prediction on row 192622644 costs more than that.
  - S1 is a TIE or a LOSS.
  - The record reads "complementary (or not), not promoted".
  - D3-C2 and D3-C3 stay in the champion.
