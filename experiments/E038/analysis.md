# E038 analysis: H027 v2 (subsampled LightGBM twin of E029, seed 42), ladder component

**No claim of its own.** Development mean **442.03 s** (E029 442.46). Against E029, all rows: −0.42 s (q95 −0.06): WIN on R1, R3 and W1; TIE elsewhere; no airport beyond +3 %.

## Run

| Item | Value |
|---|---|
| Config | E029's with `feature_fraction` 0.8, `bagging_fraction` 0.8, `bagging_freq` 1, seed 42; all 8 folds; CLASS-M |
| Status | COMPLETE: 908.5 s (E029 893 s: subsampling gave no speed-up), 6.61 GB; run commit `1e01158` |
| Per fold | R1 442.70, R2 269.76, R3 395.27, S1 632.66, W1 469.76; S1c 636.98, W1c 486.71 |
| Integrity | `route_check.py E038 - E029`: PASS |

- **Freeze:** `git diff --stat 377143d <run commit> -- src scripts pyproject.toml uv.lock research/day-06/sessions/D06-S01/run_window.sh` is **empty** (anchor = the X-D06-S01-0002 submission commit).
- **Environment (rule L v2 item 6):** manifest `python` 3.13.15, `polars_threads` 16; no swap pages during the run; clean tree at the run.
- **Window (INC-0012):** run by the pinned launcher (`run_window.sh`, SHA-256 `9da5b0c3…cf6a4d`); log copied to `research/day-06/sessions/D06-S01/run_window.log`. Ended before 21:30: no deviation.
- **Role:** control (batch X-D06-S01-0002); no candidate; never NEW (X-D06-S01-0001 ruling); ledger decision null.
- **One draw** where a GPU component is involved (rule 13 wording); the bootstrap excludes the draw.
- Deterministic (LightGBM `deterministic=True`); not a GPU draw. Its floor is "at seed 42".

## Diversity (E029 against E038)

On `NM_present_excl_LIRF`: residual correlation 0.977–0.980; RMSE −0.70 s against E029; RMS disagreement 46 s (E031: 81 s; E030: 93 s). All rows 0.983–0.996; bulk 0.971–0.975. As intended: as accurate as E029, about half the CatBoost halves' disagreement.

- **Missed prediction:** residual correlation expected 0.995–0.999 on all rows and 0.98–0.995 bulk; realised lower (more diverse than expected). Runtime expected 600–850 s; realised 908.5 s, inside the 1,100 s guard.
