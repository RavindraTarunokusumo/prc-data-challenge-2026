## Advisor result, X-D06-S01-0002 (batch H024–H028 v2, delta review)

**All five proposals are accepted, so the batch may run in tonight's window.** Each acceptance comes with seven binding conditions (C1–C7). They are written once, in `H024_review_v2.md`, and the other four reviews point to them. None of them changes a design, threshold, population or fold.

**Checks done first (read-only):**
- No fit, no score, no truth read, no holdout access.
- All five proposal hashes match the envelope.
- The experiment lock is free: no lock is held on `runtime/experiment.lock`, and its `E034` text only names the last holder. About 9.7 GiB of RAM is available.
- The next id is E035. No acks or allocations exist yet.

### What was revised

- **Every v1 required revision is made,** and the binding ruling is acknowledged.
- **The v1 to v2 diffs contain nothing unrequested.** They hold only the required items, the recommended items you adopted, and the new run order.
- **Two v1 bullets were dropped:** "selection hazard" and "none is a holdout NEW". The ruling bullet now covers both, more strictly.

### What was verified

- **Launcher.** Its hash on disk and at `377143d` is `9da5b0c3…cf6a4d`, as pinned in §Batch.
- **Freeze.** Nothing under `src`, `scripts`, `pyproject.toml`, `uv.lock` or `config` has changed since the Day 5 merge.
- **Seeds.** The runner takes each run's purpose from `gate.json`, and `primary` requires seed 42. All five configs use 42, so H027's earlier refusal is gone.
- **Configs.**
  - H024 equals E031's config except `max_ctr_complexity` and the supervisory `job_class`.
  - H027 equals E029's except the four stated keys.
- **Blend inputs.**
  - All 32 prediction files of E029, E030, E031 and E033 match their manifests.
  - E030's route check passes on all 8 folds.
- **Truth and holdout.** The route check reads predictions plus three target-free silver columns. `mechanism_check.py` reads truth only through `truth_frame`, which refuses holdout and final folds.
- **Cited figures reproduce.**
  - Blend re-draw +0.263 s, W1 +1.282 s.
  - Full-size re-draw +0.683 s (q95 +1.075), LOSS on R1 and W1.
  - The DAY_SUMMARY §1 phrase is verbatim (line 14).

### Binding conditions

- **C1, ids.** Allocate in this order, all purpose `primary`: H026 → E035, H024 → E036, H025 → E037, H027 → E038, H028 → E039.
  - Before arming, check each `gate.json` and `config.yaml` against its proposal.
  - If anything differs, do not arm. The pinned launcher hard-codes the queue, so a mismatch comes back to me.
- **C2, failures.**
  - No re-attempt or `rerun` allocation is authorized.
  - A blend whose component failed is recorded "not run (component …)".
  - A run refused before RUNNING counts as deferred.
- **C3, later windows.** A deferred run goes ahead at the owner's next window in one of two ways:
  - a direct `run_experiment.py` call; or
  - a new launcher whose hash is recorded before that window, differing only in date, times and remaining queue.

  The pinned file is never edited.
- **C4, diagnostic code.** The residual correlations, the decomposition and the closed-set comparison need code. It goes outside `src/` and `scripts/` while the freeze holds, is committed with its output and cited by hash, and runs after the window.
- **C5, wording.** A "carries" reading is recorded in bounded form: q95 below +1.0 s, one draw, equal weight, with the per-fold outcomes beside it.
  - If any fold is LOSS, the record says the removed ingredient carries a measurable part below 1.0 s.
  - "E033's margin needs no CatBoost" (H024 §Batch, H028) and "is a substitute" (rung B) get bounded wording.
  - Without this, the record could say "not needed" while a measurable part sits below 1.0 s.
- **C6, closed set.** The comparison covers every resolved key. A key present in only one arm counts as a violation; Day 5's `only_one_arm` listing does not exempt it.
- **C7, records.**
  - Any run still going at 21:30 is reported as a deviation, with its end time.
  - The launcher log goes into the session record.
  - Each analysis states the freeze diff, launcher included.
  - The H026 ack carries the attestation that no E029 + E030 blend figure was computed before the run.
  - The X-D06-S01-0001 ruling stands.

### Not blocking

- "More than 75 %" is actually 74.7 %.
- Dropping "ordered permutations" from the leakage sentence is harmless: the training-row statistics are still permutation-ordered under plain boosting.
- Rung A is one draw of the subsampling seed. Record its floor as "at seed 42".
- The W&B sync has no timeout of its own. A stall would only cause deferrals, never a result-dependent choice.

### Forecast correction

My v1 review used too wide a noise reference for the blend readings. A blend-against-blend contrast moves only half the component difference, so its spread is about 0.2–0.25 s, not 0.44 s. That makes a bounded "rung C carries" reading more likely than either of us forecast: I now put it at 0.60, against your 0.30.

### Other forecasts

- **Rung B:** "statistics carry part", P 0.72.
- **Rung A:** "twin does not reproduce the gain", P 0.95.
- **H024's own reading:** 0.35 / 0.30 / 0.35 across its three outcomes.
- **Window:** E038 and E039 run tonight with P 0.50. E038 needs E036 to finish within about 9.5 minutes.

### Review files

- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H024_review_v2.md` (shared findings and conditions C1–C7)
- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H025_review_v2.md`
- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H026_review_v2.md`
- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H027_review_v2.md`
- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H028_review_v2.md`

The acks go to `research/day-06/acks/H02x_ack_v2.md`. I wrote only these five files. I did not write `response.md` or `checksums.sha256`; per the communication contract, you store this message verbatim.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D06-S01-0002
status: COMPLETE
decisions:
  - proposal_id: H024
    proposal_sha256: 483ed0ab9995a2b067905062213b628b63f85d8f4cebdb10e25aa2188a1b71db
    decision: ACCEPT
    review_path: research/day-06/advisor/H024_review_v2.md
    review_sha256: c2c034edf0bcd83767e1a4ea7b15215e89f54d9a11f614be52318a4cc2c1bba3
  - proposal_id: H025
    proposal_sha256: 44db30f7e22dda4d21d5d6bbcd88e649b234a1b7563cde2033b6e301f2cd26df
    decision: ACCEPT
    review_path: research/day-06/advisor/H025_review_v2.md
    review_sha256: 515a376cbea31194182215e10cfc962406c7606447f059088a907bf466cfef3c
  - proposal_id: H026
    proposal_sha256: a4a9ae5000626b1eb92b110ddb4a0f6d3813729b012b8a89352cf78ebc5d6bbc
    decision: ACCEPT
    review_path: research/day-06/advisor/H026_review_v2.md
    review_sha256: 939ed3c2b72b52f970b08097648fb5c569fe3dcbfe6f979b50291e72b9b6cd40
  - proposal_id: H027
    proposal_sha256: eb9168eaef588209b22946f6cde4f4b68bcac8ebada5fe1c171ae559912ccc95
    decision: ACCEPT
    review_path: research/day-06/advisor/H027_review_v2.md
    review_sha256: f1eb5bd13df9e498bc32411e6cb2ce13ee284509e61068daa69010a4d4434b3b
  - proposal_id: H028
    proposal_sha256: 65b8f3fbc816a7bde428c7f39a8c40525dfb1ea4c9595b56444e14d4567d70a2
    decision: ACCEPT
    review_path: research/day-06/advisor/H028_review_v2.md
    review_sha256: 8f6aa94cf127b98350c85dc246639df7f0370ac8c36e3a7fe1908dec9e647433
completed_utc: 2026-10-02T18:12:04Z
```
