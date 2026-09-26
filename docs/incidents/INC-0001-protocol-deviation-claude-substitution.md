---
schema: incident-v1
incident_id: INC-0001
type: protocol_deviation
created_utc: 2026-09-26T00:00:00Z
raised_by: project owner (pre-run decision)
status: accepted
---

# Researcher and Advisor substitution (brief v2.0 → v3.0)

## What changed
- The primary researcher changed from Gemini 3.8 Flash (Antigravity `agy`) to Claude (`claude-opus-5-5`, effort `high`) in a Claude Code cloud session.
- The Advisor changed from a Codex Advisor/Orchestrator to a Claude `advisor` subagent (Opus, effort `max`).
- Days 1–4 compute changed from the RTX 5060 laptop to a CPU-only cloud container. Days 5–7 return to the laptop under the owner.

## Why
The owner decided this before Day 1, for budget and availability reasons: a promotional
credit for cloud sessions. No research had started, so no result was influenced.

## Impact on validity
- The research question now concerns a Claude researcher, not Gemini.
- The researcher also orchestrates. This is mitigated by fresh-context Advisor reviews and hash-verified gating in `scripts/gate.py` (brief v3 §2.1).
- No GPU during Days 1–4, so the Tier 3 neural and GPU-boosting comparisons are deferred to Day 5.
