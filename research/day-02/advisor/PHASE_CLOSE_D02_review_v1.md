---
schema: advisor-review-v1
hypothesis_id: PHASE_CLOSE_D02
proposal_version: 1
proposal_sha256: 958db1e83aff17fcf03a74fa228257d2723ab3468cf2fe31c0070afd67d85a3b
exchange_id: X-D02-S01-0006
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.90
created_utc: 2026-09-28T22:32:14Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**
- **The Day 2 decisions stand.** E005 remains champion, H009 v3 (E012 and E015) and H013 v2 (E017) are INCONCLUSIVE, and there is no retroactive promotion.
- **Holdout ruling: no Day 2 access.** The access is closed unused (0 of 1). It does not carry over, and no substitute comparison is admissible (ruling H).
- **Before `DAY_SUMMARY.md` is finalised,** the acknowledgement must append ten record corrections (D2-C1 to D2-C10) and adopt standing rules 9–11.
  - None of them changes a decision.
  - They change what Day 2 is recorded as having shown. Four do so materially (D2-C1 to D2-C4).

**Attack on the champion.** I tried to show that E005 is wrong, in two directions.
1. **A Day 2 candidate was promotable after all.** It was not. Both blocking facts re-verify from the ledger and the committed comparison files, and the frozen rules leave no discretion:
   - **H009 v3, criterion 6:** \|E015 − E012\| is 1.727 s on R3 and 3.503 s on S1, against a 1.0 s tolerance.
   - **H013 v2, criterion 8:** `NM_missing_LIRF.delta_rmse_bulk` against E005 is +7,104.4 s on S1, against a +6,500 s bound. No reproduction exists either.
2. **E005 is the wrong model to hold.** Partly true.
   - **Against E005.** On NM-present rows (98–99 % of each fold), every Day 2 Tier 1 fit beats it by 51.5–59.6 s on every development fold. E005 is champion by rule, not the most accurate model on most rows.
   - **For E005, and new.** On S1 (the July analogue), the candidates' loss on 218 LIRF NM-missing bulk rows is **1.38× (E012) and 1.63× (E017) their entire gain on 186,775 NM-present rows**. On S1c it is 1.16× and 1.13×.
   - **What carries S1.** Their required S1 WIN rests on 119 convention tail rows. Ten rows carry 0.69 (E012) and 0.75 (E017) of the S1 change.
   - **Consequence.** "E005 will score worse on the ranking months" (proposal, "Case against" 1) holds only if the LIRF recording convention recurs in July 2026, which target-free data cannot show. Criterion 8's guard is not a technicality.

**Where the record is wrong** (figures in Scientific Validity):

| Correction | Finding |
|---|---|
| D2-C1 | The margin is not "~100 s on every fold": R2 is −60.9 s (E012) and −65.2 s (E017). LIRF NM-missing rows (≤ 0.18 % of rows) carry 0.17–0.73 of each fold's SSE change |
| D2-C2 | On all rows, the six static keys are indistinguishable from zero in both training procedures: E012 − E006 −1.72 s (q95 +9.39); E017 − E018 −2.13 s (q95 +13.09). The "30 s vs 7 s" pair mixes populations and key sets, and what absorbs the static signal is the whole delta set, not "the anchor" |
| D2-C3 | "Static keys dilute the convention" is reversed on S1 in both procedures. H013's criterion 8 failure is carried as much by the static keys (+717 s) as by the procedure (+714 s) |
| D2-C4 | The seed variance is not confined to LIRF NM-missing rows. Excluding them, E015 − E012 is +1.33 s on S1 and **−1.94 s on W1** (unreported). Both exceed 1.0 s |
| D2-C5 | Deterministic training costs about 3 s on all rows. Its determinism on real data is untested |
| D2-C6 | `research/STATE.md` is stale again (a repeat of Day 1 C6) |
| D2-C7 | INC-0003 is live: the researcher process still carries `--effort medium`, and no Day 2 analysis cites the incident |

**The criterion 8 bound is not re-derived** (ruling B).
- It did what the H013 v1 ruling built it for: it caught a systematic worsening of the July trade.
- On identical rows, RMSE differences add exactly. That puts the S1 statistic at +5,782 (E006), +6,387 (E018), +6,390 (E012), +6,456 (E015) and +7,104 s (E017).

**Verified here.** All checks were read-only: no December target was read, `holdout_check.py` was not run, no model was fitted or scored, and I wrote only this file.
- **Hashes.**
  - The proposal matches the envelope (`958db1e8…`).
  - The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json`. `frozen.json` (`32c41c0f…`) equals `frozen_sha256` in all 18 ledger records.
  - `.claude/agents/advisor.md` is `30fff5dd…`, matching `config/agents.yaml`. `uv.lock` is `39df945c…`.
- **Ledger.** The proposal, review and ack hashes of all 18 records match their files.
- **Mirrors.** The checksums of X-D02-S01-0001 to -0005 verify (8, 8, 4, 6 and 6 files), as do those of X-D01-S01-0004 (4).
- **Predictions.** All eight prediction files of E005, E006, E010 and E012–E018 match their manifests, and silver matches the frozen pin.
- **Code.**
  - Nothing changed since `5ba9230` in `compare.py`, `mechanism_check.py`, `attribution.py`, `features.py`, `models/`, `worker.py`, `run_experiment.py`, `reproduce_check.py`, `gate.py` or `uv.lock`.
  - The code preconditions of H013 v2 and H014 v2 therefore held through the last comparison.
- **Dirty states.** E013, E014 and E015 were allocated with uncommitted files, and E015 also ran with them. The diffs contain output and record files only.
- **Holdout.** The task ledger has one `holdout_access` event (`day-01`). There is no `research/day-02/holdout/`. The worker predicts H without scoring it.
- **Tree, tests and lint.** `pytest` passes 101/101 (caches disabled). `ruff` is clean, and the tree is clean at `5d17710`.
- **Secrets.**
  - None of the credential values listed in DATA_POLICY §1 appears in the 372 tracked files.
  - The OpenSky username, which §1 does not list as a credential, occurs only inside the public repository owner's name in the brief.
- **INC-0003.** The researcher process has been running for about 4 h 10 min, all of D02-S01, and was launched with `--effort medium`.

## Scientific Validity

### (a) The Day 2 decisions re-verify

| Decision | Check (committed JSONs and ledger) | Result |
|---|---|---|
| H009 v3 not falsified | Clause 1: E012 − E005 −106.58 s (q95 −84.41), 7/7 WIN, criterion 3 true.<br>2(a): −7.155 s (q95 −6.254), 4 counted WINs (the W1c LOSS voids W1).<br>2(b): bulk −8.1 to −14.5 s on all five folds.<br>3: E012 − E013 on LIRF NM-missing −314 to −2,493 s on all five.<br>4: E012 − E014 on NM-present −51.30 s (q95 −47.49), 7/7 WIN | Confirmed |
| H009 criterion 8 resolved | Clause 3 not met. Largest development-fold bulk statistic: S1 +6,390.3 ≤ +6,500. B3: S1c −125.5 | Confirmed |
| H009 criterion 6 fails | `repro_E015_of_E012.json`: R1 −0.351, R2 +0.906, **R3 +1.727**, **S1 +3.503**, W1 −0.073. `criteria_hold` true, `passes` false | Confirmed. INCONCLUSIVE is the Day 1 category (H006) |
| H013 v2 not falsified | Clause 1: E017 − E005 −103.90 s (q95 −80.35), 7/7 WIN.<br>2(a): E017 − E018 −7.273 s (q95 −6.491), 4 counted WINs.<br>2(b): −9.0 to −16.4 s on all five.<br>3: all five folds < 0; R2 inadmissible (453.45 ≥ 157.101), so 1 failing fold.<br>4: −52.05 s (q95 −48.24); all five folds admissible (largest \|Δ\| 2.11 s against 16.585 s) | Confirmed |
| Objection T | S1c 1.675 < 21.153; W1c 2.385 < 47.966 | Does not stand. Confirmed |
| H013 criterion 8 | S1 +7,104.4 > +6,500 | **Not resolved.** Confirmed. The reproduction was correctly not run |

**Advisor record (D2-C10).**
- **Criterion 6 was foreseeable.** X-D02-S01-0001 to -0003 sized the seed risk only against the mechanism contrasts ("small next to ≥ 5 s"). They did not size it against the frozen 1.0 s whole-fold tolerance on folds that carry day-scale records. The Advisor did not flag this before E012 ran.
- **The X-D02-S01-0005 fold-scale synthetic check is not in the repository.** The committed 260,000-row test is the reproducible evidence.

### (b) The margin over E005 (D2-C1)

E012 / E017 against E005, all from `E0xx_vs_E005.json`. Shares are of each fold's SSE change.

| Fold | All rows (s) | NM-present rows (s) | LIRF NM-missing share | LIRF NM-missing bulk loss ÷ NM-present gain |
|---|---|---|---|---|
| R1 | −115.1 / −113.2 | −51.5 / −53.6 | 0.71 / 0.69 | 0.64 / 0.71 |
| R2 | **−60.9 / −65.2** | −54.0 / −53.5 | 0.17 / 0.23 | 0.10 / 0.07 |
| R3 | −119.7 / −121.0 | −54.6 / −54.6 | 0.69 / 0.70 | 0.03 / 0.03 |
| S1 | −131.9 / −121.1 | −58.2 / −59.6 | 0.73 / 0.70 | **1.38 / 1.63** |
| W1 | −105.3 / **−99.1** | −58.8 / −59.6 | 0.64 / 0.63 | 0.03 / 0.03 |
| S1c | −125.5 / −125.9 | −52.8 / −54.5 | 0.75 / 0.74 | **1.16 / 1.13** |
| W1c | **−65.7 / −74.0** | −24.1 / −21.7 | 0.82 / 0.85 | 0.03 / 0.03 |

- **The robust margin is 52–60 s on NM-present rows,** on every development fold, in both procedures. The rest of the ~104–107 s means runs through 52–337 LIRF NM-missing rows.
- **On S1 and S1c, the convention decides accuracy against E005, not only promotion.**
  - The bulk loss on the subgroup outweighs the whole NM-present gain.
  - The WIN is carried by the tail gain on 119 rows, most of it by a few day-scale records.
  - DAY_SUMMARY §6.3 ("decides promotion, not accuracy") is wrong on the July analogue.

### (c) Seed variance (D2-C4)

E015 − E012, RMSE difference (s) by population. Bold marks \|Δ\| > 1.0 on a development fold. The twins are not criterion 6 folds.

| Population | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| All rows | −0.35 | +0.91 | **+1.73** | **+3.50** | −0.07 | −4.63 | −0.96 |
| Excluding LIRF NM-missing | +0.04 | +0.33 | +0.23 | **+1.33** | **−1.94** | −0.59 | −1.31 |
| NM-present, outside LIRF | +0.13 | +0.53 | +0.21 | +0.91 | −0.52 | +0.23 | −1.40 |
| LIRF NM-missing (rows) | −16.9 (168) | +56.7 (115) | +124.4 (52) | +82.2 (337) | +93.4 (58) | −133.5 (337) | +0.4 (58) |

- **The records report only some cells.** The E015 analysis, the journal, STATE and DAY_SUMMARY §5 report R3 and S1 only; the proposal reports R3 only. None flags that S1's +1.33 s still exceeds the tolerance.
- **W1 nets opposing shifts.** Its all-rows −0.07 s combines +93 s of subgroup RMSE on 58 LIRF rows with −1.94 s elsewhere.
- **Where W1's shift lives.** Outside the LIRF NM-missing subgroup, NM-present LIRF rows and NM-missing rows at the other airports carry 0.80 of the SSE change (−1.29 × 10⁸ of −1.61 × 10⁸). `H011_ack_v2.md` had flagged W1's NM-missing rows at other airports as an exposure.
- **The frozen bootstrap turns seed-only differences into outcomes.**
  - On `NM_present_excl_LIRF`, E015 − E012 gives R2 LOSS (+0.53), S1 LOSS (+0.91), W1 WIN (−0.52) and W1c WIN (−1.40).
  - On `excl_LIRF_NM_missing`, S1 is LOSS and W1 is WIN.
- **Consequences.**
  - "The only place where Tier 1 models are seed-unstable" (DAY_SUMMARY §6.3) is withdrawn. The instability is a property of long-tail records in general.
  - The premise of DAY_SUMMARY §8.1, that a treatment of the LIRF NM-missing subgroup "could resolve … the criterion 6 exposure of any Tier 1 candidate", does not hold for a bagged model.
  - **M1 stands.** −7.2 s on `NM_present_excl_LIRF` is about eight times the largest development-fold seed shift on that population (0.91 s).

### (d) Static keys on all rows, and the S1 convention trade (D2-C2, D2-C3)

**One contrast, three populations** (mean dRMSE, s):

| Contrast | NM-present, outside LIRF | NM-present | All rows |
|---|---|---|---|
| E016 − E010 (4 keys, delta set absent) | not computed | −29.57 (q95 −27.98), 5/5 WIN | −28.01 (q95 −19.01), S1 TIE |
| E012 − E006 (6 keys, bagged) | −7.16 (q95 −6.25) | −9.15 (q95 −4.75); S1 TIE, criterion 2 false | **−1.72 (q95 +9.39)**; criteria 1 and 2 false |
| E017 − E018 (6 keys, deterministic) | −7.27 (q95 −6.49) | −8.67 (q95 −2.42); S1 TIE, criterion 2 false | **−2.13 (q95 +13.09)**; criteria 1 and 2 false |

- **The absorption figure.**
  - On the matched NM-present population the delta set absorbs 0.69–0.71 of the static signal: 1 − 9.15/29.57 and 1 − 8.67/29.57.
  - The delta set is what E010 removes: `d_aobt3`, `d_eobt1`, `d_sched` and `flt_missing` (`features.DELTAS`). The anchor's own share is not measured, and the key sets differ (four against six).
- **On all rows, the competition metric, FS1 adds nothing detectable over FS0** in either procedure. The M1 gain is offset on LIRF NM-missing rows.

**S1 criterion 8 statistic against E005** (LIRF NM-missing bulk dRMSE, s):

| | Bagged | Deterministic | Procedure effect |
|---|---|---|---|
| FS0 | E006 +5,782.0 | E018 +6,387.0 | +605.0 |
| FS1 | E012 +6,390.3 (E015 +6,455.9) | E017 **+7,104.4** | +714.1 |
| Static-key effect | +608.3 | +717.4 | |

- **How the figures were obtained.** RMSE differences on identical rows add exactly. E018 − E006 computed directly equals the implied value on all five folds.
- **Cross-check.** The E006 − E005 values reproduce the Day 1 table exactly: +5,514, +3,591, +1,985, +5,782 and +2,761.
- **Only on S1 do both changes worsen the trade.**
  - On R1–R3 and W1, the procedure effect on FS0 is −70 to −128 s.
  - S1's validation month has the lowest convention rate (0.35), while its training months have higher ones, so a sharper mixture loses there.
  - That is also SUBMIT_JUL's situation. The direction is structural, not noise.
- **"Static keys dilute the convention" is fold- and procedure-dependent.**
  - It holds on R2 and W1 in both procedures, and on R1 and R3 under bagging only.
  - It is **reversed on S1 in both procedures** (+608, +717 s) and on R3 under the deterministic procedure (+146 s).
- **H013's failure has two causes, not one.** E017's analysis and the journal attribute it to the procedure ("without bagging, … more extreme"), which is half the story. Either change alone lands at +6,387 to +6,390 s; together they reach +7,104 s.

### (e) Deterministic training (D2-C5)

- **NM-present rows.** E017 − E012 = −0.75 s (q95 −0.29).
- **All rows.**
  - E017 − E012: +2.67 s (q95 +6.95), with **S1 LOSS (+10.85)** and **W1 LOSS (+6.19)**.
  - E018 − E006: +3.08 s (q95 +7.29), with W1c LOSS.
  - The cost sits on LIRF NM-missing rows, which carry 0.89–1.60 of each development fold's E017 − E012 change.
- **Determinism on real data is untested.** No reproduction under this configuration ran. The evidence is synthetic.
- **What follows.** "Essentially free" and "makes criterion 6 a determinism check" must be qualified accordingly. Choosing the procedure for Days 3–4 remains the researcher's call.

## Novelty Relative to Existing Research

- **This exchange proposes no experiment.**
- **Day 2's contribution:**
  - static structure on NM-present rows: about 30 s without the delta set and 7–9 s with it;
  - M2 and M3 replicated across two training procedures;
  - a characterised convention subgroup, with a measured July-specific trade.
- **Coverage note.** Two brief §11 Day 2 items were not tested. This is not a gap in the decisions.
  - Calendar-month and cyclic encodings, excluded by standing rule 4.
  - Explicit airport × time interactions, left to the trees.

## Experimental Isolation

- **The phase close changes nothing and runs nothing.**
- **H013's criterion 8 failure is now isolated by attribution.** The matched references E006 and E018, with exact additivity (Scientific Validity (d)), separate the procedure effect from the static-key effect. This is attribution only and changes no outcome.
- **The clause 3 and 4 reuse assumption** ("Case against" 4) is moot for Day 2, because H013 is not promotable. For Day 3 it becomes a requirement (Missing Control 1).

## Validation Quality

**Folds and frozen artifacts.**
- The frozen folds were used unchanged in all seven Day 2 runs, including S1 and both twins.
- The frozen hashes are intact.
- H was predicted only.

### Ruling H: the Day 2 holdout access

1. **No access.**
   - The frozen `phase_close` rule compares the phase-closing champion with the phase-opening champion. Its only decision use is to revert the phase's promotions on a LOSS.
   - Day 2 has no promotion. E005 against E005 has dRMSE ≡ 0 on every resample, so it is a TIE by construction, with nothing to revert.
   - **The frozen code would refuse it anyway.** `evaluate.holdout_compare` takes the phase from NEW's gate record. E005's is `day-01`, whose single access is spent, and the refusal happens before anything is logged or read.
2. **Record it as "no promotion, no holdout access (Day 2: 0 of 1, closed unused)".** Do not record a TIE: no comparison was made.
3. **No carry-over.** `max_access_per_phase: 1` is per phase, so Day 3 has one access, not two.
4. **No substitute comparison.**
   - Any other pair (for example E012, E015, E017 or E018 against E005) is not the frozen comparison.
   - It would use H to evaluate non-champions and to inform the Day 3 base choice. That is holdout-guided selection.
   - The H009 v3 and H013 v2 authorizations already exclude "scoring H outside the frozen phase-close check".
5. **A latent loophole, closed by standing rule 9.**
   - The frozen code attributes an access to NEW's allocation day. E012–E018 are `day-02` allocations, and `day-02` has 0 accesses.
   - A command such as `holdout_check.py E017 E005 …` would therefore be **accepted at any later time** and logged as a Day 2 access.
   - The evaluator is frozen, so the governance record has to close it.

### Ruling B: the criterion 8 bound for Day 3 and later ("Case against" 2)

- **No re-derivation and no retroactive change.** H013 v2 stays INCONCLUSIVE.
- **The bound measured the model, not itself.**
  - The H013 v1 ruling set it to catch "a systematic worsening of the trade by the configuration change" (Alternative Explanation 1). E017 shows exactly that worsening.
  - (d) shows that FS1's keys worsen the S1 trade by the same amount. The 604 s excess is about the size of either change alone.
- **Default for Day 3 and later.**
  - Any candidate whose LIRF NM-missing predictions come from a learned convention mixture inherits the LIRF bulk-trade objection, with H009 v3's resolution rule unchanged.
  - That covers every Tier 1 model that sees `d_sched` or the hour-resolution proxy. Per H011 v2, it may also cover a model with static keys and neither.
- **An alternative resolution is admissible only if all three hold:**
  - it is pre-registered in the candidate's proposal and reviewed before the run;
  - its rationale rests on the forward risk in the ranking months (for example, 276 LIRF NM-missing DEP rows in July 2026, target-free, and 2025 monthly convention rates of 0.35–0.83), not on the outcomes of E006–E018;
  - it is not a new threshold on the same statistic. Any such threshold would be chosen knowing the family's values (+5,782 to +7,104 s on S1), so standing rule 10 applies.
- **Disclosure.** A Day 3 proposal that relies on this statistic states its measured S1 sensitivity:
  - seed: +66 s;
  - training procedure: +605 s (FS0) and +714 s (FS1);
  - static keys: +608 s (bagged) and +717 s (deterministic).

### Ruling R: the comparison base (DAY_SUMMARY §8.3; "Case against" 1)

- **A comparison base is a matched reference, not a champion.** Promotion is judged against E005 under the frozen rule.
- **Matched means the identical training procedure, code and environment,** so the candidate's procedure fixes the base:
  - E012 for bagged FS1 candidates;
  - E017 for deterministic FS1 candidates;
  - E006 or E018 for FS0-based candidates.

  The reuse conditions must hold: `uv.lock`, `gbm.py`, the feature-function bodies and silver unchanged.
- **The choice may not be justified by E017 being the strongest model.**
  - On all rows it is not distinguishable from E018 (−2.13 s, q95 +13.09).
  - It is worse than E012 on S1 and W1 (both LOSS).
  - Its determinism on real data is untested.
- **Criteria 1–3 against E005 cannot test a Day 3 mechanism.** Every Tier 1 candidate clears them by about 100 s. Criterion 4 against the matched base therefore carries every Day 3 mechanism claim, and its clause must be decisive against the measured noise on its population (Missing Control 4).

**Bootstrap and seed noise.** The frozen cluster bootstrap does not model training randomness. For bagged models it labels seed-only differences of 0.5–1.4 s as WIN or LOSS ((c)). Fold outcomes on margins of that size are not mechanism evidence.

## Leakage Review

### Target Leakage

PASS

- No Day 2 model uses target statistics. The rare-level collapse, vocabularies and bins come from training rows only.
- Validation truth is read only through the frozen evaluator, and `truth_frame` refuses H and the final folds.
- H was predicted only. No Day 2 run, comparison or this review read a December target.

### Temporal Leakage

CONCERN

These are label notes carried from Day 2; they are not blocking.
- **T:** `hour_utc`, `weekday`, the `d_*` deltas and the hour-resolution schedule-delay proxy.
- **F:** `ades` on diversions (~0.03 % of rows).
- **P by assumption:** stand.
- **Convention:** M3 is T and outside the causal-only variant (standing rule 8).
- **E005:** FS0 uses none of the Day 2 additions, and nothing found on Day 2 affects its admissibility.

### Competition Availability

CONCERN

Not blocking. It bears on how the candidates are read, not on E005.
- Every Day 2 input is present for ranking DEP rows.
- **The July risk.** The candidates' July advantage over E005 depends on the 2026 targets of the 276 July LIRF NM-missing DEP rows (107 in January) following the 2025 convention. The blanked targets cannot show this.
- On S1, the candidates' bulk loss on these rows already exceeds their whole NM-present gain ((b)).

## Compute Review

### RAM

PASS

No experiment. The checks were read-only JSON and hash reads plus the test suite.

### Runtime

PASS

The test suite took about 30 s.

### Disk

PASS

One review file.

## Weakest Assumption

**That the LIRF NM-missing recording convention behaves in the 2026 ranking months as it did in 2025.**
- **Both sides of the Day 2 decision rest on it:**
  - the candidates' claimed superiority on the metric (their S1 WIN rests on 119 convention tail rows, 10 of which carry 0.69–0.75 of the change);
  - E005's standing as the conservative model.
- **Day 2's decisive statistics rest on it too:**
  - the S1 criterion 8 statistic, computed on 218 rows;
  - the criterion 6 shifts on R3 and S1, whose largest parts come from 52 and 337 LIRF rows.
- **It cannot be checked on target-free data.** Holding E005 is the one decision that does not depend on it.

## Missing Control or Ablation

None blocks the phase close. Four are named for Day 3; they are named, not designed.
1. **A matched procedure for every mechanism reference.** A deterministic candidate needs deterministic ablations. H013's carry-over of bagged ablations (reading 1) must not be repeated for a claim that decides promotion.
2. **A real-data determinism check before "determinism check" is used for criterion 6.** That is a reproduction under the deterministic configuration, compared by prediction-file hashes (reading 2 of `H013_review_v2.md`).
3. **Any explicit treatment of the LIRF NM-missing subgroup is its own hypothesis.**
   - It needs an ablation that isolates its effect on that subgroup, a rule 8 pre-registration for S1 at July's rate, and fold-local fitting.
   - It cannot be credited with resolving criterion 6 for a bagged model (D2-C4).
4. **The noise scale on each clause population.** If a clause's expected effect is below about three times the measured seed or procedure shift on its population (E015 − E012, E017 − E012), the proposal must say so and explain why the outcome is decisive.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **The Day 2 decisions stand as recorded.**
   - E005 (H004) is the phase-closing champion, by rule.
   - H009 v3: INCONCLUSIVE (E012 primary, E015 reproduction; criterion 6).
   - H013 v2: INCONCLUSIVE (E017; criterion 8; not reproduced).
   - E013 (H010), E014 (H012), E016 (H011 v2) and E018 (H014 v2) keep their recorded ablation and reference outcomes.
   - No retroactive promotion and no re-adjudication (standing rule 10).
2. **No protected-holdout access for Day 2.**
   - Record "Day 2: 0 of 1, closed unused".
   - `holdout_check.py` is not run in this phase.
   - No Day-2-allocated experiment may be NEW in any phase (standing rule 9).
3. **Not authorized:**
   - any allocation, run, reproduction (including of H013 v2) or re-run;
   - any scoring of H;
   - any change to frozen files, reviews or completed records.

Required acknowledgement path: `research/day-02/acks/PHASE_CLOSE_D02_ack_v1.md`

**Contents of the acknowledgement:**
- the proposal hash (`958db1e8…`) and this review's hash;
- corrections D2-C1 to D2-C10, appended (the proposal and completed records are not edited);
- standing rules 9–11, adopted;
- rulings H, B and R, recorded.

**Corrections.** Figures are in Scientific Validity.
- **D2-C1. The margin over E005** (proposal "Case against" 1; DAY_SUMMARY §5 and §6.3).
  - "~100 s on every fold" is false: R2 is −60.9 / −65.2 s (E012 / E017), W1c −65.7 / −74.0 s, and E017's W1 −99.1 s.
  - LIRF NM-missing rows carry 0.17–0.73 of each fold's SSE change.
  - The robust margin is 51.5–59.6 s on NM-present rows.
  - On S1 and S1c, the subgroup's bulk loss exceeds the whole NM-present gain (1.13–1.63×), so the convention decides accuracy there too.
  - The ranking-month claim is conditional on the convention recurring.
- **D2-C2. The static-structure answer** (DAY_SUMMARY §1 and §6.1; E016 analysis; journal).
  - Matched NM-present population: −29.6 s (E016 − E010) against −9.1 s (E012 − E006) and −8.7 s (E017 − E018).
  - **All rows:** −1.72 s (q95 +9.39) and −2.13 s (q95 +13.09). Criterion 1 fails in both, so FS1 is not distinguishable from FS0 on the metric.
  - What absorbs about 70 % is the delta set (`d_aobt3`, `d_eobt1`, `d_sched`, `flt_missing`), not the anchor alone.
  - W1c is LOSS for M1 in both procedures.
  - The "−52.1 s deterministic" M2 figure compares a deterministic candidate with the bagged E014. It is a carry-over figure, not a deterministic M2 estimate.
- **D2-C3. Convention dilution** (DAY_SUMMARY §6.3; E012 and E017 analyses; journal).
  - It is reversed on S1 in both procedures (+608, +717 s), and on R3 under the deterministic procedure (+146 s).
  - S1 statistic: E006 +5,782, E018 +6,387, E012 +6,390, E015 +6,456, E017 +7,104 s.
  - H013's failure comes from the procedure and the static keys together, not from the procedure alone.
- **D2-C4. Seed variance** (E015 analysis; journal; STATE; DAY_SUMMARY §5, §6.3 and §8.1; proposal "Case against" 3).
  - Excluding LIRF NM-missing rows, the shift is +1.33 s on S1 and −1.94 s on W1, both above 1.0 s. Only NM-present rows outside LIRF are within 1.0 s on every development fold.
  - "The only place where Tier 1 models are seed-unstable" is withdrawn.
  - A treatment of the subgroup would not resolve a bagged model's criterion 6 exposure.
  - The bootstrap labels seed-only differences as WIN or LOSS.
- **D2-C5. Deterministic training** (DAY_SUMMARY §6.2).
  - It is free on NM-present rows only: +2.67 s and +3.08 s on all rows, with S1 and W1 LOSS for E017 − E012.
  - Determinism on real data is untested. It is a premise until a reproduction shows identical prediction files.
- **D2-C6. STATE.md is stale** (brief §13 step 3; repeats Day 1 C6).
  - The header is 21:49:50Z. It was not updated at the E017 checkpoint (`0b1e119`) or the E018 checkpoint (`3f9dd7a`).
  - It still names "`gate.py allocate H013 v2` → run" as the next action.
  - It lacks E017, E018, H013 INCONCLUSIVE and the holdout closure.
  - The E017 checkpoint also omitted its journal entry, which was added at `3f9dd7a`.
- **D2-C7. INC-0003 scope.**
  - The researcher process that produced H009 v3–H014 v2, E012–E018 and this proposal still carries `--effort medium`.
  - No Day 2 analysis cites the incident, although `H009_review_v3.md` asked for it.
  - The DAY_SUMMARY must state the scope. The incident remains open for the owner.
- **D2-C8. Missed expectations to add to DAY_SUMMARY §7.**
  - H009 v3: development mean 355–372 → 376.15; clause 1 magnitude −110 to −130 → −106.58; rule 8 tail share on R2 0.25 (band 0.3–1.1).
  - H013 v2: rule 8 bulk band → S1 +7,104.4; tail band → R2 0.28 and S1 1.17.
  - H011 v2: magnitude −8 to −30 → −30.03.
  - In the §4 table, E015's development mean is 377.29, not "—".
- **D2-C9. Allocation from a dirty tree.**
  - E013, E014 and E015 were allocated with uncommitted files. Only output and record files were involved (verified).
  - Allocation should follow the checkpoint commit. There is no numerical effect.
- **D2-C10. Advisor record.**
  - The criterion 6 exposure of a bagged model on day-scale folds was not sized before E012.
  - The X-D02-S01-0005 fold-scale synthetic check is not in the repository.

**Conditions on the phase-closing commit:**
- The acknowledgement above is committed.
- `research/STATE.md` is current, with a measured header time. It records:
  - the champion, E005 by rule, with its NM-present deficit;
  - H009 v3 and H013 v2 INCONCLUSIVE, and the E013, E014, E016 and E018 outcomes;
  - the Day 2 holdout closed unused;
  - INC-0003 open;
  - standing rules 1–11 and B1–B4, and rulings H, B and R;
  - the next action.
- DAY_SUMMARY is corrected and marked final:
  - §1, §5, §6.1–§6.3, §7, §8.1 and §8.3, per D2-C1 to D2-C5, D2-C8 and rulings B and R;
  - it records "no promotion, no holdout access".
- A Day 2 phase-close journal entry exists.
- The exchange is mirrored: `envelope.yaml`, `response.md` and `checksums.sha256`.
- A session-registry end event exists for D02-S01, as for D01-S01.

## Revision

None required for this version.

**Standing review rules added from this exchange.** They apply from the next proposal onward.

9. **Protected-holdout access.**
   - An access is authorized only by a phase-close review that names the exact command.
   - NEW must be an experiment allocated in the phase being closed, because `holdout_compare` attributes the access to NEW's gate `day`.
   - A phase that closes without a promotion closes its access unused. That access does not carry over, and no later access may be attributed to that phase.
   - For Day 2: no `holdout_check.py` invocation with E012–E018 as NEW is authorized, in any phase.
10. **No re-adjudication of recorded outcomes.**
    - A proposal is not a new test, and will be rejected, if it:
      - re-submits a completed configuration unchanged as a promotion candidate (for a bagged model, with any seed); or
      - changes only a decision threshold, population or counting rule after the relevant outcome is recorded.
    - This covers the configurations of E006, E012/E015, E017 and E018, and any criterion 8 threshold on `NM_missing_LIRF.delta_rmse_bulk`.
    - A new candidate that builds on these configurations is not affected.
11. **Headline figures.**
    - In DAY_SUMMARY, STATE and the journal, a population-restricted effect is reported next to the all-rows figure of the same contrast.
    - Comparisons between contrasts use one population.
    - A statement that localises an effect to a subgroup reports every development fold, not only the failing ones.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| The Day 2 decisions are correct under the frozen rules | 0.98 |
| A Day 2 holdout access could have changed any decision | 0 (there is no promotion, and the code refuses E005 as NEW) |
| The first reproduction under the deterministic configuration gives byte-identical prediction files on all 8 folds | 0.93 |
| A Day 3 Tier 1 candidate that keeps the learned convention mixture passes criteria 1–3 against E005 | 0.95 |
| Such a candidate, FS1-based and deterministic, with no explicit subgroup treatment, exceeds +6,500 s on S1 | 0.60 |
| E005 is still champion at the Day 3 phase close | 0.50 |

Expected magnitude:
- **This exchange:** none (no experiment, no access).
- **E005's deficit.** Its deficit to the Tier 1 family on NM-present rows (51.5–59.6 s per development fold) persists into Day 3.
- **The S1 criterion 8 statistic.** For a deterministic FS1-family Day 3 candidate without an explicit subgroup treatment: +6,400 to +7,800 s.

Primary expected failure mode:
- **Primary.** Day 3 closes like Day 2. A congestion candidate clears criteria 1–4, but criterion 8 on S1 decides its promotion through the LIRF NM-missing subgroup, not through its mechanism. The tempting fixes are a re-set bound or a re-submitted E018-like configuration, and standing rule 10 forecloses both.
- **Secondary.** A criterion 4 margin of 1–3 s is read as mechanism evidence on a population where seed or procedure noise is of the same size.
