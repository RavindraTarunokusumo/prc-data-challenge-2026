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
