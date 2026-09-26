# Communication Contract — Researcher ↔ Advisor

**Version:** 3.0 · **Status:** frozen at preamble commit; changes require an incident record.

Chat text never authorises an experiment. Only files do.

## 1. Identifiers

- Session: `D{day:02}-S{session:02}`. A new session number is used after a container
  reset or a context summary that loses the working state.
- Exchange: `X-D{day:02}-S{session:02}-{seq:04}`. Unique and never reused.
- Hypothesis: `H###`. Proposal version: `vN`. Experiment: `E###`, allocated only by `scripts/gate.py`.

## 2. Task envelope (researcher → Advisor)

Stored at `orchestration/advisor-exchanges/<exchange-id>/envelope.yaml` **before**
the Advisor is spawned. The Advisor prompt is exactly: *"Execute the task
envelope at `<path>`. Follow `.claude/agents/advisor.md`."*

```yaml
schema: advisor-task-envelope-v1
exchange_id: X-D01-S01-0001
session: D01-S01
sender: claude-researcher
recipient: advisor-subagent
purpose: proposal_review | split_freeze_review | phase_close_review | recovery_review
proposal_ids: [H001]                  # batched reviews list several
proposal_paths: [research/day-01/proposals/H001_v1.md]
proposal_sha256: [<hex>]
review_output_dir: research/day-01/advisor/
context_paths: [research/STATE.md, config/splits.yaml]
constraints: []
created_utc: YYYY-MM-DDTHH:MM:SSZ
```

## 3. Advisor result

The Advisor's final message ends with a fenced YAML block, which is stored verbatim
in `orchestration/advisor-exchanges/<exchange-id>/response.md`:

```yaml
schema: advisor-task-result-v1
exchange_id: X-D01-S01-0001
status: COMPLETE | BLOCKED | FAILED
decisions:
  - proposal_id: H001
    proposal_sha256: <hex, recomputed by the Advisor>
    decision: ACCEPT | REVISE | REJECT | HOLD
    review_path: research/day-01/advisor/H001_review_v1.md
    review_sha256: <hex>
completed_utc: YYYY-MM-DDTHH:MM:SSZ
```

If the recomputed hash differs from the envelope, the decision is `HOLD`.

## 4. Handshake

1. The researcher writes `H###_vN.md` and records its SHA-256.
2. The researcher writes the envelope and spawns `advisor`.
3. The Advisor writes `H###_review_vN.md` and returns the result block.
4. The researcher verifies both hashes and writes `research/day-XX/acks/H###_ack_vN.md`, referencing the proposal hash and the review hash.
5. `scripts/gate.py allocate H### vN` checks: review exists, `decision: ACCEPT`, hashes match, ack present, frozen-file hashes intact. Only then is `E###` issued and logged to `orchestration/task-ledger.jsonl`.
6. Any material change → `H###_vN+1` → back to step 1.

`REVISE` never permits execution. `REJECT` closes that version. `HOLD` blocks
execution until the stated operational condition is resolved.

## 5. Mirroring and redaction

- Every exchange directory contains `envelope.yaml`, `response.md` and `checksums.sha256`.
- Before writing any mirror file, known secret values (see `docs/governance/DATA_POLICY.md`) are replaced by `<REDACTED:VARNAME>`.
- `orchestration/session-registry.jsonl` (append-only) records every session: id, start/end UTC, model ids, container reset reason, and the last exchange carried over.

## 6. Recovery

An exchange may be retried only if no `response.md` exists. A retry records
`retry_of`. A new session rebuilds its state **only** from the last commit,
`research/STATE.md`, the ledgers and the mirrors, and never from chat memory.
