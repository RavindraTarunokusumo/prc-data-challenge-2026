# SESSION_START — D01-S01

- **Start (UTC):** 2026-09-27T10:54:05Z
- **Phase:** Day 1 — infrastructure, dataset audit, frozen splits, evaluator, baselines
- **Resolved researcher model:** `claude-opus-5-5` (session metadata: `session_context.model` = `claude-opus-5-5`, `external_metadata.last_served_model` = `claude-opus-5-5`), effort `high`
- **Advisor:** `advisor` subagent, alias `opus`, effort `max`; resolved ID recorded per exchange
- **Git commit:** `b83acd519e46aeff03f2d8cda9e04f846faba268` (`origin/main`, merge of PR #1 preamble); working branch `claude/quirky-dirac-c0gnnp`
- **Dirty state at start:** clean working tree (git-ignored `.env` and `data/raw/` present, as expected)

## Recovered state
Rebuilt from `research/STATE.md`, `research/PROJECT_LOG.md`, empty ledgers and the preamble commits only.

- Phase before this session: PREAMBLE complete. INC-0001 accepted (Claude substitution); INC-0002 closed (network).
- Raw data: 14 files in `data/raw/prc-2026-datasets/`, **re-verified this session** against `data/manifests/raw_manifest.json` (14/14 SHA-256 match).
- Environment: `uv sync` clean. Python 3.11.15; polars 1.44.2, lightgbm 4.7.0, xgboost 3.2.0, catboost 1.2.10, scikit-learn 1.9.1. 4 vCPU, 15 GB RAM, no swap, ~28 GB free disk.
- Network allowlist read (`config/network.yaml`).

## Research state
- **Champion:** none
- **Accepted findings:** none
- **Rejected hypotheses:** none
- **Remaining budget:** promotional cloud credit in use (rate-limit status `allowed`); no experiment compute spent yet
- **Last exchange ID:** none (task ledger and advisor-exchanges empty)

## Open questions
1. Which ranking-file columns are legitimately known at the prediction timestamp (availability audit)?
2. What is the prediction timestamp for a DEP row (off-block? scheduled time?)
3. Fold design given only Jan–Dec 2025 training data and Jan/Jul 2026 test months.

## First planned action
Dataset audit and prediction-time availability audit (`docs/methodology/DATASET_AUDIT.md`), then the silver layer, splits proposal and split-freeze review.
