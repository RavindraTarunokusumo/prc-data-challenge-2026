---
schema: advisor-review-v1
hypothesis_id: H012
proposal_version: 1
proposal_sha256: d4ad80e4a91f7bd68d5a8583420001b995981da4c43c089ab7519ba59e399e85
exchange_id: X-D02-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-09-28T19:14:58Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT, with preconditions and lapse conditions (as for H010).**

**H012 is a clean two-column ablation, and it supplies the contrast `H009_review_v1.md` required: the anchor removed with `d_sched` held fixed.**
- `fs1_no_anchor` = FS1 minus exactly {`d_aobt3`, `d_eobt1`}, asserted on real silver (R1 and W1c).
- `d_sched`, `flt_missing`, the four static keys and the four time keys are kept.
- The model, parameters, seed, folds and rare collapse are H009's.
- M2 is judged on NM-present rows, the only rows where the anchor exists. On NM-missing rows the anchor is null in both models.

**Why conditions.** H012 has meaning only inside H009's chain, and H009 v2 is REVISE (`H009_review_v2.md`).
- Running H012 earlier would reveal the static keys' effect in a no-anchor context before H009's M1 clause is fixed.
- It must also lapse if the accepted H009 version changes clause 4, or anything else H012 depends on.

**Rule 8 is engaged by exactly one record.** "Recording convention: not engaged" holds for NM-present rows with one exception.
- From January to November, **931 of 932** LIRF NM-present block-at-schedule tail rows have a normal anchor (median 1,077 s). The anchor does not carry the convention there. `d_sched` does, and `d_sched` is in both models.
- The exception is row **192622644** (S1 and S1c): y 87,002 s, `d_aobt3` 87,181 s, `d_sched` 87,001 s. It is anchor-exact and block-at-schedule at once, and carries 23–24 % of E006's NM-present SSE on S1 and S1c.
  - Without the anchor, H012 must extrapolate `d_sched` on it.
  - That can move H009 − H012 on S1 by roughly ±10–15 s in either direction, well below the expected −40 to −100 s.
  - The M2 clause stays decisive, but the row should be pre-registered as S1's expected dominant row (H009 review, Revision item 3).

**One inconsistency in the Expected Result (record only).**
- The development mean of 430–480 s does not follow from the NM-present expectation of 300–350 s.
- With E006's NM-missing SSE per fold, an NM-present RMSE of 300 or 350 s gives an all-rows development mean of about **407 or 445 s**:

  | Fold | R1 | R2 | R3 | S1 | W1 |
  |---|---|---|---|---|---|
  | All-rows RMSE (s) | 410–448 | 326–372 | 364–406 | 501–532 | 433–469 |

- It is not a clause, but the acknowledgement should record it.

**Verified here** (read-only). The batch checks in `H009_review_v2.md` cover H012: hashes, frozen files, tests 98/98, lint, secrets, and the code of `fs1` and `mechanism_check.py`.

## Scientific Validity

**The contrast.** On NM-present rows, H009 − H012 measures what the NM off-block estimates (`AOBT_3`, `EOBT_1`) add once `d_sched`, the static keys and the time keys are available.
- `d_sched` mixes gate delay into the taxi interval, so it is the noisier stand-in (audit proxy RMSE: 2,413 s against 385 s).
- The ablation attributes the gain to the two anchor inputs jointly, as the proposal states. No clause attributes it to one of them, or to the non-linearity of their use.

**The magnitudes are plausible.** On NM-present rows (development-fold RMSE):

| Model | Range | Mean |
|---|---|---|
| E010 (no deltas at all) | 319–433 s | 363 s |
| E006 (all FS0 deltas) | 226–338 s | 264 s |

H012 keeps `d_sched` and adds the static keys, so it should land between them. The proposal's 300–350 s and M2's −40 to −100 s are consistent with that.

**LIRF NM-missing ("near 0").** This is optimistic.
- H012's trees spend no splits on the anchors, so their structure differs on rows where both models see the same inputs.
- The LIRF NM-missing subgroup carries a large part of both models' SSE, so a few percent change there can reach the pre-registered |share| < 0.2 bound.
- It is a disclosure, not a clause.

## Novelty Relative to Existing Research

This is new. H008 (E010) removed `d_aobt3`, `d_eobt1`, `d_sched` and `flt_missing` together. No completed experiment removes the anchor alone.

## Experimental Isolation

**Good: two columns.** The contrast is H009 against H012, with the same code path, seed, folds and rare collapse, and with `d_sched` held fixed.

**Residual:** row 192622644 (above). It is the only NM-present record where removing the anchor also changes access to the convention.

## Validation Quality

**Folds.**
- The frozen folds are used unchanged: seven scored folds plus H, with H predicted only.
- Twin signs are pre-registered: H012 − H009 > 0 on the NM-present rows of S1c and W1c.

**The clause** belongs to H009 (clause 4): frozen criteria 1 and 2 on `NM_present`, from committed code. It is decisive. The expected effect exceeds the one-row swing on S1 by a wide margin, and the other folds have no dominant NM-present row (≤ 1.2 % of E006's NM-present SSE per row).

**Disclosures.**
- `compare.py <H009> <H012>` (rules 1, 6 and 7) is planned.
- Rule 6 on the NM-present population needs the committed code that `H009_review_v2.md` Revision item 3 requires.

## Leakage Review

### Target Leakage

PASS

- There are no new inputs: it is FS1 minus two columns.
- There are no target statistics. The collapse and vocabularies are counts from training rows only.

### Temporal Leakage

CONCERN

These are label notes, as in H009, and are not blocking:
- `ades` is F on diversions;
- `d_sched` and the derived hour-resolution proxy are T;
- the takeoff hour and weekday are T.

### Competition Availability

PASS

- Every input is present for ranking DEP rows. Unseen levels map to `__RARE__`.
- The ablation itself informs the 1.5 % of ranking DEP rows without NM data.

## Compute Review

### RAM

PASS

About 4.5–5.5 GB on fold H, as for H009 (CLASS-M: 8 GB).

### Runtime

PASS

11–17 minutes (15 features). The timeout is 45 minutes.

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

**The assumption.** H009 − H012 on NM-present rows is free of the recording convention.

**Where it fails.** It holds for 931 of 932 LIRF NM-present block-at-schedule tail rows. It fails on the one anchor-exact block-at-schedule record in S1 and S1c, which is also S1's dominant row.

## Missing Control or Ablation

None is required for its stated purpose.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions (all must hold before allocation).**
   - (a) An H009 version ≥ 3 has decision ACCEPT, and its acknowledgement is committed.
   - (b) That version keeps FS1 exactly (`src/prc/features.py: fs1` as at `cba278d`, or byte-identical output), with H009 v2's model, parameters, folds and seed.
   - (c) That version keeps clause 4 exactly: `scripts/mechanism_check.py <H009> <H012> NM_present`. H009 is falsified if it fails frozen criterion 1 or criterion 2 there.
   - (d) The H009 and H010 primary runs are COMPLETE.
   - (e) No other experiment runs concurrently.
2. **Lapse.** If (b) or (c) does not hold, this ACCEPT lapses and `H012_v2` is required.
3. **One primary run.**
   - `uv run python scripts/gate.py allocate H012 v1`.
   - Config: `model: lightgbm`, `feature_set: FS1_NO_ANCHOR`.
   - `params`: `objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 0.9`, `bagging_fraction: 0.8`, `bagging_freq: 1`, `num_threads: 4`, `num_boost_round: 1000`.
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
   - Then `uv run python scripts/run_experiment.py E###`.
4. **Comparisons** (completed experiments only; no new run):
   - `scripts/mechanism_check.py <H009> <H012> NM_present` (clause 4);
   - `scripts/compare.py <H009> <H012>` (rules 1, 6 and 7);
   - the rule 6 figures on the NM-present population, from the committed code required by `H009_review_v2.md`.
5. **Re-run after an infrastructure failure.** One identical re-run with `--purpose rerun`, logged.
6. **Not authorized:**
   - a reproduction run (H012 is not a candidate);
   - any change to features, parameters, folds or seed;
   - use as a promotion candidate or champion;
   - scoring H.

Required acknowledgement path: `research/day-02/acks/H012_ack_v1.md`.
- It must reference the proposal hash and this review's hash.
- It must adopt preconditions 1(a)–(e) and the lapse rule.
- It must record the Expected Result inconsistency (development mean against the NM-present range).
- It must record that rule 8 is engaged by one NM-present record, 192622644 (S1 and S1c).

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| H009 − H012 passes criteria 1 and 2 on NM-present rows (M2 supported) | 0.96 |
| H012 − H009 > 0 on the NM-present rows of both S1c and W1c | 0.95 |
| \|LIRF NM-missing share of the H012 − H009 SSE change\| < 0.2 on every development fold (pre-registered) | 0.55 |

Expected magnitude:

| Quantity | Expected |
|---|---|
| NM-present development mean | 295–340 s |
| All-rows development mean | 400–450 s |
| M2 (H009 − H012 on NM-present rows) | −40 to −85 s (mean) |

Primary expected failure mode:
- On S1, H012's extrapolation of `d_sched` on row 192622644 lands closer to its target than H009's anchor extrapolation. That shrinks S1's M2 margin by about 10–15 s, which is not enough to change the outcome.
- Secondary: tree-structure changes move the LIRF NM-missing predictions and break the |share| < 0.2 disclosure.
