---
schema: advisor-review-v1
hypothesis_id: H019
proposal_version: 2
proposal_sha256: df74347ccaeeb6f1b48b5089744010ce8951b943365792f49e74c3664e1d2c6d
exchange_id: X-D04-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-09-30T17:46:13Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.80), on H018 v2 as its base** (`H018_review_v2.md`).
- The prior block, its matched reference and its clauses are sound.
- Three readings are fixed in the authorization, and the acknowledgement adopts them before any run. None changes the design.

**All five required revisions of `H019_review_v1.md` are met.**

| v1 revision | What v2 does | Checked here |
|---|---|---|
| 1. W1c and W1 | W1c is inert (TIE, dRMSE 0.00), and the "LOSS with P 0.5" reasoning is removed. W1 is out of clause 1(a)'s WIN count, and its 8 post-February source months are recorded. The single-training-month unit test is added | The test is non-vacuous. The S1 twin rule needs a reading ((b)) |
| 2. Chain contingency | If the base run is INVALID, H019 is not allocated. If H018 is not promoted, H018's clauses 1–2 join criterion 4, and B2 applies | Present. The comparator term is made operational (item 4(b)) |
| 3. Rule 8 | The inherited exposure replaces "no convention bet" | One sentence overreaches ((d)) |
| 4. Key-set evidence | The selection rule is stated, the joint figures are committed, and the source is stated beside coverage | The figures match `priors_joint.json` to 4 decimals ((e)) |
| 5. Record | Measured `created_utc`; INC-0004 in the provenance line | Checked |

**The acknowledgement must fix three readings before any run** (item 4 and the ack).
1. **The WIN count in clause 1(a), and the S1 twin rule.**
   - v1's clause read "fails criterion 1 or criterion 2 (twin rule included)", and the v1 review accepted it.
   - v2 rewrote the clause to take W1 out of the count. The words "twin rule included" disappeared, and nothing says so.
   - So v2 no longer says whether an S1 WIN counts when S1c is a LOSS. Rule 10 forbids settling that after the run.
   - The reading adopted here is the frozen rule, `fold_outcome_counted`. It is what v1 accepted, and what "W1 is kept out … because its twin cannot check the block" presupposes.
   - `mechanism_check.py`'s `criterion_2` field still counts W1, so it is not the clause.
2. **"Promoted first in this chain".** This decides H019's comparator and what criterion 4 contains. `H018_review_v2.md` item 7 defines it.
3. **The Implementation Plan reads `gate.py allocate H019 v1`.** It must read v2.

**Two record corrections and one disclosure** are also required ((a), (d)).

**Verified here.** The integrity checks shared with H018 are in `H018_review_v2.md`: hashes, frozen files, 80 prediction files, 143/143 tests, `ruff`, a clean tree and no container reset. The checks specific to H019 were target-free, synthetic, on never-validation months, or comparisons of existing files.
- **Code.**
  - `src/prc/priors.py` and the `fs3` body are unchanged since the v1 review (`7ae934f`).
  - **The new test, `test_single_training_month_priors_are_inert_for_lightgbm`, is non-vacuous.** `columns()` includes `PRIOR_NUMERIC`, so the five columns reach the LightGBM.
  - It uses 5 rounds and 7 leaves on 300 rows, not E019's parameters. The v1 review checked E019's parameters and the real W1c view, and the property (a single-bin feature is never split) does not depend on them.
- **Determinism.** Every prior is a sum of integer-valued targets held in float64, which is exact and order-independent below 2^53, followed by fixed arithmetic.
  - So FS3 is deterministic.
  - Criterion 6 should be byte-identical, as it was for E019 and E022.
- **Masked view.** Embargo months are absent from it, so no prior uses August on S1 or March on W1.
- **Tools.** `mechanism_check.py` accepts `all`, which clause 2 needs.
- **EDA.**
  - These match `priors.json`, `priors_summary.md` and `priors_joint.json`: incremental R², stability, coverage and the joint table.
  - `eda_day4.py` nulls targets outside Jan, Mar–Jun and Aug right after loading.
  - K8's components have 5 and 69 levels in 2025 Jan–Nov (71 over all months). K8 has 287 levels over all months, as stated.
- **Noise scale.** The development-mean shifts +0.25, −0.24 and −0.12 s match the committed JSONs, with 1, 1 and 0 counted WINs.

## Scientific Validity

### (a) The W1c and chain revisions are correct

- **W1c.** It trains on January only.
  - All training priors are null, and the count is 0.0.
  - So H019's W1c predictions equal H018's. The test now covers the docstring's claim.
- **W1.**
  - W1 stays in criterion 1's mean and in 1(b), but out of the WIN count. That is a stated choice, which v1 allowed.
  - In the committed mechanism contrasts, W1 carried the largest fold gain: P −5.91 s against a mean of −3.47 s; C −9.52 s against −6.75 s.
  - So W1 can move a 5-fold mean by a fifth of its own excess.
  - **Disclosure:** the 4-fold mean (R1–R3, S1) is recorded beside the 5-fold mean. It is not a clause.
- **Chain.**
  - In both branches of criterion 4, a matched reference carries every mechanism claim (ruling R): H019 − H018 for the block, H018 − E019 for the exclusion.
  - When H018's change is carried, B2 is applied to H018's clauses.

### (b) Clause 1(a): the S1 twin rule

- **What the frozen code does.** `promotion_check` turns an S1 WIN into a TIE when S1c is a LOSS (`fold_outcome_counted`).
- **The two readings of v2's text:**
  - **raw outcomes:** an S1 WIN would count even when S1c contradicts it, though S1c is the one fold that checks S1's block causally;
  - **counted outcomes:** v1's accepted clause.
- **The adopted reading is the counted one.** Clause 1(a) is met if any of these holds:
  - criterion 1 fails on `NM_present_excl_LIRF`;
  - there are fewer than 3 WINs in `fold_outcome_counted` among R1, R2, R3 and S1;
  - S1 is not a counted WIN;
  - any fold R1–W1 is a LOSS.
- **The alternative.** The researcher may submit a v3 with raw outcomes instead.

### (c) The comparator and criterion 4

- **The ambiguity.** The proposal names "the champion in force at evaluation (E019, or the H018 v2 run if H018 is promoted first in this chain)". The precedents allow two readings:
  - Day 1 promoted within the chain;
  - Day 3 recorded a promotion only at the phase close.
- **The resolution.**
  - `H018_review_v2.md` item 7 defines the term.
  - H018's status is recorded before H019 is allocated.
  - So the comparator and criterion 4 are fixed before H019's results exist.
- **The W1 twin in the E019 branch.** When H019 is compared with E019:
  - W1c's outcome is H018's exclusion alone, because the priors are inert there.
  - The splice in `H018_review_v2.md` (d) suggests it may be positive: +3.9 to +6.7 s if H018 reached no-T behaviour on that cell.
  - A W1c LOSS would void a W1 WIN in H019's promotion comparison. This is disclosed, not a clause.

### (d) Rule 8: the prior source is clean, the fitted model is not insulated

- **What is true.** No tail row enters any prior, so no convention-tail row does.
- **"The prior block adds no convention exposure" does not follow at the model level.**
  - H019's LightGBM still trains on the 932 LIRF NM-present block-at-schedule tail rows.
  - Five new static-key inputs give it new ways to fit them.
  - Day 2 recorded exactly this for FS1's keys: E016, "the static keys still reach the LIRF convention", a missed rule 8 pre-registration.
- **Scale on this cell,** full dRMSE by development fold (R1 / R2 / R3 / S1 / W1):
  - E017 − E018 (FS1 keys): −57.1 / −50.5 / −37.6 / **+36.9** / −18.6;
  - E012 − E006: −53.7 / −51.8 / −33.1 / **+17.1** / −14.9.
- **At July's rate,** 1 s on this cell is about 0.1 s of S1's all-rows RMSE (+4 s gives +0.40 s). A +17 to +37 s shift would move S1 by about +1.7 to +3.8 s.
- **Consequences:**
  - The pre-registered "full within ±8 s" may well be exceeded. It stays the expectation.
  - S1, the required WIN, can be decided by this cell rather than by the priors.
  - H018 v2's rule 1 S1 recording therefore applies to H019's promotion comparison (item 4(c)).
  - The sentence is corrected in the ack.

### (e) The key set

- **The joint table supports K5 as the carrier and K4 as redundant.** K1 + K5 reaches 0.4505 from 0.2610; adding K4 gives 0.4504.
- **The selection rule is a post-hoc description of the v1 choice.**
  - Its 1,000-level criterion separates K3 (1,300 levels) from K8 (287), and nothing independent motivates that threshold.
  - It used only never-validation evidence, and the dropped K8 and K9 add 0.0022 R² in the linear model.
  - No leakage, and the consequence is bounded.

### (f) What the EDA can support (unchanged from v1)

- K5's +0.19 R² over airport × hour has no anchor or FS2 control, so it is a loose upper bound.
- The −3.0 s floor tests it.

## Novelty Relative to Existing Research

- **The run's first target statistic.** It is the brief's named Day 4 question and is not redundant.
- **Not FS1 again.** The keys are raw-level and interaction keys that FS1 collapses at 100 rows or represents only separately.
- **Not H020's mechanism.** The rejected CatBoost design did not implement it.

## Experimental Isolation

- **One change against the H018 run:** five appended numeric columns.
- **Everything else is identical:** training rows, vocabulary and the FS2 columns (`test_fs3_extends_fs2`).
- **The claim is block-level.** K5 is named as the expected carrier, not tested separately.

## Validation Quality

- **Folds.** The frozen folds are used unchanged, and S1 is a required WIN.
- **Causal checks:**
  - the R folds are causal (past-only validation priors);
  - S1c (six training months) checks S1 through the twin rule adopted in (b);
  - W1 has no functional twin, and it is out of the WIN count.
- **Conditions.** B2 and B3 apply.
- **Clause 2 can be met by the `NM_present_LIRF` cell alone** ((d)). Clause 2 is all rows, mean ≥ 0.
  - The v1 review accepted that risk by design.
  - (d) shows the risk is larger than v1 stated: about ±2 s there, and up to about +4 s on S1 by precedent.

## Leakage Review

### Target Leakage

PASS

- LOMO holds at every level of the hierarchy.
- Validation targets are unused, and the source filter acts on training rows.
- A single training month yields nulls.
- Embargo months are absent from the view.
- No December target enters a development or H prior.

### Temporal Leakage

CONCERN

This is not blocking.
- **Non-causal folds.** S1's and W1's validation priors use months after the validation month. That is the frozen design.
- **Twin checks.** S1c checks S1. Nothing checks W1, which is why it is out of the WIN count.
- **Inherited.** FS2's T features.

### Competition Availability

PASS

- Every key exists in the ranking files.
- **K5 coverage (≥ 30 rows) is 0.968 for January 2026 and 0.958 for July 2026,** counted on all DEP rows. The narrower prior source is stated beside it.

## Compute Review

### RAM

PASS

The FS3 smoke on R3 peaked at 5.1 GB, against CLASS-M's 8 GB.

### Runtime

PASS

About 6 s per fold on top of H018's run, which is of E019's class (954 s).

### Disk

PASS

About 10 MB.

## Weakest Assumption

**That FS2's LightGBM does not already extract most of the stand × runway route effect** from `stand`, `airport_runway` and the anchor. The EDA cannot speak to it.

## Missing Control or Ablation

Both are named, not required (unchanged from v1):
- **a within-key permuted prior,** to separate route information from re-encoding;
- **a K5-only block.**

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions** before `gate.py allocate H019 v2`:
   - (a) H018 v2's primary run is COMPLETE, with clause 3 not met, and its checkpoint is committed.
   - (b) H018's promotion status is recorded in the journal, as `H018_review_v2.md` item 7 defines it. It is either:
     - "promoted first in this chain", with item 4 of that review done; or
     - "not promoted", with its clause 1–2 outcomes.
   - (c) `H019_ack_v2.md` is committed, the tree is clean, and no other experiment runs.
   - (d) The tools freeze of `H018_review_v2.md` item 1(e) holds. It covers `priors.py` and the `fs3` body.
2. **One primary run.**
   - `gate.py allocate H019 v2`.
   - `config.yaml` is H018's run config with `hypothesis_id: H019`, `proposal_version: 2` and `feature_set: FS3`.
   - Everything else is identical: `route_train_exclude: true`, seed 42, all 8 folds, CLASS-M.
3. **Comparisons,** as in the Validation Plan:
   - `mechanism_check.py <H019> <H018> NM_present_excl_LIRF` (clause 1);
   - `mechanism_check.py <H019> <H018> all` (clause 2; per-airport figures against H018, LFPG named);
   - `compare.py <H019> <champion in force>`;
   - `compare.py <H019> E005`;
   - `route_check.py <H019> - E005`;
   - `range_check.py <H019> <H018>`.
4. **Readings,** adopted by the ack before the run:
   - (a) **Clause 1(a).**
     - WINs are counted in `fold_outcome_counted` (the frozen twin rule), among R1, R2, R3 and S1.
     - There must be at least 3, and S1 must be a counted WIN.
     - No fold R1–W1 may be a LOSS.
     - Criterion 1 is read from the same output.
     - The tool's `criterion_2` field is not the clause.
   - (b) **Comparator.**
     - The H018 run is the champion in force only if H018 was recorded "promoted first in this chain". Criterion 4 is then clauses 1–2.
     - Otherwise E019 is. Criterion 4 is then clauses 1–2 plus H018 v2's clauses 1–2, under B2.
   - (c) **S1 recording.** Two rules apply to H019's promotion comparison:
     - H018 v2's rule 1 S1 recording: if the `NM_present_LIRF` `share_of_sse_change` on S1 is ≥ 0.5, the record reads "S1 WIN carried by the LIRF NM-present convention mixture";
     - `H018_review_v2.md` item 8(d), with "the prior block" in place of "the D3-C2 treatment".
5. **Conditional reproduction.** Only if criteria 1–3 pass against the champion in force and no clause of criterion 4 (item 4(b)) is met:
   - one `reproduction` allocation (seed 43);
   - then `reproduce_check.py`, and the SHA-256 comparison of all 8 prediction files.
6. **Infrastructure failure.** As `H018_review_v2.md` item 5.
7. **Promotion.**
   - Only if criteria 1–8 hold (B1–B4) and no clause of criterion 4 is met.
   - Subject to the Day 4 phase-close review. Holdout access only as that review names it (rule 9).
8. **Recording.** The H019 analysis records:
   - (a) the CPU string, any container restart since H018's run, INC-0004, and who launched the run (INC-0005);
   - (b) the SHA-256 of W1c's prediction file against H018's (expected equal);
   - (c) the 4-fold mean (R1–R3, S1) beside the 5-fold mean of clause 1(b);
   - (d) `NM_present_LIRF` full and bulk per development fold against H018, beside the ±8 s and −1 to −6 s expectations;
   - (e) the attribution pair (H018 − E019) and (H019 − H018).
9. **Not authorized:**
   - any change to the keys, M, hierarchy, source filter, LOMO, features, parameters, folds, seed, routing or exclusion, populations, thresholds or clause code;
   - per-key or tuned variants;
   - any search or early stopping;
   - scoring H;
   - any FS3 fit on a frozen fold other than those of items 2, 5 and 6.

Required acknowledgement path: `research/day-04/acks/H019_ack_v2.md`.
- It references the proposal hash (`df74347c…`) and this review's hash.
- It adopts items 1, 4, 7, 8 and 9.
- It records two corrections:
  - the Implementation Plan's "`gate.py allocate H019 v1`" reads `v2`;
  - Rule 8's "The prior block adds no convention exposure" reads: "The prior block adds no convention row to any prior. The fitted model can still change its fit on the retained LIRF NM-present tail rows (E016; E017 − E018 +36.9 s on S1 in this cell)".

## Revision

None required for this version.

**Process note:** INC-0005's delegated code was reviewed on its merits: the single-training-month test, and the joint-key section of `eda_day4.py`. No defect was found.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| H019 − H018 on `NM_present_excl_LIRF`: development mean < 0 | 0.80 |
| The same mean ≤ −3.0 s (1(b) not met) | 0.30 |
| 1(a) not met, under the reading in item 4(a) | 0.50 |
| Mechanism supported (neither clause met) | 0.27 |
| W1c predictions byte-identical to H018's | 0.99 |
| All rows against H018: development mean < 0 | 0.70 |
| `NM_present_LIRF` full outside ±8 s on at least one development fold | 0.40 |
| Promotion (items 5 and 7) | 0.10 |

Expected magnitude:
- **`NM_present_excl_LIRF` against H018:** −0.5 to −4 s (central −2 s).
  - W1 is the most likely largest fold gain.
  - LFPG, EGLL and LTFM are expected to lead by airport.
- **All rows against H018:** −0.5 to −3 s.
- **W1c:** exactly 0.

Primary expected failure mode:
- **Primary.** A real but small gain below the −3.0 s floor, so 1(b) is met. FS2 already holds most of the route effect through `stand`, `airport_runway` and the anchor.
- **Secondary.** If the floor is cleared, S1's all-rows outcome decides promotion, and the `NM_present_LIRF` convention mixture may decide S1, moved by the new static-key inputs rather than by the priors' route information. Item 4(c) records that case.
