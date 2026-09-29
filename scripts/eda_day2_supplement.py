"""Day 2 EDA supplement (X-D02-S01-0001, H009 review items 4-5).

    uv run python scripts/eda_day2_supplement.py

Producing code for EDA finding 5 and the FS1 build check, plus corrected evidence:
  1. ranking-DEP unseen shares against the Jan-Nov 2025 TRAINING vocabulary
     (scripts/eda_day2.py built its vocabulary over all of silver, including Dec and the
     two ranking months, so it reported 0 %);
  2. NM-missing DEP counts and key-presence shares, Jan-Nov 2025 training rows only;
  3. finding 5: LIRF NM-missing convention-tail rate by d_sched band (FIT months only);
  4. FS1 build check on the S1 fold (time, peak RSS, levels, rare shares).
Target hygiene as scripts/eda_day2.py: targets are read only for FIT months (Jan, Mar-Jun
2025). Items 1, 2 and 4 read no target. Writes research/day-02/eda/supplement.json.
"""

from __future__ import annotations

import json
import resource
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl

from prc.data import load_silver
from prc.features import FS1_EXTRA_CATEGORICAL, RARE, fs1
from prc.paths import RAW, ROOT
from prc.splits import get_fold, masked_view

FIT = ["2025-01", "2025-03", "2025-04", "2025-05", "2025-06"]
JAN_NOV = [f"2025-{m:02d}" for m in range(1, 12)]
OUT = ROOT / "research" / "day-02" / "eda" / "supplement.json"


def key_exprs() -> list[pl.Expr]:
    return [pl.col("STAND_mvt").fill_null("NA").alias("stand"),
            pl.col("AIRCRAFT_TYPE_mvt").fill_null("UNK").alias("actype"),
            pl.col("FLIGHT_mvt").str.slice(0, 3).fill_null("UNK").alias("op_prefix"),
            pl.col("ADES_mvt").fill_null("UNK").alias("ades")]


def main() -> None:
    s = load_silver()
    out: dict = {"fit_months": FIT}
    train = s.filter((pl.col("PHASE_mvt") == "DEP") & (pl.col("src") == "train")
                     & pl.col("month").is_in(JAN_NOV))
    rank = pl.read_parquet(RAW / "ranking.parquet").filter(pl.col("PHASE_mvt") == "DEP")
    tk, rk = train.select(key_exprs()), rank.select(key_exprs())
    out["ranking_dep_unseen_share_vs_jan_nov_training"] = {
        c: float((~rk[c].is_in(tk[c].unique().to_list())).mean()) for c in tk.columns}

    miss = train.filter(pl.col("AOBT_3_flt").is_null())
    out["nm_missing_dep_jan_nov"] = {
        "rows": miss.height,
        "present_share": {c: float(miss[c].is_not_null().mean())
                          for c in ("FLIGHT_mvt", "ADES_mvt", "STAND_mvt",
                                    "AIRCRAFT_TYPE_mvt")}}

    d = (train.filter(pl.col("month").is_in(FIT) & (pl.col("ADEP_mvt") == "LIRF")
                      & pl.col("AOBT_3_flt").is_null())
         .with_columns(pl.col("TAXITIME_SEC_mvt").cast(pl.Float64).alias("y"),
                       (pl.col("MVT_TIME_UTC_mvt") - pl.col("SCHED_TIME_UTC_mvt"))
                       .dt.total_seconds().cast(pl.Float64).alias("d_sched"))
         .with_columns((((pl.col("y") - pl.col("d_sched")).abs() < 120)
                        & (pl.col("y") >= 3600)).alias("conv")))
    bands = (d.with_columns(pl.col("d_sched").cut([3600, 7200]).cast(pl.Utf8).alias("band"))
             .group_by("band").agg(pl.len().alias("rows"), pl.col("conv").mean().alias("rate"))
             .sort("band"))
    out["finding5_lirf_nm_missing_fit"] = {
        "rows": d.height, "convention_tail_rate": float(d["conv"].mean()),
        "definition": "|y - d_sched| < 120 s and y >= 3600 s; the <= 3600 s band is 0 by "
                      "construction (y >= 3600 and |y - d_sched| < 120 need d_sched > 3480)",
        "by_d_sched_band": {r["band"]: {"rows": r["rows"], "rate": r["rate"]}
                            for r in bands.iter_rows(named=True)}}

    t0 = time.time()
    f = fs1(masked_view(s, get_fold("S1")))
    build_s = time.time() - t0
    tr, va = f.filter(pl.col("role") == "train"), f.filter(pl.col("role") == "val")
    out["fs1_build_check_S1"] = {
        "build_s": round(build_s, 2), "rows": f.height, "columns": f.width,
        "peak_rss_gb_process": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6,
        "levels": {c: {"train_levels": tr[c].n_unique(),
                       "rare_share_train": float((tr[c] == RARE).mean()),
                       "rare_share_val": float((va[c] == RARE).mean())}
                   for c in FS1_EXTRA_CATEGORICAL}}
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
