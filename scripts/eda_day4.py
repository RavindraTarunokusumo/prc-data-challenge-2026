"""Day 4 descriptive EDA: candidate keys for fold-local historical target priors.

    uv run python scripts/eda_day4.py

Target hygiene (as scripts/eda_day2.py / eda_day3.py): targets are read ONLY for months that
are never a validation month of any frozen fold (Jan, Mar, Apr, May, Jun, Aug 2025). Targets
of every other month are nulled right after load_silver (December is masked by load_silver
anyway) and `target_rows` asserts the month set before any target is used. Section A is
target-free and uses all months. No model is fitted beyond tiny OLS calibrations and no
frozen fold is scored. DEP rows only.

Keys are built from the existing FS1 builder (prc.features.fs1) on a view where every row has
role 'train'. The builder's rare-level collapse (RARE_MIN=100) is switched off in this process
(identity replacement of prc.features.collapse_rare) so coverage/novelty is measured on raw
levels; the columns themselves come from the builder. All keys are airport-qualified.

Sections:
A. Target-free: cardinality (all months) and, per validation/ranking month, the share of DEP
   rows whose key has >=1, >=30, >=100 DEP rows in the fold's training months (frozen
   config/splits.yaml; ranking months use all of 2025-01..12).
B. Target-based (bulk y<3600, NM-present): statistics fit on FITA={01,03,04,05}, evaluated
   on EVB={06,08}: smoothed mean (m=50 toward airport mean), median (n>=30 else airport
   median), q20 (n>=30 else airport q20). RMSE and R2 of the statistic as a predictor; the
   incremental R2 of OLS y ~ [K1 mean, Kx stat] over y ~ [K1 mean] (cross-fitted between the
   two eval months); the correlation of the residual of y after K1 mean with the residual of
   Kx stat after K1 mean; stability of key means fit on {01,03} vs {04,05}.
C. Unimpeded taxi proxy: K5 (stand x runway) q20, alone and on top of K1.
D. NM-missing rows: RMSE of the K1 prior on LIRF vs other airports (context only).
E. Joint keys: cross-fit OLS R2 (same protocol as B) of y on the smoothed-mean priors of a set
   of keys jointly (e.g. [K1,K5]), same fit/eval months and rows as B. Written to
   priors_joint.json and appended to priors_summary.md (sections A-D outputs unchanged).
Writes research/day-04/eda/priors.json, priors_joint.json and priors_summary.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl
import yaml

import prc.features as F
from prc.data import load_silver
from prc.paths import ROOT

NEVER_VAL = ["2025-01", "2025-03", "2025-04", "2025-05", "2025-06", "2025-08"]
FITA = ["2025-01", "2025-03", "2025-04", "2025-05"]
EVB = ["2025-06", "2025-08"]
STAB_A, STAB_B = ["2025-01", "2025-03"], ["2025-04", "2025-05"]
BULK = 3600
M_SMOOTH = 50
MIN_N = 30
OUT = ROOT / "research" / "day-04" / "eda"
COV_T = (1, 30, 100)
RANKING = {"2026-01": "SUBMIT_JAN", "2026-07": "SUBMIT_JUL"}

KEYS = {
    "K1": ["ADEP_mvt", "sched_hour_local"],
    "K2": ["airport_runway"],
    "K3": ["airport_runway", "sched_hour_local"],
    "K4": ["ADEP_mvt", "stand"],
    "K5": ["ADEP_mvt", "stand", "airport_runway"],
    "K6": ["ADEP_mvt", "op_prefix"],
    "K7": ["ADEP_mvt", "actype"],
    "K8": ["ADEP_mvt", "WK_TBL_CAT_flt", "airport_runway"],
    "K9": ["ADEP_mvt", "ades"],
}
COLS = ["MVT_ID_mvt", "month", "PHASE_mvt", "TAXITIME_SEC_mvt", "ADEP_mvt", "RUNWAY_mvt",
        "WK_TBL_CAT_flt", "MARKET_SEGMENT_flt", "FLIGHT_TYPE_flt", "MVT_TIME_UTC_mvt",
        "AOBT_3_flt", "EOBT_1_flt", "SCHED_TIME_UTC_mvt", "STAND_mvt", "AIRCRAFT_TYPE_mvt",
        "FLIGHT_mvt", "ADES_mvt"]


def build() -> pl.DataFrame:
    s = load_silver(COLS)
    keep = pl.col("month").is_in(NEVER_VAL)
    s = s.with_columns(pl.when(keep).then(pl.col("TAXITIME_SEC_mvt")).alias("TAXITIME_SEC_mvt"))
    chk = s.filter(pl.col("TAXITIME_SEC_mvt").is_not_null())["month"].unique().to_list()
    assert set(chk) <= set(NEVER_VAL), chk
    F.collapse_rare = lambda feats, cols, min_rows=0: feats  # raw levels for coverage
    feats = F.fs1(s.lazy().with_columns(pl.lit("train").alias("role")))
    assert set(feats.filter(pl.col("y").is_not_null())["month"].unique()) <= set(NEVER_VAL)
    return feats.with_columns(
        [pl.concat_str([pl.col(c).cast(pl.Utf8) for c in cols], separator="|").alias(k)
         for k, cols in KEYS.items()])


def target_rows(df: pl.DataFrame, months: list[str]) -> pl.DataFrame:
    assert set(months) <= set(NEVER_VAL), months
    return df.filter(pl.col("month").is_in(months))


def fold_train_months() -> dict[str, tuple[list[str], list[str]]]:
    cfg = yaml.safe_load((ROOT / "config" / "splits.yaml").read_text())
    out = {}
    for sec in ("development_folds", "diagnostic_folds", "protected_holdout", "final"):
        for name, f in cfg[sec].items():
            out[name] = (f["train_months"], f["val_months"])
    return out


def coverage(feats: pl.DataFrame) -> dict:
    folds = fold_train_months()
    plan = {"2025-02 (W1)": "W1", "2025-07 (S1)": "S1", "2025-09 (R1)": "R1", "2025-10 (R2)": "R2",
            "2025-11 (R3)": "R3", "2025-12 (H, count-only)": "H",
            "2026-01 (rank)": "SUBMIT_JAN", "2026-07 (rank)": "SUBMIT_JUL"}
    out: dict = {}
    for k in KEYS:
        cnt = feats.group_by(k, "month").len()
        res = {"cardinality_all_months": int(feats[k].n_unique())}
        for label, fold in plan.items():
            tr, va = folds[fold]
            trc = cnt.filter(pl.col("month").is_in(tr)).group_by(k).agg(pl.col("len").sum().alias("n"))
            vc = cnt.filter(pl.col("month") == va[0]).join(trc, on=k, how="left").with_columns(
                pl.col("n").fill_null(0))
            tot = vc["len"].sum()
            res[label] = {"rows": int(tot), "val_keys": int(vc.height)} | {
                f"share_ge{t}": float(vc.filter(pl.col("n") >= t)["len"].sum() / tot)
                for t in COV_T}
        out[k] = res
    return out


def airport_stats(fit: pl.DataFrame) -> pl.DataFrame:
    return fit.group_by("ADEP_mvt").agg(pl.col("y").mean().alias("a_mean"),
                                        pl.col("y").median().alias("a_med"),
                                        pl.col("y").quantile(0.2).alias("a_q20"))


def priors(fit: pl.DataFrame, ev: pl.DataFrame, key: str) -> pl.DataFrame:
    """Return ev with columns n, p_mean, p_med, p_q20 fitted on fit rows only."""
    ap = airport_stats(fit)
    st = fit.group_by(key).agg(pl.len().alias("n"), pl.col("y").mean().alias("k_mean"),
                               pl.col("y").median().alias("k_med"),
                               pl.col("y").quantile(0.2).alias("k_q20"))
    e = ev.join(ap, on="ADEP_mvt", how="left").join(st, on=key, how="left")
    n = pl.col("n").fill_null(0)
    return e.with_columns(
        n.alias("n"),
        pl.when(n > 0).then((n * pl.col("k_mean") + M_SMOOTH * pl.col("a_mean")) / (n + M_SMOOTH))
        .otherwise(pl.col("a_mean")).alias("p_mean"),
        pl.when(n >= MIN_N).then(pl.col("k_med")).otherwise(pl.col("a_med")).alias("p_med"),
        pl.when(n >= MIN_N).then(pl.col("k_q20")).otherwise(pl.col("a_q20")).alias("p_q20"))


def r2(y, p):
    return float(1 - np.sum((y - p) ** 2) / np.sum((y - y.mean()) ** 2))


def rmse(y, p):
    return float(np.sqrt(np.mean((y - p) ** 2)))


def crossfit_r2(y, X, month) -> float:
    """OLS fitted on one eval month, scored on the other; pooled R2 over both."""
    sse = sst = 0.0
    for m in np.unique(month):
        tr, te = month != m, month == m
        A = np.column_stack([np.ones(tr.sum()), X[tr]])
        b = np.linalg.lstsq(A, y[tr], rcond=None)[0]
        p = np.column_stack([np.ones(te.sum()), X[te]]) @ b
        sse += np.sum((y[te] - p) ** 2)
        sst += np.sum((y[te] - y[te].mean()) ** 2)
    return float(1 - sse / sst)


def section_b(base: pl.DataFrame) -> tuple[dict, dict]:
    fit = target_rows(base, FITA)
    ev = target_rows(base, EVB)
    p1 = priors(fit, ev, "K1")
    y = p1["y"].to_numpy()
    mon = p1["month"].to_numpy()
    k1 = p1["p_mean"].to_numpy()
    base_r2 = crossfit_r2(y, k1[:, None], mon)
    res: dict = {"eval_rows": len(y), "fit_rows": int(fit.height),
                 "k1_mean_alone_crossfit_r2": base_r2,
                 "y_sd_eval": float(y.std())}
    cols = {"mean": "p_mean", "median": "p_med", "q20": "p_q20"}
    resid1 = y - k1
    priors_by_key = {}
    for k in KEYS:
        pk = priors(fit, ev, k)
        assert np.array_equal(pk["MVT_ID_mvt"].to_numpy(), p1["MVT_ID_mvt"].to_numpy())
        priors_by_key[k] = pk
        r = {"eval_share_n_ge30": float((pk["n"] >= MIN_N).mean()),
             "eval_share_unseen": float((pk["n"] == 0).mean())}
        for sname, c in cols.items():
            p = pk[c].to_numpy()
            d = p - k1
            r[sname] = {
                "rmse_alone": rmse(y, p), "r2_alone": r2(y, p),
                "incremental_r2_over_k1_mean": crossfit_r2(y, np.column_stack([k1, p]), mon) - base_r2,
                "corr_resid_vs_prior_minus_k1": float(np.corrcoef(resid1, d)[0, 1]) if d.std() > 0 else None,
            }
        res[k] = r
    return res, priors_by_key


def wcorr(x, z, w) -> float:
    mx, mz = np.average(x, weights=w), np.average(z, weights=w)
    return float(np.sum(w * (x - mx) * (z - mz)) /
                 np.sqrt(np.sum(w * (x - mx) ** 2) * np.sum(w * (z - mz) ** 2)))


def stability(base: pl.DataFrame) -> dict:
    a, b = target_rows(base, STAB_A), target_rows(base, STAB_B)
    apm = a.group_by("ADEP_mvt").agg(pl.col("y").mean().alias("am_a")).join(
        b.group_by("ADEP_mvt").agg(pl.col("y").mean().alias("am_b")), on="ADEP_mvt")
    out = {}
    for k in KEYS:
        ga = a.group_by(k, "ADEP_mvt").agg(pl.len().alias("na"), pl.col("y").mean().alias("ma"))
        gb = b.group_by(k, "ADEP_mvt").agg(pl.len().alias("nb"), pl.col("y").mean().alias("mb"))
        j = ga.join(gb, on=[k, "ADEP_mvt"]).filter((pl.col("na") >= MIN_N) & (pl.col("nb") >= MIN_N))
        j = j.join(apm, on="ADEP_mvt")
        ma, mb = j["ma"].to_numpy(), j["mb"].to_numpy()
        wa = ma - j["am_a"].to_numpy()
        wb = mb - j["am_b"].to_numpy()
        w = np.sqrt(j["na"].to_numpy() * j["nb"].to_numpy())

        out[k] = {"keys_both_ge30": int(j.height),
                  "corr_raw": float(np.corrcoef(ma, mb)[0, 1]),
                  "corr_within_airport": float(np.corrcoef(wa, wb)[0, 1]),
                  "wcorr_within_airport": wcorr(wa, wb, w),
                  "share_rows_b_covered": float(j["nb"].sum() / b.height)}
    return out


def section_d(feats: pl.DataFrame) -> dict:
    fit = target_rows(feats, FITA).filter((pl.col("flt_missing") == 0) & (pl.col("y") < BULK))
    ev = target_rows(feats, EVB).filter(pl.col("flt_missing") == 1)
    p = priors(fit, ev, "K1")
    out = {}
    for name, m in (("LIRF", pl.col("ADEP_mvt") == "LIRF"), ("non_LIRF", pl.col("ADEP_mvt") != "LIRF")):
        d = p.filter(m)
        db = d.filter(pl.col("y") < BULK)
        out[name] = {"rows": d.height, "rmse_k1_all_rows": rmse(d["y"].to_numpy(), d["p_mean"].to_numpy()),
                     "y_mean_all": float(d["y"].mean()),
                     "bulk_rows": db.height,
                     "rmse_k1_bulk": rmse(db["y"].to_numpy(), db["p_mean"].to_numpy()),
                     "y_mean_bulk": float(db["y"].mean())}
    return out


JOINT_SETS = [["K1"], ["K1", "K5"], ["K1", "K4", "K5"], ["K1", "K5", "K3"], ["K1", "K5", "K6"],
              ["K1", "K5", "K7"], ["K1", "K5", "K9"], ["K1", "K5", "K8"],
              ["K1", "K5", "K3", "K6", "K7"], ["K1", "K5", "K3", "K6", "K7", "K9"],
              ["K1", "K5", "K3", "K6", "K7", "K8", "K9"],
              ["K1", "K4", "K5", "K3", "K6", "K7", "K8", "K9"]]


def section_joint(pbk: dict) -> dict:
    """Cross-fit R2 of OLS y ~ [p_mean of each key in the set] (protocol of section B)."""
    y = pbk["K1"]["y"].to_numpy()
    mon = pbk["K1"]["month"].to_numpy()
    out = {}
    for ks in JOINT_SETS:
        X = np.column_stack([pbk[k]["p_mean"].to_numpy() for k in ks])
        out["+".join(ks)] = {"keys": ks, "crossfit_r2": crossfit_r2(y, X, mon)}
    return {"eval_rows": len(y), "fit_months": FITA, "eval_months": EVB,
            "protocol": "OLS on smoothed-mean priors (m=50), fit on one eval month, scored on the "
                        "other, pooled R2; bulk NM-present rows", "sets": out}


def md_table(rows: list[list], head: list[str]) -> str:
    f = lambda v: "-" if v is None else (f"{v:.4f}" if isinstance(v, float) and abs(v) < 10 else
                                         f"{v:.1f}" if isinstance(v, float) else str(v))
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
                     + ["| " + " | ".join(f(v) for v in r) + " |" for r in rows])


def main() -> None:
    feats = build()
    print("built", feats.height, "rows")
    out: dict = {"never_validation_months": NEVER_VAL, "fit_months": FITA, "eval_months": EVB,
                 "keys": {k: v for k, v in KEYS.items()}, "bulk_max_s": BULK,
                 "smoothing_m": M_SMOOTH, "min_n": MIN_N,
                 "note": "K2 airport_runway is already airport-qualified (ADEP_RUNWAY)."}
    out["A_coverage"] = coverage(feats)
    base = target_rows(feats, FITA + EVB).filter((pl.col("flt_missing") == 0) & (pl.col("y") < BULK))
    out["rows_bulk_nm_present"] = {"fit": int(base.filter(pl.col("month").is_in(FITA)).height),
                                   "eval": int(base.filter(pl.col("month").is_in(EVB)).height)}
    b, pbk = section_b(base)
    out["B_prior_eval"] = b
    out["B_stability"] = stability(base)
    # C: K5 q20 as unimpeded-taxi proxy
    y = pbk["K1"]["y"].to_numpy()
    k1 = pbk["K1"]["p_mean"].to_numpy()
    mon = pbk["K1"]["month"].to_numpy()
    k5 = pbk["K5"]
    q = k5["p_q20"].to_numpy()
    kb = crossfit_r2(y, k1[:, None], mon)
    out["C_unimpeded_k5_q20"] = {
        "r2_alone_as_predictor": r2(y, q), "rmse_alone": rmse(y, q),
        "r2_alone_linear_crossfit": crossfit_r2(y, q[:, None], mon),
        "r2_k1_mean_crossfit": kb,
        "r2_k1_plus_k5q20_crossfit": crossfit_r2(y, np.column_stack([k1, q]), mon),
        "incremental_over_k1": crossfit_r2(y, np.column_stack([k1, q]), mon) - kb,
        "share_eval_rows_k5_n_ge30": float((k5["n"] >= MIN_N).mean()),
        "n_k5_groups_fit_ge30": int(target_rows(base, FITA).group_by("K5").len().filter(pl.col("len") >= MIN_N).height),
        "note": "q20 of y per stand x runway on bulk NM-present rows, airport q20 fallback for n<30 "
                "(descriptive proxy for PRU/ANSP unimpeded taxi time)."}
    out["D_nm_missing_k1_context"] = section_d(feats)

    joint = section_joint(pbk)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "priors_joint.json").write_text(json.dumps(joint, indent=1) + "\n")
    (OUT / "priors.json").write_text(json.dumps(out, indent=1) + "\n")

    A, B, S = out["A_coverage"], out["B_prior_eval"], out["B_stability"]
    md = ["# Day 4 EDA: candidate prior keys", "",
          (f"Targets read only for {', '.join(NEVER_VAL)}. Fit {FITA}, eval {EVB}, bulk y<3600, "
           f"NM-present. Eval rows {B['eval_rows']:,}; K1 mean alone (cross-fit R2) "
           f"{B['k1_mean_alone_crossfit_r2']:.4f}."), "",
          "## A. Coverage (share of DEP rows with key count >= 30 / >= 1 in training months)", ""]
    labs = [k for k in A["K1"] if k not in ("cardinality_all_months",)]
    md.append(md_table([[k, A[k]["cardinality_all_months"]] + [
        f"{A[k][l]['share_ge30']:.3f}/{A[k][l]['share_ge1']:.3f}" for l in labs] for k in KEYS],
        ["key", "card"] + labs))
    md += ["", "## B. Prior quality on 06+08 (incr = cross-fit R2 gain over K1 mean; corr = residual corr)", ""]
    rows = []
    for k in KEYS:
        r = B[k]
        rows.append([k, r["eval_share_n_ge30"]] + [v for s in ("mean", "median", "q20") for v in
                     (r[s]["rmse_alone"], r[s]["r2_alone"], r[s]["incremental_r2_over_k1_mean"],
                      r[s]["corr_resid_vs_prior_minus_k1"])]
                    + [S[k]["keys_both_ge30"], S[k]["corr_raw"], S[k]["corr_within_airport"],
                       S[k]["share_rows_b_covered"]])
    md.append(md_table(rows, ["key", "eval n>=30", "mean rmse", "R2", "incr", "corr", "med rmse", "R2",
                              "incr", "corr", "q20 rmse", "R2", "incr", "corr", "stab keys", "stab raw",
                              "stab within-apt", "stab cover"]))
    C, D = out["C_unimpeded_k5_q20"], out["D_nm_missing_k1_context"]
    md += ["", "## C. K5 q20 unimpeded proxy", "", "```", json.dumps(C, indent=1), "```", "",
           "## D. K1 prior on NM-missing rows (context only)", "", "```", json.dumps(D, indent=1), "```", ""]
    md += ["## E. Joint keys (cross-fit R2, OLS on smoothed-mean priors, 06+08)", "",
           md_table([[" + ".join(v["keys"]), v["crossfit_r2"]] for v in joint["sets"].values()],
                    ["key set", "R2"]), ""]
    (OUT / "priors_summary.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
