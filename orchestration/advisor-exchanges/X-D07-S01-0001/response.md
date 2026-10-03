## Advisor result, X-D07-S01-0001 (batch H031–H033 v1: the SUBMIT fits)

**All three proposals are accepted: H031 at 0.85, H032 at 0.83, H033 at 0.85.** The batch can be armed for tonight's 19:00–20:00Z window. Nine binding conditions, S1–S9, are written once in the H031 review; the other two reviews adopt them by reference. None changes a configuration, threshold, population or fold.

**Checks done first, all read-only.** No fit, no score, no target or block-time column read, no holdout, and none of `holdout_check.py`, `run_experiment.py` or `make_submission.py` was run.
- **Hashes:**
  - the three proposal hashes match the envelope;
  - the launcher (`1975bbba…`), the formatter (`c99fdaba…`) and its test (`d11c773c…`) match their pins and are unchanged at `eedcd47`.
- **Tests and lint:** formatter tests 4 passed; `ruff check .` clean. The 162-test full suite was not re-run, because the envelope allowed only the formatter tests.
- **Lock and tree:** the experiment lock is free (its inode is not in `/proc/locks`; the "E041" text is the stale stamp from D6-C14). The tree was clean.
- **Data facts, target-free:**
  - the template matches its manifest: 344,841 rows, Float64 and Int32 columns, target all null, and its ids equal silver's DEP rows of 2026-01 (152,719) and 2026-07 (192,122);
  - silver holds only the 2025 months plus 2026-01 and 2026-07;
  - routed rows are 107 and 276, as stated;
  - 12-month training has 2,085,047 DEP rows, +8.6 % on H;
  - all 24 reference prediction files that the formatter reads match their manifests.
- **Config identity:** parsed-YAML comparison shows each `params` block identical to E029, E031 and E033 respectively (the blend's components aside).
- **Resolved parameters:** E031's and E040's are identical across all 8 folds, from 1 to 11 training months.

**Findings and what each condition requires:**
1. **Launcher defect: the tree goes dirty after the first run (S3).**
   - Each final-fold run appends its unmasking event to the tracked `orchestration/task-ledger.jsonl`. The launcher's checkpoint does not stage that file.
   - So after E042 the launcher logs a WARNING, and E043 and E044 will record `git_dirty_at_run: true`.
   - This is harmless and auditable, so the pinned launcher is not to be changed. S3 pre-registers the state: it is not a deviation if the WARNING lines list only that file. Commit the ledger lines after the queue. No record may claim "clean tree at each run" for this batch.
2. **Integrity reading 4 contradicts itself (S4).** "E042 and E043 only", yet E044 also logs the event. It is to be read as: exactly one event each for E042, E043 and E044 (plus any rerun), each inside its run's time span, and none for any other experiment.
3. **H032's resolved-parameter exemption has no basis (S5).** H032 exempts differences "caused by the training set". Since training size has never changed a resolved key, any difference at 12 months is a sanity flag; check `data_partition` explicitly (D6-C7).
4. **Flags versus defects (S6).** A flag whose analysis finds a code or data defect makes that run INVALID: its predictions are not submitted, and the fix is a new proposal version. Upload waits until no flag analysis is open.
5. **The rerun allowance is granted narrowly (S7).**
   - A deferred run keeps its id.
   - After RESOURCE_FAILURE or TIMEOUT, at most one unchanged `--purpose rerun` per hypothesis.
   - If a component is re-run, the blend gets a new `H033 v1 --purpose rerun` allocation with the re-run id swapped in. E044's committed config is never edited.
   - The pair to be blended must pass the route check first.
6. **Clerical (S9).** The proposals' `created_utc` (17:20:00Z) is 20 minutes after the commit that contains them (17:00:11Z). Record this in the acks.

**Before arming (S1, S2):**
- The allocated ids must be E042, E043 and E044, because the launcher hard-codes them. If they differ, do not arm.
- Commit a pre-arming record that includes the GPU memory in use at arming.
- Keep the tree clean until 19:00Z.

**Disclosures for the analysis (S9):**
- The submission's accuracy is not measured by any fold or by H; it is one draw of the CatBoost half.
- Three known data asymmetries apply:
  - the six-month gap before July 2026;
  - the 1 July month edge (no 30 June context);
  - January 2026's NM-missing share of 1.61 %, about 1.7 times January 2025's 0.93 % and above both winter analogues.

**Main risk:** GPU memory. An external process holds about 2.9 GB, and E043 needs about 3 GB. If that holder grows during the window, E043 fails as RESOURCE_FAILURE (P about 0.06), E044 is deferred, and the S7 rerun path applies in another owner window. I put the whole chain producing a submission tonight at 0.85.

Files are in `/home/rvindra/Projects/prc-data-challenge-2026/research/day-07/advisor/`:
- H031_review_v1.md
- H032_review_v1.md
- H033_review_v1.md

I wrote one throwaway read-only check script, `tf_checks.py`, in the session scratchpad, outside the repository. Nothing else was written.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D07-S01-0001
status: COMPLETE
decisions:
  - proposal_id: H031
    proposal_sha256: 560ee530f3c2e1adeb18beb1e4ab6b9602d22e9bab8188a4fb29c2cc01815cf6
    decision: ACCEPT
    review_path: research/day-07/advisor/H031_review_v1.md
    review_sha256: 0caad6a1cd0d21e31e69b43fd28858120ceda8f4d779af182dc52437f68c1abe
  - proposal_id: H032
    proposal_sha256: 139205d4964a47720b9032ad58ef147a7f83821dfa1220fb3f1e3dca2376657c
    decision: ACCEPT
    review_path: research/day-07/advisor/H032_review_v1.md
    review_sha256: c69ac98f7c0277e0de916cb01b61d391f85fdc4fe9c4491b80b38001bd279248
  - proposal_id: H033
    proposal_sha256: c908b3bedf691067020bca2bf86c826eae72a0082caad52e49710bef52649adc
    decision: ACCEPT
    review_path: research/day-07/advisor/H033_review_v1.md
    review_sha256: 33b536e33857f5ac262ea9b3d10e3b343f1010946a782f9e11f2ff13c0485482
completed_utc: 2026-10-03T17:20:44Z
```
