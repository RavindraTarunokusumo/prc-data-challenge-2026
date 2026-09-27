---
schema: advisor-review-v1
hypothesis_id: PHASE_CLOSE_D01
proposal_version: 1
proposal_sha256: 811b313c18a93a2f91751e145f961ed1cd8f253c3fda850c058f4872da7ef770
exchange_id: X-D01-S01-0004
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-09-27T13:38:06Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**
- The Day 1 decisions stand.
- The single phase-close holdout access (E005 against E001) is authorized.
- The acknowledgement must append seven record corrections (C1–C7) **before** the access. They change no decision; they change what Day 1 is recorded as having shown.

**Attack on the champion E005.** I tried to show that E005 is wrong. I found no rule violation.
- Every criterion re-verifies from the stored predictions.
- I recomputed the criterion-4 clip attribution independently. It is identical to three decimals.
- The strongest case against E005 is about the model family, not a defect in E005. On rows with NM data (98–99 % of each fold), E006's RMSE is 40–57 s below E005's on every development fold (C1). E005 holds the title because the only candidate that beats it also carries an unregistered behaviour at LIRF.

**Attack on the H006 decision.** INCONCLUSIVE is correct, and the case for it is stronger than the proposal says. Two parts of the reasoning behind it are wrong, however:
1. **"The margin is 99 % tail" is a netting artifact.**
   - On NM-present rows, H006's bulk dRMSE against ridge is −31 to −40 s on every development fold.
   - The pooled bulk *loss* on S1 and R1 comes entirely from LIRF departures without NM data. H006 predicts those at a median of 2,545–3,856 s even when the truth is below 3,600 s.
   - DAY_SUMMARY §5 item 3 ("tree models are worse than ridge in the bulk") therefore misdiagnoses the cause.
2. **The NM-missing tail is not P-labelled, and it is mostly not taxiing.**
   - At LIRF, 90 % of NM-missing tail rows have a recorded block time within 120 s of the scheduled time; for NM-present tail rows the figure is 79 %.
   - For those rows the target equals `d_sched` (takeoff minus schedule), which is label **T**.
   - `flt_missing` (P) only raises the prior that a row is such a record.

**What the holdout check can show.**
- It is operationally ready: coverage verified without reading targets, and no prior access in `day-01`.
- It is almost uninformative. On the development folds E005 WINs all seven folds against E001, and every q90 bound is ≤ −67 s.
- It guards against gross failure only. It cannot confirm E005 over E002, E003 or E006.

**Verified here** (read-only; no December target read; `holdout_check.py` not run):
- **Proposal and ledger hashes.**
  - The proposal SHA-256 matches the envelope.
  - The proposal, review and ack hashes of all 11 ledger records match their files.
- **Frozen and pinned files.**
  - The six frozen files match `config/frozen.json`.
  - The SPLITS v2 proposal, review and ack match their pins.
  - `.claude/agents/advisor.md` matches `config/agents.yaml`.
- **Exchange mirrors.** The checksums of X-D01-S01-0001 to -0003 verify (4, 4 and 18 files).
- **Tests.** `pytest` 90/90 passes, `ruff` is clean, and the tree is clean at `bad75b6`.
- **Holdout accesses.** The task ledger has no `holdout_access` event.
- **Secrets.** No configured secret value appears in any tracked file.
- **Commits after the envelope.** `bad75b6` adds the draft `research/day-01/DAY_SUMMARY.md` only. It is outside the envelope. I read it because it carries the C1 misdiagnosis.

## Scientific Validity

### (a) Champion E005 (H004 ridge): the promotion re-verifies

| Check | Result |
|---|---|
| Against E003 (criteria 1–3) | Mean −65.70 s (q95 −59.56); 7/7 WIN, including S1 (−48.33) and S1c (−48.64) |
| Tail share against E003 | 0.254 |
| Largest single row against E003 | Carries ≤ 0.021 of each fold's change |
| Pooled airport RMSE against E003 | −3.8 % (LIRF) to −28.9 % (EDDF) |
| Pooled bulk RMSE against E003 | −54 to −98 s at every airport |
| Against E004, the criterion-4 ablation | Mean −67.92 s; 7/7 WIN; tail share 0.052 |
| Clip attribution, **recomputed independently** | Clips [299, 2430], [298, 2405], [298, 2402], [298, 2420], [298, 2394]<br>Rows beyond the clip: 1,865, 1,673, 1,690, 1,905, 2,144<br>Shares: 0.395, 0.350, 0.263, 0.048, 0.106<br>All identical to `E005_vs_E004_clip_attribution.json` |
| Beyond-clip rows | Ridge beats the raw anchor there too (R1: 697 against 1,915 s), so the clip is protective |
| B3, criterion 7 | B3 holds. Criterion 7: 94 s, 3.755 GB, CLASS-S |
| Reproduction E009 | Identical. Ridge's `sparse_cg` solve does not consume the seed, so criterion 6 is a determinism check only for this model. That is inherent in the frozen rule, and not a defect. |

**Long anchors (d_aobt3 ≥ 3,600 s).** January 2026 has three times the 2025 density of these rows. On the development folds:
- only 4–28 % of them have y ≥ 3,600 s;
- the median |y − anchor| is 2,142–3,452 s;
- ridge beats the raw anchor on them on every fold except S1 and its twin S1c, where the day-scale row decides.

The clip is therefore the safer default. Its cost in the January EHAM cluster remains unmeasurable, as recorded in the H005 and H006 reviews.

### (b) H006 INCONCLUSIVE: correct, but the recorded reasoning is wrong in two places

**Decomposition** of E006 − E005 (my analysis; attribution only, no outcome changes):

| Fold | Full dRMSE | Pooled bulk dRMSE | Bulk dRMSE, NM-present rows | Full dRMSE without the LIRF NM-missing rows | LIRF NM-missing bulk rows: n; dRMSE on them |
|---|---|---|---|---|---|
| R1 | −102.5 | **+5.2** | **−32.9** | −41.0 | 94; +5,514 |
| R2 | −45.7 | −19.9 | −32.0 | −41.2 | 58; +3,591 |
| R3 | −125.4 | −35.5 | −39.3 | −42.0 | 16; +1,985 |
| S1 | −145.5 | **+46.3** | **−31.4** | −55.1 | 218; +5,782 |
| W1 | −105.2 | −33.2 | −40.2 | −42.9 | 14; +2,761 |
| S1c | −127.5 | +54.1 | −31.6 | −53.5 | 218; +6,229 |
| W1c | −91.8 | −8.8 | −17.2 | −32.3 | 14; +2,343 |

**Share of each fold's SSE change** (a positive share has the same sign as the total, i.e. it is a gain):

| Fold | LIRF, no NM, tail rows | LIRF, no NM, bulk rows | Other airports, NM present, bulk rows |
|---|---|---|---|
| R1 | +0.97 | −0.23 | +0.18 |
| R2 | +0.40 | −0.21 | +0.51 |
| R3 | +0.78 | −0.01 | +0.18 |
| S1 | +1.04 | −0.28 | +0.10 |
| W1 | +0.72 | −0.01 | +0.18 |

**What E006 does on LIRF NM-missing rows:**
- On the bulk rows its median prediction is 2,545–3,856 s, against about 1,700 s for ridge. On S1, 115 of the 218 bulk rows are predicted above 3,600 s.
- Its largest prediction on these rows is 34,034–48,989 s.

**H006 on NM-present rows:**
- H006 beats ridge in every taxi band on R1–R3 and W1. On S1 it loses only 1,200–1,800 s (279 against 272).
- Its development mean on NM-present rows is 263.8 s against 310.0 s, i.e. −14.9 %. That is inside the pre-registered "5–15 % below the better of H004 and H005".

**Consequences.**
- The pre-registered bulk mechanism of H006 (nonlinear airport × runway × delay corrections) is real on 98–99 % of rows.
- The 0.991 tail share is the sum of three pieces:
  - that bulk gain;
  - a bulk loss confined to LIRF NM-missing rows;
  - a large tail gain on the same LIRF rows.
- Standing rule 1 was still applied correctly. The candidate *as a whole* includes the LIRF behaviour, and a pooled LIRF bulk RMSE +210.9 s worse than ridge is an unresolved objection under criterion 8 in its own right.
- No retroactive promotion. The proposal's path (pre-register on Day 2) is right.

### (c) What the "NM-missing tail" actually is

Target facts below use January–November 2025 only.

- **LIRF DEP without NM data: 1,400 rows, of which 688 are tail rows (49.1 %).**
  - In 90.1 % of these tail rows, |y − `d_sched`| < 120 s, i.e. the recorded block time equals SCHED_TIME.
  - Within the tail, corr(y, `d_sched`) = 0.949. For NM-missing bulk rows the block-at-schedule share is 5.1 %.
- **All LIRF tail rows: 1,552 of 1,864 (83.3 %) are block-at-schedule,** against 24.5 % of LIRF bulk rows.
  - At the other nine airports, 0–16.7 % of tail rows are, at or below their bulk base rates (11.1–19.4 %).
  - The convention is specific to LIRF.
- **Across all airports,** 45.7 % of tail rows are block-at-schedule, and they carry 26.9 % of the constant-mean SSE.
- **E006 approximates the convention through `d_sched`.** On LIRF NM-missing validation rows, its predictions correlate 0.67–0.95 with `d_sched`.
- **Dominant rows.** Three of the four dominant LIRF rows in the B4 reports have y − `d_sched` ≤ 5 s:

  | MVT_ID | y (s) | `d_sched` (s) |
  |---|---|---|
  | 183903219 | 131,167 | 131,163 |
  | 192622644 | 87,002 | 87,001 |
  | 198941714 | 11,349 | 11,344 |

  The exception is 192628959 (87,186 s, with `d_sched` 58,563 s).

### (d) Calibration: NM-missing rows carry the metric

NM-missing rows are 0.77–2.06 % of each development fold, yet they carry a large share of every model's SSE:

| Model | Share of SSE from NM-missing rows | RMSE on NM-present rows (s) |
|---|---|---|
| E004 | 0.14–0.59 | 360–466 (mean 397) |
| E005 | 0.22–0.66 | 271–395 (mean 310) |
| E006 | 0.22–0.60 | 226–338 (mean 264) |

- The audit's §6.3 proxy RMSE (384.9 s, 98.9 % coverage) excludes these rows.
- That explains the magnitude misses, the researcher's and my predecessor's alike:
  - H004 predicted 400–470 s by the researcher and 340–420 s by the Advisor, against 482.7 s observed;
  - H005 predicted 380–450 s by the Advisor, against 550.7 s observed;
  - the Advisor gave H005 P = 0.90 of passing against H003, and it failed.
- On NM-present rows those expectations were about right. Day 2 expectations should be stated on both populations.

### (e) Other chain decisions

All of the following re-verify from the comparison JSONs:
- E002 PROMOTE: 7/7 WIN; tail share 0.037.
- E003 PROMOTE: 4 WIN, W1 TIE, twins WIN; tail share 0.065; the W1/W1c DST contrast is as predicted.
- E004 REJECT: R1 and R2 LOSS; criterion 3 fails at EDDM, EGLL, EHAM and LTFM.
- E011 REJECT: S1 TIE against E005; clause 2 met.
- E010 ablation passes.

**Chain order.** The chain was run in batch: E001–E005 finished before any comparison was computed. This is acceptable, because every configuration was fixed in the reviewed proposals. Each reproduction was allocated only after its comparison existed.

## Novelty Relative to Existing Research

- **No new experiment is proposed.** The holdout access is the pre-registered `phase_close` comparison.
- **No Day 1 experiment separates the two H006 effects.** H008 removed `d_aobt3`, `d_eobt1`, `d_sched` and `flt_missing` together, so it confounds the NM-present correction with the NM-missing/`d_sched` behaviour.
- **The Day 2 lead is not redundant with H006** only if it is framed as what it is (C2): the LIRF block-at-schedule recording convention, reached through `d_sched` and gated by NM-missingness.

## Experimental Isolation

- **The holdout access.** It changes nothing: one pre-registered paired comparison, frozen bootstrap, frozen revert rule.
- **The E006 attribution.** Neither the frozen rule nor the H006/H008 design could isolate the two mechanisms. The decomposition above is post hoc and attribution-only. It supports the decision not to promote, and it cannot support a promotion.

## Validation Quality

- **Folds.** The frozen folds were used unchanged throughout, and the frozen hashes are intact. The seasonal fold was a required WIN for every promotion (E005 against E003: S1 WIN, S1c WIN).
- **The holdout check.** Its decision power against E001 is very low:
  - development-fold intervals for E005 − E001 run from −152.7 to −67.3 s;
  - a WIN is expected, and it validates only that nothing broke between the development months and December.
- **Month-to-month instability of the LIRF pattern.**
  - The tail rate among LIRF NM-missing departures ranges from 0.35 (Jul 2025) to 0.83 (Mar 2025).
  - July has both the most such rows (337) and the lowest tail rate. That is why S1 shows the largest LIRF bulk damage.
  - July 2026 has 276 such rows (target-free count), so this trade is least favourable in July.
- **What the y ≥ 3,600 s band selects.** At LIRF, which holds 48 % of the January–November tail rows, standing rule 1's tail band selects mostly block-at-schedule records. Standing rule 7 (Revision) makes the offsetting visible.

## Leakage Review

### Target Leakage

PASS

- **Day 1 models.** None used inadmissible information.
- **The block-at-schedule convention is not leakage.** SCHED_TIME and MVT_TIME are ranking columns (§6.2).
- **The holdout access.** It reads December truth once, through the frozen evaluator, and `holdout_check.py` persists only the decision quantities.

### Temporal Leakage

CONCERN

- **Wrong label.** The proposal labels the NM-missing tail mechanism P ("the absence of an NM match is known before off-block"). The within-group signal and the magnitude come from `d_sched`, which uses the row's takeoff, so the mechanism is **T**.
- **Consequences.** It is admissible, but:
  - it must be relabelled (C2);
  - it is excluded from the Days 5–7 causal-only variant.
- **Blocking?** No. No executed model violates §6.2.

### Competition Availability

PASS

- **Both ranking months contain the population.** Target-free counts:
  - January 2026: 107 LIRF NM-missing DEP rows (0.97 % of LIRF DEP), of which 83 % took off more than 1 h after schedule;
  - July 2026: 276 such rows (1.74 %), of which 94 % did;
  - every 2025 month: 81–96 %.
- **Unverifiable.** Whether their blanked block times follow the convention cannot be checked.
- **Holdout prediction files.**
  - The E005 and E001 H files match their manifests.
  - Each has 165,677 unique, finite rows.
  - Their ID sets equal the December DEP population (0 missing, 0 extra), checked from ID, month and phase columns only.

## Compute Review

### RAM

PASS

One H truth read plus a one-fold bootstrap. The SPLITS v2 review measured 0.53 GB for seven truth reads plus `promotion_check`.

### Runtime

PASS

Seconds: the silver hash, one truth read, and 2,000 resamples on one fold.

### Disk

PASS

One small JSON in `research/day-01/holdout/` and one task-ledger line.

## Weakest Assumption

**The assumption.** "The tail" is one physical phenomenon, i.e. long taxi-outs. Three things rest on it:
- the pre-registered tail mechanism of H004–H006 (holds after NM's off-block, reflected by the anchor);
- the reading of standing rule 1;
- the proposed Day 2 lead.

**Why it fails.** At LIRF, 83 % of tail rows are block-at-schedule records. Across all airports, tail rows of that kind carry 26.9 % of the constant-mean SSE.

**What it affects.**
- E005's selection survives this: 75 % of its margin over E003 is bulk, with bulk gains at every airport.
- The interpretation of H006 and the framing of Day 2 do not survive it.

## Missing Control or Ablation

None blocks the access.

- **Missing on Day 1: the decomposition by NM status × LIRF.** It is computed above and becomes standing rule 7.
- **Missing code (C7).** The code that produced `research/comparisons/E005_vs_E004_clip_attribution.json` is not committed. I reproduced the values, but the derivation must be in the repository for the hand-off.
- **Missing ablation (named, not designed).** No Day 1 ablation separates H006's NM-present correction from its NM-missing/`d_sched` behaviour. Any Day 2 proposal that claims either effect needs one.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **The Day 1 decisions stand as recorded.**
   - E005 (H004) is the phase-closing champion.
   - E002 and E003: PROMOTE, superseded.
   - E004 (H005) and E011 (H007): REJECT.
   - E006 (H006): INCONCLUSIVE, with **no retroactive promotion**.
   - E010 (H008): ablation.
2. **Exactly one protected-holdout access**, after the acknowledgement below is committed:

   ```
   uv run python scripts/holdout_check.py E005 E001 --reason "Day 1 phase close (X-D01-S01-0004): phase-closing champion E005 vs phase-opening champion E001"
   ```

   - The proposal omits `--reason`, which the script requires. Without it, argparse exits before any access is logged.
   - Apply `phase_close.revert_on` mechanically:
     - LOSS: revert to E001;
     - WIN or TIE: E005 stands.
3. **Not authorized:**
   - any second or different holdout comparison (including anything involving E006);
   - a re-run after an exception;
   - using the printed H RMSEs for anything except recording the outcome;
   - any change to frozen files, reviews or completed records.

Required acknowledgement path: `research/day-01/acks/PHASE_CLOSE_D01_ack_v1.md`

**Hash references.** The acknowledgement must reference the proposal hash (`811b313c…`) and this review's hash.

**Corrections.** It must append the following corrections. The proposal and completed records are not edited.
- **C1. Tail-share netting.** The 0.991 tail share of E006 against E005 nets three pieces: a bulk gain on NM-present rows (−31 to −40 s on every development fold), a bulk loss on LIRF NM-missing rows, and the tail gain. "Worse than ridge in the bulk on S1/R1" is true only because of LIRF NM-missing rows (pooled LIRF bulk +210.9 s; the other nine airports −14.5 to −57.8 s).
- **C2. The NM-missing tail mechanism is label T,** through `d_sched`, and is predominantly LIRF's block-at-schedule recording convention (figures in Scientific Validity (c)). The "P-labelled" claim in the proposal is withdrawn.
- **C3. NM-missing rows carry the metric.** They are 0.77–2.06 % of rows but carry 0.14–0.66 of the SSE of E004, E005 and E006. They explain the magnitude misses. E005's RMSE on NM-present rows is 289, 288, 271, 395 and 307 s (R1, R2, R3, S1, W1).
- **C4. Three day-scale LIRF records, not two:** 87,002 s (anchor-exact), 87,186 s (no NM data) and 131,167 s (no NM data).
- **C5. Concurrency.** E006 overlapped E007, E008 and E009 as well as several comparison runs, not only E009. The reproductions are exact and every run was within class, so this has no numerical effect.
- **C6. STATE.md is stale.** It was last updated at chain step 4, and commit `917a03f` skipped §13 step 3. Stale fields:
  - last exchange;
  - accepted findings;
  - rejected hypotheses;
  - next action;
  - B1–B4 and rule 6 missing;
  - H006 INCONCLUSIVE missing.
- **C7. Clip-attribution code.** The producing code of the clip-attribution JSON is uncommitted.

**Standing rules.** The acknowledgement must adopt standing rules 7 and 8 (Revision).

**Conditions on the phase-closing commit:**
- `research/STATE.md` is current (C6);
- DAY_SUMMARY §3 and §5 are corrected per C1–C4, and the holdout outcome is recorded;
- the C7 code is committed;
- the exchange is mirrored (`response.md`, `checksums.sha256`).

## Revision

None required for this version.

**Standing review rules added from this exchange** (they apply from the next proposal onward):

7. **Subgroup disclosure.**
   - Every comparison used for a promotion or a criterion-4 check reports, per development fold and twin, the SSE-change shares and bulk dRMSE by NM status (`AOBT_3` present or missing) × LIRF against the other nine airports.
   - Where the pooled bulk dRMSE and a subgroup's bulk dRMSE differ in sign, the tail share is not read on its own.
   - This is attribution only; fold outcomes are unchanged.
8. **Recording-convention disclosure.**
   - A hypothesis whose margin concentrates on LIRF tail rows or on NM-missing rows must state whether its mechanism is taxi duration or the block-at-schedule recording convention.
   - It labels `d_sched`-derived inputs T.
   - It pre-registers its expected effect separately on the tail and on the bulk of that subpopulation, and states its S1 (July) expectation in view of the low July tail rate.
   - The convention is admissible under §6.2. It is not evidence about taxi-out dynamics, and it is outside the causal-only variant.

## Advisor Prediction

Probability of improvement:

| Holdout outcome for E005 against E001 | P |
|---|---|
| WIN | 0.97 |
| TIE | 0.03 |
| LOSS (revert) | < 0.01 |

The E005 and E001 H prediction files are verified complete, so the access will not fail after it is logged.

Expected magnitude: dRMSE (E005 − E001) on H between −60 and −125 s. For comparison, the development folds gave −76 to −118 s (mean −98.1, q95 −90.8).

Primary expected failure mode: interpretive, not operational.
- A WIN on H will be read as validating E005. It validates only E005 against a constant.
- The champion's standing rests on development-fold comparisons in which 1–2 % of rows (NM-missing, mostly LIRF block-at-schedule records) carry 46–66 % of every model's SSE on four of five folds.
- P = 0.6 that the first Day 2 hypothesis touching NM-missing rows is flagged under standing rule 7 or 8.
