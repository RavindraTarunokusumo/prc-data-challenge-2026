## Phase-close review X-D02-S01-0006: ACCEPT (confidence 0.90)

The Day 2 decisions stand: E005 stays champion, and H009 v3 (E012/E015) and H013 v2 (E017) are INCONCLUSIVE. There is no Day 2 holdout access. Before `DAY_SUMMARY.md` is finalised, the acknowledgement must append ten corrections (D2-C1 to D2-C10) and adopt standing rules 9–11. None of the corrections changes a decision.

The proposal hash matches the envelope (`958db1e8…`), and every integrity check passed. All checks were read-only: no December target was read, `holdout_check.py` was not run, and no model was fitted or scored. The review file is the only file I wrote.

### Attack on the champion
- **Could a Day 2 candidate have been promoted? No.** Both blocking facts re-verify from the ledger and the committed comparison files, and the frozen rules leave no discretion:
  - H009 v3 fails criterion 6: the seed-43 rerun moved R3 by 1.727 s and S1 by 3.503 s, against a 1.0 s tolerance.
  - H013 v2 fails criterion 8: its S1 bulk loss on LIRF NM-missing rows is +7,104.4 s against the +6,500 s bound, and it has no reproduction.
- **Is E005 the wrong model to hold? Partly.**
  - Against E005: on NM-present rows (98–99 % of each fold), every Tier 1 fit beats it by 51.5–59.6 s on every development fold. It is champion by rule, not the most accurate model.
  - For E005, and new: on S1 (the July analogue), the candidates' loss on 218 LIRF NM-missing normal-taxi rows is 1.38× (E012) and 1.63× (E017) their whole gain on NM-present rows. Their S1 WIN rests on 119 convention rows, and ten rows carry 0.69–0.75 of the change.
  - So "E005 will score worse on the ranking months" holds only if the LIRF recording convention recurs in July 2026.

### Ruling H: holdout
- **No access.** Day 2 is recorded as "0 of 1, closed unused". It is not recorded as a TIE, because no comparison was made. The unused access does not carry over, and no substitute comparison (e.g. E017 against E005) is admissible.
- **The frozen code would refuse E005 against E005 anyway.** It takes the phase from the new experiment's allocation day, which for E005 is `day-01`, already spent.
- **The same rule opens a loophole.** The code would accept `holdout_check.py E017 E005` at any later time and log it as a Day 2 access. Standing rule 9 closes this.

### Ruling B: the +6,500 s bound
- **It is not re-derived.** It caught the systematic worsening it was set to catch.
- **The decomposition is exact.** Differences on the same rows add, so the S1 statistic is: E006 +5,782, E018 +6,387, E012 +6,390, E015 +6,456, E017 +7,104 s.
- **Both changes worsen July.** The deterministic procedure adds +605/+714 s and the static keys add +608/+717 s.
- **For Day 3.** An alternative resolution needs a forward-risk rationale that does not rest on E006–E018 outcomes. A new threshold on this statistic will not be accepted (standing rule 10).

### Ruling R: comparison base
- A comparison base is a matched reference, not a champion, and must share the candidate's training procedure.
- E017 is not the strongest model on all rows.
- Criteria 1–3 against E005 cannot test a Day 3 mechanism, so criterion 4 has to carry every mechanism claim.

### Main corrections
- **D2-C1:** the margin is not "~100 s on every fold" (R2 is −60.9 / −65.2 s).
- **D2-C2:** on all rows, the static keys are a wash (E012 − E006 −1.72 s, q95 +9.39; E017 − E018 −2.13 s, q95 +13.09). The "30 s vs 7 s" comparison mixes populations.
- **D2-C3:** "static keys dilute the convention" is reversed on S1 in both procedures.
- **D2-C4:** seed variance is not confined to LIRF NM-missing rows. Excluding them, the shift is still +1.33 s on S1 and −1.94 s on W1 (W1 was never reported).
- **D2-C5:** deterministic training costs about 3 s on all rows, and its determinism is untested on real data.
- **D2-C6:** STATE.md is stale again, a repeat of Day 1's C6.
- **D2-C7:** INC-0003 is still live: the researcher process carries `--effort medium`.
- **D2-C8 to D2-C10:** missed expectations, allocations from an uncommitted tree, and my own record (the criterion 6 risk was not sized before E012 ran).

### Files
- Review: `/home/user/prc-data-challenge-2026/research/day-02/advisor/PHASE_CLOSE_D02_review_v1.md` (sha256 `f3df7e551677c75c5fc0e37a426be870ad3098f3bdbd10a272f7036bea9c03b0`)
- Acknowledgement to write: `/home/user/prc-data-challenge-2026/research/day-02/acks/PHASE_CLOSE_D02_ack_v1.md`

```yaml
schema: advisor-task-result-v1
exchange_id: X-D02-S01-0006
status: COMPLETE
decisions:
  - proposal_id: PHASE_CLOSE_D02
    proposal_sha256: 958db1e83aff17fcf03a74fa228257d2723ab3468cf2fe31c0070afd67d85a3b
    decision: ACCEPT
    review_path: research/day-02/advisor/PHASE_CLOSE_D02_review_v1.md
    review_sha256: f3df7e551677c75c5fc0e37a426be870ad3098f3bdbd10a272f7036bea9c03b0
completed_utc: 2026-09-28T22:34:02Z
```
