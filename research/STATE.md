# Research State

*Updated 2026-09-28T18:58Z (D02-S01, after exchange X-D02-S01-0001).*

- **Phase:** Day 2 — static and temporal structure. Day 1 is closed. The splits, metric and availability definition are **FROZEN** (`config/frozen.json`).
- **Current session:** D02-S01 (branch `day-2`, from `main` @ `d909de9`)
- **Last completed exchange:** X-D02-S01-0001 (Day 2 batch):
  - H009 v1 **REVISE**;
  - H010 v1 **ACCEPT (conditional)**, not yet allocatable;
  - H011 v1 **REVISE**.

  Day 1 exchanges: 0001–0004 (closed).
- **Champion:** **E005, H004 ridge on FS0** (phase-opening champion for Day 2).
  - Development mean RMSE 482.73 (R1 477.8, R2 323.5, R3 431.6, S1 670.0, W1 510.7).
  - Day 1 holdout: WIN (411.29 against E001 514.74).
- **Accepted findings:** H002, H003 and H004 were promoted in sequence on Day 1. H004 is the champion.
- **Rejected:** H005 (raw anchor), H007 (XGBoost FS0).
- **Inconclusive:** H006 (LightGBM FS0, development mean 377.87).
  - Its margin runs through LIRF NM-missing rows and the block-at-schedule convention (label T).
  - On NM-present rows it beats E005 by 31–40 s in the bulk on every fold (C1).
- **Day 2 work so far:**
  - EDA on never-validation months (`research/day-02/eda/`). Stand is the strongest static key, and static keys keep 5–15 s each on the anchor residual.
  - FS1 feature sets and tests.
  - Rule 7 disclosure in `scripts/compare.py`.
- **Day 2 plan (pending review):**
  - H009 v2: LightGBM FS1 candidate, with M1 on NM-present rows, M2 holding `d_sched` fixed, and M3 read as a lower bound.
  - H011 v2: static keys without the anchor, with no schedule-delay proxy.
  - H012: M2 anchor ablation.
  - H010 v1: the M3 ablation, allocated only after H009 v2 is ACCEPTED and its primary run is complete.
- **Standing Advisor rules:** 1 tail attribution; 2 forward exposure; 3 holdout only via phase close; 4 calendar-month identity; 5 all folds + H; 6 row concentration (B4); 7 NM × LIRF subgroup disclosure; 8 recording-convention disclosure. Batch conditions B1–B4 are carried.
- **Known leakage hazards:**
  - P/T/F labels (DATASET_AUDIT §6.2). `MVT − AOBT_3` and `d_sched` are T.
  - **Hour-resolution schedule-delay proxy:** takeoff hour or weekday (T) against scheduled local hour or weekday (P). It is label T.
  - `ades` is F for diverted flights (641 of 2,070; ~0.03 % of rows).
  - Cross-month information is inadmissible.
- **Key data facts:**
  - NM-missing rows are 0.8–2.1 % of each fold but carry 14–66 % of the SSE. There are 20,821 of them in Jan–Nov.
  - LIRF: block time is at the schedule in 83 % of tail rows.
  - 15 day-scale (≥ 80,000 s) records in Jan–Nov.
- **Open blockers:** none. The reuse of E006 and E010 as ablation references is permitted (X-D02-S01-0001).
- **Holdout:** 0 of 1 Day 2 accesses used.
- **Next action:** commit the v2 tooling (NM-present mechanism tests, subgroup tail shares, EDA finding 5 and build-check code); then H009 v2, H011 v2 and H012 v1 in exchange X-D02-S01-0002.
