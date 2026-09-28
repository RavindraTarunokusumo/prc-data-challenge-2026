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
