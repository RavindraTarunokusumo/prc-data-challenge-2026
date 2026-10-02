"""Tier 1 gradient-boosting baselines (CPU). Fixed a-priori hyperparameters from the
proposal; no search, no early stopping on validation data."""

from __future__ import annotations

import numpy as np
import polars as pl

from prc import curves
from prc.features import columns


def _frames(feats: pl.DataFrame):
    tr = feats.filter(pl.col("role") == "train")
    va = feats.filter(pl.col("role") == "val")
    cats, nums = columns(feats)
    # Category vocabulary from the training rows; unseen validation levels become null.
    enums = {c: pl.Enum(sorted(tr[c].unique().to_list())) for c in cats}

    def to_pandas(df):
        out = df.select(
            [pl.col(c).replace_strict(list(enums[c].categories), list(enums[c].categories),
                                      default=None).cast(enums[c]) for c in cats]
            + [pl.col(c).cast(pl.Float64) for c in nums]
        ).to_pandas()
        return out[cats + nums]

    return tr, va, to_pandas(tr), to_pandas(va), cats


def lightgbm(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    import lightgbm as lgb

    tr, va, x_tr, x_va, cats = _frames(feats)
    p = dict(params)
    rounds = p.pop("num_boost_round")
    p.update(seed=seed, deterministic=True, force_row_wise=True, verbosity=-1)
    ds = lgb.Dataset(x_tr, label=tr["y"].to_numpy(), categorical_feature=cats)
    if not curves.active():
        booster = lgb.train(p, ds, num_boost_round=rounds)
        return pl.DataFrame({"MVT_ID_mvt": va["MVT_ID_mvt"], "pred": booster.predict(x_va)})
    # Learning curve: the training set as its own (training-metric) eval set; the default
    # regression metric is l2. Trees are unchanged (tests/test_models.py).
    evals: dict = {}
    booster = lgb.train(p, ds, num_boost_round=rounds, valid_sets=[ds], valid_names=["train"],
                        callbacks=[lgb.record_evaluation(evals)])
    iters = curves.grid(rounds)
    staged, acc, prev = np.empty((va.height, len(iters))), np.zeros(va.height), 0
    for j, k in enumerate(iters):  # tree-range sums: about one extra predict in total
        acc = acc + booster.predict(x_va, start_iteration=prev, num_iteration=k - prev)
        staged[:, j], prev = acc, k
    curves.record("lightgbm", np.sqrt(evals["train"]["l2"]), va["MVT_ID_mvt"].to_numpy(),
                  iters, staged)
    return pl.DataFrame({"MVT_ID_mvt": va["MVT_ID_mvt"], "pred": booster.predict(x_va)})


def xgboost(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    import xgboost as xgb

    tr, va, x_tr, x_va, _ = _frames(feats)
    p = dict(params)
    rounds = p.pop("num_boost_round")
    p.update(seed=seed, tree_method="hist")
    dtr = xgb.DMatrix(x_tr, label=tr["y"].to_numpy(), enable_categorical=True)
    dva = xgb.DMatrix(x_va, enable_categorical=True)
    if not curves.active():
        booster = xgb.train(p, dtr, num_boost_round=rounds)
        return pl.DataFrame({"MVT_ID_mvt": va["MVT_ID_mvt"], "pred": booster.predict(dva)})
    evals: dict = {}
    booster = xgb.train({**p, "eval_metric": "rmse"}, dtr, num_boost_round=rounds,
                        evals=[(dtr, "train")], evals_result=evals, verbose_eval=False)
    iters = curves.grid(rounds)
    staged = np.column_stack([booster.predict(dva, iteration_range=(0, k)) for k in iters])
    curves.record("xgboost", evals["train"]["rmse"], va["MVT_ID_mvt"].to_numpy(), iters, staged)
    return pl.DataFrame({"MVT_ID_mvt": va["MVT_ID_mvt"], "pred": booster.predict(dva)})


NULL_CAT = "__NULL__"


def catboost(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    """CatBoost on the same columns and category vocabulary as `lightgbm`.

    `cat_mode` (popped from params; default "ctr"):
    - "ctr": categoricals go in as strings (unseen/null levels -> "__NULL__") and CatBoost
      builds its categorical statistics (CTRs) from them;
    - "codes" (Day 5): the same columns go in as the integer codes of the training
      vocabulary (sorted levels; unseen/null -> NaN), split as ordered numerics, so no
      categorical statistic exists. Everything else in the fit is identical.
    """
    from catboost import CatBoostRegressor, Pool

    tr, va, x_tr, x_va, cats = _frames(feats)
    p = dict(params)
    mode = p.pop("cat_mode", "ctr")
    if mode not in ("ctr", "codes"):
        raise ValueError(f"cat_mode must be 'ctr' or 'codes', got {mode!r}")

    def prep(x):
        x = x.copy()
        for c in cats:
            if mode == "ctr":
                x[c] = x[c].astype(object).where(x[c].notna(), NULL_CAT).astype(str)
            else:
                x[c] = x[c].cat.codes.astype("float64").replace(-1, np.nan)
        return x

    cat_features = cats if mode == "ctr" else []
    p.update(random_seed=seed, allow_writing_files=False, verbose=False)
    model = CatBoostRegressor(**p)
    model.fit(Pool(prep(x_tr), label=tr["y"].to_numpy(), cat_features=cat_features))
    pool_va = Pool(prep(x_va), cat_features=cat_features)
    pred = model.predict(pool_va)
    curves.note_params({"cat_mode": mode, "n_cat_features": len(cat_features),
                        **model.get_all_params()})
    if curves.active():  # CatBoost records the learn RMSE per iteration by default
        n = model.tree_count_
        iters = curves.grid(n)  # 1, then staged_predict's STEP multiples and the last tree
        staged = np.column_stack([model.predict(pool_va, ntree_end=1),
                                  *model.staged_predict(pool_va, eval_period=curves.STEP)])
        learn = model.get_evals_result().get("learn", {}).get("RMSE", [])
        curves.record("catboost", learn, va["MVT_ID_mvt"].to_numpy(), iters, staged)
    return pl.DataFrame({"MVT_ID_mvt": va["MVT_ID_mvt"], "pred": pred})
