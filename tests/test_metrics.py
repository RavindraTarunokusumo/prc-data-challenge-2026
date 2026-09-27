import datetime as dt

import numpy as np
import polars as pl
import pytest

from prc import metrics


def frame(n=200, seed=0):
    rng = np.random.default_rng(seed)
    t0 = dt.datetime(2025, 9, 1, tzinfo=dt.UTC)
    return pl.DataFrame({
        "MVT_ID_mvt": np.arange(n, dtype=np.int64),
        "TAXITIME_SEC_mvt": rng.integers(-10, 5000, n),
        "pred": rng.normal(900, 200, n),
        "ADEP_mvt": rng.choice(["EDDF", "EGLL"], n),
        "month": ["2025-09"] * n,
        "WK_TBL_CAT_flt": [[None, "M", "H"][i] for i in rng.integers(0, 3, n)],
        "MVT_TIME_UTC_mvt": [t0 + dt.timedelta(minutes=int(m)) for m in rng.integers(0, 600, n)],
    })


def test_rmse_known_value():
    assert metrics.rmse(np.array([0, 0, 0, 0]), np.array([3, -3, 3, -3])) == 3.0


def test_rmse_rejects_bad_shapes():
    with pytest.raises(ValueError):
        metrics.rmse(np.array([1, 2]), np.array([1]))


def test_score_matches_numpy_and_segments_partition():
    df = frame()
    s = metrics.score(df)
    y, p = df["TAXITIME_SEC_mvt"].to_numpy(), df["pred"].to_numpy()
    assert s["rmse"] == pytest.approx(np.sqrt(np.mean((p - y) ** 2)), rel=1e-12)
    for key in ("by_airport", "by_traffic", "by_wake", "by_taxi_band", "by_month"):
        assert sum(v["n"] for v in s[key].values()) == df.height
    assert set(s["by_taxi_band"]) <= set(metrics.TAXI_BAND_LABELS)
    assert "UNK" in s["by_wake"]


def test_taxi_bands_are_left_closed():
    df = frame(7).with_columns(pl.Series("TAXITIME_SEC_mvt", [299, 300, 600, 900, 1200, 1800, 3600]))
    seg = metrics.add_segments(df).sort("MVT_ID_mvt")["seg_taxi_band"].to_list()
    assert seg == ["<300", "300-600", "600-900", "900-1200", "1200-1800", "1800-3600", ">=3600"]


def test_score_is_order_invariant_and_deterministic():
    df = frame(500, seed=3)
    a = metrics.score(df)
    b = metrics.score(df.sample(fraction=1.0, shuffle=True, seed=11))
    assert a["n"] == b["n"]
    assert a["rmse"] == pytest.approx(b["rmse"], rel=1e-12, abs=0)
    for key in ("by_airport", "by_traffic", "by_taxi_band"):
        for k in a[key]:
            assert a[key][k]["n"] == b[key][k]["n"]
            assert a[key][k]["rmse"] == pytest.approx(b[key][k]["rmse"], rel=1e-12)
    assert metrics.score(df) == a


@pytest.mark.parametrize("mutate,msg", [
    (lambda p: pl.concat([p, p.head(1)]), "duplicate"),
    (lambda p: p.head(p.height - 1), "coverage"),
    (lambda p: pl.concat([p, pl.DataFrame({"MVT_ID_mvt": [10**9], "pred": [1.0]})]), "coverage"),
    (lambda p: p.with_columns(pl.when(pl.col("MVT_ID_mvt") == 0).then(float("nan"))
                              .otherwise(pl.col("pred")).alias("pred")), "non-finite"),
])
def test_validate_predictions_rejects(mutate, msg):
    truth = frame(20)
    pred = truth.select("MVT_ID_mvt", "pred")
    metrics.validate_predictions(pred, truth)
    with pytest.raises(ValueError, match=msg):
        metrics.validate_predictions(mutate(pred), truth)


def test_promotion_check_requires_seasonal_and_majority():
    champ = {f: {"rmse": 100.0} for f in ("R1", "R2", "R3", "S1")}
    cand = {"R1": {"rmse": 90.0}, "R2": {"rmse": 90.0}, "R3": {"rmse": 90.0}, "S1": {"rmse": 101.0}}
    air = {"EDDF": 100.0}
    r = metrics.promotion_check(cand, champ, air, air)
    assert r["overall_improves"] and not r["majority_with_seasonal"] and not r["passes_fold_criteria"]
    cand["S1"] = {"rmse": 99.0}
    assert metrics.promotion_check(cand, champ, air, air)["passes_fold_criteria"]
    r = metrics.promotion_check(cand, champ, {"EDDF": 103.5}, air)
    assert "EDDF" in r["airports_degraded_beyond_tolerance"] and not r["passes_fold_criteria"]
