**H038 v2: ACCEPT (confidence 0.80).** E051 and E052 may be allocated and run as written. Two binding rulings govern how the results are read. Neither changes the run, the tooling or the launcher.

Review: `/home/rvindra/Projects/prc-data-challenge-2026/research/day-08/advisor/H038_review_v2.md` (SHA-256 `cab179656000b329e4b58d208c0c9cf187b351483863610f072c966382a238af`). Its front matter parses the way `gate.py` reads it: ACCEPT, proposal hash matches, version 2.

**Hashes.** The proposal (`3104c018…`), launcher (`54ee5ab8…`) and params file (`b22c02c1…`) all match the envelope.

**The six revisions are all met:**
- the rule 8 band table recomputes on all seven folds;
- the S1 statement is there;
- criterion 4's claim is restated (the second option the v1 review allowed);
- the footprint is restated;
- `known_row_check.py` is committed and implements ruling (E) correctly;
- the component files now have a manifest;
- the probabilities are restated and coherent.

**The launcher change (guards 1,500 s → 840 s) is acceptable.**
- The diff against the reviewed version is the two queue values only.
- Your basis (the pilot's timings) does not carry over: the pilot used four months of data, the folds use up to eleven.
- Other records do support 5–9 minutes per run: E030's laptop folds bound the feature build at about 25–30 s, and g fits on about 7–8 % of the rows.
- My estimates: E052 deferred about 0.1, a run ending after the window about 0.03.

**Ruling (G): criterion 4's decisive reading is the proposal's sign test.**
- The frozen tooling gives the name `criterion4_reading_a` to a different rule: `mixture_analysis.py` sets `CONV_SHARE = 0.5`, so the convention rows must carry at least half of the gain. `tests/test_known_rows.py` calls the same rule "Criterion 4 (a) of H038 v2".
- The two rules disagreed on the pilot in P1 (share 0.22). The proposal governs.
- On each gaining development fold, `subgroup_sse_change_convention` must be below zero. The `criterion4_reading_a` boolean is reported as "the majority-share reading" and decides nothing.

**Ruling (E)(vi): the no-LOSS condition is covered too.**
- If criteria 1–3 pass as frozen but any development fold is LOSS once its known rows are reverted (`reverted.fold_outcome_counted` in `E051_vs_E046_known_rows.json`), G5's consequence applies: INCONCLUSIVE, never uploaded.
- Ruling (E) left this case open. With W1's single dominant row, the cluster bootstrap cannot declare a LOSS while that row gains.
- The tool's `g5_consequence` flag does not compute this, so the phase close reads it from the JSON.

**Corrections for ack v2:**
- D8-C11: the tooling and test mislabel reading (a); the ack v1 wording describes the option v2 did not take.
- D8-C12: four minor slips:
  - W1 after the known-row reversion is 14 bulk and 43 tail rows, not 13;
  - the components path is `predictions/validation/`, not `predictions/val/`;
  - the configs must carry `proposal_version: 2`, not the 1 carried over in § Proposed Change;
  - the launcher's header comment still says "v1" (it is pinned; no change).

**Scope conditions:**
- The allocation must yield exactly E051 and E052, because the pinned launcher hard-codes those IDs.
- Run only through the launcher, on the owner's go-ahead, with END = START + 30 min.
- Freeze from `ce89aeb`.
- No H, December, SUBMIT or upload.
- A deferred E052 leaves criterion 6 open, so nothing can be promoted until it runs.
- Next step: `research/day-08/acks/H038_ack_v2.md`, citing both hashes, adopting (G) and (E)(vi), and appending D8-C11 and D8-C12.

**What I read and ran.** No target, silver, December or Day 7 figure files, and no fit, run or allocation. No leaderboard figure entered this exchange. I ran the seven synthetic tests (they pass) and `ruff` on the changed files (clean). I wrote only the review file; `response.md` is left for you to mirror.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D08-S03-0002
status: COMPLETE
decisions:
  - proposal_id: H038
    proposal_sha256: 3104c018121e46b1a7ba7aafcd453b5781ebe0da41d538ac38ffe9b50cfc294c
    decision: ACCEPT
    review_path: research/day-08/advisor/H038_review_v2.md
    review_sha256: cab179656000b329e4b58d208c0c9cf187b351483863610f072c966382a238af
completed_utc: 2026-10-06T20:10:09Z
```
