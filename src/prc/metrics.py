"""Frozen metric definitions (brief §9–§10). Immutable after the Day 1 freeze commit.

Primary metric: RMSE in seconds over every row of the evaluation population, with no
clipping, filtering or weighting. Segment reports use the fixed definitions below.
"""

from __future__ import annotations

import math

import numpy as np
import polars as pl

METRIC_VERSION = "metrics-v1"
ID = "MVT_ID_mvt"
TARGET = "TAXITIME_SEC_mvt"
PRED = "pred"

# Taxi-time bands on the TRUE target (seconds), left-closed.
TAXI_BAND_EDGES = (300, 600, 900, 1200, 1800, 3600)
TAXI_BAND_LABELS = ("<300", "300-600", "600-900", "900-1200", "1200-1800", "1800-3600", ">=3600")
# Traffic regime: DEP takeoffs at the same airport in the same UTC clock hour (MVT_TIME),
# counted over the evaluation population, split at per-airport terciles of that count.
TRAFFIC_LABELS = ("low", "mid", "high")


def rmse(y: np.ndarray, p: np.ndarray) -> float:
    y = np.asarray(y, dtype=np.float64)
    p = np.asarray(p, dtype=np.float64)
    if y.shape != p.shape or y.size == 0:
        raise ValueError("rmse: shapes differ or empty input")
    return float(math.sqrt(np.mean((p - y) ** 2)))


def validate_predictions(pred: pl.DataFrame, truth: pl.DataFrame) -> None:
    """Predictions must cover the evaluation population exactly once, with finite values."""
    if pred[ID].is_duplicated().any():
        raise ValueError("duplicate MVT_ID_mvt in predictions")
    if pred[PRED].null_count() or not np.isfinite(pred[PRED].to_numpy()).all():
        raise ValueError("null or non-finite predictions")
    missing = truth.join(pred, on=ID, how="anti").height
    extra = pred.join(truth, on=ID, how="anti").height
    if missing or extra:
        raise ValueError(f"prediction coverage mismatch: {missing} missing, {extra} extra")


def add_segments(df: pl.DataFrame) -> pl.DataFrame:
    """Add the frozen segment columns to an evaluation frame (truth + meta columns)."""
    band = pl.col(TARGET).cut(list(TAXI_BAND_EDGES), labels=list(TAXI_BAND_LABELS),
                              left_closed=True)
    hourly = pl.len().over("ADEP_mvt", pl.col("MVT_TIME_UTC_mvt").dt.truncate("1h"))
    df = df.with_columns(
        band.cast(pl.String).alias("seg_taxi_band"),
        pl.col("WK_TBL_CAT_flt").fill_null("UNK").alias("seg_wake"),
        hourly.alias("_hourly_deps"),
    )
    q = df.group_by("ADEP_mvt").agg(
        pl.col("_hourly_deps").quantile(1 / 3, "linear").alias("_q1"),
        pl.col("_hourly_deps").quantile(2 / 3, "linear").alias("_q2"),
    )
    return (
        df.join(q, on="ADEP_mvt", how="left")
        .with_columns(
            pl.when(pl.col("_hourly_deps") <= pl.col("_q1")).then(pl.lit("low"))
            .when(pl.col("_hourly_deps") <= pl.col("_q2")).then(pl.lit("mid"))
            .otherwise(pl.lit("high"))
            .alias("seg_traffic")
        )
        .drop("_hourly_deps", "_q1", "_q2")
    )


def _seg_table(df: pl.DataFrame, col: str) -> dict[str, dict]:
    t = (
        df.group_by(col)
        .agg(
            pl.len().alias("n"),
            ((pl.col(PRED) - pl.col(TARGET)) ** 2).mean().sqrt().alias("rmse"),
            (pl.col(PRED) - pl.col(TARGET)).mean().alias("bias"),
        )
        .sort(col)
    )
    return {str(r[col]): {"n": r["n"], "rmse": r["rmse"], "bias": r["bias"]}
            for r in t.iter_rows(named=True)}


def score(df: pl.DataFrame) -> dict:
    """Score one evaluation frame with columns: ID, TARGET, PRED, ADEP_mvt, month,
    WK_TBL_CAT_flt, MVT_TIME_UTC_mvt."""
    df = add_segments(df.with_columns(pl.col(TARGET).cast(pl.Float64),
                                      pl.col(PRED).cast(pl.Float64)))
    return {
        "metric_version": METRIC_VERSION,
        "n": df.height,
        "rmse": rmse(df[TARGET].to_numpy(), df[PRED].to_numpy()),
        "mae": float(np.mean(np.abs(df[PRED].to_numpy() - df[TARGET].to_numpy()))),
        "bias": float(np.mean(df[PRED].to_numpy() - df[TARGET].to_numpy())),
        "by_airport": _seg_table(df, "ADEP_mvt"),
        "by_month": _seg_table(df, "month"),
        "by_traffic": _seg_table(df, "seg_traffic"),
        "by_wake": _seg_table(df, "seg_wake"),
        "by_taxi_band": _seg_table(df, "seg_taxi_band"),
    }


def promotion_check(candidate: dict[str, dict], champion: dict[str, dict],
                    pooled_airport_candidate: dict[str, float],
                    pooled_airport_champion: dict[str, float],
                    folds: tuple[str, ...] = ("R1", "R2", "R3", "S1"),
                    seasonal: str = "S1", tolerance: float = 0.03) -> dict:
    """Fold-dependent promotion criteria (brief §10, items 1–3).

    `candidate`/`champion` map fold id -> score dict. `pooled_airport_*` map airport ->
    RMSE pooled over the development folds' evaluation rows.
    """
    wins = {f: candidate[f]["rmse"] < champion[f]["rmse"] for f in folds}
    mean_c = float(np.mean([candidate[f]["rmse"] for f in folds]))
    mean_h = float(np.mean([champion[f]["rmse"] for f in folds]))
    degraded = {
        a: pooled_airport_candidate[a] / pooled_airport_champion[a] - 1
        for a in pooled_airport_champion
        if pooled_airport_candidate[a] > pooled_airport_champion[a] * (1 + tolerance)
    }
    return {
        "overall_improves": mean_c < mean_h,
        "mean_rmse_candidate": mean_c,
        "mean_rmse_champion": mean_h,
        "fold_wins": wins,
        "majority_with_seasonal": sum(wins.values()) >= 3 and wins[seasonal],
        "airports_degraded_beyond_tolerance": degraded,
        "passes_fold_criteria": (mean_c < mean_h and sum(wins.values()) >= 3
                                 and wins[seasonal] and not degraded),
    }
