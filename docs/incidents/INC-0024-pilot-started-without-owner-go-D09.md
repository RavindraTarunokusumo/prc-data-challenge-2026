---
schema: incident-v1
incident_id: INC-0024
type: researcher_error
created_utc: 2026-10-08T00:16:55Z
status: open
---

# Day 9: the taxi-state design pilot was started without the owner's go-ahead, and stopped

**Raised by:** the researcher (D09-S01).

## What happened

- The researcher committed the pilot's parameters and decision rule (`0969550`), then started `scripts/pilot_taxistate_D09.py` at once, in the background. **The owner had not authorised a run.**
- **Owner (verbatim, chat, D09-S01):**
  > I didn't tell you to run yet. Cancel run and wait.
- The researcher stopped the task. A process check then found no pilot process.
- **No pilot result exists.** The log was empty, and no JSON was written. The process was stopped during the first pilot split, before any prediction was compared with a target. The researcher saw no figure.
  - The script loads silver, which holds design-month targets. It builds P1's features and starts fitting. Its truth join comes after the three model fits.
  - The empty log was deleted. Nothing from the stopped run is kept.
- The parameters, the rule and the code are unchanged since `0969550`.

## Owner's go-ahead

- **Owner (verbatim, chat, D09-S01, before 2026-10-08T00:16:55Z):**
  > Go
- **Reading:** the go-ahead to record this incident and to run the pilot as committed. The run starts after this record is committed.

## Practice from now on

**No run of any kind** (pilot, experiment, SUBMIT fit or formatter) starts in Days 9–12 without the owner's explicit go-ahead in chat for that run. The go-ahead is recorded before the run.

## Resolution

Open. Closes at the Day 9 phase close.
