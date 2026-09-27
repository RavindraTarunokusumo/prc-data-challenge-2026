"""The validation masking protocol (DATASET_AUDIT §6.4) on the real silver layer."""

import polars as pl
import pytest

from prc.splits import BLANKED_DEP_COLS, get_fold, masked_view, train_targets


@pytest.mark.parametrize("fold_id", ["R1", "R2", "R3", "S1", "H", "SUBMIT"])
def test_masked_view_hides_validation_dep_targets(silver, fold_id):
    fold = get_fold(fold_id)
    v = masked_view(silver, fold).collect()
    assert set(v["month"].unique()) <= set(fold.months)
    val_dep = v.filter((pl.col("role") == "val") & (pl.col("PHASE_mvt") == "DEP"))
    assert val_dep.height > 0
    for c in BLANKED_DEP_COLS:
        assert val_dep[c].null_count() == val_dep.height
    # ARR rows of validation months are left untouched, as in the ranking file.
    val_arr = v.filter((pl.col("role") == "val") & (pl.col("PHASE_mvt") == "ARR"))
    src_arr = silver.filter(pl.col("month").is_in(list(fold.val_months))
                            & (pl.col("PHASE_mvt") == "ARR"))
    assert val_arr.height == src_arr.height
    assert val_arr["TAXITIME_SEC_mvt"].null_count() == src_arr["TAXITIME_SEC_mvt"].null_count()
    # Training DEP rows keep their target.
    tr_dep = v.filter((pl.col("role") == "train") & (pl.col("PHASE_mvt") == "DEP"))
    assert tr_dep["TAXITIME_SEC_mvt"].null_count() == 0


@pytest.mark.parametrize("fold_id", ["R1", "S1"])
def test_excluded_months_absent(silver, fold_id):
    fold = get_fold(fold_id)
    v = masked_view(silver, fold).collect()
    assert "2025-12" not in set(v["month"].unique())
    for m in fold.embargo_months:
        assert m not in set(v["month"].unique())


def test_train_targets_only_training_months(silver):
    fold = get_fold("S1")
    t = train_targets(silver, fold).collect()
    assert set(t["month"].unique()) == set(fold.train_months)
    assert (t["PHASE_mvt"] == "DEP").all()
