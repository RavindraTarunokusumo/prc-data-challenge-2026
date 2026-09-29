"""Day 3 congestion features: airport and runway traffic state around each departure.

Every feature is computed from the fold's masked view and uses only columns that are
present identically for training and validation rows (DATASET_AUDIT §6.2, §6.4):

- DEP rows (all, including the row itself): takeoff time MVT, runway, and the off-block
  proxy t_off = coalesce(AOBT_3, EOBT_1, SCHED) (DATASET_AUDIT §6.2, proxy for t_off);
  SCHED for scheduled demand. **Never another DEP row's block time or target.**
- ARR rows at the airport (ADES_mvt): landing time MVT and in-block time BLOCK (complete
  in training, validation and ranking).

Windows are counted over all rows of the view, so a validation row sees its own month and
any adjacent month the fold contains (the same information set as a ranking row, whose
view is its own month plus all of 2025). Months absent from the view (embargo, holdout)
are simply not counted.

Information labels (DATASET_AUDIT §6.2), relative to the row's own t_off proxy (P) and
takeoff t_to (T). Features whose label depends on the t_off proxy say so via the proxy.

P (known at t_off):
  cg_dep_taxiing       DEP j != i with t_off_j <= t_off_i < t_to_j (airborne later): aircraft
                       already off-block and not yet airborne at my off-block.
  cg_dep_taxiing_rwy   the same, restricted to my runway (runway is P by assumption).
  cg_dep_to_p15/_p30   takeoffs at the airport in [t_off_i - 15/30 min, t_off_i).
  cg_dep_to_rwy_p15    takeoffs on my runway in [t_off_i - 15 min, t_off_i).
  cg_dep_off_p15       other DEP off-blocks (proxy) in [t_off_i - 15 min, t_off_i).
  cg_arr_land_p15      ARR landings in [t_off_i - 15 min, t_off_i).
  cg_arr_taxiing       ARR with t_land <= t_off_i < t_inblock (taxiing in at my off-block).
  cg_sched_dep_n30     other DEP scheduled in [t_off_i, t_off_i + 30 min) (planned demand).
  cg_sched_arr_n30     ARR scheduled in [t_off_i, t_off_i + 30 min).
T (in (t_off, t_to]; uses the row's own takeoff time):
  cg_dep_to_during     other takeoffs at the airport in (t_off_i, t_to_i).
  cg_dep_to_rwy_during other takeoffs on my runway in (t_off_i, t_to_i).
  cg_arr_land_during   ARR landings in (t_off_i, t_to_i).
  cg_rwy_gap_prev      t_to_i - previous takeoff on my runway (s), capped at 3,600.
  cg_dep_to_rwy_m15    takeoffs on my runway in [t_to_i - 15 min, t_to_i).
"""

from __future__ import annotations

import numpy as np
import polars as pl

P_FEATURES = ["cg_dep_taxiing", "cg_dep_taxiing_rwy", "cg_dep_to_p15", "cg_dep_to_p30",
              "cg_dep_to_rwy_p15", "cg_dep_off_p15", "cg_arr_land_p15", "cg_arr_taxiing",
              "cg_sched_dep_n30", "cg_sched_arr_n30"]
T_FEATURES = ["cg_dep_to_during", "cg_dep_to_rwy_during", "cg_arr_land_during",
              "cg_rwy_gap_prev", "cg_dep_to_rwy_m15"]
FEATURES = P_FEATURES + T_FEATURES
GAP_CAP_S = 3600.0
US = 1_000_000  # timestamps are handled as int64 microseconds


def _count_le(sorted_x: np.ndarray, q: np.ndarray) -> np.ndarray:
    return np.searchsorted(sorted_x, q, side="right")


def _count_lt(sorted_x: np.ndarray, q: np.ndarray) -> np.ndarray:
    return np.searchsorted(sorted_x, q, side="left")


def _in_window(sorted_x: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> np.ndarray:
    """Number of x in [lo, hi)."""
    return _count_lt(sorted_x, hi) - _count_lt(sorted_x, lo)


def _ts(col: str) -> pl.Expr:
    return pl.col(col).dt.epoch("us")


def _dep_frame(view: pl.LazyFrame) -> pl.DataFrame:
    return (view.filter(pl.col("PHASE_mvt") == "DEP")
            .select("MVT_ID_mvt", pl.col("ADEP_mvt").alias("apt"),
                    pl.col("RUNWAY_mvt").fill_null("NA").alias("rwy"),
                    _ts("MVT_TIME_UTC_mvt").alias("t_to"),
                    pl.coalesce(_ts("AOBT_3_flt"), _ts("EOBT_1_flt"),
                                _ts("SCHED_TIME_UTC_mvt")).alias("t_off"),
                    _ts("SCHED_TIME_UTC_mvt").alias("t_sched"))
            .collect())


def _arr_frame(view: pl.LazyFrame) -> pl.DataFrame:
    return (view.filter(pl.col("PHASE_mvt") == "ARR")
            .select(pl.col("ADES_mvt").alias("apt"), _ts("MVT_TIME_UTC_mvt").alias("t_land"),
                    _ts("BLOCK_TIME_UTC_mvt").alias("t_in"),
                    _ts("SCHED_TIME_UTC_mvt").alias("t_sched"))
            .collect())


def _airport_block(dep: pl.DataFrame, arr: pl.DataFrame) -> dict[str, np.ndarray]:
    """Features for the DEP rows of one airport (dep, arr already filtered to it)."""
    m15, m30 = 15 * 60 * US, 30 * 60 * US
    t_to = dep["t_to"].to_numpy().astype(np.int64)
    t_off = dep["t_off"].to_numpy().astype(np.int64)
    s_to, s_off = np.sort(t_to), np.sort(t_off)
    # interval ends clamped to >= start, so start <= q < end is counted exactly even when
    # the off-block proxy lies after the takeoff (negative d_aobt3)
    s_end = np.sort(np.maximum(t_to, t_off))
    s_sched = np.sort(dep["t_sched"].drop_nulls().to_numpy().astype(np.int64))
    land = np.sort(arr["t_land"].drop_nulls().to_numpy().astype(np.int64))
    a = arr.drop_nulls(["t_land", "t_in"])
    a_land_s = np.sort(a["t_land"].to_numpy().astype(np.int64))
    a_in_s = np.sort(np.maximum(a["t_in"].to_numpy(), a["t_land"].to_numpy()).astype(np.int64))
    a_sched = np.sort(arr["t_sched"].drop_nulls().to_numpy().astype(np.int64))

    # Self term: row i always satisfies t_off_i <= t_off_i and is counted as taxiing unless
    # t_to_i <= t_off_i. The count subtracts 1 unconditionally and clips at 0, so a P
    # feature never reads the row's own takeoff time (rows with t_to_i <= t_off_i are
    # undercounted by one).
    out = {
        "cg_dep_taxiing": np.maximum(_count_le(s_off, t_off) - _count_le(s_end, t_off) - 1, 0),
        "cg_dep_to_p15": _in_window(s_to, t_off - m15, t_off),
        "cg_dep_to_p30": _in_window(s_to, t_off - m30, t_off),
        # other off-blocks in [t_off - 15, t_off): self is at t_off, outside the window
        "cg_dep_off_p15": _in_window(s_off, t_off - m15, t_off),
        "cg_arr_land_p15": _in_window(land, t_off - m15, t_off),
        "cg_arr_taxiing": np.maximum(_count_le(a_land_s, t_off) - _count_le(a_in_s, t_off), 0),
        "cg_arr_land_during": np.maximum(_in_window(land, t_off + 1, t_to), 0),
        "cg_sched_arr_n30": _in_window(a_sched, t_off, t_off + m30),
    }
    # scheduled DEP demand, excluding the row's own schedule if it falls in the window
    sched = dep["t_sched"].to_numpy().astype(np.int64)
    own = ((sched >= t_off) & (sched < t_off + m30)).astype(np.int64)
    out["cg_sched_dep_n30"] = _in_window(s_sched, t_off, t_off + m30) - own
    # takeoffs strictly inside (t_off, t_to), excluding self (self is at t_to, excluded by <)
    out["cg_dep_to_during"] = np.maximum(_in_window(s_to, t_off + 1, t_to), 0)

    rwy_cols = {k: np.zeros(dep.height, dtype=np.float64) for k in
                ("cg_dep_taxiing_rwy", "cg_dep_to_rwy_p15", "cg_dep_to_rwy_during",
                 "cg_rwy_gap_prev", "cg_dep_to_rwy_m15")}
    rwy = dep["rwy"].to_numpy()
    for r in np.unique(rwy):
        idx = np.nonzero(rwy == r)[0]
        rt_to, rt_off = t_to[idx], t_off[idx]
        rs_to, rs_off = np.sort(rt_to), np.sort(rt_off)
        rs_end = np.sort(np.maximum(rt_to, rt_off))
        rwy_cols["cg_dep_taxiing_rwy"][idx] = np.maximum(
            _count_le(rs_off, rt_off) - _count_le(rs_end, rt_off) - 1, 0)
        rwy_cols["cg_dep_to_rwy_p15"][idx] = _in_window(rs_to, rt_off - m15, rt_off)
        rwy_cols["cg_dep_to_rwy_during"][idx] = np.maximum(
            _in_window(rs_to, rt_off + 1, rt_to), 0)
        rwy_cols["cg_dep_to_rwy_m15"][idx] = _in_window(rs_to, rt_to - m15, rt_to)
        # previous takeoff on the runway strictly before t_to (ties: another row at the
        # same instant counts as previous with gap 0)
        k = _count_lt(rs_to, rt_to)
        prev = np.where(k > 0, rs_to[np.maximum(k - 1, 0)], np.iinfo(np.int64).min)
        gap = np.where(k > 0, (rt_to - prev) / US, GAP_CAP_S)
        rwy_cols["cg_rwy_gap_prev"][idx] = np.minimum(gap, GAP_CAP_S)
    out.update(rwy_cols)
    return {k: np.asarray(v, dtype=np.float64) for k, v in out.items()}


def congestion(view: pl.LazyFrame) -> pl.DataFrame:
    """One row per DEP movement of the view: MVT_ID_mvt plus FEATURES (Float64)."""
    dep = _dep_frame(view)
    arr = _arr_frame(view)
    parts = []
    for apt in dep["apt"].unique().sort().to_list():
        d = dep.filter(pl.col("apt") == apt)
        feats = _airport_block(d, arr.filter(pl.col("apt") == apt))
        parts.append(pl.DataFrame({"MVT_ID_mvt": d["MVT_ID_mvt"], **feats}))
    return pl.concat(parts).select("MVT_ID_mvt", *FEATURES).sort("MVT_ID_mvt")
