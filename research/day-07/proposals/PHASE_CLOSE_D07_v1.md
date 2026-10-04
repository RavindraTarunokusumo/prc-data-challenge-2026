---
schema: phase-close-proposal-v1
proposal_id: PHASE_CLOSE_D07
proposal_version: 1
day: 7
session: D07-S01
exchange_id: X-D07-S01-0003
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-10-04T17:35:34Z
---

# Day 7 phase close (and the project freeze)

## Request

1. **Adversarial review** of the Day 7 decisions (advisor policy: try to show that the champion is wrong). The decisions:
   - batch 1 (E042–E044): the champion's SUBMIT procedure; the submission file `d57ff7db…` passes I1–I5 with no flag;
   - batch 2: H035 (E046) meets criteria 1–4, 6 and the criterion 8 rule on the development folds; **objection F (U7) is open**; E049 and E050 are deferred.
2. **The Day 7 holdout access, named exactly as U7's statistic:**

   ```bash
   uv run python scripts/holdout_check.py E046 E033 --reason "Day 7 phase close (X-D07-S01-0003): phase-closing candidate E046 (H035 v1) vs phase-opening champion E033; objection F (U7 of X-D07-S01-0002)"
   ```

   It runs once, after this review's acknowledgement is committed, from a clean tree with the lock free. E046 is allocated in Day 7 and is NEW. No other run is NEW (U5).
3. **The pre-registered outcome mapping (U7, unchanged):**
   - **WIN:** objection F is resolved for December only, and H035 is PROMOTED. E046 becomes champion (`CURRENT.json`, a `champion_change` event); ledger decisions are E046 PROMOTE and E048 PROMOTE (reproduction).
     - E049 then E050 run unchanged in an owner-set window, recorded in a new incident (U10), by direct `run_experiment.py` calls in that order with the route check `E050 E044 E049`.
     - Then `make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050` (U9), with the H035 §Batch SUBMIT flag and the target-free per-month exposure (U8 (b)).
     - The final file is `predictions/final/E050/submitting.parquet`. U6 is stated in plain words to the owner before any upload.
   - **TIE:** H035 INCONCLUSIVE ("phase-close holdout TIE; forward bet not confirmed"). E033 stays champion, and E044's file is final.
   - **LOSS:** H035 INCONCLUSIVE ("phase-close holdout LOSS, frozen revert"). E033 stays champion, and E044's file is final.
   - **Under TIE or LOSS,** E049 and E050 stay ALLOCATED and are recorded "never run (not needed: H035 not promoted)". No substitute comparison follows.
4. **The FROZEN state (definition requested).** The project becomes FROZEN at one commit that contains all of:
   - `research/STATE.md` with **Phase: FROZEN**, the final champion, and the final submission file's path and SHA-256;
   - a task-ledger event `{"event": "frozen", "submission": <path>, "submission_sha256": <hex>, "champion": <E###>}`;
   - `docs/reports/FINAL_REPORT.md` (final);
   - `research/day-07/DAY_SUMMARY.md` (FINAL).

   After FROZEN: no new allocation, run or record change except appended corrections. The submission bucket may then be written **once, by the owner's decision**, with the recorded file unmodified (LEADERBOARD_POLICY). The researcher does not upload. Any leaderboard figure is recorded afterwards as an external evaluation only and is never fed back.
   - Under WIN, FROZEN comes after E050's formatting and the closure of any flag analysis (S6, U9).
   - Under TIE or LOSS, it comes right after this phase close's records.
5. **Record corrections** D7-C1 to D7-C5 (DAY_SUMMARY §7), and any the Advisor finds.
6. **Incidents:**
   - INC-0014 closes (its window is complete; no deviation).
   - INC-0015 closes under TIE or LOSS; under WIN it closes once E049 and E050 are COMPLETE.
   - INC-0004, INC-0009 and INC-0010 stay open; the final report lists them.
7. **The final report draft** `docs/reports/FINAL_REPORT.md`, for accuracy: no figure may be quoted as the submission's expected error (S9, U6).

## Decisions under review

| Step | Experiment | Proposal | Decision | Evidence |
|---|---|---|---|---|
| — | E033 | H023 v3 | phase-opening champion | Day 5 records |
| 1–3 | E042, E043, E044 | H031–H033 v1 | SUBMIT procedure: integrity holds; no flag | `experiments/E04{2,3,4}/analysis.md`; `route_check_E043.json`; `research/day-07/submission/SUBMISSION_RECORD.json` |
| 4 | E045 | H034 v1 | component; reproduces E020 | `experiments/E045/analysis.md` |
| 5 | **E046** | **H035 v1** | **criteria 1–4, 6, criterion 8 rule met; objection F open** | `experiments/E046/analysis.md`; `E046_vs_E033.json` (and E034, E041, E028); `E046_vs_E033_mech_LIRF_NM_missing.json`; `E046_exposure_U8.json`; `range_check_E046.json`; `range_check_forward_D07.json`; `route_check_E046.json` |
| 6–7 | E047, E048 | H034/H035 reproductions | byte-identical; criterion 6 PASS | `repro_E048_of_E046.json`; `route_check_E048.json` |
| 8–9 | E049, E050 | H036, H037 | DEFERRED | `research/day-07/sessions/D07-S01/run_window_2.log` |

## Case for the decisions

- Every reading follows its pre-registered rule with per-fold values beside it. The candidate's development figures match the pre-registered derivation to 0.05 s per fold.
- Every run passed integrity, ran inside its window and within class, and had an empty freeze diff. S3, S4, U3 and U4 held.
- U7 makes the candidate's promotion depend on the only fresh evidence available. It is stricter than the frozen rule, and it was pre-registered before any result.

## Case against: where I may be wrong

1. **The candidate's gain is a recording convention, not taxi physics.** It forecasts the recorded target better, and the competition scores the recorded target. If LIRF's 2026 records follow a different convention, or the data provider cleans them, the loss is of the gain's size (U6).
2. **H has 88 subgroup rows,** and the candidate differs from E033 only there. A December WIN is a subgroup result, decided by a few tail rows (rule 6). December also sits next to the training months, whereas July 2026 is seven months away and January 2026's subgroup delay tail is heavier than any 2025 month's.
3. **Selection.**
   - The candidate was chosen knowing E020's recorded results. Its development result was predictable to 0.05 s, so the development folds carry no confirmatory weight (U6).
   - It was raised late, on Day 7, after the SUBMIT batch. The owner chose among options I wrote and recommended (INC-0015).
   - The idea had been admissible since Day 4 and was not pursued until the final-report review surfaced it.
4. **The SUBMIT procedure is untested** (12 months; one CatBoost draw). January 2026 sits close to two sanity limits.
5. **Process:**
   - the forward-risk misstatement to the owner (D7-C3) and a factual slip in chat (D7-C5);
   - pre-written timestamps (D7-C2);
   - a guard underestimate that deferred two runs (D7-C4);
   - W&B mirror failures on E042, E043 and E045–E048 (INC-0009).
6. **The criterion 8 reference:** E033's routed ridge differs from E028 by up to 191 s on single rows (R3). The rule holds against both.

## Known weaknesses to attack

- `prc.blending.override` and the formatter's override mode are new Day 7 code (tested; reviewed by the Advisor in X-D07-S01-0002).
- The launcher checkpoints are scripted commits.
- The FROZEN definition is new; nothing in the code enforces it beyond the gate's ledger.

## Resource Estimate

Read-only review, then one `holdout_check.py` (seconds; reads H truth once, after the acknowledgement).

## Decision Requested From Advisor

ACCEPT (the decisions stand; the Day 7 access is named as above; the outcome mapping and the FROZEN definition apply) | REVISE | REJECT | HOLD
