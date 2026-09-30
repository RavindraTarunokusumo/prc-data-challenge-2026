import importlib.util
from pathlib import Path

import polars as pl

_spec = importlib.util.spec_from_file_location(
    "range_check", Path(__file__).resolve().parents[1] / "scripts" / "range_check.py")
rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rc)


def test_folds_exclude_holdout():
    assert rc.folds() == ["R1", "R2", "R3", "S1", "W1", "S1c", "W1c"]
    assert "H" not in rc.folds()


def _frame():
    # (ADEP, nm_missing, y, pred, d_sched)
    rows = [("EDDF", False, 900, -5, 0), ("EDDF", False, 900, 4000, 0),
            ("LIRF", False, 900, 3601, 0), ("EDDF", True, 900, -1, 4 * 3600),
            ("EDDF", True, 900, 3600, 6 * 3600), ("EDDF", True, 900, 5000, 6 * 3600),
            ("LIRF", True, 900, 9000, 6 * 3600), ("EDDF", True, 9000, 8000, 6 * 3600)]
    return pl.DataFrame(rows, schema=["ADEP_mvt", "nm_missing", "y", "pred", "d_sched"],
                        orient="row")


def test_count_fold():
    c = rc.count_fold(_frame())
    assert c["NM_present_other"] == {"bulk_rows": 2, "below_0": 1, "above_3600": 1}
    assert c["NM_present_LIRF"]["above_3600"] == 1
    assert c["NM_missing_other"] == {"bulk_rows": 3, "below_0": 1, "above_3600": 1}
    assert c["NM_missing_LIRF"]["above_3600"] == 1
    assert c["total"] == {"bulk_rows": 7, "below_0": 2, "above_3600": 4}  # tail row excluded


def test_by_dsched():
    b = rc.by_dsched(_frame())
    assert b[">5h"]["rows"] == 3 and b[">5h"]["oor_all_rows"] == 2
    assert b[">5h"]["bulk_rows"] == 2 and b[">5h"]["oor_bulk"] == 1
    assert b["3-5h"]["oor_all_rows"] == 1


def test_forward_counts_excludes_december():
    rows = [("2025-01", "EDDF", "DEP", None, 4 * 3600), ("2025-01", "LIRF", "DEP", None, 6 * 3600),
            ("2025-01", "EDDF", "DEP", 1, 6 * 3600), ("2025-01", "EDDF", "ARR", None, 6 * 3600),
            ("2025-12", "EDDF", "DEP", None, 6 * 3600), ("2026-01", "EDDF", "DEP", None, 6 * 3600)]
    df = pl.DataFrame(rows, schema=["month", "ADEP_mvt", "PHASE_mvt", "AOBT_3_flt", "d_sched"],
                      orient="row")
    r = rc.forward_counts(df)
    assert "2025-12" not in r["months_2025"]
    assert r["months_2025"]["2025-01"] == {
        "nm_missing": 2, "gt3h": 2, "gt5h": 1, "lirf_nm_missing": 1, "lirf_gt3h": 1,
        "lirf_gt5h": 1, "other_gt3h": 1, "other_gt5h": 0}
    assert r["ranking"]["2026-01"]["gt5h"] == 1 and r["ranking"]["2026-07"] is None
