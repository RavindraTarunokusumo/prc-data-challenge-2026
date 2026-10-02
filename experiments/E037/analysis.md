# E037 analysis: H025 v2 (equal-weight blend of E029 and the complexity-1 CatBoost E036), ladder rung C

**Reading: "the CTR combinations carry part of the blend's gain" (at equal weight).** D(H025) = +1.65 s (q95 +1.98) on `NM_present_excl_LIRF`, LOSS on 5 of 5 development folds. **Disclosure (C6):** E036's resolved parameters differ from E031's in `data_partition` (DocParallel against FeatureParallel) as well as the treatment.

## Run

| Item | Value |
|---|---|
| Config | `blend`, [E029, E036], [0.5, 0.5], seed 42, all 8 folds, CLASS-S |
| Status | COMPLETE: 10.4 s, 3.40 GB; run commit `563891b` |
| Development mean | 440.04 s |
| Integrity | `route_check.py E037 - E029`: PASS |

- **Freeze:** `git diff --stat 377143d <run commit> -- src scripts pyproject.toml uv.lock research/day-06/sessions/D06-S01/run_window.sh` is **empty** (anchor = the X-D06-S01-0002 submission commit).
- **Environment (rule L v2 item 6):** manifest `python` 3.13.15, `polars_threads` 16; no swap pages during the run; clean tree at the run.
- **Window (INC-0012):** run by the pinned launcher (`run_window.sh`, SHA-256 `9da5b0c3…cf6a4d`); log copied to `research/day-06/sessions/D06-S01/run_window.log`. Ended before 21:30: no deviation.
- **Role:** control (batch X-D06-S01-0002); no candidate; never NEW (X-D06-S01-0001 ruling); ledger decision null.
- **One draw** where a GPU component is involved (rule 13 wording); the bootstrap excludes the draw.

## Readings

| Contrast (`NM_present_excl_LIRF`) | Mean | q95 | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|---|---|
| G = E037 − E029 | −2.31 | −1.69 | −2.89 W | −3.37 W | −2.99 W | −4.50 W | +2.22 L | −6.39 W | −7.07 W |
| **D = E037 − E033** | **+1.65** | +1.98 | +1.01 L | +1.09 L | +1.04 L | +1.31 L | +3.81 L | +0.90 L | +1.21 L |

| Contrast (all rows) | Mean | q95 | Folds |
|---|---|---|---|
| E037 − E029 | −2.41 | −1.94 | 7 WIN; no airport beyond +3 % |
| E037 − E033 | +1.17 | +1.50 | 7 LOSS; no airport beyond +3 % |

- Rung C keeps 58 % of E033's gain on normal taxis (−2.31 of −3.96 s) and 67 % on all rows.
- **Population split:** on normal taxis rung C is *worse* than rung B (D +1.65 against +1.34); on all rows it is better (E037 − E035 = −0.64 s from the two all-rows means). The per-key statistics help on rows outside `NM_present_excl_LIRF`.
- **Missed predictions:** D expected +0.1 to +1.4 (central +0.6); the Advisor's v2 forecast put "rung C carries" at P 0.60. Realised: "combinations carry part".

## Rule 12 (bands)

< 1 h 73, 1–3 h 4, > 3 h 2 (E033: 82, 4, 3).
