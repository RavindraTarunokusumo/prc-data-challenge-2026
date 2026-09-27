"""Phase-close protected-holdout comparison (config/splits.yaml: phase_close).

    uv run python scripts/holdout_check.py NEW_EID REFERENCE_EID --reason "..."

At most one access per phase; the phase comes from NEW_EID's gate record. Writes
research/<day>/holdout/holdout_<new>_vs_<ref>.json (decision quantities only).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prc.evaluate import holdout_compare
from prc.paths import ROOT


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("new")
    ap.add_argument("reference")
    ap.add_argument("--reason", required=True)
    a = ap.parse_args()
    r = holdout_compare(a.new, a.reference, a.reason)
    out = ROOT / "research" / r["phase"] / "holdout" / f"holdout_{a.new}_vs_{a.reference}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    # Persist only the decision quantities (Advisor recommendation, SPLITS v2 review).
    keep = {k: r[k] for k in ("phase", "new", "reference", "delta_rmse", "delta_q10_q90",
                              "outcome", "revert")}
    keep["rmse_new"], keep["rmse_reference"] = r["score_new"]["rmse"], r["score_reference"]["rmse"]
    out.write_text(json.dumps(keep, indent=1) + "\n")
    print(json.dumps({k: r[k] for k in ("phase", "delta_rmse", "delta_q10_q90", "outcome",
                                         "revert")}, indent=1))
    print("H rmse:", a.new, round(r["score_new"]["rmse"], 2), "|", a.reference,
          round(r["score_reference"]["rmse"], 2))


if __name__ == "__main__":
    main()
