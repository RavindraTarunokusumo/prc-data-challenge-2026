"""Paired promotion comparison between two completed experiments (frozen rule).

    uv run python scripts/compare.py CANDIDATE_EID CHAMPION_EID [--out DIR]

Writes <out>/<cand>_vs_<champ>.json (default research/comparisons/) and prints a summary.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prc.evaluate import compare
from prc.paths import ROOT


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("champion")
    ap.add_argument("--out", default="research/comparisons")
    a = ap.parse_args()
    r = compare(a.candidate, a.champion)
    out = ROOT / a.out / f"{a.candidate}_vs_{a.champion}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, indent=1) + "\n")
    print(f"{a.candidate} vs {a.champion}: mean dRMSE {r['mean_delta_rmse']:+.2f} s "
          f"(q95 {r['mean_delta_q95']:+.2f})")
    for f, o in r["fold_outcome"].items():
        lo, hi = r["fold_delta_q10_q90"][f]
        print(f"  {f:4s} {r['fold_delta_rmse'][f]:+8.2f} s  [{lo:+.2f}, {hi:+.2f}]  {o}"
              f"{'' if o == r['fold_outcome_counted'].get(f, o) else ' (counted TIE)'}")
    print(f"  criteria: 1={r['criterion_1']} 2={r['criterion_2']} 3={r['criterion_3']}  "
          f"-> passes_criteria_1_to_3={r['passes_criteria_1_to_3']}")
    if r["airports_degraded_beyond_tolerance"]:
        print("  degraded airports:", r["airports_degraded_beyond_tolerance"])


if __name__ == "__main__":
    main()
