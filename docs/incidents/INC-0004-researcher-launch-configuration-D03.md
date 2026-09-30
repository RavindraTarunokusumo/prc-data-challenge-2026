---
schema: incident-v1
incident_id: INC-0004
type: configuration_discrepancy
created_utc: 2026-09-29T13:50:04Z
status: open
---

# Researcher launch configuration at D03-S01 start: model and effort sources disagree

**Raised by:** the researcher, at the D03-S01 session start. The check was run because of INC-0003.

## Evidence (measured 2026-09-29T13:50Z)

| Source | Model | Effort |
|---|---|---|
| Launch arguments of the running Claude Code process (`ps`, parent of the tool shell) | `--model claude-sonnet-5-5` | `--effort medium` |
| Session metadata (`get_session`): `configured_model`, `session_context.model`, `external_metadata.last_served_model`, `external_metadata.user_switched_model` | **`claude-opus-5-5`** | — |
| Session metadata: `session_context.effort_level`, `external_metadata.effort_level`, `flag_settings.effortLevel` (`server_fold_v1`) | — | **`high`** |

- The brief (§2) and `config/agents.yaml` specify `claude-opus-5-5` at `high`.
- `user_switched_model: claude-opus-5-5` suggests the model was switched in-session after a launch on `claude-sonnet-5-5`. The INC-0003 resolution was itself recorded "in a session on `claude-sonnet-5-5`".
- `last_served_model` is `claude-opus-5-5`, so the served model agrees with the brief. The effective effort tier cannot be determined from inside the session, as in INC-0003.

## Impact

- Both settings are outside the researcher's control (brief §6.1), and the researcher does not change them.
- No Day 3 experiment has run at the time of writing.
- Provenance only: no frozen artifact, split, metric or gate check depends on it.
- The session registry and `SESSION_START.md` record the served model (`claude-opus-5-5`, from metadata) and **both** effort sources.

## Resolution required (owner)

Confirm the intended configuration for D03-S01, or accept the discrepancy as in INC-0003. Until then, D03-S01 work is described as: *"served `claude-opus-5-5` (metadata); launch argument `claude-sonnet-5-5`; effort registered `high`, launch argument `medium`; effective tier not determinable"*.

The incident does not block work.

## Addendum (2026-09-30T07:06:50Z): scope after the second container restart (D3-C5, X-D03-S01-0003)

- The container restarted after E019 completed (kernel boot id `ac2b2cff-…` → `b973b4fe-…`). The researcher process was relaunched at **2026-09-30T05:34:34Z**.
- The relaunched process carries **`--model claude-opus-5-5 --effort medium`** (read from `/proc/<pid>/cmdline`).
- It covers: E020–E022, the Day 3 DAY_SUMMARY, the phase-close proposal, the holdout access and the phase-closing records.
- The incident stays **open**, non-blocking, for the owner to decide.
