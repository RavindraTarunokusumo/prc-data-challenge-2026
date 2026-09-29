# Acknowledgement — H011 v1 (exchange X-D02-S01-0001)

- proposal: `research/day-02/proposals/H011_v1.md`, sha256 `3a8b59483923c500b764dc326d0b014a7bc68b0d6689575a0d7e8530f66cbb70`
- review: `research/day-02/advisor/H011_review_v1.md`, sha256 `b6532574350a1ed5c1c519051085e61e723683c3944ac893ba96db925b4d1a28`
- decision received: **REVISE** (confidence 0.80). Both hashes verified by the researcher.

This acknowledgement confers **no authority**. The researcher accepts the four required revisions and will submit `H011_v2.md` together with `H009_v2.md`:
1. **The schedule-delay proxy.** v2 **removes** it from H011's design. The local scheduled-time keys are dropped, so that a model without the anchor has no route to the schedule delay.
2. **The static-signal falsification** is insulated from the LIRF NM-missing subgroup, with the producing code committed before the run.
3. **M2 role.** H011 is no longer H009's M2 comparator. M2 moves to a new ablation that holds `d_sched` fixed.
4. **Record corrections.** "Nearly causal" is withdrawn. The runtime estimate is corrected (v1 has 13 features). The ranking-unseen shares are not 0 %. `created_utc` 18:24:00Z was not a measured time. E010's dirty-tree flags are recorded.
