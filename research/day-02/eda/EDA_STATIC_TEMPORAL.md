# Day 2 EDA: static and temporal keys (descriptive)

**Session:** D02-S01 · **Producer:** `uv run python scripts/eda_day2.py` → `static_temporal.json` (this directory)

## Target hygiene

Targets were read only for months that are **never a validation month of any frozen fold**:
- FIT = Jan and Mar–Jun 2025;
- EVAL = Aug 2025 (the S1 embargo month; a training month in every other fold).

Feb (W1), Jul (S1), Sep–Nov (R1–R3) and Dec (H, masked by `load_silver`) targets were **not** read. The ranking-coverage column is target-free. No model was fitted and no fold was scored. Every Day 2 proposal below was written after this EDA and before any Day 2 experiment.

## Method

For each key, a shrunken within-airport key mean (pseudo-count 50) is fitted on FIT, and the out-of-time RMSE reduction is measured on EVAL. Two residuals, bulk rows only (y < 3,600 s):
- `r_apt` = y − airport median (static signal on its own; 190,840 EVAL rows);
- `r_anch` = y − (`d_aobt3` + airport median offset), NM-present rows only (signal left after the raw anchor; 188,611 EVAL rows).

Both residuals have a baseline RMSE of ≈ 350 s (346.5 and 352.8 s). The raw anchor with an airport offset is no better than the airport median in the bulk, as in Day 1 (E004).

## Results

| Key | Label | Levels (Jan–Nov) | Gain vs airport median (s) | Gain on anchor residual, NM-present (s) | EVAL unseen |
|---|---|---|---|---|---|
| `stand` | P | 1,930 | 43.0 | 14.6 | 0.19 % |
| `stand_group` | P | 61 | 18.9 | 9.9 | 0.00 % |
| `stand_runway` | P | 12,367 | **52.9** | 14.4 | 3.02 % |
| `actype` | P | 278 | 28.7 | 10.9 | 0.03 % |
| `wake` | P | 5 | 18.0 | 7.4 | 0.00 % |
| `op_prefix` (first 3 chars of `FLIGHT_mvt`) | P | 2,501 | 33.4 | 11.9 | 0.28 % |
| `operator_nm` (`AIRCRAFT_OPERATOR_flt`) | P | 707 | 31.6 | 12.0 | 0.14 % |
| `ades` | P | 1,631 | 31.5 | 12.7 | 0.27 % |
| `ades_region` | P | 234 | 28.3 | 11.7 | 0.03 % |
| `runway` | P | 53 | 19.5 | 8.0 | 0.00 % |
| `flight_rule` | P | 3 | 7.2 | 4.9 | 0.00 % |
| `market` | P | 9 | 13.3 | 7.9 | 0.00 % |
| `sched_hour_local` | P | 24 | 15.6 | 7.5 | 0.00 % |
| `sched_hour_utc` | P | 24 | 15.0 | 7.4 | 0.00 % |
| `sched_weekday_local` | P | 7 | 6.7 | 4.8 | 0.00 % |
| `sched_weekhour_local` | P | 168 | 15.3 | 7.2 | 0.01 % |
| `mvt_hour_utc` (Day 1 `hour_utc`) | T | 24 | 17.2 | 8.3 | 0.00 % |

## Findings

1. **Stand is the strongest single static key.**
   - Stand alone removes 43 s of the within-airport bulk RMSE, and stand × runway (the taxi route) removes 53 s.
   - The physical reading is taxi distance from stand to runway threshold.
2. **Operator, destination and aircraft type each carry 28–33 s against the airport median.**
   - On the anchor residual, every key keeps 5–15 s. Static structure is therefore not fully absorbed by the anchor.
   - The keys are correlated, so the individual gains do not add up.
3. **Local and UTC scheduled hours are equivalent here** (15.6 vs 15.0 s).
   - The local key is preferred on mechanism: airport operations follow local time, and the Day 1 DST reversal under the UTC key (H003) supports it.
   - The P-labelled scheduled hour carries about as much as the T-labelled takeoff hour (15.6 vs 17.2 s).
4. **Coverage.**
   - Every key has no unseen levels in the ranking DEP rows against the Jan–Nov vocabulary.
   - On NM-missing DEP rows (27,760 in Jan–Nov), `FLIGHT_mvt`, `ADES_mvt` and `STAND_mvt` are present in > 99.6 % of rows and `AIRCRAFT_TYPE_mvt` in 93.2 %.
   - The NM operator column is null there by construction, which is why the operator is taken from the flight-number prefix.
5. **The LIRF convention is not separable by static keys** (FIT months, LIRF NM-missing rows, n = 473, convention-tail rate 0.50).
   - LIRF stands are all numeric: the stand group is uninformative.
   - Operator groups are small (the largest, RYR, has 68 rows, rate 0.46).
   - `d_sched` (label T) is the separator:

     | `d_sched` | ≤ 3,600 s | 3,600–7,200 s | > 7,200 s |
     |---|---|---|---|
     | Convention-tail rate | 0.00 | 0.43 | 0.70 |

## FS1 build (non-scoring sanity check, S1 fold)

- **Cost:** the build takes 1.9 s and peaks at 3.1 GB RSS (1,728,188 DEP rows).
- **Levels after the fold-local rare collapse** (< 100 training rows → `__RARE__`):

  | Key | Levels | Rare share, training | Rare share, validation |
  |---|---|---|---|
  | stand | 1,316 | 0.76 % | 0.87 % |
  | actype | 118 | 0.14 % | 0.15 % |
  | op_prefix | 489 | 1.58 % | 1.78 % |
  | ades | 589 | 0.80 % | 0.95 % |
