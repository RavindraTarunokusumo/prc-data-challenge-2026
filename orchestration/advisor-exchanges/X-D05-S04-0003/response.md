## X-D05-S04-0003: all three accepted (H021 0.88, H022 0.90, H023 0.88)

H021 v3, H022 v3 and H023 v3 are all ACCEPTed. Each v3 makes every revision its v2 review required, and the v2-to-v3 diffs touch nothing else. No revision is required. The chain can run after the three v3 acks are written.

**What I checked**
- **Hashes and lock.** All three proposal hashes match the envelope. The experiment lock (`runtime/experiment.lock`, content E029) is not held by any process, and no experiment was running.
- **Tools-freeze anchor.** It is commit `803ceeba5965bd7c0d415eb44a13d6921854f6eb`, the commit that adds this envelope and the v3 proposals. HEAD is that commit and the tree is clean. Since `60365dd` (the code reviewed in v2), only two pieces of code changed:
  - `scripts/diag_cb_params.py`, which is new;
  - the `environment()` record in `src/prc/worker.py`.
- **The worker change only adds a record.** It runs after every fit and adds about 37 MB. The synthetic worker test passes. It records library versions, the lock hash and thread variables, and no secrets. In this venv it reads exactly rule L v2 item 6's environment.
- **The comparability set is right.** H022's 13 exempt keys equal the difference recorded in `cb_param_diff.json`, key for key:
  - 3 keys differ between the arms;
  - 10 keys exist only in the ctr arm, and none only in the codes arm;
  - the other 45 shared keys are equal.
- **The evidence is valid.** It was produced from H021's exact parameter table, on R3 with a permuted training target, and no metric was computed.
- **The `data_partition` exemption holds.** The gpu_calibration file shows both layouts already vary between identical fits.
- **No real data used.** No real target was read and no fit was run on real data. The only repo changes are the three review files.

**Notes that don't block the runs**
- **H021:**
  - No frozen script compares two runs' `resolved_params.json`. The analysis must record the full per-fold key difference for all 8 folds.
  - The freeze rule (only records may differ) covers `config/` and `tests/`, but the stated `git diff` check does not. The runner reads `config/resources.yaml`, which sets the class limits. The scope is written into the authorization.
  - If H021's reproduction ends in RESOURCE_FAILURE, clause 1 has no verdict and the chain stops.
- **H023:**
  - v3 also makes clause 1 INCONCLUSIVE when the H021/H022 pair doesn't match. That costs a little power and adds no validity, but it is pre-registered and binding.
  - If H023's reproduction can't run, or is INVALID, criterion 6 is not met and H023 is not promoted.
- **Housekeeping.** `research/STATE.md`'s Day 5 block is stale: it was last updated at 18:56Z, before X-D05-S04-0002.

**Predictions**
- The CatBoost categorical statistics help by at least 3 s (H021's mechanism clause not met): P 0.60.
- The blend shows complementarity on normal taxis (H023's clause 1 not met): P 0.35.
- H023 is promoted: P 0.04.

**Next steps for the researcher**
1. Write the acks `research/day-05/acks/H021_ack_v3.md`, `H022_ack_v3.md` and `H023_ack_v3.md`, each referencing its proposal hash and review hash.
2. Store this message as `orchestration/advisor-exchanges/X-D05-S04-0003/response.md`.
3. Run in order: H022, H021, the H021 reproduction, then H023.

Files are in /home/rvindra/Projects/prc-data-challenge-2026/research/day-05/advisor/:
- H021_review_v3.md
- H022_review_v3.md
- H023_review_v3.md

```yaml
schema: advisor-task-result-v1
exchange_id: X-D05-S04-0003
status: COMPLETE
decisions:
  - proposal_id: H021
    proposal_sha256: b8618266bf2cd259415ab3879435d5f016f8dee780a50c798d1b6cba68a19716
    decision: ACCEPT
    review_path: research/day-05/advisor/H021_review_v3.md
    review_sha256: 1091353daa939921da5326f99b04987544104b8bc702bc630c55abd5f1e145df
  - proposal_id: H022
    proposal_sha256: 43526f13c690193fe06fcc65b6fd32de6247d83a40178cdf81a0c6c9ccc9d95b
    decision: ACCEPT
    review_path: research/day-05/advisor/H022_review_v3.md
    review_sha256: 7d402c5ec8488ee8979cc377912c2e3420afcb5419b765d11781ee2e9efc8518
  - proposal_id: H023
    proposal_sha256: 41712f57b3befe4ad4a342bc129a6e447b1fd31c1e01b2070dab4903da83eec2
    decision: ACCEPT
    review_path: research/day-05/advisor/H023_review_v3.md
    review_sha256: 8a6d0719e17f468895e102d21faa1727cd43cb12590418e181723d084973e9ea
completed_utc: 2026-10-01T20:38:04Z
```
