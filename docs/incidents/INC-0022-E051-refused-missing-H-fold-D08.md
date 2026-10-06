---
schema: incident-v1
incident_id: INC-0022
type: researcher_error
created_utc: 2026-10-06T22:41:38Z
status: open
---

# Day 8: E051 refused by the runner before it started (no H fold in the config); E052 deferred

**Raised by:** the researcher (D08-S03). **The error is the researcher's.**

## What happened

- The launcher was armed on the owner's go-ahead at 2026-10-06T22:40:58Z (window to 2026-10-07T00:40:51Z, INC-0021).
- `scripts/run_experiment.py` refused E051 at once: `refused: E051 must cover all scored folds plus H; missing ['H']`.
- The runner's `check_config` (SPLITS v2 review) requires every non-final experiment to list all development and diagnostic folds **plus H**. H038 v1 and v2 listed R1–W1c only. Neither the researcher nor the reviews checked this rule, and the review's scope says "Not authorized: any H fold".
- **E051 never started.** The refusal comes before the worker: no fit, no prediction file, no score, and no truth read. Ledger status stays ALLOCATED.
- **E052 was deferred** by the launcher's rule (no start after a failed run). It also stays ALLOCATED.
- The launcher committed nothing ("nothing to commit"). Its log is copied to `research/day-08/sessions/D08-S03/run_window.log`.

## Look count (rule 15 (a))

No development-fold score exists for E051 or E052. The look count is unchanged.

## Proposed fix (needs the Advisor; X-D08-S03-0003)

- Add H to both configs' folds, as **predicted only**.
  - The worker never scores a holdout fold.
  - The H fold trains on January–November and predicts December rows with December DEP targets masked by the data layer (no unmasking: these are not final runs).
  - `holdout_check.py` is not run, and ruling H8 is unchanged.
  - E046, the base, has H predictions, so the override covers H.
  - `mixture_check.py` checks H like any other fold, without truth.
  - `mixture_analysis.py` and `known_row_check.py` read development and diagnostic folds only.
- **Keep the IDs E051 and E052** (refused before start; the pinned launcher hard-codes them). Change nothing else.
- Re-arm the launcher in the owner's existing window, if time remains, after the ruling and an acknowledgement.

## Resolution

Open. Closes when the ruling is acknowledged and the queue has run, or been deferred, under it.

## Amendment (2026-10-06T22:50:11Z): the ruling (X-D08-S03-0003, ACCEPT 0.85)

- **The review's share of the error.** The Advisor's v2 review did not check the configs against the runner's `check_config`. It also listed "any H fold" as not authorized, confusing H **prediction** (required of every non-final run) with H **access** (closed by H8). The error is the researcher's and the review's.
- **Why an amendment and not a v3.** The change is one predicted-only fold, required by the frozen runner. It changes no model, parameter, scored fold, reading or criterion, and both runs were refused before start. A v3 would need new IDs, and with them a new launcher. The envelope purpose `scope_amendment` is not one of the contract's listed purposes. It is recorded here as a deviation of form, ruled acceptable by the Advisor.
- **Fix applied:** `- H` appended to both configs (ack `H038_ack_v2_A1.md`).
- **Re-arm:** allowed only by 2026-10-07T00:12:51Z, with the same window arguments. The re-arm time is appended below when it happens.
