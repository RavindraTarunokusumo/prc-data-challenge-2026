---
schema: advisor-review-v1
hypothesis_id: H037
proposal_version: 1
proposal_sha256: 8e9c3f39082af5e613ef2b25715a6c884b4235463928769f14004d99ab2c3966
exchange_id: X-D07-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.87
created_utc: 2026-10-03T20:50:26Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.87).** The shared findings and binding conditions U1–U10 are in `H035_review_v1.md` and apply here unchanged. **U3, U4, U9 (formatting and upload) and U10 bear most directly.**

**What H037 is.** The override combiner on the final folds. It takes E044's stored SUBMIT predictions and replaces the subgroup rows (107 in 2026-01, 276 in 2026-07) with E049's. It is the candidate's submission, and it is formatted only if H035 is promoted (U9). Otherwise E050 stays a recorded, unformatted run, and E044's file stands.

**Verified here.**
- The proposal hash matches the envelope.
- **Parsed YAML:** `model: override`, `base: E044`, `override: E049`, `subgroup: LIRF_NM_missing`, the two final folds, CLASS-S.
- **The worker's dispatch:**
  - takes the fold's validation rows with `MVT_ID_mvt`, `ADEP_mvt` and `flt_missing` from the FS0 frame;
  - `prc.blending.override` refuses a component that is not COMPLETE;
  - it verifies each prediction file against its manifest, joins 1:1 and refuses nulls;
  - it selects inside one frame, so row order cannot misalign it.
- **The formatter's override mode** (`scripts/make_submission.py`):
  - the components are read from the config as `[base, override]` and must match the arguments;
  - I4 requires every row to equal the override on the subgroup and the base elsewhere, within 1e-9 s;
  - its subgroup key (LIRF and `AOBT_3_flt` null) is the worker's `flt_missing` definition;
  - a misaligned mask can only produce a refusal, never a false pass. It uses the same left-join pattern as `route_check.py`, which passed on real data in this environment (E043).
- **`--tag`:**
  - it must be alphanumeric;
  - output goes to `predictions/final/<TAG>/submitting.parquet` and the record to `SUBMISSION_RECORD_<TAG>.json`;
  - the two new tests pass. The first shows the earlier file is byte-unchanged; the second shows refusals for a wrong source and for `../x`.
- **Real files:** the H035 review's smoke test exercised `prc.blending.override` on stored, manifest-verified files.
- **E044's recorded submission** is unchanged: SHA-256 `d57ff7db7dfa34e13934aa524464ea13dbe9f5f904fae400a85f87e62c95af73`, as in `SUBMISSION_RECORD.json`.

**Three points specific to H037** (non-blocking; recorded in its analysis).
1. **The record's `rms_half_difference` is not a quantity of the submission for an override.** It is E044 against E049 over all rows, including E049's non-subgroup rows. Those are never submitted and carry D3-C2 untreated. The analysis labels it as such.
2. **The flag's subgroup mean prediction is not in the record.** It is computed from the stored files, target-free (U9).
3. **E050 loads unmasked silver** because it lists final folds, as E044 did. It uses no target. Its event is recorded as U4 states.

## Scientific Validity

- **A procedure.** The candidate's construction applied to the SUBMIT fits.
- **Nothing is fitted.** No post-processing is added beyond the formatter's rounding (half to even, at most 0.5 s), as for E044.
- **No floor or clip.** That is correct, because the submitted predictor stays the evaluated construction.

## Novelty Relative to Existing Research

- **It is the only possible submission of H035.**
- **Rule 10 is not engaged:** E050 is not a candidate.

## Experimental Isolation

Against E044, only the subgroup rows differ. The route check `route_check.py E050 E044 E049` checks this:
- subgroup rows equal E049 within 1e-6 s;
- every other row equals E044 exactly.

## Validation Quality

- **Blocking:**
  - COMPLETE;
  - the route check;
  - U4's unmasking event;
  - if formatted, I1–I5.
- **Non-blocking:** the H035 §Batch subgroup flag, under S6 as U9 applies it.
- **The upload file and its hash** are fixed by U9 if, and only if, H035 is promoted. Otherwise S8 stands.

## Leakage Review

### Target Leakage

PASS

- The combiner reads stored, manifest-verified predictions and the target-free routing key.
- The formatter reads only target-free silver columns and the template.

### Temporal Leakage

PASS

The combiner adds no information beyond its components, which trained on 2025 months only.

### Competition Availability

PASS

If formatted, the output keeps the template's format, verified by I1–I5:
- 344,841 rows;
- `MVT_ID_mvt` Float64 and `TAXITIME_SEC_mvt` Int32;
- template order.

## Compute Review

### RAM

PASS

E044 peaked at 3.54 GB, under CLASS-S's 4 GB. E050 builds the same frame.

### Runtime

PASS

- E044 took 11.2 s.
- The 60 s guard requires a start by 00:59:00Z. The CLASS-S timeout is 450 s.

### Disk

PASS

- About 5 MB of predictions.
- If formatted, a git-ignored submission file of about 1 MB, covered by `SUBMISSION_RECORD_E050.json`.

## Weakest Assumption

**That the rows E050 takes from E049 are the predictions H035 evaluated.**
- I4 and the route check prove identity to E049.
- They cannot show that E049 was trained as intended. As for E044's halves, a defect shared with the final-fold path would go unseen.

## Missing Control or Ablation

None required.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

**Allocation:** exactly one `primary` allocation, `uv run python scripts/gate.py allocate H037 v1`, made sixth in the batch (expected **E050**, U1).

**Config:** the Proposed Change block, with `base: E044` and `override: <H036 id>`.

**When:** sixth in the queue of the pinned `research/day-07/sessions/D07-S01/run_window_2.sh`, after E049 is COMPLETE, in the 2026-10-04 00:00–01:00Z window (INC-0015), or later under U10.

**Integrity:** `route_check.py E050 E044 E049`, as the launcher runs it. A failure makes E050 INVALID (U10).

**Formatting:** `make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050`, only under U9, after the Day 7 phase close promotes H035 with objection F resolved.

**Upload:** under U9 and S6, once, after FROZEN, by the owner's decision.

**Status (U5):** not a candidate, never NEW, never scored; ledger decision null.

**Not authorized:**
- any other allocation;
- formatting before the phase close's promotion;
- any write to `predictions/final/submitting.parquet` or `SUBMISSION_RECORD.json`.

Required acknowledgement path: `research/day-07/acks/H037_ack_v1.md`.
- It references the proposal hash `8e9c3f39082af5e613ef2b25715a6c884b4235463928769f14004d99ab2c3966` and this review's hash.
- It adopts U1–U10 of `H035_review_v1.md` as binding.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement: not applicable. There is no truth, and nothing is scored.

| Event | P |
|---|---|
| E050 COMPLETE within CLASS-S, inside the window | 0.88 |
| `route_check.py E050 E044 E049` PASS, given COMPLETE (107 and 276 subgroup rows; max \|Δ\| 0.0 elsewhere) | 0.97 |
| If formatted, I1–I5 hold | 0.97 |
| Each month's subgroup share above 3,600 s lies inside H035 §Batch's flag band | 0.80 |

Expected magnitude:
- **Resources:** runtime 8–20 s; peak RSS 3.4–3.6 GB.
- **Subgroup mean prediction:** January's is higher than July's, and higher than on most development folds.

Primary expected failure mode:
- **Primary:** E050 is deferred with E049 (U10). The candidate's submission then waits for another owner window.
- **Secondary:** a refusal by I4, caused by a key mismatch between the worker's `flt_missing` and the formatter's `AOBT_3_flt` mask. This is unlikely, because both are `AOBT_3_flt` null.
