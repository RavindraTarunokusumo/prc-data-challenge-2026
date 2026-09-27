"""Worker plumbing on synthetic data (no real folds scored): predictions for every fold,
manifest hashes, metrics only for scored folds, holdout predicted but never evaluated."""

import json

import numpy as np
import polars as pl
import yaml

from prc import worker
from tests.test_models import synthetic


def test_worker_end_to_end(tmp_path, monkeypatch):
    exps, preds = tmp_path / "experiments", tmp_path / "predictions" / "validation"
    (exps / "E900").mkdir(parents=True)
    folds = ["R1", "R2", "R3", "S1", "W1", "S1c", "W1c", "H"]
    (exps / "E900" / "config.yaml").write_text(yaml.safe_dump(
        {"model": "airport_median", "feature_set": "FS0", "params": {}, "folds": folds,
         "seed": 42, "job_class": "CLASS-S"}))
    (tmp_path / "data" / "manifests").mkdir(parents=True)
    (tmp_path / "data/manifests/silver_manifest.json").write_text(json.dumps({"sha256": "x"}))
    evaluated = []

    def fake_eval(pred, fold_id):
        assert fold_id != "H"
        evaluated.append(fold_id)
        return {"rmse": float(len(evaluated))}, None

    monkeypatch.setattr(worker, "EXPERIMENTS", exps)
    monkeypatch.setattr(worker, "PREDICTIONS_VAL", preds)
    monkeypatch.setattr(worker, "ROOT", tmp_path)
    monkeypatch.setattr(worker, "load_silver", lambda **kw: None)
    monkeypatch.setattr(worker, "masked_view", lambda silver, fold: None)
    monkeypatch.setattr(worker, "FEATURE_SETS", {"FS0": lambda view: synthetic()})
    monkeypatch.setattr(worker, "evaluate", fake_eval)
    monkeypatch.setattr(worker, "git_commit", lambda: "0" * 40)
    worker.main("E900")

    assert evaluated == folds[:-1]
    m = json.loads((exps / "E900" / "metrics.json").read_text())
    assert set(m["rmse_by_fold"]) == set(folds[:-1])
    assert m["mean_rmse_dev"] == np.mean([1, 2, 3, 4, 5])
    man = json.loads((exps / "E900" / "manifest.json").read_text())
    assert [a["fold"] for a in man["artifacts"]] == folds
    for a in man["artifacts"]:
        df = pl.read_parquet(tmp_path / a["path"])
        assert df.columns == ["MVT_ID_mvt", "pred"] and df.height == a["rows"] == 100


def test_runner_config_checks():
    import importlib.util
    from pathlib import Path

    import pytest

    spec = importlib.util.spec_from_file_location(
        "run_experiment", Path(__file__).resolve().parents[1] / "scripts" / "run_experiment.py")
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    ok = {"seed": 42, "folds": ["R1", "R2", "R3", "S1", "W1", "S1c", "W1c", "H"]}
    r.check_config("E1", ok, "primary")
    with pytest.raises(SystemExit, match="seed 43"):
        r.check_config("E1", ok, "reproduction")
    with pytest.raises(SystemExit, match="missing"):
        r.check_config("E1", {**ok, "folds": ["R1"]}, "primary")
    r.check_config("E1", {"seed": 43, "folds": ok["folds"]}, "reproduction")
