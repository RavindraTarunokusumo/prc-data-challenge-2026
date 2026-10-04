---
schema: incident-v1
incident_id: INC-0015
type: owner_intervention
created_utc: 2026-10-03T20:17:09Z
status: closed
---

# Day 7: owner chooses to test an unrouted-subgroup candidate before the freeze, and sets a run window at 02:00

**Raised by:** the researcher (brief §1: every owner intervention is logged).

## Context

After the SUBMIT batch (E042–E044), while preparing the final report, the researcher re-read the Day 3 phase close (X-D03-S01-0003 (e)). The routing of the LIRF NM-missing subgroup to the E005-class ridge costs **122.54 s** of development RMSE (E019 − E020). An unrouted candidate has been admissible since Day 4 under stated conditions, and no Day 4–6 proposal tested one. The researcher judged this the largest open question for the submission, paused before the phase close, and asked the owner, recommending the test.

## Owner decisions (verbatim selections)

1. To the question "Test it / Freeze now / Pause": **"Test it (Recommended)"**. The option was written and recommended by the researcher. The owner chose among options; it did not select features, parameters or thresholds.
2. To the question on the run window: **"02:00 tomorrow"**. The laptop clock is CEST, so the window starts **2026-10-04T00:00:00Z**. No end was stated. The researcher reads it as a one-hour window, **00:00–01:00Z**, matching INC-0014's length. A run that does not fit is deferred, not started.

## Handling

- As INC-0014's handling (one experiment at a time; a pinned launcher; never kills; own-path checkpoints; deferral is status-only). A new launcher for this window is pinned in the batch proposal.
- The candidate goes through the normal handshake (proposal, Advisor review, gate). Its promotion, if any, is decided at the Day 7 phase close with the Day 7 holdout access.
- The SUBMIT predictions of E044 stay recorded and unchanged. The phase close decides which submission file is final.

## Resolution

Open. Closes at the Day 7 phase close.

## Outcome of the 2026-10-04 window

- Armed 2026-10-03T20:54:26Z; window opened 00:00:08Z. E045, E046, E047, E048 ran in order, all COMPLETE, all within the window (E048 finished 00:48:40Z; launcher END 00:50:23Z). **No deviation.**
- **E049 and E050 were DEFERRED** at 00:50:28Z (E049 needs 600 s; 572 s were left). E045's and E047's runtimes (1,196 s and 1,339 s) exceeded their 1,100 s guards, and four failed W&B syncs took about 100 s each. Both stay ALLOCATED (U10); they are needed only if H035 is promoted, and they need a later owner-set window recorded in a new incident.
- No WARNING (tree clean after each checkpoint); no unmasking event for E045–E048 (U3, U4).

## Closure (P9 of X-D07-S01-0003)

Closed: H035 was promoted on the Day 7 holdout WIN, and E049 and E050 are COMPLETE and checked (INC-0016). The 2026-10-04 00:00–01:00Z window had no deviation.
