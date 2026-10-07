"""Day 8 design pilot for the weather block (agenda item 3; INC-0019), on design months only.

Reads targets of January and April-June 2025 only: the months in the training part of every
development fold (X-D08-S01-0001 (d)), as H038's pilot did. No validation-month target of
any development fold, and no December target, is read. Not an experiment: no E###, no fold
score, and no candidate is selected by it. Every parameter and the decision rule are in
research/day-08/proposals/WX_pilot_params.yaml, committed before this pilot ran.

On each pilot split: LightGBM (E045 / E020's configuration) on FS2, against the same model
on FS2 plus prc.weather.FEATURES.

    uv run python scripts/pilot_weather_D08.py --out research/day-08/eda/pilot_weather.json
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
from prc.paths import PROCESSED, ROOT, sha256_file
from prc.splits import Fold, masked_view
from prc.weather import weather_features

TAIL_S = 3600.0
WEATHER = PROCESSED / "weather_reports.parquet"


def rmse(e: np.ndarray) -> float:
    return float(np.sqrt(np.mean(e**2))) if e.size else float("nan")


def readings(rows: pl.DataFrame) -> dict:
    y = rows["y_true"].to_numpy().astype(float)
    ref, cand = rows["ref"].to_numpy(), rows["cand"].to_numpy()

    def seg(mask: np.ndarray) -> dict:
        r, c = rmse(ref[mask] - y[mask]), rmse(cand[mask] - y[mask])
        return {"rows": int(mask.sum()), "rmse_ref": r, "rmse_cand": c, "diff": c - r}

    wx = rows.select(
        ((pl.col("wx_precip_3h").fill_null(0) > 0) | (pl.col("wx_fog") == 1)
         | (pl.col("wx_vis_mi") < 1) | (pl.col("wx_ceiling_ft") < 500)).fill_null(False)
    ).to_series().to_numpy()
    nm = rows["flt_missing"].to_numpy() == 1
    out = {"all": seg(np.ones_like(y, dtype=bool)), "nm_missing": seg(nm),
           "nm_present": seg(~nm), "tail": seg(y >= TAIL_S), "bulk": seg(y < TAIL_S),
           "adverse_weather": seg(wx), "other_weather": seg(~wx), "by_airport": {},
           "coverage": {}}
    for ap in sorted(rows["ADEP_mvt"].unique()):
        m = (rows["ADEP_mvt"] == ap).to_numpy()
        out["by_airport"][ap] = seg(m)
        out["coverage"][ap] = float(rows.filter(pl.col("ADEP_mvt") == ap)["wx_wind_kt"]
                                    .is_not_null().mean())
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default="research/day-08/proposals/WX_pilot_params.yaml")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    params = yaml.safe_load((ROOT / args.params).read_text())
    design = set(params["design_months"])
    model = dict(params["model"])
    silver = load_silver()
    reps = pl.read_parquet(WEATHER)
    out = {"schema": "pilot-weather-v1", "params_file": args.params,
           "params_sha256": sha256_file(ROOT / args.params),
           "weather_sha256": sha256_file(WEATHER), "design_months": sorted(design),
           "pilots": {}}
    for pid, spec in params["pilots"].items():
        train, val = tuple(spec["train"]), tuple(spec["val"])
        assert set(train) | set(val) <= design
        t0 = time.time()
        fold = Fold(fold_id=pid, kind="pilot", train_months=train, val_months=val)
        view = masked_view(silver, fold)
        feats = FEATURE_SETS["FS2"](view)
        wfeats = feats.join(weather_features(view, reps), on="MVT_ID_mvt", how="left",
                            validate="1:1")
        ref = gbm.lightgbm(feats, model, params["seed"]).rename({"pred": "ref"})
        cand = gbm.lightgbm(wfeats, model, params["seed"]).rename({"pred": "cand"})
        truth = silver.filter(pl.col("month").is_in(list(val))
                              & (pl.col("PHASE_mvt") == "DEP")).select(
            "MVT_ID_mvt", pl.col("TAXITIME_SEC_mvt").alias("y_true"))
        rows = (ref.join(cand, on="MVT_ID_mvt", validate="1:1")
                .join(truth, on="MVT_ID_mvt", validate="1:1")
                .join(wfeats.select("MVT_ID_mvt", "ADEP_mvt", "flt_missing", "wx_wind_kt",
                                    "wx_precip_3h", "wx_fog", "wx_vis_mi", "wx_ceiling_ft"),
                      on="MVT_ID_mvt", validate="1:1"))
        res = readings(rows)
        res.update(train_months=list(train), val_months=list(val),
                   seconds=round(time.time() - t0, 1))
        out["pilots"][pid] = res
        print(f"{pid}: all rows {res['all']['rmse_ref']:.2f} -> {res['all']['rmse_cand']:.2f} "
              f"({res['all']['diff']:+.2f} s), {res['seconds']} s", flush=True)
    diffs = [p["all"]["diff"] for p in out["pilots"].values()]
    out["decision"] = ("forward to an H proposal" if all(d <= -1.0 for d in diffs)
                       else "not pursued (decision rule)")
    (ROOT / args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(out["decision"])


if __name__ == "__main__":
    main()
