# Research State

*Updated 2026-09-28T19:37:00Z (measured with `date -u` at writing; D02-S01, after X-D02-S01-0003).*

- **Phase:** Day 2 — static and temporal structure. Splits, metric and availability definition are **FROZEN** (`config/frozen.json`).
- **Current session:** D02-S01 (branch `day-2`, from `main` @ `d909de9`)
- **Last completed exchange:** X-D02-S01-0003, H009 v3 **ACCEPT** (0.85).
  - X-D02-S01-0002: H009 v2 REVISE; H011 v2 ACCEPT (conditional); H012 v1 ACCEPT (conditional).
  - X-D02-S01-0001: H009 v1 REVISE; H010 v1 ACCEPT (conditional); H011 v1 REVISE.
- **Champion:** **E005, H004 ridge on FS0.**
  - Development mean 482.73 (R1 477.8, R2 323.5, R3 431.6, S1 670.0, W1 510.7).
  - Day 1 holdout: WIN.
- **Accepted findings:** H002, H003 and H004 (Day 1 chain).
- **Rejected:** H005, H007. **Inconclusive:** H006 (LightGBM FS0, 377.87; margin via the LIRF convention).
- **Day 2 chain (authorized; runs sequential, never concurrent):**
  1. H009 v3 (LightGBM FS1, candidate) → comparisons against E005, then E006 on `NM_present_excl_LIRF` / `NM_present` / `LIRF_NM_missing`.
  2. H010 v1 (FS1 − `d_sched`, M3).
  3. H012 v1 (FS1 − anchor, M2).
  4. H011 v2 (FS0 no-deltas + 4 static keys, the Day 2 question).
  5. Conditional seed-43 reproduction of H009.
- **Frozen until clauses 1–4 are computed:** `scripts/compare.py`, `scripts/mechanism_check.py`, `src/prc/attribution.py` (as at `5ba9230`).
- **Standing Advisor rules:** 1–8. Batch conditions B1–B4 carried. The criterion 8 resolution rule is recorded in `research/day-02/acks/H009_ack_v3.md`.
- **Known leakage hazards:**
  - P/T/F labels. `MVT − AOBT_3` and `d_sched` are T.
  - The hour-resolution schedule-delay proxy (takeoff hour/weekday against scheduled local hour/weekday) is T.
  - `ades` is F on diversions (~0.03 % of rows).
  - Cross-month information is inadmissible.
- **Key data facts:**
  - NM-missing rows are 0.8–2.1 % of each fold and carry 14–66 % of the SSE; there are 20,821 in Jan–Nov.
  - LIRF: 83 % of tail rows are block-at-schedule, and 931 of 932 NM-present ones have a normal anchor.
  - Day-scale rows 192622644 (S1) and 183910286 (W1) dominate NM-present comparisons at LIRF.
- **Open incidents:** INC-0003 (researcher effort: `--effort medium` launch argument against `high` in the session metadata). Owner to resolve; not blocking.
- **Holdout:** 0 of 1 Day 2 accesses used.
- **Next action:** `gate.py allocate H009 v3` → run → chain step 1 comparisons.
