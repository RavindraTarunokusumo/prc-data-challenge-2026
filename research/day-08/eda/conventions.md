# Agenda item 1: recording conventions in the tail beyond LIRF (design months only)

*Written 2026-10-07T21:42:19Z (D08-S03, laptop).*

- **Script:** `scripts/eda_conventions_D08.py`. Its reading rule was committed before the run (commit "agenda item 1 look"). Output: `research/day-08/eda/conventions.json` and `.log`.
- **Targets read:** DEP rows of 2025-01, 04, 05 and 06 only, at row level (X-D08-S01-0001 (d)). No validation-month target and no December target was read. No model was fitted.

## What is new against PHASE_CLOSE_D01 (c)

Day 1 tested block = SCHED only. This look adds:
- block equal to EOBT_1, IOBT, LOBT or AOBT_3;
- block recorded 1–3 h early against AOBT_3, EOBT_1 or SCHED (a local-time-as-UTC error);
- block one day early against SCHED or EOBT_1;
- block on a whole hour;
- a block time repeated across five or more departures at one airport.

## Result: no finding

The rule (fixed before the run): at least 30 tail rows, and a tail share at least twice the bulk share, at an airport other than LIRF. **No signature meets it at any of the nine airports.**

| Airport | Tail rows (y ≥ 3,600 s) | NM-missing among them | Tail share of the airport's squared deviation | Largest signature in the tail |
|---|---|---|---|---|
| EGLL | 229 | 7 | 0.21 | block = SCHED: 30 rows (0.13 of tail, against 0.18 of bulk) |
| LFPG | 162 | 18 | 0.54 | block = IOBT / LOBT: 14 (0.09, against 0.20) |
| EHAM | 57 | 10 | 0.08 | block = AOBT_3: 12 (0.21, against 0.44) |
| LTFM | 47 | 9 | 0.04 | block = SCHED: 6 (0.13, against 0.20) |
| EDDF | 27 | 1 | 0.04 | block = IOBT / LOBT: 4 (0.15, against 0.17) |
| EDDM | 19 | 0 | 0.05 | block 1 h before AOBT_3: 5 (0.26, against 0.000) |
| LSZH | 13 | 3 | 0.67 | 1 row each |
| LEBL, LEMD | 0 | 0 | 0 | none |
| *LIRF (check)* | *557* | *212* | *0.85* | *block = SCHED: 470 (0.84, against 0.25), as Day 1* |

Notes:
- **Every anchor-equality signature is below its bulk base rate in the tail** outside LIRF. Long taxi-outs elsewhere are not recorded at a planned time.
- **Hour shifts are rare.** All shift signatures together cover 0–19 tail rows per airport. EDDM's 5 rows against a bulk share of 0.000 are below the 30-row floor.
- **Round-hour and repeated block times are absent** (0–1 tail rows outside LIRF).
- **Agenda item 1 is closed with no lead.** The non-LIRF tail looks like real long taxi-outs or unrecorded causes, not a recording convention a model can decode. No proposal follows.

## Corrections (2026-10-07T22:12:16Z; X-D08-S03-0004, D8-C19)

- The look tested **18** signatures, not 15.
- The ratio test is vacuous for the hour- and day-shift signatures, because such a row is in the tail by construction. Only the 30-row floor applied to them.
- Pooled across the nine airports, "block 1 h before AOBT_3" covers 30 of 554 non-LIRF tail rows. Its oracle stake is about 0.8 s of all-rows RMSE.
- The last bullet's second sentence reads: **"No tested signature explains the non-LIRF tail; the look does not show what those rows are."**
- The pre-registration commit is `a37f95e`.
