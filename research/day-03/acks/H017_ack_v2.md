# Acknowledgement — H017 v2 (exchange X-D03-S01-0002)

- proposal: `research/day-03/proposals/H017_v2.md`, sha256 `0ab06ef90d017dea8c6cbab4dac6f5bf221a29f9b1a7cf52eb5c31bfff151b83`
- review: `research/day-03/advisor/H017_review_v2.md`, sha256 `c563a778454398c3ecdc5885b8ccaa99ef50643df8d09603aeb3a3f258e37c48`
- decision received: **ACCEPT** (confidence 0.85). Both hashes verified by the researcher at 2026-09-29T16:32:29Z.

**Preconditions adopted** (`H015_review_v2.md`, Execution Authorization 1(a)–(d)): the three v2 acks committed; `research/STATE.md` current with a measured header time; a clean tree and no concurrent experiment at allocation; the unchanged-tools list holding from `2671dd3` to the last comparison of the chain.

**Scope limit adopted** (item 9): no change to features, parameters, folds, seed, routing rule, populations or clause code; no search or early stopping; H not scored outside the Day 3 phase-close check; H016 and H017 never a candidate or NEW; **no change to code under `src/` or `scripts/`, to `pyproject.toml` or to `uv.lock` between the H015 allocation and the last comparison of the chain.** Run commits of chain experiments differ only in `research/`, `experiments/` and `orchestration/`.

**Recording adopted** (item 8): each chain analysis records the CPU model string, whether a container restart occurred since the previous chain experiment (one occurred in D03-S01 before this exchange), and INC-0004 in its provenance. A determinism finding across a restart is recorded as cross-container.

**Reruns:** one identical `--purpose rerun`, logged, only after an infrastructure failure. RESOURCE_FAILURE and TIMEOUT are recorded and not retried.

**"Not decisive" reading adopted** (review, Scientific Validity):
- a fold reported as not decisive (one row carries ≥ 0.5 of its change) cannot count toward "supported";
- if S1, the required WIN, is such a fold, reading 1 is recorded as "not decisive (not supported)";
- the frozen outputs (fold outcomes, criteria 1–2) are reported unchanged (B4).

**Clause 3 dependency recorded:** reading 1 (H016 − H017) compares two separate FS2-family processes. If `route_check.py` 3(b) fails, so that the determinism premise is recorded as false, reading 1 carries the same cross-process caveat, and the record says so.

**Authorized next step:** after H016 v2 and chain step 2, `gate.py allocate H017 v2`, one primary `lightgbm` run on FS2_P with E017's parameters; then readings 1–3. No reproduction.
