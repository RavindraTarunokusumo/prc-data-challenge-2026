# Dataset Audit and Prediction-Time Availability Audit (Day 1)

**Session:** D01-S01 · **Status:** draft for the split-freeze review (becomes normative once the freeze commit lands)
**Evidence:** `research/day-01/audit/audit_stats.json`, produced by `uv run python scripts/audit_dataset.py` from bronze data only (raw manifest re-verified at session start, 14/14 SHA-256 match).
**Official column definitions:** <https://prc-data-challenge-2026.netlify.app/data.html> (read 2026-09-27; team and ranking pages not opened).

## 1. Shape and coverage

| Item | Value |
|---|---|
| Training rows (Jan–Dec 2025) | 4,167,797 (DEP 2,085,047 · ARR 2,082,750) |
| Ranking rows (Jan + Jul 2026) | 689,534 (DEP 344,841, the scored rows) |
| Airports | 10 (EDDF, EDDM, EGLL, EHAM, LEBL, LEMD, LFPG, LIRF, LSZH, LTFM); every DEP row departs from one of them |
| Columns | 30, same schema in training and ranking |
| DEP volume | Seasonal. July runs above January at every airport, by about 7 % at capacity-capped EGLL and by up to about 40 % at EDDF/EDDM. Jan 2026 and Jul 2026 volumes match Jan 2025 and Jul 2025 closely (`dep_by_month_airport`) |

## 2. Target

`TAXITIME_SEC_mvt = MVT_TIME_UTC_mvt − BLOCK_TIME_UTC_mvt`, in seconds, for DEP rows. This identity holds on 100 % of training DEP rows.

| Statistic | Value (s) |
|---|---|
| Mean / std | 991.2 / 546.4 |
| Quantiles 1 % · 25 % · 50 % · 75 % · 99 % | 291 · 719 · 912 · 1188 · 2339 |
| 99.9 % / max | 4,501 / 131,167 (36 h) |
| ≤ 0 s / < 60 s | 388 / 1,105 rows |
| > 1 h / > 2 h / > 24 h | 4,126 / 584 / 15 rows |

**The tail dominates RMSE.** Under a constant-mean predictor, the top 0.1 % of rows by squared error contribute **46.6 %** of the total SSE, and the top 1 % contribute 58.1 %. Most of this sits in physically implausible records (negative times, taxi-outs of several hours to 36 h). Silver keeps them. The evaluation population stays fixed at all rows (DATA_POLICY §10). Any capping, down-weighting or robust loss is a modelling decision and must go through review (DATA_POLICY §8).

Per-airport standard deviations run from 302 s (EDDM) to **1,332 s (LIRF)**. LIRF's tail is extreme, so it will dominate airport-level RMSE comparisons. EGLL has the highest median (1,319 s). Monthly medians are stable (902–948 s). Monthly std varies from 436 to 745 s (July is highest), and those differences are driven by the tail.

## 3. Missingness

- Movement columns (`_mvt`) are essentially complete. `AIRCRAFT_TYPE_mvt` is null in 0.1 % of rows, and `RUNWAY_mvt` is the literal `NA` in 36 DEP rows.
- NM flight columns (`_flt`) are null as a block when the movement did not match an NM flight: 1.1 % of training DEP rows and **1.5 % of ranking DEP rows** (a small shift). `FLIGHT_ID_mvt` is null in the same rows.
- Ranking DEP rows: `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt` are 100 % null (blanked by design). No other column is blanked. Ranking ARR rows are complete.

## 4. Consistency ("real data is messy")

`ADES_mvt ≠ ADES_flt` in 29,160 DEP rows. `AIRCRAFT_TYPE_mvt ≠ AIRCRAFT_TYPE_flt` in 7,013. 2,070 rows are diverted (`ADES_FILED_flt ≠ ADES_flt`), and 6 `FLIGHT_ID`s are duplicated. `ADEP_mvt = ADEP_flt` always. `MVT_ID_mvt` is unique. `SCHED_TIME` is minute-resolution. `AOBT_3_flt` is minute-resolution in 97.7 % of rows, while the true off-block time is second-resolution. Silver keeps all of these unchanged.

## 5. Category coverage (ranking DEP vs training DEP)

| Column | Train levels | Ranking DEP rows with a level unseen in training |
|---|---|---|
| RUNWAY_mvt | 53 | 0.00 % |
| STAND_mvt | 1,899 | 0.08 % |
| AIRCRAFT_TYPE_mvt | 269 | 0.01 % |
| AIRCRAFT_OPERATOR_flt | 676 | 0.05 % |
| ADES_mvt | 1,568 | 0.05 % |
| FLIGHT_mvt | 45,717 | **21.1 %** (flight numbers churn, so they are a poor identity key) |

Runway, stand, type and operator vocabularies are stable into 2026, so the test months do not require cold-start handling for these.

## 6. Prediction-time availability

### 6.1 What the competition makes available

The ranking file is a **retrospective snapshot** of Jan and Jul 2026. For a scored DEP row it contains the row's own **actual takeoff time** (`MVT_TIME_UTC_mvt`), its runway and stand, the NM actual off-block estimate (`AOBT_3_flt`), and the NM flown arrival time (`ARVT_3_flt`). It also contains every other movement of both months, including arrivals with complete block and taxi-in times. Only `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt` of DEP rows are withheld.

An operational "predict at off-block" timestamp is therefore not what the competition asks. At off-block the takeoff time would be unknown, yet the ranking file provides it. At takeoff the off-block time would be known, yet the file withholds it. No single wall-clock instant reproduces the ranking file's information set, so admissibility must be defined by the **information set** itself.

### 6.2 Definition (normative after freeze)

**Prediction timestamp:** the release of the ranking snapshot, i.e. after the end of the test months. For a scored DEP row, the admissible information set is:

1. all training files (Jan–Dec 2025) in full;
2. every column of every ranking row **except** `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt` of DEP rows, which covers the row itself, other DEP rows (takeoff times, runways, stands, NM times) and ARR rows in full.

**Inadmissible as model inputs:** the two blanked DEP columns (and anything derived from them within the evaluated period); `MVT_ID_mvt` and `FLIGHT_ID_mvt`, which are identifiers. They follow schedule order within an airport-day (median Spearman 0.344 vs `SCHED`, 0.343 vs takeoff), and the ID-rank minus takeoff-rank gap has correlation −0.008 with the target, so they carry no off-block signal. They are still excluded, because an identifier carries no mechanism.

**Temporal direction label (mandatory in proposals).** Every cross-row feature is labelled **backward** (uses events at or before the row's takeoff), **forward** (uses events after it) or **static**. Forward features are admissible under 6.2 because the snapshot contains them. They must still be labelled, so that Days 5–7 can report a causal-only variant and the Advisor can judge them.

### 6.3 Target proxies in the admissible set (not leaks, but strong features)

Differences between the row's takeoff and its NM off-block times, over training DEP rows:

| Proxy for the target | Coverage | RMSE (s) | Median \|error\| (s) |
|---|---|---|---|
| constant mean | 100 % | 546.4 | 241 |
| `MVT − AOBT_3_flt` | 98.9 % | **384.9** | 175 |
| `MVT − EOBT_1_flt` | 98.9 % | 676.7 | 303 |
| `MVT − LOBT_flt` / `− IOBT_flt` | 98.9 % | 740 | 359 |
| `MVT − SCHED_TIME_UTC_mvt` | 100 % | 2,412.7 | 481 |

`AOBT_3_flt` is **not** a copy of the withheld off-block time. `BLOCK − AOBT_3` has median +51 s, IQR −122…+183 s and a 1–99 % range of −1,194…+803 s, and 97.7 % of `AOBT_3` values are whole minutes. It is a noisy NM-side estimate. By 6.2 it is admissible, and it is the obvious anchor feature. The Advisor should still weigh one question in any proposal that uses it: whether gains come from a mechanism or from reconstructing the anchor.

### 6.4 Validation masking protocol (mandatory)

Validation must reproduce the ranking information set. For a fold with training months *T* and validation months *V*:

- Feature-building input is `masked_view(fold)`: rows of *T* in full, plus rows of *V* with DEP `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt` set to null. ARR rows of *V* stay complete, as in ranking.
- Rows from months that are neither in *T* nor in *V* for that fold (the protected holdout, embargo months) are **absent** from the view.
- Target statistics and fitted transforms use only DEP rows of *T* (DATA_POLICY §5, §9).
- A test (`tests/test_masking.py`) asserts that no validation DEP row exposes a block or taxi value to feature code.

### 6.5 Known asymmetries between validation and the real test

- **Jul 2026:** the most recent training data is 6 months old, and no Jan–Jun 2026 data exists. No 2025 fold can reproduce a 6-month gap and a prior-year same-season month at once. The seasonal fold (see `config/splits.yaml`) approximates the season and does not reproduce the gap.
- **Month edges:** in ranking, 1 Jul 2026 rows have no 30 Jun context, while 1 Jan 2026 rows do (31 Dec 2025 is in training). Validation months always have their previous month available, except when the previous month is embargoed. Cross-row windows are minutes to hours long, so this affects only the first hours of a month.
- **NM match rate:** 1.5 % of ranking DEP rows lack `_flt` data, vs 1.1 % in training. Models must handle missing `AOBT_3`.

## 7. Implications for Day 1

1. Silver keeps every row and value (tail included), casts IDs to integers and adds no derived targets.
2. RMSE on all rows of each frozen fold, with no clipping in the metric.
3. Tier 0 baselines will be tail-bound. Report RMSE by taxi-time band so tail effects are visible.
4. `MVT − AOBT_3` gives a proxy baseline at 385 s on training rows. Any model should be compared against it.
