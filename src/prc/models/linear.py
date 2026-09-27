"""Tier 0 linear baseline: ridge regression on one-hot categoricals and winsorised
numerics. Every fitted transform (quantile clips, fill values, scaling, vocabulary)
comes from the fold's training rows only."""

from __future__ import annotations

import numpy as np
import polars as pl
from scipy import sparse
from sklearn.linear_model import Ridge

from prc.features import columns


def ridge(feats: pl.DataFrame, params: dict, seed: int) -> pl.DataFrame:
    tr = feats.filter(pl.col("role") == "train")
    va = feats.filter(pl.col("role") == "val")
    lo_q, hi_q = params.get("winsor", [0.005, 0.995])
    cats, nums = columns(feats)

    def numeric_block(df, stats=None):
        cols, fitted = [], stats or {}
        for c in nums:
            x = df[c].cast(pl.Float64)
            if stats is None:
                lo, hi = tr[c].quantile(lo_q), tr[c].quantile(hi_q)
                clipped = tr[c].cast(pl.Float64).clip(lo, hi)
                fitted[c] = (lo, hi, clipped.median(), clipped.mean(), clipped.std() or 1.0)
            lo, hi, fill, mu, sd = fitted[c]
            v = x.clip(lo, hi).fill_null(fill).to_numpy()
            cols.append((v - mu) / sd)
            cols.append(x.is_null().cast(pl.Float64).to_numpy())
        return np.column_stack(cols), fitted

    vocab = {c: {v: i for i, v in enumerate(sorted(tr[c].unique().to_list()))}
             for c in cats}

    def onehot(df):
        blocks = []
        for c in cats:
            idx = np.array([vocab[c].get(v, -1) for v in df[c].to_list()])
            rows = np.nonzero(idx >= 0)[0]
            blocks.append(sparse.csr_matrix(
                (np.ones(len(rows)), (rows, idx[rows])), shape=(df.height, len(vocab[c]))))
        return sparse.hstack(blocks).tocsr()

    xn_tr, stats = numeric_block(tr)
    xn_va, _ = numeric_block(va, stats)
    x_tr = sparse.hstack([sparse.csr_matrix(xn_tr), onehot(tr)]).tocsr()
    x_va = sparse.hstack([sparse.csr_matrix(xn_va), onehot(va)]).tocsr()
    model = Ridge(alpha=params.get("alpha", 1.0), solver="auto", random_state=seed)
    model.fit(x_tr, tr["y"].to_numpy())
    return pl.DataFrame({"MVT_ID_mvt": va["MVT_ID_mvt"], "pred": model.predict(x_va)})
