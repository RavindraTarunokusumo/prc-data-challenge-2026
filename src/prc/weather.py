"""Day 8 weather block (INC-0019; DATA_POLICY rule 7): METAR reports at the departure airport.

Pure functions only. The bronze IEM files are read by scripts/build_weather.py, which writes
the weather table this module takes as input; nothing here reads a file or a target.

Availability (INC-0019, "only observations issued before the anchor"). For each DEP row the
lookup instant is the off-block proxy t_off = coalesce(AOBT_3, EOBT_1, SCHED) (the same proxy
as prc.congestion) minus LAG_MIN minutes. The row takes the latest report at its ADEP
whose observation time `valid` is at or before that instant, and none older than MAX_AGE.
A METAR is issued within minutes of its observation time, so LAG_MIN = 10 keeps every
report used issued before t_off. All features are label P (DATASET_AUDIT §6.2), with the proxy caveat.

Features (numeric):
  wx_age_min         minutes from the report's observation time to t_off
  wx_wind_kt         mean wind speed (kt)
  wx_gust_kt         gust (kt); the mean wind where no gust is reported
  wx_headwind_kt     wind component along the row's departure runway heading (kt; runway
                     designators are magnetic, METAR direction is true); null
                     for variable or calm direction, or a runway without a heading
  wx_crosswind_kt    |cross component| on that runway (kt)
  wx_vis_mi          visibility (statute miles)
  wx_ceiling_ft      lowest BKN/OVC/VV layer (ft); CEILING_NONE when no such layer
  wx_temp_c          temperature (°C)
  wx_spread_c        temperature minus dew point (°C)
  wx_rain, wx_snow, wx_freezing, wx_ts, wx_fog
                     present-weather flags in the report (0/1)
  wx_precip_3h       reports with any precipitation in the 3 h up to the report
  wx_snow_6h         reports with snow in the 6 h up to the report
"""

from __future__ import annotations

import math

import polars as pl

LAG_MIN = 10
MAX_AGE = "3h"
CEILING_NONE = 50_000.0
FEATURES = ["wx_age_min", "wx_wind_kt", "wx_gust_kt", "wx_headwind_kt", "wx_crosswind_kt",
            "wx_vis_mi", "wx_ceiling_ft", "wx_temp_c", "wx_spread_c", "wx_rain", "wx_snow",
            "wx_freezing", "wx_ts", "wx_fog", "wx_precip_3h", "wx_snow_6h"]
PRECIP = r"RA|DZ|SN|SG|PL|GS|GR|UP"
SNOW = r"SN|SG|PL"


def _num(c: str) -> pl.Expr:
    return pl.col(c).replace("M", None).cast(pl.Float64, strict=False)


def reports(raw: pl.DataFrame) -> pl.DataFrame:
    """Typed per-report table from the IEM CSV columns (all strings, 'M' for missing)."""
    wx = pl.col("wxcodes").replace("M", "").fill_null("")
    ceil = pl.min_horizontal([
        pl.when(pl.col(f"skyc{i}").is_in(["BKN", "OVC", "VV"])).then(_num(f"skyl{i}"))
        for i in range(1, 5)])
    tmp = (_num("tmpf") - 32) / 1.8
    out = raw.select(
        pl.col("station"),
        pl.col("valid").str.to_datetime("%Y-%m-%d %H:%M", time_zone="UTC"),
        _num("sknt").alias("wx_wind_kt"),
        pl.coalesce(_num("gust"), _num("sknt")).alias("wx_gust_kt"),
        _num("drct").alias("drct"),
        _num("vsby").alias("wx_vis_mi"),
        ceil.fill_null(CEILING_NONE).alias("wx_ceiling_ft"),
        tmp.alias("wx_temp_c"),
        (tmp - (_num("dwpf") - 32) / 1.8).alias("wx_spread_c"),
        wx.str.contains(r"RA|DZ").cast(pl.Int32).alias("wx_rain"),
        wx.str.contains(SNOW).cast(pl.Int32).alias("wx_snow"),
        wx.str.contains("FZ").cast(pl.Int32).alias("wx_freezing"),
        wx.str.contains("TS").cast(pl.Int32).alias("wx_ts"),
        wx.str.contains("FG").cast(pl.Int32).alias("wx_fog"),
        wx.str.contains(PRECIP).cast(pl.Int32).alias("precip"),
    ).sort("station", "valid").unique(["station", "valid"], keep="first", maintain_order=True)
    # Direction 0 with speed 0 is calm; IEM writes VRB as missing.
    out = out.with_columns(pl.when(pl.col("wx_wind_kt") > 0).then(pl.col("drct")).alias("drct"))
    return out.with_columns(
        pl.col("precip").rolling_sum_by("valid", "3h").over("station").alias("wx_precip_3h"),
        pl.col("wx_snow").rolling_sum_by("valid", "6h").over("station").alias("wx_snow_6h"),
    ).drop("precip")


def runway_heading(rwy: pl.Expr) -> pl.Expr:
    """Magnetic heading (degrees) from a runway designator such as '27L'; null otherwise."""
    d = rwy.str.extract(r"^(\d{2})[LRC]?$", 1).cast(pl.Float64, strict=False)
    return pl.when((d >= 1) & (d <= 36)).then(d * 10.0)


def weather_features(view: pl.LazyFrame, reps: pl.DataFrame) -> pl.DataFrame:
    """One row per DEP movement of the view: MVT_ID_mvt plus FEATURES."""
    dep = (view.filter(pl.col("PHASE_mvt") == "DEP")
           .select("MVT_ID_mvt", "ADEP_mvt", "RUNWAY_mvt",
                   pl.coalesce("AOBT_3_flt", "EOBT_1_flt", "SCHED_TIME_UTC_mvt").alias("t_off"))
           .with_columns((pl.col("t_off") - pl.duration(minutes=LAG_MIN)).alias("t_look"))
           .collect().sort("t_look"))
    r = reps.rename({"station": "ADEP_mvt"}).sort("valid")
    j = dep.join_asof(r, left_on="t_look", right_on="valid", by="ADEP_mvt",
                      strategy="backward", tolerance=MAX_AGE, check_sortedness=False)
    rad = ((pl.col("drct") - runway_heading(pl.col("RUNWAY_mvt"))) * math.pi / 180.0)
    return j.select(
        "MVT_ID_mvt",
        ((pl.col("t_off") - pl.col("valid")).dt.total_seconds() / 60.0).alias("wx_age_min"),
        "wx_wind_kt", "wx_gust_kt",
        (pl.col("wx_wind_kt") * rad.cos()).alias("wx_headwind_kt"),
        (pl.col("wx_wind_kt") * rad.sin()).abs().alias("wx_crosswind_kt"),
        "wx_vis_mi", "wx_ceiling_ft", "wx_temp_c", "wx_spread_c", "wx_rain", "wx_snow",
        "wx_freezing", "wx_ts", "wx_fog", "wx_precip_3h", "wx_snow_6h",
    ).sort("MVT_ID_mvt")
