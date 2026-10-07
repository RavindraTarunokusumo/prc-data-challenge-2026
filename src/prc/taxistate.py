"""Day 9 taxi-state block: how long recent movements at the airport took.

The congestion block (prc.congestion) counts movements; this block measures their durations.
Every input is present identically for training, validation and ranking rows
(DATASET_AUDIT §6.2, §6.4). **No DEP block time or target is used.**

- ARR rows at the airport (ADES_mvt): taxi-in = BLOCK - MVT (in-block minus landing). ARR rows
  are complete in every month of the view, ranking included.
- Other DEP rows: MVT - AOBT_3 (takeoff minus the NM off-block estimate), only where AOBT_3 is
  present. It is a noisy proxy of their taxi-out, built from unblanked columns.

Durations are clipped to [0, CLIP_S] s before averaging. A feature is the mean over the events
in its window, and null when the window holds none.

The row's off-block proxy is t_off = coalesce(AOBT_3, EOBT_1, SCHED), as in prc.congestion.
Labels (DATASET_AUDIT §6.2):

P (known at t_off). Events are other rows only. The row's own contribution is removed exactly,
so a P feature does not depend on the row's own takeoff time
(tests/test_taxistate.py::test_p_features_invariant_to_own_takeoff).
  tx_arr_in_p30 / _p90   mean taxi-in of ARR in-blocked in [t_off - 30/90 min, t_off)
  tx_dep_p30 / _p90      mean MVT - AOBT_3 of other DEP airborne in [t_off - 30/90 min, t_off)
  tx_dep_rwy_p30         the same, on the row's runway, 30 min
T (in (t_off, t_to]; uses the row's own takeoff time):
  tx_arr_in_during       mean taxi-in of ARR in-blocked in (t_off, t_to)
  tx_dep_during          mean MVT - AOBT_3 of other DEP airborne in (t_off, t_to)
"""

from __future__ import annotations

import numpy as np
import polars as pl

P_FEATURES = ["tx_arr_in_p30", "tx_arr_in_p90", "tx_dep_p30", "tx_dep_p90", "tx_dep_rwy_p30"]
T_FEATURES = ["tx_arr_in_during", "tx_dep_during"]
FEATURES = P_FEATURES + T_FEATURES
CLIP_S = 3600.0
US = 1_000_000  # timestamps are handled as int64 microseconds
MIN = 60 * US


def _ts(col: str) -> pl.Expr:
    return pl.col(col).dt.epoch("us")


class _Events:
    """Events (time, value) sorted by time, with prefix sums for window sums and counts."""

    def __init__(self, t: np.ndarray, v: np.ndarray):
        order = np.argsort(t, kind="stable")
        self.t = t[order]
        self.csum = np.concatenate([[0.0], np.cumsum(v[order])])

    def window(self, lo: np.ndarray, hi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """(sum, count) of the values with time in [lo, hi); empty where hi <= lo."""
        a = np.searchsorted(self.t, lo, side="left")
        b = np.maximum(np.searchsorted(self.t, hi, side="left"), a)
        return self.csum[b] - self.csum[a], (b - a).astype(np.float64)


def _mean(s: np.ndarray, n: np.ndarray) -> np.ndarray:
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, s / np.where(n > 0, n, 1.0), np.nan)


def _airport_block(dep: pl.DataFrame, arr: pl.DataFrame) -> dict[str, np.ndarray]:
    t_to = dep["t_to"].to_numpy().astype(np.int64)
    t_off = dep["t_off"].to_numpy().astype(np.int64)
    has = dep["d_dep"].is_not_null().to_numpy()
    v_dep = np.clip(dep["d_dep"].fill_null(0.0).to_numpy(), 0.0, CLIP_S)
    ev_dep = _Events(t_to[has], v_dep[has])
    a = arr.drop_nulls(["t_land", "t_in"])
    ev_arr = _Events(a["t_in"].to_numpy().astype(np.int64),
                     np.clip((a["t_in"] - a["t_land"]).to_numpy() / US, 0.0, CLIP_S))

    out: dict[str, np.ndarray] = {}
    for w in (30, 90):
        lo = t_off - w * MIN
        s, n = ev_arr.window(lo, t_off)
        out[f"tx_arr_in_p{w}"] = _mean(s, n)
        s, n = ev_dep.window(lo, t_off)
        # remove row i's own takeoff if it lies in [t_off_i - w, t_off_i)
        own = has & (t_to >= lo) & (t_to < t_off)
        out[f"tx_dep_p{w}"] = _mean(s - np.where(own, v_dep, 0.0), n - own)
    # T: events strictly inside (t_off, t_to); row i's own takeoff (at t_to) is excluded by <
    s, n = ev_arr.window(t_off + 1, t_to)
    out["tx_arr_in_during"] = _mean(s, n)
    s, n = ev_dep.window(t_off + 1, t_to)
    out["tx_dep_during"] = _mean(s, n)

    rwy_p30 = np.full(dep.height, np.nan)
    rwy = dep["rwy"].to_numpy()
    for r in np.unique(rwy):
        idx = np.nonzero(rwy == r)[0]
        h = has[idx]
        ev = _Events(t_to[idx][h], v_dep[idx][h])
        lo = t_off[idx] - 30 * MIN
        s, n = ev.window(lo, t_off[idx])
        own = h & (t_to[idx] >= lo) & (t_to[idx] < t_off[idx])
        rwy_p30[idx] = _mean(s - np.where(own, v_dep[idx], 0.0), n - own)
    out["tx_dep_rwy_p30"] = rwy_p30
    return out


def taxistate(view: pl.LazyFrame) -> pl.DataFrame:
    """One row per DEP movement of the view: MVT_ID_mvt plus FEATURES (Float64; null where a
    window holds no event)."""
    dep = (view.filter(pl.col("PHASE_mvt") == "DEP")
           .select("MVT_ID_mvt", pl.col("ADEP_mvt").alias("apt"),
                   pl.col("RUNWAY_mvt").fill_null("NA").alias("rwy"),
                   _ts("MVT_TIME_UTC_mvt").alias("t_to"),
                   pl.coalesce(_ts("AOBT_3_flt"), _ts("EOBT_1_flt"),
                               _ts("SCHED_TIME_UTC_mvt")).alias("t_off"),
                   ((pl.col("MVT_TIME_UTC_mvt") - pl.col("AOBT_3_flt")).dt.total_seconds()
                    .cast(pl.Float64)).alias("d_dep"))
           .collect())
    arr = (view.filter(pl.col("PHASE_mvt") == "ARR")
           .select(pl.col("ADES_mvt").alias("apt"), _ts("MVT_TIME_UTC_mvt").alias("t_land"),
                   _ts("BLOCK_TIME_UTC_mvt").alias("t_in"))
           .collect())
    parts = []
    for apt in dep["apt"].unique().sort().to_list():
        d = dep.filter(pl.col("apt") == apt)
        feats = _airport_block(d, arr.filter(pl.col("apt") == apt))
        parts.append(pl.DataFrame({"MVT_ID_mvt": d["MVT_ID_mvt"], **feats}))
    return (pl.concat(parts).select("MVT_ID_mvt", *FEATURES).sort("MVT_ID_mvt")
            .with_columns(pl.col(FEATURES).fill_nan(None)))
