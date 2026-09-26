# Data Policy

1. **Secrets.** The repository is public. Credentials (`PRC_S3_ACCESS_KEY`, `PRC_S3_SECRET_KEY`, `OPENSKY_PASSWORD`, and any token) never appear in tracked files, commit messages, logs, prompt mirrors or reports. They come from environment variables or the git-ignored `.env`. Scripts must never print them.
2. **Raw data is read-only.** `data/raw/` is written once by `scripts/fetch_data.py` and verified against `data/manifests/raw_manifest.json`.
3. **Manifests.** Every git-ignored artifact that supports a scientific claim has a tracked manifest: relative path, producing experiment, size, SHA-256, format, creation time, code commit and reproduction command.
4. **Prediction-time availability.** A feature is admissible only if it would be known at the prediction timestamp in the Jan/Jul 2026 test sets. The Day 1 audit defines that timestamp per row type. Every feature proposal cites that audit.
5. **Target statistics** are computed strictly inside the training part of each fold.
6. **Protected holdout.** Access is logged in `orchestration/task-ledger.jsonl` and is limited to once per phase.
7. **External data.** Only if pre-registered, available at prediction time for the test periods, and permitted by competition rules. OpenSky data falls under the same rule.

## Data layers (bronze → silver → gold)

A lightweight layering contract, not a framework. Its purpose is leakage control.

| Layer | Path | Contents | Rule |
|---|---|---|---|
| Bronze | `data/raw/` | Competition files exactly as downloaded | Immutable. Verified against `data/manifests/raw_manifest.json` before use |
| Silver | `data/processed/` | One canonical table: typed columns, IDs cast from Float64 to integer, parsed timestamps, schema fixes | Deterministic, built once by `scripts/build_silver.py`, shared by all folds, with its own manifest |
| Gold | `data/cache/features_<hash>.parquet` | Feature tables per feature set **and per fold** | `<hash>` covers feature code, config and fold ID. Target-derived values come only from that fold's training rows |

8. **Silver is scientifically neutral.** It may not use the target, fold membership or any row-dropping/capping rule that changes the evaluation population. Filtering or capping outliers, excluding rows and imputing values are modelling decisions: they belong in gold, behind an Advisor-reviewed hypothesis.
9. **Gold is fold-local.** Target statistics, historical priors and any fitted transform (encoders, scalers) are fitted on the fold's training rows and applied to its validation rows. A single global feature table containing target-derived values is a leakage violation.
10. **Evaluation population is fixed.** Validation metrics are always computed on all rows of the frozen fold, whatever filtering a model uses in training, so experiments stay comparable.
