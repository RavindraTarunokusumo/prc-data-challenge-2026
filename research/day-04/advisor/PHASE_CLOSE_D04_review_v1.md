---
schema: advisor-review-v1
hypothesis_id: PHASE_CLOSE_D04
proposal_version: 1
proposal_sha256: 1c7609037e02a42e7c185adff73354194b0dcd94eb5d1141966d0ae5e60a5ee5
exchange_id: X-D04-S02-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-10-01T01:53:13Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.85).**
- **The Day 4 decisions stand under the frozen rules.**
  - E019 remains champion.
  - H018 v2 (E023): mechanism supported, not promoted (criterion 2).
  - H019 v2 (E024): mechanism falsified, not promoted.
  - H020 v1: REJECT, closed.
- **No Day 4 holdout access** (ruling H4, Validation Quality). Record "Day 4: 0 of 1, closed unused".
- **The acknowledgement appends ten record corrections, D4-C7 to D4-C16, before `DAY_SUMMARY.md` is finalised.**
  - None changes a decision.
  - Three change what Day 4 is recorded as having shown: D4-C7, D4-C8 and D4-C9.
- **`HANDOFF_D04.md` is not ready.** It is stale in eight places and lacks four required items (D4-C14).
- **INC-0005 may close at this phase close,** once D4-C12 is appended.

**Attack on the champion.** As policy requires, I tried to show that E019 is wrong. I could not show that any Day 4 decision is wrong under the frozen rules. What I found is that **E019 is champion by rule, held against E023 by one validation row out of 190,713.**

1. **The frozen criteria re-verify byte for byte.**
   - Re-run into the scratchpad, `compare.py E023 E019`, `compare.py E024 E019` and both `range_check.py` calls are byte-identical to the committed JSONs.
   - The three mechanism checks and route integrity (all 8 folds) re-derive exactly.
   - All 192 prediction files of E001–E024 match their manifests.
2. **E019 holds against E023 by one row.** This is an audit only; it changes no outcome (rule 10).
   - Row **192622644** (LIRF, NM-present, `d_aobt3` 87,181 s, y 87,002 s) carries **8.2 % of E019's S1 SSE**. Every committed model misses it by at least 64,500 s.
   - E019's prediction there, 8,136 s, is 1,095 s closer than E023's 7,041 s, and it is the highest prediction of the FS2 family.
   - **Without that row, E023 meets criteria 1–3 against E019:** mean −2.19 s (q95 −1.53), 5/5 counted WIN.
   - **It still does with W1's favourable dominant row also removed:** mean −2.03 s (q95 −1.43), with W1 TIE.
   - The other 270 LIRF NM-present tail rows on S1 net to 0.00 s.
3. **E023 also removes the champion's known defect.**
   - D3-C2's > 3 h band falls from 81 to 5, and the > 5 h out-of-range share from 41/93 to 1/93.
   - D3-C3 records that defect's January 2026 exposure.
4. **None of this allows a promotion.**
   - Criterion 2 and the cluster bootstrap are frozen (brief §9). A fold change dominated by one airport-day is uncertain, and TIE is the frozen answer.
   - Rule 10 forbids any later change of population or counting rule.
   - The record must say plainly that E019:
     - holds by rule, by one S1 row;
     - is not the better model on the 2025 evidence;
     - carries D3-C2 and D3-C3 into Days 5–7, and into any submission unless a later candidate is promoted.

**Where the record is wrong** (figures in Scientific Validity):

| Correction | Finding |
|---|---|
| D4-C7 | The prior block is not "nothing measurable". It adds −0.40 s on all rows (q95 −0.03; R1–R3 WIN) and −0.29 s on the clause population: real, a tenth of the floor, below criterion 1. "LightGBM already holds the keys" is untested. W1's LOSS sits at LTFM and EHAM, not LFPG |
| D4-C8 | "At no cost elsewhere" (finding 3) is false outside `NM_present_excl_LIRF`. The cost is the S1 `NM_present_LIRF` cell (+7.76 s, one row: the cost that blocks promotion) and W1c `NM_missing_other` full (+106.33 s). R2 is a LOSS on the clause population (+0.37 s) |
| D4-C9 | Finding 4 is confirmed, quantified and completed. The single-row effect also carries E023's W1 WIN (row 183910286). "Any change moves the row" is too broad. H018's rule 8 cell forecast held numerically, but its stated mechanism did not occur |
| D4-C10 | DAY_SUMMARY §7 omits the Advisor's magnitude misses for H018 and H019 (repeats D3-C8) |
| D4-C11 | `experiments/ledger.jsonl` records no `decision` for E019–E024. The champion carries no PROMOTE, and E023/E024 carry no brief §10 decision |
| D4-C12 | DAY_SUMMARY §8 omits `e4c57f8` (a worker-tool output committed without the provenance line). It cites a pipeline digest that was never committed |
| D4-C13 | `research/STATE.md` is stale for the fourth phase running: completed next actions, an outdated section title, and two inconsistent open-incident lines |
| D4-C14 | `HANDOFF_D04.md`: 8 stale values, plus four omissions: H020's deferral and objections, E023/E024 as open work, the Day 5 holdout facts, and the gate's `day`/`session` semantics |
| D4-C15 | Process: E024's records say session D04-S01 (`gate.py` copies the proposal's session). E023's allocation records stayed uncommitted across a container restart |
| D4-C16 | Advisor record: the Day 4 reviews did not see the single-row S1 decision. They accepted H018's rule 8 tail mechanism. They forecast W1 as H019's largest gain against their own staleness note |

**Verified here.** Every check was read-only. Scripts and outputs stayed in the session scratchpad, Python ran with bytecode writing disabled, and the tree was clean before and after.
- **What I did not do.**
  - No December target was read, and `holdout_check.py` was not run.
  - No model was fitted.
  - `mechanism_check.py` and `route_check.py` were not run, because they write into `research/comparisons/`. Their computations were replicated with the frozen functions.
- **What I read.**
  - Development-fold truth only through `prc.evaluate.truth_frame`. The NM status came from target-free silver columns via `prc.data.load_silver`.
  - The routing check compared H predictions with H predictions, without truth.
- **Hashes.**
  - The proposal matches the envelope (`1c760903…`).
  - The six frozen files match `config/frozen.json` (`32c41c0f…`).
  - `.claude/agents/advisor.md` is `30fff5dd…`, as in `config/agents.yaml`. `uv.lock` is `39df945c…`.
  - `scripts/gate.py` is `28e0977c…`, matching the E023 and E024 gate records.
- **Mirrors.** X-D04-S01-0001 (8/8), X-D04-S01-0002 (6/6) and X-D03-S01-0003 (4/4) verify.
- **Predictions and data.** All 192 prediction files of E001–E024 match their manifests by SHA-256. Silver matches the frozen pin (`efde4262…`). The raw manifest lists 14 files and 330,216,990 bytes, as the hand-off states.
- **Configs.**
  - E023 is E019's config plus `hypothesis_id: H018` and `route_train_exclude: true`.
  - E024 is E023's plus `hypothesis_id: H019` and `feature_set: FS3`.
  - Both are exactly as authorized.
- **Code freeze.** `git diff d1cc43b HEAD` over `src`, `scripts`, `tests`, `config`, `pyproject.toml` and `uv.lock` is empty.
- **Ledger RMSE.** The per-fold RMSE of E019, E023 and E024, re-derived, equals the ledger to 0.01 s.
- **Tests and lint.** `pytest` passes 143/143 with caches disabled, and `ruff` is clean.
- **Holdout.** The task ledger has `holdout_access` events for `day-01` and `day-03` only, and there is no `research/day-04/holdout/`.
- **Secrets.**
  - No S3 access key, S3 secret or OpenSky password value appears in the 543 tracked files or in any commit message.
  - The OpenSky username occurs only inside the repository owner's public handle (brief, merge commits), as on Day 3.
- **INC-0004, measured at 01:44Z.**
  - The researcher process carries `--model claude-opus-5-5 --effort medium`. It has been running about 55 min, so since about 00:49Z.
  - Boot id `f948bf23…`, CPU "@ 2.80GHz": the same as E023 and E024.

## Scientific Validity

### (a) The Day 4 decisions re-verify

| Decision | Check | Result |
|---|---|---|
| E023 clause 3 not met | Routed rows equal E005's on all 8 folds, max \|Δ\| 0.0 (168, 115, 52, 337, 58, 337, 58 and 88 rows; H prediction against prediction) | Confirmed |
| E023 clause 1 not met | > 3 h band 5 (E019 81, E021 18, E017 14). The re-run of `range_check.py E023 E019 E021 E017 --by-dsched --bands` is byte-identical | Confirmed |
| E023 clause 2 not met | `NM_missing_other` bulk −197.85, −230.47, −105.67, −104.99 (R1, R2, R3, W1) | Confirmed |
| E023 criterion 2 fails | Re-run byte-identical. S1 +0.205 [−0.689, +1.258] TIE. Mean −2.04 (q95 −1.31), 5 WIN, 2 TIE | Confirmed |
| E024 clauses 1(a), 1(b) met | `NM_present_excl_LIRF` against E023: −0.289 (q95 +0.121). R1–R3 WIN, S1 TIE, W1 LOSS +1.625 [+0.521, +2.671] | Confirmed (re-derived) |
| E024 clause 2 not met | All rows −0.396 (q95 −0.030) | Confirmed |
| E024 W1c inert | Both W1c files `37857400ac9d…` | Confirmed |
| E024 criterion 2 fails | Re-run byte-identical. S1 +0.723 TIE, W1 −1.071 TIE. Criterion 4 (B2) bars it as well | Confirmed |
| E024 item 8(d) derived figures | A direct computation with explicit ID alignment equals the derived values to 0.01 s on all five folds | Confirmed. The proposal's weakness 1(c) is closed: RMSE differences on identical rows add exactly |
| Rule 12 | The re-run of `range_check.py E024 E023 --by-dsched --bands` is byte-identical. > 3 h band 6 | Confirmed |
| Criterion 7 | E023 925.0 s / 5.29 GB; E024 1,026.9 s / 5.73 GB (CLASS-M: 30 min / 8 GB) | Confirmed |
| No reproduction due | Criteria 1–3 fail against the champion in force in both | Confirmed |

### (b) The S1 and W1 outcomes against E019 are single-row outcomes (D4-C9)

**Row 192622644** is LIRF, NM-present, with `d_aobt3` 87,181 s and y 87,002 s. It is the Day 1 day-scale record on which the raw anchor is exact.

Its S1 predictions across the committed models:

| E005 | E006 | E012 | E015 | E017 | E018 | E019 (= E020, E022) | E021 | E023 | E024 |
|---|---|---|---|---|---|---|---|---|---|
| 2,513 | 16,545 | 5,912 | 5,776 | 6,471 | 22,473 | 8,136 | 7,261 | 7,041 | 5,780 |

- It carries 8.2 % of E019's S1 SSE (6.22 × 10⁹ of 7.62 × 10¹⁰ s²).
- E019's 8,136 s is the highest prediction of the FS2 family (E019, E021, E023, E024).

**Audit only. Rule 10 forbids using any of this for an outcome.** The frozen `paired_bootstrap` and `promotion_check` are applied unchanged, to the fold minus the named row.

| Contrast | S1 as recorded | S1 without 192622644 | Criteria 1–3 without it |
|---|---|---|---|
| E023 − E019 | +0.205 [−0.689, +1.258] TIE | −0.540 [−0.854, −0.307] WIN | Pass: mean −2.19 (q95 −1.53), 5/5 counted WIN |
| E024 − E019 | +0.723 [−1.086, +2.879] TIE | −0.879 [−1.285, −0.555] WIN | Pass: mean −2.75 (q95 −2.10), W1 TIE. Criterion 4 (B2) still bars it |
| E024 − E023 (all rows) | +0.518 [−0.520, +1.742] TIE | −0.339 [−0.689, +0.016] TIE | — |

**The lens cuts both ways.**
- E023's W1 WIN (−1.280 [−3.047, −0.038]) is carried by LIRF NM-present row 183910286:
  - y 13,865 s; E023 7,938 s against E019 1,979 s; top-1 share 0.61.
  - Without it, W1 is TIE: −0.498 [−1.551, +0.401].
- With both dominant rows removed, E023 still meets criteria 1–3: mean −2.03 (q95 −1.43); R1–R3 and S1 WIN, W1 TIE.

**The rest of the LIRF NM-present tail is a wash.** E023 − E019, excluding each fold's dominant row, from ID-aligned rows:
- S1: 270 rows, ΔSSE −9.4 × 10⁴ s² (0.00 s of fold RMSE), mean prediction change +3 s;
- W1: −0.03 s;
- R1 −0.01, R2 −0.90, R3 −0.02 s;
- S1c +0.08, W1c +0.16 s.

**Where E023's effect actually sits.** The treated cell, `NM_missing_other`, carries 1.02, 0.86, 0.95 and 1.10 of the SSE change on R1, R2, R3 and S1c.

**Consequences for the record:**
- **Finding 4 is right, and it is incomplete.**
  - S1's TIE against E019 is one row in both Day 4 comparisons.
  - E023's W1 WIN is also one row.
  - The robust part of E023's advantage is R1–R3 and S1c, all carried by the treated cell.
- **"Any treatment that changes the LightGBM's training set or features moves this row" is too broad.**
  - The committed family spans 2,513 to 22,473 s on this row.
  - What Day 4 shows is narrower: both of its changes lowered the prediction on the day-scale record (8,136 → 7,041 → 5,780).
  - Removing the LIRF NM-missing convention rows (targets up to 131,167 s) plausibly lowers the leaf values that reach day-scale records. That is untested.
  - So the S1 constraint binds changes that lower predictions on day-scale records. The D3-C2 treatment is one of them.
- **H018 v2's rule 8 forecast held numerically, but not in mechanism.**
  - The pre-registered S1 cell value was +4 s central (−5 to +15). The outcome, +7.76 s, is inside that range.
  - The stated mechanism, "predictions on LIRF NM-present tail rows fall slightly", did not occur. The other 270 S1 tail rows rose by 3 s on average.
  - The cell value is the day-scale row alone.
- **Criterion 2 is not misapplied.** The TIE stands; no reading of criterion 2 changes (brief §9; rule 10).

### (c) The prior block (H019 v2; D4-C7)

**The falsification is robust.** Clause 1(b) is met on every reading:
- the 5-fold mean, −0.29 s;
- the 4-fold mean without W1, −0.77 s;
- S1 without its dominant row, −0.34 s, TIE;
- all rows, −0.40 s.

**Its size is misstated.**
- **On all rows,** the block's gain is distinguishable from zero under the frozen bootstrap: q95 −0.03, with R1, R2 and R3 WIN.
- **On the clause population** it is not: q95 +0.12.
- **Both are about a tenth of the −3.0 s floor,** and below criterion 1's 1.0 s.
- So DAY_SUMMARY §1's "not measurably" and finding 1's "nothing measurable" are wrong. "Small, a tenth of the floor" is right.

**The W1 LOSS** (+1.63 s on `NM_present_excl_LIRF`), by airport, as a share of W1's SSE change:

| LTFM | EHAM | EDDM | LFPG | LSZH | EDDF | LEMD | EGLL | LEBL |
|---|---|---|---|---|---|---|---|---|
| 0.58 | 0.42 | 0.12 | 0.10 | 0.01 | −0.02 | −0.06 | −0.07 | −0.09 |

- The staleness explanation is untested.
- LFPG's August–November regime, which finding 2 names, is not where the loss sits.
- LTFM is both the largest pooled all-rows gain (−1.94 s) and the largest W1 loss. That fits non-stationary priors at LTFM. This is an observation only.

**Scope.**
- **What was tested.** The claim is for the block as specified: five LOMO m-estimate means, M = 50, sourced from NM-present bulk rows. It was tested on the deterministic routed LightGBM with E017's parameters, on E023's training set.
- **The explanation is untested.** "LightGBM on FS1 already holds the keys, so…" (DAY_SUMMARY §1) remains untested, as the E024 analysis itself says. The controls `H019_review_v2.md` named, a within-key permuted prior and a K5-only block, were not run.
- **§9.4.** "Not worth a further variant in LightGBM on FS2" is the researcher's planning judgement, and it is recorded as such, not as a finding.

### (d) The D3-C2 treatment (H018 v2; D4-C8)

**D3-C2's attribution to the LIRF NM-missing training rows is supported by an exact ablation.**
- The > 3 h band falls from 81 to 5, below every no-T fit (13–41). The treatment removes more than the T increment.
- The < 1 h band is unchanged (82 against 83): a generic LightGBM phenomenon, as pre-registered.

**Finding 3's "at no cost elsewhere" holds only on `NM_present_excl_LIRF`,** and there R2 is a LOSS (+0.37 s). Elsewhere the treatment has costs:
- `NM_present_LIRF` on S1: full +7.76 s. This is one row, and it blocks the promotion.
- `NM_missing_other` on W1c: full +106.33 s, from tail rows; bulk −133.27 s.

Rule 11 requires the statement to be scoped to its population.

### (e) The proposal's questions

**"Case against" 1: should the hand-off name E023 as the matched base?** The ruling:
- **What the hand-off may say.** Under ruling R, E023 is the matched reference for any candidate that keeps `route_train_exclude: true` on FS2, and E024 for FS3. That is a fact of ruling R, and stating it does not pre-empt Day 5.
- **What it may not say.** It may not call E023 a default or recommended base, or a de facto champion. Choosing the base is a Day 5 proposal's decision.
- **The comparator.** Promotion is judged against E019. A candidate that keeps H018's change carries it in that comparison, so:
  - criterion 4 includes H018 v2's clauses 1–2, as H019 v2's E019 branch did. Both are recorded as not met, so B2 does not bar such a candidate;
  - its rule 8 pre-registration states the single-row S1 exposure in (b).
- **Rule 10.** It applies to the configurations of E023 and E024, as to those of E020 and E021: no unchanged re-submission as a promotion candidate.
  - A candidate that differs from them only by compute backend or library build is, for rule 10, a re-draw of the same configuration.
  - It is admissible only if its proposal pre-registers a mechanism for that difference.
  - This matters for Day 5's CPU-against-GPU theme. The single-row S1 result is exactly the temptation rule 10 exists for.

**"Case against" 2.** This is a known limitation of criterion 2 on S1 and W1, now quantified in (b). No reading of criterion 2 changes. Rule 8 already requires pre-registering the `NM_present_LIRF` exposure with S1 at July's rate. Missing Control 1 states what that pre-registration must now contain.

**"Case against" 3.** Agreed. The scope is as in (c), and CatBoost's own statistics are a different mechanism (`H020_review_v1.md`).

**"Case against" 4.** The falsification does not depend on W1. The location table in (c) replaces the LFPG framing.

**Known weaknesses.**
1. **Evidence.** D4-C1 to D4-C6 are in the acks (`H018_ack_v1`, `H018_ack_v2`, `H019_ack_v2`). Item 8(d) is exact.
2. **Process.**
   - The restart and the pause changed no result:
     - authorization item 2 fixed E023's config, and the diff confirms it;
     - both runs started from clean commits;
     - Day 3 established determinism across CPU strings (E022 at 2.80 GHz is byte-identical to E019 at 2.10 GHz).
   - The allocation-record slip is D4-C15.
   - INC-0004 was measured above.
   - INC-0005 is audited in (f).
3. **Missed predictions.** The Advisor's misses are added in D4-C10.

### (f) INC-0005 and the records

**INC-0005.**
- **The delegated commits carry the provenance line.** Each of `ec8c5ad`, `0794612`, `7ae934f`, `e9120a9` and `99db208` says "Implemented by a claude-sonnet-5-5 worker to the researcher's specification; reviewed by the researcher (INC-0005)".
- **They touched only the following:**
  - `scripts/range_check.py`, `scripts/eda_day4.py` and `scripts/calibrate_catboost.py`;
  - `src/prc/priors.py`, `src/prc/features.py` and `src/prc/models/{__init__,gbm,routed}.py`;
  - tests, and `research/day-04/eda/`.
- **No delegated commit touched** a proposal, review, ack, envelope, gate or allocation record, the ledgers, the journal, STATE or the DAY_SUMMARY.
- **The main session launched both runs** (`provenance.yaml`).
- **The Advisor reviewed the delegated code on its merits** in X-D04-S01-0001 and -0002, and found no defect beyond D4-C3.
- **Gaps (D4-C12):**
  - `e4c57f8`, a main-session commit, also committed `range_check_refs.json`. That file is the output of the worker's `--bands` code, committed before that code (D4-C3), and it lacks the provenance line.
  - The D04-S01 "pipeline digest" was never committed. `SESSION_START.md` contains only the plan to make one.
- **Conclusion.** No obstacle to closing INC-0005 once D4-C12 is appended. If delegation recurs on Days 5–7, it needs a new incident.

**Ledger (D4-C11).**
- **`decision` is null for E019–E024.**
  - E019 is the champion (X-D03-S01-0003; H WIN), yet the ledger carries no PROMOTE.
  - `CURRENT.json` and the task ledger's `champion_change` event do record it.
  - Days 1–2 set this field at each decision.
- **The brief §10 vocabulary is PROMOTE, REJECT, INCONCLUSIVE, RESOURCE_FAILURE and INVALID.** The Day 1–2 precedents:
  - a criterion 2 failure was REJECT (E011, H007: S1 TIE);
  - INCONCLUSIVE was used for an unmet rule 1 (E006), criterion 6 (E012, E015) and an unresolved criterion 8 (E017).
- **So the consistent labels are:**
  - E023: REJECT, with the notes "mechanism supported; D3-C2 treated, not promoted (criterion 2, S1 TIE; D4-C9)";
  - E024: REJECT, with the notes "mechanism falsified (1(a), 1(b)); criterion 2 fails".

## Novelty Relative to Existing Research

- **This exchange proposes no experiment.**
- **Day 4's contribution, stated at its size:**
  - D3-C2's cause is identified by an exact ablation and treated: the > 3 h band falls from 81 to 5, and all rows improve by −2.04 s against E019.
  - The run's first target statistic: a real but small gain, a tenth of its floor. Its pre-registered mechanism is falsified.
  - A CatBoost design was rejected before any run, because its stated mechanism was false for the installed library.
  - The single-row character of S1 and W1 against E019 is now measured.
- **Coverage note.** These brief §11 items were not tested as separate hypotheses: conditional medians, quantile priors and explicit interaction features. The EDA found that the median and q20 add nothing over the mean in the linear model. CatBoost is deferred to Day 5.

## Experimental Isolation

- **The phase close changes and runs nothing.**
- **Both contrasts are exact.**
  - E023 − E019 is one training-set rule.
  - E024 − E023 is five appended columns, with W1c byte-identical.
  - The attribution pair adds exactly: −2.04 + −0.40 = −2.43 s, with rounding.
- **The audits in (b)–(d) are attribution only.** They are row exclusions and airport splits of existing prediction files, under the frozen functions unchanged. They decide nothing.

## Validation Quality

**Folds and frozen artifacts.**
- Both Day 4 runs used the frozen folds unchanged, including S1 and both twins.
- The frozen hashes are intact.
- H was predicted only.

### Ruling H4: the Day 4 holdout access

1. **No access.**
   - The frozen `phase_close` rule compares the phase-closing champion with the phase-opening champion. Both are E019, so dRMSE ≡ 0 and there is nothing to revert.
   - The frozen code would refuse it anyway. `holdout_compare` takes the phase from NEW's gate record, E019's is `day-03`, and that phase's single access is spent.
2. **Record "Day 4: 0 of 1, closed unused".** Do not record a TIE: no comparison was made.
3. **No carry-over.** Day 5 has one access.
4. **No substitute comparison.** E023 or E024 against E019 on H would use the holdout to choose Day 5's base, which is holdout-guided selection (ruling H, item 4).
5. **The rule 9 loophole, restated for Day 4.**
   - E023 and E024 are `day-04` allocations, and `day-04` has 0 accesses.
   - So `holdout_check.py E023 …` would be accepted at any later time and logged as a Day 4 access.
   - **No `holdout_check.py` invocation with E023 or E024 as NEW is authorized, in any phase.**
6. **E019 is Day 5's phase-opening champion.**
   - A Day 5 access needs a Day 5 allocation as NEW.
   - E012–E018 and E020–E024 may never be NEW.

**Bootstrap.** A fold whose change one airport-day dominates resolves as TIE (b). That is the frozen design, not a defect to correct after the fact.

## Leakage Review

### Target Leakage

PASS

- **FS3 priors are fold-local.**
  - Training rows use other training months only (LOMO), and validation rows use all training months.
  - The source filter acts on training rows.
  - A single training month yields nulls.
  - The W1c byte identity confirms this on real data.
- **H018's exclusion key** (`ADEP_mvt`, `flt_missing`) is label P and target-free, and it acts on training rows only.
- **No December target was read** by either run, any comparison or this review.

### Temporal Leakage

CONCERN

Carried, not blocking.
- **FS2's T features are unchanged,** including the SCHED-anchored windows that D3-C2's mechanism runs through.
- **S1's and W1's validation priors use later training months,** which is the frozen fold design. S1c bounds S1. W1 has no functional twin for the block, which is why the clause kept it out of the WIN count.

### Competition Availability

CONCERN

Not blocking. It bears on what the champion carries forward.
- **Every input is present in the ranking files.**
- **The champion keeps D3-C2.** January 2026 holds 435 non-LIRF NM-missing rows over 3 h and 92 over 5 h, against 2025 maxima of 222 and 36 (D3-C3).
- **On the development folds,** E019 is out of range on 41 of 93 rows over 5 h, against 1 of 93 for E023.
- **The treatment that removes this is not promoted.**

## Compute Review

### RAM

PASS

No experiment. The read-only re-derivations stayed well within the container's memory.

### Runtime

PASS

- Several read-only scripts and frozen-tool re-runs, each a few minutes. Some included frozen 2,000-resample bootstraps.
- The test suite took 26 s.
- No model was fitted.

### Disk

PASS

One review file. Scratch outputs stayed in the session scratchpad.

## Weakest Assumption

**That holding E019 costs little.**
- **On the 2025 evidence, E023 is better on every development fold except through one S1 row.**
- **It removes the defect whose January 2026 exposure D3-C3 records.** January has 2.0–2.6 times the 2025 maximum of long-delay NM-missing rows, and E019 is out of range on 44 % of such rows over 5 h, against about 1 % for E023.
- **The frozen rules keep E019, correctly.** The price of that falls on January 2026. No check before ranking can measure it, and the holdout cannot show it (Day 3, (d)).

## Missing Control or Ablation

None blocks the phase close. Three are named for Day 5; they are named, not designed.
1. **S1 and W1 single-row exposure.** A Day 5–7 proposal compared with E019, and whose promotion needs S1 (or W1), states under rule 8:
   - the expected direction of its prediction on rows 192622644 (S1) and 183910286 (W1);
   - the `NM_present_LIRF` cell expectation, read as the single-row statistic it is (b).

   This is disclosure. It is not a new reading of criterion 2.
2. **The H019 controls,** before "LightGBM already holds the keys" is used as a finding: a within-key permuted prior, and a K5-only block.
3. **The H020 controls,** for any CatBoost proposal (`H020_review_v1.md`, Missing Control):
   - a contrast whose only difference is the categorical handling, at fixed capacity;
   - sparse levels present, if a sparse-level mechanism is claimed;
   - CTR type and boosting scheme checked with `get_all_params()`;
   - a CLASS-L or GPU rationale tied to a decision;
   - the calibration script committed.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **The Day 4 decisions stand as recorded.**
   - E019 (H015 v2) is the phase-closing champion, by rule, with the standing disclosures D3-C1 to D3-C3 and D4-C9.
   - H018 v2 (E023): mechanism supported; "D3-C2 treated, not promoted" (criterion 2).
   - H019 v2 (E024): mechanism falsified; not promoted (criterion 2; criterion 4 under B2).
   - H020 v1: REJECT, closed.
   - No retroactive promotion and no re-adjudication (rule 10). The audit figures in Scientific Validity (b) are attribution only.
2. **No protected-holdout access in Day 4** (ruling H4).
   - `holdout_check.py` is not run in this phase.
   - No later invocation with E023 or E024 as NEW, in any phase.
3. **Not authorized:**
   - any allocation, run, fit, reproduction or re-run in Day 4;
   - any scoring of H;
   - any change to frozen files, reviews or completed records. Corrections are appended; filling a ledger's `decision` field, as Days 1–2 did, is permitted (D4-C11).

Required acknowledgement path: `research/day-04/acks/PHASE_CLOSE_D04_ack_v1.md`

**Contents of the acknowledgement:**
- the proposal hash (`1c760903…`) and this review's hash;
- corrections D4-C7 to D4-C16, appended. The proposal and completed records are not edited;
- ruling H4 and the hand-off base ruling (Scientific Validity (e)), recorded;
- the closure of INC-0005, with D4-C12.

**Corrections.** Figures are in Scientific Validity.
- **D4-C7. The prior block's size and scope** (DAY_SUMMARY §1, §6 finding 1, §6 finding 2, §9.4).
  - Replace "not measurably" and "nothing measurable" with: −0.29 s on `NM_present_excl_LIRF` (q95 +0.12; R1–R3 WIN, S1 TIE, W1 LOSS) and −0.40 s on all rows (q95 −0.03; R1–R3 WIN). The gain is real but small, a tenth of the −3.0 s floor and below criterion 1. The mechanism is falsified as pre-registered.
  - Mark "LightGBM already holds the keys" as untested, naming the two controls.
  - W1's LOSS sits at LTFM (0.58) and EHAM (0.42), with LFPG at 0.10. Staleness is untested.
  - §9.4 is a planning judgement.
- **D4-C8. "At no cost elsewhere"** (DAY_SUMMARY §6 finding 3).
  - Scope it to `NM_present_excl_LIRF` (±0.56 s; R2 LOSS +0.37 s).
  - The costs are S1 `NM_present_LIRF` +7.76 s (one row; it blocks the promotion) and W1c `NM_missing_other` full +106.33 s (tail rows).
- **D4-C9. Single-row outcomes against E019** (DAY_SUMMARY §6 finding 4, §9.1; STATE; HANDOFF; a standing disclosure on the champion).
  - Row 192622644 carries 8.2 % of E019's S1 SSE. Predictions across the committed models run from 2,513 to 22,473 s against y 87,002 s, and E019's 8,136 s is the FS2 family's highest.
  - Audit only: without it, S1 is WIN for E023 and E024 against E019, and E023 meets criteria 1–3. E023's W1 WIN is likewise carried by row 183910286.
  - The other LIRF NM-present tail rows net to about 0.
  - Replace "any treatment … moves this row" with the narrower Day 4 finding in (b).
  - H018 v2's rule 8 cell forecast held numerically. Its stated mechanism, tail predictions falling, did not occur.
  - No reading of criterion 2 changes.
- **D4-C10. Missed forecasts (Advisor)** (DAY_SUMMARY §7; repeats D3-C8).
  - H018: the > 3 h band, central 22 (80 % interval 12–40) → 5; W1 0 ± 1 s → −1.28 s; W1c 0 to +7 s → −1.64 s (wrong sign).
  - H019: `NM_present_excl_LIRF` −0.5 to −4 s (central −2) → −0.29 s; all rows −0.5 to −3 s → −0.40 s; "W1 the most likely largest fold gain" → W1 the only LOSS; LFPG, EGLL and LTFM to lead → LTFM only.
  - Both primary failure modes were correct.
- **D4-C11. Ledger decisions** (`experiments/ledger.jsonl` and SQLite; brief §10 and §13 step 2).
  - Record E019 PROMOTE (X-D03-S01-0003; a Day 3 record gap). Record E022 as the passing reproduction, as for E007–E009.
  - E020 and E021: no promotion decision by design, in notes (E010 practice).
  - E023 and E024: REJECT, with the notes in (f).
  - If the researcher treats ledger rows as immutable, an appended correction stating these is the alternative.
- **D4-C12. Delegated-work list** (DAY_SUMMARY §8; INC-0005).
  - Add `e4c57f8` (`range_check_refs.json`, output of the worker's `--bands` code, without the provenance line).
  - Record that the D04-S01 pipeline digest was never committed, and that no record depends on it.
  - Otherwise the list is complete and the delegation boundary held.
- **D4-C13. STATE.md is stale** (brief §13 step 3; repeats C6, D2-C6, D3-C6).
  - The 01:30:08Z version still lists "`gate.py allocate H018 v2` … `gate.py allocate H019 v2`" as next actions.
  - It still heads a section "Day 4 so far (infrastructure, no experiment)".
  - It has two open-incident lines that disagree: INC-0004 and INC-0005, against INC-0004 only.
- **D4-C14. HANDOFF_D04.md** (brief §3; `H020_review_v1.md`; `H020_ack_v1.md`).
  - **Stale values:**
    - 141 tests → 143;
    - "experiments allocated: 22" and "expected 22 rows" → 24;
    - "next is E023" → E025;
    - "`day-04/DAY_SUMMARY.md` … not yet present";
    - "Day 4's is (unverified)";
    - INC-0005 "open";
    - the "provisional" champion block.
  - **Missing:**
    - (i) H020 v1 REJECT, the deferral of CatBoost to Day 5, and the review's design objections (boosting type, pre-collapse levels, CTR complexity, a capacity control), with Missing Control 3;
    - (ii) E023 and E024 as open work, not results, with their outcomes, D4-C9, the hand-off base ruling and rule 10;
    - (iii) the champion's disclosures D3-C1 to D3-C3. D3-C2's cause is now confirmed by E023. Add D4-C9, and the consequence that the submitted model carries D3-C2 and D3-C3 unless a later candidate is promoted;
    - (iv) the Day 5 holdout facts (ruling H4, item 6);
    - (v) `gate.py` copies `day` and `session` from the proposal's folder and front matter. A Day 5 reproduction of H015 v2 is therefore recorded as `day-03` / D03-S01, and E024 shows D04-S01 (D4-C15);
    - (vi) the ledger decisions (D4-C11).
  - **Non-blocking note.** Nothing describes producing SUBMIT_JAN and SUBMIT_JUL predictions. `run_experiment.py` accepts final folds. Brief §3 does not require it, but Day 7 will need it.
- **D4-C15. Process** (DAY_SUMMARY §7).
  - E024's `gate.json` and its ledger row say session D04-S01, while the allocation ran in D04-S02. This is the tool's semantics, as in D4-C14 (v), and the gate record is not edited.
  - E023's allocation records (gate, ledger, task ledger) stayed uncommitted for about 7 h across a container restart, against the brief §4 rule ("anything uncommitted is lost"). No result depends on it. E024's same-second allocation commit is the practice to keep.
- **D4-C16. Advisor record.**
  - `H018_review_v2.md` sized S1 by a splice of the treated cell and named `NM_present_LIRF`. It did not identify that one day-scale row (8.2 % of E019's S1 SSE) would decide S1.
  - It accepted H018's rule 8 tail mechanism, which did not occur.
  - `H019_review_v2.md` forecast W1 as the largest gain while recording W1's staleness.
  - No decision would have changed.

**Conditions on the phase-closing commit:**
- **The acknowledgement** above is committed.
- **`research/STATE.md`** is current, with a measured header time. It records:
  - the champion, E019 by rule, with D3-C1 to D3-C3 and D4-C9;
  - E023 and E024 as in item 1;
  - Day 4 holdout 0 of 1, closed unused;
  - INC-0004 open and INC-0005 closed;
  - standing rules 1–12 and B1–B4, and rulings H, B, R, H3 and H4;
  - the next action: Day 5 on the laptop, from `HANDOFF_D04.md`.
- **`DAY_SUMMARY.md`** is corrected per D4-C7 to D4-C10, D4-C12 and D4-C15, and marked final, with "no promotion, no holdout access".
- **`HANDOFF_D04.md`** is finalised per D4-C14, its champion block is final, and the hand-off base ruling is stated as written.
- **Journal and ledger.** A Day 4 phase-close journal entry exists, and the ledger decisions follow D4-C11.
- **INC-0005** is closed in the incident file, with a pointer to the corrected DAY_SUMMARY §8. INC-0004 stays open.
- **Mirror.** The exchange is mirrored: `envelope.yaml`, `response.md` and `checksums.sha256`.
- **Session registry.** It has an end event for D04-S02.
- **`models/champion/CURRENT.json`** still names E019. If its disclosure list is touched, it adds D4-C9.

## Revision

None required for this version.

**No new standing rule.**
- Rule 10's application to E020, E021, E023 and E024, and to backend-only or build-only variants, is stated in Scientific Validity (e).
- Missing Control 1 states what rule 8 pre-registrations against E019 must now contain.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| The Day 4 decisions are correct under the frozen rules | 0.97 |
| A Day 4 holdout access could have changed any decision | 0 (no promotion; the code refuses E019 as NEW) |
| E023 has a lower true RMSE than E019 on January 2026 | 0.85 |
| E023 has a lower true RMSE than E019 on July 2026 | 0.65 |
| A Day 5–7 candidate that keeps H018's exclusion and is compared with E019 gets a counted S1 WIN | 0.35 |
| E019 is still champion at the Day 7 freeze | 0.50 |

Expected magnitude:
- **This exchange:** none (no experiment, no access).
- **January 2026, unobservable before ranking:** E023's advantage over E019 is larger than its −2.04 s development mean, because of the 92 rows over 5 h on which E019 goes out of range at the 2025 rate.
- **July 2026:** near the S1 development result, ±1 s, decided as much by LIRF day-scale records as by the treatment.

Primary expected failure mode:
- **Primary.** The single-row finding is read as license.
  - Days 5–7 treat E023 as the de facto champion and build on it without a pre-registered comparison against E019, or press for an S1 population or counting change.
  - Rule 10 and this review foreclose the second. The first is legitimate only as a new candidate judged against E019.
- **Secondary.** The hand-off reaches the laptop without the H020 objections or E023's status. Day 5 then re-proposes a CatBoost configuration with the same defects, or a backend-only re-run of E023's configuration as a candidate.
