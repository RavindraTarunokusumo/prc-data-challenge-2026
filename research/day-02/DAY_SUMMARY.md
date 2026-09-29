# Day 2 summary: static and temporal structure

**Session:** D02-S01 · **Branch:** `day-2` · **Status:** FINAL. Phase-close review X-D02-S01-0006: ACCEPT. **No promotion; no holdout access** (Day 2: 0 of 1, closed unused).

The draft of this file (commit `5276cd8`) contained errors that the phase-close review identified. They are corrected below per `research/day-02/acks/PHASE_CLOSE_D02_ack_v1.md` (D2-C1 to D2-C10), and the draft stays in history. Following standing rule 11, every population-restricted figure is reported next to the all-rows figure of the same contrast.

**Researcher effort (INC-0003, open).** The researcher process that produced H009 v3–H014 v2, E012–E018 and the phase close carried `--effort medium`, while the session metadata records `high`. Every Day 2 artifact falls under this unresolved discrepancy (D2-C7).

## 1. The Day 2 question and its answer

Brief §11: *how much signal exists without inferred operational state?* The static keys are stand, aircraft type, operator prefix of the flight number and destination, plus the scheduled local time in FS1.

| Contrast | NM-present rows (matched population) | All rows |
|---|---|---|
| Four static keys, **no delta features** (E016 − E010) | **−29.6 s** | −28.0 s (q95 −19.0); S1 TIE |
| Six FS1 keys **on top of the delta set**, bagged (E012 − E006) | **−9.1 s** | **−1.72 s (q95 +9.39)**: criterion 1 fails |
| The same, deterministic (E017 − E018) | **−8.7 s** | **−2.13 s (q95 +13.09)**: criterion 1 fails |

**Reading** (corrected, D2-C2).
- Static keys carry real signal on NM-present rows: about 30 s without the delta features and about 9 s with them.
- The delta set (`d_aobt3`, `d_eobt1`, `d_sched`, `flt_missing`) absorbs about 70 % of it. That is the delta set, not the anchor alone.
- **On all rows, FS1 is not distinguishable from FS0 on the metric.** The LIRF NM-missing convention records swamp the static effect.
- M1's registered test (NM-present rows outside LIRF) passed in both procedures (−7.16 s bagged, −7.27 s deterministic), with W1c LOSS both times.
- The M2 anchor effect is −51.3 s on NM-present rows (E012 − E014, bagged; all rows −37.25 s). The deterministic figure (−52.1 s, E017 − E014) is a carry-over against a bagged reference, not a deterministic M2 estimate.

## 2. What was built

| Component | Where |
|---|---|
| EDA on never-validation months only, plus supplement and corrections | `research/day-02/eda/`, `scripts/eda_day2*.py` |
| FS1 family: FS1, FS1_NO_DSCHED, FS1_NO_ANCHOR, FS1_NO_DELTAS, FS1_STATIC_NO_DELTAS; local time; counts-only rare collapse | `src/prc/features.py`, `tests/test_features_fs1.py` |
| Rule 7 subgroup disclosure (with tail and bulk shares) and rule 6 on any population | `src/prc/attribution.py`, `scripts/compare.py` |
| Mechanism checks: the frozen criteria on a named sub-population | `scripts/mechanism_check.py` |
| Determinism tests for LightGBM, including above the bin-construction threshold (synthetic data) | `tests/test_models.py` |

`pytest` 101/101 and `ruff` clean.

## 3. Advisor exchanges

| Exchange | Content | Decisions |
|---|---|---|
| X-D02-S01-0001 | H009 v1, H010 v1, H011 v1 | REVISE; ACCEPT (conditional); REVISE |
| X-D02-S01-0002 | H009 v2, H011 v2, H012 v1 | REVISE; ACCEPT; ACCEPT |
| X-D02-S01-0003 | H009 v3 | ACCEPT |
| X-D02-S01-0004 | H013 v1, H014 v1 | REVISE; ACCEPT (lapsed) |
| X-D02-S01-0005 | H013 v2, H014 v2 | ACCEPT; ACCEPT |
| X-D02-S01-0006 | Phase close | ACCEPT; corrections D2-C1 to D2-C10; standing rules 9–11; rulings H, B, R |

**The REVISEs caught real defects before any compute was spent.**
- **H009 v1:** M1 could be decided by LIRF NM-missing rows; M2 confounded `d_sched`; a missed hour-resolution schedule-delay proxy.
- **H009 v2:** one day-scale record (192622644) could decide the required S1 WIN. E012 later showed that v2's population would have falsified H009 through that row alone (S1 TIE, top-1 share −8.93).
- **H013 v1:** a false determinism premise. LightGBM's bin-construction sample consumes the seed above 200,000 training rows.

## 4. Experiments (all sequential, all within class)

| E | Hypothesis | Dev mean | Outcome |
|---|---|---|---|
| E012 | H009 v3, LightGBM FS1 (bagged), candidate | 376.15 | Clauses 1–4 not met; against E005 −106.58 s, 7/7 WIN |
| E013 | H010, FS1 − `d_sched` (M3 ablation) | 415.03 | M3 supported |
| E014 | H012, FS1 − anchor (M2 ablation) | 413.40 | M2 supported |
| E016 | H011 v2, static keys without deltas | 474.33 | Static claim not falsified |
| E015 | H009 v3 reproduction (seed 43) | 377.29 | **Criterion 6 FAILS** (R3 1.73 s, S1 3.50 s) → **H009 INCONCLUSIVE** |
| E017 | H013 v2, LightGBM FS1 with no random component, candidate | 378.82 | Clauses 1–4 not met; **criterion 8 NOT resolved** (S1 +7,104 > +6,500) → **H013 INCONCLUSIVE**; not reproduced |
| E018 | H014 v2, FS0 with no random component (M1 reference) | 380.95 | M1 replicated |

## 5. Champion: E005 by rule

**E005 (H004 ridge on FS0) remains champion by rule. It is not the most accurate model.** No Day 2 candidate met all promotion criteria.
- **H009 v3** failed criterion 6.
- **H013 v2** failed criterion 8.

**The margin over E005** (corrected, D2-C1). The candidates beat E005 on every development fold, but not by "~100 s everywhere".

| Population | E012 | E017 |
|---|---|---|
| All rows, development mean | −106.58 s | −103.90 s |
| All rows, range | R2 −60.9 s to S1 −131.9 s | R2 −65.2 s to S1 −121.1 s |
| NM-present rows | −51.5 to −59.6 s on every development fold (both fits) | |

- LIRF NM-missing rows carry 0.17–0.73 of each fold's SSE change.
- **On S1 and S1c,** the candidates' bulk loss on LIRF NM-missing normal-taxi rows exceeds their whole NM-present gain (1.13–1.63×). Their S1 WIN rests on about 119 convention rows, and ten rows carry 0.69–0.75 of the change.
- **The ranking-month advantage is therefore conditional on the LIRF recording convention recurring in July 2026.**

## 6. Findings

1. **Static structure.** See §1: about 9 s on NM-present rows with the delta features, and not distinguishable from zero on all rows.
2. **Deterministic training** (no subsampling, all-row bins) (corrected, D2-C5).
   - **On NM-present rows** it is practically free: E017 − E012 is −0.75 s, every fold within ±2.4 s.
   - **On all rows** it costs +2.67 s (FS1) and +3.08 s (FS0, E018 − E006), with S1 and W1 LOSS for E017 − E012.
   - It runs faster (668 s against 906 s).
   - Its determinism on real data is **untested**; it is a premise until a reproduction shows identical prediction files.
   - It remains the candidate procedure for criterion 6 on Days 3–4.
3. **The LIRF convention and the criterion 8 statistic** (corrected, D2-C3 and D2-C4).
   - S1 `NM_missing_LIRF.delta_rmse_bulk` against E005 (exact, same rows):

     | E006 | E018 | E012 | E015 | E017 |
     |---|---|---|---|---|
     | +5,782 | +6,387 | +6,390 | +6,456 | +7,104 |

   - Both the static keys (+608 / +717 s) and the deterministic procedure (+605 / +714 s) **worsen** July. "Static keys dilute the convention" holds on some folds but is **reversed on S1** in both procedures, and on R3 under the deterministic procedure (+146 s).
   - **Seed variance is not confined to LIRF NM-missing rows.** Excluding them, E015 − E012 is still +1.33 s on S1 and −1.94 s on W1. Only NM-present rows outside LIRF are within 1.0 s on every development fold: R1 0.13, R2 0.53, R3 0.21, S1 0.91, W1 −0.52 s. The twins are S1c 0.23 s and **W1c −1.40 s**, so even this population exceeds 1.0 s on the January-only twin. (`E015_vs_E012_mech_*.json`)
   - A structural treatment of the LIRF subgroup would therefore **not** resolve a bagged model's criterion 6 exposure.
4. **Rule 8 residuals.**
   - Even without `d_sched` or the scheduled-time proxy, static keys partly reach the convention (H011 v2: R3 and W1 tail share 0.5).
   - Without `d_sched`, the model does not simply revert to a normal-taxi prior (H010: bulk recovered on 2 of 5 folds).

## 7. Missed or corrected predictions (kept)

- **H009 v3:** development mean 355–372 → **376.15**; clause 1 −110 to −130 → **−106.58**; rule 8 tail share on R2 **0.25** (band 0.3–1.1).
- **H010:** bulk recovery on every fold → 2/5; S1 the smallest net loss → the largest.
- **H011 v2:** magnitude −8 to −30 → **−30.03**; LIRF NM-missing tail within ±0.3 and bulk within ±300 s → missed on 3 development folds and both twins.
- **H013 v1:** "identical predictions" under the v1 configuration was false. The researcher's supporting check was a false negative (simple synthetic data), and its commit citation (`f84fea3`) was wrong.
- **H013 v2:** rule 8 bulk band → S1 **+7,104.4**; tail band → R2 **0.28**, S1 **1.17**.
- **The EDA** reported 0 % unseen ranking levels, a vocabulary artifact (corrected: 0.005–0.27 %).
- **Process slips:**
  - unmeasured `created_utc` and STATE.md header times;
  - STATE.md stale at the E017 and E018 checkpoints (D2-C6, a repeat of Day 1 C6);
  - the E015/E016 allocation order (the run order was kept);
  - E013, E014 and E015 allocated from a tree with uncommitted output files (D2-C9);
  - E015's dirty tree disclosed late;
  - the H013 v1 rule 8 tail band set after E012 (withdrawn in v2).

## 8. Open questions for Day 3

1. **The LIRF NM-missing convention records.**
   - They decide promotion (criterion 8), and on S1 accuracy as well (§5).
   - A structural treatment could address criterion 8. It would not fix a bagged model's criterion 6 exposure (§6.3), so it should be paired with the deterministic procedure.
   - **Ruling B:** a new threshold on the criterion 8 statistic will not be accepted. An alternative resolution needs a forward-risk rationale that does not rest on E006–E018 outcomes (standing rule 10).
2. **Congestion reconstruction** (brief Day 3, highest priority). It should be built on the Day 2 disclosure tooling.
3. **Comparison base (ruling R).**
   - A comparison base is a **matched reference** that shares the candidate's training procedure, not a champion.
   - E017 is not the strongest model on all rows.
   - Criteria 1–3 against E005 cannot test a Day 3 mechanism, so criterion 4 must carry every mechanism claim.
4. **Standing rules 9–11** apply from the next proposal. The Day 2 holdout is closed unused, and E012–E018 may never be NEW in a holdout access.
5. **INC-0003** (researcher effort tier) awaits the owner.
