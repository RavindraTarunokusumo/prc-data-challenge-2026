# E042 analysis: H031 v1 (SUBMIT fit of E029's configuration: routed LightGBM, FS2)

**Outcome: COMPLETE; integrity holds.** The LightGBM half of the submission. No truth exists for the final folds: nothing is scored, nothing is compared with any fold, no ledger decision (role in `notes`). Batch reading: `experiments/E044/analysis.md`.

| Item | Value |
|---|---|
| Config | `routed_lightgbm`, FS2, E029's params (parsed-YAML identical), folds `[SUBMIT_JAN, SUBMIT_JUL]`, seed 42, CLASS-M |
| Status | COMPLETE: 279.7 s, peak RSS 7.02 GB, within class; run commit `eac0254`; swap-out 0 pages |
| Fold time | SUBMIT_JAN 136.9 s; SUBMIT_JUL 135.0 s |
| Rows | 152,719 (JAN), 192,122 (JUL); routed rows 107 and 276 |
| Prediction SHA-256 | JAN `0f420892199f…`, JUL `aae3e395f9bd…` (manifest) |
| Mean prediction | JAN 1,062.7 s; JUL 1,002.8 s |
| Predictions > 3,600 s | JAN 358; JUL 138 |

- **Window (INC-0014):** started 19:00:05Z by the pinned launcher; the run finished 19:04:46Z. The launcher's END line is 19:06:35Z because the W&B mirror attempt ran until then and failed (CommError; records unaffected). **E042 is not mirrored to W&B** (INC-0009).
- **Tree:** `git_dirty_at_run: false`. After its checkpoint the launcher logged `WARNING: tree not clean … M orchestration/task-ledger.jsonl` only (S3, pre-registered; not a deviation).
- **S4:** one `holdout_targets_unmasked_for_final_training` event for E042, at 19:00:12Z, inside the run span.
- **Freeze:** `git diff --stat eedcd47 c59212a -- src scripts config pyproject.toml uv.lock research/day-07/sessions/D07-S01/run_window.sh` is empty.
- **Environment (rule L v2 item 6):** manifest `python` 3.13.15, `polars_threads` 16; libraries and `uv.lock` as the pre-arming record.
- **Route reference:** none of its own (first routed SUBMIT instance); cross-checked by `route_check.py E043 - E042` (PASS, max |diff| 0.0 s on both folds).
- **Mean predictions above the proposal's range:** the proposal's analogues (H, W1, S1) do not predict January 2026's level; see `experiments/E044/analysis.md` §Disclosures.
