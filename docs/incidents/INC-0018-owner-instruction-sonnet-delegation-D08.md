---
schema: incident-v1
incident_id: INC-0018
type: protocol_deviation
created_utc: 2026-10-05T09:31:17Z
status: closed
---

# Days 8–12: owner permission to delegate coding tasks to `claude-sonnet-5-5` subagents

**Raised by:** the researcher, recording an owner instruction in D08-S01. INC-0013 closed with "Delegation in Day 7 needs a new incident"; Days 8–12 likewise need one. This is that incident.

## Instruction (owner, D08-S01, verbatim)

> Same as before if you need to spawn Sonnet or Max subagents.

"Same as before" is read as INC-0005, INC-0006 and INC-0013. The worker model ID is resolved as `claude-sonnet-5-5` (Agent tool, `model: sonnet`). "Max" is read as the fixed `advisor` subagent (Opus, effort max). It is not a second reviewer and not a delegated researcher.

## Scope (same boundary as INC-0005, INC-0006 and INC-0013)

- **Stays with the main session (`claude-opus-5-5`):** hypotheses, proposals and their pre-registered predictions; envelopes, acknowledgements and `gate.py` allocations; experiment launches; interpretation of results, decisions, `STATE.md`, the journal and `DAY_SUMMARY.md` conclusions.
- **May be delegated:** coding tasks to a written specification (analysis scripts, features, models, tests), codebase digests, mechanical records. The main session reviews every delegated diff before commit.
- **Unchanged:** the Advisor stays the fixed `advisor` subagent (definition SHA-256 `30fff5dd3c54…`). Every gate, freeze, holdout, leaderboard and contamination rule applies to workers. Workers get no write access to `research/day-*/advisor/`. They never run real-silver work while the experiment lock is held, or outside an owner run window when it is compute.

## Provenance

Every delegated record carries the line *"implemented by a `claude-sonnet-5-5` worker to the researcher's specification; reviewed by the researcher"*. The delegated-work list goes into each Day 8–12 `DAY_SUMMARY.md`.

## Resolution

Open. Closes at the last Day 8–12 phase close, with the delegated-work list.

## Closure (2026-10-08T18:08:03Z, D09-S01; X-D09-S01-0001 R3)

**Delegated-work list for Days 8–12: none.** No `claude-sonnet-5-5` worker was used in Day 8 or Day 9 (DAY_SUMMARY D8 §8, D9 §6). **Status: closed.**
