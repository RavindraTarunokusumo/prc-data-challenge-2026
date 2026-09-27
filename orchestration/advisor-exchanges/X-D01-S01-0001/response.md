Decision: **REVISE** (confidence 0.85). SPLITS_v1 is not ready to freeze. Do not run `scripts/gate.py freeze` against v1; no experiment can be allocated until a SPLITS version is accepted and frozen.

Review: `/home/user/prc-data-challenge-2026/research/day-01/advisor/SPLITS_review_v1.md` (SHA-256 `f82eba5d45b0de1b1a9a173b2329b5383910c118154c7b83c102bc3c2f96e34e`). It is the only file I wrote; I did not write `response.md` or `checksums.sha256` — mirroring stays with you.

**What checks out**
- The recomputed proposal hash matches the envelope, so there is no HOLD.
- All five pinned files and the two evidence hashes match the files on disk, and `silver.parquet` matches its manifest.
- `uv run pytest` passes 35/35.
- No tracked file contains a configured secret value.
- Commit `866b902`, which landed during the review, touched none of the freeze candidates.
- The fold table (row counts and std) reproduces exactly.
- Masking is correct on real data. ARR rows carry no copy of the DEP block time; their `AOBT_3` equals the DEP row's in 100% of linked pairs.
- `AOBT_3` in the ranking file shows no sign of perturbation by the organisers.
- The snapshot availability definition is faithful to the competition.
- Compute is well within CLASS-S: 1.0 s and 2.2 GB peak (the proposal's "< 2 GB" is slightly low).

**Required for SPLITS_v2** (how to fix each is your choice)
- **R1 – Pin the evaluation population.**
  - `evaluate()` scores against whatever silver its caller passes, and nothing enforces per-fold row counts or a fingerprint.
  - The frozen `splits.py` finds `splits.yaml` through `src/prc/paths.py`, which is not frozen. `data.py` is not frozen either.
- **R2 – Make the holdout guard real.**
  - The once-per-phase limit matches a free-form phase string, so any new label resets it.
  - `evaluate()` hands back per-row December truth.
  - State the scope honestly: the Day 1 audit already read December's target distribution, and `test_holdout_guard` scores real December truth on every pytest run.
- **R3 – Promotion needs a noise floor.**
  - A +60 s change on only 0.14–0.34% of rows (those over 3,600 s) moves fold RMSE by 0.75–1.62 s.
  - S1, the veto fold, has 63.6% of its squared error in the top 0.1% of rows.
  - Criteria 1–2 need a pre-registered threshold or paired test, and the rerun protocol (seed policy, what must reproduce within 1.0 s) must be specified.
  - `promotion_check` must read the frozen config. Today no code reads the `promotion:` block, and callers can override its defaults.
- **R4 – Winter is missing from model selection.**
  - January is 44.3% of scored rows, and no development fold validates a winter month.
  - In Jan–Feb 2025 the 90th percentile is higher than in the dev months: EDDM +253 s, LTFM +166 s, LSZH +98 s, EHAM +88 s, LFPG +66 s.
  - 12 of the 21 disrupted airport-days in Jan–Nov fall in Jan–Feb.
  - Either add winter coverage, re-assign which months play which role, or pre-register what an H result at phase close actually does. Justify the choice with training data, not December. The brief's own §9 example validates December as a rolling fold.
- **R5 – Control S1's post-July training months.**
  - At LFPG, 27L/09R went to 0% after July 2025 and 27R/09L took over. The median rose from 895 s in June to about 1,013 s in Aug–Nov.
  - S1 can learn that July regime only from Sep–Nov. Record this in DATASET_AUDIT §6.5 and pre-register a control.
  - If you choose a diagnostic fold, it has to be frozen now.
- **R6 – Fix the backward/forward labels.**
  - Labels are relative to takeoff, so the row's own taxi interval counts as "backward" and a causal-only variant can't be defined.
  - Also state whether Jan↔Jul 2026 cross-month information is admissible; no development fold can validate it.

The review also lists non-blocking recommendations (import-isolation test, gate hash in allocation records, and others) and nits.

**Other notes**
- H001–H008, committed during the review, were outside this envelope and not reviewed.
- My read-only checks read no December targets beyond one recomputation of H's row count and std, which the proposal already publishes.
- Next steps: write `research/day-01/acks/SPLITS_ack_v1.md` referencing both hashes, then resubmit as `SPLITS_v2.md` in a new exchange with re-pinned hashes.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D01-S01-0001
status: COMPLETE
decisions:
  - proposal_id: SPLITS
    proposal_sha256: 4cf31a97946c010de04856d82e041c9f3c3755697ea7d467841a31c4bd7dc022
    decision: REVISE
    review_path: research/day-01/advisor/SPLITS_review_v1.md
    review_sha256: f82eba5d45b0de1b1a9a173b2329b5383910c118154c7b83c102bc3c2f96e34e
completed_utc: 2026-09-27T11:24:44Z
```
