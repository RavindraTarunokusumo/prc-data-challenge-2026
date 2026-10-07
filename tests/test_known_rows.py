"""Day 8: the known-row reading of G5 (c) (scripts/known_row_check.py)."""

import importlib.util
from datetime import UTC, datetime, timedelta
from pathlib import Path

import numpy as np
import polars as pl

_spec = importlib.util.spec_from_file_location(
    "known_row_check", Path(__file__).resolve().parents[1] / "scripts" / "known_row_check.py")
kr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kr)


def _fold_frames(fold: str, rng):
    """Truth and two predictions. In S1/S1c the candidate differs from the base only on the
    known rows (one per cluster); elsewhere it improves every row."""
    known = kr.KNOWN_ROWS[fold]
    only_known = fold in ("S1", "S1c")
    n_clusters = len(known) + 1 if only_known else 40
    rows = []
    for k in range(n_clusters):
        day = datetime(2025, 7, 1, tzinfo=UTC) + timedelta(days=k)
        for i in range(20):
            rows.append((day + timedelta(minutes=i), "LIRF" if k % 2 else "EDDF"))
    ids = np.arange(1, len(rows) + 1, dtype=np.int64) + 10**6
    if only_known:  # one known row per cluster, in the first len(known) clusters
        for j, mid in enumerate(known):
            ids[j * 20] = mid
    else:
        ids[: len(known)] = known
    y = rng.normal(900, 200, len(rows))
    truth = pl.DataFrame({"MVT_ID_mvt": ids, "TAXITIME_SEC_mvt": y,
                          "ADEP_mvt": [r[1] for r in rows],
                          "MVT_TIME_UTC_mvt": [r[0] for r in rows]})
    base = y + rng.normal(0, 300, len(rows))
    is_known = np.isin(ids, known)
    if only_known:
        base[is_known] = y[is_known] + 20000.0
        cand = np.where(is_known, y, base)
    else:
        cand = y + (base - y) * 0.5
    return truth, base, cand, ids


def test_known_row_reading_strips_a_win_carried_by_known_rows(monkeypatch, tmp_path):
    rng = np.random.default_rng(7)
    data = {f: _fold_frames(f, rng) for f in kr.KNOWN_ROWS}
    monkeypatch.setattr(kr, "truth_frame", lambda f: data[f][0])
    monkeypatch.setattr(kr, "_predictions", lambda eid, f: pl.DataFrame(
        {"MVT_ID_mvt": data[f][3], "pred": data[f][2] if eid == "E901" else data[f][1]}))
    out = kr.main("E901", "E900", out_dir=tmp_path)
    assert out["frozen"]["passes_criteria_1_to_3"]
    assert out["weight"]["S1"] == {"frozen": "WIN", "reverted": "TIE",
                                   "confirmatory_weight": False}
    assert all(out["weight"][f]["confirmatory_weight"] for f in ("R1", "R2", "R3", "W1"))
    assert out["g5_consequence"]
    assert out["known_row_shares"]["S1"]["known_share_of_sse_change"] == 1.0
    assert (tmp_path / "E901_vs_E900_known_rows.json").exists()


_spec_ma = importlib.util.spec_from_file_location(
    "mixture_analysis", Path(__file__).resolve().parents[1] / "scripts" / "mixture_analysis.py")
ma = importlib.util.module_from_spec(_spec_ma)
_spec_ma.loader.exec_module(ma)


def test_mixture_analysis_convention_share_reading(monkeypatch, tmp_path):
    """Criterion 4 (a) of H038 v2: where the subgroup gains, convention rows (|y - d_sched| <
    120 s) must carry at least half of the gain; a gain on other rows fails it."""
    import json

    pv, ex = tmp_path / "pv", tmp_path / "ex"
    (tmp_path / "research/comparisons").mkdir(parents=True)
    ids = np.arange(1, 9, dtype=np.int64)
    y = np.array([20000., 30000., 600., 700., 900., 40000., 800., 500.])
    d_sched = np.array([20010., 30005., 9000., 8000., 100., 10000., 50., 40.])
    # rows 1-2 convention; 3-6 subgroup non-convention; 7-8 outside the subgroup
    sub = ids[:6]
    base = pl.DataFrame({"MVT_ID_mvt": ids, "pred": [5000., 5000., 5000., 5000., 900., 5000.,
                                                    800., 500.]})
    cases = {"conv": [19000., 29000., 5000., 5000., 900., 5000.],   # gain on convention rows
             "other": [5000., 5000., 600., 700., 900., 5000.]}      # gain on other rows
    for name, pred in cases.items():
        eid = f"E9{len(name)}"
        (pv / eid / "components").mkdir(parents=True, exist_ok=True)
        (ex / eid).mkdir(parents=True, exist_ok=True)
        (ex / eid / "manifest.json").write_text(json.dumps({"artifacts": [{"fold": "R1"}]}))
        comp = pl.DataFrame({"MVT_ID_mvt": sub, "pred": pred, "p_conv": [0.5] * 6,
                             "g_normal": [600.] * 6, "conv_component": d_sched[:6],
                             "d_sched": d_sched[:6], "p_train_rate": [0.5] * 6})
        comp.write_parquet(pv / eid / "components" / "R1.parquet")
        full = base.with_columns(pl.Series("pred", pred + [800., 500.]))
        full.write_parquet(pv / eid / "R1.parquet")
    (pv / "E900").mkdir(parents=True)
    base.write_parquet(pv / "E900" / "R1.parquet")
    monkeypatch.setattr(ma, "PREDICTIONS_VAL", pv)
    monkeypatch.setattr(ma, "EXPERIMENTS", ex)
    monkeypatch.setattr(ma, "ROOT", tmp_path)
    monkeypatch.setattr(ma, "truth_frame", lambda f: pl.DataFrame(
        {"MVT_ID_mvt": ids, "TAXITIME_SEC_mvt": y}))
    ma.main("E94", "E900")
    r = json.loads((tmp_path / "research/comparisons/E94_vs_E900_mixture_analysis.json")
                   .read_text())["folds"]["R1"]
    assert r["subgroup_rows"] == 6 and r["convention_rows"] == 2
    assert r["criterion4_reading_a"] is True and r["convention_share_of_gain"] == 1.0
    ma.main("E95", "E900")
    r = json.loads((tmp_path / "research/comparisons/E95_vs_E900_mixture_analysis.json")
                   .read_text())["folds"]["R1"]
    assert r["criterion4_reading_a"] is False
    assert r["subgroup_sse_change_other_dsched_ge_3600"] < 0
