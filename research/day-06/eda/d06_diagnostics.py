"""Day 6 diagnostics: prediction diversity of two experiments, and closed-set parameter diff.

Implemented by a claude-sonnet-5-5 worker to the researcher's specification; reviewed by the researcher (INC-0013).

    uv run python research/day-06/eda/d06_diagnostics.py diversity BASE SECOND [SECOND ...] --out PATH
    uv run python research/day-06/eda/d06_diagnostics.py closed-set CAND REF --out PATH

diversity: BASE is E029. For each SECOND experiment and each of the folds R1, R2, R3, S1, W1,
S1c, W1c (never H, never a final fold), loads BASE and SECOND stored predictions
(prc.blending.stored_predictions, manifest-verified), joins them 1:1 to the truth frame
(prc.evaluate.truth_frame, as scripts/mechanism_check.py obtains it) and reports, on the
populations all / bulk (y < BULK_MAX_S) / NM_present_excl_LIRF (prc.attribution.population_mask):
n rows, Pearson correlation of residuals (y - p1) vs (y - p2), MSE1, MSE2, ambiguity
A = mean((p1 - p2)^2) and the exact 0.5/0.5 decomposition
MSE_blend = 0.5 MSE1 + 0.5 MSE2 - 0.25 A, with RMSE_blend from it and a direct check
RMSE of 0.5 p1 + 0.5 p2 (must agree to 1e-9 relative). Descriptive only: never a promotion
decision. Writes JSON schema "d06-diversity-v1".

closed-set: compares experiments/CAND/resolved_params.json with experiments/REF/... per fold
(canonical JSON values). Pre-registered verdict: allowed_differences = ["max_ctr_complexity"];
violation = any key present in only one arm, or any differing key not in allowed_differences,
on any fold. Reads only those two JSON files. Writes JSON schema "d06-closed-set-v1".
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for d in (*here.parents, Path.cwd().resolve(), *Path.cwd().resolve().parents):
        if (d / "pyproject.toml").exists():
            return d
    raise RuntimeError("repo root (pyproject.toml) not found above this script")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT / "src"))

import numpy as np
import polars as pl

from prc.attribution import population_mask
from prc.blending import stored_predictions
from prc.data import load_silver
from prc.evaluate import truth_frame
from prc.metrics import BULK_MAX_S, PRED, TARGET

FOLDS = ("R1", "R2", "R3", "S1", "W1", "S1c", "W1c")
POPS = ("all", "bulk", "NM_present_excl_LIRF")
ID = "MVT_ID_mvt"
ALLOWED_DIFFERENCES = ["max_ctr_complexity"]
REL_TOL = 1e-9


def _pearson(a: np.ndarray, b: np.ndarray) -> float | None:
    if a.size < 2:
        return None
    sa, sb = a.std(), b.std()
    if sa == 0.0 or sb == 0.0:
        return None
    return float(np.mean((a - a.mean()) * (b - b.mean())) / (sa * sb))


def pop_stats(y: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> dict:
    """Diversity statistics of two prediction vectors on one population."""
    n = int(y.size)
    if n == 0:
        return {"n": 0, "residual_corr": None, "mse1": None, "mse2": None, "ambiguity": None,
                "mse_blend_decomp": None, "rmse_blend_decomp": None,
                "rmse_blend_direct": None, "blend_check_rel_diff": None}
    r1, r2 = y - p1, y - p2
    mse1, mse2 = float(np.mean(r1**2)), float(np.mean(r2**2))
    amb = float(np.mean((p1 - p2) ** 2))
    mse_b = 0.5 * mse1 + 0.5 * mse2 - 0.25 * amb
    rmse_b = float(np.sqrt(max(mse_b, 0.0)))
    direct = float(np.sqrt(np.mean((y - (0.5 * p1 + 0.5 * p2)) ** 2)))
    rel = abs(rmse_b - direct) / direct if direct > 0 else abs(rmse_b - direct)
    if rel > REL_TOL:
        raise AssertionError(f"0.5/0.5 decomposition check failed: rel diff {rel:.3e}")
    return {"n": n, "residual_corr": _pearson(r1, r2), "mse1": mse1, "mse2": mse2,
            "ambiguity": amb, "mse_blend_decomp": mse_b, "rmse_blend_decomp": rmse_b,
            "rmse_blend_direct": direct, "blend_check_rel_diff": float(rel)}


def _joined(truth: pl.DataFrame, eid: str, fold: str) -> pl.DataFrame:
    """Truth rows joined 1:1 with one experiment's stored predictions (same row set)."""
    p = stored_predictions(eid, fold).select(pl.col(ID).cast(pl.Int64),
                                             pl.col(PRED).cast(pl.Float64))
    j = truth.join(p, on=ID, how="inner", validate="1:1")
    assert j.height == truth.height == p.height, \
        f"{eid} {fold}: row sets differ (truth {truth.height}, pred {p.height}, joined {j.height})"
    assert j[PRED].null_count() == 0 and j[TARGET].null_count() == 0, \
        f"{eid} {fold}: nulls after join"
    return j.sort(ID)


def diversity(base: str, seconds: list[str]) -> dict:
    silver = (load_silver(columns=[ID, "AOBT_3_flt", "PHASE_mvt"])
              .filter(pl.col("PHASE_mvt") == "DEP")
              .select(ID, pl.col("AOBT_3_flt").is_null().alias("nm_missing")))
    pairs: dict[str, dict] = {s: {} for s in seconds}
    for f in FOLDS:
        t = (truth_frame(f).select(ID, TARGET, "ADEP_mvt")
             .join(silver, on=ID, how="left", validate="1:1"))
        assert t["nm_missing"].null_count() == 0, f"{f}: truth rows missing from silver"
        t = t.sort(ID)
        masks = {"all": np.ones(t.height, dtype=bool),
                 "NM_present_excl_LIRF": population_mask(t, "NM_present_excl_LIRF").to_numpy()}
        y = t[TARGET].cast(pl.Float64).to_numpy()
        masks["bulk"] = y < BULK_MAX_S
        j1 = _joined(t.select(ID, TARGET), base, f)
        assert np.array_equal(j1[ID].to_numpy(), t[ID].to_numpy())
        p1 = j1[PRED].to_numpy()
        for s in seconds:
            j2 = _joined(t.select(ID, TARGET), s, f)
            assert np.array_equal(j2[ID].to_numpy(), j1[ID].to_numpy()), \
                f"{base} vs {s} {f}: row sets differ"
            p2 = j2[PRED].to_numpy()
            pairs[s][f] = {pop: pop_stats(y[m], p1[m], p2[m]) for pop, m in
                           ((pop, masks[pop]) for pop in POPS)}
    return {"schema": "d06-diversity-v1", "base": base,
            "note": ("Residual correlation and exact 0.5/0.5 blend decomposition "
                     "MSE_blend = 0.5 MSE1 + 0.5 MSE2 - 0.25 A (A = mean((p1-p2)^2)); p1 = base, "
                     "p2 = second; bulk = y < BULK_MAX_S; descriptive, not a promotion decision"),
            "pairs": pairs}


def _canon(v: object) -> str:
    return json.dumps(v, sort_keys=True)


def closed_set(cand: str, ref: str) -> dict:
    rc = json.loads((ROOT / "experiments" / cand / "resolved_params.json").read_text())
    rr = json.loads((ROOT / "experiments" / ref / "resolved_params.json").read_text())
    return closed_set_from(cand, ref, rc, rr)


def closed_set_from(cand: str, ref: str, rc: dict, rr: dict) -> dict:
    per_fold, violations = {}, []
    folds = list(rc) + [f for f in rr if f not in rc]
    for f in folds:
        c, r = rc.get(f), rr.get(f)
        if c is None or r is None:
            per_fold[f] = {"present_in": "candidate" if r is None else "reference"}
            violations.append(f"{f}: fold present only in "
                              f"{'candidate' if r is None else 'reference'}")
            continue
        only_c = sorted(set(c) - set(r))
        only_r = sorted(set(r) - set(c))
        both = sorted(set(c) & set(r))
        differ = {k: {"candidate": c[k], "reference": r[k]} for k in both
                  if _canon(c[k]) != _canon(r[k])}
        per_fold[f] = {"only_in_candidate": only_c, "only_in_reference": only_r,
                       "differ": differ, "n_equal": len(both) - len(differ)}
        violations += [f"{f}: key only in candidate: {k}" for k in only_c]
        violations += [f"{f}: key only in reference: {k}" for k in only_r]
        violations += [f"{f}: differing key outside allowed set: {k}" for k in differ
                       if k not in ALLOWED_DIFFERENCES]
    return {"schema": "d06-closed-set-v1", "candidate": cand, "reference": ref,
            "allowed_differences": ALLOWED_DIFFERENCES, "per_fold": per_fold,
            "violation": bool(violations), "violations": violations}


def _fmt(x: float | None, spec: str) -> str:
    return "   n/a" if x is None else format(x, spec)


def print_diversity(res: dict) -> None:
    for s, folds in res["pairs"].items():
        print(f"{res['base']} vs {s}")
        print(f"  {'fold':4s} {'pop':21s} {'n':>7s} {'corr':>7s} {'rmse1':>8s} {'rmse2':>8s} "
              f"{'amb':>10s} {'rmse_bl':>8s}")
        for f, pops in folds.items():
            for pop, d in pops.items():
                r1 = None if d["mse1"] is None else d["mse1"] ** 0.5
                r2 = None if d["mse2"] is None else d["mse2"] ** 0.5
                print(f"  {f:4s} {pop:21s} {d['n']:7d} {_fmt(d['residual_corr'], '7.4f')} "
                      f"{_fmt(r1, '8.2f')} {_fmt(r2, '8.2f')} {_fmt(d['ambiguity'], '10.1f')} "
                      f"{_fmt(d['rmse_blend_decomp'], '8.2f')}")


def print_closed_set(res: dict) -> None:
    print(f"closed-set {res['candidate']} vs {res['reference']} "
          f"(allowed: {res['allowed_differences']})")
    for f, d in res["per_fold"].items():
        if "present_in" in d:
            print(f"  {f}: only in {d['present_in']}")
            continue
        print(f"  {f}: only-cand {len(d['only_in_candidate'])} only-ref "
              f"{len(d['only_in_reference'])} differ {sorted(d['differ'])} equal {d['n_equal']}")
    print(f"VIOLATION: {res['violation']}")
    for v in res["violations"]:
        print(f"  - {v}")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diversity")
    d.add_argument("base")
    d.add_argument("second", nargs="+")
    d.add_argument("--out", required=True)
    c = sub.add_parser("closed-set")
    c.add_argument("cand")
    c.add_argument("ref")
    c.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "diversity":
        res = diversity(a.base, a.second)
        print_diversity(res)
    else:
        res = closed_set(a.cand, a.ref)
        print_closed_set(res)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, default=float) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
