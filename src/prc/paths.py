"""Repository paths and shared helpers."""

from __future__ import annotations

import hashlib
import subprocess
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
