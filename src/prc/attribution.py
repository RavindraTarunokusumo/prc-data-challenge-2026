"""Attribution helpers for comparisons (not frozen; attribution only, never an outcome).

Standing rule 7 (X-D01-S01-0004): per fold, SSE-change shares and bulk dRMSE by NM status
(AOBT_3 present / missing) x LIRF vs the other nine airports.
"""

from __future__ import annotations

import numpy as np
import polars as pl

BULK_MAX_S = 3600  # same value as the frozen prc.metrics.BULK_MAX_S
SUBGROUPS = ("NM_present_other", "NM_present_LIRF", "NM_missing_other", "NM_missing_LIRF")


def _drmse(ea: np.ndarray, eb: np.ndarray) -> float | None:
    return float(np.sqrt(ea.mean()) - np.sqrt(eb.mean())) if ea.size else None


POPULATIONS = ("all", "NM_present", "LIRF_NM_missing", "excl_LIRF_NM_missing")


def population_mask(frame: pl.DataFrame, population: str) -> pl.Series:
    """Row mask of a named sub-population (needs ADEP_mvt and nm_missing)."""
    if population == "all":
        return pl.Series("m", [True] * frame.height)
    lirf_miss = (pl.col("ADEP_mvt") == "LIRF") & pl.col("nm_missing")
    expr = {"NM_present": ~pl.col("nm_missing"), "LIRF_NM_missing": lirf_miss,
            "excl_LIRF_NM_missing": ~lirf_miss}[population]
    return frame.select(expr.alias("m"))["m"]


def subgroup_disclosure(frame: pl.DataFrame) -> dict:
    """`frame`: one fold's rows with columns y, pred_cand, pred_champ, ADEP_mvt, nm_missing.

    Returns per subgroup: rows, tail rows, share of the fold's SSE change (same sign as the
    total = a positive share), full and bulk dRMSE (candidate - champion)."""
    y = frame["y"].to_numpy().astype(np.float64)
    ea = (frame["pred_cand"].to_numpy() - y) ** 2
    eb = (frame["pred_champ"].to_numpy() - y) ** 2
    d = ea - eb
    total = float(d.sum())
    lirf = (frame["ADEP_mvt"] == "LIRF").to_numpy()
    miss = frame["nm_missing"].to_numpy().astype(bool)
    bulk = y < BULK_MAX_S
    out = {}
    for name, m in (("NM_present_other", ~miss & ~lirf), ("NM_present_LIRF", ~miss & lirf),
                    ("NM_missing_other", miss & ~lirf), ("NM_missing_LIRF", miss & lirf)):
        mb = m & bulk
        out[name] = {
            "rows": int(m.sum()),
            "tail_rows": int((m & ~bulk).sum()),
            "share_of_sse_change": float(d[m].sum() / total) if total else None,
            "share_of_sse_change_tail": float(d[m & ~bulk].sum() / total) if total else None,
            "share_of_sse_change_bulk": float(d[mb].sum() / total) if total else None,
            "delta_rmse_full": _drmse(ea[m], eb[m]),
            "delta_rmse_bulk": _drmse(ea[mb], eb[mb]),
        }
    nm = ~miss
    out["NM_present_all"] = {"rows": int(nm.sum()),
                             "delta_rmse_full": _drmse(ea[nm], eb[nm]),
                             "delta_rmse_bulk": _drmse(ea[nm & bulk], eb[nm & bulk])}
    out["pooled"] = {"delta_rmse_full": _drmse(ea, eb),
                     "delta_rmse_bulk": _drmse(ea[bulk], eb[bulk])}
    signs = {np.sign(v["delta_rmse_bulk"]) for k, v in out.items()
             if k in SUBGROUPS and v["delta_rmse_bulk"] is not None and v["rows"] >= 1}
    out["bulk_sign_disagreement"] = len(signs - {0.0}) > 1
    return out
