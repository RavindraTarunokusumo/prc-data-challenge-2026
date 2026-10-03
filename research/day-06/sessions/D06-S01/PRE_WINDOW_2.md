# D06-S01 pre-window record, batch 2 (H029–H030; N1, N2)

*Written 2026-10-03T08:47:04Z (measured). The GPU line at arming is appended just before arming.*

- **N1.** Allocations: H029 v1 → **E040**, H030 v1 → **E041** (purpose `primary`; each `gate.json` names its hypothesis and v1). E040's `config.yaml` equals `experiments/E031/config.yaml` apart from `hypothesis_id` and `proposal_version` (parsed YAML), and equals the H029 block; E041's equals the H030 block apart from the header fields. `check_config` accepts both.
- **Launcher:** `research/day-06/sessions/D06-S01/run_window_2.sh`, SHA-256 `edfe11dfd7e5f690a722fd05e5050213fbede60b3a8ede00355c8a3e08dadf3e`. Diff against `run_window.sh`: header comment, date (2026-10-03), log name (`runtime/run_window_D06-S01_2.log`) and queue (`E040 1600 -`, `E041 60 E040`) only.
- **Freeze diff** `git diff --stat 9d245c0 -- src scripts pyproject.toml uv.lock config research/day-06/eda/d06_diagnostics.py research/day-06/sessions/D06-S01/run_window_2.sh`: **empty**.
- **Environment (rule L v2 item 6):** CPython 3.13.15; polars thread pool 16; numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, polars 1.44.2, LightGBM 4.7.0, CatBoost 1.2.10; `uv.lock` `efa4fd78eaa6`; boot `cf2c705b…`; RAM 10,951 MiB, swap 4 GiB.
- **GPU:** NVIDIA GeForce RTX 5060 Laptop GPU, driver 591.91, CUDA 13.1; 673 MiB of 8,151 MiB in use at this writing.
- **E040's overrun bound: the CLASS-L timeout of 8,100 s** (replacing INC-0012's 2,700 s for this run). In the worst case E040, started at 21:00, could run to about 23:15 local; the launcher never kills a run, and any run still executing at 21:30 is reported as an INC-0012 deviation with its end time.
- **Arming:** close to the window (recommended in the review), by a one-shot session schedule at about 20:43 local. If the session is not running then, the batch is not armed and the runs count as deferred (N3).
