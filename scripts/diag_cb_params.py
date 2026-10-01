"""Day 5: resolved-parameter difference of H021's and H022's exact CatBoost configurations
(H022 v2 review, Revision 1). Fold R3, permuted training target (rng seed 0), the routed
path with `route_train_exclude`, 20 iterations; NO metric is computed. Writes every key of
CatBoost's get_all_params() on which the two arms differ, and the keys present in only one.

    uv run python scripts/diag_cb_params.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from calibrate_gpu import H021, build_frame

from prc import curves
from prc.models import routed
from prc.paths import running_experiment

OUT = ROOT / "research" / "day-05" / "eda" / "cb_param_diff.json"


def main() -> None:
    if (eid := running_experiment()):
        raise SystemExit(f"refused: {eid} is running (INC-0008)")
    feats = build_frame("FS2_RAW", drop_routed=False)
    resolved = {}
    for mode in ("ctr", "codes"):
        curves.start()
        routed.routed_catboost(feats, {**H021, "iterations": 20, "cat_mode": mode}, 42)
        resolved[mode] = curves.take()["resolved_params"]
    a, b = resolved["ctr"], resolved["codes"]
    differ = {k: {"ctr": a[k], "codes": b[k]} for k in sorted(set(a) & set(b)) if a[k] != b[k]}
    out = {"note": "R3, permuted target, routed path, 20 iterations; no metric computed",
           "differing_keys": differ,
           "only_in_ctr": {k: a[k] for k in sorted(set(a) - set(b))},
           "only_in_codes": {k: b[k] for k in sorted(set(b) - set(a))},
           "resolved": resolved}
    OUT.write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k: out[k] for k in ("differing_keys", "only_in_ctr", "only_in_codes")},
                     default=str)[:3000])


if __name__ == "__main__":
    main()
