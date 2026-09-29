"""Tier 2 structural model (Day 3): a Tier 1 LightGBM for all rows, except rows of a
routed subgroup, which take the prediction of the champion's model class fitted on the
same fold.

`routed_lightgbm`: the subgroup is LIRF departures without an NM match (ADEP_mvt == LIRF
and AOBT_3 missing, i.e. `flt_missing == 1`; the same definition as prc.attribution's
`LIRF_NM_missing`). The routing key is label P. The ridge is H004's FS0 ridge (E005's
configuration), fitted on the fold's FS0 columns, which every FS1/FS2 frame carries
unchanged; both fits use only the fold's training rows.

params: the LightGBM parameters (as prc.models.gbm.lightgbm) plus `route_ridge_params`
(as prc.models.linear.ridge).
"""

from __future__ import annotations

import polars as pl

from prc.features import FS0
from prc.models import gbm, linear

ROUTE_AIRPORT = "LIRF"


def route_mask() -> pl.Expr:
    return (pl.col("ADEP_mvt") == ROUTE_AIRPORT) & (pl.col("flt_missing") == 1)


def routed_lightgbm(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    p = dict(params)
    ridge_params = p.pop("route_ridge_params")
    tier1 = gbm.lightgbm(feats, p, seed).rename({"pred": "pred_tier1"})
    fs0_frame = feats.select("MVT_ID_mvt", "role", "month", "y", *FS0)
    champ = linear.ridge(fs0_frame, ridge_params, seed).rename({"pred": "pred_route"})
    va = feats.filter(pl.col("role") == "val").select("MVT_ID_mvt", route_mask().alias("route"))
    return (va.join(tier1, on="MVT_ID_mvt", how="left", validate="1:1")
            .join(champ, on="MVT_ID_mvt", how="left", validate="1:1")
            .select("MVT_ID_mvt", pl.when(pl.col("route")).then(pl.col("pred_route"))
                    .otherwise(pl.col("pred_tier1")).alias("pred")))
