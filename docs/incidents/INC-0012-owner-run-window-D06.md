---
schema: incident-v1
incident_id: INC-0012
type: owner_intervention
created_utc: 2026-10-02T17:20:00Z
status: open
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
