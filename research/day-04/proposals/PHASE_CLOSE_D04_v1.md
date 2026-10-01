---
schema: phase-close-proposal-v1
proposal_id: PHASE_CLOSE_D04
proposal_version: 1
day: 4
session: D04-S02
exchange_id: X-D04-S02-0001
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-10-01T01:31:06Z
---

# Day 4 phase close

## Request

1. **Adversarial review** of the Day 4 decisions (advisor policy: "try to show that the current champion is wrong"). In particular:
   - **E019 remains champion.** No Day 4 promotion.
   - **H018 v2 (E023): mechanism holds, not promoted** (criterion 2: S1 TIE against E019).
   - **H019 v2 (E024): mechanism falsified, not promoted** (clauses 1(a) and 1(b); criterion 2: S1 TIE against E019).
   - **H020 v1: REJECT** (no run).
2. **A ruling on the Day 4 holdout access.**
   - The frozen `phase_close` rule compares the phase-closing champion with the phase-opening champion. On Day 4 both are **E019**, so the comparison would be E019 against itself (dRMSE ≡ 0, a TIE by construction).
   - **I propose not to access the protected holdout on Day 4** (0 of 1 used), as ruling H did on Day 2. E023 and E024 may never be NEW (rule 9).
   - If the Advisor rules that an access is nevertheless required, or that another comparison is admissible under the frozen rule, I will follow that ruling. I propose none myself.
3. **Record corrections** the Advisor finds necessary, appended before `DAY_SUMMARY.md` is finalised.
4. **The hand-off** (`docs/reproducibility/HANDOFF_D04.md`, draft at `ff16c8b`): check that it lets Days 5–7 reproduce E019 and carry the governance, and that it states E023's treatment and the CatBoost objections as open work, not as results.
5. **INC-0005 closure** at this phase close, with the delegated-work list (`DAY_SUMMARY.md` §8).

## Decisions under review

| Step | Experiment | Hypothesis | Decision | Evidence |
|---|---|---|---|---|
| — | E019 | H015 v2 (Day 3) | champion (incumbent) | Day 3 records |
| — | — | H020 v1 (CatBoost) | REJECT before any run | `research/day-04/advisor/H020_review_v1.md`; `acks/H020_ack_v1.md` |
| 1 | E023 | H018 v2, routed rows excluded from LightGBM training | clauses 1–3 not met; criterion 2 fails against E019 → **not promoted** | `experiments/E023/analysis.md`; `E023_vs_E019.json`; `E023_vs_E005.json`; `E023_vs_E019_mech_NM_present_excl_LIRF.json`; `range_check_E023.json`; `route_check_E023.json` |
| 2 | E024 | H019 v2, FS3 on E023's configuration | clauses 1(a), 1(b) met → **falsified**; criterion 2 fails against E019 → **not promoted** | `experiments/E024/analysis.md`; `E024_vs_E023_mech_*.json`; `E024_vs_E019.json`; `E024_vs_E005.json`; `range_check_E024.json`; `route_check_E024.json` |

Summary: `research/day-04/DAY_SUMMARY.md` (draft). Journal: `research/EXPERIMENT_JOURNAL.md`. Ledger: `experiments/ledger.jsonl`.

## Case for E019 remaining champion

The frozen rule decides it: no candidate met criteria 1–8.
- **E023** passes criteria 1 and 3 against E019 (−2.04 s, q95 −1.31) but S1 is TIE (+0.20).
- **E024** passes criteria 1 and 3 (−2.43 s, q95 −1.59) but S1 is TIE (+0.72), and its mechanism is falsified, which blocks it under B2 in any case.

## Case against: where I may be wrong

1. **The champion carries a defect with a known fix.**
   - E019 has 81 out-of-range predictions in the > 3 h band on `NM_missing_other` (D3-C2) and a January 2026 exposure beyond the 2025 range (D3-C3).
   - E023 removes it (5) and is better on all rows on 6 of 7 folds (5 WIN, 2 TIE), with no LOSS.
   - Holding E019 is correct under the rules, but the champion handed to Days 5–7 and to any submission still carries a mechanism that Day 4 has shown to be an artefact of the training set.
   - I do not propose to promote E023 (rule 10: no re-adjudication). I ask whether the hand-off should name E023's configuration as the matched base for Day 5 candidates, or whether that pre-empts a Day 5 proposal.
2. **S1 is decided by one row in every Day 4 comparison against E019** (192622644; `DAY_SUMMARY.md` finding 4).
   - Under the frozen twin rule, any change to the LightGBM's training set or features moves that row and S1 with it.
   - Criterion 2 may therefore be selecting on one convention-mixture row's response, not on the candidate's merit.
   - I do not propose a rule change; I ask the Advisor to judge whether this is a known limitation that Day 5 proposals should pre-register against (rule 6 already reads such folds as not decisive for mechanisms, but criterion 2 has no such reading).
3. **The H019 falsification may be learner-specific.** LightGBM already sees the keys as categoricals. The claim "priors add nothing" is made for FS3 on LightGBM with E017's parameters, not for priors in general (and not for CatBoost's own statistics).
4. **W1's LOSS (+1.63 s) may be staleness, not the block.** W1's validation priors are drawn mostly from months after February. Without W1, the 4-fold mean is −0.77 s, still far above the −3.0 s floor, so the falsification does not depend on W1.

## Known weaknesses to attack

1. **Evidence and records:**
   - D4-C1 (unmeasured v1 `created_utc`);
   - D4-C2 to D4-C6;
   - the `NM_present_LIRF` against-E023 figures in `E024/analysis.md` item 8(d) are derived as differences of two `compare.py` outputs against E019, not from a direct tool run.
2. **Process:**
   - a container restart between E023's allocation and run, during the owner's usage-limit pause; the allocation records were committed at D04-S02's start;
   - INC-0004 is still open (owner decision);
   - INC-0005 delegation: check that every delegated commit is listed and that no delegated work touched a proposal, ack, allocation or interpretation.
3. **Missed predictions** (`DAY_SUMMARY.md` §7): H019's mechanism and all-rows ranges; H018's > 3 h band (better than predicted), W1 `NM_present_LIRF` and S1 `NM_missing_other`.

## Resource Estimate

No experiment. Review only (read-only).

## Decision Requested From Advisor

ACCEPT (the decisions stand; no Day 4 holdout access) | REVISE | REJECT | HOLD
