---
schema: advisor-review-v1
hypothesis_id: H018
proposal_version: 2
proposal_sha256: 1fa63bb4964ddb11221aae095dafe669d6f7568a2971868eef8f53ebaa9c6f61
exchange_id: X-D04-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.86
created_utc: 2026-09-30T17:45:11Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.86).** H018 v2 is executable within the authorized scope below.

**All five required revisions of `H018_review_v1.md` are met.**

| v1 revision | What v2 does | Checked here |
|---|---|---|
| 1. Clause 1 and its reading | Clause 1 is on the > 3 h `d_sched` band (5-fold sum > 50), against the matched no-T reference E021. The < 1 h band and the total are disclosures with pre-registered readings, and a total inside 92–125 does not refute D3-C2. The stronger claim is disclaimed. Falsification clauses and disclosures are separated, and the Alternative Explanations are rewritten | Decisive in both directions ((a)) |
| 2. Noise scale and evidence | "8 times" is gone. The shifts are restated per band, E021 is added, and every count is committed | Re-derived byte for byte from the committed script ((b)) |
| 3. Rule 8 | The false sentence is replaced. `NM_present_LIRF` full and bulk expectations are given per development fold, S1 at July's rate, with a rule 1 recording for an S1 WIN that cell carries | Every figure reproduced ((c)) |
| 4. Chain contingency | If clause 3 makes the run INVALID, the chain stops on this code path | Present |
| 5. Record | `created_utc` 17:24:05Z equals the file write (17:24:05.62Z) and the commit second. INC-0004 is in the provenance line, and D4-C1 is in `H018_ack_v1.md` | Checked |

**Three record items remain.** None changes the experiment. The authorization and the acknowledgement handle them.
1. **The Implementation Plan still reads v1.** It says `gate.py allocate H018 v1` and `proposal_version: 1`, while the Validation Plan correctly says `allocate H018 v2`.
   - The gate would refuse v1, because its review is REVISE.
   - But `run_experiment.py` does not compare the config's `proposal_version` with the allocation. A `1` in `config.yaml` would therefore enter the record unnoticed.
2. **Evidence provenance.** `range_check_refs.json` was committed in `e4c57f8` (17:19:57Z).
   - The `--bands` code it depends on was committed later, in `99db208` (17:21:35Z). That is the commit the proposal cites for the file.
   - The file re-derives byte for byte from the committed code (Verified here), so only the citation is wrong.
3. **One Alternative Explanation overreaches** ((d)).

**Verified here.** Every check was read-only, target-free, synthetic, or a comparison of existing prediction files.
- **Constraints kept.**
  - No December target was read, and no model was fitted or scored on a real fold.
  - Development-fold truth was read only through `prc.evaluate.truth_frame`.
  - Scratch output stayed in the session scratchpad. Python ran with bytecode and cache writes disabled.
- **Hashes.**
  - Both proposals match the envelope.
  - The six frozen files, and the SPLITS v2 proposal, review and ack, match `config/frozen.json`.
  - `.claude/agents/advisor.md` is `30fff5dd…`, as in `config/agents.yaml`. `uv.lock` is `39df945c…`.
  - The X-D04-S01-0001 mirror verifies 8/8.
- **Predictions.** The files of E005, E006, E012, E015 and E017–E022 match their manifests, 8/8 each.
- **Code and tree.**
  - HEAD is `d1cc43b` and the tree is clean.
  - Since the v1 review (`ff16c8b`), only `scripts/range_check.py`, `scripts/eda_day4.py`, two test files and records have changed. Nothing under `src/` changed, so the treatment is the `7ea6b55` code reviewed in v1.
  - `pytest`: 143/143 pass (v1's 141 plus the two new tests). `ruff`: clean.
  - There is no Day 4 allocation in the task ledger, and no experiment is running.
  - The boot id is D04-S01's, so there was no container reset. The CPU string is E019's ("@ 2.10GHz").
- **Delegated code (INC-0005).** `band_counts`, `sum_bands` and their test are correct.
  - The bands are `d_sched` < 3,600 s, 3,600–10,800 s and ≥ 10,800 s, on `NM_missing_other` bulk rows.
  - They partition all 9,788 such rows of the development folds (2,760 + 6,500 + 528).
- **Evidence.**
  - `range_check.py E006 E012 E015 E017 E018 E019 E021 --by-dsched --bands`, with its JSON written to the scratchpad, is byte-identical to the committed `range_check_refs.json`.
  - These all match: every Observation cell, the per-band shifts, E019 − E021 (0 / +5 / +63; +68 in total), the > 5 h shares (E019 41/93, E017 4/93, E005 0/93) and the forward table (`forward_support.json`).
  - The LIRF NM-missing monthly counts sum to the excluded-set sizes: R1 1,065, S1 866, W1c 60.

## Scientific Validity

### (a) Clause 1 now tests D3-C2 as recorded, and it is decisive

- **What each hypothesis predicts for the > 3 h count** (5-fold sum):
  - **D3-C2 (source removed):** the no-T level. That is 13–41 across the six fits without T windows, and 18 for E021, the matched no-T fit.
  - **The alternative** (SCHED-anchored T windows extrapolate without the source): about E019's 81.
  - **Noise in this band:** +15 for seed (E015 − E012), and +12 and +1 for procedure.
  - **So each hypothesis sits at least about two noise units from the threshold.** 50 is 9 above the highest no-T fit and 31 below E019.
- **No single fold carries the statistic.**
  - E019's > 3 h counts are R1 30, R2 18, R3 13, S1 15 and W1 5.
  - E021's are 2, 0, 2, 12 and 2.
- **The loss clause 2 tests sits in the same band.** Of E019 − E017's `NM_missing_other` bulk SSE change:
  - the > 3 h band carries 92 % on R1, 97 % on R2 and 88 % on R3;
  - rows E019 predicts out of range carry 100 %, 89 % and 94 %;
  - on W1, one LTFM row carries 64 % (`d_sched` 16.4 h; E019 7,630 s against y 727 s).
- **The source is nearly exclusive.** In the never-validation months 06 and 08 (EDA §D), 188 of 382 LIRF NM-missing rows are tail rows. At the other nine airports it is 15 of 4,450. The exclusion therefore removes nearly all tail targets from the region of long SCHED-anchored windows.
- **A partial outcome near 50 is read as a binary.** That is acceptable as pre-registered. The analysis also states the fraction of the increment removed, (81 − n) / 63 (item 8(b)).

### (b) Noise scale and evidence

- **The three shift rows are correct.**
  - seed E015 − E012: −9 / +15 / +11;
  - procedure E017 − E012: −16 / +1 / −22;
  - procedure E018 − E006: −19 / +12 / −8.
- **"Every fit without T windows lies in 13–41"** in the > 3 h band is correct.
- **The committed file re-derives exactly.** Only its cited commit is wrong (Summary, item 2).

### (c) Rule 8 is now correct, and its figures reproduce

- **The corrected statement is true.** The 932 LIRF NM-present block-at-schedule tail rows stay in training, and so do the non-LIRF block-at-schedule rows.
- **Checked on E019's files:**
  - S1 has 271 LIRF NM-present tail rows. They carry 10.4 % of E019's S1 SSE, against 1.9 % for `NM_missing_other`.
  - The cell's full RMSE is 817.8 s on 14,874 rows, consistent with "at least about 730 s".
  - +4 s on the cell is +0.40 s on S1's all-rows RMSE.
  - The three scale series (E019 − E017, E021 − E017, E017 − E012) match the committed comparisons.
- **The S1 range is narrow, but it is a disclosure.** −5 to +15 s is narrow against the T block's own ±17 s on this cell. The rule 1 S1 recording covers what that means for promotion.
- **Full and bulk, instead of full and tail.**
  - v1 asked for full and tail. v2 gives full and bulk, and states the tail direction in the mechanism: tail predictions fall, so full dRMSE rises.
  - `compare.py` reports `share_of_sse_change_tail` for the cell.
  - I accept this as meeting the requirement.

### (d) The treated cell cannot carry S1, the WIN that promotion needs

**Splice bound.** On existing files, replacing E019's `NM_missing_other` predictions with E017's (E021's in brackets) changes all-rows RMSE by:

| Fold | R1 | R2 | R3 | **S1** | W1 | S1c | **W1c** | Development mean |
|---|---|---|---|---|---|---|---|---|
| dRMSE (s) | −3.09 (−3.29) | −4.22 (−4.19) | −1.32 (−1.52) | **+0.44 (+0.12)** | +0.47 (−0.49) | +0.26 (−0.19) | **+6.74 (+3.88)** | −1.54 (−1.87) |

- **H018's all-rows gain should concentrate on R1–R3.**
- **An S1 WIN, if one occurs, would not come from the treatment.** It would be carried by `NM_present_LIRF`, or by perturbation of `NM_present_other`.
  - The proposal's rule 1 recording covers only the first case.
  - Item 8(d) generalises it.
- **Alternative Explanations, "clause 1 met", overreaches.** H018 alone does not show that "a treatment would have to act on the T windows, not on the training set".
  - The NM-missing tail rows at the other nine airports stay in training. They are few ((a)), but they also have SCHED-anchored windows.
  - If clause 1 is met, the record states that D3-C2's attribution is falsified, without that conclusion (item 8(e)).

## Novelty Relative to Existing Research

- **It is the run's first training-set treatment.** It answers Day 3 open question 1 (D3-C2) directly.
- **It is not redundant with any journal entry.** The prediction-time alternative, clipping, is correctly declined.

## Experimental Isolation

- **One change against E019: the LightGBM's training rows.**
  - v1 verified that `fs1` is identical on all eight folds and the categorical vocabulary is unchanged.
  - `src/` has not changed since.
- **What the change moves:**
  - the numeric bin boundaries;
  - the first trees, because the removed rows carry the largest gradients;
  - the convention mixture on LIRF NM-present rows. This is now pre-registered.
- **The ablation is exact.** E019 remains the exact ablation for everything H018 claims.

## Validation Quality

- **Folds and conditions.**
  - The frozen folds are used unchanged, and the seasonal fold is included.
  - S1 is a required WIN.
  - B2 bars promotion if either falsification clause is met, and B3 applies.
- **Twins.**
  - On `NM_missing_other` bulk, E019 − E017 is −17.9 s on S1c and −141.0 s on W1c, against −31.5 s on S1 and +76.9 s on W1.
  - The splice puts W1c at +3.9 to +6.7 s on all rows, so W1c is the fold most likely to move against H018. A W1c LOSS would void a W1 WIN under the twin rule.
  - The twin cells are reported beside S1 and W1 (item 8(c)).
- **Clause 2 is unchanged and decisive.** It counts folds, so one row can flip at most one fold.

## Leakage Review

### Target Leakage

PASS

- The exclusion key (`ADEP_mvt`, `flt_missing`) is label P and target-free, and it acts on training rows only.
- No new input is added.

### Temporal Leakage

CONCERN

This is carried from Day 3 and is not blocking.
- FS2's T features are unchanged, including the SCHED-anchored in-taxi windows on NM-missing rows.
- H018's mechanism depends on how the model uses them.

### Competition Availability

CONCERN

This is carried (D3-C3) and is not blocking.
- Every input exists in the ranking files.
- **The rows the treatment targets are more numerous in January 2026 than in any 2025 month.** January has 435 non-LIRF NM-missing rows over 3 h and 92 over 5 h, against 2025 maxima of 222 and 36.
- No development fold samples that exposure (rule 2).

## Compute Review

### RAM

PASS

- E019 peaked at 4.76 GB, and the treatment removes 0.04–0.08 % of training rows.
- CLASS-M allows 8 GB, with a hard limit of 11 GB.

### Runtime

PASS

- E019 took 954 s on this CPU string.
- The runner stops at 45 min.

### Disk

PASS

About 10 MB of git-ignored predictions, covered by the manifest.

## Weakest Assumption

**That LIRF NM-missing rows are the only material source of large targets among rows with long SCHED-anchored windows.**
- EDA §D supports it: 15 tail rows of 4,450 at the other airports, against 188 of 382 at LIRF (months 06 and 08).
- The no-T fits show that `d_sched` alone still yields 13–41 out-of-range predictions above 3 h. The remaining rows can therefore keep some large-valued leaves there.

## Missing Control or Ablation

- **None is required.**
- **Named by the proposal, not run:** an FS2_P fit with the same exclusion would test the stronger claim about the < 1 h band. That claim is correctly not made.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions** before `gate.py allocate H018 v2`:
   - (a) `research/day-04/acks/H018_ack_v2.md` and `H019_ack_v2.md` are committed.
   - (b) `research/STATE.md` is current, with a measured header time. It is currently dated 16:50:42Z and records none of the following, which it must:
     - X-D04-S01-0001: H018 v1 and H019 v1 REVISE, H020 v1 REJECT;
     - correction D4-C1;
     - this exchange's result and corrections;
     - INC-0004 and INC-0005, both open;
     - the next action.
   - (c) `research/EXPERIMENT_JOURNAL.md` records X-D04-S01-0001, including H020 v1's REJECT (required by `H020_review_v1.md`: negative results are kept), and this exchange.
   - (d) The working tree is clean, and no other experiment runs.
   - (e) **Tools freeze.** From `d1cc43b` until the chain's last comparison (H019's, or its reproduction's), nothing changes in code under `src/` or `scripts/`, in `pyproject.toml` or in `uv.lock`. Run commits may differ only in records: `research/`, `experiments/`, `orchestration/`, `docs/`.
2. **One primary run.**
   - `gate.py allocate H018 v2`.
   - `config.yaml` is E019's, with `hypothesis_id: H018`, `proposal_version: 2` and `params.route_train_exclude: true`.
   - Everything else is identical: `model: routed_lightgbm`, `feature_set: FS2`, E019's `params` and `route_ridge_params`, `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
3. **Comparisons,** in the Validation Plan's order:
   - `route_check.py <H018> - E005` (clause 3);
   - `range_check.py <H018> E019 E021 E017 --by-dsched --bands`, with its JSON committed. Clause 1 reads H018's `bands_dev5[">3h"].total`;
   - `compare.py <H018> E019` (clause 2; criteria 1–3; rules 1, 6 and 7; the S1 recordings);
   - `mechanism_check.py <H018> E019 NM_present_excl_LIRF`;
   - `compare.py <H018> E005`.
4. **Conditional reproduction.** Only if criteria 1–3 pass against E019, neither falsification clause is met and clause 3 is not met:
   - one `reproduction` allocation of H018 v2 (seed 43, everything else identical);
   - then `reproduce_check.py`, and the SHA-256 comparison of all 8 prediction files.
5. **Infrastructure failure.** One identical re-run with `--purpose rerun`, logged, and only after an infrastructure failure. A RESOURCE_FAILURE or TIMEOUT is recorded and not retried.
6. **INVALID** (clause 3 met). The chain stops, and H019 v2 is not allocated.
7. **Promotion.**
   - Only if criteria 1–8 hold (B1–B4), neither falsification clause is met and clause 3 is not met.
   - Subject to the Day 4 phase-close review. Holdout access only as that review names it (rule 9).
   - **"Promoted first in this chain"** (H019 v2's comparator) means both of the following. Otherwise E019 is the champion in force for H019.
     - Every condition of this item that is verifiable before the phase close holds, including criterion 6 from item 4, with no B3 objection.
     - This is recorded in the journal before H019 v2 is allocated.
8. **Recording.** The H018 analysis records:
   - (a) the CPU model string, whether a container restart intervened since E022, INC-0004, and who launched the run (INC-0005);
   - (b) the band table (7 folds, rule 7 subgroups) and, beside the clause 1 reading, the fraction of the > 3 h increment removed, (81 − n) / 63. The pooled > 5 h share uses the Observation's all-rows definition (E019: 41/93);
   - (c) the `NM_missing_other` twin cells (S1c, W1c), beside S1 and W1;
   - (d) **S1 attribution.** If S1 is a WIN, its margin is attributed to the D3-C2 treatment only if the `NM_missing_other` cell carries at least 0.5 of S1's SSE change (`share_of_sse_change`). Otherwise the carrying cell is named. The proposal's `NM_present_LIRF` rule is one case of this;
   - (e) **If clause 1 is met,** D3-C2's attribution to LIRF NM-missing rows is recorded as falsified. The record does not conclude that no training-set treatment can act, because the remaining NM-missing tail rows at the other airports are untested.
9. **Not authorized:**
   - any change to features, parameters, folds, seed, the routing or exclusion rule, populations, bands, thresholds or clause code;
   - any search or early stopping;
   - scoring H;
   - any other fit with `route_train_exclude: true` on a frozen fold.

Required acknowledgement path: `research/day-04/acks/H018_ack_v2.md`.
- It references the proposal hash (`1fa63bb4…`) and this review's hash.
- It adopts items 1, 7, 8 and 9.
- It records two corrections:
  - the Implementation Plan's "`gate.py allocate H018 v1`" and "`proposal_version: 1`" read `v2` and `2`;
  - `range_check_refs.json` was committed in `e4c57f8`. It was produced by the `--bands` code committed in `99db208`, and re-derives byte for byte from that code.

## Revision

None required for this version.

**Process notes (non-blocking):**
- INC-0004 was not re-measured in this review.
- **INC-0005.** The delegated code (`--bands` and its test) was reviewed on its merits. No defect was found beyond the commit-order item.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Clause 3 not met (routed rows equal E005's) | 0.97 |
| Clause 1 not met (> 3 h band ≤ 50) | 0.85 |
| > 3 h band within the proposal's 10–35 | 0.70 |
| < 1 h band within 55–90 | 0.75 |
| Clause 2 not met | 0.88 |
| All rows against E019: development mean < 0 | 0.85 |
| Criterion 1 against E019 | 0.55 |
| S1 WIN against E019 | 0.20 |
| W1c LOSS against E019 | 0.35 |
| `NM_present_LIRF` on S1, full, within −5 to +15 s | 0.60 |
| `NM_present_excl_LIRF` within ±2 s on every development fold | 0.50 |
| Promotion (items 4 and 7) | 0.12 |

Expected magnitude:
- **> 3 h band:** about 22 (80 % interval 12–40). At least 0.65 of the increment is removed.
- **< 1 h band:** 60–90. **Total:** 95–130.
- **`NM_missing_other` bulk against E019:**
  - R1, R2 and R3: −60 to −240 s;
  - W1: negative, decided by one LTFM row;
  - S1: within ±30 s.
- **All rows against E019:**
  - development mean −1.0 to −2.5 s. The splice bound from the treated cell alone is −1.5 to −1.9 s;
  - by fold: R1 about −3 s, R2 about −4 s, R3 about −1.5 s, S1 and W1 about 0 (±1 s);
  - W1c 0 to +7 s.

Primary expected failure mode:
- **Primary.** The mechanism holds: clauses 1 and 2 are not met, and D3-C2 is supported. Promotion still fails on criterion 2.
  - S1 is a TIE, because the treated cell moves S1 by only +0.1 to +0.4 s (splice). `NM_present_LIRF` and perturbation decide S1.
  - The record is then "D3-C2 treated, not promoted", and H019 v2 carries H018's change against E019.
- **Secondary.** Clause 1 is met, with the count in 50–70. `d_sched` and the remaining long-window rows keep large-valued leaves above 3 h.
