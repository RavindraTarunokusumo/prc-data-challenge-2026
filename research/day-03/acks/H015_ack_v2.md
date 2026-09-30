# Acknowledgement — H015 v2 (exchange X-D03-S01-0002)

- proposal: `research/day-03/proposals/H015_v2.md`, sha256 `468b442de9f20b3d16e676d1e3584fd0fec0e3efa442b83f7133e9c975ecf499`
- review: `research/day-03/advisor/H015_review_v2.md`, sha256 `10b99752059e4f0b8a58a6a1d0f6d8154d86f9424b2e55966ced130d50d6e120`
- decision received: **ACCEPT** (confidence 0.85). Both hashes verified by the researcher at 2026-09-29T16:32:29Z.

**Preconditions adopted** (`H015_review_v2.md`, Execution Authorization 1(a)–(d)): the three v2 acks committed; `research/STATE.md` current with a measured header time; a clean tree and no concurrent experiment at allocation; the unchanged-tools list holding from `2671dd3` to the last comparison of the chain.

**Scope limit adopted** (item 9): no change to features, parameters, folds, seed, routing rule, populations or clause code; no search or early stopping; H not scored outside the Day 3 phase-close check; H016 and H017 never a candidate or NEW; **no change to code under `src/` or `scripts/`, to `pyproject.toml` or to `uv.lock` between the H015 allocation and the last comparison of the chain.** Run commits of chain experiments differ only in `research/`, `experiments/` and `orchestration/`.

**Recording adopted** (item 8): each chain analysis records the CPU model string, whether a container restart occurred since the previous chain experiment (one occurred in D03-S01 before this exchange), and INC-0004 in its provenance. A determinism finding across a restart is recorded as cross-container.

**Reruns:** one identical `--purpose rerun`, logged, only after an infrastructure failure. RESOURCE_FAILURE and TIMEOUT are recorded and not retried.

**Rule 6 reading adopted** (review (b)): "no row carries ≥ 0.5 of a fold's change" is expected only on folds with a real effect. A dominant row on a fold with |dRMSE| below about 1.5 s is expected and is not evidence against the clause. On a fold with |dRMSE| ≥ 4 s it is unexpected and is reported with its details (B4). This changes no fold outcome.

**Record correction noted:** the v1 review's runtime note should read 32 against 17 inputs, not 38 against 23.

**Authorized next step:** `gate.py allocate H015 v2`, one primary `routed_lightgbm` run on FS2 with E017's parameters and `route_ridge_params {alpha: 1.0, winsor: [0.005, 0.995]}`, folds R1, R2, R3, S1, W1, S1c, W1c, H, seed 42, CLASS-M; then chain step 1.
