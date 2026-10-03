# E036 analysis: H024 v2 (routed CatBoost GPU, CTRs at complexity 1), ladder component

**Own reading: INCONCLUSIVE by the pre-registered closed exempt set** (`data_partition` differs from E031 on every fold). The values, recorded for disclosure: E036 − E031 = **+4.96 s** (q95 +5.62) on `NM_present_excl_LIRF`, LOSS on 5/5; E036 − E030 = **+0.04 s** (q95 +0.90).

## Run

| Item | Value |
|---|---|
| Config | E031's with `max_ctr_complexity: 1`; seed 42; all 8 folds; CLASS-M |
| Status | COMPLETE: 353.6 s (E031 1,523 s), 6.73 GB; run commit `2657659` |
| Development mean | **444.46 s**: R1 445.06, R2 272.24, R3 397.22, S1 632.22, W1 475.56; S1c 635.34, W1c 492.89 |
| Integrity | `route_check.py E036 - E029`: PASS |
| GPU | device-wide peak 7,323 MiB against 5,150 MiB at start; about 2.2 GB attributable to the run. **Disclosure:** some GPU memory (4.3–5.2 GB) was held throughout the window by a process outside the WSL VM's view (idle was 921 MiB at the session start); no GPU failure occurred |

- **Freeze:** `git diff --stat 377143d <run commit> -- src scripts pyproject.toml uv.lock research/day-06/sessions/D06-S01/run_window.sh` is **empty** (anchor = the X-D06-S01-0002 submission commit).
- **Environment (rule L v2 item 6):** manifest `python` 3.13.15, `polars_threads` 16; no swap pages during the run; clean tree at the run.
- **Window (INC-0012):** run by the pinned launcher (`run_window.sh`, SHA-256 `9da5b0c3…cf6a4d`); log copied to `research/day-06/sessions/D06-S01/run_window.log`. Ended before 21:30: no deviation.
- **Role:** control (batch X-D06-S01-0002); no candidate; never NEW (X-D06-S01-0001 ruling); ledger decision null.
- **One draw** where a GPU component is involved (rule 13 wording); the bootstrap excludes the draw.

## Closed exempt set (C6; written before any H024/H025 reading)

`research/day-06/eda/closed_set_E036_vs_E031.json` (code `research/day-06/eda/d06_diagnostics.py`, SHA-256 `5fc21113…10b7`). Every fold: 56 keys equal, none in one arm only, two differ:
- `max_ctr_complexity` 1 against 4 (the treatment);
- **`data_partition`: `DocParallel` against `FeatureParallel`** (CatBoost's own GPU choice, presumably from the much smaller feature count). Outside the set: **violation**. H024's own reading is INCONCLUSIVE (pre-registered), and rung C (E037) carries this disclosure.

## Values (disclosure; not a reading)

| Contrast (`NM_present_excl_LIRF`) | Mean | q95 | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|---|---|
| E036 − E031 | +4.96 | +5.62 | +3.50 L | +3.98 L | +3.80 L | +4.43 L | +9.08 L | +3.37 L | +3.79 L |
| E036 − E030 | +0.04 | +0.90 | −0.81 W | −2.01 W | −0.60 W | +0.36 T | +3.27 L | +1.07 L | −3.41 W |

- All rows: E036 − E029 +2.01 s (q95 +3.23); LOSS on R1, R2, R3, W1, W1c; EDDM, LEMD and LSZH degrade beyond +3 %.
- **Plain reading of the values:** on normal taxis, per-key statistics alone recover none of E031's −4.91 s advantage over the codes arm; the combinations hold all of it. The magnitude is far beyond the 1.5 s threshold and the 0.68 s re-draw, but the closed-set violation means it is not a pre-registered reading.
- **Missed prediction:** E036 − E031 expected +0.5 to +3.5 s (Advisor +0.2 to +3.0); realised +4.96.

## Appended correction (D6-C7, D6-C8)

*Appended at the Day 6 phase close (X-D06-S01-0004; `research/day-06/acks/PHASE_CLOSE_D06_ack_v1.md`). The text above is unchanged.*
- **D6-C8:** "the combinations hold all of it" is withdrawn. Values only: E036 − E031 +4.96 s and E036 − E030 +0.04 s on normal taxis are **consistent with** the combinations carrying E031's advantage, but **not separated from `data_partition`** (E036 DocParallel, E031 FeatureParallel). H024's own reading is INCONCLUSIVE.
- **D6-C7:** the partition follows the CTR configuration, not GPU memory (E030 and E031 both started at 853 MiB). The external holder during E036 is therefore an unlikely cause, though not excluded.
