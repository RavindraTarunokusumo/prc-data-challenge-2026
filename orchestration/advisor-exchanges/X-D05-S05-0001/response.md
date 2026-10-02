## Phase-close review X-D05-S05-0001 (PHASE_CLOSE_D05 v1): ACCEPT, confidence 0.88

**Review file:** `/home/rvindra/Projects/prc-data-challenge-2026/research/day-05/advisor/PHASE_CLOSE_D05_review_v1.md` (SHA-256 `4d1b8770914b97ea133a7c0f4eb672e33df6ebde435af0731b090b389d953cc5`).

The proposal's hash matches the envelope (`ca9fff72…`). The Day 5 decisions stand. I tried to show that the H023 v3 blend (E033) should not be champion, and could not show it under the frozen rules.

### What I checked
Everything was read-only. The experiment lock was free, no truth was loaded on any fold, no December target was read, `holdout_check.py` was not run, and nothing was fitted or scored.
- **The margin holds against E019 itself.** Using E019's cloud metrics, E033 − E019 is −5.620 s on the development mean, against −5.618 s for E033 − E026. The largest per-fold difference is 0.0072 s.
- **Prediction files are exact.**
  - E026, E029 and E033 are bit-identical on every routed row of every fold, including H's 88 rows. The routed rows therefore contribute exactly zero to the comparison.
  - E033 equals ½ E029 + ½ E031 exactly on all 8 folds, and E034 equals ½ E029 + ½ E032.
  - All 72 prediction files of E026–E034 match their manifests.
- **No leakage path.**
  - CatBoost receives no eval set, keeps `use_best_model: False` and runs a fixed 1,000 iterations.
  - Its counters use `SkipTest`, so no validation data enters a CTR counter.
  - The frozen `masked_view` nulls validation targets.
  - The GPU calibrations used permuted targets and computed no metric.
  - H023 v3 was ACCEPTed at 20:38Z, before E030 (20:39Z) and E031 (20:44Z) were allocated.
- **Freeze and environment hold.** The tools freeze against `803ceeb` holds for E030–E034. Every chain run records the rule L v2 item 6 environment and zero swap.
- **Hashes and tests.**
  - Frozen files, the Advisor definition, `gate.py` and the earlier Day 5 mirrors all verify.
  - 62 synthetic tests pass, and `ruff` is clean.

### What the attack found
None of these changes a decision.
1. **The margin has two sources.**
   - −2.04 s comes from E029's D3-C2 treatment. That is E023's Day 4 margin, which could not be promoted alone.
   - −3.58 s comes from the CatBoost half.
   - The S1 WIN is entirely the CatBoost half (+0.20 s, then −4.38 s).
2. **The S1 WIN is not decided by one row.** Without row 192622644, E033 is still −3.76 s on S1.
   - W1 draws 0.29 of its change from row 183910286 and is −2.56 s without it. Criterion 2 does not need W1.
   - In the causal twin W1c, that row's large prediction reverses, yet W1c is still a WIN. Its W1 prediction rests on training months after the validation month.
3. **CatBoost alone is single-row carried on S1** (top-1 share 0.62, so rule 6 fires; −4.14 s falls to −1.66 s without the row). The E031 analysis and the Day 5 summary omit this. The blend's gain over E029 is diffuse (top-10 shares at most 0.37).
4. **The champion is stochastic.**
   - One re-draw moves the blend by at most 0.48 s, against CatBoost alone's 1.06 s on R1.
   - Clause 1's W1 reading changes from WIN to TIE across draws.
   - Criterion 6 is met as frozen, but the submission will be another draw.
5. **None of the process slips touched a decision quantity.** I confirmed this for each slip.

### Authorized holdout access
One access, after the acknowledgement is committed. Conditions: clean tree, lock free, no `day-05` `holdout_access` line in the task ledger, and the environment unchanged.
```
uv run python scripts/holdout_check.py E033 E026 --reason "Day 5 phase close (X-D05-S05-0001): phase-closing champion E033 (H023 v3) vs phase-opening champion E019, laptop instance E026 (rule L v2 item 5)"
```
- **WIN or TIE:** E033 becomes champion. H023 v3 and its reproduction E034 are recorded PROMOTE, and E019 becomes previous.
- **LOSS:** mechanical revert. H023 v3 is recorded INCONCLUSIVE, E019 stays champion, and no substitute comparison follows.
- **Ruling H5:**
  - H figures are recorded only.
  - H is a joint test of both mechanisms on one draw, with the routed rows excluded by construction.
  - Record E026's H RMSE beside E019's 375.9272 s as an instance check. This is disclosure only.

### Champion disclosures named for E033
- **Carried:** D3-C1 (lineage) and D3-C3, restated by D5-C16. The development out-of-range share in the over-3 h band is 0.57 % against E019's 15.3 %.
- **New:** D5-C8 (margin composition), D5-C9 (stochastic champion), D5-C10 (single rows) and the 1,000-iteration budget.
- **D3-C2** is retired as a defect but kept as history.
- **D4-C9** is superseded for E033 by D5-C10.

### Corrections the acknowledgement must append (D5-C8 to D5-C16)
- **D5-C8 to D5-C10:** the three disclosures above.
- **D5-C11:** CatBoost alone's S1 WIN is single-row carried.
- **D5-C12:** four attribution and scope over-claims in the Day 5 summary:
  - §1 "Its categorical statistics are the reason";
  - finding 3 "better than either half";
  - finding 4's out-of-range claim, which holds for the codes arm only;
  - finding 5's GPU speed comparison, which mixes hosts.
- **D5-C13:** the Advisor's magnitude misses for H021–H023 and the Advisor's own record.
- **D5-C14:** ledger decisions, which are null for E026–E034.
- **D5-C15:** clerical items:
  - E033's range-check call named E033 only, while its Validation Plan also named E029 and E026;
  - `prc.tracking`'s hard-coded W&B champion lineage omits E003 and lacks E033;
  - the proposal's "reads only `metrics.json`" is imprecise, though no H figure can reach W&B;
  - INC-0007 needs a pointer to INC-0010, and the D05-S04 session-registry line needs a note.
- **D5-C16:** D3-C3 restated for E033.

**Standing rule 13 is added.** From the next proposal on, any candidate or champion with a non-deterministic component discloses its re-draw spread. It is disclosure only.

**Incidents:** INC-0006 may close. INC-0009, INC-0010 and INC-0004 stay open.

**Forecast:** H WIN P 0.87, TIE 0.11, LOSS 0.02. E033 − E026 on H is expected at −3 to −10 s (central −6).

**Acknowledgement path:** `/home/rvindra/Projects/prc-data-challenge-2026/research/day-05/acks/PHASE_CLOSE_D05_ack_v1.md`

```yaml
schema: advisor-task-result-v1
exchange_id: X-D05-S05-0001
status: COMPLETE
decisions:
  - proposal_id: PHASE_CLOSE_D05
    proposal_sha256: ca9fff72ecc60effd757e1df132ae606cf6dfdbca3a29043bf1829073041ee00
    decision: ACCEPT
    review_path: research/day-05/advisor/PHASE_CLOSE_D05_review_v1.md
    review_sha256: 4d1b8770914b97ea133a7c0f4eb672e33df6ebde435af0731b090b389d953cc5
completed_utc: 2026-10-02T13:12:24Z
```
