---
schema: incident-v1
incident_id: INC-0021
type: owner_decision
created_utc: 2026-10-06T19:19:47Z
status: open
---

# Day 8: owner sets the run window for H038 (D08-S03)

**Raised by:** the researcher, recording owner decisions (brief §1: run windows are the owner's).

## Instructions (owner, D08-S03, verbatim, in order)

> I thought you already had an experiment plan ready? Please run that experiment now. Max time: 30m

The researcher answered that no reviewed proposal existed and offered two options: follow the protocol, or waive the review for an exploratory run. The owner answered:

> Option 1

After the proposal went to review:

> Start at my go ahead

## Reading

- **Window length:** at most 30 minutes, the launcher's END = START + 30 min.
- **Start:** only on the owner's explicit go-ahead, given after the review is ACCEPTED and acknowledged and E051/E052 are allocated. No run is armed before it.
- No protocol rule is waived (option 1).

## Resolution

Open. Closes when the H038 queue has run or been deferred, recorded in the session.

## Amendment (2026-10-06T21:28:44Z): the window is 2 hours

The owner, after E051 and E052 were allocated (D08-S03, verbatim):

> Replace window with 2hrs. Wait for my go ahead.

**Reading.**
- The window is **at most 2 hours**: the launcher's END = START + 2 h. This replaces the 30 minutes above.
- **The start is unchanged:** only on the owner's explicit go-ahead. Nothing is armed before it.
- The launcher (`54ee5ab8…`) and its guards (840 s per run) are unchanged. The window is passed to it as arguments, so the pinned file is not edited.
- **Effect on H038 v2's scope** (ack v2: "END = START + 30 minutes"): the window is the owner's decision (G3; brief §1), and this amendment supersedes that line. A longer window only lowers the chance that E052 is deferred. No run, fold, guard or reading changes. The phase close records it.
