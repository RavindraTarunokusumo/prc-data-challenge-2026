# Acknowledgement — H016 v2 (exchange X-D03-S01-0002)

- proposal: `research/day-03/proposals/H016_v2.md`, sha256 `7f44ac059e993f55a8a70913d011647737795e1e3a162068366fb574335ff58b`
- review: `research/day-03/advisor/H016_review_v2.md`, sha256 `e3ab0584c43acf7819573c5714427d4d631731db77d07388ffd238565c9d0edc`
- decision received: **ACCEPT** (confidence 0.88). Both hashes verified by the researcher at 2026-09-29T16:32:29Z.

**Preconditions adopted** (`H015_review_v2.md`, Execution Authorization 1(a)–(d)): the three v2 acks committed; `research/STATE.md` current with a measured header time; a clean tree and no concurrent experiment at allocation; the unchanged-tools list holding from `2671dd3` to the last comparison of the chain.

**Scope limit adopted** (item 9): no change to features, parameters, folds, seed, routing rule, populations or clause code; no search or early stopping; H not scored outside the Day 3 phase-close check; H016 and H017 never a candidate or NEW; **no change to code under `src/` or `scripts/`, to `pyproject.toml` or to `uv.lock` between the H015 allocation and the last comparison of the chain.** Run commits of chain experiments differ only in `research/`, `experiments/` and `orchestration/`.

**Recording adopted** (item 8): each chain analysis records the CPU model string, whether a container restart occurred since the previous chain experiment (one occurred in D03-S01 before this exchange), and INC-0004 in its provenance. A determinism finding across a restart is recorded as cross-container.

**Reruns:** one identical `--purpose rerun`, logged, only after an infrastructure failure. RESOURCE_FAILURE and TIMEOUT are recorded and not retried.

**Record note adopted** (review, Scientific Validity): H016 v2's development-mean expectation (360–380 s) is looser than its dRMSE range implies. −2 to −15 s against E017's 378.82 gives 363.8–376.8 s; the two ranges should coincide. No clause depends on it.

**Authorized next step:** after H015 v2's primary and chain step 1, `gate.py allocate H016 v2`, one primary `lightgbm` run on FS2 with E017's parameters; then chain step 2 (`route_check.py <H015> <H016> E005`, `mechanism_check.py <H015> <H016> LIRF_NM_missing`) and H016's own comparisons.
