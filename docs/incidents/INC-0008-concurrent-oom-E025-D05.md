---
schema: incident-v1
incident_id: INC-0008
type: infrastructure
created_utc: 2026-10-01T17:05:00Z
status: closed
---

# E025 killed by a global OOM caused by concurrent researcher side work (D05-S03)

**Raised by:** the researcher, at the D05-S04 start.

## What happened

- 16:16:57Z: E025 (the H015 v2 reproduction, the Day 5 compute check) started on the laptop (WSL2, 11 GB, swap 0).
- About 16:19Z: while E025 ran, the researcher started `uv run pytest` on `tests/test_features_fs2.py` and `tests/test_features_fs1.py`. The latter's real-silver tests load the silver layer.
- 16:19:23Z: **global OOM.** Resident at the kill: E025 worker 4.14 GiB, pytest 3.46 GB, and the owner's other processes in the same VM (editor, notebook kernel, agent runtimes; one at 1.37 GB). The kernel killed the E025 worker. E025 had completed R1 (RMSE 446.40, equal to E019).
- The VM kept hitting OOM until a power-off at 16:33:09Z, which ended the researcher session (D05-S03). The next boot (`cf2c705b…`) started D05-S04.
- Evidence: `journalctl -b -1 -k` on the laptop (boot `71605e21…`).

## Cause

A researcher process error. The D05-S03 plan already said that nothing memory-heavy should run beside E025, but the feature tests were not recognised as memory-heavy. Claude Code runs commands in a sandbox with its own PID namespace, so the kernel's pid 1430 is the worker seen inside the sandbox as pid 1159.

## Handling

- **E025 is recorded as RESOURCE_FAILURE and not retried** (brief §4). The records were reconstructed from the kernel log because the runner died with its worker. The reproduction gets a new id.
- **Guard added (infrastructure, no frozen file touched):**
  - `scripts/run_experiment.py` holds an exclusive `flock` on `runtime/experiment.lock` for the whole run, and the worker inherits it. The lock is kernel-level, so every sandbox sees it. It is released when the holders exit, and a second experiment is refused while it is held.
  - The real-silver test fixture (`tests/conftest.py`) skips while the lock is held, and `scripts/calibrate_gpu.py` refuses.
  - Tested in `tests/test_worker.py`.
- **Practice:** while an experiment runs, the researcher runs only light work (text, light tests). Calibrations and real-data scripts wait.

## Note for the owner (not blocking)

The 11 GB VM is shared with other workloads the owner runs in WSL (editor servers, a notebook kernel, other agent runtimes). Experiment peaks are 4.8–5.7 GB, so this leaves headroom, but less than the 11 GB figure suggests.

## Resolution

Closed at creation: the cause is identified, the guard is in place, and the failed run is recorded.
