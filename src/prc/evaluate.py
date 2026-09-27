"""Evaluator: the only code path that reads validation truth.

Frozen. Imports only prc.metrics and prc.splits; resolves every path from this file's
location. It loads silver itself and refuses unless the file's SHA-256 and each fold's
row count match `evaluation_population` in the frozen config/splits.yaml (R1).

- `evaluate(pred, fold)`: score a development or diagnostic fold.
- `compare(candidate_eid, champion_eid)`: brief §10 criteria 1–3 from stored predictions.
- `holdout_compare(new_eid, ref_eid, reason)`: the only reader of protected-holdout truth.
  The phase is taken from the new experiment's gate record, the frozen per-phase limit is
  enforced against the append-only task ledger, the access is logged before truth is read,
  and only aggregate results are returned (no per-row truth).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import polars as pl

from prc import metrics
from prc.splits import get_fold, load_splits, promotion_config

ROOT = Path(__file__).resolve().parents[2]
SILVER = ROOT / "data" / "processed" / "silver.parquet"
TASK_LEDGER = ROOT / "orchestration" / "task-ledger.jsonl"
EXPERIMENTS = ROOT / "experiments"
PREDICTIONS_VAL = ROOT / "predictions" / "validation"
META = ["MVT_ID_mvt", "TAXITIME_SEC_mvt", "ADEP_mvt", "month", "WK_TBL_CAT_flt",
        "MVT_TIME_UTC_mvt"]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def _now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


@lru_cache(maxsize=1)
def _verified_silver() -> Path:
    pinned = load_splits()["evaluation_population"]["silver_sha256"]
    if _sha256(SILVER) != pinned:
        raise RuntimeError("silver.parquet does not match the frozen evaluation population")
    return SILVER


def _truth(fold_id: str) -> pl.DataFrame:
    fold = get_fold(fold_id)
    df = (
        pl.scan_parquet(_verified_silver())
        .filter(pl.col("month").is_in(list(fold.val_months)) & (pl.col("PHASE_mvt") == "DEP"))
        .select(META)
        .sort("MVT_ID_mvt")
        .collect()
    )
    expected = load_splits()["evaluation_population"]["eval_rows"][fold_id]
    if df.height != expected:
        raise RuntimeError(f"fold {fold_id}: {df.height} evaluation rows, frozen {expected}")
    return df


def _join(pred: pl.DataFrame, truth: pl.DataFrame) -> pl.DataFrame:
    pred = pred.select(pl.col("MVT_ID_mvt").cast(pl.Int64), pl.col("pred").cast(pl.Float64))
    metrics.validate_predictions(pred, truth)
    return truth.join(pred, on="MVT_ID_mvt", how="inner").sort("MVT_ID_mvt")


def truth_frame(fold_id: str) -> pl.DataFrame:
    """Evaluation rows with truth for a development or diagnostic fold."""
    kind = get_fold(fold_id).kind
    if kind in ("holdout", "final"):
        raise PermissionError(f"fold {fold_id} ({kind}) truth is not available here")
    return _truth(fold_id)


def evaluate(pred: pl.DataFrame, fold_id: str) -> tuple[dict, pl.DataFrame]:
    """Score predictions for one development or diagnostic fold."""
    joined = _join(pred, truth_frame(fold_id))
    return metrics.score(joined), joined


def _predictions(eid: str, fold_id: str) -> pl.DataFrame:
    manifest = json.loads((EXPERIMENTS / eid / "manifest.json").read_text())
    rel = f"predictions/validation/{eid}/{fold_id}.parquet"
    entry = next((a for a in manifest["artifacts"] if a["path"] == rel), None)
    if entry is None:
        raise FileNotFoundError(f"{eid} has no predictions for {fold_id}")
    if _sha256(ROOT / rel) != entry["sha256"]:
        raise RuntimeError(f"{rel} does not match {eid}/manifest.json")
    return pl.read_parquet(ROOT / rel)


def compare(candidate_eid: str, champion_eid: str) -> dict:
    """Brief §10 criteria 1–3 from two experiments' stored predictions."""
    cfg = promotion_config()
    folds = list(cfg["development_folds"]) + list(cfg["causal_twins"].values())
    cand, champ = {}, {}
    for f in folds:
        truth = truth_frame(f)
        cand[f] = _join(_predictions(candidate_eid, f), truth)
        champ[f] = _join(_predictions(champion_eid, f), truth)
    return {"candidate": candidate_eid, "champion": champion_eid,
            **metrics.promotion_check(cand, champ)}


def _ledger_rows() -> dict[str, dict]:
    path = EXPERIMENTS / "ledger.jsonl"
    rows = [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
    return {r["experiment_id"]: r for r in rows}


def holdout_accesses(phase: str) -> int:
    if not TASK_LEDGER.exists():
        return 0
    recs = [json.loads(x) for x in TASK_LEDGER.read_text().splitlines() if x.strip()]
    return sum(r.get("event") == "holdout_access" and r.get("phase") == phase for r in recs)


def holdout_compare(new_eid: str, ref_eid: str, reason: str) -> dict:
    """Phase-close comparison on the protected holdout (config: phase_close)."""
    (hid,) = load_splits()["protected_holdout"].keys()
    limit = load_splits()["protected_holdout"][hid]["max_access_per_phase"]
    gate = json.loads((EXPERIMENTS / new_eid / "gate.json").read_text())
    phase = gate["day"]
    rows = _ledger_rows()
    for eid in (new_eid, ref_eid):
        if eid not in rows or rows[eid]["status"] != "COMPLETE":
            raise PermissionError(f"{eid} is not a COMPLETE experiment in the ledger")
    if holdout_accesses(phase) >= limit:
        raise PermissionError(f"protected holdout already accessed {limit}x in {phase}")
    preds = {eid: _predictions(eid, hid) for eid in (new_eid, ref_eid)}
    with open(TASK_LEDGER, "a") as f:
        f.write(json.dumps({"event": "holdout_access", "phase": phase, "utc": _now(),
                            "experiments": [new_eid, ref_eid], "reason": reason}) + "\n")
    truth = _truth(hid)
    j_new, j_ref = _join(preds[new_eid], truth), _join(preds[ref_eid], truth)
    boot = metrics.paired_bootstrap({hid: (j_new, j_ref)})[hid]
    outcome = metrics.fold_outcome(boot["draws"])
    return {
        "phase": phase,
        "new": new_eid,
        "reference": ref_eid,
        "score_new": metrics.score(j_new),
        "score_reference": metrics.score(j_ref),
        "delta_rmse": boot["point"],
        "delta_q10_q90": [float(np.quantile(boot["draws"], 0.10)),
                          float(np.quantile(boot["draws"], 0.90))],
        "outcome": outcome,
        "revert": outcome == load_splits()["phase_close"]["revert_on"],
    }
