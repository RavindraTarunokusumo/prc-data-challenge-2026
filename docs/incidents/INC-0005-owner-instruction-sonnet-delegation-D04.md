---
schema: incident-v1
incident_id: INC-0005
type: protocol_deviation
created_utc: 2026-09-30T16:06:53Z
status: closed
---

# Day 4: owner instruction to delegate work to `claude-sonnet-5-5` subagents

**Raised by:** the researcher, at the D04-S01 session start, recording an owner instruction.

## Instruction (owner, D04-S01 launch message, paraphrased without secrets)

> Begin Day 4. Make use of `claude-sonnet-5-5` subagents to delegate work
> (the owner's promotional credit is spent; Day 4 runs on the owner's daily subscription limit).

This is an owner intervention for an explicit budget reason (brief §1, §2 "Budget").

## Deviation from the brief

- Brief §2 and `config/agents.yaml` name the researcher as the main session on `claude-opus-5-5`. From D04-S01, parts of the researcher's work are carried out by **worker subagents on `claude-sonnet-5-5`** (Agent tool, `model: sonnet`), spawned by the main session.
- **What stays with the main session (`claude-opus-5-5`):**
  - hypotheses, proposals and their pre-registered predictions;
  - envelopes, acknowledgements and `gate.py` allocations;
  - interpretation of results, promotion decisions, `STATE.md` and `DAY_SUMMARY.md` conclusions.
- **What may be delegated to Sonnet workers:**
  - environment and data verification;
  - codebase digests;
  - EDA scripts;
  - implementation of features, models and tests to a written specification;
  - launching allocated experiments and drafting mechanical records (metrics tables, manifests, ledger exports).

  The main session reviews each delegated diff before it is committed.
- **Unchanged:**
  - The Advisor stays the fixed `advisor` subagent (`opus`, effort `max`, definition SHA-256 `30fff5dd3c54…`). It is not delegated or substituted.
  - Every gate, freeze, holdout, leaderboard and contamination rule applies to workers exactly as to the researcher. Workers receive no Advisor role and no write access to `research/day-*/advisor/`.

## Provenance

- Every Day 4 record that a worker drafted or implemented says so in its provenance line: *"implemented by a `claude-sonnet-5-5` worker to the researcher's specification; reviewed by the researcher"*.
- The session registry records the delegation at the session start.

## Impact

Provenance only. No frozen artifact, split, metric or gate check changes. INC-0004 (launch effort `medium` against registered `high`) is still open and also covers D04-S01: at 16:06:53Z the process carries `--model claude-opus-5-5 --effort medium`, and the metadata says `high`.

## Resolution required (owner)

None beyond the instruction itself. The incident closes at the Day 4 phase close, with the list of delegated work in `research/day-04/DAY_SUMMARY.md`.

## Closure (2026-10-01T01:59:30Z)

**Closed at the Day 4 phase close** (X-D04-S02-0001 ACCEPT; `research/day-04/acks/PHASE_CLOSE_D04_ack_v1.md`).
- **The delegated-work list** is in `research/day-04/DAY_SUMMARY.md` §8, corrected per D4-C12:
  - `e4c57f8` is added;
  - the D04-S01 pipeline digest was never committed.
- **The Advisor audited the boundary.** No delegated commit touched a proposal, review, ack, envelope, gate or allocation record, ledger, journal, STATE or summary. The main session launched both Day 4 runs.
- **Delegation on Days 5–7 needs a new incident.**
