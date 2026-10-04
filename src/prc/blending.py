"""Day 5: fixed-weight blend of gate-allocated component experiments' stored predictions.

Not a model (it fits nothing and reads files), so it lives outside prc.models and is
dispatched by the worker for `model: blend`. It never imports truth-reading or data-loading
code (tests/test_isolation.py::test_blending_does_not_import_truth).

params: {"components": [E###, ...], "weights": [w, ...]} with weights fixed a priori in the
proposal (they sum to 1; nothing is fitted). Each component must be COMPLETE in the ledger
and cover the fold. Its prediction file is checked against the component's manifest
SHA-256 before use. Components were trained on the same fold's training rows only, so the
blend uses no information beyond theirs.
"""

from __future__ import annotations

import json

import polars as pl

from prc import ledger
from prc.paths import EXPERIMENTS, PREDICTIONS_VAL, ROOT, sha256_file


def stored_predictions(eid: str, fold: str) -> pl.DataFrame:
    """A component's predictions for one fold, verified against its manifest."""
    manifest = json.loads((EXPERIMENTS / eid / "manifest.json").read_text())
    path = PREDICTIONS_VAL / eid / f"{fold}.parquet"
    rel = str(path.relative_to(ROOT))
    entry = next((a for a in manifest["artifacts"] if a["path"] == rel), None)
    if entry is None:
        raise FileNotFoundError(f"blend: {eid} has no predictions for {fold}")
    if sha256_file(path) != entry["sha256"]:
        raise RuntimeError(f"blend: {rel} does not match {eid}/manifest.json")
    return pl.read_parquet(path)


def blend(val_ids: pl.Series, params: dict, fold: str, loader=stored_predictions
          ) -> pl.DataFrame:
    comps, weights = params["components"], params["weights"]
    if len(comps) != len(weights) or len(comps) < 2 or abs(sum(weights) - 1.0) > 1e-12:
        raise ValueError("blend: components and weights must match, n >= 2, weights sum 1")
    for eid in comps:
        rec = ledger.get(eid)
        if rec is None or rec["status"] != "COMPLETE":
            raise ValueError(f"blend: component {eid} is not COMPLETE")
    out = pl.DataFrame({"MVT_ID_mvt": val_ids.cast(pl.Int64)}).with_columns(
        pl.lit(0.0).alias("pred"))
    for eid, w in zip(comps, weights, strict=True):
        p = loader(eid, fold).select(pl.col("MVT_ID_mvt").cast(pl.Int64),
                                     pl.col("pred").alias("c"))
        out = out.join(p, on="MVT_ID_mvt", how="left", validate="1:1")
        if out["c"].null_count():
            raise ValueError(f"blend: {eid} lacks predictions for some {fold} rows")
        out = out.with_columns((pl.col("pred") + w * pl.col("c")).alias("pred")).drop("c")
    return out


# Day 7 (H035/H037): the routed subgroup of prc.models.routed (LIRF departures without an
# NM match; label P). Kept identical to routed.route_mask (tests/test_worker.py) without
# importing model code here.
OVERRIDE_SUBGROUPS = {"LIRF_NM_missing": (pl.col("ADEP_mvt") == "LIRF")
                      & (pl.col("flt_missing") == 1)}


def override(val: pl.DataFrame, params: dict, fold: str, loader=stored_predictions
             ) -> pl.DataFrame:
    """Day 7: a base experiment's stored predictions, with the rows of one named, target-free
    subgroup taken from a second experiment instead. Fits nothing.

    `val`: the fold's validation rows with MVT_ID_mvt, ADEP_mvt and flt_missing.
    params: {"base": E###, "override": E###, "subgroup": "LIRF_NM_missing"}. Both
    experiments must be COMPLETE and cover every row (the override's predictions outside the
    subgroup are read and discarded)."""
    base, over, name = params["base"], params["override"], params["subgroup"]
    if base == over:
        raise ValueError("override: base and override must differ")
    for eid in (base, over):
        rec = ledger.get(eid)
        if rec is None or rec["status"] != "COMPLETE":
            raise ValueError(f"override: {eid} is not COMPLETE")
    rows = val.select(pl.col("MVT_ID_mvt").cast(pl.Int64),
                      OVERRIDE_SUBGROUPS[name].alias("sub"))
    for eid, col in ((base, "pb"), (over, "po")):
        p = loader(eid, fold).select(pl.col("MVT_ID_mvt").cast(pl.Int64),
                                     pl.col("pred").alias(col))
        rows = rows.join(p, on="MVT_ID_mvt", how="left", validate="1:1")
        if rows[col].null_count():
            raise ValueError(f"override: {eid} lacks predictions for some {fold} rows")
    return rows.select("MVT_ID_mvt", pl.when(pl.col("sub")).then(pl.col("po"))
                       .otherwise(pl.col("pb")).alias("pred"))
