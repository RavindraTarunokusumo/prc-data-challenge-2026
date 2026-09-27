"""Evaluator: pinned population, determinism, and the holdout guard. December truth is
never read: holdout tests substitute a synthetic truth frame."""

import json

import numpy as np
import polars as pl
import pytest

from prc import evaluate as ev


@pytest.fixture(scope="module")
def r3_truth():
    return ev.truth_frame("R3")


def preds_for(truth, seed=0):
    rng = np.random.default_rng(seed)
    return pl.DataFrame({"MVT_ID_mvt": truth["MVT_ID_mvt"],
                         "pred": rng.normal(990, 300, truth.height)})


def test_evaluator_is_deterministic(r3_truth):
    p = preds_for(r3_truth)
    a, _ = ev.evaluate(p, "R3")
    b, _ = ev.evaluate(p.sample(fraction=1.0, shuffle=True, seed=5), "R3")
    c, _ = ev.evaluate(p, "R3")
    assert json.dumps(a, sort_keys=True) == json.dumps(c, sort_keys=True)
    assert a["rmse"] == pytest.approx(b["rmse"], rel=1e-12)
    assert a["n"] == b["n"] == p.height


@pytest.mark.parametrize("fold_id", ["R1", "R2", "R3", "S1", "W1", "S1c", "W1c"])
def test_population_matches_frozen_counts(fold_id):
    assert ev.truth_frame(fold_id).height == \
        ev.load_splits()["evaluation_population"]["eval_rows"][fold_id]


@pytest.mark.parametrize("fold_id", ["H", "SUBMIT_JAN", "SUBMIT_JUL"])
def test_no_truth_for_holdout_or_final(fold_id):
    with pytest.raises(PermissionError):
        ev.truth_frame(fold_id)
    with pytest.raises(PermissionError):
        ev.evaluate(pl.DataFrame({"MVT_ID_mvt": [1], "pred": [1.0]}), fold_id)


@pytest.fixture
def fake_repo(tmp_path, monkeypatch):
    """Two COMPLETE experiments with holdout predictions; synthetic holdout truth."""
    rng = np.random.default_rng(0)
    n = 500
    import datetime as dt
    t0 = dt.datetime(2025, 12, 1, tzinfo=dt.UTC)
    truth = pl.DataFrame({
        "MVT_ID_mvt": np.arange(n, dtype=np.int64),
        "TAXITIME_SEC_mvt": rng.integers(300, 2000, n).astype(np.int32),
        "ADEP_mvt": rng.choice(["EDDF", "EGLL"], n),
        "month": "2025-12",
        "WK_TBL_CAT_flt": "M",
        "MVT_TIME_UTC_mvt": [t0 + dt.timedelta(hours=int(h)) for h in rng.integers(0, 600, n)],
    })
    exps, preds = tmp_path / "experiments", tmp_path / "predictions" / "validation"
    ledger_rows = []
    for eid, noise in (("E001", 50.0), ("E002", 400.0)):
        (exps / eid).mkdir(parents=True)
        (preds / eid).mkdir(parents=True)
        path = preds / eid / "H.parquet"
        pl.DataFrame({"MVT_ID_mvt": truth["MVT_ID_mvt"],
                      "pred": truth["TAXITIME_SEC_mvt"] + rng.normal(0, noise, n)}
                     ).write_parquet(path)
        rel = f"predictions/validation/{eid}/H.parquet"
        (exps / eid / "manifest.json").write_text(json.dumps(
            {"artifacts": [{"path": rel, "sha256": ev._sha256(path)}]}))
        (exps / eid / "gate.json").write_text(json.dumps({"day": "day-01"}))
        ledger_rows.append({"experiment_id": eid, "status": "COMPLETE"})
    (exps / "ledger.jsonl").write_text("".join(json.dumps(r) + "\n" for r in ledger_rows))
    ledger = tmp_path / "task-ledger.jsonl"
    monkeypatch.setattr(ev, "ROOT", tmp_path)
    monkeypatch.setattr(ev, "EXPERIMENTS", exps)
    monkeypatch.setattr(ev, "TASK_LEDGER", ledger)
    calls = []

    def fake_truth(fold_id):
        # The access must already be logged when truth is read.
        assert ledger.exists() and "holdout_access" in ledger.read_text()
        calls.append(fold_id)
        return truth

    monkeypatch.setattr(ev, "_truth", fake_truth)
    return ledger, calls


def test_holdout_compare_logs_before_reading_and_returns_aggregates(fake_repo):
    _, calls = fake_repo
    r = ev.holdout_compare("E001", "E002", "unit test")
    assert calls == ["H"]
    assert r["phase"] == "day-01" and r["outcome"] == "WIN" and r["revert"] is False
    assert set(r) == {"phase", "new", "reference", "score_new", "score_reference",
                      "delta_rmse", "delta_q10_q90", "outcome", "revert"}
    assert ev.holdout_accesses("day-01") == 1


def test_holdout_second_access_refused_without_reading(fake_repo):
    _, calls = fake_repo
    ev.holdout_compare("E001", "E002", "first")
    with pytest.raises(PermissionError, match="already accessed"):
        ev.holdout_compare("E002", "E001", "second")
    assert calls == ["H"]


def test_holdout_requires_complete_experiments(fake_repo):
    ledger, calls = fake_repo
    with pytest.raises(PermissionError, match="not a COMPLETE"):
        ev.holdout_compare("E001", "E999", "x")
    assert calls == [] and not ledger.exists()
