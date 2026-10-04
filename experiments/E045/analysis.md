# E045 analysis: H034 v1 (E020's configuration, unrouted LightGBM on FS2; the laptop instance; component of H035)

**Outcome: COMPLETE; reproduces E020 exactly.** Per-fold RMSE equals E020's to 0.000000 s on all seven scored folds (R1 284.67, R2 248.97, R3 300.02, S1 420.73, W1 355.37, S1c 440.87, W1c 441.90). Component only: never a candidate, never NEW (U5; rule 10 bars E020's configuration and its re-draws as a candidate). No ledger decision.

| Item | Value |
|---|---|
| Status | COMPLETE: 1,195.8 s, peak RSS 5.38 GB, within CLASS-M; swap-out 0 |
| Window (INC-0015) | started 00:00:08Z, finished 00:20:06Z; launcher END 00:21:52Z (failed W&B sync, CommError; **not mirrored**, INC-0009) |
| Tree | `git_dirty_at_run: false`; no WARNING after its checkpoint; no unmasking event (U4) |
| Freeze | `git diff --stat 76e80f1 3eccc98 -- src scripts config pyproject.toml uv.lock research/day-07/sessions/D07-S01/run_window_2.sh`: empty |
| Reproduction | E047 (seed 43): all 8 prediction files byte-identical (SHA-256) |

- **Missed:** runtime 1,195.8 s against the 13–17 min forecast (upper end 1,020 s) and above the 1,100 s window guard; peak RAM 5.38 GB against 6.3–6.8 GB (lower than forecast). E020 took 1,181 s in the cloud; the laptop did not run faster here.
