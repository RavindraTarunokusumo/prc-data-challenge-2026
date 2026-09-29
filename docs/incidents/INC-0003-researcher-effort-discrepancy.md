---
schema: incident-v1
incident_id: INC-0003
type: configuration_discrepancy
created_utc: 2026-09-28T19:19:54Z
status: open
---

# Researcher effort tier: two sources disagree

**Raised by:** Advisor, review X-D02-S01-0002 (process note, non-blocking). **Verified by the researcher** in D02-S01 at the time above.

## Evidence

| Source | Effort |
|---|---|
| Launch arguments of the running Claude Code process (`ps`) | `--effort medium` (model `--model claude-opus-5-5`) |
| Session metadata (`get_session`): `session_context.effort_level`, `external_metadata.effort_level` and `flag_settings.effortLevel` (`flag_settings_origin: server_fold_v1`) | **`high`** |

- The brief (§2, `config/agents.yaml`) specifies `high`.
- `orchestration/session-registry.jsonl` and `SESSION_START.md` recorded `high` from the session metadata.
- The researcher cannot determine from inside the session which source governs the served turns. The server-side flag may override the launch argument, or the reverse.
- The model is unaffected: `claude-opus-5-5` is configured and served.

## Impact

- The effort tier is outside the researcher's control (brief §6.1).
- No experiment has run under D02-S01. Every Day 2 artifact so far is proposals, tooling and EDA, all reviewed by the Advisor at `max`.
- If the effective tier was `medium`, the D02-S01 researcher work was done at a lower tier than registered. It is a protocol deviation in provenance only: no frozen artifact, split, metric or gate check depends on it.
- D01-S01 may have run under the same launch configuration. That cannot be verified retroactively.

## Resolution required (owner)

Confirm which effort setting applies to this cloud session, and either:
- confirm `high` and close this incident; or
- record `medium` as the effective tier for the affected sessions, and decide whether to change the environment's setting.

The researcher continues under the recorded configuration and does not change its own settings.
