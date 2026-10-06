---
schema: incident-v1
incident_id: INC-0018
type: owner_intervention
created_utc: 2026-10-04T22:35:39Z
status: open
---

# After FROZEN: owner asks for a six-day improvement plan and discloses a leaderboard figure

**Raised by:** the researcher (brief §1).

## Instruction (owner, verbatim)

> We still have 6 more days, and the No. 1 ranked submission is 214. Plan for the next 6 days on how to bump our scores up. After the handover, we'll conclude the session. Consult the Advisor if you need to.

## Why this is an incident

1. **Scope.** Brief §3 ends the programme at Day 7, and the project is FROZEN (P7). Any further work is an **extension** outside the frozen autonomous run. The frozen records (champion E046, submission v1 `f0dc2c7c…`, `docs/reports/FINAL_REPORT.md`) stand unchanged and remain the run's result.
2. **Leaderboard exposure.** "214" is another team's leaderboard figure. LEADERBOARD_POLICY and P7 (d) say a leaderboard figure is "recorded as an external evaluation only and is never fed back into methodology". The researcher's context now holds it. The plan written in response (`docs/reproducibility/HANDOFF_D07.md` §3) does not use it to choose methods or thresholds. The owner's goal ("bump our scores up") is leaderboard-motivated, and any extension is labelled accordingly.
3. **No holdout remains** (ruling H7: the Day 7 access was the project's last H read). An extension has only the development folds for selection, or the leaderboard, which would be leaderboard-guided optimisation.

## Handling

- The researcher wrote the plan and the handover. **No experiment, allocation, proposal or Advisor exchange was started.** The plan's first step is an Advisor governance review that sets the extension's rules.
- The owner must decide the leaderboard policy for the extension (HANDOFF_D07 §3.1).

## Resolution

Open. It closes when the owner declines an extension, or when the extension's governance review records its own rules.
