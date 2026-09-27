"""Run a gated experiment under resource supervision (brief §4, §13).

    uv run python scripts/run_experiment.py E###

Refuses unless the experiment was allocated by scripts/gate.py, is still ALLOCATED and
the frozen files are intact. The work runs in a child process (prc.worker); this parent
samples the child tree's RSS, kills it above the hard RAM limit (RESOURCE_FAILURE) or
past the class timeout (TIMEOUT), and records the outcome in the ledger. Failed runs are
never retried: a new attempt needs a new E###.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import psutil
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prc import ledger
from prc.paths import EXPERIMENTS, RESOURCES, ROOT, git_commit, git_dirty

GB = 1024**3


def load_gate():
    spec = importlib.util.spec_from_file_location("gate", ROOT / "scripts" / "gate.py")
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return g


def tree_rss(proc: psutil.Process) -> int:
    total = 0
    for p in [proc, *proc.children(recursive=True)]:
        try:
            total += p.memory_info().rss
        except psutil.Error:
            pass
    return total


def kill_tree(proc: psutil.Process) -> None:
    for p in [*proc.children(recursive=True), proc]:
        try:
            p.kill()
        except psutil.Error:
            pass


def check_config(eid: str, cfg: dict, purpose: str) -> None:
    """Seed by purpose and fold coverage (Advisor recommendations, SPLITS v2 review)."""
    from prc.splits import load_splits

    splits = load_splits()
    rep = splits["promotion"]["reproduction"]
    want_seed = rep["reproduction_seed"] if purpose == "reproduction" else rep["primary_seed"]
    if cfg.get("seed") != want_seed:
        sys.exit(f"refused: {eid} ({purpose}) must use seed {want_seed}, config has "
                 f"{cfg.get('seed')}")
    if any(splits["final"].get(f) for f in cfg["folds"]):
        return  # final (SUBMIT) runs have their own fold list
    required = (list(splits["development_folds"]) + list(splits["diagnostic_folds"])
                + list(splits["protected_holdout"]))
    missing = [f for f in required if f not in cfg["folds"]]
    if missing:
        sys.exit(f"refused: {eid} must cover all scored folds plus H; missing {missing}")


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(eid: str) -> None:
    exp = EXPERIMENTS / eid
    if not (exp / "gate.json").exists():
        sys.exit(f"refused: {eid} was not allocated by scripts/gate.py")
    rec = ledger.get(eid)
    if rec is None or rec["status"] != "ALLOCATED":
        sys.exit(f"refused: {eid} status is {rec and rec['status']}, not ALLOCATED")
    gate = load_gate()
    gate.check_advisor_definition()
    gate.check_frozen()
    cfg = yaml.safe_load((exp / "config.yaml").read_text())
    check_config(eid, cfg, json.loads((exp / "gate.json").read_text())["purpose"])
    res = yaml.safe_load(RESOURCES.read_text())
    klass = res["classes"][cfg["job_class"]]
    hard_gb = min(res["limits"]["ram_hard_gb_per_experiment"], klass.get("ram_hard_gb", 1e9))
    timeout_s = klass["runtime_min"] * 60 * res["limits"].get("timeout_factor", 1.5)

    commit, dirty = git_commit(), git_dirty()
    ledger.update(eid, status="RUNNING", run_commit=commit, job_class=cfg["job_class"])
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    t0 = time.time()
    peak, status = 0, None
    with open(exp / "worker.log", "w") as log:
        child = subprocess.Popen([sys.executable, "-m", "prc.worker", eid], cwd=ROOT, env=env,
                                 stdout=log, stderr=subprocess.STDOUT)
        proc = psutil.Process(child.pid)
        while child.poll() is None:
            peak = max(peak, tree_rss(proc))
            if peak > hard_gb * GB:
                status = "RESOURCE_FAILURE"
                kill_tree(proc)
            elif time.time() - t0 > timeout_s:
                status = "TIMEOUT"
                kill_tree(proc)
            time.sleep(0.25)
        child.wait()
    runtime = time.time() - t0
    if status is None:
        status = "COMPLETE" if child.returncode == 0 else "INVALID"
        if child.returncode in (-9, 137):
            status = "RESOURCE_FAILURE"  # killed by the kernel (OOM)

    usage = {
        "experiment_id": eid,
        "status": status,
        "exit_code": child.returncode,
        "runtime_s": round(runtime, 1),
        "peak_rss_gb": round(peak / GB, 3),
        "job_class": cfg["job_class"],
        "class_limits": klass,
        "hard_ram_gb": hard_gb,
        "timeout_s": timeout_s,
        "within_class": runtime <= klass["runtime_min"] * 60 and peak / GB <= klass["ram_gb"],
        "cpu_count": psutil.cpu_count(),
        "run_commit": commit,
        "git_dirty_at_run": dirty,
        "finished_utc": now(),
    }
    (exp / "resource-usage.json").write_text(json.dumps(usage, indent=1) + "\n")
    fields = {"status": status, "runtime_s": usage["runtime_s"],
              "peak_rss_gb": usage["peak_rss_gb"], "finished_utc": usage["finished_utc"]}
    if status == "COMPLETE":
        m = json.loads((exp / "metrics.json").read_text())
        fields.update(mean_rmse_dev=m["mean_rmse_dev"],
                      rmse_by_fold=json.dumps(m["rmse_by_fold"]))
    else:
        fields["decision"] = "RESOURCE_FAILURE" if status in ("RESOURCE_FAILURE",
                                                              "TIMEOUT") else "INVALID"
    ledger.update(eid, **fields)
    print(json.dumps({k: usage[k] for k in ("status", "runtime_s", "peak_rss_gb",
                                             "within_class")}))
    if status != "COMPLETE":
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])
