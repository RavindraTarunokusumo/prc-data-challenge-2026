# Acknowledgement — H021 v3 (exchange X-D05-S04-0003)

- proposal: `research/day-05/proposals/H021_v3.md`, sha256 `b8618266bf2cd259415ab3879435d5f016f8dee780a50c798d1b6cba68a19716`
- review: `research/day-05/advisor/H021_review_v3.md`, sha256 `1091353daa939921da5326f99b04987544104b8bc702bc630c55abd5f1e145df`
- decision received: **ACCEPT** (confidence 0.88). Both hashes verified by the researcher at 2026-10-01T20:40Z.

The researcher adopts the review's Execution Authorization as written, including its preconditions:
- the freeze anchor `803ceeb` for every path outside `research/`, `experiments/`, `orchestration/` and `docs/` (`config/` and `tests/` included);
- rule L v2 item 6's environment, confirmed from each manifest;
- a clean tree, no experiment running, and nothing memory-heavy beside a run.

It also adopts the review's "Not authorized" list and its execution notes.

Execution note 1 is adopted: the analysis records the full per-fold `resolved_params.json` key difference of H021 against H022, for all 8 folds.
