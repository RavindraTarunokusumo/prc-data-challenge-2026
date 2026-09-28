"""Feature sets. Every function takes a fold's masked view (splits.masked_view), never
evaluation truth, and returns one row per DEP movement with `role` and the target
(null for validation rows).

FS0 (Day 1 baseline set): row-level columns of the movement itself only. No cross-row
information, no target statistics, no high-cardinality categoricals. All inputs are
admissible under DATASET_AUDIT §6.2 and row-own. Labels: categoricals and flt_missing
are P; hour_utc, weekday and the d_* deltas are T (they use the row's own takeoff time).

FS1 (Day 2, static structure): FS0 plus row-own static keys and the local scheduled time.
All added inputs are label P (stand, aircraft type, operator prefix of the flight number,
destination, scheduled departure time in the airport's local time). Levels of the added
categoricals with fewer than RARE_MIN training DEP rows in the fold become "__RARE__";
the counts use only the fold's training rows and no target.
"""

from __future__ import annotations

import polars as pl

MVT = pl.col("MVT_TIME_UTC_mvt")

FS0_CATEGORICAL = ["ADEP_mvt", "airport_runway", "WK_TBL_CAT_flt", "MARKET_SEGMENT_flt",
                   "FLIGHT_TYPE_flt"]
FS0_NUMERIC = ["hour_utc", "weekday", "d_aobt3", "d_eobt1", "d_sched", "flt_missing"]
FS0 = FS0_CATEGORICAL + FS0_NUMERIC

FS1_EXTRA_CATEGORICAL = ["stand", "actype", "op_prefix", "ades"]
FS1_EXTRA_NUMERIC = ["sched_hour_local", "sched_weekday_local"]
CATEGORICAL = FS0_CATEGORICAL + FS1_EXTRA_CATEGORICAL
NUMERIC = FS0_NUMERIC + FS1_EXTRA_NUMERIC
RARE_MIN = 100  # equals LightGBM's default min_data_per_group
RARE = "__RARE__"
AIRPORT_TZ = {"EDDF": "Europe/Berlin", "EDDM": "Europe/Berlin", "EGLL": "Europe/London",
              "EHAM": "Europe/Amsterdam", "LEBL": "Europe/Madrid", "LEMD": "Europe/Madrid",
              "LFPG": "Europe/Paris", "LIRF": "Europe/Rome", "LSZH": "Europe/Zurich",
              "LTFM": "Europe/Istanbul"}


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


def local_time(col: str) -> pl.Expr:
    """Wall-clock time of a UTC column in the departure airport's time zone."""
    return pl.coalesce([
        pl.when(pl.col("ADEP_mvt") == apt)
        .then(pl.col(col).dt.convert_time_zone(tz).dt.replace_time_zone(None))
        for apt, tz in AIRPORT_TZ.items()])


def collapse_rare(feats: pl.DataFrame, cols: list[str], min_rows: int = RARE_MIN) -> pl.DataFrame:
    """Replace levels seen in fewer than `min_rows` training rows (role == 'train') by RARE.
    Uses row counts only, never the target."""
    tr = feats.filter(pl.col("role") == "train")
    out = []
    for c in cols:
        keep = tr.group_by(c).len().filter(pl.col("len") >= min_rows)[c].to_list()
        out.append(pl.when(pl.col(c).is_in(keep)).then(pl.col(c)).otherwise(pl.lit(RARE))
                   .alias(c))
    return feats.with_columns(out)


def fs1(view: pl.LazyFrame) -> pl.DataFrame:
    dep = view.filter(pl.col("PHASE_mvt") == "DEP")
    sched_local = local_time("SCHED_TIME_UTC_mvt")
    static = dep.select(
        "MVT_ID_mvt",
        pl.col("STAND_mvt").fill_null("NA").alias("stand"),
        pl.col("AIRCRAFT_TYPE_mvt").fill_null("UNK").alias("actype"),
        pl.col("FLIGHT_mvt").str.slice(0, 3).fill_null("UNK").alias("op_prefix"),
        pl.col("ADES_mvt").fill_null("UNK").alias("ades"),
        sched_local.dt.hour().cast(pl.Int32).alias("sched_hour_local"),
        sched_local.dt.weekday().cast(pl.Int32).alias("sched_weekday_local"),
    ).collect()
    feats = fs0(view).join(static, on="MVT_ID_mvt", how="left", validate="1:1")
    return collapse_rare(feats, FS1_EXTRA_CATEGORICAL).sort("MVT_ID_mvt")


def fs1_no_deltas(view: pl.LazyFrame) -> pl.DataFrame:
    """FS1 minus the NM/schedule time deltas (H011: static structure without the anchor)."""
    return fs1(view).drop(DELTAS)


def fs1_no_dsched(view: pl.LazyFrame) -> pl.DataFrame:
    """FS1 minus d_sched only (H010: convention ablation)."""
    return fs1(view).drop("d_sched")


FEATURE_SETS = {"FS0": fs0, "FS0_NO_DELTAS": fs0_no_deltas, "FS1": fs1,
                "FS1_NO_DELTAS": fs1_no_deltas, "FS1_NO_DSCHED": fs1_no_dsched}


def columns(feats: pl.DataFrame) -> tuple[list[str], list[str]]:
    """(categorical, numeric) model inputs present in a feature frame. FS0 columns keep
    their FS0 order; FS1 additions follow."""
    return ([c for c in CATEGORICAL if c in feats.columns],
            [c for c in NUMERIC if c in feats.columns])
