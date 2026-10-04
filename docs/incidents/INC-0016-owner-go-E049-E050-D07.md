---
schema: incident-v1
incident_id: INC-0016
type: owner_intervention
created_utc: 2026-10-04T18:01:43Z
status: open
---

# Day 7: the deferred SUBMIT runs E049 and E050 start on the owner's word

**Raised by:** the researcher (P5 of X-D07-S01-0003: under WIN, a new incident before the E049/E050 window, stating the window and the procedure).

## Context

The Day 7 holdout access gave E046 a WIN against E033 (December 2025, one access), and H035 was promoted. E049 (H036 v1) and E050 (H037 v1) were DEFERRED in the INC-0015 window and stay ALLOCATED. Under P4, E050's file is final only if both complete and pass their checks; otherwise E044's file is final.

## Owner instruction (verbatim answer)

The researcher asked when the two runs may execute (options: tonight 21:00–22:00, as soon as ready, or not at all). The owner answered: **"Begin when I say so later."**

## Reading

- The window opens when the owner says so in this session, and the researcher starts the procedure below at once. The window has no fixed end; the two runs take about 10 minutes (E042, the same learner on the final folds, took 280 s; E045's development runs took 1,196 s on eight folds; each failed W&B sync adds about 100 s).
- If the owner does not give the word, or declines, P4's fallback applies: E044's file is final.

## Procedure (P5 (b): direct calls with a scripted checkpoint)

- Script `research/day-07/sessions/D07-S01/run_e049_e050.sh`, SHA-256 `db6f7d883dc23ec8a43fb9270f6db445ff9314192b9e5a6547b9eaf4d2a4dced`, committed with this record. The exact sequence:
  1. abort unless the tree is clean and E049 is ALLOCATED;
  2. `uv run python scripts/run_experiment.py E049`;
  3. checkpoint of E049's own records (the launchers' pinned `checkpoint` function: `experiments/E049`, `experiments/ledger.jsonl`; commit; push to `day-7` under a 60 s timeout);
  4. only if E049 is COMPLETE: `uv run python scripts/run_experiment.py E050`;
  5. if E050 is COMPLETE: `uv run python scripts/route_check.py E050 E044 E049`;
  6. checkpoint of E050's own records (with `research/comparisons/route_check_E050.json`).
- It is started detached by the researcher on the owner's word: `setsid nohup bash research/day-07/sessions/D07-S01/run_e049_e050.sh`.
- **Pre-registered tree state (U3):** after E049's checkpoint, a WARNING listing only `orchestration/task-ledger.jsonl` (E049's unmasking line). E049 records `git_dirty_at_run: false`, and E050 records `true` with the task ledger as the only entry. Nothing is edited, staged or committed by hand while the script runs.
- **Unmasking (U4):** exactly one event each for E049 and E050, inside their run spans.
- **Freeze:** `git diff --stat 76e80f1 -- src scripts config pyproject.toml uv.lock` empty at the start (verified at this writing).
- **No other run.** After the script: `make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050` (P6; not a run), the P6 flag and the U8 (b) disclosure, then FROZEN (P7).

## Resolution

Closes when E049 and E050 are COMPLETE and checked, or when P4's fallback is invoked.

## The owner's word (2026-10-04T20:57:31Z)

- Owner (verbatim): "Begin experiment". The window opens now; the script is started immediately after this record is committed and pushed.
- Pre-start checks: script SHA-256 db6f7d883dc23ec8a43fb9270f6db445ff9314192b9e5a6547b9eaf4d2a4dced (equals the pin); freeze diff from `76e80f1` over `src scripts config pyproject.toml uv.lock`: empty; E049 and E050 ALLOCATED; GPU not used.
