# Day 1 summary: infrastructure, audit, frozen validation, baselines

**Session:** D01-S01 · **Branch:** `day-1` · **Status:** DRAFT. The phase-close review (X-D01-S01-0004) and the holdout check are pending.

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
- X-D01-S01-0004: phase close, *pending*.

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
3. **Day-scale records exist and are partly predictable.** At LIRF, one row has anchor 87,181 s against target 87,002 s (the anchor is exact), and another has no NM data and target 87,186 s. Each alone decides single-fold outcomes.
4. **NM-unmatched departures carry a heavy tail.** Their tail rate (y ≥ 3,600 s) is 4.9 %, against 0.15 % for matched rows; at **LIRF it is 49 %** (mean 6,457 s).
   - LightGBM exploits this. Its margin over ridge (−104.9 s) is 99 % tail, and it comes mostly from these rows, not from the pre-registered anchor mechanism.
   - H006 is therefore INCONCLUSIVE, not promoted (standing rule 1). It is the strongest Day 2 lead.
5. **Seasonality and regime effects are visible.** LTFM's winter tail (W1 RMSE 909 s under the global mean). A DST reversal between W1 and W1c for the hour key (H003). LFPG forward exposure on S1 (H002: 400.5 against 412.6 on S1c).
6. **Pre-registered magnitudes often missed.** Ridge 482.7 against 400–470 predicted; H003 0.96 % against 1–3 %; H006 tail share 0.991 against < 0.5. Direction predictions held, except H005 against H003.

## 4. Champion

**E005: H004 ridge on FS0** (development mean 482.73). Holdout check against E001: *pending*.

## 5. Open questions for Day 2

1. **The NM-unmatched tail mechanism** (LIRF above all). Pre-register it as its own hypothesis, with P-labelled inputs.
2. **Day-scale anchors and targets.** Should a model trust anchors above 20,000 s? n = 1 in training; July 2026 has one such row.
3. **Robustness in the bulk.** Tree models are worse than ridge in the bulk on S1 and R1. Candidates: tail-aware losses, or a two-stage model (tail classifier + bulk regressor). These are Tier 2 structural alternatives.
4. **Static structure (the brief's Day 2 theme).** Stand, aircraft type, operator, destination, local time (a P-labelled time key instead of the takeoff hour, per the H003 review).
5. **January 2026 anchor tail.** 0.375 % of rows have anchors ≥ 3,600 s, 3× any 2025 month, mostly EHAM 3–9 Jan. No fold reproduces it.
