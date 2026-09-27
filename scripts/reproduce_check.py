"""Brief §10 item 6 under the frozen reproduction rule (splits.yaml: promotion.reproduction).

    uv run python scripts/reproduce_check.py REPRO_EID PRIMARY_EID [--champion EID]

Checks that REPRO_EID is a gate-allocated `reproduction` of the same hypothesis version,
that every development-fold RMSE is within the tolerance of PRIMARY_EID, and (with
--champion) that criteria 1-3 also hold for the reproduction against the champion.
Writes research/comparisons/repro_<repro>_of_<primary>.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prc import ledger
from prc.evaluate import compare
from prc.paths import EXPERIMENTS, ROOT
from prc.splits import promotion_config


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("repro")
    ap.add_argument("primary")
    ap.add_argument("--champion")
    a = ap.parse_args()
    rep, pri = ledger.get(a.repro), ledger.get(a.primary)
    if not rep or not pri or rep["status"] != "COMPLETE" or pri["status"] != "COMPLETE":
        sys.exit("refused: both experiments must be COMPLETE")
    if rep["purpose"] != "reproduction" or (rep["hypothesis_id"], rep["proposal_version"]) != (
            pri["hypothesis_id"], pri["proposal_version"]):
        sys.exit("refused: not a reproduction of the same hypothesis version")
    cfg = promotion_config()["reproduction"]
    m_rep = json.loads((EXPERIMENTS / a.repro / "metrics.json").read_text())["rmse_by_fold"]
    m_pri = json.loads((EXPERIMENTS / a.primary / "metrics.json").read_text())["rmse_by_fold"]
    dev = promotion_config()["development_folds"]
    diffs = {f: m_rep[f] - m_pri[f] for f in dev}
    within = all(abs(d) <= cfg["rmse_tolerance_s"] for d in diffs.values())
    out = {"reproduction": a.repro, "primary": a.primary, "rmse_diff_by_fold": diffs,
           "within_tolerance": within}
    if a.champion:
        c = compare(a.repro, a.champion)
        out["criteria_vs_champion"] = {k: c[k] for k in ("criterion_1", "criterion_2",
                                                         "criterion_3", "fold_outcome")}
        out["criteria_hold"] = c["passes_criteria_1_to_3"]
    out["passes"] = within and out.get("criteria_hold", True)
    path = ROOT / "research" / "comparisons" / f"repro_{a.repro}_of_{a.primary}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
