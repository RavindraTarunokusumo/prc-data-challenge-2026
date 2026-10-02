# E035 analysis: H026 v2 (equal-weight blend of E029 and the integer-codes CatBoost E030), ladder rung B

**Reading: "the categorical statistics carry part of the blend's gain" (at equal weight).** D(H026) = +1.34 s (q95 +1.65) on `NM_present_excl_LIRF`, LOSS on 5 of 5 development folds. Not carried by W1 alone.

## Run

| Item | Value |
|---|---|
| Config | `blend`, [E029, E030], [0.5, 0.5], seed 42, all 8 folds, CLASS-S |
| Status | COMPLETE: 11.7 s, 3.37 GB; run commit `48e633b` |
| Development mean | 440.68 s |
| Integrity | `route_check.py E035 - E029`: PASS (8 folds) |

- **Freeze:** `git diff --stat 377143d <run commit> -- src scripts pyproject.toml uv.lock research/day-06/sessions/D06-S01/run_window.sh` is **empty** (anchor = the X-D06-S01-0002 submission commit).
- **Environment (rule L v2 item 6):** manifest `python` 3.13.15, `polars_threads` 16; no swap pages during the run; clean tree at the run.
- **Window (INC-0012):** run by the pinned launcher (`run_window.sh`, SHA-256 `9da5b0c3…cf6a4d`); log copied to `research/day-06/sessions/D06-S01/run_window.log`. Ended before 21:30: no deviation.
- **Role:** control (batch X-D06-S01-0002); no candidate; never NEW (X-D06-S01-0001 ruling); ledger decision null.
- **One draw** where a GPU component is involved (rule 13 wording); the bootstrap excludes the draw.
- **Attestation:** H026's acknowledgement attests that no E029 + E030 blend figure was computed before the run.

## Readings (H024 v2 §Batch)

| Contrast (`NM_present_excl_LIRF`) | Mean | q95 | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|---|---|
| G = E035 − E029 | −2.62 | −2.06 | −2.75 W | −2.81 W | −2.97 W | −5.03 W | +0.44 T | −7.19 W | −5.28 W |
| **D = E035 − E033** | **+1.34** | +1.65 | +1.16 L | +1.66 L | +1.06 L | +0.78 L | +2.03 L | +0.10 T | +3.01 L |

| Contrast (all rows, `compare.py`) | Mean | q95 | Folds |
|---|---|---|---|
| E035 − E029 | −1.77 | −1.17 | 6 WIN, W1 TIE; no airport beyond +3 % |
| E035 − E033 | +1.81 | +2.30 | 6 LOSS, S1c TIE; no airport beyond +3 % |

- **Rung B keeps 66 % of E033's gain on normal taxis** (−2.62 of −3.96 s) and 49 % on all rows (−1.77 of −3.58).
- At E033's construction, the codes CatBoost is no substitute; this includes its weaker accuracy (below).

## Diversity (E029 against E030; `research/day-06/eda/diversity_E029.json`)

On `NM_present_excl_LIRF`, development folds: residual correlation 0.904–0.926 (E031: 0.925–0.940); E030's RMSE is +4.62 s above E029's (E031: −0.30 s); RMS disagreement 93 s (E031: 81 s). **E030 disagrees with E029 more than E031 does, but is less accurate.** The gain that the statistics add in the blend runs through the CatBoost half's accuracy, not through extra disagreement.

## Rule 12 (bands, 5 development folds, `NM_missing_other` bulk)

< 1 h 29, 1–3 h 3, > 3 h 6 (E033: 82, 4, 3). Disclosure only.
