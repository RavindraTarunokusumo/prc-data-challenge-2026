"""Day 5: fixed-weight blend of gate-allocated component experiments' stored predictions.

params: {"components": [E###, ...], "weights": [w, ...]} with weights fixed a priori in the
proposal (they sum to 1; nothing is fitted). Each component must be COMPLETE in the ledger
and cover the fold; its prediction file is read through prc.evaluate's manifest-checked
loader. Components were trained on the same fold's training rows only, so the blend uses
no information beyond theirs. The features frame supplies only the validation ids.
"""

from __future__ import annotations

import polars as pl

from prc import ledger
from prc.evaluate import _predictions


def blend(feats: pl.DataFrame, params: dict, seed: int, fold: str) -> pl.DataFrame:
    comps, weights = params["components"], params["weights"]
    if len(comps) != len(weights) or len(comps) < 2 or abs(sum(weights) - 1.0) > 1e-12:
        raise ValueError("blend: components and weights must match, n >= 2, weights sum 1")
    for eid in comps:
        rec = ledger.get(eid)
        if rec is None or rec["status"] != "COMPLETE":
            raise ValueError(f"blend: component {eid} is not COMPLETE")
    ids = feats.filter(pl.col("role") == "val").select(pl.col("MVT_ID_mvt").cast(pl.Int64))
    out = ids.with_columns(pl.lit(0.0).alias("pred"))
    for eid, w in zip(comps, weights, strict=True):
        p = _predictions(eid, fold).select(pl.col("MVT_ID_mvt").cast(pl.Int64),
                                            pl.col("pred").alias("c"))
        out = out.join(p, on="MVT_ID_mvt", how="left", validate="1:1")
        if out["c"].null_count():
            raise ValueError(f"blend: {eid} lacks predictions for some {fold} rows")
        out = out.with_columns((pl.col("pred") + w * pl.col("c")).alias("pred")).drop("c")
    return out


blend.needs_fold = True
