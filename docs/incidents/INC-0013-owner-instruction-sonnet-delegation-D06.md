---
schema: incident-v1
incident_id: INC-0013
type: protocol_deviation
created_utc: 2026-10-02T17:51:24Z
status: closed
---

# Day 6: owner permission to delegate coding tasks to `claude-sonnet-5-5` subagents

**Raised by:** the researcher, recording an owner instruction in D06-S01. INC-0006 closed with the rule that delegation on Days 6–7 needs a new incident; this is that incident.

## Instruction (owner, D06-S01, verbatim)

> Don't forget to use `claude-sonnet-5.5` subagents to delegate coding tasks if necessary.

The model ID is resolved as `claude-sonnet-5-5` (Agent tool, `model: sonnet`).

## Scope (same boundary as INC-0005 and INC-0006)

- **Stays with the main session (`claude-opus-5-5`):** hypotheses, proposals and their pre-registered predictions; envelopes, acknowledgements and `gate.py` allocations; experiment launches; interpretation of results, decisions, `STATE.md`, the journal and `DAY_SUMMARY.md` conclusions.
- **May be delegated:** coding tasks to a written specification (analysis scripts, features, models, tests), codebase digests, mechanical records. The main session reviews every delegated diff before commit.
- **Unchanged:** the Advisor stays the fixed `advisor` subagent (definition SHA-256 `30fff5dd3c54…`). Every gate, freeze, holdout, leaderboard and contamination rule applies to workers. Workers get no write access to `research/day-*/advisor/`, never touch files under a tools freeze while it holds, and never run real-silver work while the experiment lock is held or outside the INC-0012 window if it is compute.

## Provenance

Every delegated record carries the line *"implemented by a `claude-sonnet-5-5` worker to the researcher's specification; reviewed by the researcher"*. The delegated-work list goes into `research/day-06/DAY_SUMMARY.md`.

## State at the instruction

The batch in review (H024–H028 v2) needs no code change (existing code paths). Delegation is used only if a coding task arises ("if necessary").

## Resolution

Closes at the Day 6 phase close, with the delegated-work list.

## Closure (Day 6 phase close, X-D06-S01-0004)

**Delegated work:** `research/day-06/eda/d06_diagnostics.py` (SHA-256 `5fc21113…10b7`) and `research/day-06/eda/d06_diagnostics_test.py`, implemented by a `claude-sonnet-5-5` worker to the researcher's specification; reviewed by the researcher. The worker wrote only in the scratchpad while experiments ran. D6-C14 (b): the test file lacked the provenance line; added at this phase close. Delegation in Day 7 needs a new incident.
