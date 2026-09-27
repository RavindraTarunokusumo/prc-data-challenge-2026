# Research State

- **Phase:** Day 1 (in progress). Splits, metric and availability definition **FROZEN** (`config/frozen.json`, 2026-09-27T12:00:10Z)
- **Current session:** D01-S01 (branch `day-1`)
- **Last completed exchange:** X-D01-S01-0002 (SPLITS v2: ACCEPT). X-D01-S01-0001 (SPLITS v1: REVISE)
- **Champion:** E003 (H003 airport × UTC-hour median; dev mean RMSE 548.42; chain step 2)
- **Accepted findings:** none (no experiments yet)
- **Rejected hypotheses:** none
- **Frozen design:** development folds R1–R3 (Sep–Nov), S1 (Jul), W1 (Feb). Causal twins S1c, W1c. Protected holdout H = Dec 2025 (targets masked at the data layer, one paired access per phase). Final folds SUBMIT_JAN / SUBMIT_JUL. Paired airport-day bootstrap promotion rule (`config/splits.yaml: promotion`)
- **Standing Advisor rules:** tail attribution, forward exposure (S1c/W1c sign), holdout only via phase close, calendar-month identity, all 7 folds + H (`research/day-01/advisor/SPLITS_review_v2.md`)
- **Known leakage hazards:** P/T/F information labels (DATASET_AUDIT §6.2). The `MVT − AOBT_3` anchor is label T. Cross-month information is inadmissible
- **Open blockers:** none
- **Next action:** regenerate H001–H008 with measured timestamps and standing-rule sections, then submit them as a batch (X-D01-S01-0003)
