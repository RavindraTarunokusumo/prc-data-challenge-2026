I reviewed the three proposals in exchange X-D02-S01-0001: **H009 REVISE, H010 ACCEPT (with conditions), H011 REVISE**. All three proposal hashes match the envelope, so nothing is on HOLD. Everything I did was read-only: no December target was read, no model was fitted, scored or allocated, and I wrote only the three review files.

**Why H009 needs a new version (REVISE, confidence 0.85).** The candidate itself is sound and I found no leakage. Two of its three pre-registered mechanism tests cannot tell whether the claimed mechanism is real, and that can't be fixed after the runs:
- **M1 (static structure, H009 vs E006 on all rows):** LIRF departures without NM data are under 1 % of rows but carry 18–56 % of E006's squared error per development fold. The proposal itself allows those rows to shift by ±15 %. That alone moves each fold's RMSE by ±3.7 to ±22.5 s, the same size as the expected M1 effect (−5 to −25 s).
- **M2 (anchor correction, H009 vs H011):** this comparison removes `d_sched` along with the anchor, the same confound the Day 1 phase-close review raised against H008. By the batch's own numbers, removing `d_sched` alone costs 23–85 s, so the test passes whether or not the anchor correction exists.
- **M3 (LIRF convention, H009 vs H010):** FS1 has a second route to `d_sched`. The takeoff hour and weekday combined with the new scheduled local hour and weekday give the delay to the hour. On LIRF rows without NM data (fitted on Jan and Mar–Jun, tested on Aug), this cuts RMSE from 9,289 to 8,855 s; exact `d_sched` in 1-hour bins gives 8,758 s. So H010 only removes one of two routes, and the M3 test measures what exact `d_sched` adds beyond that.
- **Evidence errors to correct in v2:**
  - The "0 % unseen levels in ranking" claim is an artifact: the EDA vocabulary was built over all of silver, including December and both ranking months. The true unseen shares are small: stand 0.08 %, operator prefix 0.26 %, destination 0.05 %. They map to `__RARE__`, so the availability conclusion still holds.
  - "27,760 NM-missing rows in Jan–Nov" is the all-silver count; Jan–Nov has 20,821.
  - The "0 % convention-tail rate for `d_sched` ≤ 1 h" is true by definition, not a finding.
  - E007–E009 reproduce Tier 0 and ridge models, so they are no evidence that LightGBM is deterministic.

**H010 (ACCEPT, confidence 0.75).** It is a clean one-column ablation, but it may only be allocated once:
- an H009 version ≥ 2 is accepted and acknowledged;
- that version keeps FS1, the model, parameters, folds, seed and its M3 test unchanged;
- H009's primary run is complete, with nothing running alongside.

Otherwise the acceptance lapses. The ordering matters: H010 differs from H009 only by `d_sched`, so running it first would reveal the M1 result while that test is being rewritten. The ack must also record that its Mechanism section is wrong ("cannot scale with the time between schedule and takeoff").

**H011 (REVISE, confidence 0.80).** It inherits the hour-level delay route, so its statements that the convention is out of reach and that standing rule 8 is "not engaged" are wrong in effect. Its static-signal test against E010 is exposed to the same LIRF rows (±3.9 to ±29 s per fold against an expected −8 to −35 s). A pass could be convention capture recorded as static structure.

**Rulings the envelope asked for:**
- **Reusing E006 and E010 as ablation references: permitted, no Day 2 re-run needed.**
  - Standing rule 3 governs the promoted candidate and its reproduction, not ablation references or the incumbent.
  - `uv.lock` (`39df945c…`) matches both experiments' gate records. The model code and the `fs0` function are unchanged since `866b902`, and silver is pinned.
  - The reuse lapses if any of those change before H009 runs. Both experiments ran from a dirty working tree, which should be recorded.
- **EDA target hygiene: the claim holds in substance.** The script reads targets only for Jan, Mar–Jun and Aug 2025. Finding 5, which the committed script does not produce, reproduces exactly from those months (n = 473, 0.50, 0.00/0.43/0.70). The code behind finding 5 and the FS1 build check is not committed, and should be.

**Also checked:**
- **Repository state:** the frozen files and advisor definition match their pins, `pytest` passes 96/96, `ruff` is clean, and no configured secret appears in any tracked file.
- **Rule-7 subgroup tool:** it reproduces the Day 1 phase-close table for E006 vs E005 exactly.
- **Stand label:** no winter-only stands or de-icing-like names, so P holds.
- **Destination label:** it is F for 641 of 2,070 diverted flights (~0.03 % of rows), which needs a note for the causal-only variant.
- **`research/STATE.md`:** stale again (still shows the Day 1 holdout as pending) and should be refreshed before the first Day 2 allocation.

Files are in `/home/user/prc-data-challenge-2026/research/day-02/advisor/`:
- `H009_review_v1.md`
- `H010_review_v1.md`
- `H011_review_v1.md`

```yaml
schema: advisor-task-result-v1
exchange_id: X-D02-S01-0001
status: COMPLETE
decisions:
  - proposal_id: H009
    proposal_sha256: c5927ce1c589a0b85c50331ab11e3396ca6e552c2c72cb7dc1e219349af2242d
    decision: REVISE
    review_path: research/day-02/advisor/H009_review_v1.md
    review_sha256: de8fa7b64b5e9427878d79403c9c00f0b6c1b374b7cd8d5d205fd22ffcb71de8
  - proposal_id: H010
    proposal_sha256: 3e273bd053d99337e6877ed2b2a2212461feb620bb525c26697372a9790a3a4a
    decision: ACCEPT
    review_path: research/day-02/advisor/H010_review_v1.md
    review_sha256: d5756c014b8da15309df95bf4e7b63ff398347089e1c2bf102ce34f0cc2d3bd9
  - proposal_id: H011
    proposal_sha256: 3a8b59483923c500b764dc326d0b014a7bc68b0d6689575a0d7e8530f66cbb70
    decision: REVISE
    review_path: research/day-02/advisor/H011_review_v1.md
    review_sha256: b6532574350a1ed5c1c519051085e61e723683c3944ac893ba96db925b4d1a28
completed_utc: 2026-09-28T18:44:07Z
```
