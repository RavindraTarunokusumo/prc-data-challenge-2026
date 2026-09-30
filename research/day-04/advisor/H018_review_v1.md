---
schema: advisor-review-v1
hypothesis_id: H018
proposal_version: 1
proposal_sha256: 2234bfb839a0ba2eaefe1e55ee2a63353d07c5b4f24abb9aced98886b8af485c
exchange_id: X-D04-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.88
created_utc: 2026-09-30T17:13:23Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE.**

**What is sound.** The treatment is the right one for D3-C2, and it is cleanly built:
- It changes one training-set rule, and E019 is its exact matched ablation (ruling R).
- The exclusion key is target-free and label P.
- The code does what the proposal says. Every other part of the design is acceptable as is (Revision).

**What must change.** Two pre-registration defects would make the run, as written, likely to produce a wrong record:

1. **Clause 1 does not test the claim it names.**
   - The out-of-range count is dominated by a d_sched band that D3-C2's mechanism does not touch. Predictions with `d_sched` < 1 h run 60–83 per 5-fold sum in *every* LightGBM fit, with or without T windows.
   - The congestion increment that D3-C2 explains sits almost entirely above 3 h. Against the matched no-T fit E021: +63 of +68.
   - So if the exclusion removes exactly the D3-C2 increment, the count lands near E021's 118. That is above the 93 threshold.
   - The record would then say "mechanism falsified… D3-C2's causal statement would need correcting", which is the opposite of what the data would show. Under B2 the promotion would also be barred.
2. **Rule 8 is misstated.**
   - "The LightGBM no longer learns the convention from LIRF" is false. The 932 LIRF NM-present block-at-schedule tail rows (Jan–Nov) stay in its training set.
   - That cell can decide S1, which is the WIN that promotion requires.

There are also four record items: an uncommitted evidence table, an arithmetic slip, a missing chain contingency, and `created_utc` values that post-date the commit containing the proposal.

**Verified here.** All checks were read-only, target-free or synthetic.
- **Constraints kept.** No December target was read, and no model was fitted or scored on a real fold. Development-fold truth was read only through `prc.evaluate.truth_frame`. Scratch scripts stayed outside the repository.
- **Hashes.**
  - The proposal matches the envelope.
  - The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json`.
  - `.claude/agents/advisor.md` is `30fff5dd…`, as in `config/agents.yaml`.
  - `uv.lock` is `39df945c…`, as in E019's gate record.
  - Silver is `efde4262…`, as in its manifest.
  - The X-D03-S01-0003 mirror verifies 4/4.
- **Predictions.** The files of E005, E006, E012, E015 and E017–E022 match their manifests, 8/8 each.
- **Code and tree.**
  - HEAD is `ff16c8b`. The only commit after `3298cc0` adds `docs/reproducibility/HANDOFF_D04.md`, so no code changed after submission.
  - `pytest`: 141/141 pass with caches disabled. `ruff`: clean.
  - There is no Day 4 allocation in the task ledger, and no worker is running.
- **`fs1` is unchanged by the Day 4 refactor.** `fs1` at `564f2c8` equals `fs1` at HEAD on all eight fold views (target-free: DEP block time and target nulled for every month), with identical `columns()`. `congestion.py` is unchanged, so FS2 is unchanged. The researcher had checked R3 and W1c only.
- **The exclusion.**
  - Excluded training rows per fold: R1 1,065, R2 1,233, R3 1,348, S1 866, W1 1,283, S1c 531, W1c 60, H 1,400. These match the proposal.
  - No categorical level of any FS2 categorical disappears from the LightGBM's training vocabulary on any fold. The category coding is therefore unchanged, and only rows and numeric bin boundaries change.
- **Out-of-range counts.** Re-derived with `range_check.py` (no `--json`, nothing written) for E006, E012, E015, E018, E020 and E021. They match the proposal: 123, 114, 125, 115, and E020 = E019 = 186. E021 (FS2_P) gives 118.

## Scientific Validity

### (a) The mechanism is supported by existing files, and it is T-specific

Out-of-range predictions on `NM_missing_other` bulk rows (y < 3,600 s), summed over the five development folds and split by `d_sched` band. Each cell gives below 0 s / above 3,600 s. Bulk rows per band: < 1 h (including negative `d_sched`) 2,760; 1–3 h 6,500; > 3 h 528.

| Fit | < 1 h | 1–3 h | > 3 h | Total |
|---|---|---|---|---|
| E017 (FS1, deterministic) | 60 (52/8) | 18 (8/10) | 14 (6/8) | 92 |
| E012 (FS1, bagged) | 76 (71/5) | 25 (17/8) | 13 (8/5) | 114 |
| **E021 (FS2_P: FS1 + P, no T)** | **83 (78/5)** | 17 (9/8) | **18 (9/9)** | **118** |
| E018 (FS0, deterministic) | 62 (49/13) | 12 (3/9) | 41 (39/2) | 115 |
| **E019 (FS2, champion)** | **83 (77/6)** | 22 (17/5) | **81 (48/33)** | **186** |

- **E021 is the matched no-T reference.** E019 is E021 plus the five T columns plus routing, and routing does not touch these rows.
- **The T block's increment is +68.** Of that, +63 is above 3 h, +5 is in 1–3 h, and 0 is below 1 h. This is exactly D3-C2's picture: SCHED-anchored T windows grow with the schedule delay and carry the convention learned from LIRF NM-missing rows.
- **H018 removes the named source and nothing else.** The mechanism is plausible, and clause 2 is a decisive accuracy test of it.

### (b) Clause 1 is mis-specified (Revision 1)

- **The < 1 h band is a generic LightGBM phenomenon.** It is mostly negative predictions: 60–83 in every fit, including the fits without T windows.
  - Nothing in D3-C2's mechanism acts on it. A T window starting at SCHED is short when the delay is short.
  - This band alone (83 in E019 and E021) is at the clause's threshold of 93.
- **What each hypothesis predicts:**
  - **D3-C2 as recorded** (the increment comes from LIRF convention rows through T windows): H018 falls to about E021's level. That is 118 ± about 22, using the proposal's own shift scale.
  - **The proposal's stronger expectation** (20–70): this also needs the < 1 h negatives to be LIRF-driven, so that the exclusion lowers the count below every no-T fit. No existing file tests that.
- **As written, the most likely outcome for a correct D3-C2 is "clause 1 met":**
  - a count in about 93–130, together with a large fall in the > 3 h band;
  - H018 is then recorded as falsified, and B2 bars its promotion even if criteria 1–3 pass;
  - the Alternative Explanations paragraph then records "D3-C2's causal statement would need correcting".

  All three readings would be wrong, and rule 10 forbids repairing them after the run.
- **The noise sentence is wrong.** "The margin is about 8 times the largest seed or procedure shift (22)": 186 − 93 = 93, which is about 4.2 times 22. "8 times" holds for the seed shift (11), not for the largest shift.

### (c) Rule 8: the LightGBM still learns the convention at LIRF (Revision 3)

- **The convention rows that remain.** From January to November, 932 of the 1,176 LIRF NM-present tail rows are block-at-schedule, and 931 of those have a normal anchor (`H009_review_v2.md`, `H012_review_v1.md`, STATE). H018 keeps them in the LightGBM's training set. It removes only the NM-missing half of LIRF's convention rows.
- **The rule 8 text needs correcting.** "It still sees `d_sched` on non-LIRF rows, where the convention is not recorded" also needs correcting: Day 1 found block-at-schedule at the other airports at or below base rates, which is not the same as absent.
- **Why it matters for promotion:**
  - On S1, E019's LIRF NM-present tail (271 rows) carries 10.4 % of the fold's SSE. `NM_missing_other`, the treated cell, carries 1.9 %.
  - How much the LIRF NM-present rows move S1 in fits that train on everything: replacing only E019's LIRF NM-present SSE by another fit's changes S1's all-rows RMSE by +1.75 s (E017), +1.09 s (E021), +2.44 s (E012) and −1.96 s (E018). On R1–R3 and W1 the change is within ±0.9 s for the FS1-based fits.
  - E019 − E017 on `NM_present_LIRF`, full: S1 −17.2 s, W1 +16.6 s.
- **The consequence.** H018's S1 outcome, and so its promotion, can be carried by the convention mixture on LIRF NM-present rows, in either direction. That mixture changes because about half of the convention rows leave training.
- **What rule 8 asks for.** The routing answer (X-D03-S01-0003 (e)) requires unrouted candidates to pre-register this exposure with an S1 expectation. H018's exposure is of the same kind, on the non-routed LIRF rows.

### (d) The code, reviewed as code (INC-0005)

- **`_routed`.**
  - The filter `~((role == train) & route_mask())` keeps every validation row.
  - `flt_missing` is `is_null()`-derived and never null.
  - The ridge still gets the full frame.
  - Absent or false gives the Day 3 path, a trivially equivalent refactor.
- **Tests.** The unit test checks the three properties the proposal states.
- **`route_check.py <H018> - E005`.** It checks the routed subgroup only. The property "non-routed rows equal a LightGBM fitted without the routed training rows" is therefore verified synthetically, not on real data. That is acceptable, since the code path differs from the real-data-verified E019/E020 path only by the filter.
- **`range_check.py`.** It re-derives every cited figure (above).

## Novelty Relative to Existing Research

- **It is the first training-set treatment in the run.** It answers Day 3 open question 1 (D3-C2) directly and is not redundant with any journal entry.
- **The prediction-time alternative** (clipping) is correctly declined. The Day 1 clip attribution already showed that clipping is a secondary mechanism.

## Experimental Isolation

- **One change against E019: the LightGBM's training rows.**
  - Features are identical: `fs1` is identical on all folds and congestion is unchanged.
  - The categorical vocabulary is identical.
  - The routed rows are E005's.
- **What the change moves, beyond `NM_missing_other`:**
  - the numeric bin boundaries;
  - the first trees, because the removed rows have the largest squared-loss gradients in the training set;
  - the LightGBM's convention mixture on LIRF NM-present rows ((c)).
- **The last of these is a direct consequence of the treatment, not an "unsigned perturbation".** It needs its own pre-registered expectation (Revision 3).
- **The ablation is exact.** E019 remains the exact ablation for everything H018 claims.

## Validation Quality

- **Folds and criteria.**
  - The frozen folds are used unchanged, and the seasonal fold is included.
  - Clause 2 counts R1, R2, R3 and W1: the four folds where E019 lost to E017 on the treated cell (+76.9 to +233.8 s bulk; verified in `E019_vs_E017.json`).
  - B2 (a falsified candidate is not promoted) and B3 (an S1 WIN with S1c point dRMSE ≥ 0 is an unresolved objection) apply. B2 is why Revision 1 is blocking and not cosmetic.
- **Twin disclosure.** On `NM_missing_other` bulk, E019 − E017 is −141.0 s on W1c and −17.9 s on S1c, against +76.9 s on W1 and −31.5 s on S1. The twins do not share W1's sign. Report H018's twin cells beside W1 and S1 in the analysis.

## Leakage Review

### Target Leakage

PASS

- The exclusion uses `ADEP_mvt` and `flt_missing` (label P, target-free) on training rows only.
- No new input is added. No validation target is available to the fit, since it is null in the masked view.

### Temporal Leakage

CONCERN

This is carried from Day 3 and is not blocking.
- FS2's T features (the in-taxi counts and the `d_*` deltas) are unchanged.
- The SCHED-anchored T windows on NM-missing rows remain inputs, and H018's mechanism depends on how the model uses them.

### Competition Availability

CONCERN

This is carried (D3-C3) and is not blocking.
- Every input exists in the ranking files.
- The rows the treatment targets are 2.0–2.6 times the 2025 maximum in January 2026: 435 non-LIRF NM-missing rows over 3 h and 92 over 5 h.
- July 2026's 39 rows over 5 h are slightly above the 2025 maximum of 36.
- No development fold samples January's exposure (proposal rule 2, correctly stated).

## Compute Review

### RAM

PASS

E019 peaked at 4.76 GB, and the treatment only removes about 0.04–0.08 % of training rows. CLASS-M allows 8 GB, with a hard limit of 11 GB.

### Runtime

PASS

- E019 took 954 s on an "@ 2.10GHz" host, the host string of this container. E022 took 1,339 s on "@ 2.80GHz".
- The 15–25 min estimate is inside the 30 min CLASS-M target, and the runner stops at 45 min.

### Disk

PASS

About 10 MB of predictions, git-ignored and covered by the manifest.

## Weakest Assumption

**That the out-of-range predictions below 1 h of schedule delay come from the same LIRF source as those above 3 h.**
- The proposal's expected 20–70 needs it.
- Every no-T fit contradicts it on its face: 60–83 in the < 1 h band, whatever the feature set.
- Clause 1's threshold sits exactly where this assumption decides the outcome.

## Missing Control or Ablation

- **Named, not required.** An FS1 or FS2_P fit with the same exclusion would decide the stronger claim: do LIRF NM-missing training rows drive the no-T fits' out-of-range predictions? It is needed only if the researcher keeps that claim inside a falsification clause.
- **Required as a pre-registration, not a run.** State the rule 8 expectation for `NM_present_LIRF` (Revision 3).

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- There is no allocation of H018 v1, and H019 v1 and H020 v1 cannot be allocated on its base.
- **No fit of any configuration with `route_train_exclude: true` on a frozen fold** before an H018 version ≥ 2 is ACCEPTED and acknowledged. Its outcome is H018's outcome.
- **Still allowed:**
  - target-free checks;
  - EDA on never-validation months under the Day 2–4 hygiene;
  - synthetic tests;
  - comparisons of existing prediction files, including rule 12 re-derivations like those above.

Required acknowledgement path: none for v1. Submit `research/day-04/proposals/H018_v2.md` in a new exchange.

## Revision

**Required (minimal):**

1. **Clause 1 and its reading.**
   - State which claim clause 1 tests. It can be D3-C2 as recorded (the congestion increment), or the stronger claim that LIRF NM-missing training rows drive the out-of-range predictions of any LightGBM, or both, as separate clauses.
   - Pre-register the reading of each outcome region consistently with the band evidence in (a).
   - A count inside the range of the no-T-window fits must not be read as refuting D3-C2's statement about the increment. That range is 92–125: E017, E012, E018, E021, E006, E015.
   - The statistic, bands, population and thresholds are the researcher's choice.
   - Rewrite the Alternative Explanations paragraph to match.
   - Since B2 applies, state which clauses are falsification clauses (they bar promotion) and which are disclosures.
2. **Noise scale and evidence.**
   - Correct "about 8 times" to about 4.2 times the largest shift (22), or restate the comparison.
   - Add E021 (FS2_P, 118) as the matched no-T reference.
   - Commit the `range_check.py` output for every experiment the proposal cites. The cited `range_check_baseline.json` holds only E005, E017 and E019. The E006, E012, E015 and E018 figures are uncommitted, although they re-derive exactly.
3. **Rule 8.**
   - Replace "The LightGBM no longer learns the convention from LIRF". State that the LIRF NM-present block-at-schedule tail rows (932 in Jan–Nov) and the non-LIRF block-at-schedule rows (at base rates) stay in training.
   - Pre-register the expected direction and rough size of H018 − E019 on `NM_present_LIRF`, full and tail, per development fold, with the S1 expectation at July's rate (S1 has 271 LIRF NM-present tail rows).
   - State how a promotion is recorded if its S1 outcome is carried by that cell (rule 1 attribution).
4. **Chain contingency.** If clause 3 makes the H018 run INVALID, no later chain step is allocated on this code path until a new version is accepted.
5. **Record.**
   - `created_utc` must be measured. v1's 17:05:00Z post-dates the commit that contains the proposal (`3298cc0`, 16:51:03Z), and the envelope's 16:51:03Z.
   - Add INC-0004 to the provenance line: `SESSION_START.md` records that it covers D04-S01.

**Acceptable as is:**
- the treatment, as implemented at `7ea6b55`, and its unit test;
- E019 as the matched reference and exact ablation;
- clause 2, and clause 3 with its consequence;
- the promotion path (criteria 1–3 against E019, criterion 6 with SHA-256 equality recorded, criterion 8 unchanged);
- the frozen-tools list, the Validation Plan (including `--by-dsched`), the class;
- rules 1–7 and 9–12, except as amended above.

**Process notes (non-blocking):**
- **INC-0005.** The delegated code (`range_check.py`, the `route_check.py` `-` mode) was reviewed here on its merits, with no defect found.
- **INC-0004** was not re-measured in this review.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| H018 − E019, all rows, development mean < 0 | 0.80 |
| Out-of-range count above 3 h (5-fold sum) falls from 81 to ≤ 30 | 0.80 |
| Out-of-range count below 1 h stays within 60–95 | 0.70 |
| v1 clause 1 met (5-fold total > 93) | 0.70 |
| Clause 2 not met (`NM_missing_other` bulk < 0 on at least 3 of R1, R2, R3, W1) | 0.85 |
| S1 WIN on all rows against E019 | 0.30 |
| Promotion under criteria 1–3 and B2, with a clause 1 restated as in Revision 1 | 0.20 |
| Promotion as written in v1 (B2 with v1's clause 1) | 0.07 |

Expected magnitude:
- **Out-of-range, 5-fold total:** about 110 (80 % interval 80–135).
- **`NM_missing_other` bulk against E019:** −40 to −200 s on R1, R2, R3 and W1; S1 within ±30 s.
- **All rows against E019:** mean −0.5 to −3 s. The W1 fold gains most (`NM_missing_other` is 10.8 % of E019's W1 SSE). S1 is decided by `NM_present_LIRF` and perturbation.
- **`NM_present_excl_LIRF` against E019:** within ±3 s per fold. The removed rows dominate the first trees' gradients, so the shift may exceed the ±2 s perturbation scale.

Primary expected failure mode:
- **Primary.** The exclusion removes the above-3 h out-of-range predictions (D3-C2 confirmed), but the below-1 h band does not move. The total lands between 93 and about 130. Under v1, clause 1 then records the mechanism as falsified, B2 bars a promotion the data would support, and the record wrongly corrects D3-C2.
- **Secondary.** The treated cell improves on four folds, but S1, the required WIN, is decided by the changed convention mixture on LIRF NM-present tail rows, a cell v1 does not pre-register.
