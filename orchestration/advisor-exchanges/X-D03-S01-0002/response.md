# Advisor response — X-D03-S01-0002

Final message of the `advisor` subagent, mirrored verbatim below the rule. No secrets present.

---

All three v2 proposals are ACCEPTED, so the H015 chain may run once the acks and a current STATE.md are committed. I wrote the three review files and nothing else.

**Decisions**
- **H015 v2: ACCEPT** (confidence 0.85). All six v1 revisions are done, and the items the v1 review found acceptable are unchanged (checked by diff).
  - **The congestion clause can no longer be decided by one record.** The new clause population (NM-present rows outside LIRF) excludes row 192622644. Computed without targets, its largest in-taxi count is 93–129 per fold, against 486 for that row. One row would need a squared-error change of 1.9–2.6 × 10⁸ s² to carry half of a −6 s fold change; the largest seen on this population is 4.5 × 10⁷ s².
  - **The P-feature fix is correct.** The two new tests fail 6 times on the old code and pass on the new. My own recomputation of all ten P features on 3,262 real July rows matches the code exactly (this includes every row that takes off at or before its off-block proxy). Moving a row's own takeoff changes none of them.
  - **Other checks.** The noise table matches the committed comparison files to 0.01 s. The routing rationale now rests on Day 1 figures, as ruling B requires. Criterion 3 at LIRF has ample room: 0.977 against a 1.03 tolerance.
- **H016 v2: ACCEPT** (confidence 0.88). Its three revisions are done. Its all-rows comparison with E017 may be driven by rows without an NM match rather than by queueing. The proposal already reports that figure whatever its sign.
- **H017 v2: ACCEPT** (confidence 0.85). Its four revisions are done. The ack must adopt one reading: a fold marked "not decisive" cannot count towards support. The ack must also note that reading 1 depends on H015's clause 3 determinism check.

**Conditions of the authorization** (full text in `H015_review_v2.md`, Execution Authorization)
- **Before allocation:** the three acks are committed, STATE.md is brought current and the tree is clean. STATE.md is stale now: last written at 14:03Z, it still lists X-D03-S01-0001 as pending.
- **Code freeze:** no change to code under `src/` or `scripts/`, to `pyproject.toml` or to `uv.lock` from the H015 allocation to the last comparison of the chain. This closes gaps in the proposal's own list (`worker.py`, `run_experiment.py`, `data.py`, `models/__init__.py` and the helpers in `features.py`).
- **Recording:** each chain analysis records the CPU model, whether the container restarted since the previous run, and INC-0004. The container restarted once this session, and identical outputs across processes are likely but not guaranteed on a different host.
- **Reruns:** one logged `rerun` is allowed after an infrastructure failure only. A RESOURCE_FAILURE or TIMEOUT is not retried.

**What I expect.** Clause 1 against E005 passes (0.93). The congestion effect probably lands at −3 to −5 s, above the −6.0 s floor. H015 is therefore most likely falsified on clause 2(b), with its margin of about 40 s over E005 intact. I put the chance that H015 is promotable at 0.20.

**Record corrections**
- The v1 review's runtime note said "38 against 23 inputs"; the correct figures are 32 against 17.
- H016's development-mean range (360–380 s) is looser than its dRMSE range implies (363.8–376.8 s).

**What I verified.** Everything was read-only, target-free or synthetic: no December target was read, and no model was fitted or scored on real data.
- **Hashes:** the proposals, the frozen files, `advisor.md`, `uv.lock`, silver and the X-D03-S01-0001 mirror all match.
- **Predictions:** the reference prediction files of E005, E006, E012, E015, E017 and E018 match their manifests.
- **Code:** unchanged since E017's run where claimed. The FS2 frames carry exactly E005's and E017's inputs.
- **Tests:** pytest passes 123/123 and ruff is clean.
- **Ledger:** there is no Day 3 allocation and no FS2 output anywhere.
- **Secrets:** no credential value appears in the 410 tracked files.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D03-S01-0002
status: COMPLETE
decisions:
  - proposal_id: H015
    proposal_sha256: 468b442de9f20b3d16e676d1e3584fd0fec0e3efa442b83f7133e9c975ecf499
    decision: ACCEPT
    review_path: research/day-03/advisor/H015_review_v2.md
    review_sha256: 10b99752059e4f0b8a58a6a1d0f6d8154d86f9424b2e55966ced130d50d6e120
  - proposal_id: H016
    proposal_sha256: 7f44ac059e993f55a8a70913d011647737795e1e3a162068366fb574335ff58b
    decision: ACCEPT
    review_path: research/day-03/advisor/H016_review_v2.md
    review_sha256: e3ab0584c43acf7819573c5714427d4d631731db77d07388ffd238565c9d0edc
  - proposal_id: H017
    proposal_sha256: 0ab06ef90d017dea8c6cbab4dac6f5bf221a29f9b1a7cf52eb5c31bfff151b83
    decision: ACCEPT
    review_path: research/day-03/advisor/H017_review_v2.md
    review_sha256: c563a778454398c3ecdc5885b8ccaa99ef50643df8d09603aeb3a3f258e37c48
completed_utc: 2026-09-29T16:31:02Z
```
