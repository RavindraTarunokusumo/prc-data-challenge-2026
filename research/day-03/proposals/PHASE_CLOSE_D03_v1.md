---
schema: phase-close-proposal-v1
proposal_id: PHASE_CLOSE_D03
proposal_version: 1
day: 3
session: D03-S01
exchange_id: X-D03-S01-0003
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-09-30T06:42:02Z
---

# Day 3 phase close

## Request

1. **Adversarial review** of the Day 3 decisions (advisor policy: "try to show that the current champion is wrong"). In particular, try to show that **E019 (H015 v2) should not be promoted.**
2. **A ruling on the Day 3 holdout access** (frozen `phase_close` rule: at most one access, the phase-closing champion against the phase-opening champion on H, with a revert on LOSS).
   - **I propose one access: `holdout_check.py` E019 against E005** on H (December 2025), recording the reason "Day 3 phase close: H015 v2 promotion".
   - WIN or TIE: E019 becomes champion. LOSS: the promotion is reverted and E005 stays.
   - E020 (H016 v2) and E021 (H017 v2) are never NEW (rule 9) and are not in the access.
3. **Record corrections** before `DAY_SUMMARY.md` is finalised.

## Decisions under review

| Step | Experiment | Hypothesis | Decision | Evidence |
|---|---|---|---|---|
| — | E005 | H004 ridge (Day 1) | champion (incumbent) | Day 1 records |
| 1 | E019 | H015 v2, routed LightGBM on FS2 | Clauses 1, 2, 4 not met | `experiments/E019/analysis.md`; `E019_vs_E005.json`; `E019_vs_E017_mech_*.json` |
| 2 | E020 | H016 v2, R ablation | H015 clause 3 not met (bit-identical outside the routed rows, cross-container); disclosures | `experiments/E020/analysis.md`; `route_check_E019.json`; `E020_vs_*.json`; `E019_vs_E020_mech_LIRF_NM_missing.json` |
| 3 | E021 | H017 v2, P/T | Readings 1 and 2 below the floor (not supported / not distinguishable) | `experiments/E021/analysis.md`; `E021_vs_E017*.json`; `E020_vs_E021_mech_*.json` |
| 4 | E022 | H015 v2 reproduction (seed 43) | **Criterion 6 PASS; byte-identical predictions** | `experiments/E022/analysis.md`; `repro_E022_of_E019.json` |

Summary: `research/day-03/DAY_SUMMARY.md` (draft). Journal: `research/EXPERIMENT_JOURNAL.md`. Ledger: `experiments/ledger.jsonl`.

## Case for promoting E019

- **Every pre-registered clause and criterion that can be checked before the phase close holds:**
  - clause 1 not met, since criteria 1–3 pass against E005 (−38.23 s, 7/7 WIN, no degraded airport);
  - clause 2 not met, since C is −6.75 s with 7/7 WIN and the bulk is negative on every development fold;
  - clause 3 not met, since the routing is exact;
  - clause 4 not met, since criterion 8 is 0.0;
  - criterion 6 passes, with byte-identical files.
- **The margin over E005 is mostly bulk:** NM-present bulk −48.9 to −55.4 s on every development fold. It is not tail-driven: the tail share is 0.300, and the top-row shares are ≤ 0.10.
- **Its routed subgroup carries no convention bet,** so the ranking-month risk that decided Day 2 is removed there.

## Case against: where I may be wrong

1. **C clears the floor by 0.75 s.** The bootstrap q95 of the mean is −5.97 s, 0.03 s inside the floor. The Advisor forecast −3 to −5 s.
   - The promotion does not rest on C: clause 1 is −38.23 s and is mostly the routed Tier 1 structure.
   - But the Day 3 **mechanism** claim (congestion) rests on a thin margin over a floor I set myself (3 × 1.96 s).
2. **The routing costs 122.5 s on the 2025 folds.** E020, the unrouted twin, is far more accurate on every fold (development mean 321.95 against 444.49).
   - Promoting E019 locks in a model that is much worse than an available one on all 2025 evidence, on the argument that the 2026 LIRF convention rate is not estimable.
   - If the Advisor judges that argument too weak to carry a 122 s cost, the right response is not to promote E020 (it is not a candidate and never NEW). It is to say so, so that Day 4 can propose an unrouted candidate properly.
3. **E020's criterion 8 statistic is inside the bound on every development fold** (S1 +4,292 s). The Day 2 reason for routing (criterion 8 failure) no longer holds for FS2 unrouted. The remaining reason is forward risk only.
4. **Extreme predictions on NM-missing rows at the nine non-LIRF airports** (−8,859 s on EHAM row 197540199). E019 loses to E005 in bulk on that group on R1, R2, R3, W1 and W1c (rule 7 sign disagreement), and these rows are not routed.
   - Their 2026 share rose at those airports in January (1.66 % against 0.97 %).
   - E019 may carry a ranking-month risk that E005 does not. Criterion 3 passes on the development folds, but the group is small there.
5. **Holdout H is December 2025.** H015's routed subgroup has 88 rows there (0.73 % of LIRF DEP rows). A WIN on H is expected from the development pattern; it would not test the January-2026 shift in finding 4.

## Known weaknesses to attack

1. **Researcher evidence failures:**
   - the v1 false forward-risk counts;
   - the v1 false P-label claim;
   - the noise scale on the wrong population;
   - three missed H016/H017 predictions (DAY_SUMMARY §7).
2. **Process:**
   - two container restarts, one killing an Advisor run that was retried under the contract;
   - a transient approval outage, which delayed a checkpoint;
   - E019's analysis committed after the second restart, with predictions re-verified;
   - the EDA P figures were computed with the v1 code (0.086 % of rows differ).
3. **INC-0004 is open:** the launch arguments (`--model claude-sonnet-5-5 --effort medium`) disagree with the session metadata (served `claude-opus-5-5`, effort `high`).
4. **The code freeze held** from the H015 allocation (`7e9c431`) to the last comparison: `git diff --stat 7e9c431 HEAD -- src scripts pyproject.toml uv.lock` is empty. Please verify.

## Resource Estimate

No experiment. Review only (read-only). The holdout access, if ruled, is one `holdout_check.py` call after the ruling and the ack.

## Decision Requested From Advisor

ACCEPT (promote E019 subject to the H access; E005 restored on LOSS) | REVISE | REJECT | HOLD
