"""Day 4 CatBoost resource calibration. Fold R3 (largest training set), FS2 features, the
training target replaced by a random permutation of itself (rng seed 0) and LIRF NM-missing
training rows dropped (as `route_train_exclude`). Computes NO metric: predictions are timed,
never scored; the permuted target carries no signal.

    uv run python scripts/calibrate_catboost.py
Each configuration runs in a fresh subprocess so peak RSS (ru_maxrss) is per configuration.
"""

from __future__ import annotations

import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR", "load_as_storage")

OUT = ROOT / "research" / "day-04" / "eda" / "catboost_calibration.json"
CB = {"loss_function": "RMSE", "learning_rate": 0.08, "border_count": 254, "thread_count": 4}
LGB = {"objective": "regression", "learning_rate": 0.05, "num_leaves": 255,
       "min_data_in_leaf": 100, "feature_fraction": 1.0, "bagging_fraction": 1.0,
       "bagging_freq": 0, "bin_construct_sample_cnt": 5_000_000, "num_threads": 4}
CONFIGS = [("catboost", 6, 100), ("catboost", 8, 100), ("catboost", 6, 300),
           ("catboost", 8, 300), ("lightgbm", None, 100)]
# Training DEP rows per fold (from the month counts in the pipeline digest).
M = {"01": 153706, "02": 143732, "03": 164449, "04": 175288, "05": 185202, "06": 183142,
     "07": 190713, "08": 191182, "09": 183950, "10": 185674, "11": 162332}
TRAIN = {"R1": sum(M[k] for k in ["01", "02", "03", "04", "05", "06", "07", "08"]),
         "R2": sum(M[k] for k in ["01", "02", "03", "04", "05", "06", "07", "08", "09"]),
         "R3": sum(M[k] for k in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]),
         "S1": sum(M[k] for k in ["01", "02", "03", "04", "05", "06", "09", "10", "11"]),
         "W1": sum(M[k] for k in ["01", "04", "05", "06", "07", "09", "10", "11"]) + M["08"],
         "S1c": sum(M[k] for k in ["01", "02", "03", "04", "05", "06"]),
         "W1c": M["01"],
         "H": sum(M.values())}
VAL = {"R1": M["09"], "R2": M["10"], "R3": M["11"], "S1": M["07"], "W1": M["02"],
       "S1c": M["07"], "W1c": M["02"], "H": 165677}


def build_frame():
    import numpy as np
    import polars as pl

    from prc.data import load_silver
    from prc.features import FEATURE_SETS
    from prc.models.routed import route_mask
    from prc.splits import get_fold, masked_view

    feats = FEATURE_SETS["FS2"](masked_view(load_silver(), get_fold("R3")))
    tr_mask = (feats["role"] == "train").to_numpy()
    y = feats["y"].to_numpy().astype("float64")
    perm = np.random.default_rng(0).permutation(y[tr_mask])
    y[tr_mask] = perm
    feats = feats.with_columns(pl.Series("y", y, dtype=pl.Float64).fill_nan(None))
    feats = feats.filter(~((pl.col("role") == "train") & route_mask()))
    return feats


def child(model: str, depth: int | None, iters: int) -> dict:
    import polars as pl

    from prc.features import columns
    from prc.models import gbm

    feats = build_frame()
    rss_frame = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**2
    tr = feats.filter(pl.col("role") == "train")
    cats, nums = columns(feats)
    out = {"model": model, "depth": depth, "iterations": iters,
           "train_rows": tr.height, "val_rows": feats.height - tr.height,
           "n_cat": len(cats), "n_num": len(nums),
           "cat_cardinality": {c: tr[c].n_unique() for c in cats},
           "peak_rss_gb_after_frame": round(rss_frame, 3),
           "uptime_before": Path("/proc/loadavg").read_text().split()[:3]}
    if model == "catboost":
        p = {**CB, "depth": depth, "iterations": iters}
        fit_fn = gbm.catboost
    else:
        p = {**LGB, "num_boost_round": iters}
        fit_fn = gbm.lightgbm
    # total (encode + fit + predict) via the registry function; fit vs predict split below
    t0 = time.time()
    fit_fn(feats, p, 42)
    out["total_s"] = round(time.time() - t0, 1)
    out["peak_rss_gb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**2, 3)
    if model == "catboost":  # separate fit / predict timing (second, identical fit)
        from catboost import CatBoostRegressor, Pool
        tr_, _va, x_tr, x_va, cats_ = gbm._frames(feats)
        def prep(x):
            x = x.copy()
            for c in cats_:
                x[c] = x[c].astype(object).where(x[c].notna(), gbm.NULL_CAT).astype(str)
            return x
        ptr = Pool(prep(x_tr), label=tr_["y"].to_numpy(), cat_features=cats_)
        pva = Pool(prep(x_va), cat_features=cats_)
        m = CatBoostRegressor(**p, random_seed=42, allow_writing_files=False, verbose=False)
        t0 = time.time(); m.fit(ptr); out["fit_s"] = round(time.time() - t0, 1)
        t0 = time.time(); m.predict(pva); out["predict_s"] = round(time.time() - t0, 2)
        out["peak_rss_gb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**2, 3)
    return out


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--child":
        d = None if sys.argv[3] == "None" else int(sys.argv[3])
        print("RESULT " + json.dumps(child(sys.argv[2], d, int(sys.argv[4]))))
        return
    runs = []
    for model, depth, iters in CONFIGS:
        r = subprocess.run([sys.executable, __file__, "--child", model, str(depth), str(iters)],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [ln for ln in r.stdout.splitlines() if ln.startswith("RESULT ")]
        if not line:
            print(r.stderr[-2000:]); raise SystemExit("child failed")
        res = json.loads(line[0][7:]); runs.append(res); print(res, flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    result = {"note": "permuted-target timing only; no metric computed", "fold": "R3",
              "feature_set": "FS2", "runs": runs, "train_rows_by_fold": TRAIN,
              "val_rows_by_fold": VAL}
    OUT.write_text(json.dumps(result, indent=1) + "\n")


if __name__ == "__main__":
    main()
