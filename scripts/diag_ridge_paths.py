"""Day 5 target-free diagnosis of the laptop ridge-path difference (D5-C4).

On a fold's masked view, with the training target replaced by a fixed permutation of itself
(rng seed 0; the same permutation for every path, keyed by MVT_ID), the FS0 ridge
(prc.models.linear.ridge, E005's parameters) is fitted on the frames of each code path:

- fs0: `fs0(view)`, as a standalone ridge experiment (E005, E028);
- fs2: `fs2(view)` reduced to FS0 columns, as `routed._routed` does (E019, E023, E027, E029);
- fs2_raw: `fs2_raw(view)` reduced the same way (the CatBoost path of H021, H022);
- fs2_after_lgb: as fs2, after a LightGBM fit in the same process (the routed run order);
- fs0_again: fs0 refitted (repeatability).

Recorded per path: hashes of the ridge's design matrix and target (captured at Ridge.fit),
and the maximum absolute prediction difference against fs0 on all validation rows and on
the routed rows. NO metric is computed; the permuted target carries no signal.

    uv run python scripts/diag_ridge_paths.py R3 S1
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from prc.data import load_silver
from prc.features import FS0, fs0, fs2, fs2_raw
from prc.models import gbm, linear
from prc.models.routed import route_mask
from prc.paths import running_experiment
from prc.splits import get_fold, masked_view

OUT = ROOT / "research" / "day-05" / "eda" / "ridge_paths.json"
RIDGE = {"alpha": 1.0, "winsor": [0.005, 0.995]}
KEEP = ["MVT_ID_mvt", "role", "month", "y", *FS0]
captured: dict = {}


def _h(a) -> str:
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def spy_fit(orig):
    def fit(self, x, y, *a, **k):
        captured["x"] = {"data": _h(x.data), "indices": _h(x.indices), "indptr": _h(x.indptr),
                         "shape": list(x.shape), "dtype": str(x.dtype)}
        captured["y"] = _h(np.asarray(y, dtype=np.float64))
        return orig(self, x, y, *a, **k)
    return fit


def permute(frame: pl.DataFrame, perm: pl.DataFrame) -> pl.DataFrame:
    return frame.drop("y").join(perm, on="MVT_ID_mvt", how="left").select(frame.columns)


def fit(name: str, frame: pl.DataFrame, base: pl.DataFrame, res: dict, preds: dict) -> None:
    captured.clear()
    p = linear.ridge(frame, RIDGE, 42).sort("MVT_ID_mvt")
    preds[name] = p["pred"].to_numpy()
    res[name] = {"x": captured["x"], "y": captured["y"],
                 "frame_equals_fs0": frame.select(KEEP).equals(base.select(KEEP))}


def main(folds: list[str]) -> None:
    if (eid := running_experiment()):
        raise SystemExit(f"refused: {eid} is running (INC-0008)")
    from sklearn.linear_model import Ridge
    Ridge.fit = spy_fit(Ridge.fit)
    silver = load_silver()
    out = {"note": "permuted-target ridge fits on each code path; no metric computed",
           "folds": {}}
    for fid in folds:
        view = masked_view(silver, get_fold(fid))
        a = fs0(view)
        tr = a.filter(pl.col("role") == "train")
        rng = np.random.default_rng(0)
        perm = pl.DataFrame({"MVT_ID_mvt": tr["MVT_ID_mvt"],
                             "y": rng.permutation(tr["y"].to_numpy())}).vstack(
            a.filter(pl.col("role") == "val").select("MVT_ID_mvt", "y"))
        f2 = fs2(view)
        frames = {"fs0": permute(a, perm),
                  "fs2": permute(f2.select(KEEP), perm),
                  "fs2_raw": permute(fs2_raw(view).select(KEEP), perm)}
        routed = a.filter(pl.col("role") == "val").select(
            "MVT_ID_mvt", (route_mask()).alias("route"))
        res, preds = {}, {}
        for name, frame in frames.items():
            fit(name, frame, frames["fs0"], res, preds)
        fit("fs0_again", frames["fs0"], frames["fs0"], res, preds)
        # the routed run order: a LightGBM fit in the same process before the ridge
        lgb_params = {"objective": "regression", "learning_rate": 0.05, "num_leaves": 255,
                      "min_data_in_leaf": 100, "num_threads": 4, "num_boost_round": 20,
                      "bin_construct_sample_cnt": 5_000_000}
        gbm.lightgbm(permute(f2, perm), lgb_params, 42)
        fit("fs2_after_lgb", frames["fs2"], frames["fs0"], res, preds)
        fit("fs0_after_lgb", frames["fs0"], frames["fs0"], res, preds)
        r = routed.sort("MVT_ID_mvt")["route"].to_numpy()
        for name, rec in res.items():
            d = np.abs(preds[name] - preds["fs0"])
            rec.update(max_abs_vs_fs0_all=float(d.max()),
                             max_abs_vs_fs0_routed=float(d[r].max()) if r.any() else None,
                             routed_rows=int(r.sum()),
                             bit_equal_fs0=bool(np.array_equal(preds[name], preds["fs0"])))
        out["folds"][fid] = res
        print(fid, json.dumps({k: {kk: v[kk] for kk in ("frame_equals_fs0", "bit_equal_fs0",
                                                          "max_abs_vs_fs0_routed")}
                               for k, v in res.items()}), flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:] or ["R3"])
