"""Integrity check of a routed candidate (Day 3, H015 clause 3). Never reads truth.

    uv run python scripts/route_check.py ROUTED_EID UNROUTED_EID CHAMPION_EID

For every fold the routed experiment predicted (scored folds and H), compares prediction
files row by row:
  - on the routed subgroup (ADEP_mvt == LIRF and AOBT_3 missing; target-free silver
    columns), ROUTED must equal CHAMPION (max |diff| <= 1e-6 s);
  - elsewhere, ROUTED must equal UNROUTED exactly (max |diff| == 0).
Also records the SHA-256 of each prediction file from the manifests.
Writes research/comparisons/route_check_<routed>.json and exits 1 if any check fails.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl

from prc.paths import EXPERIMENTS, PREDICTIONS_VAL, ROOT

TOL_CHAMPION = 1e-6


def manifest(eid: str) -> dict:
    m = json.loads((EXPERIMENTS / eid / "manifest.json").read_text())
    return {a["fold"]: a["sha256"] for a in m["artifacts"]}


def load(eid: str, fold: str) -> pl.DataFrame:
    return pl.read_parquet(PREDICTIONS_VAL / eid / f"{fold}.parquet").sort("MVT_ID_mvt")


def main(routed: str, unrouted: str, champion: str) -> None:
    silver = pl.read_parquet(ROOT / "data" / "processed" / "silver.parquet",
                             columns=["MVT_ID_mvt", "ADEP_mvt", "AOBT_3_flt"])
    sub = silver.select("MVT_ID_mvt", ((pl.col("ADEP_mvt") == "LIRF")
                                       & pl.col("AOBT_3_flt").is_null()).alias("route"))
    shas = {e: manifest(e) for e in (routed, unrouted, champion)}
    out, ok = {"routed": routed, "unrouted": unrouted, "champion": champion,
               "tolerance_champion_s": TOL_CHAMPION, "folds": {}}, True
    for fold in shas[routed]:
        r, u, c = load(routed, fold), load(unrouted, fold), load(champion, fold)
        if not (r["MVT_ID_mvt"].equals(u["MVT_ID_mvt"]) and r["MVT_ID_mvt"].equals(c["MVT_ID_mvt"])):
            sys.exit(f"{fold}: prediction files cover different rows")
        m = r.join(sub, on="MVT_ID_mvt", how="left")["route"].fill_null(False).to_numpy()
        pr, pu, pc = (x["pred"].to_numpy() for x in (r, u, c))
        d_champ = float(np.abs(pr[m] - pc[m]).max()) if m.any() else 0.0
        d_unr = float(np.abs(pr[~m] - pu[~m]).max()) if (~m).any() else 0.0
        passed = d_champ <= TOL_CHAMPION and d_unr == 0.0
        ok &= passed
        out["folds"][fold] = {
            "rows": int(m.size), "routed_rows": int(m.sum()),
            "max_abs_diff_routed_vs_champion": d_champ,
            "max_abs_diff_nonrouted_vs_unrouted": d_unr,
            "routed_rows_differing_from_unrouted": int((pr[m] != pu[m]).sum()),
            "sha256": {e: shas[e].get(fold) for e in shas}, "passes": passed}
    out["passes"] = bool(ok)
    path = ROOT / "research" / "comparisons" / f"route_check_{routed}.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({f: (v["passes"], v["routed_rows"]) for f, v in out["folds"].items()}))
    print(f"passes: {ok} -> {path.relative_to(ROOT)}")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
