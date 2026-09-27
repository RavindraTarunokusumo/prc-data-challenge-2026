"""Evaluator: the only code path that reads validation truth.

Model code produces a frame [MVT_ID_mvt, pred] for a fold; `evaluate` checks coverage
and scores it with the frozen metric. Protected-holdout scoring is refused unless
explicitly requested, and each access is logged to orchestration/task-ledger.jsonl
(max one per phase, DATA_POLICY §6).
"""

from __future__ import annotations

import datetime as dt
import json

import numpy as np
import polars as pl

from prc import metrics
from prc.paths import ROOT
from prc.splits import DEVELOPMENT, eval_rows, get_fold

TASK_LEDGER = ROOT / "orchestration" / "task-ledger.jsonl"
META = ["MVT_ID_mvt", "TAXITIME_SEC_mvt", "ADEP_mvt", "month", "WK_TBL_CAT_flt",
        "MVT_TIME_UTC_mvt"]


def holdout_accesses(phase: str) -> int:
    if not TASK_LEDGER.exists():
        return 0
    n = 0
    for line in TASK_LEDGER.read_text().splitlines():
        if line.strip():
            rec = json.loads(line)
            if rec.get("event") == "holdout_access" and rec.get("phase") == phase:
                n += 1
    return n


def log_holdout_access(phase: str, experiment_id: str, reason: str) -> None:
    rec = {
        "event": "holdout_access",
        "phase": phase,
        "experiment_id": experiment_id,
        "reason": reason,
        "utc": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(TASK_LEDGER, "a") as f:
        f.write(json.dumps(rec) + "\n")


def truth_frame(silver: pl.DataFrame, fold_id: str) -> pl.DataFrame:
    return eval_rows(silver, get_fold(fold_id)).select(META).collect()


def evaluate(pred: pl.DataFrame, fold_id: str, silver: pl.DataFrame, *,
             holdout: dict | None = None) -> tuple[dict, pl.DataFrame]:
    """Score predictions for one fold. Returns (score dict, joined frame)."""
    fold = get_fold(fold_id)
    if fold.kind == "final":
        raise ValueError("the final fold has no truth")
    if fold.kind == "holdout":
        if not holdout or not {"phase", "experiment_id", "reason"} <= holdout.keys():
            raise PermissionError("protected holdout: pass holdout={phase, experiment_id, reason}")
        if holdout_accesses(holdout["phase"]) >= 1:
            raise PermissionError(f"protected holdout already accessed in {holdout['phase']}")
        log_holdout_access(holdout["phase"], holdout["experiment_id"], holdout["reason"])
    truth = truth_frame(silver, fold_id)
    pred = pred.select(pl.col("MVT_ID_mvt").cast(pl.Int64), pl.col("pred").cast(pl.Float64))
    metrics.validate_predictions(pred, truth)
    joined = truth.join(pred, on="MVT_ID_mvt", how="inner").sort("MVT_ID_mvt")
    return metrics.score(joined), joined


def pooled_airport_rmse(joined_frames: dict[str, pl.DataFrame],
                        folds: tuple[str, ...] = DEVELOPMENT) -> dict[str, float]:
    """Per-airport RMSE pooled over the development folds' evaluation rows."""
    df = pl.concat([joined_frames[f] for f in folds])
    out = {}
    for (airport,), g in df.group_by("ADEP_mvt"):
        out[airport] = metrics.rmse(g["TAXITIME_SEC_mvt"].to_numpy(), g["pred"].to_numpy())
    return dict(sorted(out.items()))


def summary(scores: dict[str, dict]) -> dict:
    dev = [f for f in DEVELOPMENT if f in scores]
    return {
        "rmse_by_fold": {f: scores[f]["rmse"] for f in scores},
        "mean_rmse_dev": float(np.mean([scores[f]["rmse"] for f in dev])) if dev else None,
    }
