"""Pre-registered mechanism checks on a named sub-population (Day 2, X-D02-S01-0001).

    uv run python scripts/mechanism_check.py CANDIDATE_EID REFERENCE_EID POPULATION

POPULATION: all | NM_present | LIRF_NM_missing | excl_LIRF_NM_missing | NM_present_excl_LIRF
(prc.attribution). Also reports standing rule 6 (row concentration) on the population.
Applies the frozen paired bootstrap and criteria 1-3 (prc.metrics.promotion_check,
unchanged) to the rows of each development fold and twin that belong to POPULATION, and
reports per fold the full and bulk (y < 3600 s) dRMSE on that population. A mechanism
test, never a promotion decision: promotion uses scripts/compare.py on all rows.
Writes research/comparisons/<cand>_vs_<ref>_mech_<population>.json.
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
from prc.attribution import POPULATIONS, population_mask, row_concentration
from prc.data import load_silver
from prc.evaluate import _join, _predictions, truth_frame
from prc.metrics import BULK_MAX_S, PRED, TARGET, promotion_check
from prc.paths import ROOT
from prc.splits import promotion_config


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("reference")
    ap.add_argument("population", choices=POPULATIONS)
    a = ap.parse_args()
    for eid in (a.candidate, a.reference):
        rec = ledger.get(eid)
        if rec is None or rec["status"] != "COMPLETE":
            sys.exit(f"refused: {eid} is not COMPLETE in the ledger")
    cfg = promotion_config()
    folds = list(cfg["development_folds"]) + list(cfg["causal_twins"].values())
    silver = (load_silver(columns=["MVT_ID_mvt", "AOBT_3_flt", "MVT_TIME_UTC_mvt",
                                   "SCHED_TIME_UTC_mvt", "PHASE_mvt", "month"])
              .filter(pl.col("PHASE_mvt") == "DEP"))
    nm = silver.select("MVT_ID_mvt", pl.col("AOBT_3_flt").is_null().alias("nm_missing"))
    detail = silver.select(
        "MVT_ID_mvt",
        (pl.col("MVT_TIME_UTC_mvt") - pl.col("AOBT_3_flt")).dt.total_seconds().alias("d_aobt3"),
        (pl.col("MVT_TIME_UTC_mvt") - pl.col("SCHED_TIME_UTC_mvt")).dt.total_seconds()
        .alias("d_sched"))
    cand, ref, per_fold, conc = {}, {}, {}, {}
    for f in folds:
        t = truth_frame(f).join(nm, on="MVT_ID_mvt", how="left")
        keep = population_mask(t, a.population)
        t = t.filter(keep).drop("nm_missing")
        ref[f] = _join(_predictions(a.reference, f).join(t.select("MVT_ID_mvt"),
                                                         on="MVT_ID_mvt"), t)
        cand[f] = _join(_predictions(a.candidate, f).join(t.select("MVT_ID_mvt"),
                                                          on="MVT_ID_mvt"), t)
        y = cand[f][TARGET].cast(pl.Float64).to_numpy()
        ec = (cand[f][PRED].to_numpy() - y) ** 2
        er = (ref[f][PRED].to_numpy() - y) ** 2
        b = y < BULK_MAX_S
        per_fold[f] = {
            "rows": int(y.size), "tail_rows": int((~b).sum()),
            "delta_rmse_full": float(np.sqrt(ec.mean()) - np.sqrt(er.mean())),
            "delta_rmse_bulk": float(np.sqrt(ec[b].mean()) - np.sqrt(er[b].mean()))
            if b.any() else None,
        }
        rows = (cand[f].select("MVT_ID_mvt", "ADEP_mvt", pl.col(TARGET).cast(pl.Float64)
                               .alias("y"), pl.col(PRED).alias("pred_cand"))
                .join(ref[f].select("MVT_ID_mvt", pl.col(PRED).alias("pred_champ")),
                      on="MVT_ID_mvt")
                .join(detail, on="MVT_ID_mvt", how="left"))
        conc[f] = row_concentration(rows, ("ADEP_mvt", "d_aobt3", "d_sched"))
    r = {"candidate": a.candidate, "reference": a.reference, "population": a.population,
         "per_fold": per_fold, "row_concentration_rule6": conc,
         **promotion_check(cand, ref)}
    out = ROOT / "research" / "comparisons" / \
        f"{a.candidate}_vs_{a.reference}_mech_{a.population}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, indent=1, default=float) + "\n")
    print(f"{a.candidate} vs {a.reference} on {a.population}: mean dRMSE "
          f"{r['mean_delta_rmse']:+.2f} (q95 {r['mean_delta_q95']:+.2f}) "
          f"crit1={r['criterion_1']} crit2={r['criterion_2']}")
    for f in folds:
        p = per_fold[f]
        bulk = "n/a" if p["delta_rmse_bulk"] is None else f"{p['delta_rmse_bulk']:+.2f}"
        c = conc[f]
        top = "n/a" if c["top1_share"] is None else f"{c['top1_share']:+.2f}/{c['top10_share']:+.2f}"
        print(f"  {f:4s} n={p['rows']:6d} full {p['delta_rmse_full']:+8.2f} bulk {bulk:>8s} "
              f"{r['fold_outcome'][f]:4s} top1/top10 {top}")
        if "dominant_row" in c:
            print(f"       DOMINANT ROW: {c['dominant_row']}")


if __name__ == "__main__":
    main()
