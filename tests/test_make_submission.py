import importlib.util
import json
from argparse import Namespace
from pathlib import Path

import numpy as np
import polars as pl
import pytest

_spec = importlib.util.spec_from_file_location(
    "make_submission", Path(__file__).resolve().parents[1] / "scripts" / "make_submission.py")
ms = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ms)

IDS = {"SUBMIT_JAN": [202601001, 202601002, 202601003],
       "SUBMIT_JUL": [202607001, 202607002]}
HALVES = {"A": {202601001: 100.0, 202601002: 2000.25, 202601003: -10.0,
                202607001: 800.0, 202607002: 5000.0},
          "B": {202601001: 300.0, 202601002: 2000.75, 202601003: 6.0,
                202607001: 801.0, 202607002: 3000.0}}


def _preds(eid, fold, *, drop=None):
    ids = [i for i in IDS.get(fold, [202512001]) if i != drop]
    if eid in HALVES:
        vals = [HALVES[eid].get(i, 1.0) for i in ids]
    else:  # the blend
        vals = [0.5 * HALVES["A"].get(i, 1.0) + 0.5 * HALVES["B"].get(i, 1.0) for i in ids]
    return pl.DataFrame({"MVT_ID_mvt": pl.Series(ids, dtype=pl.Int64), "pred": vals})


@pytest.fixture
def env(tmp_path, monkeypatch):
    template = pl.DataFrame({
        "MVT_ID_mvt": pl.Series([202607002, 202601001, 202601003, 202607001, 202601002],
                                dtype=pl.Float64),
        "TAXITIME_SEC_mvt": pl.Series([None] * 5, dtype=pl.Int32)})
    tpath = tmp_path / "submitting.parquet"
    template.write_parquet(tpath)
    manifest = tmp_path / "raw_manifest.json"
    manifest.write_text(json.dumps({"files": [{"path": "x/submitting.parquet",
                                               "sha256": ms.sha256_file(tpath)}]}))
    exps = tmp_path / "experiments"
    (exps / "BL").mkdir(parents=True)
    (exps / "BL" / "config.yaml").write_text(
        "params:\n  components: [A, B]\n  weights: [0.5, 0.5]\n")
    monkeypatch.setattr(ms, "TEMPLATE", tpath)
    monkeypatch.setattr(ms, "RAW_MANIFEST", manifest)
    monkeypatch.setattr(ms, "EXPERIMENTS", exps)
    monkeypatch.setattr(ms, "ROOT", tmp_path)
    monkeypatch.setattr(ms, "OUT", tmp_path / "predictions" / "final" / "submitting.parquet")
    monkeypatch.setattr(ms, "RECORD", tmp_path / "rec" / "SUBMISSION_RECORD.json")
    monkeypatch.setattr(ms, "REF_FOLDS", ("H",))
    monkeypatch.setattr(ms, "manifest_sha", lambda e, f: f"{e}-{f}")
    monkeypatch.setattr(ms, "stored_predictions", _preds)
    monkeypatch.setattr(ms, "subgroups", lambda: pl.DataFrame({
        "MVT_ID_mvt": pl.Series([*IDS["SUBMIT_JAN"], *IDS["SUBMIT_JUL"], 202512001],
                                dtype=pl.Int64),
        "ADEP_mvt": ["LIRF", "EDDF", "EDDF", "LIRF", "EDDF", "EDDF"],
        "nm_missing": [True, False, False, False, True, False]}))
    return tmp_path, template


ARGS = Namespace(blend="BL", half_a="A", half_b="B", ref=["BL", "A", "B"])


def test_writes_template_shaped_rounded_submission(env):
    tmp, template = env
    ms.main(ARGS)
    out = pl.read_parquet(tmp / "predictions" / "final" / "submitting.parquet")
    assert out.schema == template.schema
    assert out["MVT_ID_mvt"].equals(template["MVT_ID_mvt"])  # template order kept
    # 4000 (07002), 200 (01001), -2 (01003; no clipping), 800.5 -> 800 (half to even), 2000.5
    # -> 2000 (half to even)
    assert out["TAXITIME_SEC_mvt"].to_list() == [4000, 200, -2, 800, 2000]
    rec = json.loads((tmp / "rec" / "SUBMISSION_RECORD.json").read_text())
    assert rec["rounding"]["max_abs_s"] == 0.5
    jan = rec["final_folds"]["SUBMIT_JAN"]
    assert jan["out_of_range"]["all"] == {"rows": 3, "below0": 1, "above3600": 0}
    assert jan["routed_rows"] == 1
    assert rec["final_folds"]["SUBMIT_JUL"]["out_of_range"]["all"]["above3600"] == 1
    assert np.isclose(jan["rms_half_difference"], np.sqrt((200**2 + 0.5**2 + 16**2) / 3))


def test_refuses_missing_prediction(env, monkeypatch):
    monkeypatch.setattr(ms, "stored_predictions",
                        lambda e, f: _preds(e, f, drop=202607001))
    with pytest.raises(SystemExit, match="REFUSED"):
        ms.main(ARGS)
    assert not (env[0] / "predictions" / "final" / "submitting.parquet").exists()


def test_refuses_blend_not_equal_to_halves(env, monkeypatch):
    def bad(e, f):
        p = _preds(e, f)
        return p.with_columns(pl.col("pred") + 1.0) if e == "BL" else p
    monkeypatch.setattr(ms, "stored_predictions", bad)
    with pytest.raises(SystemExit, match="weighted halves"):
        ms.main(ARGS)


def test_refuses_tampered_template(env):
    tmp, template = env
    template.head(4).write_parquet(tmp / "submitting.parquet")
    with pytest.raises(SystemExit, match="raw_manifest"):
        ms.main(ARGS)
