"""Day 4 target priors: fold-local, leave-one-month-out smoothed means of the taxi-out time
by static keys (FS3 = FS2 + this block).

Definitions. Source rows = training rows (role == 'train') of the fold frame with a target,
flt_missing == 0 (NM present) and y < 3600 (bulk). Keys use RAW levels (before FS1's
collapse_rare), airport-qualified; a null key value (stand, operator prefix, aircraft type,
local scheduled hour) is treated as an unseen key (n = 0, so the value falls back to the
parent), not as a level of its own. Hierarchy of smoothed means (m-estimate):

    prior(key) = (sum_y + M * parent) / (n + M),   M = PRIOR_M = 50

  airport mean   plain mean by ADEP_mvt (global source mean if the airport has no source rows)
  K2 (internal)  airport_runway; parent = airport mean
  pr_stand_rwy   K5: (ADEP, stand, airport_runway); parent = K2 prior
  pr_stand_rwy_logn  log1p(n) of the K5 key in the same source set
  pr_rwy_hour    K3: (airport_runway, sched_hour_local); parent = K2 prior
  pr_op          K6: (ADEP, op_prefix); parent = airport mean
  pr_actype      K7: (ADEP, actype); parent = airport mean

Label P: keys are row-own static values known at prediction time; the targets are historical
targets of the fold's training months only. Statistics come only from role == 'train' rows of
the frame it is given, so no information from the validation month (or other ranking months)
enters; validation targets are never read (they are null in the masked view, and ignored
even if filled).

Leave-one-month-out (LOMO). For a training row in calendar month m the whole hierarchy
(keys, parents, airport mean) uses source rows of all OTHER training months; validation rows
use all training months (their month has no source rows, so the same formula applies). A
training row's own target, and its own month's targets, never enter its own features, so the
training-row feature distribution matches the validation rows' (up to one month of history)
and the model cannot learn to trust an in-sample prior. Implemented as per-(key, month) sums
and counts: total minus own month. If a fold has a single training month, training rows have
no history and their priors are null (never filled from their own month).

M = 50 is fixed a priori (no tuning).
"""

from __future__ import annotations

import polars as pl

from prc.features import raw_static_exprs

PRIOR_M = 50
Y_BULK = 3600.0
FEATURES = ["pr_stand_rwy", "pr_stand_rwy_logn", "pr_rwy_hour", "pr_op", "pr_actype"]


def _rows(view: pl.LazyFrame) -> pl.DataFrame:
    raw = raw_static_exprs()
    return (view.filter(pl.col("PHASE_mvt") == "DEP")
            .select("MVT_ID_mvt", "role", "month", "ADEP_mvt",
                    (pl.col("ADEP_mvt") + "_" + pl.col("RUNWAY_mvt").fill_null("NA")).alias(
                        "airport_runway"),
                    raw["stand"], raw["op_prefix"], raw["actype"], raw["sched_hour_local"],
                    pl.col("TAXITIME_SEC_mvt").cast(pl.Float64).alias("y"),
                    pl.col("AOBT_3_flt").is_null().cast(pl.Int32).alias("flt_missing"))
            .collect())


def _lomo(rows: pl.DataFrame, src: pl.DataFrame, keys: list[str]) -> pl.DataFrame:
    """rows plus `_s`, `_n`: sum and count of source y over the same key, minus the row's own
    month. Null key values never match (n = 0)."""
    s = src.drop_nulls(keys)
    tot = s.group_by(keys).agg(pl.col("y").sum().alias("_st"), pl.len().alias("_nt"))
    own = s.group_by(keys + ["month"]).agg(pl.col("y").sum().alias("_so"),
                                           pl.len().alias("_no"))
    return (rows.join(tot, on=keys, how="left").join(own, on=keys + ["month"], how="left")
            .with_columns(pl.col("_st", "_so").fill_null(0.0), pl.col("_nt", "_no").fill_null(0))
            .with_columns((pl.col("_st") - pl.col("_so")).alias("_s"),
                          (pl.col("_nt") - pl.col("_no")).alias("_n"))
            .drop("_st", "_so", "_nt", "_no"))


def _smooth(rows: pl.DataFrame, src: pl.DataFrame, keys: list[str], parent: str,
            name: str, keep_n: str | None = None) -> pl.DataFrame:
    r = _lomo(rows, src, keys)
    r = r.with_columns(((pl.col("_s") + PRIOR_M * pl.col(parent)) / (pl.col("_n") + PRIOR_M))
                       .alias(name))
    if keep_n:
        r = r.with_columns(pl.col("_n").cast(pl.Float64).log1p().alias(keep_n))
    return r.drop("_s", "_n")


def priors(view: pl.LazyFrame) -> pl.DataFrame:
    """One row per DEP movement of the view: MVT_ID_mvt plus FEATURES (Float64), sorted."""
    rows = _rows(view)
    src = rows.filter((pl.col("role") == "train") & pl.col("y").is_not_null()
                      & (pl.col("flt_missing") == 0) & (pl.col("y") < Y_BULK))
    # airport mean (LOMO), falling back to the LOMO global source mean
    r = _lomo(rows, src, ["ADEP_mvt"]).rename({"_s": "_as", "_n": "_an"})
    r = _lomo(r.with_columns(pl.lit(0).alias("_g")), src.with_columns(pl.lit(0).alias("_g")),
              ["_g"]).rename({"_s": "_gs", "_n": "_gn"}).drop("_g")
    r = r.with_columns(
        pl.when(pl.col("_an") > 0).then(pl.col("_as") / pl.col("_an"))
        .otherwise(pl.when(pl.col("_gn") > 0).then(pl.col("_gs") / pl.col("_gn")))
        .alias("_apt")).drop("_as", "_an", "_gs", "_gn")
    r = _smooth(r, src, ["airport_runway"], "_apt", "_k2")
    r = _smooth(r, src, ["ADEP_mvt", "stand", "airport_runway"], "_k2", "pr_stand_rwy",
                keep_n="pr_stand_rwy_logn")
    r = _smooth(r, src, ["airport_runway", "sched_hour_local"], "_k2", "pr_rwy_hour")
    r = _smooth(r, src, ["ADEP_mvt", "op_prefix"], "_apt", "pr_op")
    r = _smooth(r, src, ["ADEP_mvt", "actype"], "_apt", "pr_actype")
    return r.select("MVT_ID_mvt", *[pl.col(c).cast(pl.Float64) for c in FEATURES]).sort(
        "MVT_ID_mvt")
