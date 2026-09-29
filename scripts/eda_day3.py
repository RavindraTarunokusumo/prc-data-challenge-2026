"""Day 3 descriptive EDA: congestion features (brief §11, Day 3).

    uv run python scripts/eda_day3.py

Target hygiene (as scripts/eda_day2.py): targets are read only for months that are never
a validation month of any frozen fold (FIT = Jan, Mar-Jun 2025; EVAL = Aug 2025). Feb,
Jul, Sep-Nov targets are not read; December targets are masked by load_silver. Congestion
features are target-free, so they are computed over Jan-Nov 2025 and over each ranking
month. Descriptive only: no model is fitted and no fold is scored.

Sections:
1. Masking invariance on real data: prc.congestion features computed from a view with DEP
   block times and targets nulled equal those from the unmasked view (all Jan-Nov rows).
2. Target-free distribution shift: per feature, quantiles in Jan/Jul 2025 against the
   ranking months Jan/Jul 2026 (each ranking month's view is that month plus 2025, as in
   SUBMIT_JAN / SUBMIT_JUL), and the share of rows in the first hour of a month.
3. Out-of-time signal: for each feature, the airport x decile conditional mean of a
   residual, fitted on FIT and applied to EVAL; reported as the RMSE reduction on EVAL
   bulk rows (y < 3600 s) for
     r_apt  = y - airport median                       (all rows),
     r_anch = y - (d_aobt3 + airport median of y - d_aobt3)   (NM-present rows).
   Deciles are FIT-quantiles per airport; unseen bins fall back to 0. `null` is the same
   procedure with a constant feature (airport mean only); `incremental_s` is a feature's
   reduction minus the null reduction.
Writes research/day-03/eda/congestion.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl

from prc.congestion import FEATURES, P_FEATURES, congestion
from prc.data import load_silver
from prc.paths import ROOT

FIT = ["2025-01", "2025-03", "2025-04", "2025-05", "2025-06"]
EVAL = ["2025-08"]
TRAIN_MONTHS = [f"2025-{m:02d}" for m in range(1, 12)]
BULK = 3600
OUT = ROOT / "research" / "day-03" / "eda" / "congestion.json"
QS = [0.05, 0.25, 0.5, 0.75, 0.95]


def view(s: pl.DataFrame, months: list[str], mask_dep: bool) -> pl.LazyFrame:
    lf = s.lazy().filter(pl.col("month").is_in(months))
    if mask_dep:
        hide = pl.col("PHASE_mvt") == "DEP"
        lf = lf.with_columns([pl.when(hide).then(None).otherwise(pl.col(c)).alias(c)
                              for c in ("BLOCK_TIME_UTC_mvt", "TAXITIME_SEC_mvt")])
    return lf


def quantiles(df: pl.DataFrame) -> dict:
    return {f: [float(df[f].quantile(q)) for q in QS] + [float(df[f].mean())]
            for f in FEATURES}


def binned_signal(fit: pl.DataFrame, ev: pl.DataFrame, feat: str, resid: str) -> dict:
    """RMSE of resid on EVAL before/after subtracting the FIT airport x decile mean."""
    edges = (fit.group_by("ADEP_mvt").agg(
        pl.col(feat).quantile(q).alias(f"q{i}") for i, q in enumerate(np.arange(.1, 1, .1))))

    def binned(df):
        d = df.join(edges, on="ADEP_mvt", how="left")
        b = sum((pl.col(feat) > pl.col(f"q{i}")).cast(pl.Int32) for i in range(9))
        return d.with_columns(b.alias("bin"))

    means = binned(fit).group_by("ADEP_mvt", "bin").agg(pl.col(resid).mean().alias("m"))
    e = binned(ev).join(means, on=["ADEP_mvt", "bin"], how="left").with_columns(
        pl.col("m").fill_null(0.0))
    r = e[resid].to_numpy()
    after = r - e["m"].to_numpy()
    return {"rmse_before": float(np.sqrt(np.mean(r**2))),
            "rmse_after": float(np.sqrt(np.mean(after**2))),
            "reduction_s": float(np.sqrt(np.mean(r**2)) - np.sqrt(np.mean(after**2))),
            "spearman_fit": float(fit.select(pl.corr(feat, resid, method="spearman")).item())}


def main() -> None:
    s = load_silver()
    out: dict = {"fit_months": FIT, "eval_months": EVAL, "bulk_max_s": BULK}

    # 1. masking invariance
    masked = congestion(view(s, TRAIN_MONTHS, True))
    unmasked = congestion(view(s, TRAIN_MONTHS, False))
    out["masking_invariance_jan_nov"] = {"rows": masked.height,
                                         "identical": bool(masked.equals(unmasked))}
    cg = masked

    # 2. target-free shift: 2025 same-month vs ranking months
    shift = {}
    for m25, m26, ctx in (("2025-01", "2026-01", TRAIN_MONTHS + ["2025-12"]),
                          ("2025-07", "2026-07", TRAIN_MONTHS + ["2025-12"])):
        rk = congestion(view(s, ctx + [m26], True))
        ids26 = s.filter(pl.col("month") == m26, pl.col("PHASE_mvt") == "DEP")["MVT_ID_mvt"]
        ids25 = s.filter(pl.col("month") == m25, pl.col("PHASE_mvt") == "DEP")["MVT_ID_mvt"]
        shift[m26] = {"rows": int(ids26.len()),
                      "ranking": quantiles(rk.filter(pl.col("MVT_ID_mvt").is_in(ids26))),
                      "same_month_2025": quantiles(cg.filter(pl.col("MVT_ID_mvt").is_in(ids25)))}
    dep = s.filter(pl.col("PHASE_mvt") == "DEP")
    first_hour = dep.select(
        ((pl.col("MVT_TIME_UTC_mvt").dt.day() == 1)
         & (pl.col("MVT_TIME_UTC_mvt").dt.hour() == 0)).mean()).item()
    shift["share_dep_rows_first_utc_hour_of_month"] = float(first_hour)
    out["distribution_shift"] = shift

    # 3. out-of-time signal on never-validation months
    base = (dep.filter(pl.col("month").is_in(FIT + EVAL))
            .select("MVT_ID_mvt", "ADEP_mvt", "month",
                    pl.col("TAXITIME_SEC_mvt").cast(pl.Float64).alias("y"),
                    (pl.col("MVT_TIME_UTC_mvt") - pl.col("AOBT_3_flt")).dt.total_seconds()
                    .cast(pl.Float64).alias("d_aobt3"))
            .join(cg, on="MVT_ID_mvt", how="inner", validate="1:1")
            .filter(pl.col("y") < BULK))
    fit = base.filter(pl.col("month").is_in(FIT))
    med = fit.group_by("ADEP_mvt").agg(pl.col("y").median().alias("med_y"),
                                       (pl.col("y") - pl.col("d_aobt3")).median().alias("med_a"))
    base = base.join(med, on="ADEP_mvt").with_columns(
        (pl.col("y") - pl.col("med_y")).alias("r_apt"),
        (pl.col("y") - pl.col("d_aobt3") - pl.col("med_a")).alias("r_anch"))
    fit, ev = base.filter(pl.col("month").is_in(FIT)), base.filter(pl.col("month").is_in(EVAL))
    nm_fit, nm_ev = fit.drop_nulls("r_anch"), ev.drop_nulls("r_anch")
    null = {r: binned_signal(a.with_columns(pl.lit(0.0).alias("__null__")),
                             b.with_columns(pl.lit(0.0).alias("__null__")), "__null__", r)
            for r, a, b in (("r_apt", fit, ev), ("r_anch", nm_fit, nm_ev))}
    out["null"] = null
    sig = {}
    for f in FEATURES:
        sig[f] = {"label": "P" if f in P_FEATURES else "T",
                  "r_apt": binned_signal(fit, ev, f, "r_apt"),
                  "r_anch": binned_signal(nm_fit, nm_ev, f, "r_anch")}
        for r in ("r_apt", "r_anch"):
            sig[f][r]["incremental_s"] = sig[f][r]["reduction_s"] - null[r]["reduction_s"]
    out["signal"] = sig
    out["rows"] = {"fit_bulk": fit.height, "eval_bulk": ev.height,
                   "fit_bulk_nm_present": nm_fit.height, "eval_bulk_nm_present": nm_ev.height}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({"null": null, "invariance": out["masking_invariance_jan_nov"],
                      "first_hour": first_hour}, indent=1))
    for f, v in sig.items():
        print(f"{f:22s} {v['label']}  r_apt {v['r_apt']['incremental_s']:7.2f} "
              f"(rho {v['r_apt']['spearman_fit']:+.2f})  r_anch {v['r_anch']['incremental_s']:7.2f} "
              f"(rho {v['r_anch']['spearman_fit']:+.2f})")


if __name__ == "__main__":
    main()
