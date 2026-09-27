import pytest

from prc.splits import SECTIONS, development_folds, get_fold, holdout_months, load_splits


def all_fold_ids():
    cfg = load_splits()
    return [fid for s in SECTIONS for fid in cfg[s]]


def test_all_folds_parse_and_are_disjoint():
    for fid in all_fold_ids():
        f = get_fold(fid)
        assert not set(f.train_months) & set(f.val_months)
        assert not set(f.embargo_months) & set(f.months)


def test_holdout_month_never_used_by_development_or_diagnostic_folds():
    cfg = load_splits()
    for fid in [*cfg["development_folds"], *cfg["diagnostic_folds"]]:
        assert not set(holdout_months()) & set(get_fold(fid).months), fid


def test_rolling_and_causal_twins_train_strictly_before_validation():
    for fid in ("R1", "R2", "R3", "S1c", "W1c"):
        f = get_fold(fid)
        assert max(f.train_months) < min(f.val_months), fid


def test_twins_share_validation_months():
    cfg = load_splits()
    for fold, twin in cfg["promotion"]["causal_twins"].items():
        assert get_fold(fold).val_months == get_fold(twin).val_months
        assert cfg["diagnostic_folds"][twin]["twin_of"] == fold


def test_seasonal_and_winter_folds():
    assert get_fold("S1").val_months == ("2025-07",) and "2025-08" in get_fold("S1").embargo_months
    assert get_fold("W1").val_months == ("2025-02",) and "2025-03" in get_fold("W1").embargo_months
    assert development_folds() == ("R1", "R2", "R3", "S1", "W1")


def test_final_folds_never_mix_ranking_months():
    assert get_fold("SUBMIT_JAN").months.count("2026-07") == 0
    assert get_fold("SUBMIT_JUL").months.count("2026-01") == 0


def test_every_scored_fold_has_a_pinned_population():
    cfg = load_splits()
    pinned = cfg["evaluation_population"]["eval_rows"]
    for fid in [*cfg["development_folds"], *cfg["diagnostic_folds"], *cfg["protected_holdout"]]:
        assert fid in pinned


def test_unknown_fold():
    with pytest.raises(KeyError):
        get_fold("X9")
