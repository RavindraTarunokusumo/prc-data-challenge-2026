"""Day 8 agenda item 1: recording conventions in the tail beyond LIRF, on design months only.

Reads DEP targets of 2025-01, 04, 05 and 06 only: the months in the training part of every
development fold (X-D08-S01-0001 (d)), as H038's and the weather pilots did. No validation-month
target of any development fold, and no December target, is read. Not an experiment: no model is
fitted and no candidate is selected.

What is new against PHASE_CLOSE_D01 (c). Day 1 tested one convention, block = SCHED
(|y - d_sched| < 120 s), and found it at or below base rates outside LIRF. This script tests
other signatures, per airport, on tail rows (y >= 3,600 s) against bulk rows:

  anchor equality   |BLOCK - X| < 120 s for X in EOBT_1, IOBT, LOBT, AOBT_3 (and SCHED, as
                    Day 1's check on these months)
  hour shift        |BLOCK - X + k * 3,600| < 120 s for k in 1..3 (block recorded k hours
                    early, e.g. local time written as UTC), X in AOBT_3, EOBT_1, SCHED
  day shift         |BLOCK - X + 86,400| < 600 s for X in SCHED, EOBT_1 (previous day)
  round block       BLOCK on a whole hour (hh:00:00)
  repeated block    BLOCK shared by >= 5 DEP rows at the same airport

Reading rule (fixed before the run). A signature is a finding at an airport (LIRF excluded) if,
over the four design months, it covers at least 30 tail rows and its tail share is at least
twice its bulk share. Anything else is reported only. A finding is a lead for a proposal, which
would state this footprint (design months, row level); it is not evidence on any fold.

    uv run python scripts/eda_conventions_D08.py --out research/day-08/eda/conventions.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl

from prc.data import load_silver
from prc.paths import ROOT

DESIGN_MONTHS = ["2025-01", "2025-04", "2025-05", "2025-06"]
TAIL_S = 3600
TOL_S = 120
MIN_TAIL_ROWS = 30
MIN_RATIO = 2.0
ANCHORS = ["SCHED_TIME_UTC_mvt", "EOBT_1_flt", "IOBT_flt", "LOBT_flt", "AOBT_3_flt"]


def secs(a: str, b: str) -> pl.Expr:
    return (pl.col(a) - pl.col(b)).dt.total_seconds()


def signatures() -> dict[str, pl.Expr]:
    sig = {f"eq_{a}": secs("BLOCK_TIME_UTC_mvt", a).abs() < TOL_S for a in ANCHORS}
    for a in ("AOBT_3_flt", "EOBT_1_flt", "SCHED_TIME_UTC_mvt"):
        for k in (1, 2, 3):
            sig[f"early_{k}h_{a}"] = (secs("BLOCK_TIME_UTC_mvt", a) + k * 3600).abs() < TOL_S
    for a in ("SCHED_TIME_UTC_mvt", "EOBT_1_flt"):
        sig[f"early_1d_{a}"] = (secs("BLOCK_TIME_UTC_mvt", a) + 86_400).abs() < 600
    b = pl.col("BLOCK_TIME_UTC_mvt")
    sig["round_hour"] = (b.dt.minute() == 0) & (b.dt.second() == 0)
    sig["repeated_block"] = pl.len().over("ADEP_mvt", "BLOCK_TIME_UTC_mvt") >= 5
    return {k: v.fill_null(False) for k, v in sig.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    s = load_silver()
    dep = s.filter(pl.col("month").is_in(DESIGN_MONTHS) & (pl.col("PHASE_mvt") == "DEP"))
    assert set(dep["month"].unique()) <= set(DESIGN_MONTHS)
    sig = signatures()
    dep = dep.with_columns(
        (pl.col("TAXITIME_SEC_mvt") >= TAIL_S).alias("tail"),
        pl.col("AOBT_3_flt").is_null().alias("nm_missing"),
        **sig)
    y2 = (pl.col("TAXITIME_SEC_mvt").cast(pl.Float64) - pl.col("TAXITIME_SEC_mvt").mean()) ** 2
    dep = dep.with_columns(y2.over("ADEP_mvt").alias("sq"))
    out = {"schema": "conventions-v1", "design_months": DESIGN_MONTHS, "tail_s": TAIL_S,
           "rule": {"min_tail_rows": MIN_TAIL_ROWS, "min_ratio": MIN_RATIO},
           "airports": {}, "findings": []}
    for ap_ in sorted(dep["ADEP_mvt"].unique()):
        d = dep.filter(pl.col("ADEP_mvt") == ap_)
        t, b = d.filter(pl.col("tail")), d.filter(~pl.col("tail"))
        rec = {"rows": d.height, "tail_rows": t.height,
               "tail_nm_missing": int(t["nm_missing"].sum()),
               "tail_sq_share": float(t["sq"].sum() / d["sq"].sum()), "signatures": {}}
        for k in sig:
            nt, nb = int(t[k].sum()), int(b[k].sum())
            st = nt / t.height if t.height else 0.0
            sb = nb / b.height if b.height else 0.0
            rec["signatures"][k] = {"tail_rows": nt, "tail_share": st, "bulk_share": sb,
                                    "ratio": st / sb if sb else None,
                                    "tail_sq_share": float(t.filter(pl.col(k))["sq"].sum()
                                                           / d["sq"].sum())}
            if (ap_ != "LIRF" and nt >= MIN_TAIL_ROWS
                    and (sb == 0 or st / sb >= MIN_RATIO)):
                out["findings"].append({"airport": ap_, "signature": k, "tail_rows": nt,
                                        "tail_share": st, "bulk_share": sb})
        out["airports"][ap_] = rec
    (ROOT / args.out).write_text(json.dumps(out, indent=1) + "\n")
    for ap_, r in out["airports"].items():
        top = sorted(r["signatures"].items(), key=lambda kv: -kv[1]["tail_rows"])[:3]
        print(ap_, r["tail_rows"], "tail;",
              ", ".join(f"{k} {v['tail_rows']} ({v['tail_share']:.2f} vs {v['bulk_share']:.3f})"
                        for k, v in top))
    print("findings:", out["findings"] or "none")


if __name__ == "__main__":
    main()
