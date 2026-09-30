# ruff: noqa: C408
"""Day 4 prior block (prc.priors) and FS3, on synthetic views."""

from __future__ import annotations

import math

import polars as pl
import pytest

from prc import priors as pr
from prc.features import FEATURE_SETS, PRIOR_NUMERIC, columns, fs2, fs3
from tests.test_features_fs2 import at, dep, frame

MONTHS = ["2025-01", "2025-02", "2025-03"]


def mk(mid, month, y, role="train", stand="A1", rwy="09", apt="EDDF", op="DLH",
       actype="A320", hour=12, aobt=True):
    r = dep(mid, mid, mid + 20, rwy=rwy, apt=apt, aobt=aobt)  # distinct times
    r.update(month=month, role=role, STAND_mvt=stand, AIRCRAFT_TYPE_mvt=actype,
             FLIGHT_mvt=op + "1", TAXITIME_SEC_mvt=None if y is None else int(y),
             SCHED_TIME_UTC_mvt=at(mid).replace(hour=hour, minute=0))
    return r


def rows_from(specs):
    return frame([mk(i + 1, **s) for i, s in enumerate(specs)])


def big():
    specs = []
    for m in MONTHS:
        for k in range(6):
            specs.append(dict(month=m, y=600 + 100 * k + 10 * MONTHS.index(m),
                              stand="A1" if k % 2 else "B2", op="DLH" if k < 3 else "BAW",
                              hour=8 + k))
    specs += [dict(month="2025-04", y=None, role="val", stand="A1"),
              dict(month="2025-04", y=None, role="val", stand="ZZZ", op="XXX", actype="Q")]
    return specs


def run(specs, mutate=None):
    if mutate:
        specs = mutate([dict(s) for s in specs])
    return pr.priors(rows_from(specs))


def test_own_target_exclusion():
    base = run(big())
    idx = 3  # a training row of 2025-01
    def mutate(s):
        s[idx]["y"] = 3000 - 1  # still bulk, big change
        return s
    new = run(big(), mutate)
    specs = big()
    changed = (base.join(new, on="MVT_ID_mvt", suffix="_n")
               .with_columns([(pl.col(c) != pl.col(c + "_n")).alias(c + "_d") for c in pr.FEATURES]))
    for i, s in enumerate(specs):
        d = changed.filter(pl.col("MVT_ID_mvt") == i + 1)
        anychg = any(d[c + "_d"][0] for c in pr.FEATURES)
        if s["month"] == "2025-01":
            assert not anychg, f"row {i + 1} of the perturbed month changed"
    assert any(any(changed.filter(pl.col("MVT_ID_mvt") == i + 1)[c + "_d"][0]
                   for c in pr.FEATURES)
               for i, s in enumerate(specs) if s["month"] != "2025-01")


def test_validation_target_independence():
    a = run(big())
    b = run(big(), lambda s: [dict(x, y=1e9) if x.get("role") == "val" else x for x in s])
    assert a.equals(b)


def test_source_filter():
    base = run(big())
    def mutate(s):
        s.append(dict(month="2025-01", y=3600, stand="A1"))            # y >= 3600
        s.append(dict(month="2025-02", y=50000, stand="A1", op="DLH"))
        s.append(dict(month="2025-02", y=100, stand="A1", aobt=False))  # flt_missing == 1
        return s
    new = run(big(), mutate)
    n = len(big())
    assert new.head(n).equals(base)


def test_hand_values():
    # month A: two rows at stand A1 rwy 09 (y=1000, 2000); month B: one row (y=3000) same key;
    # validation row seen key; validation row unseen stand; unseen runway.
    specs = [dict(month="2025-01", y=1000), dict(month="2025-01", y=2000),
             dict(month="2025-02", y=3000),
             dict(month="2025-03", y=None, role="val"),
             dict(month="2025-03", y=None, role="val", stand="NEW"),
             dict(month="2025-03", y=None, role="val", rwy="27", stand="NEW")]
    o = run(specs).sort("MVT_ID_mvt")
    M = pr.PRIOR_M
    apt = 2000.0
    k2 = (6000 + M * apt) / (3 + M)
    k5 = (6000 + M * k2) / (3 + M)
    assert o["pr_stand_rwy"][3] == pytest.approx(k5)
    assert o["pr_stand_rwy_logn"][3] == pytest.approx(math.log1p(3))
    assert o["pr_op"][3] == pytest.approx((6000 + M * apt) / (3 + M))
    assert o["pr_actype"][3] == pytest.approx((6000 + M * apt) / (3 + M))
    # unseen stand -> K2 prior, n = 0
    assert o["pr_stand_rwy"][4] == pytest.approx(k2)
    assert o["pr_stand_rwy_logn"][4] == 0.0
    # unseen runway (and stand) -> airport mean
    assert o["pr_stand_rwy"][5] == pytest.approx(apt)
    # LOMO for a training row of month 2025-02 (y=3000): others are 1000, 2000
    a2 = 1500.0
    k2b = (3000 + M * a2) / (2 + M)
    assert o["pr_stand_rwy"][2] == pytest.approx((3000 + M * k2b) / (2 + M))
    # month 2025-01 row 0: others = 2000 (m01) excluded, 3000 (m02) only
    a0 = 3000.0
    k2c = (3000 + M * a0) / (1 + M)
    assert o["pr_stand_rwy"][0] == pytest.approx((3000 + M * k2c) / (1 + M))


def test_fs3_extends_fs2():
    v = rows_from(big())
    a, b = fs2(v), fs3(v)
    assert set(a.columns) <= set(b.columns)
    assert b.select(a.columns).equals(a)
    assert b.columns[len(a.columns):] == PRIOR_NUMERIC == pr.FEATURES
    assert set(PRIOR_NUMERIC) <= set(columns(b)[1]) and "FS3" in FEATURE_SETS
    for name in ("FS0", "FS1", "FS2", "FS2_P"):
        assert not set(PRIOR_NUMERIC) & set(FEATURE_SETS[name](v).columns)


def test_rows_order_no_nulls():
    v = rows_from(big())
    o = pr.priors(v)
    assert o.height == len(big())
    assert o["MVT_ID_mvt"].to_list() == list(range(1, len(big()) + 1))
    assert all(o[c].null_count() == 0 for c in pr.FEATURES)
    assert all(o[c].dtype == pl.Float64 for c in pr.FEATURES)


def test_null_key_is_unseen():
    specs = big()
    specs.append(dict(month="2025-04", y=None, role="val", stand=None))
    o = run(specs)
    assert o["pr_stand_rwy_logn"][-1] == 0.0
