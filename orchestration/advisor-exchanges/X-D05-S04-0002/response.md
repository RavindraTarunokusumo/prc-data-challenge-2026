I'm returning one acceptance and three revisions:
- **LAPTOP_REFS v2:** ACCEPT (0.88).
- **H021 v2:** REVISE (0.85).
- **H022 v2:** REVISE (0.92).
- **H023 v2:** REVISE (0.88).

Nothing in the H021–H023 chain can run yet. All four proposal hashes match the envelope.

**The new route-integrity reference works.** I confirmed E029's routed rows can serve as the 1e-6 s reference for the CatBoost runs:
- **Real data, no target:** the ridge's input matrices from the FS2 and FS2_RAW feature builds are bit-identical on W1c, S1c and W1, in addition to the researcher's R3. That covers 4 of 8 folds.
- **Synthetic GPU data:** a CatBoost fit earlier in the same process leaves the ridge's output unchanged. The CatBoost and LightGBM routed paths give identical routed rows.
- **Existing files:** E029 equals E026 bit for bit on every routed row of all 8 folds.

I put the chance that H021 passes the route check at about 0.95. The ratifications are granted: E029 for its three uses, E028 in the reduced role, E027 for curves only. One condition is added: each chain run records the lock hash, library versions and the launching shell's thread variables.

**Why H021 and H022 come back:**
- **H022's comparability check would mark H021's mechanism test inconclusive by construction.** On a synthetic GPU fit, CatBoost's resolved settings differ between the two arms on keys outside H022's exemption list. The main one is `data_partition` (FeatureParallel against DocParallel). Six more appear only when categorical features are declared: `permutation_count`, `fold_permutation_block`, `has_time`, `counter_calc_method`, `ctr_history_unit`, `ctr_target_border_count`.
- **The fix is the researcher's choice.** Either exempt a closed list with a rationale, or set `data_partition` the same in both arms; both values are accepted in both modes. The second option changes both configurations, so the pair is revised together.
- **The tools freeze is anchored to the wrong commit.** It starts at the X-D05-S04-0001 submission (`503763b`), but `60365dd` has since changed `gbm.py`, `curves.py`, `worker.py` and `run_experiment.py`. The list also leaves out `linear.py` (the routed ridge), `attribution.py` (the clause population) and `uv.lock`.
- **H021's seed-43 reproduction needs its own route check,** because H023's reproduction blend uses it.

**Why H023 comes back:**
- **Criterion 7 is stated two ways.** One passage says H021 is CLASS-M; another says it declared its class "from measured RAM". It actually declared CLASS-L from runtime. With about a 0.65 chance that H021 runs over 30 min, the two readings decide differently.
- **An INCONCLUSIVE mechanism clause has no stated consequence for promotion.** It should bar promotion.
- **The reproduction blend needs a route check.**
- **It inherits the freeze error and has one typo:** "E026 and E026" should read "E026 and E027".

**CLASS-L for H021: justified, for H021 and its reproduction only.** The measured exact configuration gives 28–35 min against CLASS-M's 30-min target. Cutting iterations would change a configuration already accepted. Unlike H020 on Day 4, it is tied to decisions. Conditions: no parameter changes, a CLASS-M comparison and any swap use reported beside criterion 7, and H023 reads H021's class as CLASS-L. v3 can carry this unchanged.

**My forecasts for revised runs:**
- **H021's mechanism clause not met** (categorical statistics help by at least 3 s): P 0.60.
- **H023's complementarity clause not met:** P 0.35.
- **H023 promotion:** P 0.04. Its S1 fold is the likely blocker: a WIN has P 0.07 and a LOSS P 0.25.

**What I did not do:**
- I read no December target, ran no `holdout_check.py`, and fitted or scored no model on a real fold with a real target.
- The experiment lock was free at every check.
- The real-data check peaked at 4.0 GB of memory.
- The only files written to the repo are the four reviews. Scratch scripts stayed in the session scratchpad.

Each review lists what is acceptable as is, so v3 of H021, H022 and H023 can be one small exchange. LAPTOP_REFS v2 stands.

Files are in `/home/rvindra/Projects/prc-data-challenge-2026/research/day-05/advisor/`:
- LAPTOP_REFS_review_v2.md
- H021_review_v2.md
- H022_review_v2.md
- H023_review_v2.md

```yaml
schema: advisor-task-result-v1
exchange_id: X-D05-S04-0002
status: COMPLETE
decisions:
  - proposal_id: LAPTOP_REFS
    proposal_sha256: 4a4a03d75eeb6a5318003a9bb5d80ebbf5b34dda0df30b87af6bed61d95312da
    decision: ACCEPT
    review_path: research/day-05/advisor/LAPTOP_REFS_review_v2.md
    review_sha256: fc96008d7577548baf77fa66b9dc4e7a4db129971e13e55b6168929448be52e1
  - proposal_id: H021
    proposal_sha256: c97b36b34eeda65400d861381722f0a339d8edd5e1114f88cfddbeeb57d7acde
    decision: REVISE
    review_path: research/day-05/advisor/H021_review_v2.md
    review_sha256: 4d1325bca6e7d4c000ff4f7e9bf836c0b6542dc50ef6564864b3e30a2da3e43d
  - proposal_id: H022
    proposal_sha256: 363b736693175f9224ea5cd2d5fcd6d4806a40522c2a8a7b05eabd1bbeafb920
    decision: REVISE
    review_path: research/day-05/advisor/H022_review_v2.md
    review_sha256: 3c651e292d777aeb7d1059156af6486cb12a55572e3e8588274c977034d242f9
  - proposal_id: H023
    proposal_sha256: 05b13cfb32db777fa20fbf4706b3367a158b8604b207005a5f4d978730226a7c
    decision: REVISE
    review_path: research/day-05/advisor/H023_review_v2.md
    review_sha256: 4ad25586420c5e3a2cef6f84efd9a3460680c6351a70ccebe464d724d9ac8bef
completed_utc: 2026-10-01T20:19:34Z
```
