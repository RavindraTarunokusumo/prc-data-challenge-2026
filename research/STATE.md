# Research State

*Updated 2026-09-28T20:57:38Z (measured with `date -u` at writing; D02-S01, Day 2 chain complete).*

- **Phase:** Day 2 — static and temporal structure. Splits, metric and availability definition are **FROZEN** (`config/frozen.json`).
- **Current session:** D02-S01 (branch `day-2`, from `main` @ `d909de9`)
- **Last completed exchange:** X-D02-S01-0003, H009 v3 **ACCEPT** (0.85).
  - X-D02-S01-0002: H009 v2 REVISE; H011 v2 ACCEPT (conditional); H012 v1 ACCEPT (conditional).
  - X-D02-S01-0001: H009 v1 REVISE; H010 v1 ACCEPT (conditional); H011 v1 REVISE.
- **Champion:** **E005, H004 ridge on FS0** (unchanged by Day 2 so far).
  - Development mean 482.73 (R1 477.8, R2 323.5, R3 431.6, S1 670.0, W1 510.7).
  - Day 1 holdout: WIN.
- **Accepted findings:** H002, H003 and H004 (Day 1 chain).
- **Rejected:** H005, H007. **Inconclusive:** H006 (LightGBM FS0, 377.87; margin via the LIRF convention).
- **Day 2 chain: complete.** All runs sequential and within class.

  | Run | Hypothesis | Development mean | Outcome |
  |---|---|---|---|
  | E012 | H009 v3, LightGBM FS1 (candidate) | 376.15 | Clauses 1–4 not met (not falsified); against E005 −106.58 s, 7/7 WIN |
  | E013 | H010, − `d_sched` | 415.03 | M3 supported |
  | E014 | H012, − anchor | 413.40 | M2 supported (−51.3 s on NM-present rows) |
  | E016 | H011 v2, static keys without deltas | 474.33 | Static claim holds (−30.0 s against E010) |
  | E015 | H009 reproduction, seed 43 | — | **Criterion 6 FAILS** (R3 1.73 s, S1 3.50 s against a 1.0 s tolerance) |

  - The E015 failure is carried by LIRF NM-missing convention records.
  - Outside them, the seed shifts are 0.23 s (R3) and 1.33 s (S1); on NM-present rows outside LIRF, 0.21 s and 0.91 s.
  - **H009: INCONCLUSIVE**, not promoted.
- **Day 2 findings:**
  - The static keys are worth about 30 s without the anchor and about 7 s with it.
  - The anchor (M2) is worth about 51 s on NM-present rows beyond `d_sched`.
  - The exact `d_sched` convention route (M3) is real, and even the static keys alone partly reach it.
  - Bagged Tier 1 models are seed-unstable on LIRF day-scale convention records, which exposes every such candidate to criterion 6.
- **Standing Advisor rules:** 1–8. Batch conditions B1–B4 carried. The criterion 8 resolution rule is recorded in `research/day-02/acks/H009_ack_v3.md`.
- **Known leakage hazards:**
  - P/T/F labels. `MVT − AOBT_3` and `d_sched` are T.
  - The hour-resolution schedule-delay proxy (takeoff hour/weekday against scheduled local hour/weekday) is T.
  - `ades` is F on diversions (~0.03 % of rows).
  - Cross-month information is inadmissible.
- **Key data facts:**
  - NM-missing rows are 0.8–2.1 % of each fold and carry 14–66 % of the SSE; there are 20,821 in Jan–Nov.
  - LIRF: 83 % of tail rows are block-at-schedule, and 931 of 932 NM-present ones have a normal anchor.
  - LIRF rows 192622644 (S1, y 87,002 s, day-scale) and 183910286 (W1, y 13,865 s) dominate NM-present comparisons.
- **Open incidents:** INC-0003 (researcher effort: `--effort medium` launch argument against `high` in the session metadata). Owner to resolve; not blocking.
- **Holdout:** 0 of 1 Day 2 accesses used.
- **Next action:** decide how to handle the criterion 6 exposure (a pre-registered, seed-stable design), or proceed to the Day 2 phase close with E005 as champion.
