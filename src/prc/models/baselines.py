"""Tier 0 baselines. All statistics come from the fold's training rows only."""

from __future__ import annotations

import polars as pl


def _split(feats: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    tr = feats.filter(pl.col("role") == "train")
    va = feats.filter(pl.col("role") == "val")
    assert tr["y"].null_count() == 0 and va["y"].null_count() == va.height
    return tr, va


def global_mean(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    tr, va = _split(feats)
    return va.select("MVT_ID_mvt", pl.lit(tr["y"].mean()).alias("pred"))


def airport_median(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    tr, va = _split(feats)
    med = tr.group_by("ADEP_mvt").agg(pl.col("y").median().alias("pred"))
    out = va.join(med, on="ADEP_mvt", how="left")
    return out.select("MVT_ID_mvt", pl.col("pred").fill_null(tr["y"].median()))


def airport_hour_median(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    tr, va = _split(feats)
    keys = ["ADEP_mvt", "hour_utc"]
    cell = tr.group_by(keys).agg(pl.col("y").median().alias("p_cell"), pl.len().alias("n"))
    cell = cell.filter(pl.col("n") >= params.get("min_cell", 30))
    apt = tr.group_by("ADEP_mvt").agg(pl.col("y").median().alias("p_apt"))
    out = va.join(cell, on=keys, how="left").join(apt, on="ADEP_mvt", how="left")
    return out.select(
        "MVT_ID_mvt",
        pl.coalesce("p_cell", "p_apt", pl.lit(tr["y"].median())).alias("pred"),
    )


def anchor_aobt3(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    """Unfitted proxy: takeoff minus NM actual off-block; airport median where missing."""
    tr, va = _split(feats)
    apt = tr.group_by("ADEP_mvt").agg(pl.col("y").median().alias("p_apt"))
    out = va.join(apt, on="ADEP_mvt", how="left")
    return out.select("MVT_ID_mvt",
                      pl.coalesce("d_aobt3", "p_apt", pl.lit(tr["y"].median())).alias("pred"))
