"""Tier 1 gradient-boosting baselines (CPU). Fixed a-priori hyperparameters from the
proposal; no search, no early stopping on validation data."""

from __future__ import annotations

import polars as pl

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
    booster = lgb.train(p, ds, num_boost_round=rounds)
    return pl.DataFrame({"MVT_ID_mvt": va["MVT_ID_mvt"], "pred": booster.predict(x_va)})


def xgboost(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    import xgboost as xgb

    tr, va, x_tr, x_va, _ = _frames(feats)
    p = dict(params)
    rounds = p.pop("num_boost_round")
    p.update(seed=seed, tree_method="hist")
    dtr = xgb.DMatrix(x_tr, label=tr["y"].to_numpy(), enable_categorical=True)
    dva = xgb.DMatrix(x_va, enable_categorical=True)
    booster = xgb.train(p, dtr, num_boost_round=rounds)
    return pl.DataFrame({"MVT_ID_mvt": va["MVT_ID_mvt"], "pred": booster.predict(dva)})
