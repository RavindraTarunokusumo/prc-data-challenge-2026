"""Day 9 design pilot for the taxi-state block (prc.taxistate), on design months only.

Reads targets of January and April-June 2025 only: the months in the training part of every
development fold (X-D08-S01-0001 (d); X-D08-S03-0004 Q5 B2). No validation-month target of any
development fold, and no December target, is read. Not an experiment: no E###, no fold score,
and no candidate is selected by it. Every parameter and the decision rule are in
research/day-09/proposals/TX_pilot_params.yaml, committed before this pilot ran.

On each pilot split: LightGBM (E045 / E020's configuration) on FS2, against the same model on
FS2 plus prc.taxistate.FEATURES; and, reported only, on FS2 plus the P features alone.

    uv run python scripts/pilot_taxistate_D09.py --out research/day-09/eda/pilot_taxistate.json
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
from prc.paths import ROOT, sha256_file
from prc.splits import Fold, masked_view
from prc.taxistate import P_FEATURES, T_FEATURES, taxistate

TAIL_S = 3600.0


def rmse(e: np.ndarray) -> float:
    return float(np.sqrt(np.mean(e**2))) if e.size else float("nan")


def readings(rows: pl.DataFrame, cand: str) -> dict:
    y = rows["y_true"].to_numpy().astype(float)
    ref, c = rows["ref"].to_numpy(), rows[cand].to_numpy()

    def seg(mask: np.ndarray) -> dict:
        r, k = rmse(ref[mask] - y[mask]), rmse(c[mask] - y[mask])
        return {"rows": int(mask.sum()), "rmse_ref": r, "rmse_cand": k, "diff": k - r}

    nm = rows["flt_missing"].to_numpy() == 1
    out = {"all": seg(np.ones_like(y, dtype=bool)), "nm_missing": seg(nm),
           "nm_present": seg(~nm), "tail": seg(y >= TAIL_S), "bulk": seg(y < TAIL_S),
           "by_airport": {}}
    for ap in sorted(rows["ADEP_mvt"].unique()):
        out["by_airport"][ap] = seg((rows["ADEP_mvt"] == ap).to_numpy())
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default="research/day-09/proposals/TX_pilot_params.yaml")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    params = yaml.safe_load((ROOT / args.params).read_text())
    design = set(params["design_months"])
    model = dict(params["model"])
    silver = load_silver()
    out = {"schema": "pilot-taxistate-v1", "params_file": args.params,
           "params_sha256": sha256_file(ROOT / args.params), "design_months": sorted(design),
           "pilots": {}}
    for pid, spec in params["pilots"].items():
        train, val = tuple(spec["train"]), tuple(spec["val"])
        assert set(train) | set(val) <= design
        t0 = time.time()
        fold = Fold(fold_id=pid, kind="pilot", train_months=train, val_months=val)
        view = masked_view(silver, fold)
        feats = FEATURE_SETS["FS2"](view)
        tfeats = feats.join(taxistate(view), on="MVT_ID_mvt", how="left", validate="1:1")
        ref = gbm.lightgbm(feats, model, params["seed"]).rename({"pred": "ref"})
        cand = gbm.lightgbm(tfeats, model, params["seed"]).rename({"pred": "cand"})
        p_only = gbm.lightgbm(tfeats.drop(T_FEATURES), model, params["seed"]).rename(
            {"pred": "p_only"})
        truth = silver.filter(pl.col("month").is_in(list(val))
                              & (pl.col("PHASE_mvt") == "DEP")).select(
            "MVT_ID_mvt", pl.col("TAXITIME_SEC_mvt").alias("y_true"))
        rows = (ref.join(cand, on="MVT_ID_mvt", validate="1:1")
                .join(p_only, on="MVT_ID_mvt", validate="1:1")
                .join(truth, on="MVT_ID_mvt", validate="1:1")
                .join(feats.select("MVT_ID_mvt", "ADEP_mvt", "flt_missing"),
                      on="MVT_ID_mvt", validate="1:1"))
        res = {"candidate": readings(rows, "cand"),
               "p_only_reported": readings(rows, "p_only"),
               "train_months": list(train), "val_months": list(val),
               "p_features": P_FEATURES, "t_features": T_FEATURES,
               "seconds": round(time.time() - t0, 1)}
        out["pilots"][pid] = res
        c, p = res["candidate"]["all"], res["p_only_reported"]["all"]
        print(f"{pid}: all rows {c['rmse_ref']:.2f} -> {c['rmse_cand']:.2f} ({c['diff']:+.2f} s);"
              f" P-only {p['diff']:+.2f} s; {res['seconds']} s", flush=True)
    diffs = [p["candidate"]["all"]["diff"] for p in out["pilots"].values()]
    out["decision"] = ("write H039 and send it for review" if all(d <= -1.0 for d in diffs)
                       else "not pursued (decision rule); HANDOFF_D08 §4.3")
    (ROOT / args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(out["decision"])


if __name__ == "__main__":
    main()
