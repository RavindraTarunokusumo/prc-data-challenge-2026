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
import yaml

from prc.data import load_silver
from prc.evaluate import evaluate
from prc.features import FEATURE_SETS
from prc.models import REGISTRY
from prc.paths import EXPERIMENTS, PREDICTIONS_VAL, ROOT, git_commit, sha256_file
from prc.splits import development_folds, get_fold, masked_view


def main(eid: str) -> None:
    exp = EXPERIMENTS / eid
    cfg = yaml.safe_load((exp / "config.yaml").read_text())
    folds = [get_fold(f) for f in cfg["folds"]]
    final = any(f.kind == "final" for f in folds)
    silver = load_silver(unmask_holdout_for=eid if final else None)
    out_dir = PREDICTIONS_VAL / eid
    out_dir.mkdir(parents=True, exist_ok=True)
    scores, timing, files = {}, {}, []
    for fold in folds:
        t0 = time.time()
        feats = FEATURE_SETS[cfg["feature_set"]](masked_view(silver, fold))
        pred = REGISTRY[cfg["model"]](feats, cfg.get("params", {}), cfg.get("seed", 42))
        path = out_dir / f"{fold.fold_id}.parquet"
        pred.select("MVT_ID_mvt", "pred").sort("MVT_ID_mvt").write_parquet(path)
        files.append({"path": str(path.relative_to(ROOT)), "fold": fold.fold_id,
                      "rows": pred.height, "size": path.stat().st_size,
                      "sha256": sha256_file(path)})
        # Holdout and final folds are predicted only: holdout truth is read solely by
        # evaluate.holdout_compare, and final folds have no truth.
        if fold.kind not in ("holdout", "final"):
            scores[fold.fold_id], _ = evaluate(pred, fold.fold_id)
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
    (exp / "manifest.json").write_text(json.dumps({
        "schema": "artifact-manifest-v1",
        "producing_experiment": eid,
        "artifacts": files,
        "format": "parquet [MVT_ID_mvt, pred]",
        "code_commit": git_commit(),
        "silver_sha256": json.loads((ROOT / "data/manifests/silver_manifest.json")
                                    .read_text())["sha256"],
        "reproduce": f"uv run python scripts/run_experiment.py {eid}  (a reproduction needs a "
                     "fresh E### from scripts/gate.py)",
    }, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
