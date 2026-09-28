"""Day 2 descriptive EDA: static and temporal keys (brief §11, Day 2).

    uv run python scripts/eda_day2.py

Target hygiene: targets are read only for months that are never a validation month of
any frozen fold (FIT = Jan, Mar-Jun 2025; EVAL = Aug 2025). Feb (W1), Jul (S1),
Sep-Nov (R1-R3) and Dec (H, masked by load_silver) targets are not read. Ranking-file
coverage is target-free. Descriptive only: no model is fitted and no fold is scored.

For each key: levels, ranking DEP coverage, and the out-of-time RMSE on EVAL of a
shrunken within-airport key mean, on two residuals:
  - r_apt  = y - airport median (static signal on its own);
  - r_anch = y - (d_aobt3 + airport median of (y - d_aobt3)), NM-present rows only
    (signal left after the Day 1 anchor mechanism).
All on bulk rows (y < 3600 s). Writes research/day-02/eda/static_temporal.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl

from prc.data import load_silver
from prc.paths import RAW, ROOT

FIT = ["2025-01", "2025-03", "2025-04", "2025-05", "2025-06"]
EVAL = ["2025-08"]
BULK = 3600
SHRINK = 50  # pseudo-count toward the airport mean of the residual
TZ = {"EDDF": "Europe/Berlin", "EDDM": "Europe/Berlin", "EGLL": "Europe/London",
      "EHAM": "Europe/Amsterdam", "LEBL": "Europe/Madrid", "LEMD": "Europe/Madrid",
      "LFPG": "Europe/Paris", "LIRF": "Europe/Rome", "LSZH": "Europe/Zurich",
      "LTFM": "Europe/Istanbul"}
OUT = ROOT / "research" / "day-02" / "eda" / "static_temporal.json"


def local(col: str) -> pl.Expr:
    """Local wall-clock time of a UTC column at the departure airport."""
    parts = [pl.when(pl.col("ADEP_mvt") == a).then(pl.col(col).dt.convert_time_zone(tz)
                                                    .dt.replace_time_zone(None))
             for a, tz in TZ.items()]
    return pl.coalesce(parts)


def keys(df: pl.DataFrame | pl.LazyFrame):
    sched_loc = local("SCHED_TIME_UTC_mvt")
    return df.with_columns(
        pl.col("STAND_mvt").fill_null("NA").alias("stand"),
        pl.col("STAND_mvt").fill_null("NA").str.extract(r"^([A-Za-z]+)", 1)
        .fill_null("#").alias("stand_group"),
        pl.col("AIRCRAFT_TYPE_mvt").fill_null("UNK").alias("actype"),
        pl.col("WK_TBL_CAT_flt").fill_null("UNK").alias("wake"),
        pl.col("FLIGHT_mvt").str.slice(0, 3).fill_null("UNK").alias("op_prefix"),
        pl.col("AIRCRAFT_OPERATOR_flt").fill_null("UNK").alias("operator_nm"),
        pl.col("ADES_mvt").fill_null("UNK").alias("ades"),
        pl.col("ADES_mvt").str.slice(0, 2).fill_null("UN").alias("ades_region"),
        pl.col("RUNWAY_mvt").fill_null("NA").alias("runway"),
        (pl.col("STAND_mvt").fill_null("NA") + "_" + pl.col("RUNWAY_mvt").fill_null("NA"))
        .alias("stand_runway"),
        pl.col("FLIGHT_RULE_mvt").fill_null("UNK").alias("flight_rule"),
        pl.col("MARKET_SEGMENT_flt").fill_null("UNK").alias("market"),
        sched_loc.dt.hour().cast(pl.Utf8).alias("sched_hour_local"),
        pl.col("SCHED_TIME_UTC_mvt").dt.hour().cast(pl.Utf8).alias("sched_hour_utc"),
        sched_loc.dt.weekday().cast(pl.Utf8).alias("sched_weekday_local"),
        (sched_loc.dt.weekday().cast(pl.Utf8) + "_" + sched_loc.dt.hour().cast(pl.Utf8))
        .alias("sched_weekhour_local"),
        pl.col("MVT_TIME_UTC_mvt").dt.hour().cast(pl.Utf8).alias("mvt_hour_utc"),
    )


KEYS = ["stand", "stand_group", "stand_runway", "actype", "wake", "op_prefix", "operator_nm", "ades",
        "ades_region", "runway", "flight_rule", "market", "sched_hour_local",
        "sched_hour_utc", "sched_weekday_local", "sched_weekhour_local", "mvt_hour_utc"]
LABEL = {"mvt_hour_utc": "T"}  # everything else is P (row-own static or schedule)


def rmse(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(x**2)))


def key_gain(fit: pl.DataFrame, ev: pl.DataFrame, key: str, res: str) -> dict:
    """Out-of-time RMSE of res on EVAL before/after subtracting a shrunken
    within-airport key mean fitted on FIT."""
    g = (fit.group_by(["ADEP_mvt", key])
         .agg(pl.col(res).sum().alias("s"), pl.len().alias("n")))
    g = g.with_columns((pl.col("s") / (pl.col("n") + SHRINK)).alias("adj"))
    e = ev.join(g.select("ADEP_mvt", key, "adj"), on=["ADEP_mvt", key], how="left")
    base = e[res].to_numpy()
    after = base - e["adj"].fill_null(0).to_numpy()
    return {"rmse_before": rmse(base), "rmse_after": rmse(after),
            "gain_s": rmse(base) - rmse(after),
            "eval_unseen_share": float(e["adj"].is_null().mean())}


def main() -> None:
    s = load_silver()
    dep = keys(s.filter((pl.col("PHASE_mvt") == "DEP")
                        & pl.col("month").is_in(FIT + EVAL)))
    dep = dep.with_columns(
        pl.col("TAXITIME_SEC_mvt").cast(pl.Float64).alias("y"),
        (pl.col("MVT_TIME_UTC_mvt") - pl.col("AOBT_3_flt")).dt.total_seconds()
        .cast(pl.Float64).alias("d_aobt3"),
        (pl.col("MVT_TIME_UTC_mvt") - pl.col("SCHED_TIME_UTC_mvt")).dt.total_seconds()
        .cast(pl.Float64).alias("d_sched"),
    )
    fit, ev = (dep.filter(pl.col("month").is_in(m)) for m in (FIT, EVAL))
    fbulk = fit.filter(pl.col("y") < BULK)
    med = fbulk.group_by("ADEP_mvt").agg(pl.col("y").median().alias("apt_med"))
    off = (fbulk.drop_nulls("d_aobt3").group_by("ADEP_mvt")
           .agg((pl.col("y") - pl.col("d_aobt3")).median().alias("anch_off")))

    def residuals(df):
        return (df.filter(pl.col("y") < BULK).join(med, on="ADEP_mvt").join(off, on="ADEP_mvt")
                .with_columns((pl.col("y") - pl.col("apt_med")).alias("r_apt"),
                              (pl.col("y") - pl.col("d_aobt3") - pl.col("anch_off"))
                              .alias("r_anch")))

    rf, re_ = residuals(fit), residuals(ev)
    rfa, rea = rf.drop_nulls("r_anch"), re_.drop_nulls("r_anch")

    rank = keys(pl.read_parquet(RAW / "ranking.parquet").lazy()
                .filter(pl.col("PHASE_mvt") == "DEP")).collect()
    train_all = keys(s.filter(pl.col("PHASE_mvt") == "DEP").select(
        "ADEP_mvt", "STAND_mvt", "AIRCRAFT_TYPE_mvt", "WK_TBL_CAT_flt", "FLIGHT_mvt",
        "AIRCRAFT_OPERATOR_flt", "ADES_mvt", "RUNWAY_mvt", "FLIGHT_RULE_mvt",
        "MARKET_SEGMENT_flt", "SCHED_TIME_UTC_mvt", "MVT_TIME_UTC_mvt"))

    out = {"fit_months": FIT, "eval_months": EVAL, "bulk_max_s": BULK,
           "shrink_pseudocount": SHRINK,
           "eval_rows_bulk": re_.height, "eval_rows_bulk_nm_present": rea.height,
           "keys": {}}
    for k in KEYS:
        seen = set(train_all[k].unique().to_list())
        out["keys"][k] = {
            "label": LABEL.get(k, "P"),
            "levels_train_jan_nov": len(seen),
            "ranking_dep_unseen_share": float((~rank[k].is_in(list(seen))).mean()),
            "r_apt": key_gain(rf, re_, k, "r_apt"),
            "r_anch_nm_present": key_gain(rfa, rea, k, "r_anch"),
        }
        print(f"{k:22s} base {out['keys'][k]['r_apt']['rmse_before']:6.1f}/"
              f"{out['keys'][k]['r_anch_nm_present']['rmse_before']:6.1f} lv {len(seen):5d}  apt-gain {out['keys'][k]['r_apt']['gain_s']:6.1f}"
              f"  anch-gain {out['keys'][k]['r_anch_nm_present']['gain_s']:6.1f}", flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
