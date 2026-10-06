"""Pre-registered readings of a convention-mixture candidate (Day 8, H038 criterion 4).

    uv run python scripts/mixture_analysis.py CANDIDATE_EID BASE_EID

Development and diagnostic folds only (truth through prc.evaluate.truth_frame; never H).
Per fold, on the LIRF NM-missing subgroup (the rows where CANDIDATE and BASE may differ):
  - the SSE change against BASE, split by the Day 1 convention label on the validation rows
    (c = |y - d_sched| < 120 s), by the y >= 3,600 s band (bulk / tail), and for c = 0 by
    d_sched >= 3,600 s (target-free);
  - H038 v2 criterion 4 reading (a): where the subgroup SSE change is negative, the
    convention rows carry at least half of it (`criterion4_reading_a`);
  - ablations from the stored components, with no refit: constant p (the fold's training
    convention rate), the convention component alone, g alone;
  - the classifier's AUC and Brier score against c;
  - rule 6 (the top-10 rows' share of the subgroup SSE change) and rule 12 (subgroup
    predictions below 0 s, and above 3,600 s on bulk rows).
Also the all-rows RMSE of both (scripts/compare.py governs criteria 1-3).
Writes research/comparisons/<cand>_vs_<base>_mixture_analysis.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl

from prc.evaluate import truth_frame
from prc.paths import EXPERIMENTS, PREDICTIONS_VAL, ROOT

FOLDS = ["R1", "R2", "R3", "S1", "W1", "S1c", "W1c"]
TOL_S, TAIL_S = 120.0, 3600.0
CONV_SHARE = 0.5  # H038 v2 criterion 4: convention rows carry at least half the gain


def sse(e: np.ndarray) -> float:
    return float(np.sum(e**2))


def auc(y: np.ndarray, s: np.ndarray) -> float | None:
    pos, neg = s[y == 1], s[y == 0]
    if not pos.size or not neg.size:
        return None
    ranks = pl.Series(np.concatenate([pos, neg])).rank("average").to_numpy()
    return float((ranks[: pos.size].sum() - pos.size * (pos.size + 1) / 2)
                 / (pos.size * neg.size))


def main(cand: str, base: str) -> None:
    out = {"candidate": cand, "base": base, "folds": {}}
    have = {a["fold"] for a in json.loads((EXPERIMENTS / cand / "manifest.json").read_text())
            ["artifacts"]}
    for fold in [f for f in FOLDS if f in have]:
        truth = truth_frame(fold).select(pl.col("MVT_ID_mvt").cast(pl.Int64),
                                         pl.col("TAXITIME_SEC_mvt").cast(pl.Float64).alias("y"))
        c = pl.read_parquet(PREDICTIONS_VAL / cand / "components" / f"{fold}.parquet")
        b = pl.read_parquet(PREDICTIONS_VAL / base / f"{fold}.parquet").rename({"pred": "pb"})
        m = pl.read_parquet(PREDICTIONS_VAL / cand / f"{fold}.parquet").rename({"pred": "pm"})
        allr = (m.join(b, on="MVT_ID_mvt", validate="1:1")
                .join(truth, on="MVT_ID_mvt", validate="1:1"))
        j = c.join(allr, on="MVT_ID_mvt", how="left", validate="1:1")
        y = j["y"].to_numpy()
        pred, pb = j["pred"].to_numpy(), j["pb"].to_numpy()
        p, g, rate = (j[k].to_numpy() for k in ("p_conv", "g_normal", "p_train_rate"))
        has_c = ~j["conv_component"].is_null().to_numpy()
        conv = j["conv_component"].fill_null(0.0).to_numpy()
        lab = (has_c & (np.abs(y - j["d_sched"].fill_null(np.nan).to_numpy()) < TOL_S))
        tail = y >= TAIL_S
        big = j["d_sched"].fill_null(0.0).to_numpy() >= TAIL_S  # target-free
        abl = {"constant_p": np.where(has_c, rate * conv + (1 - rate) * g, g),
               "convention_only": np.where(has_c, conv, g), "g_only": g}
        d = (pred - y) ** 2 - (pb - y) ** 2
        top = np.sort(np.abs(d))[::-1]
        r = {"subgroup_rows": j.height, "convention_rows": int(lab.sum()),
             "tail_rows": int(tail.sum()),
             "all_rows": {"rmse_candidate": float(np.sqrt(np.mean((allr["pm"] - allr["y"]).to_numpy() ** 2))),
                          "rmse_base": float(np.sqrt(np.mean((allr["pb"] - allr["y"]).to_numpy() ** 2))),
                          "sse_change": float(np.sum(((allr["pm"] - allr["y"]) ** 2
                                                      - (allr["pb"] - allr["y"]) ** 2).to_numpy()))},
             "subgroup_sse_change": float(d.sum()),
             "subgroup_sse_change_convention": float(d[lab].sum()),
             "subgroup_sse_change_other": float(d[~lab].sum()),
             "subgroup_sse_change_other_dsched_ge_3600": float(d[~lab & big].sum()),
             "subgroup_sse_change_other_dsched_lt_3600": float(d[~lab & ~big].sum()),
             "convention_share_of_gain": float(d[lab].sum() / d.sum()) if d.sum() < 0 else None,
             "criterion4_reading_a": (None if d.sum() >= 0
                                      else bool(d[lab].sum() <= CONV_SHARE * d.sum())),
             "subgroup_sse_change_tail": float(d[tail].sum()),
             "subgroup_sse_change_bulk": float(d[~tail].sum()),
             "subgroup_rmse": {"candidate": float(np.sqrt(np.mean((pred - y) ** 2))) if y.size else None,
                               "base": float(np.sqrt(np.mean((pb - y) ** 2))) if y.size else None},
             "ablation_sse_change_vs_candidate": {k: sse(v - y) - sse(pred - y)
                                                  for k, v in abl.items()},
             "ablation_sse_change_vs_base": {k: sse(v - y) - sse(pb - y) for k, v in abl.items()},
             "classifier_auc": auc(lab.astype(int), p), "classifier_brier":
                 float(np.mean((p - lab) ** 2)) if y.size else None,
             "mean_p_conv": float(p.mean()) if y.size else None,
             "training_convention_rate": float(rate[0]) if y.size else None,
             "rule6_top10_share": float(top[:10].sum() / np.abs(d).sum()) if np.abs(d).sum() else None,
             "rule12": {"pred_below_0": int((pred < 0).sum()),
                        "bulk_pred_above_3600": int(((pred > TAIL_S) & ~tail).sum()),
                        "base_bulk_pred_above_3600": int(((pb > TAIL_S) & ~tail).sum())}}
        out["folds"][fold] = r
        print(fold, json.dumps({k: r[k] for k in ("subgroup_rows", "subgroup_sse_change",
                                                  "subgroup_sse_change_convention",
                                                  "classifier_auc")}), flush=True)
    path = ROOT / "research/comparisons" / f"{cand}_vs_{base}_mixture_analysis.json"
    path.write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
