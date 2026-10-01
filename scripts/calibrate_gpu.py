"""Day 5 laptop resource calibration: GPU XGBoost and CatBoost against CPU LightGBM.

Same frame as scripts/calibrate_catboost.py (fold R3, the training target replaced by a
random permutation of itself (rng seed 0), LIRF NM-missing training rows dropped), with the
feature set FS2 or FS2_RAW. Computes NO metric: predictions are timed and hashed, never
scored; the permuted target carries no signal.

Per configuration, in a fresh subprocess: encode + fit + predict time, peak RSS, peak GPU
memory of the device (nvidia-smi poll, 0.25 s), the hash of the predictions of two
identical fits (determinism), and for CatBoost the resolved boosting scheme and CTR types
from get_all_params().

    uv run python scripts/calibrate_gpu.py            # all configurations
    uv run python scripts/calibrate_gpu.py NAME ...   # a subset by name
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import resource
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
os.environ.setdefault("POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR", "load_as_storage")

OUT = ROOT / "research" / "day-05" / "eda" / "gpu_calibration.json"
LGB = {"objective": "regression", "learning_rate": 0.05, "num_leaves": 255,
       "min_data_in_leaf": 100, "feature_fraction": 1.0, "bagging_fraction": 1.0,
       "bagging_freq": 0, "bin_construct_sample_cnt": 5_000_000, "num_threads": 4}
# XGBoost shaped like the LightGBM: leaf-wise, 255 leaves, min hessian 100 (= 100 rows for L2)
XGB = {"objective": "reg:squarederror", "eta": 0.05, "grow_policy": "lossguide",
       "max_leaves": 255, "max_depth": 0, "min_child_weight": 100, "max_bin": 256,
       "device": "cuda", "nthread": 4}
CB = {"loss_function": "RMSE", "learning_rate": 0.05, "depth": 8, "border_count": 254,
      "task_type": "GPU", "devices": "0", "thread_count": 4}
# name: (model, feature set, extra params, iterations)
CONFIGS = {
    "lgb_cpu_fs2": ("lightgbm", "FS2", {}, 200),
    "lgb_cpu8_fs2": ("lightgbm", "FS2", {"num_threads": 8}, 200),
    "xgb_gpu_fs2": ("xgboost", "FS2", {}, 500),
    "cb_gpu_fs2": ("catboost", "FS2", {}, 500),
    "cb_gpu_raw": ("catboost", "FS2_RAW", {}, 500),
    "cb_gpu_raw_ordered": ("catboost", "FS2_RAW", {"boosting_type": "Ordered"}, 500),
    "cb_gpu_nocat": ("catboost_nocat", "FS2", {}, 500),
    # target-mean CTRs (GPU-only type) beside the default border share and frequency, and
    # a VRAM cap so the device peak reflects need rather than CatBoost's 95 % pre-allocation
    "cb_gpu_raw_mean": ("catboost", "FS2_RAW", {
        "simple_ctr": ["Borders", "FeatureFreq", "FloatTargetMeanValue"],
        "combinations_ctr": ["Borders", "FeatureFreq", "FloatTargetMeanValue"]}, 500),
    "cb_gpu_raw_cap": ("catboost", "FS2_RAW", {"gpu_ram_part": 0.4}, 500),
}
CB_KEYS = ["boosting_type", "grow_policy", "simple_ctr", "combinations_ctr",
           "max_ctr_complexity", "one_hot_max_size", "bootstrap_type", "subsample",
           "random_strength", "l2_leaf_reg", "border_count", "depth", "task_type",
           "gpu_ram_part"]


def build_frame(fs: str):
    import numpy as np
    import polars as pl

    from prc.data import load_silver
    from prc.features import FEATURE_SETS
    from prc.models.routed import route_mask
    from prc.splits import get_fold, masked_view

    feats = FEATURE_SETS[fs](masked_view(load_silver(), get_fold("R3")))
    tr_mask = (feats["role"] == "train").to_numpy()
    y = feats["y"].to_numpy().astype("float64")
    y[tr_mask] = np.random.default_rng(0).permutation(y[tr_mask])
    feats = feats.with_columns(pl.Series("y", y, dtype=pl.Float64).fill_nan(None))
    return feats.filter(~((pl.col("role") == "train") & route_mask()))


class GpuPoll(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.peak, self.stop = 0, False

    def run(self):
        while not self.stop:
            with contextlib.suppress(Exception):  # a failed poll only loses one sample
                self.peak = max(self.peak, gpu_used_mib())
            time.sleep(0.25)


def gpu_used_mib() -> int:
    out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used",
                          "--format=csv,noheader,nounits"], capture_output=True, text=True,
                         timeout=5, check=False)
    return int(out.stdout.split()[0])


def fit_predict(model: str, feats, params: dict, iters: int):
    """Returns (predictions, resolved CatBoost params or None)."""
    import numpy as np

    from prc.models import gbm

    if model == "lightgbm":
        return gbm.lightgbm(feats, {**LGB, **params, "num_boost_round": iters}, 42)["pred"], None
    if model == "xgboost":
        return gbm.xgboost(feats, {**XGB, **params, "num_boost_round": iters}, 42)["pred"], None
    from catboost import CatBoostRegressor, Pool

    tr, _va, x_tr, x_va, cats = gbm._frames(feats)
    if model == "catboost":
        def prep(x):
            x = x.copy()
            for c in cats:
                x[c] = x[c].astype(object).where(x[c].notna(), gbm.NULL_CAT).astype(str)
            return x
        cat_features = cats
    else:  # catboost_nocat: categoricals as integer codes, split as ordered numerics (no CTR)
        def prep(x):
            x = x.copy()
            for c in cats:
                x[c] = x[c].cat.codes.astype("float64").replace(-1, np.nan)
            return x
        cat_features = []
    m = CatBoostRegressor(**{**CB, **params, "iterations": iters}, random_seed=42,
                          allow_writing_files=False, verbose=False)
    m.fit(Pool(prep(x_tr), label=tr["y"].to_numpy(), cat_features=cat_features))
    resolved = {k: m.get_all_params().get(k) for k in CB_KEYS}
    return m.predict(Pool(prep(x_va), cat_features=cat_features)), resolved


def child(name: str) -> dict:
    import numpy as np
    import polars as pl

    from prc.features import columns

    model, fs, params, iters = CONFIGS[name]
    feats = build_frame(fs)
    tr = feats.filter(pl.col("role") == "train")
    cats, nums = columns(feats)
    out = {"name": name, "model": model, "feature_set": fs, "params": params,
           "iterations": iters, "train_rows": tr.height, "val_rows": feats.height - tr.height,
           "cat_cardinality": {c: tr[c].n_unique() for c in cats}, "n_num": len(nums),
           "rss_gb_after_frame": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                                       / 1024**2, 3),
           "gpu_mib_before": gpu_used_mib(),
           "loadavg_before": Path("/proc/loadavg").read_text().split()[:3]}
    poll = GpuPoll()
    poll.start()
    hashes, times = [], []
    for _ in range(2):
        t0 = time.time()
        pred, resolved = fit_predict(model, feats, params, iters)
        times.append(round(time.time() - t0, 1))
        hashes.append(hashlib.sha256(np.asarray(pred, dtype="float64").tobytes()).hexdigest())
    poll.stop = True
    poll.join()
    out.update(total_s=times, s_per_iter=round(times[0] / iters, 4),
               deterministic=hashes[0] == hashes[1], pred_sha256=[h[:12] for h in hashes],
               peak_rss_gb=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                                 / 1024**2, 3),
               gpu_mib_peak=poll.peak, resolved=resolved)
    return out


def main() -> None:
    if len(sys.argv) > 2 and sys.argv[1] == "--child":
        print("RESULT " + json.dumps(child(sys.argv[2])))
        return
    from prc.paths import running_experiment

    if (eid := running_experiment()):
        raise SystemExit(f"refused: {eid} is running (INC-0008)")
    names = sys.argv[1:] or list(CONFIGS)
    prior = json.loads(OUT.read_text())["runs"] if OUT.exists() else []
    runs = [r for r in prior if r["name"] not in names]
    for name in names:
        r = subprocess.run([sys.executable, __file__, "--child", name],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [ln for ln in r.stdout.splitlines() if ln.startswith("RESULT ")]
        if not line:
            print(r.stderr[-3000:])
            runs.append({"name": name, "error": r.stderr[-1000:]})
            continue
        res = json.loads(line[0][7:])
        runs.append(res)
        print(json.dumps(res), flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "note": "permuted-target timing only; no metric computed (scripts/calibrate_gpu.py)",
        "fold": "R3", "host": "owner laptop: Ryzen 7 260, RTX 5060 Laptop 8 GB, WSL2 11 GB",
        "runs": runs}, indent=1) + "\n")


if __name__ == "__main__":
    main()
