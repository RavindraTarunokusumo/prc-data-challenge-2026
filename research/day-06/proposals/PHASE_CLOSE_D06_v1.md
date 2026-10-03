---
schema: phase-close-proposal-v1
proposal_id: PHASE_CLOSE_D06
proposal_version: 1
day: 6
session: D06-S01
exchange_id: X-D06-S01-0004
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-10-03T16:06:52Z
---

# Day 6 phase close

## Request

1. **Adversarial review** of the Day 6 decisions (advisor policy: try to show that the champion is wrong). The decisions:
   - **E033 remains champion.** Day 6 had no candidate.
   - Batch 1 (ladder, E035–E039): rung B "statistics carry part"; rung C "combinations carry part" (with the closed-set disclosure); rung A "twin does not reproduce the gain"; H024's own reading INCONCLUSIVE (closed set).
   - Batch 2 (E040–E041): "robust to one further fixed-seed (GPU-only) draw".
2. **A ruling on the Day 6 holdout access.**
   - The frozen `phase_close` rule compares the phase-closing champion with the phase-opening champion. Both are **E033**, so the comparison would be E033 against itself (a TIE by construction).
   - E035–E041 are never NEW (X-D06-S01-0001 ruling, extended by X-D06-S01-0003).
   - **I propose not to access the protected holdout on Day 6** (0 of 1 used), as rulings H (Day 2) and H4 (Day 4). No carry-over (rule 9).
3. **Disclosures on E033** (DAY_SUMMARY D6 §5): the attribution finding and the three-draw record, worded under C5 and N4/N5.
4. **Record corrections** D6-C1 to D6-C5 (DAY_SUMMARY D6 §7), and any the Advisor finds, appended before `DAY_SUMMARY.md` is finalised. D6-C5 is an appended correction to the Day 5 summary's "a second learner family adds signal".
5. **Incidents:**
   - INC-0012 (run window) closes: its windows are complete and no deviation occurred; future run timing follows the owner's next instruction;
   - INC-0013 (delegation) closes with the delegated-work list (one script);
   - INC-0009 (W&B; the post-analysis re-sync of E035–E039 timed out), INC-0010 (environment binding) and INC-0004 stay open.

## Decisions under review

| Step | Experiment | Proposal | Decision | Evidence |
|---|---|---|---|---|
| — | E033 | H023 v3 (Day 5) | phase-opening champion | Day 5 records |
| 1 | E035 | H026 v2 (rung B) | statistics carry part | `experiments/E035/analysis.md`; `E035_vs_E033_mech_NM_present_excl_LIRF.json`; `E035_vs_E029*.json`; `E035_vs_E033.json`; `route_check_E035.json` |
| 2 | E036 | H024 v2 | INCONCLUSIVE (closed set) | `experiments/E036/analysis.md`; `research/day-06/eda/closed_set_E036_vs_E031.json`; `E036_vs_E031_mech_*.json`; `E036_vs_E030_mech_*.json`; `E036_vs_E029.json` |
| 3 | E037 | H025 v2 (rung C) | combinations carry part (closed-set disclosure) | `experiments/E037/analysis.md`; `E037_vs_E033*.json`; `E037_vs_E029*.json` |
| 4 | E038 | H027 v2 | component | `experiments/E038/analysis.md`; `E038_vs_E029.json` |
| 5 | E039 | H028 v2 (rung A) | twin does not reproduce the gain | `experiments/E039/analysis.md`; `E039_vs_E033*.json`; `E039_vs_E029*.json` |
| 6 | E040 | H029 v1 | pure fixed-seed re-draw | `experiments/E040/analysis.md`; `closed_set_E040_vs_E031.json`; `E040_vs_E031*.json`; `diversity_E031_draws.json` |
| 7 | E041 | H030 v1 | robust to one further fixed-seed draw | `experiments/E041/analysis.md`; `E041_vs_E026.json`; `E041_vs_E033*.json`; `E034_vs_E033.json`; `E041_vs_E034*.json`; `diversity_E033_draws.json` |

Diagnostics: `research/day-06/eda/diversity_E029.json`, `range_check_D06_blends.json`, `range_check_E040_E041.json`. Summary: `research/day-06/DAY_SUMMARY.md` (draft). Journal: `research/EXPERIMENT_JOURNAL.md` (Day 6 sections). Ledger: `experiments/ledger.jsonl`.

## Case for the decisions

- Every reading follows its pre-registered rule (C5, N5) on the stated population, with per-fold values beside it.
- All seven runs passed integrity, ran within class, with a clean tree and empty freeze diffs.
- No run was a candidate; nothing was promoted; no threshold moved.

## Case against: where I may be wrong

1. **Equal weight only.** Every ladder reading is at E033's 0.5/0.5 construction. A weaker second half is penalised by the fixed weight; "carries part" for rung B includes E030's weaker accuracy.
2. **Rung C rests on a run outside its closed set.** `data_partition` differs (DocParallel against FeatureParallel), chosen by CatBoost. I recorded rung C's reading with the disclosure, as pre-registered, but the Advisor may judge it should be INCONCLUSIVE too.
3. **One draw per CatBoost rung.** Rungs B and C each hold one GPU draw; the 1.0 s threshold is about four times the measured blend re-draw mean, but W1 moved 1.28 s in a blend re-draw, and rung C's largest fold contrast is W1 (+3.81 s).
4. **Batch 2 had little power**, and E040 measures only fixed-seed GPU variation.
5. **Day 6 did not attack** the SUBMIT procedure or D3-C3; the strongest open risks to the final claim are untested.
6. **Process:** batch 2 ran outside the original window at the owner's instruction; I assumed and then withdrew a standing window; one lint-failing commit; v1 errors (D6-C1) and a misdescription (D6-C2).
7. **The external GPU holder** on 2026-10-02 (4.3–5.2 GB) during E036: E036's resolved `data_partition` might depend on available GPU memory. If so, the closed-set violation is an environment effect.

## Known weaknesses to attack

- The delegated diagnostics script (INC-0013), reviewed by me only.
- The launcher's checkpoint commits are made by a script, not by hand.
- Rule L v2 item 6's environment held throughout (manifests record it); INC-0010 stays open.

## Resource Estimate

Read-only review. No holdout access is proposed.

## Decision Requested From Advisor

ACCEPT (E033 remains champion; Day 6 holdout closed unused; the decisions stand) | REVISE | REJECT | HOLD
