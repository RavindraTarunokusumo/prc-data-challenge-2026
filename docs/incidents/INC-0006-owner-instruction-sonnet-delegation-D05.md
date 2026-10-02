---
schema: incident-v1
incident_id: INC-0006
type: protocol_deviation
created_utc: 2026-10-01T16:10:00Z
status: closed
---

# Day 5: owner permission to delegate work to `claude-sonnet-5-5` subagents

**Raised by:** the researcher, at the D05-S01 session start, recording an owner instruction. INC-0005 (Day 4) closed with the rule that delegation on Days 5–7 needs a new incident; this is that incident.

## Instruction (owner, D05-S01 launch message, verbatim)

> Begin Day 5. You may use `claude-sonnet-5.5` subagents.

The model ID is resolved as `claude-sonnet-5-5` (Agent tool, `model: sonnet`).

## Scope (same boundary as INC-0005)

- **Stays with the main session (`claude-opus-5-5`):** hypotheses, proposals and their pre-registered predictions; envelopes, acknowledgements and `gate.py` allocations; experiment launches; interpretation of results, promotion decisions, `STATE.md`, the journal and `DAY_SUMMARY.md` conclusions.
- **May be delegated:** environment and data verification; codebase digests; EDA scripts; implementation of features, models and tests to a written specification; drafting mechanical records (metrics tables, manifests). The main session reviews every delegated diff before commit.
- **Unchanged:** the Advisor stays the fixed `advisor` subagent (definition SHA-256 `30fff5dd3c54…`), and is not delegated or substituted. Every gate, freeze, holdout, leaderboard and contamination rule applies to workers. Workers get no write access to `research/day-*/advisor/`.

## Provenance

Every delegated record carries the line *"implemented by a `claude-sonnet-5-5` worker to the researcher's specification; reviewed by the researcher"*. The delegated-work list goes into `research/day-05/DAY_SUMMARY.md`.

## Resolution

Closes at the Day 5 phase close, with the delegated-work list.

## Closure (2026-10-02, Day 5 phase close X-D05-S05-0001 ACCEPT)

**No delegated work.** Delegation to `claude-sonnet-5-5` workers was permitted but never used. No Day 5 record carries the delegation provenance line, and none claims delegation (verified by the phase-close review). The delegated-work list in `research/day-05/DAY_SUMMARY.md` §8 is empty. Delegation on Days 6–7 needs a new incident.
