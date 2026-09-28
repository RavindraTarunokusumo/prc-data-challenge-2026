"""FS1 (Day 2 static structure): FS0 columns unchanged, validation targets absent, local
time correct, rare-level collapse driven by training-row counts only."""

import datetime as dt

import polars as pl
import pytest

from prc.features import (
    FEATURE_SETS,
    FS0,
    FS1_EXTRA_CATEGORICAL,
    FS1_EXTRA_NUMERIC,
    RARE,
    collapse_rare,
    columns,
    fs0,
    fs1,
    local_time,
)
from prc.splits import get_fold, masked_view


def test_local_time_per_airport_and_dst():
    utc = dt.UTC
    df = pl.DataFrame({
        "ADEP_mvt": ["EGLL", "EGLL", "LTFM", "EDDF", "LIRF"],
        "t": [dt.datetime(2025, 7, 1, 12, tzinfo=utc), dt.datetime(2025, 1, 15, 12, tzinfo=utc),
              dt.datetime(2025, 7, 1, 12, tzinfo=utc), dt.datetime(2025, 1, 15, 23, tzinfo=utc),
              dt.datetime(2025, 3, 30, 1, 30, tzinfo=utc)],
    }).with_columns(pl.col("t").dt.cast_time_unit("us"))
    hours = df.select(local_time("t").dt.hour())["t"].to_list()
    # BST +1, GMT +0, Istanbul +3 all year, CET +1 crossing midnight, CEST from 01:00 UTC
    assert hours == [13, 12, 15, 0, 3]


def test_collapse_rare_counts_training_rows_only():
    feats = pl.DataFrame({
        "role": ["train"] * 5 + ["val"] * 10,
        "stand": ["A"] * 3 + ["B"] * 2 + ["B"] * 10,
        "y": [1.0] * 5 + [None] * 10,
    })
    out = collapse_rare(feats, ["stand"], min_rows=3)
    # B has 12 rows overall but only 2 training rows: collapsed everywhere.
    assert out["stand"].to_list() == ["A"] * 3 + [RARE] * 12


def test_columns_keep_fs0_order():
    frame = pl.DataFrame({c: [0] for c in FS0 + FS1_EXTRA_CATEGORICAL + FS1_EXTRA_NUMERIC})
    cats, nums = columns(frame)
    assert cats[:5] == FS0[:5] and cats[5:] == FS1_EXTRA_CATEGORICAL
    assert nums[:6] == FS0[5:] and nums[6:] == FS1_EXTRA_NUMERIC
    cats0, nums0 = columns(frame.select(FS0))
    assert cats0 + nums0 == FS0


@pytest.mark.parametrize("fold_id", ["R1", "W1c"])
def test_fs1_extends_fs0_on_real_silver(silver, fold_id):
    view = masked_view(silver, get_fold(fold_id))
    f0, f1 = fs0(view), fs1(view)
    assert f1.height == f0.height
    assert f1["MVT_ID_mvt"].to_list() == f0["MVT_ID_mvt"].to_list()
    assert f1.select(f0.columns).equals(f0)
    val = f1.filter(pl.col("role") == "val")
    assert val["y"].null_count() == val.height
    for c in FS1_EXTRA_CATEGORICAL + FS1_EXTRA_NUMERIC:
        assert f1[c].null_count() == 0, c
    assert f1["sched_hour_local"].is_between(0, 23).all()
    for name, drop in (("FS1_NO_DELTAS", {"d_aobt3", "d_eobt1", "d_sched", "flt_missing"}),
                       ("FS1_NO_DSCHED", {"d_sched"})):
        assert set(f1.columns) - set(FEATURE_SETS[name](view).columns) == drop
