"""The known-row reading of G5 (c) (Day 8; X-D08-S03-0001 (E), binding on H038 v2).

    uv run python scripts/known_row_check.py CANDIDATE_EID BASE_EID

The known rows are the LIRF NM-missing validation rows of the development folds whose MVT_ID
appears in a tracked file at 3c23aab (the review's table (E)). For each development fold and
twin, the candidate's predictions on that fold's known rows are set equal to BASE's, and the
frozen promotion computation (prc.metrics.promotion_check, unchanged: the paired cluster
bootstrap on the full fold, the twin rule on the reverted twin) is run again. A development
fold's WIN carries confirmatory weight only if it is still a WIN under this reading. If S1's
WIN, or the third WIN of criterion 2, lacks weight, G5's consequence applies (INCONCLUSIVE).
A LOSS in the frozen computation stays a LOSS. Criteria 1 and 3 are read as frozen.
Development and diagnostic folds only. Writes
research/comparisons/<cand>_vs_<base>_known_rows.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl

from prc.evaluate import _join, _predictions, truth_frame
from prc.metrics import PRED, TARGET, promotion_check, promotion_config

# X-D08-S03-0001 (E), table "Known rows" (twins share their fold's validation month).
KNOWN_ROWS = {
    "R1": [196123310, 196129531],
    "R2": [198934338, 198939290, 198939422, 198941714],
    "R3": [200297323, 200300302],
    "S1": [192615553, 192615662, 192621162, 192626268, 192628959],
    "W1": [183903219],
}
KNOWN_ROWS["S1c"], KNOWN_ROWS["W1c"] = KNOWN_ROWS["S1"], KNOWN_ROWS["W1"]


def main(cand: str, base: str, out_dir: Path | None = None) -> dict:
    cfg = promotion_config()
    dev = list(cfg["development_folds"])
    folds = dev + list(cfg["causal_twins"].values())
    frozen_c, frozen_b, reverted_c, shares = {}, {}, {}, {}
    for f in folds:
        truth = truth_frame(f)
        c, b = _join(_predictions(cand, f), truth), _join(_predictions(base, f), truth)
        known = list(KNOWN_ROWS[f])
        found = c.filter(pl.col("MVT_ID_mvt").is_in(known)).height
        if found != len(KNOWN_ROWS[f]):
            raise ValueError(f"{f}: {found} of {len(KNOWN_ROWS[f])} known rows in the fold")
        rev = (c.join(b.select("MVT_ID_mvt", pl.col(PRED).alias("pb")), on="MVT_ID_mvt",
                      how="left", validate="1:1")
               .with_columns(pl.when(pl.col("MVT_ID_mvt").is_in(known)).then(pl.col("pb"))
                             .otherwise(pl.col(PRED)).alias(PRED)).drop("pb"))
        d = (c.select("MVT_ID_mvt", ((pl.col(PRED) - pl.col(TARGET).cast(pl.Float64)) ** 2)
                      .alias("sc"))
             .join(b.select("MVT_ID_mvt", ((pl.col(PRED) - pl.col(TARGET).cast(pl.Float64))
                                           ** 2).alias("sb")), on="MVT_ID_mvt")
             .with_columns((pl.col("sc") - pl.col("sb")).alias("d")))
        total = float(d["d"].sum())
        on_known = float(d.filter(pl.col("MVT_ID_mvt").is_in(known))["d"].sum())
        shares[f] = {"sse_change_all_rows": total, "sse_change_known_rows": on_known,
                     "known_share_of_sse_change": on_known / total if total else None,
                     "known_rows": len(KNOWN_ROWS[f])}
        frozen_c[f], frozen_b[f], reverted_c[f] = c, b, rev
    frozen = promotion_check(frozen_c, frozen_b)
    reverted = promotion_check(reverted_c, frozen_b)
    weight = {}
    for f in dev:
        fo, ro = frozen["fold_outcome_counted"][f], reverted["fold_outcome_counted"][f]
        weight[f] = {"frozen": fo, "reverted": ro,
                     "confirmatory_weight": fo == "WIN" and ro == "WIN"}
    weighted_wins = [f for f in dev if weight[f]["confirmatory_weight"]]
    s1 = cfg["seasonal_fold"]
    frozen_wins = [f for f in dev if frozen["fold_outcome_counted"][f] == "WIN"]
    g5 = bool(frozen["passes_criteria_1_to_3"]) and (
        not weight[s1]["confirmatory_weight"] or len(weighted_wins) < cfg["criterion_2"]["min_wins"])
    out = {"candidate": cand, "base": base, "known_rows": KNOWN_ROWS,
           "frozen": {k: frozen[k] for k in ("fold_delta_rmse", "fold_outcome",
                                             "fold_outcome_counted", "criterion_1",
                                             "criterion_2", "criterion_3",
                                             "passes_criteria_1_to_3")},
           "reverted": {k: reverted[k] for k in ("fold_delta_rmse", "fold_delta_q10_q90",
                                                 "fold_outcome", "fold_outcome_counted")},
           "known_row_shares": shares, "weight": weight, "frozen_wins": frozen_wins,
           "weighted_wins": weighted_wins,
           "g5_consequence": g5,
           "note": "g5_consequence is true when criteria 1-3 pass as frozen but S1's WIN or "
                   "the third WIN lacks confirmatory weight (INCONCLUSIVE, never uploaded)"}
    out_dir = out_dir or Path(__file__).resolve().parents[1] / "research/comparisons"
    path = out_dir / f"{cand}_vs_{base}_known_rows.json"
    path.write_text(json.dumps(out, indent=1, default=float) + "\n")
    for f in dev:
        print(f, weight[f], f"known share {shares[f]['known_share_of_sse_change']}")
    print("weighted WINs:", weighted_wins, "| G5 consequence:", g5)
    return out


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
