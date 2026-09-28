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


POPULATIONS = ("all", "NM_present", "LIRF_NM_missing", "excl_LIRF_NM_missing",
               "NM_present_excl_LIRF")


def population_mask(frame: pl.DataFrame, population: str) -> pl.Series:
    """Row mask of a named sub-population (needs ADEP_mvt and nm_missing)."""
    if population == "all":
        return pl.Series("m", [True] * frame.height)
    lirf_miss = (pl.col("ADEP_mvt") == "LIRF") & pl.col("nm_missing")
    expr = {"NM_present": ~pl.col("nm_missing"), "LIRF_NM_missing": lirf_miss,
            "excl_LIRF_NM_missing": ~lirf_miss,
            "NM_present_excl_LIRF": ~pl.col("nm_missing") & (pl.col("ADEP_mvt") != "LIRF")
            }[population]
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


def row_concentration(frame: pl.DataFrame, detail_cols: tuple[str, ...] = ()) -> dict:
    """Standing rule 6 on one fold's rows (columns y, pred_cand, pred_champ, MVT_ID_mvt):
    signed shares of the SSE change carried by the largest row and the 10 largest rows by
    |change|; the dominant row's details when one row carries >= 50 %."""
    d = frame.with_columns(((pl.col("pred_cand") - pl.col("y")) ** 2
                            - (pl.col("pred_champ") - pl.col("y")) ** 2).alias("d"))
    total = float(d["d"].sum())
    top = d.with_columns(pl.col("d").abs().alias("absd")).sort("absd", descending=True)
    rec = {"delta_sse": total,
           "top1_share": float(top["d"][0]) / total if total and top.height else None,
           "top10_share": float(top["d"][:10].sum()) / total if total and top.height else None}
    if rec["top1_share"] is not None and abs(rec["top1_share"]) >= 0.5:
        r = top.row(0, named=True)
        rec["dominant_row"] = {k: r[k] for k in ("MVT_ID_mvt", "y", "pred_cand", "pred_champ",
                                                 *detail_cols) if k in r}
    return rec
