"""Repository paths and shared helpers."""

from __future__ import annotations

import fcntl
import hashlib
import subprocess
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "prc-2026-datasets"
PROCESSED = ROOT / "data" / "processed"
CACHE = ROOT / "data" / "cache"
MANIFESTS = ROOT / "data" / "manifests"
SILVER = PROCESSED / "silver.parquet"
SILVER_MANIFEST = MANIFESTS / "silver_manifest.json"
RAW_MANIFEST = MANIFESTS / "raw_manifest.json"
EXPERIMENTS = ROOT / "experiments"
PREDICTIONS_VAL = ROOT / "predictions" / "validation"
SPLITS = ROOT / "config" / "splits.yaml"
RESOURCES = ROOT / "config" / "resources.yaml"
RUNTIME = ROOT / "runtime"
EXPERIMENT_LOCK = RUNTIME / "experiment.lock"


@contextmanager
def experiment_lock(eid: str):
    """Hold an exclusive flock on EXPERIMENT_LOCK while an experiment runs (Day 5, INC-0008).
    flock is kernel-level, so it is visible across the sandbox's PID namespaces, and it is
    released when every holder of the file description exits. Yields the open file, whose
    descriptor the worker inherits (pass_fds) so the lock outlives a dead runner."""
    RUNTIME.mkdir(exist_ok=True)
    f = open(EXPERIMENT_LOCK, "a+")  # noqa: SIM115 - held for the with-block of the caller
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        f.seek(0)
        held = f.read().strip()
        f.close()
        raise SystemExit(f"refused: experiment {held or '?'} is running (runtime/experiment.lock)")
    f.seek(0)
    f.truncate()
    f.write(eid)
    f.flush()
    try:
        yield f
    finally:
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()


def running_experiment() -> str | None:
    """The id of the experiment holding EXPERIMENT_LOCK, or None. Memory-heavy side work
    (real-silver tests, calibrations) checks this and stands down."""
    if not EXPERIMENT_LOCK.exists():
        return None
    with open(EXPERIMENT_LOCK, "a+") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            f.seek(0)
            return f.read().strip() or "?"
        fcntl.flock(f, fcntl.LOCK_UN)
        return None


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def git_commit() -> str:
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True,
                         check=True)
    return out.stdout.strip()


def git_dirty() -> bool:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True,
                         check=True)
    return bool(out.stdout.strip())
