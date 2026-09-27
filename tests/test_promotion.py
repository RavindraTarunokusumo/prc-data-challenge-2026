"""Frozen promotion rule (brief §10 criteria 1-3) on synthetic paired predictions."""

import datetime as dt

import numpy as np
import polars as pl
import pytest

from prc import metrics
from prc.splits import promotion_config

FOLDS = ["R1", "R2", "R3", "S1", "W1", "S1c", "W1c"]


def fold_frame(seed, n=3000):
    rng = np.random.default_rng(seed)
    t0 = dt.datetime(2025, 9, 1, tzinfo=dt.UTC)
    y = rng.gamma(4, 250, n)
    return pl.DataFrame({
        "MVT_ID_mvt": np.arange(n, dtype=np.int64),
        "TAXITIME_SEC_mvt": y,
        "ADEP_mvt": rng.choice(["EDDF", "EGLL", "LIRF"], n),
        "month": "2025-09",
        "WK_TBL_CAT_flt": "M",
        "MVT_TIME_UTC_mvt": [t0 + dt.timedelta(hours=int(h)) for h in rng.integers(0, 720, n)],
    })


def with_pred(df, err_sd, seed):
    rng = np.random.default_rng(seed)
    return df.with_columns(pl.Series("pred", df["TAXITIME_SEC_mvt"].to_numpy()
                                     + rng.normal(0, err_sd, df.height)))


def pair(cand_sd, champ_sd, override=None):
    cand, champ = {}, {}
    for i, f in enumerate(FOLDS):
        base = fold_frame(i)
        sd = (override or {}).get(f, cand_sd)
        champ[f] = with_pred(base, champ_sd, 200 + i)
        cand[f] = champ[f] if sd == "same" else with_pred(base, sd, 100 + i)
    return cand, champ


def test_clear_improvement_passes():
    r = metrics.promotion_check(*pair(200, 300))
    assert r["criterion_1"] and r["criterion_2"] and r["criterion_3"]
    assert all(o == "WIN" for o in r["fold_outcome"].values())


def test_identical_predictions_do_not_pass():
    cand, _ = pair(250, 250)
    r = metrics.promotion_check(cand, cand)
    assert not r["criterion_1"] and not r["criterion_2"]
    assert set(r["fold_outcome"].values()) == {"TIE"}


def test_seasonal_fold_must_win():
    r = metrics.promotion_check(*pair(200, 300, override={"S1": "same"}))
    assert r["fold_outcome"]["S1"] == "TIE" and not r["criterion_2"]


def test_twin_loss_demotes_seasonal_win():
    r = metrics.promotion_check(*pair(200, 300, override={"S1c": 450}))
    assert r["fold_outcome"]["S1"] == "WIN" and r["fold_outcome"]["S1c"] == "LOSS"
    assert r["fold_outcome_counted"]["S1"] == "TIE" and not r["criterion_2"]


def test_any_development_loss_blocks():
    r = metrics.promotion_check(*pair(200, 300, override={"R2": 450}))
    assert r["fold_outcome"]["R2"] == "LOSS" and not r["criterion_2"]


def test_missing_folds_rejected():
    cand, champ = pair(200, 300)
    del cand["W1c"]
    with pytest.raises(ValueError, match="missing folds"):
        metrics.promotion_check(cand, champ)


def test_bootstrap_is_deterministic_and_fold_set_independent():
    cand, champ = pair(200, 300)
    a = metrics.paired_bootstrap({"R1": (cand["R1"], champ["R1"])})
    b = metrics.paired_bootstrap({f: (cand[f], champ[f]) for f in FOLDS})
    assert np.array_equal(a["R1"]["draws"], b["R1"]["draws"])
    assert len(a["R1"]["draws"]) == promotion_config()["bootstrap"]["resamples"]
