"""Day 8 design pilot for the convention mixture, on design months only.

Reads targets of January and April-June 2025 only: the months in the training part of every
development fold (X-D08-S01-0001 (d), "What stays legitimate"). No validation-month target of
any development fold, and no December target, is read. Not an experiment: no E###, no fold
score, and no candidate is selected by it. The parameters are the ones the proposal
registers, fixed before this pilot.

Two pilot splits: P1 trains on 2025-01, 04, 05 and predicts 2025-06; P2 trains on 2025-01,
04, 06 and predicts 2025-05. On each, for the LIRF NM-missing rows of the predicted month:
the mixture, its components, and the direct LightGBM regression with E020's configuration
(E045's parameters) on all rows, as in E046's subgroup.

    uv run python scripts/pilot_mixture_D08.py --out research/day-08/eda/pilot_mixture.json
"""

from __future__ import annotations

import argparse
import json
import time

import numpy as np
import polars as pl
import yaml

from prc.data import load_silver
from prc.features import FEATURE_SETS
from prc.models import gbm
from prc.models.mixture import convention_mixture
from prc.models.routed import route_mask
from prc.paths import ROOT
from prc.splits import Fold, masked_view

DESIGN_MONTHS = {"2025-01", "2025-04", "2025-05", "2025-06"}
PILOTS = {"P1": (("2025-01", "2025-04", "2025-05"), ("2025-06",)),
          "P2": (("2025-01", "2025-04", "2025-06"), ("2025-05",))}
TAIL_S = 3600.0


def rmse(e: np.ndarray) -> float:
    return float(np.sqrt(np.mean(e**2))) if e.size else float("nan")


def auc(y: np.ndarray, s: np.ndarray) -> float:
    pos, neg = s[y == 1], s[y == 0]
    if not pos.size or not neg.size:
        return float("nan")
    ranks = pl.Series(np.concatenate([pos, neg])).rank("average").to_numpy()
    return float((ranks[: pos.size].sum() - pos.size * (pos.size + 1) / 2)
                 / (pos.size * neg.size))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default="research/day-08/proposals/H038_params.yaml")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    params = yaml.safe_load((ROOT / args.params).read_text())
    mix, direct = params["mixture"], dict(params["direct_reference"])
    silver = load_silver()
    out = {"schema": "pilot-mixture-v1", "design_months": sorted(DESIGN_MONTHS),
           "params_file": args.params, "pilots": {}}
    for pid, (train, val) in PILOTS.items():
        assert set(train) | set(val) <= DESIGN_MONTHS
        t0 = time.time()
        fold = Fold(fold_id=pid, kind="pilot", train_months=train, val_months=val)
        feats = FEATURE_SETS["FS2"](masked_view(silver, fold))
        comp = convention_mixture(feats, mix, 42)
        d = gbm.lightgbm(feats, direct, 42).rename({"pred": "direct"})
        truth = silver.filter(pl.col("month").is_in(list(val))).select(
            pl.col("MVT_ID_mvt").cast(pl.Int64), pl.col("TAXITIME_SEC_mvt").alias("y_true"))
        rows = (comp.join(d.with_columns(pl.col("MVT_ID_mvt").cast(pl.Int64)),
                          on="MVT_ID_mvt", how="left", validate="1:1")
                .join(truth, on="MVT_ID_mvt", how="left", validate="1:1")
                .join(feats.select(pl.col("MVT_ID_mvt").cast(pl.Int64), "d_sched"),
                      on="MVT_ID_mvt", how="left", validate="1:1"))
        y = rows["y_true"].to_numpy().astype(float)
        conv = (np.abs(y - rows["d_sched"].fill_null(np.nan).to_numpy()) < 120).astype(int)
        tail = y >= TAIL_S
        res = {"train_months": list(train), "val_month": val[0], "subgroup_rows": rows.height,
               "train_subgroup_rows": feats.filter((pl.col("role") == "train")
                                                   & route_mask()).height,
               "convention_rate_val": float(conv.mean()), "tail_rows_val": int(tail.sum()),
               "classifier_auc": auc(conv, rows["p_conv"].to_numpy()),
               "classifier_brier": float(np.mean((rows["p_conv"].to_numpy() - conv) ** 2)),
               "mean_p_conv": float(rows["p_conv"].mean())}
        for name in ("pred", "direct", "g_normal", "conv_component"):
            e = rows[name].to_numpy() - y
            key = "mixture" if name == "pred" else name
            res[key] = {"rmse": rmse(e), "rmse_convention": rmse(e[conv == 1]),
                        "rmse_other": rmse(e[conv == 0]), "rmse_tail": rmse(e[tail]),
                        "rmse_bulk": rmse(e[~tail]), "sse": float(np.sum(e**2))}
        res["mixture_minus_direct_rmse"] = res["mixture"]["rmse"] - res["direct"]["rmse"]
        res["seconds"] = round(time.time() - t0, 1)
        out["pilots"][pid] = res
        print(pid, json.dumps({k: res[k] for k in ("subgroup_rows", "convention_rate_val",
                                                   "classifier_auc",
                                                   "mixture_minus_direct_rmse", "seconds")}),
              flush=True)
    (ROOT / args.out).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / args.out).write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
