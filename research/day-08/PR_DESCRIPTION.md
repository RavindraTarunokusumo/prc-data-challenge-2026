# Day 8: the first reopened phase (closed; champion unchanged)

**Outcome.** No promotion. **E046 remains champion.** H stays closed (H8). There is no Day 8 upload, and **E050's file stands** (`f0dc2c7c…06e8`). Phase close X-D08-S03-0004: ACCEPT (0.85).

## What happened

- **H038 v2: a convention mixture for LIRF's NM-missing subgroup (E051, E052).**
  - Development mean 294.32 against 314.42.
  - **Criterion 2 is not met:** one WIN (R3, carried by its known rows), and S1 is a TIE.
  - **REJECT.** E052 reproduces E051 byte for byte.
- **External weather (INC-0019).**
  - METAR reports for all ten airports were fetched by the owner and are kept as bronze data with manifests.
  - The design-month pilot failed its pre-registered rule (+1.43 / −0.48 s). Not pursued.
- **Recording conventions beyond LIRF.** A design-month look at 18 signatures found none meeting its pre-set rule. No lead.

## Key metrics

| | Development mean |
|---|---|
| E046 (champion) | 314.42 |
| E051 (best Day 8 run; REJECT) | 294.32 |
| E033 (previous champion) | 438.87 |

## Deviations and corrections

- **INC-0022:** E051's first arming was refused (no H fold). Nothing ran.
- **D8-C14:** the weather-host failure was first blamed on the Claude Code sandbox. It was in the laptop's network path.
- **D8-C15:** the wind mechanism was overstated to the owner, because the runway is already a model input.
- **D8-C18:** E051's reverted known-row reading is weaker than first written.
- **INC-0023:** the owner's choices among research options. One offered option was a route around a pre-registered rule.
- Full list: D8-C14 to D8-C22 in `research/day-08/acks/PHASE_CLOSE_D08_ack_v1.md`.

## Pending

The owner's decision: continue (Days 9–12, within X-D08-S03-0004 Q5) or refreeze (Q6).

## Merge

Content-neutral: no frozen file changes (`config/splits.yaml`, `src/prc/metrics.py`, `splits.py` and `evaluate.py` are unchanged against `main`).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
