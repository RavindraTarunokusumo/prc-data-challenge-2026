# AGENTS.md — operating rules for every agent in this repository

Normative brief: `docs/PROJECT_BRIEF.md` (v3.0). If anything here conflicts with it, the brief wins.

## Roles
- **Researcher**: the main Claude Code session. Proposes, implements, runs, analyses.
- **Advisor**: the `advisor` subagent (`.claude/agents/advisor.md`). Reviews only.

## Session start (researcher)
1. Read `docs/PROJECT_BRIEF.md`, `docs/governance/COMMUNICATION_CONTRACT.md`, `config/agents.yaml`, `config/network.yaml` (the network allowlist; read it before any research or web access), `research/STATE.md`, the latest `DAY_SUMMARY.md`/`SESSION_SUMMARY.md`, the tail of `orchestration/task-ledger.jsonl` and `orchestration/session-registry.jsonl`.
2. Append a session entry to `orchestration/session-registry.jsonl`.
3. Write `research/day-XX/sessions/<session>/SESSION_START.md`: recovered state, champion, accepted and rejected findings, remaining budget, open questions, first planned action, resolved model ID, last exchange ID, and the git commit with a dirty-state declaration.
4. Only then begin work.

## Non-negotiables
- **Secrets never enter tracked files, commits, logs or mirrors.** The repo is public. Use env vars or `.env`.
- No experiment runs without an `E###` from `scripts/gate.py` (ACCEPT + hashes + ack).
- Frozen after the Day 1 freeze commit: `config/splits.yaml`, `src/prc/metrics.py`, the protected holdout definition.
- No leaderboard access, no submission-bucket access, no competitor-solution searches.
- Network: fetch only from hosts in `config/network.yaml`. Web searches exclude github.com and kaggle.com. An unlisted host is a HOLD, never a workaround.
- Never rewrite completed records. Append corrections.
- Checkpoint after every experiment (brief §13): commit **and push**, since the container is ephemeral.
