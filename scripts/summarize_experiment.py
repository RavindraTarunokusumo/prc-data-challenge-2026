"""Markdown tables from an experiment's metrics.json and resource-usage.json, used as the
factual part of experiments/E###/analysis.md.

    uv run python scripts/summarize_experiment.py E###
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(eid: str) -> None:
    exp = ROOT / "experiments" / eid
    m = json.loads((exp / "metrics.json").read_text())
    u = json.loads((exp / "resource-usage.json").read_text())
    cfg = (exp / "config.yaml").read_text().splitlines()
    hyp = next(x.split(": ")[1] for x in cfg if x.startswith("hypothesis_id"))
    s = m["scores"]
    folds = list(s)
    print(f"**{eid}** ({hyp}): status {u['status']}, {u['runtime_s']} s, peak "
          f"{u['peak_rss_gb']} GB, within class {u['within_class']} ({u['job_class']}).\n")
    print("| Fold | RMSE | MAE | Bias |\n|---|---|---|---|")
    for f in folds:
        print(f"| {f} | {s[f]['rmse']:.2f} | {s[f]['mae']:.1f} | {s[f]['bias']:+.1f} |")
    if m.get("mean_rmse_dev") is not None:
        print(f"| **dev mean** (R1–R3, S1, W1) | **{m['mean_rmse_dev']:.2f}** | | |")
    airports = sorted(s[folds[0]]["by_airport"])
    print("\nRMSE by airport (all rows / bulk y < 3,600 s):\n")
    print("| Airport | " + " | ".join(folds) + " |\n|---|" + "---|" * len(folds))
    for a in airports:
        cells = [f"{s[f]['by_airport'][a]['rmse']:.0f} / {s[f]['by_airport_bulk'][a]['rmse']:.0f}"
                 for f in folds]
        print(f"| {a} | " + " | ".join(cells) + " |")
    bands = list(s[folds[0]]["by_taxi_band"])
    print("\nRMSE by taxi band (true target):\n")
    print("| Band | " + " | ".join(folds) + " |\n|---|" + "---|" * len(folds))
    for b in ["<300", "300-600", "600-900", "900-1200", "1200-1800", "1800-3600", ">=3600"]:
        if b in bands:
            print(f"| {b} | " + " | ".join(f"{s[f]['by_taxi_band'].get(b, {}).get('rmse', 0):.0f}"
                                             for f in folds) + " |")


if __name__ == "__main__":
    main(sys.argv[1])
