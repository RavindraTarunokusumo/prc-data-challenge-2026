# LTFM weather: coverage and event months (target-free)

*Written 2026-10-07T19:25:54Z (D08-S03, laptop). INC-0019. Reads weather files only. No challenge file and no target was read.*

## Data

- **Source:** IEM ASOS archive (`mesonet.agron.iastate.edu`). The owner ran `scripts/fetch_weather.py` from the owner's terminal, because the session's network path resets these hosts (INC-0019 correction).
- **Manifest:** `data/manifests/weather_LTFM_manifest.json`.
  - 19 months, 2025-01 to 2026-07; 27,680 reports.
  - All 19 SHA-256 values were re-verified.
- **Cadence:** one report every 30 minutes (median and q99 gap 30 min; the largest gap is 90 min). No duplicate times.
- **Missing values:**
  - none in temperature, visibility, wind speed or precipitation;
  - `wxcodes` is empty in 84 % of reports (no present weather);
  - gusts are missing in 98.6 %;
  - ice accretion, peak wind and snow depth are always empty.

## Weather events by month (counts of half-hourly reports)

Columns:
- **snow:** `wxcodes` contains SN, SG or PL.
- **fog:** FG.
- **vis < 0.5 mi:** visibility below 0.5 statute miles.
- **TS:** thunderstorm.
- **≤ 0 °C:** temperature at or below freezing.

| Month | snow | snow days | fog | vis < 0.5 mi | TS | ≤ 0 °C |
|---|---|---|---|---|---|---|
| 2025-01 | 0 | 0 | 15 | 0 | 1 | 0 |
| **2025-02 (W1 validation)** | **258** | **12** | 29 | 20 | 9 | **135** |
| 2025-03 (W1 embargo) | 12 | 2 | 125 | 46 | 2 | 0 |
| 2025-04 | 2 | 1 | 123 | 68 | 3 | 0 |
| 2025-05 to 2025-10 | 0 | 0 | 0–9 | 0–4 | 0–10 | 0 |
| 2025-11 | 0 | 0 | 33 | 2 | 2 | 0 |
| 2025-12 (H, closed) | 17 | 4 | 1 | 0 | 7 | 12 |
| **2026-01 (ranking)** | **147** | **9** | 20 | 9 | 10 | **103** |
| 2026-07 (ranking) | 0 | 0 | 2 | 1 | 23 | 0 |

## Consequence for agenda item 3 (LTFM winter with weather)

1. **In 2025, LTFM snow falls almost only in February, which is W1's validation month.**
   - W1's training months hold 2 snow reports (April) and no report at or below 0 °C.
   - W1c trains on January only, which has no snow.
   - No development fold can learn a snow or freezing effect from its training months.
2. **S1 (July 2025) has no snow, fog-limited visibility or thunderstorm reports.**
   - A snow or freezing mechanism cannot reach S1, and criterion 2 needs an S1 WIN.
   - **A snow-only LTFM candidate therefore cannot meet criterion 2.**
3. **A SUBMIT fit (12 months, including February 2025) could learn a snow effect for January 2026 (9 snow days).** No development fold or H access would test it. It would be a forward bet of U6's type, which G7 and P4 do not allow as an upload ground.
4. **What stays testable on all folds:** weather that occurs in every season at every airport.
   - Above all, wind direction and speed, which set the runway configuration and therefore taxi distance.
   - Also visibility and precipitation.
   - This needs the other nine airports' reports. Their fetch is the owner's (INC-0019 network path).

## Design pilot result (2026-10-07T21:34:39Z; appended)

- **Run:** `scripts/pilot_weather_D08.py`, parameters and decision rule in `research/day-08/proposals/WX_pilot_params.yaml` (committed at d506516, before the pilot ran). Output: `research/day-08/eda/pilot_weather.json` and `.log`.
- **Model:** LightGBM (E045 / E020's configuration), FS2 against FS2 plus the 16 weather columns, on all ten airports.
- **Weather table:** `data/processed/weather_reports.parquet` (277,489 reports; manifest `data/manifests/weather_reports_manifest.json`). Coverage is 100 % of DEP rows at every airport.
- **Targets read:** the design months only (2025-01, 04, 05, 06), at row level, as in H038's pilot. No validation-month target and no December target was read.

| Pilot | Predicted month | Reference RMSE | With weather | Difference |
|---|---|---|---|---|
| P1 | 2025-06 | 373.26 | 374.69 | **+1.43** |
| P2 | 2025-05 | 327.05 | 326.57 | **−0.48** |

**Decision rule (pre-registered): not met.** It needed at least 1.0 s better in both pilots. Agenda item 3 is not pursued in Days 8–12, and no weather proposal is written.

Segment readings (reported only; the rule says they do not override it):
- **Bulk (y < 3,600 s):** −1.27 s (P1) and −1.17 s (P2).
- **Tail (y ≥ 3,600 s):** +71.61 s (P1, 395 rows) and +12.72 s (P2, 219 rows).
- **NM-missing rows:** +14.24 s and +2.05 s.
- **EHAM:** −10.62 s and −6.09 s.
- **LIRF:** +8.95 s and +2.02 s.
- **LTFM:** +2.41 s and +1.68 s.
- **Reading:** the weather columns help the ordinary rows a little, and the trees spend them on the few hundred tail rows, where they lose more. These readings are post hoc. A restricted weather candidate (bulk or NM-present only) would choose its population after seeing them, and would need its own proposal stating that selection (rule 10).

## Corrections (2026-10-07T22:12:16Z; X-D08-S03-0004)

- **D8-C17.** Consequence 1's "No development fold can learn a snow or freezing effect from its training months" is wrong as stated.
  - R1–R3, S1 and S1c train on February and March 2025 (270 LTFM snow reports).
  - W1 and W1c, the only folds whose validation month has snow, have 2 and 0 in training.
  - So **no fold can both learn and score a snow effect.** The consequence for criterion 2 is unchanged.
- **D8-C20.** The pilot section's restricted-candidate sentence is corrected by the review's finding 2. No implementable or oracle restriction reaches −1.0 s in both pilots:
  - bulk (oracle): −0.91 / −0.80 s;
  - NM-present: +0.17 / −0.63 s;
  - EHAM only: −0.61 / −0.36 s;
  - the four in-sample airports: −1.28 / −0.59 s.

  **Weather is not a lead.**
