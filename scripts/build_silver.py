"""Build the silver layer: one canonical, typed table of all movements (DATA_POLICY §8).

Scientifically neutral: every raw row and value is kept, nothing is derived from the
target, fold membership plays no role. Changes are limited to:
- concatenating the 12 training files and the ranking file, with a `src` column
  (`train` | `rank`);
- casting `MVT_ID_mvt` and `FLIGHT_ID_mvt` from Float64 to Int64 (verified integral);
- adding `month` (YYYY-MM of `MVT_TIME_UTC_mvt`), the join key for fold definitions;
- a deterministic row order (`MVT_TIME_UTC_mvt`, `MVT_ID_mvt`).

Usage:
    uv run python scripts/build_silver.py
"""

from __future__ import annotations

import datetime as dt
import glob
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
os.environ.setdefault("POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR", "load_as_storage")

import polars as pl

from prc.paths import (
    RAW,
    RAW_MANIFEST,
    ROOT,
    SILVER,
    SILVER_MANIFEST,
    git_commit,
    git_dirty,
    sha256_file,
)

ID_COLS = ("MVT_ID_mvt", "FLIGHT_ID_mvt")


def verify_raw() -> dict[str, str]:
    manifest = json.loads(RAW_MANIFEST.read_text())
    hashes = {}
    for f in manifest["files"]:
        path = ROOT / f["path"]
        digest = sha256_file(path)
        if digest != f["sha256"]:
            sys.exit(f"raw file hash mismatch: {f['path']}")
        hashes[f["path"]] = digest
    return hashes


def cast_ids(df: pl.DataFrame) -> pl.DataFrame:
    for c in ID_COLS:
        s = df[c].drop_nulls()
        if not (s == s.round(0)).all():
            sys.exit(f"non-integral values in {c}")
    return df.with_columns([pl.col(c).cast(pl.Int64) for c in ID_COLS])


def main() -> None:
    raw_hashes = verify_raw()
    train_files = sorted(glob.glob(str(RAW / "training_*.parquet")))
    train = pl.read_parquet(train_files).with_columns(pl.lit("train").alias("src"))
    rank = pl.read_parquet(RAW / "ranking.parquet").with_columns(pl.lit("rank").alias("src"))
    n_in = train.height + rank.height

    silver = (
        cast_ids(pl.concat([train, rank], how="vertical_relaxed"))
        .with_columns(pl.col("MVT_TIME_UTC_mvt").dt.strftime("%Y-%m").alias("month"))
        .sort(["MVT_TIME_UTC_mvt", "MVT_ID_mvt"])
    )
    assert silver.height == n_in, "row count changed"
    assert silver["MVT_ID_mvt"].n_unique() == silver.height, "MVT_ID not unique"

    SILVER.parent.mkdir(parents=True, exist_ok=True)
    silver.write_parquet(SILVER, compression="zstd", statistics=True)

    manifest = {
        "schema": "artifact-manifest-v1",
        "path": str(SILVER.relative_to(ROOT)),
        "layer": "silver",
        "producing_experiment": None,
        "format": "parquet/zstd",
        "rows": silver.height,
        "rows_by_src_phase": silver.group_by("src", "PHASE_mvt").len().sort("src", "PHASE_mvt")
        .rows(),
        "columns": {c: str(t) for c, t in silver.schema.items()},
        "size": SILVER.stat().st_size,
        "sha256": sha256_file(SILVER),
        "inputs_sha256": raw_hashes,
        "code_sha256": sha256_file(Path(__file__)),
        "code_commit": git_commit(),
        "code_dirty": git_dirty(),
        "created_utc": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reproduce": "uv run python scripts/build_silver.py",
    }
    SILVER_MANIFEST.write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"silver: {silver.height} rows, sha256 {manifest['sha256'][:12]}…")


if __name__ == "__main__":
    main()
