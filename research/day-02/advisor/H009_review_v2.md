---
schema: advisor-review-v1
hypothesis_id: H009
proposal_version: 2
proposal_sha256: 0afb084ef5d4594391ee804c1373859137fa6f1a300ce144ecaa5923a06b78b9
exchange_id: X-D02-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.80
created_utc: 2026-09-28T19:12:21Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE.**

v2 addresses all six v1 items, and I found no leakage. One defect remains, and it is of the kind v1 raised: **the M1 clause's required S1 outcome can be decided by something other than static structure.** A pre-registered clause cannot be repaired after the runs, so this needs a new version. Everything else in v2 is acceptable as written.

**What v2 fixes:**

| v1 item | Status in v2 |
|---|---|
| 1. M1 insulated from LIRF NM-missing | Done. Clause 2(a) now runs on `NM_present`, so the LIRF NM-missing subgroup cannot decide it. A new exposure inside that population is described below |
| 2. M2 with `d_sched` held fixed | Done. H009 − H012 on NM-present rows (H012 = FS1 − {`d_aobt3`, `d_eobt1`}) |
| 3. M3 proxy, lower-bound reading, AE2 contrast | Done |
| 4. Committed code | Done (`19ba509`). One gap remains: rule 6 on the mechanism-check populations (Revision item 3) |
| 5. Evidence corrections (a)–(f) | Done and verified (below) |
| 6. Conditional reproduction | Done |

**The remaining defect: one record can decide M1's required S1 WIN.**
- **The record.** Row **192622644** (LIRF, July 2025) has y = 87,002 s, `d_aobt3` = 87,181 s and `d_sched` = 87,001 s. It is NM-present, anchor-exact and block-at-schedule at once.
- **Its weight.** It carries **23.2 % of E006's NM-present SSE on S1** (24.0 % on S1c). On R1, R2, R3, W1 and W1c, no NM-present row carries more than 1.2 %.
- **Tree models extrapolate it very differently:**

  | Model | S1 prediction (s) | S1c prediction (s) |
  |---|---|---|
  | E006 (LightGBM FS0) | 16,545 | 14,395 |
  | E011 (XGBoost FS0) | 26,884 | 24,188 |
  | E005 (ridge) | 2,513 | 2,548 |
  | E010 (LightGBM, no deltas) | 1,009 | 1,027 |

- **Evidence from completed Day 1 runs** (E011 − E006 on NM-present rows, same FS0 inputs):

  | Fold | dRMSE, all NM-present rows | Without row 192622644 |
  |---|---|---|
  | S1 | −10.52 s (TIE) | +0.37 s (TIE) |
  | S1c | −8.44 s (TIE) | +2.30 s (**LOSS**) |

  The row alone moves S1 by about 11 s, as much as the whole expected M1 effect (−5 to −20 s).

- **Sensitivity of the frozen S1 outcome.**
  - Method: E006's stored predictions against themselves, an idealised uniform NM-present bulk gain, and a shift of this row's prediction only. The frozen `paired_bootstrap` and `fold_outcome` were then applied. No model was fitted.

    | NM-present bulk dRMSE on S1 | Shift of this row's prediction that turns S1 from WIN into TIE |
    |---|---|
    | −3 s | −1,500 s |
    | −6 s | −3,000 s |
    | −10 s | −5,000 s |

  - A real bulk change is not uniform and widens the interval, so these thresholds are optimistic. S1c behaves the same way.
- **Consequence.**
  - Clause 2(a) applies criterion 2, which requires an S1 WIN (and an S1c that is not LOSS).
  - H009 can therefore be falsified, and under B2 not promoted, by one record's extrapolated prediction, while the NM-present bulk improves on every fold.
  - The reverse, an S1 WIN produced by this row, is also possible. Clause 2(b) limits that only to a sign.
- **A smaller exposure on the same folds.**
  - S1 has 271 LIRF NM-present tail rows, 180 of them block-at-schedule.
  - Together with row 192622644 they carry 33.6 % of E006's NM-present SSE on S1; without it, about 10 %.
  - A ±15 % change of that subgroup's SSE moves S1 by ±8.5 s, or ±2.7 s without the row. On R1–R3 and W1 the same change moves the fold by ±0.6 to ±1.9 s.
- **Not pre-registered.** The proposal's rule 6 names only row 183903219 (W1 and W1c against E005). No committed code reports row concentration on a mechanism-check population.

**Verified here.** All checks were read-only: no December target was read, and no model was fitted, scored or allocated.
- **Hashes.**
  - All three proposal hashes match the envelope.
  - The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json`.
  - `.claude/agents/advisor.md` is `30fff5dd…` and `uv.lock` is `39df945c…`.
  - The tree is clean at `d02c4e3`.
- **Tests and lint.** `pytest` passes 98/98 (the 96 from X-D02-S01-0001 plus 2 new), and `ruff` is clean.
- **Code.**
  - `fs1`, `fs0`, `local_time` and `collapse_rare` are unchanged since `cba278d`; the diff only appends `fs1_no_anchor` and `fs1_static_no_deltas`.
  - `src/prc/models/gbm.py` is unchanged since `866b902`.
  - `scripts/mechanism_check.py`:
    - it restricts truth and both predictions to the population and applies the frozen `promotion_check` unchanged;
    - its per-fold bulk uses the frozen `BULK_MAX_S`;
    - `nm_missing` is `AOBT_3_flt` null, the same definition as FS0's `flt_missing` and rule 7;
    - the E006 − E005 NM-present figures in `E006_vs_E005_mech_NM_present.json` reproduce: S1 −56.75, S1c −53.88; mean −46.28, q95 −43.01; 7/7 WIN; bulk −31.4 to −40.2.
- **Rule 7 tail shares.**
  - E006 − E005 `NM_missing_LIRF.share_of_sse_change_tail`:

    | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
    |---|---|---|---|---|---|---|
    | 0.973 | 0.398 | 0.776 | 1.038 | 0.724 | 1.095 | 0.762 |

  - v2's "0.40–1.04" and its band 0.3–1.1 are consistent with the committed tool.
- **Evidence corrections.** `supplement.json` reproduces the cited values:
  - ranking-unseen shares against the January–November vocabulary: 0.098 / 0.005 / 0.268 / 0.069 %;
  - 20,821 NM-missing rows, and the presence shares;
  - the definitional ≤ 1 h band;
  - the build check: 3.16 s and 4.27 GB.
- **Timestamps.** `created_utc` 18:52:02Z equals the file time and the envelope time.
- **State.**
  - No Day 2 experiment has been allocated.
  - The only holdout access is Day 1's.
  - No configured secret value appears in any of the 257 tracked files.

**H010's preconditions (envelope request).**
- **(b) holds.** `fs1` is unchanged, and the model, parameters, folds and seed are identical to v1.
- **(c) holds.** The M3 clause keeps the LIRF NM-missing subgroup, the full dRMSE and the rule "≥ 0 on 3 of 5 → falsified". It is now tied to `mechanism_check.py … LIRF_NM_missing: per_fold.*.delta_rmse_full`.
- **(a) is not met,** because this version is REVISE.
- H010 v1's ACCEPT does not lapse. It stays unallocatable until an H009 version ≥ 3 is ACCEPTED and acknowledged, and that version must again keep (b) and (c).

## Scientific Validity

**M1 (static structure).**
- The mechanism is plausible. On NM-present rows the anchor already measures most of the taxi interval, so static keys can only reduce its residual.
- Judging M1 on NM-present rows (clause 2(a)) and on their bulk (clause 2(b)) is right in principle.

**What the NM-present population still contains:**
- **The LIRF convention, reached through `d_sched`, not through the anchor.**
  - From January to November, 932 of the 1,176 LIRF NM-present tail rows are block-at-schedule.
  - **931 of those have a normal anchor** (median 1,077 s). The single exception is row 192622644.
  - So on NM-present rows the convention is reached through `d_sched`, and the static keys can act as identifiers of convention-prone flights. Alternative Explanation 2 applies to NM-present LIRF rows, not only to NM-missing ones.
- **The day-scale anchor-exact record.** Its prediction is an extrapolation of the anchor (M2 territory) on a block-at-schedule record (M3 territory). Static structure has nothing to do with it.

**M2 (clause 4) is valid.**
- With `d_sched`, `flt_missing`, the static keys and the time keys held fixed, H009 − H012 measures the anchor's contribution.
- It attributes the gain to the anchor inputs, not to the non-linearity of their use. That contrast is Day 1's E006 − E005.
- Row 192622644 enters here too: it is anchor-exact, and H012 must extrapolate `d_sched` = 87,001 s instead. It can move S1 by roughly ±10–15 s, which cannot decide an effect of −40 to −100 s.

**M3 (clause 3).** Unchanged, and correctly read as what exact `d_sched` adds beyond the proxy. As the H010 review recorded, a few rows decide it.

**Criterion 8 (the LIRF bulk trade from X-D01-S01-0004).** The v1 resolution rule carries over to the accepted version. The objection is resolved if both of the following hold:
- the M3 clause holds;
- the LIRF NM-missing bulk dRMSE against E005 is ≤ +6,500 s on every development fold.

## Novelty Relative to Existing Research

**Not redundant** (as in v1).
- No completed experiment tests row-own static keys.
- H006 is INCONCLUSIVE and H007 is REJECT.
- The candidate answers brief §11 Day 2 and DAY_SUMMARY open questions 1 and 4.

## Experimental Isolation

| Contrast | Population | Change | What can decide it | Status |
|---|---|---|---|---|
| H009 − E006, clause 2(a) (M1) | NM-present | + 6 keys | R1–R3, W1: static structure (tail swing ±0.6 to ±1.9 s). **S1, S1c:** row 192622644 (±11 s between two tree models) and the LIRF NM-present convention tail | **Defect on S1 and S1c** |
| H009 − E006, clause 2(b) (M1) | NM-present bulk | + 6 keys | Bulk rows only | Insulated; a sign test |
| H009 − H012 (M2) | NM-present | − `d_aobt3`, `d_eobt1` | The anchor. Row 192622644 adds about ±10–15 s on S1 | Adequate |
| H009 − H010 (M3) | LIRF NM-missing | − `d_sched` | Exact `d_sched` beyond the proxy; few rows | As accepted |

## Validation Quality

**Folds.**
- The frozen folds are used unchanged: seven scored folds plus H, with H predicted only.
- S1 is a required WIN.
- B1–B4 apply, and B3 is adopted.

**Reuse of E006 and E010.** The conditions of X-D02-S01-0001 still hold:
- `uv.lock` is `39df945c…`;
- `gbm.py` and `fs0` are unchanged;
- silver is pinned, and the evaluator re-verified it on every truth read in this review.

The lapse rule stands.

**Is each falsification clause decisive?**

| Clause | Verdict |
|---|---|
| 1 (promotion against E005, all rows) | Decisive |
| 2(a) (M1, criteria 1–2 on NM-present rows) | Decisive on R1–R3 and W1. **Not decisive on S1 and S1c** (row 192622644), and S1 is the required WIN |
| 2(b) (M1, NM-present bulk sign) | Insulated from the tail; a sign test only |
| 3 (M3) | As accepted in X-D02-S01-0001 |
| 4 (M2) | Decisive; the expected effect is far larger than the one-row swing |

**Rules 6 and 7 for M1.**
- Standing rules 6 (B4) and 7 cover every criterion-4 comparison. For H009 against E006, however, the chain runs only `mechanism_check.py`: `compare.py <H009> E006` is not in the plan.
- The all-row figures would not show the NM-present decider anyway. On S1, the largest all-row contributions to H009 − E006 are likely LIRF NM-missing records.

## Leakage Review

### Target Leakage

PASS

The situation is unchanged from v1:
- there are no target statistics;
- the rare collapse counts training rows only, and the vocabularies come from training rows;
- validation `y` is null (tested on real silver).

### Temporal Leakage

CONCERN

These are label notes, all stated in v2. They do not affect admissibility and are not blocking:
- `ades` is F on diversions;
- the T × P schedule-delay proxy is label T;
- stand is P on an assumption.

### Competition Availability

PASS

Every input is present for ranking DEP rows. Unseen levels map to `__RARE__`:
- 0.005–0.27 % against the January–November vocabulary;
- 0.005–0.26 % against January–December, which is what the SUBMIT folds train on.

## Compute Review

### RAM

PASS

- E006 peaked at 3.74 GB, and the FS1 build plus the silver load at 4.27 GB (S1).
- Fold H is about 21 % larger. Expect 4.5–5.5 GB, inside CLASS-M (8 GB).

### Runtime

PASS

- E006 took 676 s. H009 has 17 features against 11, four of them high-cardinality categoricals.
- Expect 11–18 minutes. The timeout is 45 minutes.
- The sequential chain (H009, H010, H012, H011 and a conditional reproduction) takes about 70 minutes in all.

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

**The assumption.** The NM-present population measures static structure on every development fold.

**Why it fails on S1 and S1c:**
- one anchor-exact, block-at-schedule, day-scale record carries a quarter of the reference model's NM-present SSE;
- two tree models on identical inputs differ on it by 10,000 s, which is 11 s of S1 RMSE;
- criterion 2 requires S1 to WIN.

## Missing Control or Ablation

- **M1:** a test whose S1 and S1c outcomes that record cannot decide. The population, statistic or rule is the researcher's choice.
- **Rule 6 (B4)** on each mechanism-check population, and **rule 7** for the M1 comparison.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- No FS1-family run (H009, H010, H011 or H012) may be allocated before an H009 version ≥ 3 is ACCEPTED and acknowledged. Any earlier FS1-family outcome would reveal the static-key effect before the M1 clause is fixed.

Required acknowledgement path: none for v2. Submit `research/day-02/proposals/H009_v3.md` in a new exchange.

## Revision

**Required (minimal):**

1. **M1 clause 2(a), S1 and S1c.**
   - Re-specify it so that the S1 and S1c outcomes cannot be decided by row 192622644 (y 87,002 s, `d_aobt3` 87,181 s, `d_sched` 87,001 s).
   - The population, statistic or decision rule is the researcher's choice.
   - A new population must be defined in committed code, with a test, before the first FS1-family run.
2. **Rule 8 for M1 on NM-present LIRF rows.** State how the LIRF NM-present block-at-schedule tail rows enter M1:
   - in July, 180 of the 271 LIRF NM-present tail rows are block-at-schedule;
   - from January to November, 931 of 932 such rows have a normal anchor, so they are reached through `d_sched` and possibly identified by the static keys.

   Either insulate M1 from them, or pre-register their tail and bulk expectations and an S1 expectation. Extend Alternative Explanation 2 to them.
3. **Rules 6 and 7 on every criterion-4 comparison.**
   - Add `compare.py <H009> E006` to the chain.
   - Make committed code report the rule 6 figures on each mechanism-check population (M1, M2, M3), per development fold and twin: the top-1 and top-10 shares of the SSE change, and the dominant-row details where one row carries ≥ 50 %.
   - Pre-register the expected dominant row for M1 and M2 on S1 and S1c.
4. **Carry-over.** Keep H010's preconditions (b) and (c), and clause 4 exactly as written, which H012 v1 depends on (`H012_review_v1.md`).

**Acceptable as is:**
- FS1, the model, parameters, folds, seed and class;
- clause 1, clause 2(b), clause 3 and clause 4;
- the rule 8 pre-registration of M3 against E005;
- the twin expectations;
- the chain order and the conditional reproduction;
- the evidence corrections.

**Process notes (non-blocking):**
- **`research/STATE.md`.** Its header says "Updated 2026-09-28T18:58Z". That is later than its own commit (`d0c4f82`, 18:46:43Z) and later than this envelope (18:52:02Z), so it is not a measured time. Correct it at the next refresh.
- **`research/day-02/acks/H010_ack_v1.md`.** It labels the January–December-vocabulary shares (0.08 / 0.26 / 0.05 %) as "against the Jan–Nov training vocabulary". The January–November figures are 0.098 / 0.268 / 0.069 % (`supplement.json`). Append a correction.
- **Researcher effort (unverified).**
  - The running Claude Code process's launch arguments include `--effort medium`.
  - `orchestration/session-registry.jsonl` and `SESSION_START.md` record `high` for D02-S01. The recorded model has a metadata source; the effort does not.
  - I did not inspect the harness settings, which may override the flag.
  - The owner or researcher should verify this. If the session runs at medium, record it under `docs/incidents/` (brief §2 and §6.1; `MODEL_REGISTRY.md`).

## Advisor Prediction

Probability of improvement, for the v2 configuration:

| Event | P |
|---|---|
| Passes criteria 1–3 against E005 (all rows) | 0.90 |
| NM-present bulk dRMSE against E006 < 0 on ≥ 4 of 5 development folds (clause 2(b)) | 0.85 |
| Clause 2(a) passes as written | 0.60 |
| Removing row 192622644 would change S1's outcome in clause 2(a) | 0.30 |
| M2 (clause 4) passes | 0.96 |
| M3 (clause 3) passes | 0.80 |
| v2 not falsified, and passes criteria 1–3 against E005 | 0.40 |

Expected magnitude:

| Quantity | Expected |
|---|---|
| Development mean | 358–375 s |
| NM-present bulk dRMSE against E006 | −3 to −12 s per fold |
| S1 NM-present full dRMSE against E006 | About 0.78 × the S1 bulk dRMSE, plus −11 to +11 s from row 192622644 |

Primary expected failure mode:
- S1 in clause 2(a) comes out TIE because of row 192622644 while the NM-present bulk improves on every fold. H009 is then falsified by one record.
- Secondary: W1c, trained on January alone, comes out TIE.
