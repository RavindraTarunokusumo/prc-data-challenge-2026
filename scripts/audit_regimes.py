"""Seasonal and regime evidence for SPLITS v2 (winter coverage, S1 forward exposure).

December (the protected holdout) is removed before any statistic is computed: no
December target is read. Output: research/day-01/audit/regime_stats.json.

    uv run python scripts/audit_regimes.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
os.environ.setdefault("POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR", "load_as_storage")

import polars as pl

from prc.paths import ROOT, SILVER

OUT = ROOT / "research" / "day-01" / "audit" / "regime_stats.json"
Y = "TAXITIME_SEC_mvt"


def main() -> None:
    dep = (
        pl.scan_parquet(SILVER)
        .filter((pl.col("src") == "train") & (pl.col("PHASE_mvt") == "DEP")
                & (pl.col("month") != "2025-12"))
        .select("month", "ADEP_mvt", "RUNWAY_mvt", "MVT_TIME_UTC_mvt", Y)
        .collect()
    )
    assert "2025-12" not in dep["month"].unique().to_list()
    s: dict = {"excluded_months": ["2025-12"]}

    winter = ["2025-01", "2025-02"]
    dev_val = ["2025-07", "2025-09", "2025-10", "2025-11"]
    q = (
        dep.with_columns(
            pl.when(pl.col("month").is_in(winter)).then(pl.lit("winter_JanFeb"))
            .when(pl.col("month").is_in(dev_val)).then(pl.lit("v1_dev_val_JulSepOctNov"))
            .otherwise(pl.lit("other")).alias("grp"))
        .filter(pl.col("grp") != "other")
        .group_by("ADEP_mvt", "grp")
        .agg(pl.col(Y).quantile(0.5).alias("p50"), pl.col(Y).quantile(0.9).alias("p90"),
             pl.col(Y).quantile(0.99).alias("p99"))
        .sort("ADEP_mvt", "grp")
    )
    s["winter_vs_v1_dev_quantiles"] = q.rows(named=True)
    p90 = q.pivot(on="grp", index="ADEP_mvt", values="p90")
    s["p90_winter_minus_dev"] = dict(zip(
        p90["ADEP_mvt"], (p90["winter_JanFeb"] - p90["v1_dev_val_JulSepOctNov"]).to_list()))

    daily = dep.group_by("ADEP_mvt", pl.col("MVT_TIME_UTC_mvt").dt.date().alias("day")).agg(
        pl.col(Y).median().alias("med"), pl.first("month"))
    typical = daily.group_by("ADEP_mvt").agg(pl.col("med").median().alias("typ"))
    disrupted = (daily.join(typical, on="ADEP_mvt")
                 .filter(pl.col("med") > pl.col("typ") + 300).sort("day"))
    s["disrupted_airport_days_rule"] = "airport-day median > airport median of daily medians + 300 s"
    s["disrupted_airport_days"] = [(r["ADEP_mvt"], str(r["day"])) for r in disrupted.iter_rows(
        named=True)]
    s["disrupted_by_month"] = dict(sorted(disrupted.group_by("month").len().rows()))

    lfpg = dep.filter(pl.col("ADEP_mvt") == "LFPG")
    share = (lfpg.group_by("month", "RUNWAY_mvt").len()
             .with_columns((pl.col("len") / pl.col("len").sum().over("month")).round(3)
                           .alias("share"))
             .pivot(on="RUNWAY_mvt", index="month", values="share").sort("month").fill_null(0))
    s["lfpg_runway_share_by_month"] = share.rows(named=True)
    s["lfpg_median_by_month"] = dict(sorted(
        lfpg.group_by("month").agg(pl.col(Y).median()).rows()))
    OUT.write_text(json.dumps(s, indent=1, default=str) + "\n")
    print(json.dumps({k: s[k] for k in ("p90_winter_minus_dev", "disrupted_by_month",
                                          "lfpg_median_by_month")}, indent=1))
    print(share)


if __name__ == "__main__":
    main()
