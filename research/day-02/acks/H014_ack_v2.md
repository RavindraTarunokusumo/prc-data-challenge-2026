# Acknowledgement — H014 v2 (exchange X-D02-S01-0005)

- proposal: `research/day-02/proposals/H014_v2.md`, sha256 `49a8ec9036a62c59850a61c102119c17eb5b136a1941d8b09a63819374b441f4`
- review: `research/day-02/advisor/H014_review_v2.md`, sha256 `4d6395c87af7c72effa2a6e4eaa854524519b85300e954b069fb0b8e57bb1c9a`
- decision received: **ACCEPT** (confidence 0.85), conditional. Both hashes verified by the researcher.

## Adopted preconditions (before `gate.py allocate H014 v2`)

- (a) H013 v2 has decision ACCEPT, and `H013_ack_v2.md` is committed.
- (b) **H013 v2's primary run used exactly its authorized configuration,** checked in its `config.yaml`:
  - `model: lightgbm`;
  - `params`: `objective: regression`, `learning_rate: 0.05`, `num_leaves: 255`, `min_data_in_leaf: 100`, `feature_fraction: 1.0`, `bagging_fraction: 1.0`, `bagging_freq: 0`, `bin_construct_sample_cnt: 5000000`, `num_threads: 4`, `num_boost_round: 1000`;
  - `seed: 42`;
  - no other training parameter.
- (c) H013 v2 uses H014 v2 as its M1 reference (`mechanism_check.py <H013> <H014> NM_present_excl_LIRF` and `… NM_present`).
- (d) H013 v2's primary run is COMPLETE, and H013 does not meet its clause 1.
- (e) The code and environment are unchanged:
  - the `fs0` body and `gbm.py` are unchanged, `uv.lock` is `39df945c…` and silver is pinned;
  - the clause code is unchanged from `5ba9230` until clauses 2(a) and 2(b) are computed;
  - no other experiment runs concurrently.

**Lapse rule adopted:** if (b) or (c) fails, this ACCEPT lapses and `H014_v3` is required.

**Recorded:** H014 v2 matches H013 v2's shared-feature bins **by construction**, because both build bins from all rows of identical training rows. This supersedes the seed-dependent record in `H014_ack_v1.md`.
