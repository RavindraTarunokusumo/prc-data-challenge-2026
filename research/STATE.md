# Research State

*Updated 2026-09-27T13:42:27Z (C6 correction: previously stale since chain step 4).*

- **Phase:** Day 1 closing. Splits, metric and availability definition **FROZEN** (`config/frozen.json`). Phase-close review X-D01-S01-0004: **ACCEPT**. The holdout check is authorized and pending.
- **Current session:** D01-S01 (branch `day-1`)
- **Last completed exchange:** X-D01-S01-0004 (phase close, ACCEPT). Earlier: 0003 (H001–H008 ACCEPT), 0002 (SPLITS v2 ACCEPT), 0001 (SPLITS v1 REVISE)
- **Champion:** **E005, H004 ridge on FS0.** Development mean RMSE 482.73 (R1 477.8, R2 323.5, R3 431.6, S1 670.0, W1 510.7). Reproduction E009 is exact.
- **Accepted findings:** H002 (airport median) and H003 (airport × UTC hour) promoted in sequence. H004 promoted over H003.
- **Rejected:** H005 (raw anchor, falsified); H007 (XGBoost, falsified on both clauses)
- **Inconclusive:** H006 (LightGBM, development mean 377.87). It passes criteria 1–3 against E005 but fails criterion 4 under standing rule 1: its margin runs through LIRF NM-missing tail rows and the block-at-schedule convention (label T), not the pre-registered anchor mechanism. On NM-present rows it beats E005 by 40–57 s on every fold (C1).
- **Ablation:** H008 (E010), development mean 502.34. The deltas are used.
- **Standing Advisor rules:** 1 tail attribution; 2 forward exposure; 3 holdout only via phase close; 4 calendar-month identity; 5 all folds + H; 6 row concentration (B4); 7 NM × LIRF subgroup disclosure; 8 recording-convention disclosure
- **Known leakage hazards:** P/T/F labels (DATASET_AUDIT §6.2). `MVT − AOBT_3` and `d_sched` are T. Cross-month information is inadmissible.
- **Key data facts:**
  - NM-missing rows are 0.8–2.1 % of each fold but carry 14–66 % of SSE.
  - LIRF: block at schedule in 83 % of tail rows.
  - 15 day-scale (≥ 80,000 s) records in Jan–Nov: 13 at LIRF, 14 without NM data.
- **Open blockers:** none
- **Next action:** Day 1 holdout check (E005 vs E001), then DAY_SUMMARY finalisation, session end and the PR `day-1` → `main`. Day 2 on a new `day-2` branch.
