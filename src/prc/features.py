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
# Day 3 congestion columns are appended after the FS1 columns (same names as
# prc.congestion.FEATURES; test_features_fs2 checks they agree), so FS0/FS1 frames keep
# their exact column order.
CONGESTION_NUMERIC = ["cg_dep_taxiing", "cg_dep_taxiing_rwy", "cg_dep_to_p15", "cg_dep_to_p30",
                      "cg_dep_to_rwy_p15", "cg_dep_off_p15", "cg_arr_land_p15",
                      "cg_arr_taxiing", "cg_sched_dep_n30", "cg_sched_arr_n30",
                      "cg_dep_to_during", "cg_dep_to_rwy_during", "cg_arr_land_during",
                      "cg_rwy_gap_prev", "cg_dep_to_rwy_m15"]
# Day 4 prior columns (same names as prc.priors.FEATURES; a test checks they agree)
PRIOR_NUMERIC = ["pr_stand_rwy", "pr_stand_rwy_logn", "pr_rwy_hour", "pr_op", "pr_actype"]
# Day 8 weather columns (same names as prc.weather.FEATURES; a test checks they agree).
# No FEATURE_SETS entry: the weather table is an input the caller joins (INC-0019).
WEATHER_NUMERIC = ["wx_age_min", "wx_wind_kt", "wx_gust_kt", "wx_headwind_kt",
                   "wx_crosswind_kt", "wx_vis_mi", "wx_ceiling_ft", "wx_temp_c", "wx_spread_c",
                   "wx_rain", "wx_snow", "wx_freezing", "wx_ts", "wx_fog", "wx_precip_3h",
                   "wx_snow_6h"]
NUMERIC = (FS0_NUMERIC + FS1_EXTRA_NUMERIC + CONGESTION_NUMERIC + PRIOR_NUMERIC
           + WEATHER_NUMERIC)
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


def raw_static_exprs() -> dict[str, pl.Expr]:
    """Row-own static keys at raw level, nulls kept (fs1 fills them with sentinels; the Day 4
    priors treat null as an unseen key). Shared so both use the same expressions."""
    sched_local = local_time("SCHED_TIME_UTC_mvt")
    return {
        "stand": pl.col("STAND_mvt").alias("stand"),
        "actype": pl.col("AIRCRAFT_TYPE_mvt").alias("actype"),
        "op_prefix": pl.col("FLIGHT_mvt").str.slice(0, 3).alias("op_prefix"),
        "ades": pl.col("ADES_mvt").alias("ades"),
        "sched_hour_local": sched_local.dt.hour().cast(pl.Int32).alias("sched_hour_local"),
        "sched_weekday_local": sched_local.dt.weekday().cast(pl.Int32).alias(
            "sched_weekday_local"),
    }


def fs1(view: pl.LazyFrame, collapse: bool = True) -> pl.DataFrame:
    dep = view.filter(pl.col("PHASE_mvt") == "DEP")
    raw = raw_static_exprs()
    fill = {"stand": "NA", "actype": "UNK", "op_prefix": "UNK", "ades": "UNK"}
    static = dep.select(
        "MVT_ID_mvt",
        *[(e.fill_null(fill[k]) if k in fill else e).alias(k) for k, e in raw.items()],
    ).collect()
    feats = fs0(view).join(static, on="MVT_ID_mvt", how="left", validate="1:1")
    if collapse:
        feats = collapse_rare(feats, FS1_EXTRA_CATEGORICAL)
    return feats.sort("MVT_ID_mvt")


def fs1_no_deltas(view: pl.LazyFrame) -> pl.DataFrame:
    """FS1 minus the NM/schedule time deltas (H011: static structure without the anchor)."""
    return fs1(view).drop(DELTAS)


def fs1_no_dsched(view: pl.LazyFrame) -> pl.DataFrame:
    """FS1 minus d_sched only (H010: convention ablation)."""
    return fs1(view).drop("d_sched")


ANCHOR = ["d_aobt3", "d_eobt1"]
SCHED_LOCAL = ["sched_hour_local", "sched_weekday_local"]


def fs1_no_anchor(view: pl.LazyFrame) -> pl.DataFrame:
    """FS1 minus the NM anchor deltas d_aobt3 and d_eobt1; d_sched and flt_missing kept
    (H012: M2 ablation with d_sched held fixed)."""
    return fs1(view).drop(ANCHOR)


def fs1_static_no_deltas(view: pl.LazyFrame) -> pl.DataFrame:
    """FS0_NO_DELTAS plus the four static FS1 keys, without the local scheduled time, so that
    no hour-resolution schedule-delay proxy (takeoff hour vs scheduled hour) exists
    (H011 v2)."""
    return fs1(view).drop(DELTAS + SCHED_LOCAL)


def fs2(view: pl.LazyFrame) -> pl.DataFrame:
    """FS1 plus the Day 3 congestion block (prc.congestion: P and T groups)."""
    from prc.congestion import congestion

    return fs1(view).join(congestion(view), on="MVT_ID_mvt", how="left",
                          validate="1:1").sort("MVT_ID_mvt")


def fs2_raw(view: pl.LazyFrame) -> pl.DataFrame:
    """FS2 without the RARE_MIN collapse of the FS1 static keys (Day 5): stand, actype,
    op_prefix and ades keep every raw level seen in training. Levels absent from the
    training rows still become null in the model frame (prc.models.gbm._frames)."""
    from prc.congestion import congestion

    return fs1(view, collapse=False).join(congestion(view), on="MVT_ID_mvt", how="left",
                                          validate="1:1").sort("MVT_ID_mvt")


def fs2_p(view: pl.LazyFrame) -> pl.DataFrame:
    """FS1 plus the P-labelled congestion features only (state at the off-block proxy)."""
    from prc.congestion import T_FEATURES

    return fs2(view).drop(T_FEATURES)


def fs3(view: pl.LazyFrame) -> pl.DataFrame:
    """FS2 plus the Day 4 fold-local target-prior block (prc.priors, label P)."""
    from prc.priors import priors

    return fs2(view).join(priors(view), on="MVT_ID_mvt", how="left",
                          validate="1:1").sort("MVT_ID_mvt")


FEATURE_SETS = {"FS0": fs0, "FS0_NO_DELTAS": fs0_no_deltas, "FS1": fs1,
                "FS1_NO_DELTAS": fs1_no_deltas, "FS1_NO_DSCHED": fs1_no_dsched,
                "FS1_NO_ANCHOR": fs1_no_anchor, "FS1_STATIC_NO_DELTAS": fs1_static_no_deltas,
                "FS2": fs2, "FS2_RAW": fs2_raw, "FS2_P": fs2_p, "FS3": fs3}


def columns(feats: pl.DataFrame) -> tuple[list[str], list[str]]:
    """(categorical, numeric) model inputs present in a feature frame. FS0 columns keep
    their FS0 order; FS1 additions follow."""
    return ([c for c in CATEGORICAL if c in feats.columns],
            [c for c in NUMERIC if c in feats.columns])
