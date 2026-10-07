"""Integrity check of a convention-mixture experiment (Day 8, H038). Never reads truth.

    uv run python scripts/mixture_check.py MIXTURE_EID BASE_EID

For every fold the experiment predicted:
  - outside the LIRF NM-missing subgroup (target-free silver columns), MIXTURE must equal
    BASE exactly (max |diff| == 0);
  - on the subgroup, MIXTURE must equal its stored components' `pred` (within 1e-6 s), and
    `pred` must equal p * conv + (1 - p) * g (within 1e-6 s; g alone where conv is null);
  - the components cover exactly the subgroup's rows.
Records each component file's path, size and SHA-256 (their tracked manifest, DATA_POLICY §3;
the launcher commits this JSON).
Writes research/comparisons/mixture_check_<eid>.json and exits 1 if any check fails.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl

from prc.blending import OVERRIDE_SUBGROUPS
from prc.data import load_silver
from prc.paths import EXPERIMENTS, PREDICTIONS_VAL, ROOT, sha256_file

TOL = 1e-6


def main(eid: str, base: str) -> int:
    folds = [a["fold"] for a in json.loads((EXPERIMENTS / eid / "manifest.json").read_text())
             ["artifacts"]]
    keys = load_silver().select(pl.col("MVT_ID_mvt").cast(pl.Int64), "ADEP_mvt",
                                pl.col("AOBT_3_flt").is_null().cast(pl.Int32)
                                .alias("flt_missing"))
    sub_expr = OVERRIDE_SUBGROUPS["LIRF_NM_missing"]
    out, ok = {"experiment": eid, "base": base, "folds": {}}, True
    for fold in folds:
        m = pl.read_parquet(PREDICTIONS_VAL / eid / f"{fold}.parquet")
        b = pl.read_parquet(PREDICTIONS_VAL / base / f"{fold}.parquet").rename({"pred": "pb"})
        cpath = PREDICTIONS_VAL / eid / "components" / f"{fold}.parquet"
        c = pl.read_parquet(cpath)
        j = (m.join(b, on="MVT_ID_mvt", how="left", validate="1:1")
             .join(keys, on="MVT_ID_mvt", how="left", validate="1:1")
             .with_columns(sub_expr.alias("sub")))
        sub, rest = j.filter(pl.col("sub")), j.filter(~pl.col("sub"))
        sc = sub.join(c.rename({"pred": "pc"}), on="MVT_ID_mvt", how="left", validate="1:1")
        recon = np.where(c["conv_component"].is_null().to_numpy(), c["g_normal"].to_numpy(),
                         c["p_conv"].to_numpy() * c["conv_component"].fill_null(0).to_numpy()
                         + (1 - c["p_conv"].to_numpy()) * c["g_normal"].to_numpy())
        r = {"rows": j.height, "subgroup_rows": sub.height, "component_rows": c.height,
             "base_missing": int(j["pb"].null_count()),
             "max_abs_diff_outside": float((rest["pred"] - rest["pb"]).abs().max() or 0.0),
             "max_abs_diff_subgroup_vs_components":
                 float((sc["pred"] - sc["pc"]).abs().max() or 0.0) if sub.height else 0.0,
             "max_abs_diff_components_formula":
                 float(np.max(np.abs(recon - c["pred"].to_numpy()))) if c.height else 0.0}
        # DATA_POLICY §3: the component files are git-ignored; this record is their manifest
        r["components_file"] = {"path": str(cpath.relative_to(ROOT)), "size": cpath.stat().st_size,
                                "sha256": sha256_file(cpath)}
        r["pass"] = (r["base_missing"] == 0 and r["component_rows"] == r["subgroup_rows"]
                     and sc["pc"].null_count() == 0 and r["max_abs_diff_outside"] == 0.0
                     and r["max_abs_diff_subgroup_vs_components"] <= TOL
                     and r["max_abs_diff_components_formula"] <= TOL)
        ok &= r["pass"]
        out["folds"][fold] = r
        print(fold, "PASS" if r["pass"] else "FAIL", json.dumps(r), flush=True)
    out["pass"] = ok
    (ROOT / "research/comparisons" / f"mixture_check_{eid}.json").write_text(
        json.dumps(out, indent=1) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
