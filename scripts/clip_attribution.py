"""Share of a candidate's SSE advantage over a comparator carried by rows whose anchor
`d_aobt3` lies beyond the fold's training winsorisation clip (0.5 / 99.5 % quantiles,
the H004 ridge setting). Produces research/comparisons/<cand>_vs_<champ>_clip_attribution.json.

    uv run python scripts/clip_attribution.py E005 E004
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl

from prc.data import load_silver
from prc.evaluate import _join, _predictions, truth_frame
from prc.features import fs0
from prc.paths import ROOT
from prc.splits import get_fold, masked_view, promotion_config


def main(cand: str, champ: str) -> None:
    s = load_silver()
    res = {}
    for f in promotion_config()["development_folds"]:
        feats = fs0(masked_view(s, get_fold(f)))
        tr = feats.filter(pl.col("role") == "train")
        lo, hi = tr["d_aobt3"].quantile(0.005), tr["d_aobt3"].quantile(0.995)
        va = feats.filter(pl.col("role") == "val").select("MVT_ID_mvt", "d_aobt3")
        t = truth_frame(f)
        a = _join(_predictions(cand, f), t).join(va, on="MVT_ID_mvt")
        b = _join(_predictions(champ, f), t).select("MVT_ID_mvt", pl.col("pred").alias("pb"))
        y = pl.col("TAXITIME_SEC_mvt").cast(pl.Float64)
        j = a.join(b, on="MVT_ID_mvt").with_columns(
            ((pl.col("pred") - y) ** 2 - (pl.col("pb") - y) ** 2).alias("d"),
            ((pl.col("d_aobt3") < lo) | (pl.col("d_aobt3") > hi)).fill_null(False).alias("beyond"))
        tot, bey = j["d"].sum(), j.filter(pl.col("beyond"))["d"].sum()
        res[f] = {"clip": [lo, hi], "rows_beyond": int(j["beyond"].sum()),
                  "share_of_sse_change_beyond_clip": round(bey / tot, 3)}
    out = ROOT / "research" / "comparisons" / f"{cand}_vs_{champ}_clip_attribution.json"
    out.write_text(json.dumps(res, indent=1))
    print(json.dumps(res))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
