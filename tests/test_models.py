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
    "routed_lightgbm": {"objective": "regression", "num_boost_round": 5, "num_leaves": 7,
                        "num_threads": 1,
                        "route_ridge_params": {"alpha": 1.0, "winsor": [0.005, 0.995]}},
    "catboost": {"loss_function": "RMSE", "iterations": 5, "depth": 3, "thread_count": 1},
    "routed_catboost": {"loss_function": "RMSE", "iterations": 5, "depth": 3,
                        "thread_count": 1,
                        "route_ridge_params": {"alpha": 1.0, "winsor": [0.005, 0.995]}},
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


@pytest.mark.parametrize("name", ["lightgbm", "xgboost", "ridge", "catboost"])
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


def test_lightgbm_without_subsampling_is_seed_invariant():
    """With bagging and feature subsampling off, LightGBM does not consume the seed:
    two seeds give identical predictions (basis of the H013 design)."""
    feats = synthetic(n=2000)
    p = {"objective": "regression", "num_boost_round": 30, "num_leaves": 15,
         "num_threads": 1, "bagging_fraction": 1.0, "bagging_freq": 0,
         "feature_fraction": 1.0, "min_data_in_leaf": 20}
    a = REGISTRY["lightgbm"](feats, p, 42)["pred"].to_numpy()
    b = REGISTRY["lightgbm"](feats, p, 43)["pred"].to_numpy()
    assert np.array_equal(a, b)
    bag = {**p, "bagging_fraction": 0.8, "bagging_freq": 1, "feature_fraction": 0.9}
    c = REGISTRY["lightgbm"](feats, bag, 42)["pred"].to_numpy()
    d = REGISTRY["lightgbm"](feats, bag, 43)["pred"].to_numpy()
    assert not np.array_equal(c, d)  # the Day 1/2 configuration does consume the seed


def realistic(n_train, n_val=5000, seed=0):
    """Continuous, heavy-tailed synthetic FS1-like frame (after the X-D02-S01-0004
    review's check): simple synthetic features bin identically whatever the bin sample,
    which hid the bin-construction seed dependence in the test above."""
    rng = np.random.default_rng(seed)
    n = n_train + n_val
    role = np.where(np.arange(n) < n_train, "train", "val")
    base = rng.gamma(4.0, 250.0, n)
    d_sched = base + rng.exponential(900, n)
    y = base
    lv = lambda k, p: np.array([f"{p}{i}" for i in rng.integers(0, k, n)])
    return pl.DataFrame({
        "MVT_ID_mvt": np.arange(n, dtype=np.int64), "role": role, "month": "2025-09",
        "y": np.where(role == "train", y, np.nan),
        "ADEP_mvt": rng.choice(["EDDF", "EGLL", "LIRF"], n), "airport_runway": lv(40, "R"),
        "WK_TBL_CAT_flt": rng.choice(["M", "H"], n), "MARKET_SEGMENT_flt": lv(3, "M"),
        "FLIGHT_TYPE_flt": lv(2, "F"), "hour_utc": rng.integers(0, 24, n).astype(np.int32),
        "weekday": rng.integers(1, 8, n).astype(np.int32),
        "d_aobt3": y + rng.normal(0, 150, n), "d_eobt1": y + rng.normal(0, 400, n),
        "d_sched": d_sched, "flt_missing": np.zeros(n, dtype=np.int32),
    }).with_columns(pl.col("y").fill_nan(None))


def test_lightgbm_seed_invariance_above_bin_sample_threshold():
    """Above LightGBM's bin_construct_sample_cnt (default 200,000 rows) the seed also draws
    the bin-construction sample. Without subsampling that is the only random component;
    binning from all rows (H013 v2) removes it. Committed evidence for H013 v2."""
    feats = realistic(n_train=260_000)
    p = {"objective": "regression", "num_boost_round": 15, "num_leaves": 63,
         "num_threads": 4, "bagging_fraction": 1.0, "bagging_freq": 0,
         "feature_fraction": 1.0, "min_data_in_leaf": 100}
    a = REGISTRY["lightgbm"](feats, p, 42)["pred"].to_numpy()
    b = REGISTRY["lightgbm"](feats, p, 43)["pred"].to_numpy()
    assert not np.array_equal(a, b)  # H013 v1 configuration: the bin sample follows the seed
    full = {**p, "bin_construct_sample_cnt": 5_000_000}
    c = REGISTRY["lightgbm"](feats, full, 42)["pred"].to_numpy()
    d = REGISTRY["lightgbm"](feats, full, 43)["pred"].to_numpy()
    e = REGISTRY["lightgbm"](feats, full, 42)["pred"].to_numpy()
    assert np.array_equal(c, d) and np.array_equal(c, e)  # H013 v2: no random component


def test_routed_lightgbm_routes_only_lirf_nm_missing():
    """Routed rows take the FS0 ridge prediction, all others the LightGBM prediction, each
    identical to the standalone model fitted on the same fold."""
    feats = synthetic(n=2000, seed=5)
    p = PARAMS["routed_lightgbm"]
    out = REGISTRY["routed_lightgbm"](feats, p, 42).sort("MVT_ID_mvt")
    gb = REGISTRY["lightgbm"](feats, {k: v for k, v in p.items() if k != "route_ridge_params"},
                              42).sort("MVT_ID_mvt")
    rd = REGISTRY["ridge"](feats, p["route_ridge_params"], 42).sort("MVT_ID_mvt")
    va = feats.filter(pl.col("role") == "val").sort("MVT_ID_mvt")
    route = ((va["ADEP_mvt"] == "LIRF") & (va["flt_missing"] == 1)).to_numpy()
    assert 0 < route.sum() < route.size
    got = out["pred"].to_numpy()
    assert np.array_equal(got[route], rd["pred"].to_numpy()[route])
    assert np.array_equal(got[~route], gb["pred"].to_numpy()[~route])


def test_routed_ridge_sees_fs0_columns_only():
    """Extra (FS1/FS2) columns change the LightGBM part but never the routed ridge part."""
    feats = synthetic(n=2000, seed=6)
    rng = np.random.default_rng(0)
    extra = feats.with_columns(pl.Series("cg_dep_to_during", rng.normal(size=feats.height)),
                               pl.Series("stand", rng.choice(["A", "B"], feats.height)))
    p = PARAMS["routed_lightgbm"]
    a = REGISTRY["routed_lightgbm"](feats, p, 42).sort("MVT_ID_mvt")
    b = REGISTRY["routed_lightgbm"](extra, p, 42).sort("MVT_ID_mvt")
    va = feats.filter(pl.col("role") == "val").sort("MVT_ID_mvt")
    route = ((va["ADEP_mvt"] == "LIRF") & (va["flt_missing"] == 1)).to_numpy()
    assert np.array_equal(a["pred"].to_numpy()[route], b["pred"].to_numpy()[route])


def test_routed_train_exclude_drops_only_routed_training_rows():
    """H018: with `route_train_exclude`, non-routed rows equal a LightGBM fitted without the
    routed subgroup's training rows, routed rows still take the ridge fitted on every
    training row, and absent/false reproduces the Day 3 procedure."""
    feats = synthetic(n=2000, seed=7)
    p = PARAMS["routed_lightgbm"]
    gb_p = {k: v for k, v in p.items() if k != "route_ridge_params"}
    base = REGISTRY["routed_lightgbm"](feats, p, 42).sort("MVT_ID_mvt")
    off = REGISTRY["routed_lightgbm"](feats, {**p, "route_train_exclude": False}, 42)
    assert np.array_equal(base["pred"].to_numpy(), off.sort("MVT_ID_mvt")["pred"].to_numpy())
    out = REGISTRY["routed_lightgbm"](feats, {**p, "route_train_exclude": True}, 42)
    out = out.sort("MVT_ID_mvt")
    routed_train = (pl.col("role") == "train") & (pl.col("ADEP_mvt") == "LIRF") & (
        pl.col("flt_missing") == 1)
    assert feats.filter(routed_train).height > 0
    gb = REGISTRY["lightgbm"](feats.filter(~routed_train), gb_p, 42).sort("MVT_ID_mvt")
    rd = REGISTRY["ridge"](feats, p["route_ridge_params"], 42).sort("MVT_ID_mvt")
    va = feats.filter(pl.col("role") == "val").sort("MVT_ID_mvt")
    route = ((va["ADEP_mvt"] == "LIRF") & (va["flt_missing"] == 1)).to_numpy()
    got = out["pred"].to_numpy()
    assert np.array_equal(got[route], rd["pred"].to_numpy()[route])
    assert np.array_equal(got[~route], gb["pred"].to_numpy()[~route])


def test_catboost_deterministic_multithread_and_unseen_levels():
    """Same input + seed + thread_count gives identical predictions; a validation level
    unseen in training (null after the vocabulary step) does not break the fit."""
    feats = synthetic(n=2000, seed=8).with_columns(
        pl.when(pl.col("role") == "val").then(pl.lit("NEWRWY")).otherwise(pl.col("airport_runway"))
        .alias("airport_runway"))
    p = {**PARAMS["catboost"], "iterations": 20, "thread_count": 4}
    a = REGISTRY["catboost"](feats, p, 42)["pred"].to_numpy()
    b = REGISTRY["catboost"](feats, p, 42)["pred"].to_numpy()
    assert np.isfinite(a).all() and np.array_equal(a, b)


def test_routed_catboost_routes_only_lirf_nm_missing():
    feats = synthetic(n=2000, seed=5)
    p = PARAMS["routed_catboost"]
    out = REGISTRY["routed_catboost"](feats, p, 42).sort("MVT_ID_mvt")
    cb = REGISTRY["catboost"](feats, {k: v for k, v in p.items() if k != "route_ridge_params"},
                              42).sort("MVT_ID_mvt")
    rd = REGISTRY["ridge"](feats, p["route_ridge_params"], 42).sort("MVT_ID_mvt")
    va = feats.filter(pl.col("role") == "val").sort("MVT_ID_mvt")
    route = ((va["ADEP_mvt"] == "LIRF") & (va["flt_missing"] == 1)).to_numpy()
    assert 0 < route.sum() < route.size
    got = out["pred"].to_numpy()
    assert np.array_equal(got[route], rd["pred"].to_numpy()[route])
    assert np.array_equal(got[~route], cb["pred"].to_numpy()[~route])


def test_routed_catboost_train_exclude():
    feats = synthetic(n=2000, seed=7)
    p = PARAMS["routed_catboost"]
    cb_p = {k: v for k, v in p.items() if k != "route_ridge_params"}
    out = REGISTRY["routed_catboost"](feats, {**p, "route_train_exclude": True}, 42)
    out = out.sort("MVT_ID_mvt")
    routed_train = (pl.col("role") == "train") & (pl.col("ADEP_mvt") == "LIRF") & (
        pl.col("flt_missing") == 1)
    cb = REGISTRY["catboost"](feats.filter(~routed_train), cb_p, 42).sort("MVT_ID_mvt")
    va = feats.filter(pl.col("role") == "val").sort("MVT_ID_mvt")
    route = ((va["ADEP_mvt"] == "LIRF") & (va["flt_missing"] == 1)).to_numpy()
    assert np.array_equal(out["pred"].to_numpy()[~route], cb["pred"].to_numpy()[~route])


@pytest.mark.parametrize("name", ["lightgbm", "xgboost", "catboost", "routed_lightgbm",
                                  "routed_catboost"])
def test_learning_curve_recording_leaves_predictions_unchanged(name):
    """Day 5: recording a learning curve must not change the model. The last staged
    prediction equals the returned prediction, and routed rows hold their ridge value."""
    from prc import curves

    feats = synthetic(n=2000, seed=5)
    p = dict(PARAMS[name])
    rounds_key = "iterations" if "catboost" in name else "num_boost_round"
    p[rounds_key] = 25
    off = REGISTRY[name](feats, p, 42)["pred"].to_numpy()
    curves.start()
    on = REGISTRY[name](feats, p, 42)
    c = curves.take()
    assert np.array_equal(off, on["pred"].to_numpy())
    assert c["iterations"] == [1, 10, 20, 25] and len(c["train_rmse"]) == 25
    assert c["train_rmse"][-1] < c["train_rmse"][0]
    pos = {int(m): i for i, m in enumerate(c["ids"])}
    last = c["staged"][[pos[int(m)] for m in on["MVT_ID_mvt"]], -1]
    np.testing.assert_allclose(last, on["pred"].to_numpy(), rtol=1e-9, atol=1e-6)
    if name.startswith("routed"):
        va = feats.filter(pl.col("role") == "val")
        route = ((va["ADEP_mvt"] == "LIRF") & (va["flt_missing"] == 1)).to_numpy()
        rows = [pos[int(m)] for m in va["MVT_ID_mvt"].to_numpy()[route]]
        assert np.all(c["staged"][rows, 0] == c["staged"][rows, -1])
    assert curves.take() is None and not curves.active()
