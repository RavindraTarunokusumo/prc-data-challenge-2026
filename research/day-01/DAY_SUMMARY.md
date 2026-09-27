# Day 1 summary: infrastructure, audit, frozen validation, baselines

**Session:** D01-S01 · **Branch:** `day-1` · **Status:** FINAL. Phase-close review X-D01-S01-0004: ACCEPT. Holdout check: WIN.

The draft of this file (commit `bad75b6`) contained errors that the phase-close review identified. They are corrected below per `research/day-01/acks/PHASE_CLOSE_D01_ack_v1.md` (C1–C4), and the draft stays in history.

## 1. What was built

| Component | Where | Notes |
|---|---|---|
| Dataset + availability audit | `docs/methodology/DATASET_AUDIT.md` (frozen) | Snapshot-based admissibility; P/T/F information labels; cross-month inadmissible; holdout scope stated |
| Silver layer | `scripts/build_silver.py`, `data/manifests/silver_manifest.json` | 4,857,331 rows, deterministic (`efde4262…`) |
| Frozen validation | `config/splits.yaml`, `src/prc/{splits,metrics,evaluate}.py`, `config/frozen.json` | R1–R3 (Sep–Nov), S1 (Jul), W1 (Feb); twins S1c, W1c; holdout H = Dec 2025; paired airport-day bootstrap promotion rule |
| Governance | `scripts/gate.py`, `src/prc/ledger.py`, `scripts/run_experiment.py` | Hash-verified allocation; child-process runner with RAM/timeout watchdog; SQLite ledger + JSONL export |
| Attribution tooling | `scripts/compare.py`, `scripts/tail_mechanism.py`, `scripts/reproduce_check.py` | Standing rules 1 (tail) and 6 (row concentration); criterion-6 reproduction |
| Tests | `tests/` | 90 pass; lint clean |

**Advisor exchanges.**
- X-D01-S01-0001: SPLITS v1, **REVISE** (six defects).
- X-D01-S01-0002: SPLITS v2, **ACCEPT**, then frozen.
- X-D01-S01-0003: H001–H008, all **ACCEPT** with batch conditions B1–B4.
- X-D01-S01-0004: phase close, **ACCEPT**, with record corrections C1–C7 and new standing rules 7–8.

## 2. Baseline chain (pre-registered order; frozen promotion rule)

| Experiment | Hypothesis | Dev mean RMSE | R1 | R2 | R3 | S1 | W1 | Decision |
|---|---|---|---|---|---|---|---|---|
| E001 | H001 global mean | 580.79 | 560.3 | 437.1 | 532.1 | 746.1 | 628.4 | incumbent |
| E002 | H002 airport median | 553.74 | 530.0 | 397.5 | 507.3 | 723.9 | 610.0 | PROMOTE |
| E003 | H003 airport × hour median | 548.42 | 521.6 | 388.4 | 504.0 | 718.3 | 609.7 | PROMOTE |
| E004 | H005 raw anchor | 550.65 | 556.8 | 419.8 | 496.5 | 720.7 | 559.5 | REJECT |
| **E005** | **H004 ridge FS0** | **482.73** | 477.8 | 323.5 | 431.6 | 670.0 | 510.7 | **PROMOTE (champion)** |
| E006 | H006 LightGBM FS0 | 377.87 | 375.3 | 277.8 | 306.2 | 524.5 | 405.5 | INCONCLUSIVE |
| E011 | H007 XGBoost FS0 | 424.67 | 413.2 | 293.7 | 350.3 | 628.0 | 438.3 | REJECT |
| E010 | H008 LightGBM, no deltas (ablation) | 502.34 | 455.0 | 356.6 | 468.0 | 667.6 | 564.6 | ablation |

Reproductions E007, E008 and E009 (seed 43) are exact. Every run was within its resource class.

## 3. Findings

1. **The tail decides RMSE.** The top 0.1 % of rows carry 20–64 % of the fold SSE. The global mean's RMSE in the ≥ 3,600 s band is 5,155–10,594 s.
2. **The anchor `MVT − AOBT_3` is a strong but noisy input.**
   - Raw, it loses to a median in the bulk (R1 +53 s) and wins strongly in winter (W1 −47 s bulk).
   - Linearly corrected (ridge), it beats every Tier 0 model on every fold. The winsorisation clip carries only 5–40 % of that margin.
3. **Day-scale records exist and are partly predictable.**
   - Jan–Nov contains **15** DEP rows with targets ≥ 80,000 s: 13 at LIRF, 14 without NM data, and 5 in July 2025.
   - One of them (LIRF, anchor 87,181 s, target 87,002 s) has an exact anchor.
   - Single records like these decide single-fold outcomes (see the B4 dominant-row reports).
4. **NM-unmatched rows carry the metric, and at LIRF the tail is a recording convention.**
   - NM-missing rows are 0.8–2.1 % of each fold but carry 14–66 % of every model's SSE (C3). Their tail rate is 4.9 %, against 0.15 % for matched rows, and **49 % at LIRF**.
   - At LIRF, block time is within 120 s of the scheduled time in **83 %** of tail rows (base rate 26 %). The long "taxi-out" is therefore largely `MVT − SCHED`, a **block-at-schedule recording convention**, not taxi duration (C2). It is label T, not P.
   - H006's 0.991 tail share against ridge **nets** three pieces (C1): a bulk gain of 31–40 s on NM-present rows (every fold), a bulk loss on LIRF NM-missing rows, and a tail gain. On NM-present rows (98–99 % of each fold), LightGBM beats ridge by 40–57 s on every fold.
   - H006 is INCONCLUSIVE because its margin does not run through its pre-registered mechanism, not because trees are weaker in the bulk. That draft claim was wrong.
5. **Seasonality and regime effects are visible.** LTFM's winter tail (W1 RMSE 909 s under the global mean). A DST reversal between W1 and W1c for the hour key (H003). LFPG forward exposure on S1 (H002: 400.5 against 412.6 on S1c).
6. **Pre-registered magnitudes often missed** (explained largely by C3: NM-missing rows carry the SSE, and the audit's 385 s proxy excluded them). Ridge 482.7 against 400–470 predicted; H003 0.96 % against 1–3 %; H006 tail share 0.991 against < 0.5. Direction predictions held, except H005 against H003.

## 4. Champion

**E005: H004 ridge on FS0** (development mean 482.73; RMSE on NM-present rows 289 / 288 / 271 / 395 / 307 s for R1, R2, R3, S1, W1).

**Phase-close holdout check** (the single Day 1 access, logged 2026-09-27T13:42:35Z; `research/day-01/holdout/holdout_E005_vs_E001.json`):

| | H RMSE (Dec 2025) |
|---|---|
| E005 ridge | **411.29** |
| E001 global mean | 514.74 |
| dRMSE (q10…q90) | **−103.45** (−122.60…−90.21) → **WIN**, no revert |

The result is inside the Advisor's predicted range (−60 to −125 s). As the Advisor noted, this check can catch only a gross failure.

## 5. Open questions for Day 2

1. **The LIRF block-at-schedule convention and NM-missing rows.** Pre-register a hypothesis under standing rule 8:
   - state whether the mechanism is taxi duration or the recording convention;
   - label `d_sched`-derived inputs T;
   - give separate tail and bulk expectations for that subpopulation, plus an S1 expectation.
2. **Day-scale anchors and targets.** Should a model trust anchors above 20,000 s? n = 1 in training; July 2026 has one such row.
3. **Structural separation.** LightGBM is already better than ridge on NM-present rows. Candidate Tier 2 designs separate the populations that behave differently, e.g. NM-present vs NM-missing, LIRF convention rows, day-scale records. Every comparison discloses NM × LIRF subgroups (standing rule 7).
4. **Static structure (the brief's Day 2 theme).** Stand, aircraft type, operator, destination, local time (a P-labelled time key instead of the takeoff hour, per the H003 review).
5. **January 2026 anchor tail.** 0.375 % of rows have anchors ≥ 3,600 s, 3× any 2025 month, mostly EHAM 3–9 Jan. No fold reproduces it.
