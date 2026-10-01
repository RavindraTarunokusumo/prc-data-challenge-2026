# Advisor response — X-D04-S02-0001 (phase close)

Final message of the `advisor` subagent, mirrored verbatim below the rule (the harness indentation removed). No secrets present.

---

**ACCEPT (confidence 0.85).** The Day 4 decisions stand under the frozen rules: E019 stays champion, E023 and E024 are not promoted, H020 v1 stays rejected, and Day 4 makes no holdout access. The acknowledgement must append ten record corrections (D4-C7 to D4-C16) before `DAY_SUMMARY.md` is finalised, and `HANDOFF_D04.md` is not ready yet.

The proposal's SHA-256 matches the envelope (`1c760903…`). The review file is the only thing I wrote in the repository.

**Main adversarial finding: E019 is champion by rule, held against E023 by one validation row out of 190,713 on S1.** This is an audit result only and changes no outcome (rule 10).
- **The row.** Row 192622644 (LIRF, y 87,002 s) carries 8.2 % of E019's S1 SSE, and every committed model misses it by at least 64,500 s. E019's prediction there (8,136 s) is the highest in the FS2 family.
- **Without it, E023 meets criteria 1–3** against E019 (mean −2.19 s, q95 −1.53, 5/5 counted WIN). It still does when W1's dominant row is also removed.
- **The effect cuts both ways.** E023's W1 WIN is also carried by a single row (183910286); without it, W1 is a TIE.
- **The rest of the LIRF NM-present tail is a wash** (S1: 270 rows, about 0.00 s).
- **H018's rule 8 forecast held numerically for the wrong reason.** The S1 cell value came in inside its range, but the stated mechanism (tail predictions fall) did not occur; the value is that one row.
- **E023 also removes the champion's known defect, D3-C2.** The > 3 h out-of-range band falls from 81 to 5, and the > 5 h share from 41/93 to 1/93.
- **Criterion 2 was not misapplied.** A TIE is the frozen answer when one airport-day dominates a fold. The record must say plainly that E019 holds by rule and carries D3-C2 and D3-C3 into Days 5–7 and any submission.

**Rulings**
- **Ruling H4, Day 4 holdout.** No access; record "Day 4: 0 of 1, closed unused", not a TIE. There is no carry-over and no substitute comparison. E023 and E024 are `day-04` allocations, which still has an unused access, so the frozen code would accept them as NEW later. Rule 9 forbids that in any phase. E019 is Day 5's phase-opening champion.
- **Hand-off base ("Case against" 1).**
  - The hand-off may state, under ruling R, that E023 is the matched reference for candidates that keep `route_train_exclude` on FS2, and E024 for FS3.
  - It may not call E023 a default base or a de facto champion.
  - A candidate that keeps H018's change is still judged against E019, and its criterion 4 includes H018 v2's clauses.
  - Rule 10 covers E023's and E024's configurations. A variant that changes only the compute backend or library build counts as the same configuration unless it pre-registers a mechanism for that change.
- **INC-0005 may close** once D4-C12 is appended. No delegated commit touched a proposal, review, ack, allocation, ledger, journal, STATE or summary. **INC-0004 stays open:** measured at 01:44Z, the researcher process still runs with `--effort medium`.

**Corrections D4-C7 to D4-C16**
- **D4-C7.** The prior block is not "nothing measurable". It gives −0.40 s on all rows (q95 −0.03, R1–R3 WIN): real, but a tenth of the floor. W1's LOSS sits at LTFM (0.58) and EHAM (0.42); LFPG carries only 0.10.
- **D4-C8.** "At no cost elsewhere" is false outside `NM_present_excl_LIRF`.
- **D4-C9.** The single-row S1/W1 quantification above, recorded as a standing disclosure on the champion.
- **D4-C10.** DAY_SUMMARY §7 omits the Advisor's forecast misses for H018 and H019.
- **D4-C11.** The ledger `decision` field is null for E019–E024. By the Day 1 precedent, E023 and E024 are REJECT, with their mechanism outcomes in the notes.
- **D4-C12.** The delegated-work list omits `e4c57f8`, and cites a pipeline digest that was never committed.
- **D4-C13.** STATE.md is stale for the fourth phase running.
- **D4-C14.** HANDOFF_D04.md has eight stale values (143 tests, 24 experiments, next ID E025, among others). It also lacks:
  - H020's deferral and its CatBoost objections;
  - E023 and E024 as open work;
  - the Day 5 holdout facts;
  - a note that `gate.py` takes `day` and `session` from the proposal.
- **D4-C15.** Process notes:
  - E024's gate record shows session D04-S01 because of that same gate semantics;
  - E023's allocation records stayed uncommitted across a container restart.
- **D4-C16.** Advisor-record items from the Day 4 reviews.

**Verified (all read-only)**
- Re-running `compare.py` for E023 and E024 against E019, and both `range_check.py` calls, into the scratchpad gave files byte-identical to the committed ones.
- The mechanism checks and route integrity (all 8 folds) re-derive exactly.
- All 192 prediction files match their manifests.
- Frozen files, advisor definition, `uv.lock` and the Day 4 mirrors are intact; the code freeze held from `d1cc43b`.
- `pytest` passes 143/143 and `ruff` is clean.
- No credential value appears in tracked files or commit messages.
- I read no December target, did not run `holdout_check.py`, and fitted no model.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D04-S02-0001
status: COMPLETE
decisions:
  - proposal_id: PHASE_CLOSE_D04
    proposal_sha256: 1c7609037e02a42e7c185adff73354194b0dcd94eb5d1141966d0ae5e60a5ee5
    decision: ACCEPT
    review_path: research/day-04/advisor/PHASE_CLOSE_D04_review_v1.md
    review_sha256: c809853a0fa97efce1135feb899262ee2713b615aa378110c403f9d17460eb6f
completed_utc: 2026-10-01T01:55:21Z
```
