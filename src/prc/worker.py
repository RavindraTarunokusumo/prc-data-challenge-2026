"""Experiment worker, run as a child of scripts/run_experiment.py:

    python -m prc.worker E###

Model code sees only the fold's masked view (via a feature-set function); evaluation
truth is read by prc.evaluate after predictions exist.
"""

from __future__ import annotations

import json
import sys
import time

import yaml

from prc.data import load_silver
from prc.evaluate import evaluate, pooled_airport_rmse, summary
from prc.features import FEATURE_SETS
from prc.models import REGISTRY
from prc.paths import EXPERIMENTS, PREDICTIONS_VAL, ROOT, git_commit, sha256_file
from prc.splits import DEVELOPMENT, get_fold, masked_view


def main(eid: str) -> None:
    exp = EXPERIMENTS / eid
    cfg = yaml.safe_load((exp / "config.yaml").read_text())
    silver = load_silver()
    out_dir = PREDICTIONS_VAL / eid
    out_dir.mkdir(parents=True, exist_ok=True)
    scores, joined, timing, files = {}, {}, {}, []
    for fold_id in cfg["folds"]:
        t0 = time.time()
        fold = get_fold(fold_id)
        feats = FEATURE_SETS[cfg["feature_set"]](masked_view(silver, fold))
        pred = REGISTRY[cfg["model"]](feats, cfg.get("params", {}), cfg.get("seed", 42))
        holdout = None
        if fold.kind == "holdout":
            holdout = {**cfg["holdout_access"], "experiment_id": eid}
        scores[fold_id], joined[fold_id] = evaluate(pred, fold_id, silver, holdout=holdout)
        path = out_dir / f"{fold_id}.parquet"
        joined[fold_id].select("MVT_ID_mvt", "pred").write_parquet(path)
        files.append({"path": str(path.relative_to(ROOT)), "fold": fold_id,
                      "rows": joined[fold_id].height, "size": path.stat().st_size,
                      "sha256": sha256_file(path)})
        timing[fold_id] = round(time.time() - t0, 2)
        print(f"{eid} {fold_id}: rmse={scores[fold_id]['rmse']:.2f} ({timing[fold_id]}s)",
              flush=True)

    dev = tuple(f for f in DEVELOPMENT if f in joined)
    metrics = {
        "experiment_id": eid,
        **summary(scores),
        "pooled_airport_rmse_dev": pooled_airport_rmse(joined, dev) if len(dev) == 4 else None,
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
        "reproduce": f"uv run python scripts/run_experiment.py {eid}  (fresh E### via gate for "
                     "a reproduction run)",
    }, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
