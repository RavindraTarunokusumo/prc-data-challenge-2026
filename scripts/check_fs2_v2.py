"""Target-free checks for H015 v2 (X-D03-S01-0001 review, Revisions 1 and 4).

    uv run python scripts/check_fs2_v2.py [--old-congestion PATH]

1. Masking invariance of the re-implemented congestion block on real data: features from a
   Jan-Nov 2025 view with every DEP block time and target nulled must equal those from the
   unmasked view (the property H015 v1 verified for the previous implementation).
2. With --old-congestion (the previous prc/congestion.py, e.g. from `git show`): per
   feature, the number of DEP rows whose value changes, and whether every changed row takes
   off at or before its t_off proxy (the only rows the fix may touch).
3. LIRF DEP rows with AOBT_3 missing, per month of 2025 and 2026 (silver; target-free).

Reads no DEP block time or target: every view is masked before use except the unmasked
side of check 1, whose features are compared for equality only.
Writes research/day-03/eda/fs2_v2_checks.json.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl

from prc import congestion as cg
from prc.data import load_silver
from prc.paths import ROOT

OUT = ROOT / "research" / "day-03" / "eda" / "fs2_v2_checks.json"
TRAIN_MONTHS = [f"2025-{m:02d}" for m in range(1, 12)]
HIDE = ("BLOCK_TIME_UTC_mvt", "TAXITIME_SEC_mvt")


def view(s: pl.DataFrame, months: list[str], mask_dep: bool) -> pl.LazyFrame:
    lf = s.lazy().filter(pl.col("month").is_in(months))
    if mask_dep:
        dep = pl.col("PHASE_mvt") == "DEP"
        lf = lf.with_columns([pl.when(dep).then(None).otherwise(pl.col(c)).alias(c)
                              for c in HIDE])
    return lf


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("congestion_old", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--old-congestion", type=Path, default=None)
    a = ap.parse_args()
    s = load_silver()
    out: dict = {}

    masked_view = view(s, TRAIN_MONTHS, True)
    new = cg.congestion(masked_view)
    unmasked = cg.congestion(view(s, TRAIN_MONTHS, False))
    out["masking_invariance_jan_nov"] = {"rows": new.height,
                                         "identical": bool(new.equals(unmasked))}

    if a.old_congestion is not None:
        old = load_module(a.old_congestion).congestion(masked_view)
        prox = (masked_view.filter(pl.col("PHASE_mvt") == "DEP")
                .select("MVT_ID_mvt",
                        (pl.col("MVT_TIME_UTC_mvt") <= pl.coalesce(
                            "AOBT_3_flt", "EOBT_1_flt", "SCHED_TIME_UTC_mvt"))
                        .alias("to_le_proxy"))
                .collect())
        j = new.join(old, on="MVT_ID_mvt", suffix="_old").join(prox, on="MVT_ID_mvt")
        per = {}
        any_changed = pl.lit(False)
        for f in cg.FEATURES:
            ch = pl.col(f) != pl.col(f"{f}_old")
            any_changed = any_changed | ch
            per[f] = {"rows_changed": int(j.select(ch.sum()).item()),
                      "all_changed_rows_take_off_at_or_before_proxy": bool(
                          j.filter(ch).select(pl.col("to_le_proxy").all()).item()
                          if j.select(ch.sum()).item() else True)}
        changed = j.filter(any_changed)
        out["old_vs_new_jan_nov"] = {
            "rows": j.height,
            "rows_any_feature_changed": changed.height,
            "rows_taking_off_at_or_before_proxy": int(j["to_le_proxy"].sum()),
            "per_feature": per}

    lirf = (s.lazy().filter((pl.col("PHASE_mvt") == "DEP") & (pl.col("ADEP_mvt") == "LIRF"))
            .group_by("month")
            .agg(pl.len().alias("lirf_dep_rows"),
                 pl.col("AOBT_3_flt").is_null().sum().alias("nm_missing_rows"))
            .with_columns((pl.col("nm_missing_rows") / pl.col("lirf_dep_rows"))
                          .alias("nm_missing_share"))
            .sort("month").collect())
    out["lirf_nm_missing_by_month"] = lirf.to_dicts()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, default=str))
    print(json.dumps({k: v for k, v in out.items() if k != "lirf_nm_missing_by_month"},
                     indent=1))
    for r in out["lirf_nm_missing_by_month"]:
        print(r["month"], r["nm_missing_rows"], f"{r['nm_missing_share']:.4f}")


if __name__ == "__main__":
    main()
