"""Day 8: convention mixture for the routed subgroup (LIRF departures without an NM match;
`routed.route_mask`, label P).

At LIRF, many long recorded taxi-outs are a block-at-schedule recording convention: the
recorded off-block time equals SCHED_TIME, so y = MVT - SCHED = `d_sched` (Day 1, PHASE_CLOSE_D01
review (c); label T). Under squared error the best point forecast is the conditional mean
(Gneiting 2011), which for a two-component population is

    pred = p * max(d_sched, 0) + (1 - p) * g

- p: P(convention | x), a LightGBM binary classifier fitted on the fold's training rows of
  the subgroup, with the label c = |y - d_sched| < `convention_tolerance_s` (Day 1's
  definition, 120 s);
- the convention component is `d_sched` itself (floored at 0 s; nothing is fitted);
- g: the normal-taxi component, a LightGBM regression fitted on the fold's LIRF training rows
  with c = 0 (every LIRF row whose recorded off-block is not at schedule).

Both fits use the fold's training rows only, with fixed a-priori parameters. A subgroup row
with `d_sched` null takes g. Returns the subgroup's validation rows only, with the
components beside the prediction (diagnostics; the worker stores them apart): p, g, the
convention component, the raw `d_sched` and the training subgroup's convention rate.
"""

from __future__ import annotations

import numpy as np
import polars as pl

from prc import curves
from prc.models import gbm
from prc.models.routed import ROUTE_AIRPORT, route_mask

COMPONENT_COLUMNS = ["MVT_ID_mvt", "pred", "p_conv", "g_normal", "conv_component", "d_sched",
                     "p_train_rate"]


def convention_label(tolerance_s: float) -> pl.Expr:
    """c = 1 when the recorded block time is at schedule (training rows only)."""
    return ((pl.col("y") - pl.col("d_sched")).abs() < tolerance_s).fill_null(False)


def convention_mixture(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    tol = float(params["convention_tolerance_s"])
    clf_params = {"objective": "binary", **params["classifier_params"]}
    reg_params = dict(params["normal_params"])
    tr = feats.filter(pl.col("role") == "train")
    va_sub = feats.filter((pl.col("role") == "val") & route_mask())
    if va_sub.height == 0:
        return pl.DataFrame(schema={c: pl.Float64 for c in COMPONENT_COLUMNS}
                            | {"MVT_ID_mvt": pl.Int64})  # no subgroup row in this fold
    tr_sub = tr.filter(route_mask()).with_columns(
        convention_label(tol).cast(pl.Float64).alias("y"))
    tr_normal = tr.filter((pl.col("ADEP_mvt") == ROUTE_AIRPORT) & ~convention_label(tol))
    if tr_sub.height == 0 or not 0 < tr_sub["y"].mean() < 1:
        raise ValueError("convention_mixture: the training subgroup has one class only")
    with curves.paused():  # component fits; their stages are not the experiment's
        p = gbm.lightgbm(pl.concat([tr_sub, va_sub]), clf_params, seed).rename(
            {"pred": "p_conv"})
        g = gbm.lightgbm(pl.concat([tr_normal, va_sub]), reg_params, seed).rename(
            {"pred": "g_normal"})
    out = (va_sub.select(pl.col("MVT_ID_mvt").cast(pl.Int64), "d_sched")
           .join(p.with_columns(pl.col("MVT_ID_mvt").cast(pl.Int64)), on="MVT_ID_mvt",
                 how="left", validate="1:1")
           .join(g.with_columns(pl.col("MVT_ID_mvt").cast(pl.Int64)), on="MVT_ID_mvt",
                 how="left", validate="1:1")
           .with_columns(pl.col("d_sched").cast(pl.Float64).clip(lower_bound=0.0)
                         .alias("conv_component")))
    pred = np.where(out["conv_component"].is_null().to_numpy(), out["g_normal"].to_numpy(),
                    out["p_conv"].to_numpy() * out["conv_component"].fill_null(0.0).to_numpy()
                    + (1.0 - out["p_conv"].to_numpy()) * out["g_normal"].to_numpy())
    # p_train_rate: the training subgroup's convention rate (the constant-p ablation)
    return out.with_columns(pl.Series("pred", pred), pl.col("d_sched").cast(pl.Float64),
                            pl.lit(float(tr_sub["y"].mean())).alias("p_train_rate")
                            ).select(COMPONENT_COLUMNS)
