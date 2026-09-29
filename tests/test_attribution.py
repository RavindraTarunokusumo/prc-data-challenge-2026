"""Standing rule 7 subgroup disclosure (synthetic data; attribution only)."""

import numpy as np
import polars as pl
import pytest

from prc.attribution import subgroup_disclosure


def test_subgroup_shares_sum_to_one_and_signs():
    frame = pl.DataFrame({
        "y": [500.0, 600.0, 5000.0, 700.0, 800.0, 6000.0],
        "pred_cand": [510.0, 590.0, 4000.0, 900.0, 800.0, 6000.0],
        "pred_champ": [600.0, 700.0, 1000.0, 700.0, 800.0, 1000.0],
        "ADEP_mvt": ["EDDF", "EDDF", "LIRF", "LIRF", "EGLL", "LIRF"],
        "nm_missing": [False, False, True, True, True, False],
    })
    out = subgroup_disclosure(frame)
    shares = [out[g]["share_of_sse_change"] for g in
              ("NM_present_other", "NM_present_LIRF", "NM_missing_other", "NM_missing_LIRF")]
    assert sum(shares) == pytest.approx(1.0)
    for g in ("NM_present_other", "NM_present_LIRF", "NM_missing_other", "NM_missing_LIRF"):
        assert out[g]["share_of_sse_change_tail"] + out[g]["share_of_sse_change_bulk"] == \
            pytest.approx(out[g]["share_of_sse_change"])
    assert out["NM_missing_LIRF"]["rows"] == 2 and out["NM_missing_LIRF"]["tail_rows"] == 1
    # bulk: candidate better at EDDF, worse on the LIRF NM-missing bulk row
    assert out["NM_present_other"]["delta_rmse_bulk"] < 0
    assert out["NM_missing_LIRF"]["delta_rmse_bulk"] == pytest.approx(200.0)
    assert out["NM_missing_other"]["delta_rmse_bulk"] == 0.0
    assert out["NM_present_LIRF"]["delta_rmse_bulk"] is None  # only a tail row
    assert out["bulk_sign_disagreement"] is True
    assert out["pooled"]["delta_rmse_full"] == pytest.approx(
        np.sqrt(((frame["pred_cand"] - frame["y"]) ** 2).mean())
        - np.sqrt(((frame["pred_champ"] - frame["y"]) ** 2).mean()))


def test_population_masks():
    from prc.attribution import population_mask
    f = pl.DataFrame({"ADEP_mvt": ["LIRF", "LIRF", "EDDF", "EDDF"],
                      "nm_missing": [True, False, True, False]})
    assert population_mask(f, "NM_present").to_list() == [False, True, False, True]
    assert population_mask(f, "LIRF_NM_missing").to_list() == [True, False, False, False]
    assert population_mask(f, "excl_LIRF_NM_missing").to_list() == [False, True, True, True]
    assert population_mask(f, "all").to_list() == [True] * 4
    assert population_mask(f, "NM_present_excl_LIRF").to_list() == [False, False, False, True]


def test_row_concentration_dominant_row():
    from prc.attribution import row_concentration
    f = pl.DataFrame({"MVT_ID_mvt": [1, 2, 3], "y": [100.0, 100.0, 87000.0],
                      "pred_cand": [110.0, 90.0, 20000.0], "pred_champ": [100.0, 100.0, 1000.0],
                      "ADEP_mvt": ["LIRF"] * 3})
    rc = row_concentration(f, ("ADEP_mvt",))
    assert rc["top1_share"] == pytest.approx(1.0, abs=1e-6)
    assert rc["dominant_row"]["MVT_ID_mvt"] == 3 and rc["dominant_row"]["ADEP_mvt"] == "LIRF"
    even = pl.DataFrame({"MVT_ID_mvt": [1, 2, 3], "y": [100.0] * 3,
                         "pred_cand": [110.0] * 3, "pred_champ": [100.0] * 3})
    rc2 = row_concentration(even)  # three equal rows: top1 share 1/3
    assert "dominant_row" not in rc2
