---
schema: incident-v1
incident_id: INC-0009
type: protocol_deviation
created_utc: 2026-10-01T17:35:00Z
status: open
---

# Day 5: owner instruction to mirror experiments to Weights & Biases

**Raised by:** the researcher, recording an owner instruction in D05-S04. Changing `config/network.yaml` needs an owner decision logged here. This is that record.

## Instruction (owner, D05-S04, verbatim)

> Please connect it to my Weights and Bias project PRC-Data-Challenge-2026
> WANDB_API_KEY already in .env

## What was done

- **Network allowlist:** `api.wandb.ai` (API) and `storage.googleapis.com` (W&B's signed-URL file uploads), under a new `tracking` category scoped to this use.
- **Code:** `src/prc/tracking.py`, `scripts/wandb_sync.py`, and a hook in `scripts/run_experiment.py` after the ledger update. Dependency `wandb==0.30.0`; `uv.lock` SHA-256 is now `efa4fd78…` (was `39df945c…`).
- **What a W&B run carries:** one run per experiment (run id = E###), built from committed files only:
  - gate metadata, config and ledger decision, with tags for day, purpose, status, decision and champion lineage;
  - development and diagnostic fold RMSEs (`metrics.json`), and segment tables (airport, traffic, wake, taxi band);
  - resource usage.
- **What it never carries:** predictions, targets, data rows, holdout comparisons or credentials. Console capture, code saving, system stats and host metadata are off.
- **Source of truth:** the repository. The mirror is best-effort: a failure is printed and never changes a record.

## Integrity notes

- **No leaderboard or contamination change.** W&B holds this project's own records only, with no competition leaderboard data.
- **Holdout:** no holdout figure is mirrored, so W&B cannot become a second view of H.
- **Reading the dashboard:** a lower `mean_rmse_dev` is not a better candidate. E020 (321.95) and E012 (376.15) are not champions, because their margin comes from the LIRF recording-convention rows. Promotion follows brief §10 and the rulings in `research/STATE.md`; the `decision:` and `champion-lineage` tags carry that.
- **Secrets:** `WANDB_API_KEY` is read from the environment or `.env`. It is added to the redaction list (`scripts/fetch_data.py` `SECRET_VARS`) and to `.env.example` as a name only. Local run files go to the git-ignored `runtime/wandb/`.

## Resolution

Stays open while the mirror is in use, and is reviewed at the Day 5 phase close.

## Addendum (2026-10-01T17:58Z): learning curves (owner request)

> I want the remaining model training, particularly the final champions, to show a clear learning curve of RMSE against steps of the training and eval phase.

- `src/prc/curves.py` and the worker now record, for LightGBM, XGBoost and CatBoost:
  - **training RMSE per iteration:** the learner's own training loss on its training rows;
  - **validation RMSE every 10 iterations:** staged predictions of the *finished* model, scored after training through `prc.evaluate.truth_frame`.

  The results go to `experiments/E###/curves.json` and the W&B history (x-axis `iteration`).
- **Integrity:**
  - nothing feeds back into training (no validation set inside the learner, no early stopping, no parameter change);
  - predictions are bit-identical with recording on or off (`tests/test_models.py`), and the last stage must equal the evaluator's RMSE;
  - **the holdout gets no validation curve** (`truth_frame` refuses H as well).
- **Selection hazard, stated:** a validation curve invites picking `num_boost_round` at its minimum. That would be validation-guided tuning, and any proposal using it must say so and pre-register it.
- Experiments before E027 have no curves: their per-iteration values were never recorded.

## Amendment (Day 6 phase close, X-D06-S01-0004; D6-C13)

- E036, E037, E038 and E039 failed to initialise their W&B runs at completion on 2026-10-02 ("runupserter: failed to init run", context deadline exceeded). E035 synced at completion; E040 and E041 synced on 2026-10-03. Two post-window re-syncs (E035–E039) failed. The W&B mirror therefore lacks E036–E039; the repository records are complete. Stays open.

## Amendment (Day 7, D07-S01)

- E042 and E043 (the SUBMIT fits) failed to sync at completion on 2026-10-03 (CommError; each attempt took about 2 min after the run). E044 synced. The W&B mirror therefore lacks E042 and E043; the repository records are complete. Stays open.
