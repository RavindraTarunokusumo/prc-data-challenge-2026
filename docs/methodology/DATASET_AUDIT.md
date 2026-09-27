# Dataset Audit and Prediction-Time Availability Audit (Day 1)

**Session:** D01-S01 · **Version:** 2 (revised after review X-D01-S01-0001) · **Status:** draft for the split-freeze review (becomes normative once the freeze commit lands)
**Evidence:** `research/day-01/audit/audit_stats.json`, produced by `uv run python scripts/audit_dataset.py` from bronze data only (raw manifest re-verified at session start, 14/14 SHA-256 match). It is a pre-freeze audit that includes December; see §6.6. Seasonal and regime evidence: `research/day-01/audit/regime_stats.json`, from `scripts/audit_regimes.py`, which excludes December targets.
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

**Prediction timestamp:** the release of the ranking snapshot, i.e. after the end of the test months. For a scored DEP row in ranking month *M* (Jan 2026 or Jul 2026), the admissible information set is:

1. all training files (Jan–Dec 2025) in full;
2. every column of every ranking row **of the same month *M*** **except** `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt` of DEP rows. This covers the row itself, other DEP rows (takeoff times, runways, stands, NM times) and ARR rows in full.

**Cross-month information is inadmissible.** January 2026 predictions may not use July 2026 rows, and vice versa, because no development fold can validate a feature that pools two test months. This is enforced structurally: the final folds `SUBMIT_JAN` and `SUBMIT_JUL` each contain a single ranking month, so the other month is absent from the masked view.

**Inadmissible as model inputs:** the two blanked DEP columns (and anything derived from them within the evaluated period); `MVT_ID_mvt` and `FLIGHT_ID_mvt`. The identifiers may serve as **join keys** (for example, linking a DEP row to the ARR row of the same flight) but never as model inputs. Within an airport-day their order is only weakly associated with time (median Spearman ≈ 0.34 against scheduled, takeoff and block times alike, with large variation between airports). The pooled rank-gap test (correlation −0.008 with the target) cannot exclude structure within subgroups. The exclusion rests on the fact that an identifier carries no mechanism, not on that test.

**Information labels (mandatory in every proposal).** Each feature is labelled by the latest instant at which any of its inputs becomes known. The instant is measured relative to two reference instants of the row itself: its off-block time *t_off* (the operational prediction instant for taxi-out, i.e. pushback) and its takeoff *t_to*.

| Label | Known… | Examples |
|---|---|---|
| **P** (pre-off-block) | at or before *t_off* | airport, stand, aircraft type, operator, schedule and flight-plan times (`SCHED`, `EOBT_1`, `IOBT`, `LOBT`), `AOBT_3` (an estimate of *t_off*), cross-row events that occurred before *t_off* |
| **T** (in-taxi) | in (*t_off*, *t_to*] | the row's **own takeoff time** and anything derived from it (`MVT − AOBT_3`, takeoff hour), other movements during the row's own taxi interval (departures ahead on the same runway, arrivals crossing) |
| **F** (post-takeoff) | after *t_to* | `ARVT_3`, later movements at the airport |

- **Precedence.** A feature takes the latest label among its inputs (F > T > P).
- **Proxy for *t_off*.** The true *t_off* is withheld, so labelling uses `AOBT_3_flt`, then `EOBT_1_flt`, then `SCHED_TIME_UTC_mvt`, whichever is first available. Features whose label depends on this proxy must say so.
- **Runway.** The departure runway (`RUNWAY_mvt`) is labelled P, on the assumption that it is assigned before pushback. It is recorded after the fact, so proposals that depend on runway identity must note the assumption.
- **Admissibility.** All three labels are admissible under this section. The labels exist so that Days 5–7 can report a **causal-only variant**, restricted to P-labelled features, and so that the Advisor can weigh T and F features, which are the most target-revealing.

### 6.3 Target proxies in the admissible set (not leaks, but strong features)

Differences between the row's takeoff and its NM off-block times, over training DEP rows (pre-freeze statistics, December included; see §6.6):

| Proxy for the target | Coverage | RMSE (s) | Median \|error\| (s) |
|---|---|---|---|
| constant mean | 100 % | 546.4 | 241 |
| `MVT − AOBT_3_flt` | 98.9 % | **384.9** | 175 |
| `MVT − EOBT_1_flt` | 98.9 % | 676.7 | 303 |
| `MVT − LOBT_flt` / `− IOBT_flt` | 98.9 % | 740 | 359 |
| `MVT − SCHED_TIME_UTC_mvt` | 100 % | 2,412.7 | 481 |

`AOBT_3_flt` is **not** a copy of the withheld off-block time.
- `BLOCK − AOBT_3` has median +51 s, IQR −122…+183 s and a 1–99 % range of −1,194…+803 s.
- `AOBT_3_flt` itself is whole-minute in 97.7 % of rows.
- The review X-D01-S01-0001 verified that it lies within 1 s of the true block time in only 2.0 % of rows (whole-minute values) or 0.5 % (values with seconds). Those are coincidences.
- Linked ARR rows carry no copy of the DEP block time.

It is a noisy NM-side estimate: admissible, label P, and the obvious anchor. `MVT − AOBT_3` is label **T**, because it uses the row's takeoff. Any proposal that uses it must show whether gains come from a mechanism or from reconstructing the anchor.

### 6.4 Validation masking protocol (mandatory)

Validation must reproduce the ranking information set. For a fold with training months *T* and validation months *V*:

- Feature-building input is `masked_view(fold)`: rows of *T* in full, plus rows of *V* with DEP `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt` set to null. ARR rows of *V* stay complete, as in ranking.
- Rows from months that are neither in *T* nor in *V* for that fold (the protected holdout, embargo months) are **absent** from the view.
- Target statistics and fitted transforms use only DEP rows of *T* (DATA_POLICY §5, §9).
- Feature and model code may not import truth-reading or data-loading code (`tests/test_isolation.py`). Only `prc.evaluate` reads validation truth, and it verifies silver and each fold's row count against `config/splits.yaml: evaluation_population` itself.
- `tests/test_masking.py` asserts on real silver that no validation DEP row exposes a block or taxi value to feature code.

### 6.5 Known asymmetries between validation and the real test

- **Jul 2026 gap.** For Jul 2026 the most recent training data is 6 months old, and no Jan–Jun 2026 data exists. No 2025 fold can reproduce both a 6-month gap and a prior-year same-season month. S1 approximates the season and does not reproduce the gap. Features that depend on the freshest targets must declare their staleness sensitivity (from Day 3 onward).
- **LFPG runway regime (temporary, Aug–Nov 2025).** Evidence: `regime_stats.json`, plus target-free runway shares.
  - 27L and 09R carried 30.2 % and 13.6 % of LFPG departures in June 2025, 14.2 % and 6.7 % in July, and **0 %** in Aug–Nov. 27R and 09L took over: 27R rose from 0.2 % in June to 16.1 % in July and 15–24 % in Aug–Nov.
  - The LFPG median taxi-out rose from 895 s in June to 962 s in July and 1,012–1,015 s in Aug–Nov.
  - The configuration partly reverts in December, and **both ranking months use the Jan–Jun layout again**: 27L carries 29.5 % in Jan 2026 and 20.4 % in Jul 2026, while 27R carries 0.0 % and 0.1 %.
  - Consequences:
    1. S1's post-validation training months (Sep–Nov) expose a regime that starts inside the validation month and is absent from both test months. The causal twin S1c controls for this (`splits.yaml: promotion.criterion_2`).
    2. R1–R3 validate LFPG on a configuration that does not occur in the test months.
- **Winter.** January is 44.3 % of scored rows. Evidence from `regime_stats.json`, which excludes December:
  - Jan–Feb 2025 has a heavier upper tail than the v1 development validation months (Jul, Sep–Nov). The p90 difference is +253 s at EDDM, +166 s at LTFM, +98 s at LSZH, +88 s at EHAM and +66 s at LFPG. It is negative at EGLL, LEBL, LEMD and LIRF.
  - 12 of the 21 disrupted airport-days in Jan–Nov (days whose median exceeds the airport's typical daily median by more than 300 s) fall in Jan–Feb. The v1 development validation months hold 6.
  - Hence the winter fold W1 (validates Feb 2025) and its causal twin W1c, whose training data is only Jan 2025 and which is a small-sample diagnostic.
- **Month edges.** In ranking, 1 Jul 2026 rows have no 30 Jun context, while 1 Jan 2026 rows do (31 Dec 2025 is in training). Validation months always have their previous month available. Cross-row windows are minutes to hours long, so this affects only the first hours of a month.
- **NM match rate.** 1.5 % of ranking DEP rows lack `_flt` data, vs 1.1 % in training. Models must handle missing `AOBT_3`.

### 6.6 Protected-holdout scope (stated plainly)

- **Before the freeze.** The Day 1 audit (`audit_stats.json`: target quantiles, tail shares, proxy RMSEs, per-airport std) and the SPLITS v1 fold table read **December targets at distribution level**. The v1 test suite also scored real December truth with random predictions. H is therefore not pristine: its marginal target distribution is known. No model has been fitted, tuned or scored on it.
- **From the freeze onward:**
  - `prc.data.load_silver` nulls December DEP block times and targets by default. Only final (SUBMIT) training may unmask them, and that is logged.
  - `scripts/audit_dataset.py` refuses to run.
  - No EDA, audit or test reads December targets. The holdout tests use synthetic truth.
  - The only reader is `evaluate.holdout_compare`. It takes the phase from the experiment's gate record, enforces `max_access_per_phase` against the append-only task ledger, logs the access before reading, and returns aggregates only.

## 7. Implications for Day 1

1. Silver keeps every row and value (tail included), casts IDs to integers and adds no derived targets.
2. RMSE on all rows of each frozen fold, with no clipping in the metric. Per-airport RMSE on rows below 3,600 s is reported as a diagnostic, because LIRF's tail (std 1,332 s) makes the airport tolerance insensitive to degradation in the bulk.
3. Tier 0 baselines will be tail-bound. Report RMSE by taxi-time band so tail effects are visible. Promotion requires bootstrap-significant gains (`splits.yaml: promotion`).
4. `MVT − AOBT_3` gives a proxy baseline at 385 s on training rows. Any model should be compared against it.
