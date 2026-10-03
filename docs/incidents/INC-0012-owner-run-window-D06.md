---
schema: incident-v1
incident_id: INC-0012
type: owner_intervention
created_utc: 2026-10-02T17:20:00Z
status: closed
---

# Day 6: owner restricts experiment runs to 21:00–21:30 local time

**Raised by:** the researcher, recording an owner instruction at the D06-S01 start (brief §1: the owner may start or stop the run; every intervention is logged).

## Instruction (owner, verbatim)

> Begin Day 6. Schedule experiment runs (both GPU and CPU) between 21:00 - 21:30.

No reason was stated. The laptop clock is CEST (UTC+2), so the window is **19:00:00Z–19:30:00Z on 2026-10-02**.

## Reading

- **Experiment runs** (anything started by `scripts/run_experiment.py`, GPU or CPU) execute only inside the window. The researcher reads "between" as: a run starts at or after 21:00 and is expected to end by 21:30.
- The day's runs should include at least one GPU run and at least one CPU run.
- Text work (proposals, the Advisor review, acknowledgements, allocation, records, analysis of stored files) is not an experiment run and continues outside the window.
- Real-silver calibrations are compute on the same laptop and are treated as runs: none happen outside the window.

## Handling

- **One experiment at a time is unchanged** (INC-0008 lock). A GPU run and a CPU run are not run concurrently: the Day 5 peaks (CatBoost GPU 6.4–7.1 GB, LightGBM 6.6 GB) sum above the 11 GB VM.
- **A launcher** (`research/day-06/sessions/D06-S01/run_window.sh`, committed before the window) waits until 21:00 and runs the allocated queue in order. It starts a run only if the current time plus that run's pessimistic runtime is no later than 21:30. A run that does not fit is **deferred**, not started: it stays ALLOCATED for the owner's next window and is reported. A running experiment is never killed by the launcher.
- A blend starts only if its component is COMPLETE (the blend itself also refuses otherwise).
- No file under the repository changes during the window, so each run records a clean tree.

## Resolution

Open for Day 6. Closes at the Day 6 phase close, or when the owner changes the window.

## Amendment (2026-10-02, after X-D06-S01-0001)

- "No file under the repository changes during the window" reads: **no file outside the running experiment's own records changes during the window.** The launcher's per-run checkpoint commits only that run's paths (`experiments/<E###>/`, `experiments/ledger.jsonl`, `research/comparisons/route_check_<E###>.json`).
- The launcher was revised for batch v2 (rung B first; own-path staging; clean-tree re-check at window open; `TZ=Europe/Amsterdam` with the window computed from UTC; non-interactive push under a 60 s timeout; a log line for any run that ends after 21:30). Its SHA-256 is pinned in `research/day-06/proposals/H024_v2.md` §Batch.
- **Overrun:** the launcher never kills a run; the CLASS-M timeout (2,700 s) bounds it. Any run still executing at 21:30 is reported, with its end time, as a deviation under this incident.

## Amendment (2026-10-03, D06-S01)

- Owner (2026-10-03): "Continue with more tests. GPU is free." The researcher reads the 21:00–21:30 window as a **standing daily window** (the instruction named no end date). The next batch (H029–H030) runs 21:00–21:30 Europe/Amsterdam on 2026-10-03 (19:00–19:30Z) unless the owner says otherwise.
- Launcher `research/day-06/sessions/D06-S01/run_window_2.sh` (SHA-256 `edfe11dfd7e5f690a722fd05e5050213fbede60b3a8ede00355c8a3e08dadf3e`): the pinned `run_window.sh` logic with only the date, log name and queue changed.
- GPU memory in use at 2026-10-03T08:13Z: 635 MiB (the 4.3–5.2 GB external holder of 2026-10-02 is gone, as the owner reports).

## Amendment (2026-10-03T08:53:32Z, D06-S01): owner moves batch 2 into an immediate run

- Owner (verbatim, replying to the plan to arm at 20:43 for the 21:00–21:30 window): "No, run now."
- The researcher reads this as an owner decision (brief §1: the owner may start the run) that **replaces the 21:00–21:30 window for batch 2 (E040, E041)**. The standing-daily-window reading of the 2026-10-03 amendment is withdrawn as unconfirmed; future windows follow the owner's next instruction.
- The scheduled arming was cancelled. The pinned `run_window_2.sh` is not used (its window is fixed) and not edited. Per N2/C3 of the reviews, the runs are started by **direct `scripts/run_experiment.py` calls**, in order (E040, then E041 only if E040 is COMPLETE and passes `route_check.py E040 - E029`), with the same own-path checkpoint commits. Not a deviation from the reviews: the window is the owner's to set.

## Closure (Day 6 phase close, X-D06-S01-0004)

Closed by its resolution clause. Batch 1 (E035–E039) ran inside the 2026-10-02 window, all ending by 19:29:17Z; batch 2 (E040–E041) ran on the owner's recorded instruction "No, run now." (an amendment, not a deviation). No run executed past a window. Any new owner instruction on run timing in Day 7 needs a new incident.
