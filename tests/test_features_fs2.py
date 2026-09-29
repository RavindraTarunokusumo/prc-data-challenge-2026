"""Day 3 congestion block (prc.congestion) and the FS2 feature sets, on synthetic views."""

from __future__ import annotations

import datetime as dt

import polars as pl
import pytest

from prc import congestion as cg
from prc.features import CONGESTION_NUMERIC, FEATURE_SETS, columns, fs1, fs2, fs2_p

T0 = dt.datetime(2025, 3, 10, 12, 0, tzinfo=dt.UTC)


def at(minutes: float) -> dt.datetime:
    return T0 + dt.timedelta(minutes=minutes)


def dep(mid, off, to, rwy="09", sched=None, apt="EDDF", aobt=True, block=None):
    return {"MVT_ID_mvt": mid, "PHASE_mvt": "DEP", "ADEP_mvt": apt, "ADES_mvt": "LIRF",
            "RUNWAY_mvt": rwy, "MVT_TIME_UTC_mvt": at(to),
            "BLOCK_TIME_UTC_mvt": at(block if block is not None else off),
            "TAXITIME_SEC_mvt": int((to - (block if block is not None else off)) * 60),
            "SCHED_TIME_UTC_mvt": at(sched if sched is not None else off),
            "AOBT_3_flt": at(off) if aobt else None, "EOBT_1_flt": None,
            "STAND_mvt": "A1", "AIRCRAFT_TYPE_mvt": "A320", "FLIGHT_mvt": "DLH1",
            "WK_TBL_CAT_flt": "M", "MARKET_SEGMENT_flt": "S", "FLIGHT_TYPE_flt": "S",
            "month": "2025-03", "role": "train"}


def arr(mid, land, inblock, sched=None, apt="EDDF"):
    return {"MVT_ID_mvt": mid, "PHASE_mvt": "ARR", "ADEP_mvt": "LIRF", "ADES_mvt": apt,
            "RUNWAY_mvt": "25", "MVT_TIME_UTC_mvt": at(land), "BLOCK_TIME_UTC_mvt": at(inblock),
            "TAXITIME_SEC_mvt": int((inblock - land) * 60),
            "SCHED_TIME_UTC_mvt": at(sched if sched is not None else land),
            "AOBT_3_flt": None, "EOBT_1_flt": None, "STAND_mvt": "B2",
            "AIRCRAFT_TYPE_mvt": "A320", "FLIGHT_mvt": "AZA1", "WK_TBL_CAT_flt": None,
            "MARKET_SEGMENT_flt": None, "FLIGHT_TYPE_flt": None, "month": "2025-03",
            "role": "train"}


def frame(rows) -> pl.LazyFrame:
    return pl.DataFrame(rows).with_columns(
        pl.col("AOBT_3_flt").cast(pl.Datetime("us", "UTC")),
        pl.col("EOBT_1_flt").cast(pl.Datetime("us", "UTC"))).lazy()


@pytest.fixture
def scene():
    # Row 1 (the subject): off 0, takeoff 20, runway 09.
    rows = [
        dep(1, 0, 20),
        dep(2, -10, 5),            # taxiing at 0 (off -10, airborne 5), rwy 09, took off during
        dep(3, -5, 30, rwy="27"),  # taxiing at 0 on another runway; airborne after my takeoff
        dep(4, -20, -2),           # took off in [-15, 0): recent takeoff, rwy 09
        dep(5, 3, 10),             # pushed after me, took off during my taxi (rwy 09)
        dep(6, 10, 25, sched=12),  # scheduled within [0, 30)
        dep(7, -40, -35),          # outside all windows
        dep(8, 0, 21, apt="EGLL"),  # other airport: never counted for EDDF rows
        arr(101, -8, -1),          # landed in [-15, 0), in-block before 0
        arr(102, -3, 6),           # landed in [-15, 0), taxiing in at 0
        arr(103, 7, 15, sched=25),  # lands during my taxi; scheduled within [0, 30)
    ]
    return frame(rows)


def row(df: pl.DataFrame, mid: int) -> dict:
    return df.filter(pl.col("MVT_ID_mvt") == mid).to_dicts()[0]


def test_hand_counts(scene):
    r = row(cg.congestion(scene), 1)
    assert r["cg_dep_taxiing"] == 2          # rows 2 and 3
    assert r["cg_dep_taxiing_rwy"] == 1      # row 2 only
    assert r["cg_dep_to_p15"] == 1           # row 4 (at -2); row 7 is at -35
    assert r["cg_dep_to_p30"] == 1
    assert r["cg_dep_to_rwy_p15"] == 1
    assert r["cg_dep_off_p15"] == 2          # rows 2 (-10) and 3 (-5)
    assert r["cg_arr_land_p15"] == 2         # 101, 102
    assert r["cg_arr_taxiing"] == 1          # 102
    assert r["cg_sched_dep_n30"] == 2        # rows 5 (sched 3) and 6 (sched 12); self excluded
    assert r["cg_sched_arr_n30"] == 1        # 103 (sched 25); 101/102 scheduled before 0
    assert r["cg_dep_to_during"] == 2        # rows 2 (5) and 5 (10); row 6 at 25 is after
    assert r["cg_dep_to_rwy_during"] == 2
    assert r["cg_arr_land_during"] == 1      # 103
    assert r["cg_rwy_gap_prev"] == 600.0     # previous rwy-09 takeoff at 10 (row 5)
    assert r["cg_dep_to_rwy_m15"] == 2       # rows 2 (5) and 5 (10) in [5, 20)


def test_other_airport_isolated(scene):
    r = row(cg.congestion(scene), 8)
    assert r["cg_dep_taxiing"] == 0 and r["cg_arr_land_p15"] == 0
    assert r["cg_rwy_gap_prev"] == cg.GAP_CAP_S  # first takeoff on its runway


def test_invariant_to_dep_block_and_target(scene):
    masked = scene.with_columns(
        pl.when(pl.col("PHASE_mvt") == "DEP").then(None).otherwise(pl.col(c)).alias(c)
        for c in ("BLOCK_TIME_UTC_mvt", "TAXITIME_SEC_mvt"))
    assert cg.congestion(scene).equals(cg.congestion(masked))


def test_negative_anchor_interval_not_counted():
    # row 2's off-block proxy lies after its takeoff: it must not count as taxiing at 0
    v = frame([dep(1, 0, 20), dep(2, -1, -6), dep(3, -12, 4)])
    assert row(cg.congestion(v), 1)["cg_dep_taxiing"] == 1  # row 3 only


def test_missing_aobt_falls_back_to_eobt_then_sched():
    v = frame([dep(1, 0, 20), dep(2, -10, 5, aobt=False, sched=-10)])
    r = row(cg.congestion(v), 1)
    assert r["cg_dep_taxiing"] == 1  # row 2 via SCHED proxy at -10


def test_fs2_extends_fs1_without_changing_it(scene):
    a, b = fs1(scene), fs2(scene)
    assert b.columns[: len(a.columns)] == a.columns
    assert b.select(a.columns).equals(a)
    assert b.columns[len(a.columns):] == cg.FEATURES
    assert fs2_p(scene).columns == a.columns + cg.P_FEATURES
    assert set(FEATURE_SETS) >= {"FS2", "FS2_P"}


def test_numeric_names_agree_and_fs1_columns_unchanged(scene):
    assert CONGESTION_NUMERIC == cg.FEATURES
    assert columns(fs1(scene)) == (
        ["ADEP_mvt", "airport_runway", "WK_TBL_CAT_flt", "MARKET_SEGMENT_flt",
         "FLIGHT_TYPE_flt", "stand", "actype", "op_prefix", "ades"],
        ["hour_utc", "weekday", "d_aobt3", "d_eobt1", "d_sched", "flt_missing",
         "sched_hour_local", "sched_weekday_local"])
    _, nums = columns(fs2(scene))
    assert nums[-len(cg.FEATURES):] == cg.FEATURES
