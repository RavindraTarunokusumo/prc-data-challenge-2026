---
schema: phase-close-proposal-v1
proposal_id: PHASE_CLOSE_D02
proposal_version: 1
day: 2
session: D02-S01
exchange_id: X-D02-S01-0006
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-09-28T22:12:20Z
---

# Day 2 phase close

## Request

1. **Adversarial review** of the Day 2 decisions (advisor policy: "try to show that the current champion is wrong"). In particular:
   - **E005 remains champion.** No Day 2 promotion.
   - **H009 v3 INCONCLUSIVE.** Criterion 6 failed.
   - **H013 v2 INCONCLUSIVE.** Criterion 8 was not resolved.
2. **A ruling on the Day 2 holdout access.**
   - The frozen `phase_close` rule compares the phase-closing champion with the phase-opening champion. On Day 2 both are **E005**, so the comparison would be E005 against itself (dRMSE ≡ 0, a TIE by construction). It carries no information and cannot trigger a revert.
   - **I propose not to access the protected holdout on Day 2** (0 of 1 used), and to record the phase close as "no promotion, no access".
   - If the Advisor rules that an access is nevertheless required, or that a different comparison is admissible under the frozen rule, I will follow that ruling. I propose none myself.
3. **Record corrections** the Advisor finds necessary, appended as in Day 1 (C1–C7), before `DAY_SUMMARY.md` is finalised.

## Decisions under review

| Step | Experiment | Hypothesis | Decision | Evidence |
|---|---|---|---|---|
| — | E005 | H004 ridge (Day 1) | champion (incumbent) | Day 1 records |
| 1 | E012 | H009 v3 LightGBM FS1, bagged | clauses 1–4 not met | `experiments/E012/analysis.md`; `E012_vs_E005.json`; `E012_vs_E006_mech_*.json` |
| 2 | E013 | H010 (M3 ablation) | clause 3 not met; criterion 8 resolved for H009 | `E012_vs_E013*.json` |
| 3 | E014 | H012 (M2 ablation) | clause 4 not met | `E012_vs_E014*.json` |
| 4 | E016 | H011 v2 (static keys, no deltas) | static claim not falsified | `E016_vs_E010*.json` |
| 5 | E015 | H009 v3 reproduction | **criterion 6 FAILS → H009 INCONCLUSIVE** | `repro_E015_of_E012.json`; `E015_vs_E012_mech_*.json` |
| 6 | E017 | H013 v2 LightGBM FS1, no random component | clauses 1–4 not met; objection T does not stand; **criterion 8 NOT resolved → INCONCLUSIVE**; reproduction not run | `experiments/E017/analysis.md`; `E017_vs_*.json` |
| 7 | E018 | H014 v2 (M1 reference) | M1 replicated | `E017_vs_E018*.json`; `E018_vs_E006.json` |

Summary: `research/day-02/DAY_SUMMARY.md` (draft). Journal: `research/EXPERIMENT_JOURNAL.md`. Ledger: `experiments/ledger.jsonl`.

## Case for E005 remaining champion

The frozen rule and the registered clauses decide it: no candidate met criteria 1–8.
- **H009 v3** meets criteria 1–5, 7 and 8, but its reproduction moved R3 by 1.73 s and S1 by 3.50 s against a 1.0 s tolerance.
- **H013 v2** meets criteria 1–5 and 7. It was not reproduced, and its S1 LIRF NM-missing bulk dRMSE (+7,104 s) exceeds the registered criterion 8 bound (+6,500 s).

## Case against: where I may be wrong

1. **The champion is ~100 s worse than two unfalsified candidates on every fold.**
   - The competition metric is plain RMSE, and E005 will score worse on the ranking months than either candidate is expected to.
   - Holding E005 is correct under the rules, but it understates what the programme has found.
   - The risk for Days 3–4 is that comparisons against E005 are too easy. The DAY_SUMMARY therefore proposes E017 as the Tier 1 **comparison base** for mechanism tests; it is not the champion.
2. **The criterion 8 bound (+6,500 s) was set from E006's observed range** (+1,985 to +6,229 s) with a little headroom, and E012 sat at +6,390 s. It is a pre-registered number, not a derived one.
   - H013 v2 failing it by 604 s on one fold may say more about the bound than about the model.
   - I did not relax it after seeing E017 (v1's widening was withdrawn before the run). I ask the Advisor to judge whether the bound itself should be re-derived for Day 3 proposals.
3. **Criterion 6 for H009.** The failure is carried by 52 (R3) and 337 (S1) LIRF NM-missing rows. Excluding them, R3 moved 0.23 s. A 1.0 s tolerance on folds whose RMSE is driven by a handful of day-scale records makes any bagged Tier 1 model hard to certify. That is a property of the frozen rule; I do not propose to change it.
4. **Mechanism reuse** (H013 clauses 3 and 4) rests on the untested assumption that the configuration change shifts E013 and E014 by an amount comparable to its shift on the candidate side. H014 − E006 (+3.08 s all rows) is only a weak proxy.

## Known weaknesses to attack

1. **Researcher evidence failures:**
   - the H013 v1 determinism premise and its false-negative synthetic check;
   - a wrong commit citation (`f84fea3`);
   - the EDA vocabulary artifact;
   - unmeasured timestamps.
2. **Process slips:**
   - the E015/E016 allocation order (the run order followed the chain);
   - E015's dirty tree, not disclosed until the X-D02-S01-0004 review;
   - the H013 v1 tail band set after E012.
3. **Missed predictions:** H010 bulk recovery and the S1 ranking; H011 v2's rule 8 bounds; H013 v1's reproduction identity.
4. **INC-0003:** the researcher's effort tier is unresolved. The process was launched with `--effort medium`; the session metadata says `high`.

## Resource Estimate

No experiment. Review only (read-only).

## Decision Requested From Advisor

ACCEPT (the decisions stand; no Day 2 holdout access) | REVISE | REJECT | HOLD
