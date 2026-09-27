"""Evaluator determinism and holdout guard."""

import json

import numpy as np
import polars as pl
import pytest

from prc import evaluate as ev


def preds_for(silver, fold_id, seed=0):
    ids = ev.truth_frame(silver, fold_id)["MVT_ID_mvt"]
    rng = np.random.default_rng(seed)
    return pl.DataFrame({"MVT_ID_mvt": ids, "pred": rng.normal(990, 300, len(ids))})


def test_evaluator_is_deterministic(silver):
    p = preds_for(silver, "R3")
    a, _ = ev.evaluate(p, "R3", silver)
    b, _ = ev.evaluate(p.sample(fraction=1.0, shuffle=True, seed=5), "R3", silver)
    c, _ = ev.evaluate(p, "R3", silver)
    assert json.dumps(a, sort_keys=True) == json.dumps(c, sort_keys=True)
    assert a["rmse"] == pytest.approx(b["rmse"], rel=1e-12)
    assert a["n"] == b["n"] == p.height


def test_final_fold_has_no_truth(silver):
    with pytest.raises(ValueError):
        ev.evaluate(pl.DataFrame({"MVT_ID_mvt": [1], "pred": [1.0]}), "SUBMIT", silver)


def test_holdout_guard(silver, tmp_path, monkeypatch):
    monkeypatch.setattr(ev, "TASK_LEDGER", tmp_path / "ledger.jsonl")
    p = preds_for(silver, "H")
    with pytest.raises(PermissionError):
        ev.evaluate(p, "H", silver)
    meta = {"phase": "TEST", "experiment_id": "E000", "reason": "unit test"}
    ev.evaluate(p, "H", silver, holdout=meta)
    assert ev.holdout_accesses("TEST") == 1
    with pytest.raises(PermissionError, match="already accessed"):
        ev.evaluate(p, "H", silver, holdout=meta)
