# Day 2 summary: static and temporal structure

**Session:** D02-S01 · **Branch:** `day-2` · **Status:** DRAFT, pending the phase-close review (X-D02-S01-0006).

## 1. The Day 2 question and its answer

Brief §11: *how much signal exists without inferred operational state?* The static keys are stand, aircraft type, operator prefix of the flight number, and destination, plus the scheduled local time for H009 and H013.

| Measure | Value | Source |
|---|---|---|
| Four static keys, **no anchor, no schedule-delay route** (H011 v2 against E010, rows excluding LIRF NM-missing) | **−30.0 s** (q95 −28.5), 5/5 WIN | E016 |
| Six FS1 keys **on top of the full anchor set** (M1, NM-present rows outside LIRF) | **−7.2 s** bagged (E012 − E006); **−7.3 s** deterministic (E017 − E018) | clause 2(a) |
| The NM anchor (`d_aobt3`, `d_eobt1`) beyond `d_sched` and the static keys (M2, NM-present rows) | **−51.3 s** bagged; **−52.1 s** deterministic; largest in winter (W1 −84 s) | E012/E017 against E014 |
| Exact `d_sched` beyond the hour-resolution proxy on LIRF NM-missing rows (M3, the recording convention) | −314 to −2,493 s on every development fold | E012 against E013 |

**Reading.**
- Static structure is real and robust: every fold, both training procedures, no row concentration.
- **The anchor absorbs about three-quarters of it.** Most of what stand, type and operator say about taxi time is already reflected in NM's off-block estimate relative to takeoff.
- The single largest mechanism is the anchor.

## 2. What was built

| Component | Where |
|---|---|
| EDA on never-validation months only, plus supplement and corrections | `research/day-02/eda/`, `scripts/eda_day2*.py` |
| FS1 family: FS1, FS1_NO_DSCHED, FS1_NO_ANCHOR, FS1_NO_DELTAS, FS1_STATIC_NO_DELTAS; local time; counts-only rare collapse | `src/prc/features.py`, `tests/test_features_fs1.py` |
| Rule 7 subgroup disclosure (with tail and bulk shares) and rule 6 on any population | `src/prc/attribution.py`, `scripts/compare.py` |
| Mechanism checks: the frozen criteria on a named sub-population | `scripts/mechanism_check.py` |
| Determinism tests for LightGBM, including above the bin-construction threshold | `tests/test_models.py` |

`pytest` 101/101 and `ruff` clean at the time of writing.

## 3. Advisor exchanges

| Exchange | Content | Decisions |
|---|---|---|
| X-D02-S01-0001 | H009 v1, H010 v1, H011 v1 | REVISE; ACCEPT (conditional); REVISE |
| X-D02-S01-0002 | H009 v2, H011 v2, H012 v1 | REVISE; ACCEPT; ACCEPT |
| X-D02-S01-0003 | H009 v3 | ACCEPT |
| X-D02-S01-0004 | H013 v1, H014 v1 | REVISE; ACCEPT (lapsed) |
| X-D02-S01-0005 | H013 v2, H014 v2 | ACCEPT; ACCEPT |

**The REVISEs caught real defects before any compute was spent.**
- H009 v1: M1 could be decided by LIRF NM-missing rows; M2 confounded `d_sched`; a missed hour-resolution schedule-delay proxy.
- H009 v2: one day-scale record (192622644) could decide the required S1 WIN. E012 later showed that v2's population **would have falsified H009 through that row alone** (S1 TIE, top-1 share −8.93).
- H013 v1: a false determinism premise (LightGBM's bin-construction sample consumes the seed above 200,000 rows).

## 4. Experiments (all sequential, all within class)

| E | Hypothesis | Dev mean | Outcome |
|---|---|---|---|
| E012 | H009 v3, LightGBM FS1 (bagged), candidate | 376.15 | Clauses 1–4 not met (not falsified); against E005 −106.58 s, 7/7 WIN |
| E013 | H010, FS1 − `d_sched` (M3 ablation) | 415.03 | M3 supported |
| E014 | H012, FS1 − anchor (M2 ablation) | 413.40 | M2 supported |
| E016 | H011 v2, static keys without deltas | 474.33 | Static claim holds (−30.0 s) |
| E015 | H009 v3 reproduction (seed 43) | — | **Criterion 6 FAILS** (R3 1.73 s, S1 3.50 s) → **H009 INCONCLUSIVE** |
| E017 | H013 v2, LightGBM FS1 with no random component, candidate | 378.82 | Clauses 1–4 not met; **criterion 8 NOT resolved** (S1 LIRF NM-missing bulk +7,104 > +6,500) → **H013 INCONCLUSIVE** |
| E018 | H014 v2, FS0 with no random component (M1 reference) | 380.95 | M1 replicated (−7.27 s) |

## 5. Champion

**E005 (H004 ridge on FS0) remains champion.** No Day 2 candidate met all promotion criteria.
- **H009** failed criterion 6. Its seed variance was carried by LIRF NM-missing convention records: excluding them, R3 moved 0.23 s and S1 1.33 s.
- **H013** failed criterion 8. Without bagging, its convention-row predictions were more extreme.

**Both candidates beat E005 by more than 100 s on every fold** and are not falsified. What blocks them is the same structural problem: a few hundred LIRF records whose block time is recorded at the schedule.

## 6. Findings

1. **Static structure** is worth about 30 s without the anchor and about 7 s with it (§1).
2. **Deterministic training is essentially free.** On NM-present rows, deterministic LightGBM (no subsampling, all-row bins) differs from the bagged model by −0.75 s on average (every fold within ±2.4 s), and it runs faster (668 s against 906 s). It makes criterion 6 a determinism check. It is the recommended default for Days 3–4.
3. **The LIRF convention decides promotion, not accuracy.**
   - The block-at-schedule mixture on LIRF NM-missing rows is the only place where Tier 1 models are seed-unstable.
   - It is where criterion 8's bulk trade lives (+5,000 to +7,100 s bulk dRMSE on S1).
   - Static keys **dilute** it: they move convention predictions toward normal taxi time. That was the reverse of the feared "identifier" effect.
4. **Rule 8 residuals.**
   - Even without `d_sched` or the scheduled-time proxy, static keys partly reach the convention (H011 v2: R3 and W1 tail share 0.5).
   - Without `d_sched`, the model does not simply revert to a normal-taxi prior (H010: bulk recovered on only 2 of 5 folds).

## 7. Missed or corrected predictions (kept)

- **H010:** bulk recovery on every fold (2/5); S1 the smallest net loss (it was the largest).
- **H011 v2:** LIRF NM-missing tail within ±0.3 and bulk within ±300 s (missed on 3 development folds and both twins).
- **H013 v1:** "identical predictions" under the v1 configuration was false. The researcher's supporting check was a false negative, and its commit citation was wrong.
- **The EDA** reported 0 % unseen ranking levels, a vocabulary artifact (corrected: 0.005–0.27 %).
- **Process slips:**
  - unmeasured `created_utc` and STATE.md header times;
  - the E015/E016 allocation order (run order was kept);
  - E015's dirty tree was undisclosed (appended);
  - the H013 v1 rule 8 tail band was widened after E012 (withdrawn in v2).

## 8. Open questions for Day 3

1. **A structural treatment of LIRF NM-missing convention records** (Tier 2). A deterministic, explicit mixture for that subgroup could resolve both the criterion 6 and the criterion 8 exposure of any Tier 1 candidate. This is a candidate before or alongside congestion features.
2. **Congestion reconstruction** (brief Day 3, highest priority). It should be built on the deterministic LightGBM FS1 configuration and use the Day 2 disclosure tooling.
3. **Whether E017 or E012 should be the Day 3 comparison base.** The champion remains E005 by rule, but Day 3's mechanism tests need a strong Tier 1 reference.
4. **INC-0003** (researcher effort tier) awaits the owner.
