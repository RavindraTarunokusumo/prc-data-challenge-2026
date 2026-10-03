# E039 analysis: H028 v2 (equal-weight blend of E029 and its LightGBM twin E038), ladder rung A

**Reading: "a perturbation twin of E029, at its measured disagreement, does not reproduce the gain; G(H028) = −1.53 s on normal taxis is the generic-averaging floor at that disagreement (seed 42)."** D(H028) = +2.43 s (q95 +2.99), LOSS on 4 of 5 development folds (W1 TIE). This is **not** support for "a second learner family adds signal" (X-D06-S01-0001 ruling).

## Run

| Item | Value |
|---|---|
| Config | `blend`, [E029, E038], [0.5, 0.5], seed 42, all 8 folds, CLASS-S |
| Status | COMPLETE: 14.3 s, 3.41 GB; run commit `2a7d2b2` |
| Development mean | 441.44 s |
| Integrity | `route_check.py E039 - E029`: PASS |

- **Freeze:** `git diff --stat 377143d <run commit> -- src scripts pyproject.toml uv.lock research/day-06/sessions/D06-S01/run_window.sh` is **empty** (anchor = the X-D06-S01-0002 submission commit).
- **Environment (rule L v2 item 6):** manifest `python` 3.13.15, `polars_threads` 16; no swap pages during the run; clean tree at the run.
- **Window (INC-0012):** run by the pinned launcher (`run_window.sh`, SHA-256 `9da5b0c3…cf6a4d`); log copied to `research/day-06/sessions/D06-S01/run_window.log`. Ended before 21:30: no deviation.
- **Role:** control (batch X-D06-S01-0002); no candidate; never NEW (X-D06-S01-0001 ruling); ledger decision null.
- **One draw** where a GPU component is involved (rule 13 wording); the bootstrap excludes the draw.

## Readings

| Contrast (`NM_present_excl_LIRF`) | Mean | q95 | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|---|---|
| G = E039 − E029 | −1.53 | −1.30 | −1.12 W | −1.33 W | −1.30 W | −1.46 W | −2.45 W | −2.16 W | −2.93 W |
| **D = E039 − E033** | **+2.43** | +2.99 | +2.78 L | +3.14 L | +2.73 L | +4.34 L | −0.86 T | +5.13 L | +5.36 L |

| Contrast (all rows) | Mean | q95 | Folds |
|---|---|---|---|
| E039 − E029 | −1.02 | −0.82 | 7 WIN |
| E039 − E033 | +2.57 | +3.36 | 7 LOSS; LFPG +3.9 % against E033 |

- **The averaging floor is larger than predicted:** G expected −0.2 to −1.2 s; realised −1.53 s (39 % of E033's gain on normal taxis; 28 % on all rows). Generic averaging at half the disagreement buys a real part of the gain; the rest needs E031.
- On W1 the twin's blend is level with E033 (−0.86 s, TIE).

## Appended correction (D6-C9)

*Appended at the Day 6 phase close (X-D06-S01-0004; `research/day-06/acks/PHASE_CLOSE_D06_ack_v1.md`). The text above is unchanged.*
- **D6-C9:** "the rest needs E031" is withdrawn (no necessity claim). The reading is: a perturbation twin of E029 at its measured disagreement does not reproduce the gain; the averaging floor is −1.53 s at seed 42. It holds against every champion draw (E034 +2.16 s, E041 +2.06 s).
