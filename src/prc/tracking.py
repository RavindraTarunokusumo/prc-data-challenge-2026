"""Weights & Biases mirror of experiment records (Day 5, owner instruction INC-0009).

The repository stays the source of truth. A W&B run is a read-only mirror of one
experiment's committed records: gate metadata, config, fold metrics (development and
diagnostic folds as in metrics.json; never holdout comparisons), resource usage, and the
learning curves in curves.json when the experiment recorded them (Day 5 on). No
predictions, targets or data rows leave the machine.

One run per experiment, with run id == experiment id, so a re-sync updates the same run.
Syncing is best-effort: a failure is reported and never touches the experiment's records.
Enabled only when WANDB_API_KEY is set (environment or the git-ignored .env); PRC_WANDB=0
disables it.
"""

from __future__ import annotations

import json
import os

import yaml

from prc import ledger
from prc.paths import EXPERIMENTS, ROOT, RUNTIME

PROJECT = "PRC-Data-Challenge-2026"
CHAMPIONS = {"E001", "E002", "E005", "E019"}  # champion lineage (STATE.md)
SEGMENTS = ("by_airport", "by_airport_bulk", "by_traffic", "by_wake", "by_taxi_band")


def load_env() -> None:
    """Read the git-ignored .env into os.environ (no override; values never printed)."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def enabled() -> bool:
    load_env()
    return bool(os.environ.get("WANDB_API_KEY")) and os.environ.get("PRC_WANDB", "1") != "0"


def _read(eid: str, name: str, loader=json.loads):
    p = EXPERIMENTS / eid / name
    return loader(p.read_text()) if p.exists() else None


def payload(eid: str) -> dict:
    """Everything a run carries, built from committed files only (no network)."""
    rec = ledger.get(eid) or {}
    gate = _read(eid, "gate.json") or {}
    cfg = _read(eid, "config.yaml", yaml.safe_load) or {}
    metrics = _read(eid, "metrics.json") or {}
    usage = _read(eid, "resource-usage.json") or {}
    hyp, ver = rec.get("hypothesis_id"), rec.get("proposal_version")
    decision = rec.get("decision")
    tags = [t for t in (rec.get("day"), rec.get("purpose"), rec.get("status"),
                        f"decision:{decision}" if decision else "decision:none",
                        cfg.get("model"), cfg.get("feature_set")) if t]
    if eid in CHAMPIONS:
        tags.append("champion-lineage")
    config = {
        "experiment_id": eid, "hypothesis": hyp, "proposal_version": ver,
        "purpose": rec.get("purpose"), "day": rec.get("day"), "session": rec.get("session"),
        "model": cfg.get("model"), "feature_set": cfg.get("feature_set"),
        "params": cfg.get("params"), "folds": cfg.get("folds"), "seed": cfg.get("seed"),
        "job_class": cfg.get("job_class"),
        "proposal": gate.get("proposal"), "review": gate.get("review"),
        "proposal_sha256": gate.get("proposal_sha256"), "run_commit": rec.get("run_commit"),
        "uv_lock_sha256": gate.get("uv_lock_sha256"),
    }
    summary = {"status": rec.get("status"), "decision": decision or "none",
               "mean_rmse_dev": metrics.get("mean_rmse_dev"),
               "runtime_s": usage.get("runtime_s"), "peak_rss_gb": usage.get("peak_rss_gb"),
               "within_class": usage.get("within_class"), "cpu_count": usage.get("cpu_count")}
    for fold, v in (metrics.get("rmse_by_fold") or {}).items():
        summary[f"rmse/{fold}"] = v
    for fold, v in (metrics.get("fold_seconds") or {}).items():
        summary[f"fold_seconds/{fold}"] = v
    rows = []
    for fold, s in (metrics.get("scores") or {}).items():
        for seg in SEGMENTS:
            for key, cell in (s.get(seg) or {}).items():
                rows.append([fold, seg, str(key), cell.get("n"), cell.get("rmse"),
                             cell.get("bias")])
    return {"id": eid, "name": eid, "group": f"{hyp} v{ver}" if hyp else None,
            "job_type": rec.get("purpose"), "tags": tags, "config": config,
            "summary": {k: v for k, v in summary.items() if v is not None},
            "segments": rows, "notes": rec.get("notes"),
            "history": curve_history(_read(eid, "curves.json"))}


DEV_FOLDS = ("R1", "R2", "R3", "S1", "W1")


def curve_history(curves: dict | None) -> list[dict]:
    """Rows for W&B history, one per staged iteration (curves.json). Keys per fold:
    `train_rmse/<fold>` and `eval_rmse/<fold>`, plus `eval_rmse/dev_mean` over the five
    development folds. The x-axis is `iteration`."""
    if not curves:
        return []
    folds = curves["folds"]
    grids = {tuple(c["iterations"]) for c in folds.values()}
    iters = sorted({i for g in grids for i in g})
    rows = []
    for it in iters:
        row = {"iteration": it}
        for fold, c in folds.items():
            if it in c["iterations"]:
                k = c["iterations"].index(it)
                row[f"train_rmse/{fold}"] = c["train_rmse"][it - 1]
                if "eval_rmse" in c:
                    row[f"eval_rmse/{fold}"] = c["eval_rmse"][k]
        dev = [row.get(f"eval_rmse/{f}") for f in DEV_FOLDS]
        if all(v is not None for v in dev):
            row["eval_rmse/dev_mean"] = sum(dev) / len(dev)
        rows.append(row)
    return rows


def sync(eid: str) -> str | None:
    """Create or update the W&B run for `eid`. Returns the run URL, or None if disabled."""
    if not enabled():
        return None
    import wandb

    p = payload(eid)
    (RUNTIME / "wandb").mkdir(parents=True, exist_ok=True)
    settings = wandb.Settings(console="off", save_code=False, silent=True,
                              x_disable_stats=True, x_disable_meta=True)
    run = wandb.init(project=PROJECT, id=p["id"], name=p["name"], group=p["group"],
                     job_type=p["job_type"], tags=p["tags"], config=p["config"],
                     notes=p["notes"], resume="allow", dir=str(RUNTIME), settings=settings)
    try:
        if p["history"]:
            run.define_metric("iteration")
            run.define_metric("train_rmse/*", step_metric="iteration", summary="min")
            run.define_metric("eval_rmse/*", step_metric="iteration", summary="min")
            for i, row in enumerate(p["history"]):
                run.log(row, step=i)  # a re-sync's lower steps are ignored by W&B
        run.summary.update(p["summary"])
        if p["segments"]:
            run.log({"segments": wandb.Table(
                columns=["fold", "segment", "key", "n", "rmse", "bias"], data=p["segments"])})
        url = run.url
    finally:
        run.finish()
    return url


def sync_safely(eid: str) -> None:
    """For run_experiment.py: never raises, never alters records."""
    try:
        url = sync(eid)
        if url:
            print(f"wandb: {eid} -> {url}")
    except Exception as exc:  # noqa: BLE001 - the mirror must not affect the experiment
        print(f"wandb: sync of {eid} failed ({type(exc).__name__}); records unaffected")
