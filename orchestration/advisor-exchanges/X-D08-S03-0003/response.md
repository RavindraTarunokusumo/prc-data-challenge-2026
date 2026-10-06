**Decision: ACCEPT (0.85).** Adding H to E051 and E052 as a predicted-only fold is not a material change to H038 v2. The two runs keep their IDs and may run in the owner's existing window, within the scope below.

The proposal hash matches the envelope (`a3cc9bc7…`). The review is at `/home/rvindra/Projects/prc-data-challenge-2026/research/day-08/advisor/H038_review_v2_A1.md`. It is the only file I wrote; the tree is otherwise clean at `3242c09`.

**What I checked in the code (read-only, no truth or silver read):**
- **Nothing ran.** The runner's config check comes before it sets status to RUNNING. E051 and E052 are still ALLOCATED in both ledgers, with no run commit and no output files. The runner's own "must be ALLOCATED" gate is what allows a second invocation, so keeping the IDs is consistent with it.
- **H is never scored or truth-read.**
  - With H listed, the run is still not "final", so December DEP block time and target stay masked.
  - The worker skips scoring and the learning curve for the holdout fold.
  - The frozen `truth_frame` refuses holdout folds in code.
  - All five analysis tools are fixed to R1–W1c: compare, known_row_check, mixture_analysis, range_check and reproduce_check. Your amendment listed only two of them, but the claim holds for all five.
- **The H fold itself is clean.**
  - Its fits use January–November training rows only, and the H component file has no target column.
  - Only block time and target are blanked in December, so the subgroup flag on H is the real one, computed the same way in the worker and the mixture check.
  - The W&B mirror sends development and diagnostic metrics only.
- **E046 covers H:** 165,677 rows (the frozen count), and the file hash matches its manifest.
- **Scored folds should be unchanged.** Folds are computed independently from the same masked data, so adding H is expected to change no byte of the seven scored folds.

**The error was mine as well as yours.** My v2 review never checked the configs against the runner's config check. It also treated "no H fold" as a merit and listed "any H fold" as not authorized. That confused predicting H, which the runner requires of every non-final run, with accessing H, which is what H8 closes. INC-0022 should record the review's share.

**Authorized scope (binding):**
- **Configs:** append `- H` as the last entry of `folds` in both configs, one added line per file and nothing else. `gate.json` (which keeps citing v2), the ledgers, the launcher and the frozen files stay unchanged.
- **Commit first:** commit and push the configs, the review, the exchange mirror and the acknowledgement before re-arming.
- **Re-arm:**
  - only with the same arguments: START 2026-10-06T22:40:51Z, END 2026-10-07T00:40:51Z;
  - only **by 00:12:51Z**, which is your own condition (END − 2 × 840 s);
  - after that, nothing is re-armed and both runs wait for a new owner window. The launcher's guards decide each start; a deferred E052 leaves criterion 6 open.
- **H counts for integrity:** a mixture-check FAIL on H makes the run INVALID.
- **Not authorized:**
  - any H score;
  - any December target read by any path, including direct silver reads;
  - holdout_check or holdout_compare on any experiment (H8);
  - any analysis of E051/E052's H predictions beyond the mixture check's record;
  - any other change, fold, rerun or experiment.

**Records required:**
- **Acknowledgement:** `research/day-08/acks/H038_ack_v2_A1.md`. It must:
  - cite both hashes;
  - show the two config diffs;
  - restate the two changed scope lines of ack v2;
  - append correction D8-C13.
- **INC-0022:** must record the review's share of the error, why an amendment was used instead of a v3 (the envelope purpose `scope_amendment` is not a contract purpose), and the re-arm time.
- **Phase close:** repeats the H8 check that the task ledger has no holdout access after 2026-10-04T17:57:38Z.

**One residual risk, stated plainly.** Once E051 has an H file, only the records stop a holdout comparison being run on it, the same as for E046. The control is the phase-close ledger check above.

**Re-arm and owner:** I did not require a new go-ahead: the owner's go-ahead covers this queue and the window is unchanged. Whether to ask again is the owner's call. INC-0022 should be reported to the owner plainly.

**Predictions:**
- The scientific predictions from my v2 review are unchanged: P(development mean improves) 0.60, P(promote) 0.11.
- Operational: mixture check passes on all 8 folds 0.94; E052 starts inside the window 0.92.

**Mirror:** I did not write `response.md` or `checksums.sha256` in `orchestration/advisor-exchanges/X-D08-S03-0003/`. The researcher mirrors this message verbatim.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D08-S03-0003
status: COMPLETE
decisions:
  - proposal_id: H038
    proposal_sha256: a3cc9bc7139dedd24ba00c3bf9719fb99b6efcec16c65f72f9caae960ef02a66
    decision: ACCEPT
    review_path: research/day-08/advisor/H038_review_v2_A1.md
    review_sha256: 542fb59b8da7ec88e826af4d8e14efabd1586d3b53ff197b2b52e99dbf3c1d6f
completed_utc: 2026-10-06T22:49:13Z
```
