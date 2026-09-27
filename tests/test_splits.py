import pytest

from prc.splits import DEVELOPMENT, get_fold, load_splits


def test_all_folds_parse_and_are_disjoint():
    cfg = load_splits()
    for section in ("development_folds", "protected_holdout", "final"):
        for fid in cfg[section]:
            f = get_fold(fid)
            assert not set(f.train_months) & set(f.val_months)
            assert not set(f.embargo_months) & set(f.months)


def test_holdout_month_never_used_by_development_folds():
    holdout = set(get_fold("H").val_months)
    for fid in DEVELOPMENT:
        assert not holdout & set(get_fold(fid).months)


def test_rolling_folds_train_strictly_before_validation():
    for fid in ("R1", "R2", "R3"):
        f = get_fold(fid)
        assert max(f.train_months) < min(f.val_months)


def test_seasonal_fold_validates_july_with_embargo():
    f = get_fold("S1")
    assert f.val_months == ("2025-07",) and "2025-08" in f.embargo_months


def test_unknown_fold():
    with pytest.raises(KeyError):
        get_fold("X9")
