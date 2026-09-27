"""Paired promotion comparison between two completed experiments (frozen rule), plus the
tail attribution required by the Advisor's standing rule 1 (SPLITS v2 review).

    uv run python scripts/compare.py CANDIDATE_EID CHAMPION_EID [--out DIR]

Both experiments must be COMPLETE in the ledger. Writes <out>/<cand>_vs_<champ>.json
(default research/comparisons/) and prints a summary.
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
from prc.data import load_silver
from prc.evaluate import _join, _predictions, compare, truth_frame
from prc.metrics import BULK_MAX_S, PRED, TARGET
from prc.paths import ROOT
from prc.splits import promotion_config


def tail_attribution(cand: str, champ: str) -> dict:
    """Per development fold: dRMSE on the bulk (y < 3600 s) next to the full population,
    and the share of the SSE change contributed by the tail (y >= 3600 s)."""
    out, tot_bulk, tot_tail = {}, 0.0, 0.0
    for f in promotion_config()["development_folds"]:
        t = truth_frame(f)
        a, b = _join(_predictions(cand, f), t), _join(_predictions(champ, f), t)
        y = a[TARGET].cast(pl.Float64).to_numpy()
        ea, eb = (a[PRED].to_numpy() - y) ** 2, (b[PRED].to_numpy() - y) ** 2
        bulk = y < BULK_MAX_S
        d_bulk, d_tail = float((ea - eb)[bulk].sum()), float((ea - eb)[~bulk].sum())
        tot_bulk += d_bulk
        tot_tail += d_tail
        out[f] = {
            "delta_rmse_full": float(np.sqrt(ea.mean()) - np.sqrt(eb.mean())),
            "delta_rmse_bulk": float(np.sqrt(ea[bulk].mean()) - np.sqrt(eb[bulk].mean())),
            "delta_sse_bulk": d_bulk,
            "delta_sse_tail": d_tail,
            "tail_share_of_sse_change": d_tail / (d_bulk + d_tail) if d_bulk + d_tail else None,
            "tail_rows": int((~bulk).sum()),
        }
    total = tot_bulk + tot_tail
    return {"by_fold": out, "pooled_tail_share_of_sse_change": tot_tail / total if total else None}


def row_concentration(cand: str, champ: str) -> dict:
    """Standing rule 6 (B4, X-D01-S01-0003): per fold, the signed share of the SSE change
    (sum of e_cand^2 - e_champ^2) carried by the largest single row and the 10 largest rows
    by |contribution|. Rows carrying >= 50 % are reported with airport, anchor, target and
    both predictions. Attribution only; fold outcomes are unchanged."""
    cfg = promotion_config()
    folds = list(cfg["development_folds"]) + list(cfg["causal_twins"].values())
    anchor = (
        load_silver(columns=["MVT_ID_mvt", "MVT_TIME_UTC_mvt", "AOBT_3_flt", "month",
                             "PHASE_mvt"])
        .filter(pl.col("PHASE_mvt") == "DEP")
        .select("MVT_ID_mvt", (pl.col("MVT_TIME_UTC_mvt") - pl.col("AOBT_3_flt"))
                .dt.total_seconds().alias("d_aobt3"))
    )
    out = {}
    for f in folds:
        t = truth_frame(f)
        a = _join(_predictions(cand, f), t).rename({PRED: "pred_cand"})
        b = _join(_predictions(champ, f), t).select("MVT_ID_mvt", pl.col(PRED).alias(
            "pred_champ"))
        j = a.join(b, on="MVT_ID_mvt").with_columns(pl.col(TARGET).cast(pl.Float64)).with_columns(
            ((pl.col("pred_cand") - pl.col(TARGET)) ** 2
             - (pl.col("pred_champ") - pl.col(TARGET)) ** 2).alias("d"))
        total = float(j["d"].sum())
        top = j.with_columns(pl.col("d").abs().alias("absd")).sort("absd", descending=True)
        top1, top10 = float(top["d"][0]), float(top["d"][:10].sum())
        rec = {"delta_sse": total,
               "top1_share": top1 / total if total else None,
               "top10_share": top10 / total if total else None}
        if total and abs(top1 / total) >= 0.5:
            r = top.head(1).join(anchor, on="MVT_ID_mvt", how="left").row(0, named=True)
            rec["dominant_row"] = {k: r[k] for k in ("MVT_ID_mvt", "ADEP_mvt", "d_aobt3", TARGET,
                                                     "pred_cand", "pred_champ")}
        out[f] = rec
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("champion")
    ap.add_argument("--out", default="research/comparisons")
    a = ap.parse_args()
    for eid in (a.candidate, a.champion):
        rec = ledger.get(eid)
        if rec is None or rec["status"] != "COMPLETE":
            sys.exit(f"refused: {eid} is not COMPLETE in the ledger")
    r = compare(a.candidate, a.champion)
    r["tail_attribution"] = tail_attribution(a.candidate, a.champion)
    r["row_concentration"] = row_concentration(a.candidate, a.champion)
    out = ROOT / a.out / f"{a.candidate}_vs_{a.champion}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, indent=1) + "\n")
    print(f"{a.candidate} vs {a.champion}: mean dRMSE {r['mean_delta_rmse']:+.2f} s "
          f"(q95 {r['mean_delta_q95']:+.2f})")
    ta = r["tail_attribution"]["by_fold"]
    for f, o in r["fold_outcome"].items():
        lo, hi = r["fold_delta_q10_q90"][f]
        counted = r["fold_outcome_counted"].get(f, o)
        extra = f"  bulk {ta[f]['delta_rmse_bulk']:+.2f}" if f in ta else ""
        print(f"  {f:4s} {r['fold_delta_rmse'][f]:+8.2f} s  [{lo:+.2f}, {hi:+.2f}]  {o:4s}"
              f"{'' if o == counted else ' (counted ' + counted + ')'}{extra}")
    rc = r["row_concentration"]
    print("  row concentration (top1 / top10 share of SSE change):",
          ", ".join(f"{f} {v['top1_share']:+.2f}/{v['top10_share']:+.2f}"
                    for f, v in rc.items() if v["top1_share"] is not None))
    for f, v in rc.items():
        if "dominant_row" in v:
            print(f"  DOMINANT ROW {f}: {v['dominant_row']}")
    share = r["tail_attribution"]["pooled_tail_share_of_sse_change"]
    print(f"  tail share of SSE change (dev folds): {share:.3f}" if share is not None else "")
    print(f"  criteria: 1={r['criterion_1']} 2={r['criterion_2']} 3={r['criterion_3']}  "
          f"-> passes_criteria_1_to_3={r['passes_criteria_1_to_3']}")
    if r["airports_degraded_beyond_tolerance"]:
        print("  degraded airports:", r["airports_degraded_beyond_tolerance"])


if __name__ == "__main__":
    main()
