"""Day 9: the taxi-state block (prc.taxistate), on the congestion tests' synthetic scene."""

from __future__ import annotations

import polars as pl
import pytest

from prc import taxistate as tx
from tests.test_features_fs2 import arr, at, dep, frame, row, scene  # noqa: F401


def test_hand_values(scene):  # noqa: F811
    # Subject: row 1, off 0, takeoff 20, runway 09. Durations are (takeoff - AOBT_3) for
    # DEP and (in-block - landing) for ARR, in seconds.
    r = row(tx.taxistate(scene), 1)
    assert r["tx_dep_p30"] == 1080.0            # row 4 (airborne -2, 18 min)
    assert r["tx_dep_p90"] == (1080.0 + 300.0) / 2  # rows 4 and 7
    assert r["tx_dep_rwy_p30"] == 1080.0        # row 4 is on 09
    assert r["tx_dep_during"] == (900.0 + 420.0) / 2  # rows 2 (5) and 5 (10); not row 1
    assert r["tx_arr_in_p30"] == 420.0 and r["tx_arr_in_p90"] == 420.0  # ARR 101
    assert r["tx_arr_in_during"] == (540.0 + 480.0) / 2  # ARR 102 and 103


def test_other_airport_and_empty_windows_give_null(scene):  # noqa: F811
    r = row(tx.taxistate(scene), 8)  # the only EGLL row
    assert all(r[f] is None for f in tx.FEATURES)


def test_invariant_to_dep_block_and_target(scene):  # noqa: F811
    masked = scene.with_columns(
        pl.when(pl.col("PHASE_mvt") == "DEP").then(None).otherwise(pl.col(c)).alias(c)
        for c in ("BLOCK_TIME_UTC_mvt", "TAXITIME_SEC_mvt"))
    assert tx.taxistate(scene).equals(tx.taxistate(masked))


@pytest.mark.parametrize("own_to", [-40, -20, -10, -1, 0, 1, 5, 20, 45])
def test_p_features_invariant_to_own_takeoff(scene, own_to):  # noqa: F811
    """A P feature averages other rows only: moving the subject's own takeoff time (its
    t_off proxy held fixed) changes no P feature."""
    base = row(tx.taxistate(scene), 1)
    moved = scene.with_columns(
        pl.when(pl.col("MVT_ID_mvt") == 1).then(pl.lit(at(own_to)))
        .otherwise(pl.col("MVT_TIME_UTC_mvt")).alias("MVT_TIME_UTC_mvt"))
    r = row(tx.taxistate(moved), 1)
    for f in tx.P_FEATURES:
        if base[f] is None:
            assert r[f] is None, (f, own_to)
        else:  # prefix-sum subtraction: equal up to rounding
            assert r[f] == pytest.approx(base[f], abs=1e-6), (f, own_to)


def test_durations_clipped_and_missing_aobt_skipped():
    v = frame([dep(1, 0, 20), dep(2, -200, -5), dep(3, -20, -3, aobt=False),
               arr(101, -100, -2)])
    r = row(tx.taxistate(v), 1)
    assert r["tx_dep_p30"] == tx.CLIP_S          # row 2: 195 min, clipped; row 3 has no AOBT_3
    assert r["tx_arr_in_p30"] == tx.CLIP_S       # 98 min taxi-in, clipped


def test_feature_names_agree_with_prc_features():
    from prc.features import TAXISTATE_NUMERIC
    assert TAXISTATE_NUMERIC == tx.FEATURES
