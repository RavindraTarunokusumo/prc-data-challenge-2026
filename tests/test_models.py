"""Every registered model returns one finite prediction per validation row, using only
training targets (synthetic data; no scoring)."""

import numpy as np
import polars as pl
import pytest

from prc.models import REGISTRY

PARAMS = {
    "lightgbm": {"objective": "regression", "num_boost_round": 5, "num_leaves": 7,
                 "num_threads": 1},
    "xgboost": {"objective": "reg:squarederror", "num_boost_round": 5, "max_depth": 3,
                "nthread": 1},
}


def synthetic(n=400, seed=0):
    rng = np.random.default_rng(seed)
    role = np.where(np.arange(n) < 300, "train", "val")
    y = rng.normal(900, 200, n)
    d_aobt3 = y + rng.normal(0, 100, n)
    d_aobt3[rng.random(n) < 0.05] = np.nan
    return pl.DataFrame({
        "MVT_ID_mvt": np.arange(n, dtype=np.int64),
        "role": role,
        "month": "2025-09",
        "y": np.where(role == "train", y, np.nan),
        "ADEP_mvt": rng.choice(["EDDF", "EGLL", "LIRF"], n),
        "airport_runway": rng.choice(["EDDF_07C", "EGLL_27R", "LIRF_25", "LIRF_NEW"], n),
        "WK_TBL_CAT_flt": rng.choice(["M", "H", "UNK"], n),
        "MARKET_SEGMENT_flt": rng.choice(["Mainline", "Lowcost"], n),
        "FLIGHT_TYPE_flt": rng.choice(["S", "N"], n),
        "hour_utc": rng.integers(0, 24, n).astype(np.int32),
        "weekday": rng.integers(1, 8, n).astype(np.int32),
        "d_aobt3": d_aobt3,
        "d_eobt1": y + rng.normal(0, 300, n),
        "d_sched": y + rng.normal(0, 900, n),
        "flt_missing": np.isnan(d_aobt3).astype(np.int32),
    }).with_columns(pl.col("y").fill_nan(None), pl.col("d_aobt3").fill_nan(None))


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_model_contract(name):
    feats = synthetic()
    pred = REGISTRY[name](feats, PARAMS.get(name, {}), 42)
    val_ids = feats.filter(pl.col("role") == "val")["MVT_ID_mvt"]
    assert pred.columns == ["MVT_ID_mvt", "pred"]
    assert pred.height == val_ids.len() and set(pred["MVT_ID_mvt"]) == set(val_ids)
    assert np.isfinite(pred["pred"].to_numpy()).all()


@pytest.mark.parametrize("name", ["lightgbm", "xgboost", "ridge"])
def test_model_deterministic(name):
    feats = synthetic(seed=1)
    a = REGISTRY[name](feats, PARAMS.get(name, {}), 42)
    b = REGISTRY[name](feats, PARAMS.get(name, {}), 42)
    assert np.array_equal(a["pred"].to_numpy(), b["pred"].to_numpy())


def test_models_ignore_validation_targets():
    """Changing validation-row targets (which should be null anyway) cannot change output."""
    feats = synthetic(seed=2)
    a = REGISTRY["airport_hour_median"](feats, {}, 42)
    tampered = feats.with_columns(
        pl.when(pl.col("role") == "val").then(None).otherwise(pl.col("y")).alias("y"))
    b = REGISTRY["airport_hour_median"](tampered, {}, 42)
    assert a.equals(b)


def test_gbm_uses_only_present_columns():
    from prc.features import DELTAS

    feats = synthetic(seed=3).drop(DELTAS)
    pred = REGISTRY["lightgbm"](feats, PARAMS["lightgbm"], 42)
    assert pred.height == feats.filter(pl.col("role") == "val").height
