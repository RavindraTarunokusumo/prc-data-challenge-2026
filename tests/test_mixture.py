"""Day 8: the convention mixture (prc.models.mixture) and its in-run override."""

import numpy as np
import polars as pl
import pytest

from prc import blending, curves
from prc.models.mixture import COMPONENT_COLUMNS, convention_label, convention_mixture
from prc.models.routed import route_mask
from tests.test_models import synthetic

PARAMS = {"convention_tolerance_s": 120,
          "classifier_params": {"learning_rate": 0.1, "num_leaves": 4, "min_data_in_leaf": 5,
                                "num_boost_round": 20},
          "normal_params": {"objective": "regression", "learning_rate": 0.1, "num_leaves": 4,
                            "min_data_in_leaf": 5, "num_boost_round": 20}}


def convention_frame(n=600, seed=3):
    """LIRF-heavy synthetic rows; half the LIRF NM-missing training rows are recorded at
    schedule (y = d_sched)."""
    feats = synthetic(n, seed).with_columns(
        pl.when(pl.col("MVT_ID_mvt") % 3 == 0).then(pl.lit("EDDF")).otherwise(pl.lit("LIRF"))
        .alias("ADEP_mvt"),
        (pl.col("MVT_ID_mvt") % 2).cast(pl.Int32).alias("flt_missing"),
        (pl.col("d_sched").abs() + 3600.0).alias("d_sched"))
    conv = (pl.col("role") == "train") & route_mask() & (pl.col("MVT_ID_mvt") % 4 == 1)
    return feats.with_columns(pl.when(conv).then(pl.col("d_sched")).otherwise(pl.col("y"))
                              .alias("y"))


def test_mixture_combines_its_components_on_the_subgroup_only():
    feats = convention_frame()
    out = convention_mixture(feats, PARAMS, 42)
    sub = feats.filter((pl.col("role") == "val") & route_mask())
    assert out.columns == COMPONENT_COLUMNS
    assert out.height == sub.height and set(out["MVT_ID_mvt"]) == set(sub["MVT_ID_mvt"])
    p, g, c = (out[k].to_numpy() for k in ("p_conv", "g_normal", "conv_component"))
    assert ((p > 0) & (p < 1)).all() and (c >= 0).all()
    assert np.allclose(out["pred"].to_numpy(), p * c + (1 - p) * g)
    tr = feats.filter((pl.col("role") == "train") & route_mask())
    rate = tr.select(convention_label(120).mean())[0, 0]
    assert np.allclose(out["p_train_rate"].to_numpy(), rate)
    assert np.allclose(c, np.maximum(out["d_sched"].to_numpy(), 0))
    again = convention_mixture(feats, PARAMS, 42)
    assert np.array_equal(out["pred"].to_numpy(), again["pred"].to_numpy())


def test_mixture_label_and_normal_rows_use_training_rows_only():
    feats = convention_frame()
    tr = feats.filter((pl.col("role") == "train") & route_mask())
    c = tr.select(convention_label(120))[:, 0]
    assert 0 < c.mean() < 1
    # Validation rows have no target, so their label is never true.
    va = feats.filter(pl.col("role") == "val").select(convention_label(120))[:, 0]
    assert not va.any()


def test_mixture_records_no_learning_curve():
    curves.start()
    convention_mixture(convention_frame(), PARAMS, 42)
    assert curves.active() and curves.take() is None


def test_mixture_refuses_a_one_class_subgroup():
    feats = convention_frame().with_columns(
        pl.when(pl.col("role") == "train").then(pl.col("d_sched")).otherwise(pl.col("y"))
        .alias("y"))
    with pytest.raises(ValueError, match="one class"):
        convention_mixture(feats, PARAMS, 42)


def test_override_fitted_swaps_exactly_the_subgroup(monkeypatch):
    ids = np.arange(1, 7, dtype=np.int64)
    val = pl.DataFrame({"MVT_ID_mvt": ids,
                        "ADEP_mvt": ["LIRF", "LIRF", "EDDF", "EDDF", "LIRF", "EGLL"],
                        "flt_missing": [1, 0, 1, 0, 1, 1]})
    monkeypatch.setattr(blending.ledger, "get", lambda eid: {"status": "COMPLETE"})
    load = lambda eid, fold: pl.DataFrame({"MVT_ID_mvt": ids[::-1], "pred": [1.0] * 6})
    params = {"base": "E900", "subgroup": "LIRF_NM_missing"}
    fitted = pl.DataFrame({"MVT_ID_mvt": [5, 1], "pred": [7.0, 9.0]})
    out = blending.override_fitted(val, params, "R1", fitted, loader=load).sort("MVT_ID_mvt")
    assert out["pred"].to_list() == [9.0, 1.0, 1.0, 1.0, 7.0, 1.0]
    with pytest.raises(ValueError, match="fitted rows differ"):
        blending.override_fitted(val, params, "R1", fitted.head(1), loader=load)
