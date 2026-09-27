"""Diagnostic for standing rule 1: does a candidate's tail gain (y >= 3600 s) over a
champion run through the pre-registered anchor mechanism?

Per development fold, it splits the SSE change (candidate - champion) into bulk rows,
tail rows with the anchor present, and tail rows without it (no NM data). For
anchor-present tail rows it also reports how often the candidate is closer to the anchor
than the champion is.

    uv run python scripts/tail_mechanism.py CANDIDATE_EID CHAMPION_EID
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl

from prc.data import load_silver
from prc.evaluate import _join, _predictions, truth_frame
from prc.metrics import BULK_MAX_S, TARGET
from prc.paths import ROOT
from prc.splits import promotion_config


def main(cand: str, champ: str) -> None:
    anchor = (load_silver(columns=["MVT_ID_mvt", "MVT_TIME_UTC_mvt", "AOBT_3_flt", "PHASE_mvt",
                                   "month"])
              .filter(pl.col("PHASE_mvt") == "DEP")
              .select("MVT_ID_mvt", (pl.col("MVT_TIME_UTC_mvt") - pl.col("AOBT_3_flt"))
                      .dt.total_seconds().cast(pl.Float64).alias("anchor")))
    out = {}
    for f in promotion_config()["development_folds"]:
        t = truth_frame(f)
        a = _join(_predictions(cand, f), t).rename({"pred": "pc"})
        b = _join(_predictions(champ, f), t).select("MVT_ID_mvt", pl.col("pred").alias("ph"))
        y = pl.col(TARGET).cast(pl.Float64)
        j = (a.join(b, on="MVT_ID_mvt").join(anchor, on="MVT_ID_mvt", how="left")
             .with_columns(((pl.col("pc") - y) ** 2 - (pl.col("ph") - y) ** 2).alias("d"),
                           pl.when(y < BULK_MAX_S).then(pl.lit("bulk"))
                           .when(pl.col("anchor").is_null()).then(pl.lit("tail_no_anchor"))
                           .otherwise(pl.lit("tail_anchor")).alias("grp")))
        total = j["d"].sum()
        g = j.group_by("grp").agg(pl.len().alias("rows"), pl.col("d").sum().alias("dsse"))
        rec = {r["grp"]: {"rows": r["rows"], "share_of_sse_change": r["dsse"] / total}
               for r in g.iter_rows(named=True)}
        ta = j.filter(pl.col("grp") == "tail_anchor")
        if ta.height:
            closer = ((ta["pc"] - ta["anchor"]).abs() < (ta["ph"] - ta["anchor"]).abs()).mean()
            rec["tail_anchor"]["candidate_closer_to_anchor_share"] = float(closer)
        out[f] = rec
        print(f, json.dumps(rec))
    path = ROOT / "research" / "comparisons" / f"{cand}_vs_{champ}_tail_mechanism.json"
    path.write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
