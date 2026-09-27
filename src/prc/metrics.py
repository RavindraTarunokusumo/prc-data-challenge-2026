"""Frozen metric definitions (brief §9–§10). Immutable after the Day 1 freeze commit.

Primary metric: RMSE in seconds over every row of the evaluation population, with no
clipping, filtering or weighting. Segment reports use the fixed definitions below.
Promotion (brief §10 items 1–3) uses a paired cluster bootstrap whose parameters come
only from the frozen config/splits.yaml `promotion` block.
"""

from __future__ import annotations

import math
import zlib

import numpy as np
import polars as pl

from prc.splits import promotion_config

METRIC_VERSION = "metrics-v2"
ID = "MVT_ID_mvt"
TARGET = "TAXITIME_SEC_mvt"
PRED = "pred"

# Taxi-time bands on the TRUE target (seconds), left-closed.
TAXI_BAND_EDGES = (300, 600, 900, 1200, 1800, 3600)
TAXI_BAND_LABELS = ("<300", "300-600", "600-900", "900-1200", "1200-1800", "1800-3600", ">=3600")
# Diagnostic "bulk" population for per-airport reports: true target below this value.
BULK_MAX_S = 3600
# Traffic regime: DEP takeoffs at the same airport in the same UTC clock hour (MVT_TIME),
# counted over the evaluation population, split at per-airport terciles of that count.
# Terciles are computed per evaluation frame, so labels are not comparable across folds.
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
    err = df[PRED].to_numpy() - df[TARGET].to_numpy()
    return {
        "metric_version": METRIC_VERSION,
        "n": df.height,
        "rmse": rmse(df[TARGET].to_numpy(), df[PRED].to_numpy()),
        "mae": float(np.mean(np.abs(err))),
        "bias": float(np.mean(err)),
        "by_airport": _seg_table(df, "ADEP_mvt"),
        "by_airport_bulk": _seg_table(df.filter(pl.col(TARGET) < BULK_MAX_S), "ADEP_mvt"),
        "by_month": _seg_table(df, "month"),
        "by_traffic": _seg_table(df, "seg_traffic"),
        "by_wake": _seg_table(df, "seg_wake"),
        "by_taxi_band": _seg_table(df, "seg_taxi_band"),
    }


# --- Paired comparison (brief §10) -------------------------------------------------------

def _cluster_sums(cand: pl.DataFrame, champ: pl.DataFrame) -> tuple[np.ndarray, ...]:
    """Per-cluster (airport x UTC day) row counts and SSEs of two predictions on the same
    evaluation rows. Both frames: ID, TARGET, PRED, ADEP_mvt, MVT_TIME_UTC_mvt."""
    j = cand.select(ID, TARGET, "ADEP_mvt", "MVT_TIME_UTC_mvt", pl.col(PRED).alias("pc")).join(
        champ.select(ID, pl.col(PRED).alias("ph")), on=ID, how="inner")
    if j.height != cand.height or j.height != champ.height:
        raise ValueError("paired comparison: candidate and champion rows differ")
    y = pl.col(TARGET).cast(pl.Float64)
    g = (
        j.group_by("ADEP_mvt", pl.col("MVT_TIME_UTC_mvt").dt.date().alias("day"))
        .agg(pl.len().alias("n"), ((pl.col("pc") - y) ** 2).sum().alias("sc"),
             ((pl.col("ph") - y) ** 2).sum().alias("sh"))
        .sort("ADEP_mvt", "day")
    )
    return (g["n"].to_numpy().astype(np.float64), g["sc"].to_numpy(), g["sh"].to_numpy())


def paired_bootstrap(pairs: dict[str, tuple[pl.DataFrame, pl.DataFrame]]) -> dict:
    """dRMSE = RMSE(candidate) - RMSE(champion) per fold: point estimate and bootstrap
    draws (clusters resampled independently per fold; each fold's stream is seeded by the
    frozen seed and the fold id, so it does not depend on which other folds are passed)."""
    cfg = promotion_config()["bootstrap"]
    b = cfg["resamples"]
    out = {}
    for fold in sorted(pairs):
        rng = np.random.default_rng([cfg["seed"], zlib.crc32(fold.encode())])
        n, sc, sh = _cluster_sums(*pairs[fold])
        k = len(n)
        w = rng.multinomial(k, np.full(k, 1.0 / k), size=b).astype(np.float64)
        draws = np.sqrt(w @ sc / (w @ n)) - np.sqrt(w @ sh / (w @ n))
        point = math.sqrt(sc.sum() / n.sum()) - math.sqrt(sh.sum() / n.sum())
        out[fold] = {"point": point, "draws": draws, "clusters": k}
    return out


def fold_outcome(draws: np.ndarray) -> str:
    cfg = promotion_config()["fold_outcome"]
    if np.quantile(draws, cfg["win_upper_quantile"]) < 0:
        return "WIN"
    if np.quantile(draws, cfg["loss_lower_quantile"]) > 0:
        return "LOSS"
    return "TIE"


def _pooled_airport(frames: list[pl.DataFrame]) -> dict[str, float]:
    df = pl.concat([f.select("ADEP_mvt", TARGET, PRED) for f in frames])
    t = df.group_by("ADEP_mvt").agg(
        ((pl.col(PRED) - pl.col(TARGET).cast(pl.Float64)) ** 2).mean().sqrt().alias("r"))
    return dict(sorted(zip(t["ADEP_mvt"], t["r"], strict=True)))


def promotion_check(candidate: dict[str, pl.DataFrame], champion: dict[str, pl.DataFrame]
                    ) -> dict:
    """Brief §10 criteria 1–3 for a candidate against the champion.

    `candidate`/`champion` map fold id -> joined evaluation frame (truth + PRED) and must
    cover every development fold and every causal twin named in the frozen config.
    """
    cfg = promotion_config()
    dev = list(cfg["development_folds"])
    twins = dict(cfg["causal_twins"])
    folds = dev + list(twins.values())
    missing = [f for f in folds if f not in candidate or f not in champion]
    if missing:
        raise ValueError(f"promotion_check: missing folds {missing}")
    boot = paired_bootstrap({f: (candidate[f], champion[f]) for f in folds})
    outcome = {f: fold_outcome(boot[f]["draws"]) for f in folds}

    counted = {}
    for f in dev:
        o = outcome[f]
        if o == "WIN" and f in twins and outcome[twins[f]] == "LOSS":
            o = "TIE"  # a WIN that its causal twin contradicts does not count
        counted[f] = o

    c1 = cfg["criterion_1"]
    mean_draws = np.mean([boot[f]["draws"] for f in dev], axis=0)
    mean_point = float(np.mean([boot[f]["point"] for f in dev]))
    crit1 = (mean_point <= -c1["min_mean_improvement_s"]
             and float(np.quantile(mean_draws, c1["mean_upper_quantile"])) < 0)

    c2 = cfg["criterion_2"]
    wins = sum(o == "WIN" for o in counted.values())
    crit2 = (wins >= c2["min_wins"]
             and (not c2["seasonal_must_win"] or counted[cfg["seasonal_fold"]] == "WIN")
             and (not c2["no_losses"] or all(o != "LOSS" for o in counted.values())))

    tol = cfg["criterion_3"]["airport_rmse_tolerance"]
    air_c = _pooled_airport([candidate[f] for f in dev])
    air_h = _pooled_airport([champion[f] for f in dev])
    degraded = {a: air_c[a] / air_h[a] - 1 for a in air_h if air_c[a] > air_h[a] * (1 + tol)}
    bulk = lambda fr: [x.filter(pl.col(TARGET) < BULK_MAX_S) for x in fr]
    air_c_bulk = _pooled_airport(bulk([candidate[f] for f in dev]))
    air_h_bulk = _pooled_airport(bulk([champion[f] for f in dev]))

    return {
        "fold_delta_rmse": {f: boot[f]["point"] for f in folds},
        "fold_delta_q10_q90": {f: [float(np.quantile(boot[f]["draws"], 0.10)),
                                   float(np.quantile(boot[f]["draws"], 0.90))] for f in folds},
        "fold_outcome": outcome,
        "fold_outcome_counted": counted,
        "mean_delta_rmse": mean_point,
        "mean_delta_q95": float(np.quantile(mean_draws, c1["mean_upper_quantile"])),
        "criterion_1": crit1,
        "criterion_2": crit2,
        "pooled_airport_rmse_candidate": air_c,
        "pooled_airport_rmse_champion": air_h,
        "airports_degraded_beyond_tolerance": degraded,
        "criterion_3": not degraded,
        "diagnostic_pooled_airport_bulk_delta": {a: air_c_bulk[a] - air_h_bulk[a]
                                                 for a in air_h_bulk},
        "passes_criteria_1_to_3": bool(crit1 and crit2 and not degraded),
    }
