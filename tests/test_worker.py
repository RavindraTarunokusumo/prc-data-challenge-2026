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


def test_experiment_lock_is_exclusive_and_visible(tmp_path, monkeypatch):
    import pytest

    from prc import paths

    monkeypatch.setattr(paths, "RUNTIME", tmp_path)
    monkeypatch.setattr(paths, "EXPERIMENT_LOCK", tmp_path / "experiment.lock")
    assert paths.running_experiment() is None
    with paths.experiment_lock("E999"):
        assert paths.running_experiment() == "E999"
        with pytest.raises(SystemExit, match="E999 is running"), paths.experiment_lock("E998"):
            pass
    assert paths.running_experiment() is None


def test_tracking_payload_from_records_only(monkeypatch):
    from prc import tracking

    monkeypatch.setenv("PRC_WANDB", "0")
    assert tracking.enabled() is False
    p = tracking.payload("E019")
    assert p["id"] == "E019" and p["group"] == "H015 v2"
    assert "champion-lineage" in p["tags"] and "decision:PROMOTE" in p["tags"]
    assert p["summary"]["mean_rmse_dev"] > 0 and "rmse/R1" in p["summary"]
    assert not any(k.startswith("rmse/H") for k in p["summary"])  # no holdout figures
    assert tracking.sync("E019") is None  # disabled: no network


def test_curve_history_rows():
    from prc.tracking import curve_history

    c = {"folds": {f: {"iterations": [1, 10], "train_rmse": [9.0] * 10,
                       "eval_rmse": [5.0, 4.0]} for f in ("R1", "R2", "R3", "S1", "W1")}}
    c["folds"]["H"] = {"iterations": [1, 10], "train_rmse": [8.0] * 10}  # no eval for H
    rows = curve_history(c)
    assert [r["iteration"] for r in rows] == [1, 10]
    assert rows[1]["eval_rmse/dev_mean"] == 4.0 and rows[1]["train_rmse/H"] == 8.0
    assert "eval_rmse/H" not in rows[1]
    assert curve_history(None) == []


def test_gpu_failure_is_a_resource_failure():
    import importlib.util
    from pathlib import Path

    spec = importlib.util.spec_from_file_location(
        "run_experiment", Path(__file__).resolve().parents[1] / "scripts" / "run_experiment.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    assert m.gpu_failure("...\n_catboost.CatBoostError: CUDA error 2: out of memory\n")
    assert m.gpu_failure("xgboost.core.XGBoostError: cudaErrorMemoryAllocation")
    assert not m.gpu_failure("Traceback ...\nValueError: blend: weights must sum 1\n")


def test_blend_fixed_weights_of_stored_components(monkeypatch):
    """Day 5: the blend is the fixed-weight mean of the components' stored predictions,
    joined by id; incomplete components and bad weights are refused."""
    import numpy as np
    import polars as pl
    import pytest

    from prc import blending

    ids = np.arange(100, 200, dtype=np.int64)
    stored = {"E900": pl.DataFrame({"MVT_ID_mvt": ids[::-1], "pred": ids[::-1] * 1.0}),
              "E901": pl.DataFrame({"MVT_ID_mvt": ids, "pred": np.full(ids.size, 10.0)})}
    status = {"E900": "COMPLETE", "E901": "COMPLETE", "E902": "RESOURCE_FAILURE"}
    monkeypatch.setattr(blending.ledger, "get", lambda eid: {"status": status[eid]})
    load = lambda eid, fold: stored[eid]
    out = blending.blend(pl.Series(ids), {"components": ["E900", "E901"],
                                          "weights": [0.5, 0.5]}, "R1", loader=load)
    assert np.allclose(out.sort("MVT_ID_mvt")["pred"].to_numpy(), ids * 0.5 + 5.0)
    with pytest.raises(ValueError, match="not COMPLETE"):
        blending.blend(pl.Series(ids), {"components": ["E900", "E902"],
                                        "weights": [0.5, 0.5]}, "R1", loader=load)
    with pytest.raises(ValueError, match="weights"):
        blending.blend(pl.Series(ids), {"components": ["E900", "E901"],
                                        "weights": [0.6, 0.5]}, "R1", loader=load)


def test_blend_refuses_a_file_that_does_not_match_its_manifest(tmp_path, monkeypatch):
    import json

    import polars as pl
    import pytest

    from prc import blending

    exp, pred = tmp_path / "experiments", tmp_path / "predictions" / "validation"
    (exp / "E900").mkdir(parents=True)
    (pred / "E900").mkdir(parents=True)
    pl.DataFrame({"MVT_ID_mvt": [1], "pred": [1.0]}).write_parquet(pred / "E900" / "R1.parquet")
    (exp / "E900" / "manifest.json").write_text(json.dumps({"artifacts": [
        {"path": "predictions/validation/E900/R1.parquet", "sha256": "0" * 64}]}))
    monkeypatch.setattr(blending, "EXPERIMENTS", exp)
    monkeypatch.setattr(blending, "PREDICTIONS_VAL", pred)
    monkeypatch.setattr(blending, "ROOT", tmp_path)
    with pytest.raises(RuntimeError, match="does not match"):
        blending.stored_predictions("E900", "R1")
