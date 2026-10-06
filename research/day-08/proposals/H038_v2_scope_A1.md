---
schema: scope-amendment-request-v1
hypothesis_id: H038
proposal_version: 2
amendment: A1
session: D08-S03
exchange_id: X-D08-S03-0003
created_utc: 2026-10-06T22:41:58Z
---

# H038 v2, scope amendment A1: add the H fold to E051 and E052 as predicted only

## Why

- E051 was refused by `run_experiment.py` before it started: every non-final experiment must list H (INC-0022). This is the researcher's error.
- H038 v2's configs list R1, R2, R3, S1, W1, S1c and W1c, and the review's scope says "Not authorized: any H fold".
- Nothing ran: E051 and E052 are ALLOCATED, with no prediction file, no score and no truth read.

## Requested change (and nothing else)

1. Add `H` to the `folds` of `experiments/E051/config.yaml` and `experiments/E052/config.yaml`. Every other field stays as in ack v2.
2. **Keep the IDs E051 and E052.** Both were refused before start, and the pinned launcher (`54ee5ab8…`) hard-codes them. The configs are amended and committed before re-arming. `gate.json` is unchanged.
3. **Re-arm the pinned launcher** within the owner's existing window (INC-0021: 2026-10-06T22:40:51Z to 2026-10-07T00:40:51Z), if both runs still fit by its guards. The re-arm uses the same START and END arguments, so the window is not extended. Otherwise the queue waits for a new owner window.

## Why H is safe here (H8 unchanged)

- **H is predicted, never scored.** `prc.worker` skips evaluation for `kind == holdout`. The H fold trains on January–November. December DEP targets stay masked by `prc.data.load_silver`, because these runs are not final runs and unmask nothing.
- **No H read follows:**
  - `holdout_check.py` is not run;
  - `mixture_analysis.py` and `known_row_check.py` read development and diagnostic folds only;
  - `mixture_check.py` checks H's prediction and component files without truth.
- **E046,** the base, has H predictions (its manifest lists H).
- **Runtime:** one more fold, about 1–1.5 minutes more per run. The 840 s guard still covers both runs.
- **H predictions are recorded only.** They could serve a later SUBMIT-stage target-free check, which would need its own review.

## Decision requested

ACCEPT the amendment (or rule otherwise). The researcher records it in `research/day-08/acks/H038_ack_v2_A1.md` before re-arming.
