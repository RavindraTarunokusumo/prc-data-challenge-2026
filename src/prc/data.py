"""Silver-layer access with manifest verification."""

from __future__ import annotations

import json

import polars as pl

from prc.paths import SILVER, SILVER_MANIFEST, sha256_file


def load_silver(columns: list[str] | None = None, verify: bool = True) -> pl.DataFrame:
    if verify:
        manifest = json.loads(SILVER_MANIFEST.read_text())
        if sha256_file(SILVER) != manifest["sha256"]:
            raise RuntimeError("silver.parquet does not match data/manifests/silver_manifest.json")
    return pl.read_parquet(SILVER, columns=columns)
