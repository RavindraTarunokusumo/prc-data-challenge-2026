# Model Registry

Frozen at the preamble commit. Substituting any model mid-run is a protocol
deviation and must be recorded in `docs/incidents/` before work continues.

| Role | Runtime | Requested model | Effort | Pinned by |
|---|---|---|---|---|
| Primary researcher | Main Claude Code cloud session | `claude-opus-5-5` | `high` | Session configuration |
| Advisor | `advisor` subagent, fresh context per exchange | `opus` alias → resolved ID recorded per exchange | `max` | `.claude/agents/advisor.md` frontmatter |

Notes:
- The researcher records the resolved serving model at every session start (`SESSION_START.md`) from the session metadata, not from self-report.
- The Advisor definition file is hashed in `config/agents.yaml`. `scripts/gate.py` refuses to run if the hash changes.
- Advisor policy version: `advisor-policy-v3.0` (the body of `.claude/agents/advisor.md`).
- Review schema: `advisor-review-v1` (v2 §10, with v3 field substitutions).
