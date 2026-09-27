"""Day 1 resource calibration (brief §4). Measures wall time and peak RSS of the pipeline
stages on real fold data. Computes NO metric: predictions are never scored, so this is
infrastructure, not an experiment.

    uv run python scripts/calibrate_resources.py
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
os.environ.setdefault("POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR", "load_as_storage")

import polars as pl
import psutil

from prc.data import load_silver
from prc.features import fs0
from prc.models import gbm, linear
from prc.paths import ROOT
from prc.splits import get_fold, masked_view

OUT = ROOT / "research" / "day-01" / "calibration" / "calibration.json"
PROC = psutil.Process()


class Peak:
    def __enter__(self):
        self.peak, self.stop = PROC.memory_info().rss, False
        self.t = threading.Thread(target=self._run, daemon=True)
        self.t0 = time.time()
        self.t.start()
        return self

    def _run(self):
        while not self.stop:
            self.peak = max(self.peak, PROC.memory_info().rss)
            time.sleep(0.1)

    def __exit__(self, *exc):
        self.stop = True
        self.t.join()
        self.seconds = round(time.time() - self.t0, 2)
        self.peak_gb = round(self.peak / 1024**3, 3)


def main() -> None:
    res = {"cpu_count": psutil.cpu_count(), "ram_total_gb":
           round(psutil.virtual_memory().total / 1024**3, 2)}
    with Peak() as p:
        silver = load_silver()
    res["load_silver"] = {"s": p.seconds, "peak_gb": p.peak_gb, "rows": silver.height}
    for fid in ("R1", "S1"):
        with Peak() as p:
            feats = fs0(masked_view(silver, get_fold(fid)))
        res[f"fs0_{fid}"] = {"s": p.seconds, "peak_gb": p.peak_gb, "rows": feats.height,
                             "train_rows": feats.filter(pl.col("role") == "train").height}
    feats = fs0(masked_view(silver, get_fold("S1")))  # largest training set
    with Peak() as p:
        linear.ridge(feats, {"alpha": 1.0}, 42)
    res["ridge_S1"] = {"s": p.seconds, "peak_gb": p.peak_gb}
    lgb_p = {"objective": "regression", "learning_rate": 0.05, "num_leaves": 255,
             "min_data_in_leaf": 100, "feature_fraction": 0.9, "bagging_fraction": 0.8,
             "bagging_freq": 1, "num_threads": 4}
    for rounds in (50, 200):
        with Peak() as p:
            gbm.lightgbm(feats, {**lgb_p, "num_boost_round": rounds}, 42)
        res[f"lightgbm_S1_{rounds}r"] = {"s": p.seconds, "peak_gb": p.peak_gb}
    xgb_p = {"objective": "reg:squarederror", "eta": 0.05, "max_depth": 10,
             "min_child_weight": 10, "subsample": 0.8, "colsample_bytree": 0.9, "nthread": 4,
             "max_cat_to_onehot": 1}
    for rounds in (50, 200):
        with Peak() as p:
            gbm.xgboost(feats, {**xgb_p, "num_boost_round": rounds}, 42)
        res[f"xgboost_S1_{rounds}r"] = {"s": p.seconds, "peak_gb": p.peak_gb}
    for m in ("lightgbm", "xgboost"):
        a, b = res[f"{m}_S1_50r"]["s"], res[f"{m}_S1_200r"]["s"]
        res[f"{m}_s_per_round"] = round((b - a) / 150, 4)
        res[f"{m}_fixed_s"] = round(a - 50 * (b - a) / 150, 2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
