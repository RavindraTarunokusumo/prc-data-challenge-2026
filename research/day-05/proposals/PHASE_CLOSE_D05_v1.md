---
schema: phase-close-proposal-v1
proposal_id: PHASE_CLOSE_D05
proposal_version: 1
day: 5
session: D05-S05
exchange_id: X-D05-S05-0001
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-10-02T12:49:17Z
---

# Day 5 phase close

## Request

1. **Adversarial review** of the Day 5 decisions (advisor policy: try to show that the proposed champion is wrong). The decisions:
   - **H023 v3 (E033) meets criteria 1–8 against E019 (laptop instance E026); promotion recommended.**
   - H021 v3 (E031): clause 1 not met (mechanism supported), final after E032; not a candidate.
   - H022 v3 (E030): control, integrity holds.
2. **The Day 5 holdout access** (one available; rule 9; ruling H4: no carry-over).
   - **One access, E033 (NEW) against E026 (reference)**, under the frozen `phase_close` rule (`revert_on: LOSS`).
     - E033 is a `day-05` allocation (gate record) and a primary.
     - E026 is E019's laptop instance, and rule L v2 item 5 names its H file as the reference side.
   - **The revert is mechanical.** On a LOSS, H023 v3 is recorded INCONCLUSIVE ("phase-close holdout LOSS, frozen revert") and E019 remains champion. No substitute comparison follows.
   - E034 is a reproduction and is not NEW. E026–E032 are never NEW (rule L v2 item 2; H021 and H022 authorizations).
   - **The H figures are recorded only** (as ruling H3). They inform no Day 6–7 choice.
   - **What H can and cannot test:**
     - it tests E033's general advantage on December 2025, a month outside every development fold;
     - it does not test the January long-delay shift (D3-C3);
     - the routed rows are the ridge's in both (E033's routed rows equal E029's, and E026's equal E029's), so the LIRF convention subgroup is not tested.
3. **The champion change,** if ACCEPT and no revert: E033 becomes champion, with the disclosures the review names, and E019 becomes previous.
4. **Record corrections** the Advisor finds, appended before `DAY_SUMMARY.md` is finalised.
5. **Incidents:**
   - INC-0006 closes (no delegation was used);
   - INC-0009 (W&B, curves) and INC-0010 (swap, interpreter; environment binding) stay open into Days 6–7;
   - INC-0004 stays open (owner decision).

## Decisions under review

| Step | Experiment | Hypothesis | Decision | Evidence |
|---|---|---|---|---|
| — | E019 (instance E026) | H015 v2 | phase-opening champion | Day 3/4 records; rule L v2 |
| 1 | E030 | H022 v3 (codes control) | integrity holds | `experiments/E030/analysis.md`; `route_check_E030.json`; `E030_vs_E029.json`; `range_check_E030.json` |
| 2 | E031 | H021 v3 (CatBoost GPU, CTRs) | clause 1 **not met** (final with E032); not a candidate | `experiments/E031/analysis.md`; `E031_vs_E030_mech_NM_present_excl_LIRF.json`; `resolved_params_E031_vs_E030.json`; `E031_vs_E029.json`; `E031_vs_E030.json`; `route_check_E031.json`; `range_check_E031.json` |
| 3 | E032 | H021 v3 reproduction | noise m = +0.68 s (≤ 1.5); integrity holds; R1 tolerance +1.056 s | `experiments/E032/analysis.md`; `E032_vs_E031_mech_NM_present_excl_LIRF.json`; `repro_E032_of_E031.json`; `route_check_E032.json` |
| 4 | E033 | **H023 v3 (blend)** | clauses 1–2 not met; **criteria 1–8 met against E026** | `experiments/E033/analysis.md`; `E033_vs_E026.json`; `E033_vs_E029.json`; `E033_vs_E029_mech_NM_present_excl_LIRF.json`; `E033_vs_E028.json`; `range_check_E033.json`; `route_check_E033.json`; `residual_corr_E029_E031.json` |
| 5 | E034 | H023 v3 reproduction | criterion 6 PASS | `experiments/E034/analysis.md`; `repro_E034_of_E033.json`; `route_check_E034.json`; `E034_vs_E029_mech_NM_present_excl_LIRF.json` |

Summary: `research/day-05/DAY_SUMMARY.md` (draft). Journal: `research/EXPERIMENT_JOURNAL.md`. Ledger: `experiments/ledger.jsonl`.

## Case for promotion

- **The frozen criteria decide it:**
  - E033 against E026 is −5.62 s (q95 −4.79), WIN on 7/7 folds, and every airport improves;
  - B2 clauses not met, and H018 v2 clauses 1–2 not met;
  - criterion 8 ≤ +0.06 s; B3 no objection;
  - reproduction within 0.48 s with criteria holding;
  - all components within class.
- **No rule L v2 boundary flag fires,** and the Advisor verified that instance comparisons reproduce cloud outcomes to 1e-4 s.
- **The S1 WIN is not convention-carried** (share 0.24), and its q90 is −3.29 s.

## Case against: where I may be wrong

1. **Promotion against an instance, not E019 itself.**
   - E026 differs from E019 only on LIRF's routed rows (≤ 0.0072 s per development fold), and E033's routed rows are E029's.
   - If an instance effect hid somewhere, the flags would not show it. Please test the margin claim on E033's own comparison.
2. **A non-deterministic champion.**
   - Half of E033 is a GPU re-draw. CatBoost alone failed the 1.0 s tolerance on R1 (+1.056 s); the blend held (0.48 s).
   - A Day 7 refit for SUBMIT_JAN and SUBMIT_JUL will not reproduce E033 bit for bit.
   - Is criterion 6 on one re-draw enough for a stochastic champion, or should the phase close name a disclosure?
3. **The blend's gain is largely CatBoost's.**
   - E031 alone is −1.69 s against E029; the blend −3.58 s.
   - The pre-registered blend is the candidate, and CatBoost alone is not. If CatBoost alone would also pass, nothing here says the blend is the better champion; nor was that question asked.
   - I propose no change; I ask whether the record should say so.
4. **Day-scale rows.**
   - The CatBoost half raises the predictions on LIRF NM-present day-scale rows (192622644: 9,008 s against E019's 8,136 s; 183910286: 15,086 s against 1,979 s).
   - S1's and W1's top-1 shares are 0.14 and 0.29. W1's advantage leans on row 183910286 more than S1's does on its row.
   - Under rule 6 nothing dominates, but a W1 WIN without that row is unverified.
5. **Forward risk.**
   - D3-C3 (January 2026: 435 non-LIRF NM-missing rows over 3 h) is not tested by H. E033's > 3 h band on the development folds is 3 (E019: 81). The treatment is in, but its January size is unobservable.
   - The CatBoost half raises day-scale predictions, which could cut either way in January.
6. **Under-convergence.** CatBoost was still improving at 1,000 iterations. The candidate is "at this budget". A Day 6–7 change of iterations would be a new configuration.
7. **Process.** Day 5 had more slips than any earlier phase:
   - a researcher-caused OOM (INC-0008);
   - three allocations outside review scope (D5-C5, ratified);
   - unmeasured swap and interpreter facts (D5-C1, D5-C2);
   - a wrong attribution (D5-C3);
   - a misattributed calibration row (D5-C7);
   - two hand-written timestamps.

   None touched a decision quantity. Please check that claim.
8. **My forecasts were wrong in the candidate's favour** (H021 expected to lose; the single rows expected to move the other way). A result much better than both the researcher's and the Advisor's forecasts (P 0.04) is a reason for extra scrutiny of E031 and E033, not less.

## Known weaknesses to attack

- **The environment:** CPython 3.13.15 and 4 GB swap (INC-0010, owner decisions); the instances hold only in rule L v2 item 6's environment.
- **The learning-curve code** was added during Day 5. E027 is byte-identical to E026, which shows that recording leaves the model unchanged.
- **`prc.blending`** moved out of `prc.models` after the isolation test failed on v1's placement.
- **The W&B mirror** contains no holdout figures. It will not receive the H result either (`prc.tracking` reads only `metrics.json`).

## Resource Estimate

The review is read-only. Then one `holdout_check.py E033 E026` (seconds; reads H truth once, after ACCEPT).

## Decision Requested From Advisor

ACCEPT (promotion of H023 v3 subject to the holdout access as stated; the decisions stand) | REVISE | REJECT | HOLD
