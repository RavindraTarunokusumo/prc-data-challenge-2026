"""Synthetic tests for d06_diagnostics.py (no real data). Run from the repo root:
PYTHONDONTWRITEBYTECODE=1 uv run python <this file>

Implemented by a claude-sonnet-5-5 worker to the researcher's specification; reviewed by the researcher (INC-0013).
"""
import json
import sys
import tempfile
import zlib
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import d06_diagnostics as d
import numpy as np
import polars as pl

rng = np.random.default_rng(0)
N = 4000
ids = np.arange(1000, 1000 + N)
y = rng.gamma(3.0, 300.0, N)
y[:50] += 4000.0  # tail rows
adep = rng.choice(["LIRF", "EGLL", "LSZH"], N)
nm_missing = rng.random(N) < 0.3
PRED_SETS = {}
for i, e in enumerate(("E029", "EX1", "EX2")):
    r = np.random.default_rng(i + 1)
    PRED_SETS[e] = np.floor(y) + r.normal(0, 150, N) + 20 * (i - 1)


def fake_truth(fold):
    perm = np.random.default_rng(zlib.crc32(fold.encode())).permutation(N)  # unsorted order
    return pl.DataFrame({d.ID: ids[perm], d.TARGET: np.floor(y[perm]).astype(np.int64),
                         "ADEP_mvt": adep[perm]})


def fake_silver(columns=None):
    return pl.DataFrame({d.ID: ids, "AOBT_3_flt": [None if m else 1.0 for m in nm_missing],
                         "PHASE_mvt": ["DEP"] * N},
                        schema_overrides={"AOBT_3_flt": pl.Float64})


calls = []


def fake_preds(eid, fold):
    calls.append((eid, fold))
    perm = np.random.default_rng(7).permutation(N)
    return pl.DataFrame({d.ID: ids[perm], "pred": PRED_SETS[eid][perm]})


d.truth_frame, d.stored_predictions, d.load_silver = fake_truth, fake_preds, fake_silver
res = d.diversity("E029", ["EX1", "EX2"])
assert res["schema"] == "d06-diversity-v1" and res["base"] == "E029"
assert set(res["pairs"]) == {"EX1", "EX2"}
assert tuple(res["pairs"]["EX1"]) == d.FOLDS
yi = np.floor(y)
for f in d.FOLDS:
    for pop in d.POPS:
        s = res["pairs"]["EX1"][f][pop]
        m = {"all": np.ones(N, bool), "bulk": yi < 3600,
             "NM_present_excl_LIRF": (~nm_missing) & (adep != "LIRF")}[pop]
        p1, p2 = PRED_SETS["E029"][m], PRED_SETS["EX1"][m]
        assert s["n"] == int(m.sum())
        assert abs(s["residual_corr"] - np.corrcoef(yi[m] - p1, yi[m] - p2)[0, 1]) < 1e-9
        assert abs(s["mse1"] - np.mean((yi[m] - p1) ** 2)) < 1e-6
        assert abs(s["ambiguity"] - np.mean((p1 - p2) ** 2)) < 1e-6
        assert s["blend_check_rel_diff"] < 1e-9
        direct = np.sqrt(np.mean((yi[m] - 0.5 * (p1 + p2)) ** 2))
        assert abs(s["rmse_blend_decomp"] - direct) / direct < 1e-9
    assert res["pairs"]["EX1"][f]["bulk"]["n"] < N
assert "H" not in {f for _, f in calls} and {f for _, f in calls} == set(d.FOLDS)
d.print_diversity(res)

# failure mode: mismatched row set
def bad_preds(eid, fold):
    p = fake_preds(eid, fold)
    return p.head(N - 1) if eid == "EX2" else p
d.stored_predictions = bad_preds
try:
    d.diversity("E029", ["EX2"])
    raise SystemExit("expected failure on row mismatch")
except AssertionError:
    pass
d.stored_predictions = fake_preds
assert d._pearson(np.ones(5), np.arange(5.0)) is None
assert d.pop_stats(np.array([]), np.array([]), np.array([]))["n"] == 0

with tempfile.TemporaryDirectory() as td:
    out = Path(td) / "sub" / "div.json"
    d.main(["diversity", "E029", "EX1", "--out", str(out)])
    assert json.loads(out.read_text())["schema"] == "d06-diversity-v1"

# closed-set
rc = {"R1": {"a": 1, "b": [1, 2], "max_ctr_complexity": 2, "c": {"x": 1, "y": 2}, "n": 5},
      "H": {"a": 1}}
rr = {"R1": {"a": 1, "b": [1, 2], "max_ctr_complexity": 4, "c": {"y": 2, "x": 1}, "n": 5},
      "H": {"a": 1}}
r = d.closed_set_from("C", "R", rc, rr)
assert r["violation"] is False and r["violations"] == []
assert r["per_fold"]["R1"]["differ"] == {"max_ctr_complexity": {"candidate": 2, "reference": 4}}
assert r["per_fold"]["R1"]["n_equal"] == 4 and r["per_fold"]["H"]["n_equal"] == 1
rc["R1"]["z"] = 1
rr["R1"]["a"] = 2
rr["W1"] = {"a": 1}
r = d.closed_set_from("C", "R", rc, rr)
assert r["violation"] is True
assert any("only in candidate: z" in v for v in r["violations"])
assert any("outside allowed set: a" in v for v in r["violations"])
assert any(v.startswith("W1") for v in r["violations"])
d.print_closed_set(r)
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    for e, p in (("C", rc), ("R", rr)):
        (td / "experiments" / e).mkdir(parents=True)
        (td / "experiments" / e / "resolved_params.json").write_text(json.dumps(p))
    d.ROOT = td
    d.main(["closed-set", "C", "R", "--out", str(td / "cs.json")])
    assert json.loads((td / "cs.json").read_text())["schema"] == "d06-closed-set-v1"
print("ALL TESTS PASSED")
