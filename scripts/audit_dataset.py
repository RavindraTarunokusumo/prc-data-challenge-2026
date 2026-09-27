"""Day 1 dataset audit: reproducible statistics behind docs/methodology/DATASET_AUDIT.md.

Reads only bronze data (data/raw/), writes research/day-01/audit/audit_stats.json.

Usage:
    uv run python scripts/audit_dataset.py
"""

from __future__ import annotations

import glob
import json
import os
from pathlib import Path

os.environ.setdefault("POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR", "load_as_storage")

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "prc-2026-datasets"
OUT = ROOT / "research" / "day-01" / "audit" / "audit_stats.json"
Y = "TAXITIME_SEC_mvt"
MVT = "MVT_TIME_UTC_mvt"


def rmse(e: np.ndarray) -> float:
    return float(np.sqrt(np.mean(e**2)))


def main() -> None:
    if (ROOT / "config" / "frozen.json").exists():
        # This pre-freeze audit read the full training year, December included
        # (DATASET_AUDIT §6.6). After the freeze no audit may read holdout targets.
        raise SystemExit("refused: pre-freeze audit; December targets are protected after "
                         "the freeze (use prc.data.load_silver, which masks them)")
    train = pl.read_parquet(sorted(glob.glob(str(RAW / "training_*.parquet"))))
    rank = pl.read_parquet(RAW / "ranking.parquet")
    dep = train.filter(pl.col("PHASE_mvt") == "DEP")
    rdep = rank.filter(pl.col("PHASE_mvt") == "DEP")
    y = dep[Y].cast(pl.Float64)
    s: dict = {}

    s["rows"] = {
        "train": train.height,
        "train_dep": dep.height,
        "train_arr": train.height - dep.height,
        "rank": rank.height,
        "rank_dep": rdep.height,
    }
    s["dep_by_month_airport"] = (
        pl.concat([dep, rdep])
        .with_columns(pl.col(MVT).dt.strftime("%Y-%m").alias("ym"))
        .group_by("ym", "ADEP_mvt")
        .len()
        .sort("ym", "ADEP_mvt")
        .rows()
    )

    def nulls(df: pl.DataFrame) -> dict:
        return {c: round(df[c].null_count() / df.height, 4) for c in df.columns}

    s["null_fraction"] = {
        "train_dep": nulls(dep),
        "train_arr": nulls(train.filter(pl.col("PHASE_mvt") == "ARR")),
        "rank_dep": nulls(rdep),
        "rank_arr": nulls(rank.filter(pl.col("PHASE_mvt") == "ARR")),
    }

    qs = [0, 0.001, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 0.999, 1]
    se = ((y - y.mean()) ** 2).sort(descending=True)
    s["target"] = {
        "definition_exact": bool(
            ((dep[MVT] - dep["BLOCK_TIME_UTC_mvt"]).dt.total_seconds() == dep[Y]).all()
        ),
        "mean": y.mean(),
        "std": y.std(),
        "quantiles": {str(q): y.quantile(q) for q in qs},
        "count_le_0": int((y <= 0).sum()),
        "count_lt_60": int((y < 60).sum()),
        "count_gt_3600": int((y > 3600).sum()),
        "count_gt_7200": int((y > 7200).sum()),
        "count_gt_86400": int((y > 86400).sum()),
        "sse_share_top_0p1pct_const_mean": se[: len(se) // 1000].sum() / se.sum(),
        "sse_share_top_1pct_const_mean": se[: len(se) // 100].sum() / se.sum(),
        "by_month": dep.group_by(pl.col(MVT).dt.month().alias("m"))
        .agg(pl.col(Y).mean().alias("mean"), pl.col(Y).std().alias("std"),
             pl.col(Y).median().alias("median"))
        .sort("m")
        .rows(),
        "by_airport": dep.group_by("ADEP_mvt")
        .agg(pl.len(), pl.col(Y).mean().alias("mean"), pl.col(Y).std().alias("std"),
             pl.col(Y).median().alias("median"))
        .sort("ADEP_mvt")
        .rows(),
    }

    # Proxies of the target built from non-blanked ranking columns.
    proxies = {}
    for c in ["AOBT_3_flt", "EOBT_1_flt", "LOBT_flt", "IOBT_flt", "SCHED_TIME_UTC_mvt"]:
        x = dep.select(
            (pl.col(MVT) - pl.col(c)).dt.total_seconds().cast(pl.Float64).alias("p"),
            pl.col(Y).cast(pl.Float64).alias("y"),
        ).drop_nulls()
        e = (x["p"] - x["y"]).to_numpy()
        proxies[f"MVT_minus_{c}"] = {
            "coverage": x.height / dep.height,
            "rmse": rmse(e),
            "mae": float(np.abs(e).mean()),
            "median_abs_err": float(np.median(np.abs(e))),
        }
    proxies["constant_mean"] = {"coverage": 1.0, "rmse": float(y.std(ddof=0))}
    blk = dep.select(
        (pl.col("BLOCK_TIME_UTC_mvt") - pl.col("AOBT_3_flt")).dt.total_seconds().alias("d")
    ).drop_nulls()["d"]
    proxies["BLOCK_minus_AOBT_3_quantiles"] = {
        str(q): blk.quantile(q) for q in [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
    }
    proxies["AOBT_3_whole_minute_share"] = float(dep["AOBT_3_flt"].dt.second().eq(0).mean())
    proxies["BLOCK_whole_minute_share"] = float(
        dep["BLOCK_TIME_UTC_mvt"].dt.second().eq(0).mean()
    )
    s["target_proxies"] = proxies

    # Identifier ordering: does MVT_ID encode off-block order beyond takeoff order?
    day = dep.with_columns(pl.col(MVT).dt.date().alias("day"))
    g = day.group_by("ADEP_mvt", "day").agg(
        *[
            pl.corr(pl.col("MVT_ID_mvt"), pl.col(c).dt.epoch("s"), method="spearman").alias(c)
            for c in [MVT, "BLOCK_TIME_UTC_mvt", "SCHED_TIME_UTC_mvt"]
        ]
    )
    rank_gap = day.with_columns(
        (
            pl.col("MVT_ID_mvt").rank().over("ADEP_mvt", "day")
            - pl.col(MVT).rank().over("ADEP_mvt", "day")
        ).alias("gap")
    )
    s["mvt_id_ordering"] = {
        "median_spearman_within_airport_day": g.select(
            pl.col(MVT, "BLOCK_TIME_UTC_mvt", "SCHED_TIME_UTC_mvt").median()
        ).row(0, named=True),
        "corr_idrank_minus_mvtrank_vs_target": rank_gap.select(pl.corr("gap", Y))[0, 0],
    }

    unseen = {}
    for c in ["RUNWAY_mvt", "STAND_mvt", "AIRCRAFT_TYPE_mvt", "AIRCRAFT_OPERATOR_flt",
              "ADES_mvt", "FLIGHT_mvt"]:
        seen = dep[c].drop_nulls().unique()
        r = rdep[c].drop_nulls()
        unseen[c] = {
            "train_levels": seen.len(),
            "rank_levels": r.n_unique(),
            "rank_dep_rows_unseen_share": float((~r.is_in(seen.implode())).mean()),
        }
    s["category_coverage_rank_vs_train"] = unseen

    s["categoricals"] = {
        c: dep[c].value_counts().sort("count", descending=True).rows()
        for c in ["FLIGHT_RULE_mvt", "FLIGHT_TYPE_flt", "MARKET_SEGMENT_flt", "WK_TBL_CAT_flt",
                  "FLIGHT_RULE_flt"]
    }
    s["consistency"] = {
        "dep_adep_not_in_10_airports": dep.filter(
            ~pl.col("ADEP_mvt").is_in(sorted(dep["ADEP_mvt"].unique().to_list()))
        ).height,
        "adep_mvt_ne_adep_flt": dep.filter(pl.col("ADEP_flt").is_not_null()
                                           & (pl.col("ADEP_mvt") != pl.col("ADEP_flt"))).height,
        "ades_mvt_ne_ades_flt": dep.filter(pl.col("ADES_flt").is_not_null()
                                           & (pl.col("ADES_mvt") != pl.col("ADES_flt"))).height,
        "aircraft_type_mvt_ne_flt": dep.filter(
            pl.col("AIRCRAFT_TYPE_flt").is_not_null()
            & (pl.col("AIRCRAFT_TYPE_mvt") != pl.col("AIRCRAFT_TYPE_flt"))
        ).height,
        "diverted_ades_filed_ne_ades_flt": dep.filter(
            pl.col("ADES_FILED_flt") != pl.col("ADES_flt")
        ).height,
        "duplicate_flight_id_dep": int(
            dep.filter(pl.col("FLIGHT_ID_mvt").is_not_null())["FLIGHT_ID_mvt"].is_duplicated().sum()
        ),
        "mvt_id_unique_train": dep["MVT_ID_mvt"].n_unique() == dep.height,
        "runway_na_rows": dep.filter(pl.col("RUNWAY_mvt").is_in(["NA", ""])).height,
        "sched_whole_minute_share": float(dep["SCHED_TIME_UTC_mvt"].dt.second().eq(0).mean()),
        "runways_per_airport": dep.group_by("ADEP_mvt").agg(pl.col("RUNWAY_mvt").n_unique())
        .sort("ADEP_mvt").rows(),
        "stands_per_airport": dep.group_by("ADEP_mvt").agg(pl.col("STAND_mvt").n_unique())
        .sort("ADEP_mvt").rows(),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(s, indent=1, default=str) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
