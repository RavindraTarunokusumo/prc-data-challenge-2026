"""Feature sets. Every function takes a fold's masked view (splits.masked_view), never
evaluation truth, and returns one row per DEP movement with `role` and the target
(null for validation rows).

FS0 (Day 1 baseline set): row-level columns of the movement itself only. No cross-row
information, no target statistics, no high-cardinality categoricals. All inputs are
admissible under DATASET_AUDIT §6.2 and row-own. Labels: categoricals and flt_missing
are P; hour_utc, weekday and the d_* deltas are T (they use the row's own takeoff time).
"""

from __future__ import annotations

import polars as pl

MVT = pl.col("MVT_TIME_UTC_mvt")

FS0_CATEGORICAL = ["ADEP_mvt", "airport_runway", "WK_TBL_CAT_flt", "MARKET_SEGMENT_flt",
                   "FLIGHT_TYPE_flt"]
FS0_NUMERIC = ["hour_utc", "weekday", "d_aobt3", "d_eobt1", "d_sched", "flt_missing"]
FS0 = FS0_CATEGORICAL + FS0_NUMERIC


def _secs(a: pl.Expr, b: pl.Expr) -> pl.Expr:
    return (a - b).dt.total_seconds().cast(pl.Float64)


def fs0(view: pl.LazyFrame) -> pl.DataFrame:
    return (
        view.filter(pl.col("PHASE_mvt") == "DEP")
        .select(
            "MVT_ID_mvt",
            "role",
            "month",
            pl.col("TAXITIME_SEC_mvt").cast(pl.Float64).alias("y"),
            "ADEP_mvt",
            (pl.col("ADEP_mvt") + "_" + pl.col("RUNWAY_mvt").fill_null("NA")).alias(
                "airport_runway"),
            pl.col("WK_TBL_CAT_flt").fill_null("UNK"),
            pl.col("MARKET_SEGMENT_flt").fill_null("UNK"),
            pl.col("FLIGHT_TYPE_flt").fill_null("UNK"),
            MVT.dt.hour().cast(pl.Int32).alias("hour_utc"),
            MVT.dt.weekday().cast(pl.Int32).alias("weekday"),
            _secs(MVT, pl.col("AOBT_3_flt")).alias("d_aobt3"),
            _secs(MVT, pl.col("EOBT_1_flt")).alias("d_eobt1"),
            _secs(MVT, pl.col("SCHED_TIME_UTC_mvt")).alias("d_sched"),
            pl.col("AOBT_3_flt").is_null().cast(pl.Int32).alias("flt_missing"),
        )
        .sort("MVT_ID_mvt")
        .collect()
    )


DELTAS = ["d_aobt3", "d_eobt1", "d_sched", "flt_missing"]


def fs0_no_deltas(view: pl.LazyFrame) -> pl.DataFrame:
    """FS0 minus the NM/schedule time deltas (H008 ablation)."""
    return fs0(view).drop(DELTAS)


FEATURE_SETS = {"FS0": fs0, "FS0_NO_DELTAS": fs0_no_deltas}


def columns(feats: pl.DataFrame) -> tuple[list[str], list[str]]:
    """(categorical, numeric) model inputs present in a feature frame, in FS0 order."""
    return ([c for c in FS0_CATEGORICAL if c in feats.columns],
            [c for c in FS0_NUMERIC if c in feats.columns])
