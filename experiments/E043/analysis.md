# E043 analysis: H032 v1 (SUBMIT fit of E031's configuration: routed CatBoost GPU, FS2_RAW, CTRs at complexity 4)

**Outcome: COMPLETE; route check PASS; resolved parameters identical to E031 (S5).** The CatBoost half of the submission, and **one GPU draw** of E031's configuration trained on 12 months. No truth: nothing is scored, no ledger decision (role in `notes`). Batch reading: `experiments/E044/analysis.md`.

| Item | Value |
|---|---|
| Config | `routed_catboost`, FS2_RAW, E031's params (parsed-YAML identical), folds `[SUBMIT_JAN, SUBMIT_JUL]`, seed 42, CLASS-L |
| Status | COMPLETE: 419.3 s, peak RSS 7.69 GB, within class; run commit `552f49d`; swap-out 0 pages |
| GPU | device-wide 906 MiB at start, peak 3,784 MiB (of 8,151 MiB); the external holder of the session start (2.9 GB) was gone by 19:00Z (704 MiB at window open) |
| Fold time | SUBMIT_JAN 214.5 s; SUBMIT_JUL 197.1 s |
| Prediction SHA-256 | JAN `9076ebab13ca…`, JUL `092673a89519…` |
| Mean prediction | JAN 1,062.9 s; JUL 1,001.2 s |
| Predictions > 3,600 s | JAN 340; JUL 131 |

- **Integrity:** `route_check.py E043 - E042` **PASS**: on the routed rows (107 JAN, 276 JUL) max |E043 − E042| = 0.0 s (`research/comparisons/route_check_E043.json`).
- **S5 (resolved parameters):** E043's `resolved_params.json` equals E031's key by key on both final folds (compared against E031's R1 and H entries; E031's folds are mutually identical). `data_partition` is `FeatureParallel` in both. **No difference; no flag.**
- **Window:** started 19:06:38Z, finished 19:13:38Z; W&B mirror failed (CommError) until 19:15:17Z. **E043 is not mirrored to W&B** (INC-0009).
- **Tree (S3):** `git_dirty_at_run: true` (task-ledger append from the final-fold unmasking only; S3). The post-checkpoint WARNING lists only `orchestration/task-ledger.jsonl`.
- **S4:** one unmasking event for E043, at 19:06:44Z, inside the run span.
- **Freeze and environment:** as E042 (freeze diff empty; python 3.13.15; polars 16).
- **Rule 13:** E043 is one draw. Rule 13's quantities need truth and a twin and cannot be computed on final folds. The halves' disagreement RMS(E042 − E043) is 110.0 s (JAN) and 100.9 s (JUL); that is model disagreement, not a draw change.
