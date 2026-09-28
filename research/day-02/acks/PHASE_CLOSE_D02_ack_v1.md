# Acknowledgement — Day 2 phase close (exchange X-D02-S01-0006)

- proposal: `research/day-02/proposals/PHASE_CLOSE_D02_v1.md`, sha256 `958db1e83aff17fcf03a74fa228257d2723ab3468cf2fe31c0070afd67d85a3b`
- review: `research/day-02/advisor/PHASE_CLOSE_D02_review_v1.md`, sha256 `f3df7e551677c75c5fc0e37a426be870ad3098f3bdbd10a272f7036bea9c03b0`
- decision received: **ACCEPT** (confidence 0.90). Both hashes verified by the researcher.

## Decisions (standing)

- **E005 (H004 ridge)** is the phase-closing champion, **by rule**.
- **H009 v3:** INCONCLUSIVE (E012 primary, E015 reproduction; criterion 6).
- **H013 v2:** INCONCLUSIVE (E017; criterion 8; not reproduced).
- **Ablation and reference outcomes:** E013 (H010), E014 (H012), E016 (H011 v2) and E018 (H014 v2) keep them as recorded.
- **No retroactive promotion and no re-adjudication.**

## Rulings recorded

**H (holdout).**
- **Day 2: 0 of 1, closed unused.** It is not a TIE, because no comparison was made.
- The access does not carry over, and no substitute comparison is admissible.
- `holdout_check.py` is not run in this phase. No Day-2-allocated experiment (E012–E018) may be NEW in any phase.

**B (the criterion 8 bound, +6,500 s).**
- It is **not re-derived**: it caught the systematic worsening it was set to catch.
- S1 statistic, exact decomposition on the same rows:

  | E006 | E018 | E012 | E015 | E017 |
  |---|---|---|---|---|
  | +5,782 | +6,387 | +6,390 | +6,456 | +7,104 |

- The deterministic procedure (+605 / +714 s) and the static keys (+608 / +717 s) both worsen July.
- A Day 3 alternative resolution needs a forward-risk rationale that does not rest on E006–E018 outcomes. A new threshold on this statistic will not be accepted (rule 10).

**R (comparison base).**
- A comparison base is a matched reference, not a champion, and shares the candidate's training procedure.
- E017 is not the strongest model on all rows.
- Criteria 1–3 against E005 cannot test a Day 3 mechanism, so criterion 4 carries every mechanism claim.

## Corrections (appended; the proposal and completed records are not edited)

- **D2-C1. The margin over E005.** "~100 s on every fold" is false.
  - R2 is −60.9 / −65.2 s (E012 / E017), W1c −65.7 / −74.0 s, and E017's W1 −99.1 s.
  - LIRF NM-missing rows carry 0.17–0.73 of each fold's SSE change. The robust margin is **51.5–59.6 s on NM-present rows**.
  - On S1 and S1c, the subgroup's bulk loss exceeds the whole NM-present gain (1.13–1.63×), so the convention decides accuracy there too.
  - The claim that "E005 will score worse on the ranking months" holds only if the convention recurs in July 2026.
- **D2-C2. The static-structure answer.**
  - On the matched NM-present population: **−29.6 s** (E016 − E010) against **−9.1 s** (E012 − E006) and **−8.7 s** (E017 − E018).
  - **All rows:** −1.72 s (q95 +9.39) and −2.13 s (q95 +13.09). Criterion 1 fails in both, so **FS1 is not distinguishable from FS0 on the metric.**
  - What absorbs about 70 % is the **delta set** (`d_aobt3`, `d_eobt1`, `d_sched`, `flt_missing`), not the anchor alone.
  - W1c is LOSS for M1 in both procedures.
  - The "−52.1 s deterministic" M2 figure is a carry-over figure (a deterministic candidate against the bagged E014), not a deterministic M2 estimate.
- **D2-C3. Convention "dilution"** is reversed on S1 in both procedures (+608, +717 s) and on R3 under the deterministic procedure (+146 s). H013's criterion 8 failure comes from the procedure and the static keys together.
- **D2-C4. Seed variance.**
  - Excluding LIRF NM-missing rows, the E015 − E012 shift is still **+1.33 s on S1 and −1.94 s on W1** (W1 was not reported before). Only NM-present rows outside LIRF are within 1.0 s on every development fold.
  - "The only place where Tier 1 models are seed-unstable" is **withdrawn**. A treatment of that subgroup would not resolve a bagged model's criterion 6 exposure.
  - The bootstrap labels seed-only differences as WIN or LOSS.
- **D2-C5. Deterministic training** is free on NM-present rows only. On all rows it costs +2.67 s (FS1) and +3.08 s (FS0), with S1 and W1 LOSS for E017 − E012. Its determinism on real data is untested: a premise until a reproduction shows identical prediction files.
- **D2-C6. STATE.md was stale.** It was not updated at the E017 or E018 checkpoints, and still named "`gate.py allocate H013 v2` → run" as the next action. The E017 checkpoint also omitted its journal entry, which was added at `3f9dd7a`. This repeats Day 1's C6. It is refreshed in the phase-closing commit.
- **D2-C7. INC-0003 scope.** The researcher process that produced H009 v3–H014 v2, E012–E018 and the phase-close proposal carried `--effort medium`. No Day 2 analysis cited the incident. DAY_SUMMARY now states the scope. The incident remains open for the owner.
- **D2-C8. Missed expectations** (added to DAY_SUMMARY §7):
  - H009 v3: development mean 355–372 → 376.15; clause 1 −110 to −130 → −106.58; rule 8 tail share on R2 0.25 (band 0.3–1.1).
  - H013 v2: rule 8 bulk on S1 +7,104.4; tail share R2 0.28 and S1 1.17.
  - H011 v2: −8 to −30 → −30.03.
  - E015's development mean is 377.29.
- **D2-C9. Allocation from a dirty tree.** E013, E014 and E015 were allocated with uncommitted files, all output and record files only. Allocation should follow the checkpoint commit. There is no numerical effect.
- **D2-C10. Advisor record.** The criterion 6 exposure of a bagged model on day-scale folds was not sized before E012. The X-D02-S01-0005 fold-scale synthetic check is not in the repository.

## Standing rules adopted (from the next proposal onward)

9. **Protected-holdout access.**
   - An access is authorized only by a phase-close review that names the exact command.
   - NEW must be an experiment allocated in the phase being closed.
   - A phase that closes without a promotion closes its access unused. It does not carry over, and no later access may be attributed to that phase.
   - No `holdout_check.py` invocation with E012–E018 as NEW, in any phase.
10. **No re-adjudication of recorded outcomes.**
    - A proposal is not a new test, and will be rejected, if it:
      - re-submits a completed configuration unchanged as a promotion candidate (for a bagged model, with any seed); or
      - changes only a decision threshold, population or counting rule after the relevant outcome is recorded.
    - This covers E006, E012/E015, E017 and E018, and any criterion 8 threshold on `NM_missing_LIRF.delta_rmse_bulk`.
11. **Headline figures.**
    - In DAY_SUMMARY, STATE and the journal, a population-restricted effect is reported next to the all-rows figure of the same contrast.
    - Comparisons between contrasts use one population.
    - A statement that localises an effect to a subgroup reports every development fold.
