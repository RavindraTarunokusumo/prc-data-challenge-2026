---
schema: advisor-review-v1
hypothesis_id: H009
proposal_version: 3
proposal_sha256: f013c86f75d0cfb3b8643862cf3829991ad095a38f045f2e965e1f298f303a20
exchange_id: X-D02-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-09-28T19:34:45Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT, with preconditions.**

v3 fixes the one v2 defect and the three items that depended on it. I found no new blocking defect. FS1, the model, parameters, folds, seed and class are unchanged, and so are clauses 1, 2(b), 3 and 4.

| v2 required item | Status in v3 |
|---|---|
| 1. Clause 2(a) must not be decidable by row 192622644 | **Done.** The clause moves to `NM_present_excl_LIRF` (NM-present rows, `ADEP_mvt` ≠ LIRF). The population is target-free, is defined in `prc.attribution.population_mask`, and is tested (`tests/test_attribution.py`). It was committed at `64c165b` (19:20:12Z), before v3 and before any FS1-family allocation (there is none) |
| 2. Rule 8 for M1 (LIRF NM-present block-at-schedule tail rows) | **Done, by insulation.** These rows are outside 2(a) (LIRF excluded) and outside 2(b) (tail rows by definition). Reporting expectations are pre-registered, and Alternative Explanation 2 is extended to them |
| 3. Rules 6 and 7 on every criterion-4 comparison | **Done.** `compare.py <H009> E006` is in chain step 1. `mechanism_check.py` reports top-1 and top-10 shares per fold and twin, plus dominant-row details with `d_aobt3` and `d_sched` (`row_concentration`, tested). The expected dominant rows for M1 and M2 on S1 and S1c are pre-registered |
| 4. Carry-over | **Done.** Verified byte for byte (below) |

**The fix works.** This was checked read-only on E006's stored predictions:

| Clause 2(a) population | Largest single-row share of E006's SSE, S1 / S1c | Other folds | Rows with y ≥ 20,000 s |
|---|---|---|---|
| v2: `NM_present` | 23.2 % / 24.0 % (row 192622644) | ≤ 1.2 % | 1 |
| v3: `NM_present_excl_LIRF` | 1.32 % / 1.36 % (row 191767771: LFPG, y = 15,059 s) | 0.37–1.66 % | 0 |

- **S1's new top row cannot decide the fold.**
  - Day 1 tree models agree on it: E006 predicts 2,873 s and E011 2,919 s.
  - A 5,000 s shift of the prediction on it moves S1 by about 1–2 s. In v2, row 192622644 moved S1 by about 11 s.
- **Block-at-schedule signatures outside LIRF are too small to matter** (y ≥ 3,600 s and |y − `d_sched`| < 120 s).
  - There are 10–47 such rows per fold, mostly EGLL, and LTFM on W1 and W1c.
  - They carry 0.07–2.8 % of E006's SSE in the population. A ±15 % change of that moves a fold by at most ±0.55 s.
  - This matches Day 1: outside LIRF the rate in the tail is at or below the bulk base rate (X-D01-S01-0004).
- **Anchor-wrong tail rows** (y − `d_aobt3` > 3,600 s): 22–109 per fold, carrying 2.3–7.8 % of E006's SSE. A ±15 % change of that moves a fold by at most ±1.5 s (S1 and S1c).
- **The cited Day 1 evidence reproduces exactly.** I recomputed E011 against E006 on `NM_present_excl_LIRF` with the frozen `promotion_check`, without writing into the repository:
  - mean +0.9908 s and q95 +1.8105 s, with identical fold points, intervals and outcomes on all seven folds;
  - top-1 shares −0.17 (S1) and −0.20 (S1c) on this population, against +1.03 and +1.24 on `NM_present`;
  - the R1 and R3 caveat (|dRMSE| 0.35 and 0.05 s).

**One residual exposure: late departures.** It is disclosed here and cannot decide the clause.
- **Definition:** rows of the 2(a) population with `d_sched` ≥ 3,600 s and a normal taxi (y < 3,600 s).
- H009 and E006 see identical `d_sched` on them, so any difference comes from how the trees use it. That is not static structure.

  | Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
  |---|---|---|---|---|---|---|---|
  | Rows | 18,619 | 15,876 | 10,598 | 21,750 | 7,979 | 21,750 | 7,979 |
  | Share of E006's SSE in the population | 23.2 % | 21.7 % | 17.9 % | 26.4 % | 15.5 % | 26.9 % | 19.7 % |
  | Contribution to E011 − E006 (same inputs), s | −0.26 | +0.67 | −0.02 | +0.33 | +1.36 | +0.53 | **+21.8** |

- **Development folds.** The same-input swing is at most 1.4 s. That is within the exposure v2 accepted on R1–R3 and W1 (±0.6 to ±1.9 s), and it cannot decide 2(a) at the expected −5 to −20 s.
- **W1c.** These rows carried 22 of W1c's 30 s. They are the likeliest way that W1c comes out LOSS and voids a W1 WIN under the twin rule.

**Envelope request: H010 preconditions (b) and (c) and H012 precondition (c) are kept exactly.**
- **H010 (b) holds.**
  - The `fs1` function body is byte-identical to `cba278d`. The only line removed from `features.py` since then is the `FEATURE_SETS` literal, which was extended.
  - `gbm.py` is unchanged since `866b902`.
  - The Model and FS1 blocks are byte-identical to v2. The parameters, folds, seed and class are identical to v1.
- **H010 (c) holds.** Clause 3 is byte-identical to v2: LIRF NM-missing subgroup, full dRMSE, falsified at ≥ 0 on 3 of 5. X-D02-S01-0002 confirmed that this matches v1.
- **H012 (c) holds.**
  - Clause 4 is byte-identical to v2: `mechanism_check.py <H009> <H012> NM_present`, falsified if it fails criterion 1 or 2.
  - `64c165b` left the `NM_present` path of `mechanism_check.py` unchanged. It added only the rule 6 output and the new population.
- **Also verified.** H012 (b) holds. The chain order H009 → H010 → H012 → H011 matches H011 v2's precondition (b).
- **Effect of this ACCEPT.** Once the acknowledgement is committed, it satisfies precondition (a) of H010 v1, H011 v2 and H012 v1.

**Verified here.** All checks were read-only: no December target was read, no model was fitted, scored or allocated, and I wrote only this file.
- **Hashes.**
  - The proposal matches the envelope.
  - The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json`.
  - `.claude/agents/advisor.md` is `30fff5dd…` (matches `config/agents.yaml`), and `uv.lock` is `39df945c…`.
  - The checksums of X-D02-S01-0001 and -0002 verify.
  - The evaluator re-verified silver against the frozen pin on every truth read.
- **Tree, tests and lint.** The tree is clean at `5ba9230`. `pytest` passes 99/99 (98 plus the new `row_concentration` test), and `ruff` is clean.
- **Timestamp.** `created_utc` 19:21:13Z equals the file time and the commit time, so it is a measured time.
- **State.**
  - There is no Day 2 allocation in `orchestration/task-ledger.jsonl`, and the only holdout access is Day 1's.
  - `research/comparisons/` holds no FS1-family output.

## Scientific Validity

**M1, clause 2(a).**
- It now tests what it names, at nine airports. A pass supports static structure (with the scheduled local time) on NM-present rows outside LIRF. LIRF's static structure is reported under rule 7 but untested, as the proposal states.
- "The scheduled-time keys add no new delay information" on this population is correct as a statement about information. It does not hold `d_sched`'s use by the trees fixed (the late-departure exposure above).

**M1, clause 2(b)** (unchanged; a sign test).
- Its population includes LIRF NM-present bulk rows.
- **LIRF late departures** (`d_sched` ≥ 3,600 s, y < 3,600 s) are where the convention could be misapplied or separated better. They carry 2.1–10.0 % of E006's NM-present bulk SSE. A ±15 % change of that moves S1 by ±2.0 s and the other development folds by at most ±0.9 s.
- No single bulk row carries more than 0.41 % on a development fold.
- A falsification needs two folds, so the clause stays insulated. The fully insulated bulk figure is `per_fold.*.delta_rmse_bulk` of `mechanism_check.py <H009> E006 NM_present_excl_LIRF`, which chain step 1 produces anyway. Read 2(b) next to it.

**M2 (clause 4)** is unchanged and valid. One rule 6 addition, for the record only:
- **The row.** On W1, row **183910286** (LIRF, y 13,865 s, `d_aobt3` 16,622 s, `d_sched` 13,862 s) carried 0.80 of E011 − E006 on `NM_present`. E011 predicted 42,003 s for it.
- **What it can do.** An anchor extrapolation of that size by H009 would move H009 − H012 on W1 by about 11 s. That cannot decide a −40 to −100 s effect, but rule 6 may flag the row.

**M3 (clause 3)** is as accepted: it measures exact `d_sched` beyond the hour-resolution proxy, and a few rows decide it.

**Criterion 8 (the LIRF bulk trade, X-D01-S01-0004)** keeps the v1 and v2 resolution rule. The objection is resolved if both hold:
- clause 3 is not met, so M3 is supported;
- `NM_missing_LIRF.delta_rmse_bulk` against E005 is ≤ +6,500 s on every development fold.

B3 carries: an S1 WIN with an S1c point dRMSE ≥ 0 against E005 is an objection.

## Novelty Relative to Existing Research

**Not redundant** (as in v1 and v2).
- No completed experiment tests row-own static keys. H006 is INCONCLUSIVE and H007 is REJECT.
- v3 changes only the M1 test population and the reporting.

## Experimental Isolation

| Contrast | Population | Change | What can decide it | Status |
|---|---|---|---|---|
| H009 − E006, 2(a) (M1) | NM-present, not LIRF | + 6 keys | Static structure. Residual: the trees' use of `d_sched` on late departures (≤ 1.4 s on development folds, same-input evidence). No row carries more than 1.7 % of E006's SSE | **Adequate** |
| H009 − E006, 2(b) (M1) | NM-present bulk | + 6 keys | Bulk rows. LIRF late departures ±2.0 s on S1 | Insulated sign test |
| H009 − H012 (M2) | NM-present | − `d_aobt3`, `d_eobt1` | The anchor. Rows 192622644 (S1, S1c) and 183910286 (W1) can move a fold by about ±10–15 s | Adequate |
| H009 − H010 (M3) | LIRF NM-missing | − `d_sched` | Exact `d_sched` beyond the proxy; few rows | As accepted |

## Validation Quality

**Folds.**
- The frozen folds are used unchanged: seven scored folds plus H, with H predicted only.
- S1 is a required WIN. B1–B4 apply.

**Reuse of E006 and E010.** The X-D02-S01-0001 conditions hold today:
- `uv.lock` is `39df945c…`;
- `gbm.py` and `fs0` are unchanged;
- silver is pinned.

**Is each falsification clause decisive?**

| Clause | Verdict |
|---|---|
| 1 (promotion against E005, all rows) | Decisive |
| 2(a) (M1, criteria 1–2 on `NM_present_excl_LIRF`) | **Decisive on all five development folds.** No single record decides S1 or S1c |
| 2(b) (M1, NM-present bulk sign) | Insulated sign test |
| 3 (M3) | As accepted in X-D01-S01-0001 (H010) |
| 4 (M2) | Decisive |

**The rule 6 pre-registration for M1 is consistent with the evidence.**
- At −5 s on S1, the SSE change is about −4.4 × 10⁸. E006's largest row error² in the population is 1.5 × 10⁸.
- A single row could reach a 50 % share only through an error of about 19,000 s. No Day 1 tree model came close in this population, where the largest y is below 20,000 s.
- The pre-registered M2 dominant row (192622644 on S1 and S1c, sign undetermined) is right.

**Twins.**
- The same-input E011 − E006 comparison on this population gave **+29.9 s (LOSS) on W1c**, 73 % of it from late departures.
- W1c is highly specification-sensitive, and a W1c LOSS voids a W1 WIN.
- The pre-registered "W1c ≤ 0, TIE possible" is optimistic but is not a clause.

**The clause code is not frozen.**
- Clauses 1–4 are computed by `scripts/compare.py`, `scripts/mechanism_check.py` and `src/prc/attribution.py`, none of which the gate hash-checks.
- Pre-registration requires them unchanged from the reviewed state (Execution Authorization, precondition (d)).

**Seed variance.**
- The frozen bootstrap does not include seed variance, and E006 has no reproduction.
- In this population, a same-input model change produced −0.05 to +3.03 s on the development folds. S1 and W1 were classified LOSS, with interval half-widths of about 0.6 and 2.4 s. See Weakest Assumption.

## Leakage Review

### Target Leakage

PASS

- There are no target statistics.
- The rare collapse and the vocabularies are counts over training rows only.
- Validation `y` is null (tested on real silver).
- The new population is defined by `AOBT_3_flt` nullness and `ADEP_mvt` only. The rule 6 detail columns (`d_aobt3`, `d_sched`) are not targets.

### Temporal Leakage

CONCERN

These are label notes, unchanged from v2. They do not affect admissibility and are not blocking:
- `ades` is F on diversions (~0.03 % of rows);
- the T × P schedule-delay proxy is label T;
- stand is P on an assumption.

### Competition Availability

PASS

Every input is present for ranking DEP rows. Unseen levels (0.005–0.27 % against the January–November vocabulary) map to `__RARE__`.

## Compute Review

### RAM

PASS

Unchanged from v2: 4.5–5.5 GB expected on fold H, inside CLASS-M (8 GB).

### Runtime

PASS

- 11–18 minutes for H009. The timeout is 45 minutes.
- The sequential chain (H009, H010, H012, H011 and a conditional reproduction) takes about 70 minutes in all.

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

**The assumption.** On NM-present rows outside LIRF, the static-key effect is large compared with the tree-specification noise in the same population.

**The evidence.**
- A same-input change of model (E011 against E006) produced −0.05 to +3.03 s on the development folds. S1 and W1 came out LOSS on intervals of about ±0.6 and ±2.4 s. On W1c it produced +29.9 s.
- Much of this ran through the trees' use of `d_sched` on late departures (for example 45 % on W1 and 73 % on W1c).

**What follows.**
- At the expected −5 to −20 s, the assumption holds.
- At −2 to −4 s, the outcomes on S1 and the twins are partly decided by noise that the bootstrap does not model.

## Missing Control or Ablation

None is required for the stated claims. Two are named for the record:
- **A descriptive split of the M1 figure** on `NM_present_excl_LIRF` by late-departure status (`d_sched` ≥ 3,600 s or not). It would show whether a margin is static structure or a changed use of `d_sched`. It is not a clause.
- **The LightGBM seed scale.** The seed-43 reproduction supplies it only if H009 passes.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions (all must hold before `gate.py allocate H009 v3`).**
   - (a) `research/day-02/acks/H009_ack_v3.md` is committed, as specified below.
   - (b) `research/STATE.md` is refreshed, with a measured header time. The researcher committed to this in `H009_ack_v1.md` and `H009_ack_v2.md`. Today the file stops at X-D02-S01-0001 and lists H009 v2 as pending.
   - (c) The E006 and E010 reuse conditions hold: `uv.lock` is `39df945c…`, `gbm.py` and `fs0` are unchanged, and silver is pinned. The analysis records H009's `gate.json` `uv_lock_sha256`.
   - (d) `scripts/compare.py`, `scripts/mechanism_check.py` and `src/prc/attribution.py` stay unchanged from `5ba9230` until clauses 1–4 are computed. Any earlier change needs a new exchange.
   - (e) No other experiment runs concurrently.
2. **One primary run.**
   - `uv run python scripts/gate.py allocate H009 v3`.
   - Config: `model: lightgbm`, `feature_set: FS1`.
   - `params`: `objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 0.9`, `bagging_fraction: 0.8`, `bagging_freq: 1`, `num_threads: 4`, `num_boost_round: 1000`.
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
   - Then `uv run python scripts/run_experiment.py E###`.
3. **Comparisons** (completed experiments only), in chain order:
   - `compare.py <H009> E005` (clause 1; rules 1, 6 and 7);
   - `mechanism_check.py <H009> E006 NM_present_excl_LIRF` (clause 2(a));
   - `mechanism_check.py <H009> E006 NM_present` (clause 2(b));
   - `compare.py <H009> E006` (rules 1, 6 and 7);
   - `mechanism_check.py <H009> E006 LIRF_NM_missing` (Alternative Explanation 2; reported);
   - after H010 runs under its own ACCEPT: `mechanism_check.py <H009> <H010> LIRF_NM_missing` (clause 3) and `compare.py <H009> <H010>`;
   - after H012 runs under its own ACCEPT: `mechanism_check.py <H009> <H012> NM_present` (clause 4) and `compare.py <H009> <H012>`.

   H011 v2 then runs under its own ACCEPT.
4. **Conditional reproduction.** Only if H009 passes criteria 1–3 against E005 and none of clauses 2–4 is met:
   - one `reproduction` allocation of H009 v3, with seed 43 and everything else identical;
   - then `reproduce_check.py`.
5. **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun`, logged.
6. **Promotion.** Only if criteria 1–8 hold (B1–B4), with criterion 8 resolved under the rule in Scientific Validity. The Day 2 phase-close holdout check is governed by the frozen `phase_close` rule and the phase-close exchange, not by this authorization.
7. **Not authorized:**
   - any change to features, parameters, folds, seed or clause code;
   - any search or early stopping;
   - scoring H outside the frozen phase-close check;
   - redefining any population after the H009 run.

Required acknowledgement path: `research/day-02/acks/H009_ack_v3.md`.
- It must reference the proposal hash and this review's hash.
- It must adopt preconditions 1(a)–(e).
- It must record the criterion 8 resolution rule.
- It must record the residual exposures: late departures in 2(a), W1c sensitivity, LIRF late departures in 2(b), and row 183910286 for M2 on W1. They are not a change of claim.

## Revision

None required for this version.

**Process notes (non-blocking):**
- **INC-0003 is still open.** At 19:30Z the running researcher process still carries `--effort medium`.
  - The `MODEL_REGISTRY.md` requirement is met: the deviation was recorded before work continued.
  - The owner should resolve it. H009's analysis should cite it in its provenance.
- **The pre-registered `NM_present_LIRF.share_of_sse_change_tail` band (±0.3)** is relative to the all-rows SSE change of H009 − E006, which LIRF NM-missing rows dominate. Read it next to the fold's all-rows dRMSE, as the rule 6 caveat does.
- **The rule 2 twin expectations for M1** (S1c < 0; W1c ≤ 0) are read on `NM_present_excl_LIRF`, the clause population.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Passes criteria 1–3 against E005 (all rows) | 0.90 |
| Clause 2(a) not met (criteria 1 and 2 pass on `NM_present_excl_LIRF`) | 0.72 |
| Clause 2(b) not met (NM-present bulk dRMSE < 0 on at least 4 of 5 development folds) | 0.85 |
| Clause 3 not met (M3) | 0.78 |
| Clause 4 not met (M2) | 0.95 |
| No row with \|top-1 share\| ≥ 0.5 for M1 on S1 or S1c | 0.93 |
| W1c comes out LOSS on `NM_present_excl_LIRF` | 0.25 |
| v3 not falsified, and passes criteria 1–3 against E005 | 0.48 |

Expected magnitude:

| Quantity | Expected |
|---|---|
| Development mean (all rows) | 358–375 s |
| H009 − E006 on `NM_present_excl_LIRF` | −3 to −12 s per development fold (mean −4 to −10 s) |
| NM-present bulk dRMSE against E006 | −3 to −12 s per fold |
| M2 (H009 − H012, NM-present) | −40 to −90 s (mean) |

Primary expected failure mode:
- **Primary.** Clause 2(a) fails criterion 2 on one development fold, most likely R3 or W1. The static-key gain there is 3 s or less, and the trees' use of `d_sched` on late departures decides the fold's outcome. Alternatively, a W1c LOSS voids W1's WIN and one of R1–R3 comes out TIE.
- **Secondary.** Clause 3 fails on R3 and W1, where one to three long LIRF NM-missing records decide the sign.
