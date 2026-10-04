---
schema: incident-v1
incident_id: INC-0014
type: owner_intervention
created_utc: 2026-10-03T16:58:00Z
status: closed
---

# Day 7: owner restricts experiment runs to 21:00–22:00 local time

**Raised by:** the researcher, recording an owner instruction at the D07-S01 start (brief §1: the owner may start or stop the run; every intervention is logged). INC-0012's closure requires a new incident for any Day 7 instruction on run timing.

## Instruction (owner, verbatim)

> Begin Day 7. Schedule experiment runs between 21:00 - 22:00

No reason was stated. The laptop clock is CEST (UTC+2; measured 18:56 CEST = 16:56Z at the session start), so the window is **19:00:00Z–20:00:00Z on 2026-10-03**.

## Reading

- **Experiment runs** (anything started by `scripts/run_experiment.py`) execute only inside the window: a run starts at or after 21:00 and is expected to end by 22:00. Unlike INC-0012, the instruction names no backend, so no GPU/CPU mix is required.
- Text work (proposals, the Advisor review, acknowledgements, allocation, records, analysis of stored files, formatting stored predictions with `scripts/make_submission.py`) is not an experiment run and continues outside the window.
- Real-silver calibrations or feature builds are compute on the same laptop and are treated as runs: none happen outside the window.
- The window is read for **2026-10-03 only**. INC-0012's "standing daily window" reading was withdrawn as unconfirmed; a later window needs the owner's next instruction.

## Handling

- **One experiment at a time** (INC-0008 lock); a GPU and a CPU run are never concurrent.
- **A launcher** (`research/day-07/sessions/D07-S01/run_window.sh`, committed and SHA-256-pinned before the window) keeps INC-0012's pinned logic: it waits until 21:00, runs the allocated queue in order, starts a run only if now + its pessimistic runtime ≤ 22:00 (otherwise DEFERRED, left ALLOCATED), never kills a run (the class timeout bounds it), starts a blend only if its components are COMPLETE and route-checked, and commits and pushes only each run's own records.
- **Overrun:** any run still executing at 22:00 is reported here, with its end time, as a deviation.

## Resolution

Open for Day 7. Closes at the Day 7 phase close, or when the owner changes the window.

## Outcome of the window (2026-10-03, D07-S01)

- Armed 17:22:54Z as a detached process; window opened 19:00:05Z; queue E042 → E043 → E044 ran in order and ended **19:15:43Z**. No run executed outside the window; **no deviation.**
- After each checkpoint the launcher logged `WARNING: tree not clean … M orchestration/task-ledger.jsonl` only: the final-fold unmasking append pre-registered as S3 of `research/day-07/advisor/H031_review_v1.md` (not a deviation). The lines were committed after the window.
- `make_submission.py` (formatting stored files, not a run) was run at 20:00Z, after the window closed (S8).
- GPU in use: 2,938 MiB at arming (external holder), 704 MiB at window open.

## Amendment (2026-10-03T20:17Z): a second Day 7 window

- The owner set a further run window at 02:00 CEST on 2026-10-04 for the routing candidate (INC-0015, which records it and its 00:00–01:00Z reading).

## Closure (Day 7 phase close, X-D07-S01-0003, P9)

Closed: the 2026-10-03 window is complete with no deviation. The second Day 7 window is recorded under INC-0015.
