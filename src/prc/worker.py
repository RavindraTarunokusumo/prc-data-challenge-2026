"""Experiment worker, run as a child of scripts/run_experiment.py:

    python -m prc.worker E###

Model code sees only the fold's masked view (via a feature-set function); evaluation
truth is read by prc.evaluate after predictions exist.
"""

from __future__ import annotations

import json
import sys
import time

import numpy as np
import polars as pl
import yaml

from prc import blending, curves
from prc.data import load_silver
from prc.evaluate import evaluate, truth_frame
from prc.features import FEATURE_SETS
from prc.models import REGISTRY
from prc.paths import EXPERIMENTS, PREDICTIONS_VAL, ROOT, git_commit, sha256_file
from prc.splits import development_folds, get_fold, masked_view


def environment() -> dict:
    """The run's environment record (LAPTOP_REFS v2, condition (a)): lock hash, library
    versions and the launching shell's thread variables."""
    import importlib
    import os

    libs = {}
    for mod in ("numpy", "scipy", "sklearn", "polars", "lightgbm", "catboost", "xgboost",
                "pandas"):
        try:
            libs[mod] = importlib.import_module(mod).__version__
        except ImportError:
            libs[mod] = None
    lock = ROOT / "uv.lock"
    return {"uv_lock_sha256": sha256_file(lock) if lock.exists() else None, "libraries": libs,
            "thread_variables": {k: v for k, v in os.environ.items()
                                 if k.endswith("_THREADS")}}


def learning_curve(curve: dict, fold, score: dict | None) -> dict:
    """Train RMSE per iteration, and for scored folds the RMSE of each staged prediction
    against truth. The last stage must equal the evaluator's RMSE (consistency check)."""
    out = {"learner": curve["learner"], "iterations": curve["iterations"],
           "train_rmse": curve["train_rmse"]}
    if fold.kind in ("holdout", "final") or score is None:
        return out  # predicted only: no truth is read for a curve
    truth = truth_frame(fold.fold_id)
    pos = pl.DataFrame({"MVT_ID_mvt": curve["ids"].astype(np.int64)}).with_row_index("i")
    j = truth.select(pl.col("MVT_ID_mvt").cast(pl.Int64), "TAXITIME_SEC_mvt").join(
        pos, on="MVT_ID_mvt", how="inner")
    err = curve["staged"][j["i"].to_numpy()] - j["TAXITIME_SEC_mvt"].to_numpy()[:, None]
    eval_rmse = np.sqrt(np.mean(err**2, axis=0))
    out["eval_rmse"] = [float(v) for v in eval_rmse]
    out["eval_rows"] = j.height
    out["last_minus_evaluator"] = float(eval_rmse[-1] - score["rmse"])
    return out


def main(eid: str) -> None:
    exp = EXPERIMENTS / eid
    commit = git_commit()  # at start: the code the run used (D5-C6)
    cfg = yaml.safe_load((exp / "config.yaml").read_text())
    folds = [get_fold(f) for f in cfg["folds"]]
    final = any(f.kind == "final" for f in folds)
    silver = load_silver(unmask_holdout_for=eid if final else None)
    out_dir = PREDICTIONS_VAL / eid
    out_dir.mkdir(parents=True, exist_ok=True)
    scores, timing, files, curve_out, resolved = {}, {}, [], {}, {}
    for fold in folds:
        t0 = time.time()
        feats = FEATURE_SETS[cfg["feature_set"]](masked_view(silver, fold))
        curves.start()
        if cfg["model"] == "blend":  # stored component predictions (prc.blending)
            val_ids = feats.filter(pl.col("role") == "val")["MVT_ID_mvt"]
            pred = blending.blend(val_ids, cfg["params"], fold.fold_id)
        else:
            pred = REGISTRY[cfg["model"]](feats, cfg.get("params", {}), cfg.get("seed", 42))
        curve = curves.take()
        if curve and curve.get("resolved_params"):
            resolved[fold.fold_id] = curve["resolved_params"]
        path = out_dir / f"{fold.fold_id}.parquet"
        pred.select("MVT_ID_mvt", "pred").sort("MVT_ID_mvt").write_parquet(path)
        files.append({"path": str(path.relative_to(ROOT)), "fold": fold.fold_id,
                      "rows": pred.height, "size": path.stat().st_size,
                      "sha256": sha256_file(path)})
        # Holdout and final folds are predicted only: holdout truth is read solely by
        # evaluate.holdout_compare, and final folds have no truth.
        if fold.kind not in ("holdout", "final"):
            scores[fold.fold_id], _ = evaluate(pred, fold.fold_id)
        if curve is not None:
            curve_out[fold.fold_id] = learning_curve(curve, fold, scores.get(fold.fold_id))
        timing[fold.fold_id] = round(time.time() - t0, 2)
        msg = f"rmse={scores[fold.fold_id]['rmse']:.2f}" if fold.fold_id in scores else "saved"
        print(f"{eid} {fold.fold_id}: {msg} ({timing[fold.fold_id]}s)", flush=True)

    dev = [f for f in development_folds() if f in scores]
    metrics = {
        "experiment_id": eid,
        "rmse_by_fold": {f: s["rmse"] for f, s in scores.items()},
        "mean_rmse_dev": float(np.mean([scores[f]["rmse"] for f in dev]))
        if len(dev) == len(development_folds()) else None,
        "fold_seconds": timing,
        "scores": scores,
    }
    (exp / "metrics.json").write_text(json.dumps(metrics, indent=1) + "\n")
    if curve_out:
        (exp / "curves.json").write_text(json.dumps({
            "schema": "learning-curves-v1", "experiment_id": eid, "step": curves.STEP,
            "note": "train_rmse: the learner's own training loss per iteration; eval_rmse: "
                    "staged predictions of the finished model scored after training "
                    "(development and diagnostic folds only; never the holdout)",
            "folds": curve_out}) + "\n")
    if resolved:  # the learner's own resolved parameters (e.g. CatBoost get_all_params)
        (exp / "resolved_params.json").write_text(json.dumps(resolved, indent=1,
                                                             default=str) + "\n")
    (exp / "manifest.json").write_text(json.dumps({
        "schema": "artifact-manifest-v1",
        "producing_experiment": eid,
        "artifacts": files,
        "format": "parquet [MVT_ID_mvt, pred]",
        "code_commit": commit,
        # polars' thread pool sets the summation order of the fitted ridge statistics, and
        # so the routed rows' bits (research/day-05/eda/ridge_paths*.json)
        "polars_threads": pl.thread_pool_size(),
        "python": sys.version.split()[0],
        "environment": environment(),  # rule L v2 condition (a)
        "silver_sha256": json.loads((ROOT / "data/manifests/silver_manifest.json")
                                    .read_text())["sha256"],
        "reproduce": f"uv run python scripts/run_experiment.py {eid}  (a reproduction needs a "
                     "fresh E### from scripts/gate.py)",
    }, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
