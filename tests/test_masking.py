"""The validation masking protocol (DATASET_AUDIT §6.4) and holdout-target masking in the
data layer, on the real silver layer. December targets are never read."""

import polars as pl
import pytest

from prc.splits import BLANKED_DEP_COLS, get_fold, holdout_months, masked_view, train_targets

FOLDS = ["R1", "R2", "R3", "S1", "W1", "S1c", "W1c", "H", "SUBMIT_JAN", "SUBMIT_JUL"]


def test_load_silver_masks_holdout_targets(silver):
    hold = silver.filter(pl.col("month").is_in(list(holdout_months()))
                         & (pl.col("PHASE_mvt") == "DEP"))
    assert hold.height > 0
    for c in BLANKED_DEP_COLS:
        assert hold[c].null_count() == hold.height


@pytest.mark.parametrize("fold_id", FOLDS)
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
    # Training DEP rows keep their target, except protected-holdout months (masked in silver).
    tr_dep = v.filter((pl.col("role") == "train") & (pl.col("PHASE_mvt") == "DEP")
                      & ~pl.col("month").is_in(list(holdout_months())))
    assert tr_dep["TAXITIME_SEC_mvt"].null_count() == 0


@pytest.mark.parametrize("fold_id", ["R1", "S1", "W1", "S1c", "W1c"])
def test_excluded_months_absent(silver, fold_id):
    fold = get_fold(fold_id)
    months = set(masked_view(silver, fold).collect()["month"].unique())
    assert not months & set(holdout_months())
    assert not months & set(fold.embargo_months)
    assert months == set(fold.months)


def test_train_targets_only_training_months(silver):
    fold = get_fold("S1")
    t = train_targets(silver, fold).collect()
    assert set(t["month"].unique()) == set(fold.train_months)
    assert (t["PHASE_mvt"] == "DEP").all()
