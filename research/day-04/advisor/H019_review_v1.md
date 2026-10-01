---
schema: advisor-review-v1
hypothesis_id: H019
proposal_version: 1
proposal_sha256: 0d2535d466bf00ff28a5004fb0168aa6a8b1bb461b0a62502d5b60716e2bef0c
exchange_id: X-D04-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.82
created_utc: 2026-09-30T17:15:11Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE.**

**What is sound.** H019 asks the brief's Day 4 question, in the champion's learner and against a matched base.
- The prior block is well built. It uses leave-one-month-out (LOMO) arithmetic, fold-local sources, M fixed a priori, and airport-qualified keys that are already admitted inputs. The code is correct.
- The mechanism clause is decisive against perturbation, and more so than the proposal argues ((c)).

**What must change.** Two points are blocking, and three are record items:

1. **W1c is inert by construction.**
   - W1c has one training month, so every W1c training row gets null priors in four columns and a constant `pr_stand_rwy_logn` of 0. LightGBM ignores such columns.
   - So H019's W1c predictions will equal H018's byte for byte. W1c is a TIE with dRMSE 0.0, not "a LOSS with probability 0.5".
   - The W1 causal twin is therefore vacuous for the prior block. A W1 WIN would count with no causal check, although 8 of the 9 months that build W1's validation priors lie after February.
   - The proposal's pre-registered W1c reasoning rests on a false premise and must be replaced.
2. **The chain contingency is missing.**
   - Nothing says what happens if the H018 base run is INVALID.
   - Nothing says how criterion 4 and B2 treat H018's carried change when H019's promotion contrast is against E019.
3. **Rule 8 is misstated** (the same error as H018 v1).
4. **Two evidence items are missing.** The joint-key figures are uncommitted, and the rule that selected the five columns is not stated.
5. **The `created_utc` post-dates the commit** that contains the proposal.

**Dependency.** H019's base is H018, which is also REVISE. H019 v2 should name the H018 version it builds on.

**Verified here.** The shared integrity checks are listed in `H018_review_v1.md`: hashes, frozen files, predictions, 141/141 tests, `ruff`, and `fs1` identical on all eight folds. Specific to H019, all read-only, target-free or synthetic:
- **`src/prc/priors.py`, reviewed as code (INC-0005).**
  - LOMO is implemented as total minus own-month sums and counts per key, at every level of the hierarchy: airport mean, K2 parent, K5, K3, K6, K7.
  - Null keys never match a group, because polars joins do not match nulls, so they fall back to the parent.
  - The source is `role == "train"` rows that are NM-present with y < 3,600 s. Validation rows have no source rows in their month, so they use all training months.
  - `tests/test_priors.py` covers own-month exclusion, validation-target independence, the source filter, hand-computed values and FS3 ⊇ FS2.
  - The single-training-month behaviour stated in the docstring is untested. It was verified here.
- **Real W1c view** (DEP targets replaced by a constant, block times nulled; no target read):
  - all 153,706 training rows have null `pr_stand_rwy`, `pr_rwy_hour`, `pr_op` and `pr_actype`, and `pr_stand_rwy_logn` = 0.0;
  - all 143,732 validation rows are populated;
  - S1c and W1 training rows are fully populated.
- **Synthetic LightGBM test.** Through `gbm.lightgbm` with E019's parameters, adding four all-null prior columns and one constant-zero column (populated in validation) leaves the predictions byte-identical to the fit without them.
- **EDA.**
  - Every Observation figure except the joint-key figures matches `priors.json` and `priors_summary.md`: incremental R², within-airport stability and K5 coverage.
  - `scripts/eda_day4.py` reads targets only for Jan, Mar–Jun and Aug. December is masked by `load_silver`.

## Scientific Validity

### (a) The prior block is correct as implemented

- **No training row's features contain its own target, or any target of its own calendar month.**
- **The parents are LOMO too.** A training row's airport mean and runway parent also exclude its month, so no own-month information enters through the hierarchy.
- **No leak through the count.** The count feature `pr_stand_rwy_logn` counts other months' NM-present bulk rows, so it does not depend on the row's own month.

### (b) W1c cannot test the block, and W1 is left without a causal check (Revision 1)

- **The mechanism.**
  - W1c trains on January only, so LOMO leaves no other month and the training priors are null, or 0 for the count.
  - LightGBM removes features that cannot be split, so the W1c model is H018's W1c model.
  - This is verified on the real view and in a synthetic fit ("Verified here").
- **Consequences for v1:**
  - **Expected Result:** "W1c: structurally degraded; LOSS possible" and "a W1c LOSS is expected with probability 0.5" are wrong. The outcome is W1c = H018 exactly.
  - **Validation logic:** "Under the twin rule, a W1c LOSS voids a W1 WIN… This is pre-registered, not a post-hoc exclusion" rests on that false premise. A TIE never voids W1.
  - **What is actually true:**
    - W1's validation priors come from January plus April–November, so 8 of the 9 source months lie after the validation month.
    - The frozen twin rule is met vacuously for the block.
    - No fold checks W1's prior gain causally.
    - The R folds are causal, and S1c (six training months) is an informative twin.
- **W1 carries a specific risk.** The LFPG August–November runway regime enters W1's validation priors for February. The proposal names this break for LFPG but not for W1.

### (c) Clause 1 is decisive, for a better reason than the proposal gives

- **The proposal's argument.** It justifies −3.0 s as 1.5 times the largest fold-level shift (1.96 s), plus the WIN pattern.
- **The relevant noise scale for a development-mean floor is the development-mean shift.** In the three committed perturbation contrasts on `NM_present_excl_LIRF` it is +0.25 s (E015 − E012), −0.24 s (E017 − E012) and −0.12 s (E018 − E006).
- **The floor is at least 12 times these.** None of the three contrasts has more than one counted WIN (verified in the JSONs).
- **Clauses 1(a) and 1(b) are decisive against perturbation as written.** No change is required.

### (d) What the EDA can and cannot support

- **What it measured.** The EDA measures increments over K1 (airport × local scheduled hour) in a linear model whose K1-only RMSE is 327 s, on NM-present bulk rows.
- **What it did not control.** It has no anchor control. FS2 already contains:
  - `d_aobt3`;
  - `stand` (levels with ≥ 100 training rows);
  - `airport_runway`;
  - `op_prefix` and `actype`;
  - 255-leaf trees that can form stand × runway interactions.
- **Day 3's lesson applies.** There, the EDA figure partly re-measured the anchor, and the model gain was far below it.
- **What this means for the estimate.** K5's +0.19 R² is a loose upper bound. The proposal's −2 to −7 s is plausible at its low end only. This is a prediction (see below), not a defect: the clause tests it.

### (e) Selecting the five columns

- **The EDA's single-key ranking** is K5 +0.189, K4 +0.128, K6 +0.087, K8 +0.078, K9 +0.078, K7 +0.068, K3 +0.060.
- **FS3 keeps K5, K3, K6 and K7.** It drops K4 (subsumed), and also K8 and K9, which rank above K7 and K3.
- **The selection rule is not stated.** For K9, `ades` is label F on diversions, which may be the reason.
- **The multi-key figures behind the choice are not in any committed file:** [K1, K5] 0.4505; [K1, K4, K5] 0.4504; +0.007 for K3, K6, K7 and K9 together.
- **The selection used only never-validation months, which is legitimate.** The record needs the rule and the numbers.

### (f) The usual out-of-fold skew (disclosure)

- **Training priors use N − 1 months; validation priors use N.**
  - `pr_stand_rwy_logn` shifts accordingly. On the real views, the training and validation maxima are 7.769 and 7.857 on W1, and 7.230 and 7.373 on S1c.
  - The shrinkage weight differs by the same factor.
- **In the R folds**, validation priors are past-only, while training priors mix past and future months.
- **This is standard for out-of-fold target encoding and not blocking.** State it once in the record.

## Novelty Relative to Existing Research

- **This is the run's first target statistic.** It is the brief's named Day 4 question, and nothing in the journal is redundant with it.
- **It is not a re-submission of FS1.** The keys are raw-level and interaction keys that FS1 collapses at 100 rows or represents only separately.

## Experimental Isolation

- **One change against the H018 base: five appended numeric columns.**
  - The FS2 part is bit-identical: `fs1` is identical on all folds, congestion is unchanged, and `test_fs3_extends_fs2` checks the column order.
  - The training rows are identical: same exclusion, same vocabulary.
- **The block-level claim is stated honestly.** K5 is named as the expected carrier, not tested separately.
- **W1c is not an isolation of anything** for this block ((b)).

## Validation Quality

- **The frozen folds are used unchanged**, and the S1 WIN is required.
- **B2 and B3 apply.**
- **Where causal checks hold:** the R folds are causal and S1c is informative.
- **W1 has no functional twin** for the treatment (Revision 1).
- **Clause 2** (all rows, mean ≥ 0) is a conservative guard. On S1, the LIRF NM-present tail alone can move all-rows RMSE by about ±2 s (`H018_review_v1.md` (c)), so clause 2 can be met by a cell unrelated to the priors. The proposal accepts that risk by design, and I do not require a change.

## Leakage Review

### Target Leakage

PASS

- **LOMO holds.** Own-month exclusion holds at every level of the hierarchy, validation targets are unused, and the source filter reads training rows only.
- **The single-month case yields nulls**, never same-month values (verified).
- **No December target enters a development or H prior.** H trains on January–November.

### Temporal Leakage

CONCERN

This is not blocking.
- **S1's and W1's validation priors use post-validation months.** That is the frozen non-causal fold design.
- **S1c checks S1.** No fold checks W1 for this block ((b)).
- **FS2's T features are inherited.**

### Competition Availability

PASS

- **Every key exists in the ranking files:** stand, runway, operator prefix, aircraft type and local scheduled hour, all FS0/FS1 inputs.
- **K5 coverage is high.** The share of rows whose key has ≥ 30 training rows is 0.968 for January 2026 and 0.958 for July 2026.
- **The source is narrower than the EDA's count.** Coverage was counted on all DEP rows, but priors use only NM-present bulk rows, so the effective n is somewhat lower. State this beside the coverage figure.

## Compute Review

### RAM

PASS

The FS3 smoke on R3 peaked at 5.1 GB, including a duplicate FS2 build, against CLASS-M's 8 GB.

### Runtime

PASS

The block adds about 6 s per fold to E019's 954 s class of run.

### Disk

PASS

About 10 MB.

## Weakest Assumption

**That FS2's LightGBM does not already extract most of the stand × runway route effect** from `stand`, `airport_runway` and the anchor. The EDA cannot speak to it, because it has no anchor or FS2 control.

## Missing Control or Ablation

Both are named, not required:
- **A within-key permuted prior**: the same marginal values, with the key–target link broken. It would separate route information from re-encoding and regularisation, the proposal's first Alternative Explanation.
- **A K5-only block.** The proposal declines it for budget. That is acceptable, given the block-level claim.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- There is no allocation of H019 v1.
- **No FS3 fit on a frozen fold** before an H019 version ≥ 2 is ACCEPTED and acknowledged, and its H018 base run is complete. Its outcome is H019's outcome.
- **Still allowed:**
  - target-free checks;
  - never-validation-month EDA under the Day 2–4 hygiene;
  - synthetic tests;
  - comparisons of existing prediction files.

Required acknowledgement path: none for v1. Submit `research/day-04/proposals/H019_v2.md` in a new exchange, with the H018 version it builds on.

## Revision

**Required (minimal):**

1. **W1c and W1.**
   - Replace the W1c expectation. With one training month the block is inert: H019's W1c predictions equal H018's, and W1c is a TIE with dRMSE 0.0.
   - Remove the "LOSS with probability 0.5" reasoning.
   - State how W1 enters clause 1(a), given that its twin cannot check the block. Either count it under the frozen rule with disclosure, or keep it out of the mechanism clause; the choice is the researcher's.
   - Record that W1's validation priors are built from 8 post-February months.
   - Add the unit test for the single-training-month behaviour that the `priors.py` docstring states.
2. **Chain contingency.**
   - If the H018 base run is INVALID, H019 is not allocated.
   - If H018 is not promoted, H019's promotion contrast against E019 carries H018's change. State whether H018's falsification clauses form part of H019's criterion 4 in that case.
   - State how B2 applies if H018's own criterion was met.
3. **Rule 8.** Replace "no convention bet" with the inherited exposure: the Tier 1 fit still trains on the LIRF NM-present block-at-schedule tail rows (`H018_review_v1.md` (c)). The priors' source (NM-present, y < 3,600 s) excludes the tail.
4. **Evidence for the key set.**
   - Commit the joint-key computation and its output, or drop those figures.
   - State the rule that selected K5, K3, K6 and K7 and excluded K4, K8 and K9.
   - State the NM-present bulk source beside the coverage figure (Competition Availability).
5. **Record.**
   - Use a measured `created_utc`. v1's 17:25:00Z post-dates the commit that contains it (`3298cc0`, 16:51:03Z).
   - Add INC-0004 to the provenance line.

**Acceptable as is:**
- the prior definitions: keys, hierarchy, M = 50, LOMO, source filter;
- H018's configuration as the matched base, with only `feature_set` changed;
- the extended tools freeze (`priors.py` and the `fs3` body);
- clauses 1(a) and 1(b) (subject to item 1 for W1) and clause 2;
- the promotion path, criterion 6 with SHA-256 equality, criterion 8;
- the class;
- the Validation Plan and its disclosures (per-airport against H018, LFPG named);
- the block-level Required Ablation, the Alternative Explanations;
- rules 1–7 and 9–12.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| H019 − H018 on `NM_present_excl_LIRF`, development mean < 0 | 0.80 |
| The same mean ≤ −3.0 s (clause 1(b) not met) | 0.30 |
| Criteria 1–2 met on `NM_present_excl_LIRF`, twin rule included | 0.50 |
| Mechanism supported (neither clause met) | 0.25 |
| W1c predictions identical to H018's (dRMSE 0.00) | 0.99 |
| All rows, development mean < 0 | 0.70 |
| Promotion (criteria 1–3 against the champion in force, B2) | 0.15 |

Expected magnitude:
- **`NM_present_excl_LIRF`:** −0.5 to −4 s (central −2 s). Largest at LFPG, EGLL and LTFM.
- **W1** is the weakest development fold: its February priors include LFPG's August–November regime.
- **All rows:** −0.5 to −3 s.
- **W1c:** exactly 0.

Primary expected failure mode:
- **Primary.** A real but small gain, below the −3.0 s floor. FS2 already holds most of the route effect through `stand`, `airport_runway` and the anchor, and the EDA's increments were measured over airport × hour only.
- **Secondary.** If the gain does clear the floor, criterion 2 may rest on a W1 WIN that no fold checks causally.
