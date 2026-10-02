---
schema: advisor-review-v1
hypothesis_id: H023
proposal_version: 3
proposal_sha256: 41712f57b3befe4ad4a342bc129a6e447b1fd31c1e01b2070dab4903da83eec2
exchange_id: X-D05-S04-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.88
created_utc: 2026-10-01T20:35:39Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.88).**
- v3 meets all five required revisions of `H023_review_v2.md`.
- The v2-to-v3 diff changes nothing else.

**v2 required revisions:**

| v2 item | v3 | Verdict |
|---|---|---|
| 1. Criterion 7 | Stated once: H021's class is CLASS-L, for H021 and H021r. "(CLASS-M, GPU)" and "declares its class from measured RAM" are removed. The CLASS-M comparison and swap use are reported beside criterion 7. If H021 or H021r is outside CLASS-L, H023 fails criterion 7 | **Met.** The Resource Estimate reads "H021 (CLASS-L, GPU)". The one remaining "H021 v2's measured RAM" is in the historical v1-to-v2 change log |
| 2. INCONCLUSIVE clause 1 | Bars promotion (criterion 4 not satisfied); H023r is then not due | **Met** |
| 3. H023r integrity | `route_check.py <H023r> - E029`, with H021r's own check as the allocation precondition. A failure makes H023r INVALID for criterion 6 | **Met** |
| 4. Tools freeze | As H021 v3 | **Met.** Anchor `803ceeb` (`H021_review_v3.md`) |
| 5. Clerical | "E026 and E027"; references follow H021 v3 | **Met** |

**Verified here.** All checks are read-only.
- **`prc.blending` reads only `manifest["artifacts"]`** from a component's manifest. The new `environment` key leaves it unchanged.
- **The environment record** adds about 37 MB at the end of a blend-like worker. LightGBM, CatBoost and XGBoost are first imported there; scipy, scikit-learn and pandas are already loaded. H023's ~3.5 GB stays inside CLASS-S's 4 GB.
- **E029's manifest** lists 8 prediction artifacts.
- **No allocation since E029.** The next id is E030.

**Readings under which this ACCEPT is given.** These are non-blocking, and bind as stated.
1. **A second INCONCLUSIVE source.** v3 also reads H023's clause 1 as INCONCLUSIVE when H021's pair is not matched under H022 v3's closed set.
   - That fact concerns H021's mechanism claim, not H023's complementarity, which is scoped to "this CatBoost configuration".
   - It therefore adds no validity, and costs a little power (P ≈ 0.03).
   - It is conservative and pre-registered, so it stands. It cannot be dropped after the run.
2. **Criterion 6 when H023r cannot be run.**
   - H023r may not be allocatable, because H021r failed its route check or ended in RESOURCE_FAILURE (the chain then stops). Or H023r may be INVALID by its own route check.
   - In each case, criterion 6 is **not satisfied** and H023 is not promoted (brief §10 item 6). It is not "not applicable".
3. **The Validation Plan's last line** ("Reproduction only if criteria 1–3 pass against E026 and no clause is met") is a necessary condition.
   - The full H023r rule is in Gating and in the INCONCLUSIVE section. It adds that clause 1 is not INCONCLUSIVE, and that H021r has passed its route check.
   - Read together, the three are consistent.
4. **Freeze verification:** as `H021_review_v3.md` execution note 2. The rule covers `config/`.

## Scientific Validity

### (a) The expected gain is small, and clause 1 is a fair test

Unchanged from v1 and v2.
- At a 6 s component gap, an equal-weight blend gains 1 s on normal taxis only if the residual correlation is about 0.92 or less.
- My prior is 0.93–0.96.
- The −1.0 s threshold therefore sits near the expected value, which makes clause 1 decisive in both directions.

### (b) The noise condition is a proxy

Unchanged.
- |m| / 2 approximates the blend's re-draw sensitivity.
- H023r's own clause 1 reading is recorded beside it when H023r runs.
- "The primary reading stands" is consistent with criterion 6, which re-checks criteria 1–3 only.

### (c) S1 and the single row

Unchanged.
- An S1 LOSS against E026 is a real possibility.
- Missing Control 1's pre-registration covers its direction.

### (d) Criterion 7 is single and consistent

- It reads H021, and now H021r, against CLASS-L (90 min, 11 GB), as ruled in `H021_review_v2.md`.
- The CLASS-M comparison and swap use are disclosed beside it.
- A swapping run is not called within class on RSS alone (INC-0010).

## Novelty Relative to Existing Research

- **This is the project's first ensemble,** and it answers Day 5's architecture question for this configuration.
- **It is not a re-adjudication of E023.** Rule L v2 item 3 applies, and B2 bars promotion on E023's known margin alone.

## Experimental Isolation

- **Against E029: exact.** H023 − E029 = ½ (H021 − E029).
- **Attribution beyond "this configuration"** would need the named E029 + H022 blend, which is not claimed.

## Validation Quality

**The validation design is correct:**
- the frozen folds;
- criteria 1–3 against E026, with rule L v2 item 4's flags;
- criterion 4, with B2 and H018 v2's clauses 1–2;
- criterion 6 through [E029, H021r], with both route checks;
- criterion 7 against CLASS-L;
- criterion 8 against E028, with a 200 s margin;
- B3 against E026;
- the rule 1 S1 recording;
- Missing Control 1.

**The v2 gaps are closed.**

## Leakage Review

### Target Leakage

PASS

- The weight is fixed a priori, and nothing is fitted.
- The blend reads only manifest-verified prediction files, never truth (`test_blending_does_not_import_truth`).

### Temporal Leakage

CONCERN

This is inherited, not blocking: FS2's T features in both components, and the CTRs over post-validation months in S1 and W1. The twins bound them.

### Competition Availability

PASS

- Both components can predict SUBMIT_JAN and SUBMIT_JUL.
- A submitted blend needs a SUBMIT run of a stochastic GPU component. The Day 7 procedure is untested. Non-blocking.

## Compute Review

### RAM

PASS

About 3.5 GB, plus about 37 MB from the environment record. That is inside CLASS-S's 4 GB, with little margin.

### Runtime

PASS

1–3 min.

### Disk

PASS

About 10 MB.

## Weakest Assumption

**That a CatBoost about 6 s worse on normal taxis is decorrelated enough from E029** for an equal-weight average to gain at least 1 s. It needs a residual correlation of about 0.92 or less.

## Missing Control or Ablation

**The E029 + H022 equal-weight blend.**
- It is required only if complementarity is attributed to categorical handling.
- The claim is scoped to "this CatBoost configuration", so it is not required.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
1. **Primary run.** One allocation, `gate.py allocate H023 v3`.
   - **When:**
     - H021 v3's primary run is COMPLETE and has passed `route_check.py <H021> - E029`;
     - H021's reproduction has run, in the order of H021 v3's Validation Plan;
     - the chain has not stopped under H021's or H022's RESOURCE_FAILURE rule.
   - **No accuracy condition gates it.**
   - **Config:**
     - `model: blend`, `components` [E029, H021's primary E###], `weights` [0.5, 0.5];
     - `feature_set: FS0`, `folds` all 8, `seed: 42`, `job_class: CLASS-S`.
2. **Reproduction.** One allocation, `gate.py allocate H023 v3 --purpose reproduction`.
   - **Config:** `components` [E029, H021r's E###], `weights` [0.5, 0.5], `seed: 43`, CLASS-S.
   - **Only if:**
     - criteria 1–3 pass against E026;
     - no clause is met;
     - clause 1 is not INCONCLUSIVE, for either reason;
     - H021r has passed `route_check.py <H021r> - E029`.
   - **Then:** `route_check.py <H023r> - E029` and `reproduce_check.py <H023r> <H023> --champion E026`.
3. **Post-run steps:** exactly those of the Validation Plan.
4. **Preconditions:** as `H021_review_v3.md`, Execution Authorization item 4:
   - anchor `803ceeb` for every path outside the record directories;
   - rule L v2 item 6's environment;
   - a clean tree, and no experiment running.
5. **Promotion only through the stated path:**
   - criteria 1–8 as written;
   - B2, H018 v2's clauses 1–2, and B3 against E026;
   - readings 1–2 of the Summary.
6. **Not authorized:**
   - any other weight or component, including the E029 + H022 blend;
   - a re-run of E029;
   - holdout access in this chain;
   - a re-adjudication of E023.

Required acknowledgement path: `research/day-05/acks/H023_ack_v3.md`. It references the proposal hash above and this review's hash.

## Revision

None required.

## Advisor Prediction

These are for this v3 run.

Probability of improvement:

| Event | P |
|---|---|
| Clause 1 not met (H023 − E029 ≤ −1.0 s, q95 < 0, `NM_present_excl_LIRF`) | 0.35 |
| H023 − E029 below 0 on `NM_present_excl_LIRF` (point) | 0.75 |
| Clause 2 not met (all rows against E029 < 0) | 0.65 |
| Clause 1 INCONCLUSIVE, for either reason | 0.15 |
| Criterion 1 against E026 | 0.95 |
| S1 counted WIN against E026 | 0.07 |
| S1 LOSS against E026 | 0.25 |
| H018 v2 clauses 1–2 not met | 0.93 |
| Criterion 3 (no airport beyond +3 % against E026) | 0.90 |
| H023r due | 0.05 |
| Promotion | 0.04 |

Expected magnitude:
- **H023 − E029, `NM_present_excl_LIRF`:** −1.8 to +0.3 s (central −0.7).
- **H023 − E029, all rows:** −1.5 to +0.5 s (central −0.5).
- **H023 − E026, all rows:** −1.5 to −3.5 s (central −2.5).
- **S1 against E026:** −0.3 to +1.8 s (central +0.7).
- **Residual correlation, E029 against H021,** on the clause population: 0.92–0.97.
- **Row 192622644:** 4,500–8,000 s (P 0.85 below E026's 8,136 s).

Primary expected failure mode:
- The complementarity is real but small, and S1 is a TIE or a LOSS against E026.
- The record reads "complementary (or not), not promoted", and D3-C2 and D3-C3 stay in the champion.
