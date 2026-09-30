---
schema: incident-v1
incident_id: INC-0003
type: configuration_discrepancy
created_utc: 2026-09-28T19:19:54Z
status: closed
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

## Resolution

**Recorded:** 2026-09-29T13:35:30Z, in a session on `claude-sonnet-5-5`, on the owner's instruction: *"Please record the incident report. Nothing should be affected."*

**Owner decision:** accept as is. No remedial action and no re-run.

- **Nothing is affected.** The Day 2 results, the Advisor decisions (including the phase-close ACCEPT, X-D02-S01-0006), the INCONCLUSIVE outcomes of H009 v3 and H013 v2, and the champion (E005) stand unchanged.
- **No frozen artifact was touched.** Splits, metric, evaluator and audit are unchanged, and no experiment is invalidated or re-labelled.
- **Effective tier not determined.** It was never established whether `medium` (launch argument) or `high` (session metadata) governed the served D02-S01 turns. This record does not settle that. It records that the owner has accepted the uncertainty and that the Day 2 work stands either way.
- **Provenance note.** For the final report, the D02-S01 effort tier is to be described as *"registered `high`; launch argument `medium`; effective tier not determinable"*. D01-S01 remains unverifiable, as stated above.
- **Not addressed by this decision:** the effort setting for future sessions. That is unchanged by this record.

The incident is closed. No other record was edited, other than this file's `status` line, the open-incident line in `research/STATE.md`, and one appended line in `research/PROJECT_LOG.md`.
