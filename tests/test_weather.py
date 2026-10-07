"""Day 8: the weather block (prc.weather), on synthetic reports."""

import datetime as dt

import polars as pl
import pytest

from prc.weather import CEILING_NONE, FEATURES, reports, weather_features

T0 = dt.datetime(2025, 1, 10, 12, 0, tzinfo=dt.UTC)


def raw(rows):
    """IEM-style string rows: (minutes after T0, sknt, drct, wxcodes, skyc1, skyl1)."""
    cols = {k: [] for k in ("station", "valid", "tmpf", "dwpf", "sknt", "drct", "gust", "vsby",
                            "wxcodes", "skyc1", "skyl1", "skyc2", "skyl2", "skyc3", "skyl3",
                            "skyc4", "skyl4")}
    for m, sknt, drct, wx, c1, l1 in rows:
        t = T0 + dt.timedelta(minutes=m)
        for k, v in (("station", "EDDF"), ("valid", t.strftime("%Y-%m-%d %H:%M")),
                     ("tmpf", "32.0"), ("dwpf", "28.4"), ("sknt", sknt), ("drct", drct),
                     ("gust", "M"), ("vsby", "6.21"), ("wxcodes", wx), ("skyc1", c1),
                     ("skyl1", l1), ("skyc2", "M"), ("skyl2", "M"), ("skyc3", "M"),
                     ("skyl3", "M"), ("skyc4", "M"), ("skyl4", "M")):
            cols[k].append(v)
    return pl.DataFrame(cols)


def view(t_off_minutes, runway="25C"):
    n = len(t_off_minutes)
    return pl.DataFrame({
        "MVT_ID_mvt": list(range(1, n + 1)), "PHASE_mvt": ["DEP"] * n, "ADEP_mvt": ["EDDF"] * n,
        "RUNWAY_mvt": [runway] * n,
        "AOBT_3_flt": [T0 + dt.timedelta(minutes=m) for m in t_off_minutes],
        "EOBT_1_flt": [None] * n, "SCHED_TIME_UTC_mvt": [T0] * n,
    }).with_columns(pl.col("EOBT_1_flt").cast(pl.Datetime("us", "UTC")),
                    pl.col("AOBT_3_flt").cast(pl.Datetime("us", "UTC")),
                    pl.col("SCHED_TIME_UTC_mvt").cast(pl.Datetime("us", "UTC"))).lazy()


REPS = reports(raw([(0, "10", "250", "M", "FEW", "3000"),
                    (30, "20", "60", "-SN", "BKN", "800"),
                    (60, "0", "0", "FZFG", "OVC", "200")]))


def test_report_used_is_observed_at_least_ten_minutes_before_off_block():
    # t_off 39 min: lookup 29 min, so the 0-min report, not the 30-min one.
    out = weather_features(view([39, 40, 41]), REPS)
    assert out.columns == ["MVT_ID_mvt", *FEATURES]
    assert out["wx_wind_kt"].to_list() == [10.0, 20.0, 20.0]
    assert out["wx_age_min"].to_list() == [39.0, 10.0, 11.0]


def test_no_report_before_lookup_or_older_than_three_hours_gives_null():
    out = weather_features(view([5, 300]), REPS)
    assert out["wx_wind_kt"].to_list() == [None, None]


def test_wind_components_against_runway_heading():
    out = weather_features(view([15, 45]), REPS)  # 250° 10 kt, then 060° 20 kt on 25C
    head, cross = out["wx_headwind_kt"].to_list(), out["wx_crosswind_kt"].to_list()
    assert head[0] == pytest.approx(10.0) and cross[0] == pytest.approx(0.0, abs=1e-9)
    assert head[1] == pytest.approx(-20.0 * 0.9848, rel=1e-3) and cross[1] > 0


def test_calm_wind_and_runway_without_heading_give_null_components():
    calm = weather_features(view([75]), REPS)
    assert calm["wx_headwind_kt"].to_list() == [None]
    letter = weather_features(view([15], runway="H"), REPS)
    assert letter["wx_headwind_kt"].to_list() == [None]


def test_flags_ceiling_and_trailing_counts():
    out = weather_features(view([45, 75]), REPS).to_dicts()
    assert out[0]["wx_snow"] == 1 and out[0]["wx_ceiling_ft"] == 800.0
    assert out[1]["wx_freezing"] == 1 and out[1]["wx_fog"] == 1 and out[1]["wx_snow"] == 0
    assert out[1]["wx_snow_6h"] == 1 and out[1]["wx_precip_3h"] == 1
    first = weather_features(view([15]), REPS).to_dicts()[0]
    assert first["wx_ceiling_ft"] == CEILING_NONE and first["wx_temp_c"] == pytest.approx(0.0)
    assert first["wx_spread_c"] == pytest.approx(2.0)


def test_feature_names_agree_with_prc_features():
    from prc.features import WEATHER_NUMERIC
    assert WEATHER_NUMERIC == FEATURES
