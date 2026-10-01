"""Standing rule 12: out-of-range predictions and forward support (disclosure only).

    uv run python scripts/range_check.py EXP [EXP2 ...] [--by-dsched] [--json PATH]
    uv run python scripts/range_check.py EXP [EXP2 ...] --bands [--json PATH]
    uv run python scripts/range_check.py --forward [--json PATH]

Mode 1 counts, per experiment and fold in FOLDS (R1,R2,R3,S1,W1,S1c,W1c; never H), the
predictions < 0 s and > 3,600 s on bulk rows (y < 3,600 s), by the four rule-7 subgroups
(NM status x LIRF, prc.attribution definitions) and in total. Truth comes only through
prc.evaluate.truth_frame, which refuses holdout/final folds.

--bands adds, per experiment, the sum over the five development folds (R1,R2,R3,S1,W1) of
out-of-range predictions on bulk rows of NM_missing_other by d_sched band (<1h incl. negative,
1-3h, >3h), as below0/above3600/total plus bulk-row counts, under the key "bands_dev5".

Mode 2 (--forward) is target-free: per ranking month and per 2025 month except December
(holdout month), the DEP NM-missing rows with d_sched > 3 h and > 5 h, split LIRF / other.
No target column is read. Changes no fold outcome or frozen criterion.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl

from prc import ledger
from prc.attribution import SUBGROUPS, population_mask
from prc.data import load_silver
from prc.evaluate import _join, _predictions, truth_frame
from prc.features import _secs
from prc.metrics import BULK_MAX_S, PRED, TARGET
from prc.splits import promotion_config

UPPER_S = 3600.0
FORWARD_MONTHS = ("2026-01", "2026-07")
HOLDOUT_MONTH = "2025-12"
H3, H5 = 3 * 3600, 5 * 3600
DSCHED_BINS = (("<1h", -np.inf, 3600.0), ("1-3h", 3600.0, 3 * 3600.0),
               ("3-5h", 3 * 3600.0, 5 * 3600.0), (">5h", 5 * 3600.0, np.inf))


def folds() -> list[str]:
    cfg = promotion_config()
    return list(cfg["development_folds"]) + list(cfg["causal_twins"].values())


def subgroup_masks(adep: pl.Series, nm_missing: pl.Series) -> dict[str, np.ndarray]:
    """Rule-7 subgroup masks, derived from prc.attribution.population_mask."""
    fr = pl.DataFrame({"ADEP_mvt": adep, "nm_missing": nm_missing})
    present = population_mask(fr, "NM_present").to_numpy()
    present_other = population_mask(fr, "NM_present_excl_LIRF").to_numpy()
    lirf_miss = population_mask(fr, "LIRF_NM_missing").to_numpy()
    return {"NM_present_other": present_other, "NM_present_LIRF": present & ~present_other,
            "NM_missing_other": ~present & ~lirf_miss, "NM_missing_LIRF": lirf_miss}


def count_fold(frame: pl.DataFrame) -> dict:
    """frame: y, pred, ADEP_mvt, nm_missing (+ d_sched when by-dsched wanted)."""
    y = frame["y"].to_numpy().astype(np.float64)
    p = frame["pred"].to_numpy().astype(np.float64)
    bulk = y < BULK_MAX_S
    lo, hi = p < 0, p > UPPER_S
    out = {}
    masks = subgroup_masks(frame["ADEP_mvt"], frame["nm_missing"])
    for name in SUBGROUPS:
        m = masks[name] & bulk
        out[name] = {"bulk_rows": int(m.sum()), "below_0": int((lo & m).sum()),
                     "above_3600": int((hi & m).sum())}
    out["total"] = {"bulk_rows": int(bulk.sum()), "below_0": int((lo & bulk).sum()),
                    "above_3600": int((hi & bulk).sum())}
    return out


def by_dsched(frame: pl.DataFrame) -> dict:
    """NM-missing non-LIRF rows: out-of-range share per d_sched bin. Two definitions:
    bulk_only (bulk rows, pred<0 or >3600) and all_rows (any row, pred<0 or >3600)."""
    y = frame["y"].to_numpy().astype(np.float64)
    p = frame["pred"].to_numpy().astype(np.float64)
    d = frame["d_sched"].to_numpy().astype(np.float64)
    sel = subgroup_masks(frame["ADEP_mvt"], frame["nm_missing"])["NM_missing_other"]
    oor = (p < 0) | (p > UPPER_S)
    bulk = y < BULK_MAX_S
    out = {}
    for name, a, b in DSCHED_BINS:
        m = sel & (d >= a) & (d < b)
        mb = m & bulk
        out[name] = {
            "rows": int(m.sum()), "oor_all_rows": int((m & oor).sum()),
            "share_all_rows": float((m & oor).sum() / m.sum()) if m.any() else None,
            "above_3600_all_rows": int((m & (p > UPPER_S)).sum()),
            "share_above_3600_all_rows": float((m & (p > UPPER_S)).sum() / m.sum())
            if m.any() else None,
            "bulk_rows": int(mb.sum()), "oor_bulk": int((mb & oor).sum()),
            "share_bulk": float((mb & oor).sum() / mb.sum()) if mb.any() else None,
        }
    return out


BAND_BINS = (("<1h", -np.inf, 3600.0), ("1-3h", 3600.0, 3 * 3600.0), (">3h", 3 * 3600.0, np.inf))


def band_counts(frame: pl.DataFrame) -> dict:
    """NM_missing_other bulk rows (y<3600): per d_sched band, bulk rows and predictions
    <0 / >3600 (total = sum)."""
    y = frame["y"].to_numpy().astype(np.float64)
    p = frame["pred"].to_numpy().astype(np.float64)
    d = frame["d_sched"].to_numpy().astype(np.float64)
    sel = subgroup_masks(frame["ADEP_mvt"], frame["nm_missing"])["NM_missing_other"] & (
        y < BULK_MAX_S)
    out = {}
    for name, a, b in BAND_BINS:
        m = sel & (d >= a) & (d < b)
        lo, hi = int((m & (p < 0)).sum()), int((m & (p > UPPER_S)).sum())
        out[name] = {"bulk_rows": int(m.sum()), "below_0": lo, "above_3600": hi,
                     "total": lo + hi}
    return out


def sum_bands(per_fold: list[dict]) -> dict:
    return {b: {k: sum(f[b][k] for f in per_fold) for k in per_fold[0][b]}
            for b, _, _ in BAND_BINS}


def baseline(eids: list[str], with_dsched: bool, with_bands: bool = False) -> dict:
    cols = ["MVT_ID_mvt", "AOBT_3_flt", "MVT_TIME_UTC_mvt", "SCHED_TIME_UTC_mvt", "PHASE_mvt",
            "month"]
    silver = load_silver(columns=cols).filter(pl.col("PHASE_mvt") == "DEP")
    aux = silver.select("MVT_ID_mvt", pl.col("AOBT_3_flt").is_null().alias("nm_missing"),
                        _secs(pl.col("MVT_TIME_UTC_mvt"),
                              pl.col("SCHED_TIME_UTC_mvt")).alias("d_sched"))
    res: dict = {}
    dev5 = list(promotion_config()["development_folds"])
    for eid in eids:
        rec = ledger.get(eid)
        if rec is None or rec["status"] != "COMPLETE":
            sys.exit(f"refused: {eid} is not COMPLETE in the ledger")
        res[eid] = {}
        bands = []
        for f in folds():
            j = _join(_predictions(eid, f), truth_frame(f)).join(aux, on="MVT_ID_mvt",
                                                                 how="left")
            j = j.with_columns(pl.col(TARGET).cast(pl.Float64).alias("y"),
                               pl.col(PRED).alias("pred"))
            res[eid][f] = count_fold(j)
            if with_dsched:
                res[eid][f]["NM_missing_other_by_dsched"] = by_dsched(j)
            if with_bands and f in dev5:
                bands.append(band_counts(j))
        if with_bands:
            res[eid]["bands_dev5"] = sum_bands(bands)
    return res


def forward_counts(df: pl.DataFrame) -> dict:
    """df: month, ADEP_mvt, PHASE_mvt, AOBT_3_flt, d_sched. Target-free; December excluded."""
    d = df.filter((pl.col("PHASE_mvt") == "DEP") & (pl.col("month") != HOLDOUT_MONTH)
                  & pl.col("AOBT_3_flt").is_null())
    lirf = pl.col("ADEP_mvt") == "LIRF"
    g = d.group_by("month").agg(
        pl.len().alias("nm_missing"),
        (pl.col("d_sched") > H3).sum().alias("gt3h"),
        (pl.col("d_sched") > H5).sum().alias("gt5h"),
        (lirf).sum().alias("lirf_nm_missing"),
        (lirf & (pl.col("d_sched") > H3)).sum().alias("lirf_gt3h"),
        (lirf & (pl.col("d_sched") > H5)).sum().alias("lirf_gt5h"),
        (~lirf & (pl.col("d_sched") > H3)).sum().alias("other_gt3h"),
        (~lirf & (pl.col("d_sched") > H5)).sum().alias("other_gt5h"),
    ).sort("month")
    months = {r["month"]: {k: int(v) for k, v in r.items() if k != "month"}
              for r in g.iter_rows(named=True)}
    m25 = {m: v for m, v in months.items() if m.startswith("2025-")}
    keys = ("nm_missing", "gt3h", "gt5h", "lirf_nm_missing", "lirf_gt3h", "lirf_gt5h",
            "other_gt3h", "other_gt5h")
    rng = {k: {"min": min(v[k] for v in m25.values()), "max": max(v[k] for v in m25.values())}
           for k in keys} if m25 else {}
    return {"months_2025": m25, "range_2025": rng,
            "ranking": {m: months.get(m) for m in FORWARD_MONTHS}}


def forward() -> dict:
    cols = ["AOBT_3_flt", "MVT_TIME_UTC_mvt", "SCHED_TIME_UTC_mvt", "PHASE_mvt", "month",
            "ADEP_mvt"]
    df = load_silver(columns=cols).with_columns(
        _secs(pl.col("MVT_TIME_UTC_mvt"), pl.col("SCHED_TIME_UTC_mvt")).alias("d_sched"))
    return forward_counts(df)


def print_baseline(res: dict) -> None:
    for eid, per in res.items():
        print(f"\n{eid}: predictions <0 / >3600 on bulk rows (y<3600)")
        print(f"{'fold':5}" + "".join(f"{s:>22}" for s in (*SUBGROUPS, "total")))
        for f, c in per.items():
            if f == "bands_dev5":
                continue
            cells = [f"{c[s]['below_0']}/{c[s]['above_3600']} of {c[s]['bulk_rows']}"
                     for s in (*SUBGROUPS, "total")]
            print(f"{f:5}" + "".join(f"{x:>22}" for x in cells))
        if "bands_dev5" in per:
            print("  5-dev-fold sum, NM_missing_other bulk rows, below0/above3600 (total) | rows:")
            for b, v in per["bands_dev5"].items():
                print(f"    {b:5} {v['below_0']}/{v['above_3600']} ({v['total']}) | "
                      f"{v['bulk_rows']}")
        for f, c in per.items():
            if f != "bands_dev5" and "NM_missing_other_by_dsched" in c:
                print(f"  {f} NM_missing_other by d_sched (share OOR all rows | >3600 only | "
                      "bulk-only):")
                for b, v in c["NM_missing_other_by_dsched"].items():
                    def s(x):
                        return "n/a" if x is None else f"{100 * x:.1f}%"
                    print(f"    {b:5} n={v['rows']:6} {s(v['share_all_rows']):>7} "
                          f"{s(v['share_above_3600_all_rows']):>7} {s(v['share_bulk']):>7}")


def print_forward(r: dict) -> None:
    print("\nNM-missing DEP rows (target-free; December excluded)")
    hdr = f"{'month':8}{'miss':>6}{'>3h':>6}{'>5h':>6}{'LIRF':>6}{'L>3h':>6}{'L>5h':>6}" \
          f"{'O>3h':>6}{'O>5h':>6}"
    print(hdr)
    keys = ("nm_missing", "gt3h", "gt5h", "lirf_nm_missing", "lirf_gt3h", "lirf_gt5h",
            "other_gt3h", "other_gt5h")
    for m, v in r["months_2025"].items():
        print(f"{m:8}" + "".join(f"{v[k]:>6}" for k in keys))
    print(f"{'2025 min':8}" + "".join(f"{r['range_2025'][k]['min']:>6}" for k in keys))
    print(f"{'2025 max':8}" + "".join(f"{r['range_2025'][k]['max']:>6}" for k in keys))
    for m, v in r["ranking"].items():
        print(f"{m:8}" + "".join(f"{v[k]:>6}" for k in keys))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("experiments", nargs="*")
    ap.add_argument("--forward", action="store_true")
    ap.add_argument("--by-dsched", action="store_true")
    ap.add_argument("--bands", action="store_true")
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    if a.forward == bool(a.experiments):
        sys.exit("give either experiment ids or --forward")
    if a.forward:
        res = forward()
        print_forward(res)
    else:
        res = baseline(a.experiments, a.by_dsched, a.bands)
        print_baseline(res)
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
