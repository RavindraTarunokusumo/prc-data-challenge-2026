"""Silver-layer access with manifest verification.

Protected-holdout targets are masked here by default (R2): DEP block time and target of
the holdout months are nulled before any caller sees them. Only final (SUBMIT) training
may unmask them, and doing so is logged in the task ledger.
"""

from __future__ import annotations

import datetime as dt
import json

import polars as pl

from prc.paths import ROOT, SILVER, SILVER_MANIFEST, sha256_file
from prc.splits import BLANKED_DEP_COLS, holdout_months

TASK_LEDGER = ROOT / "orchestration" / "task-ledger.jsonl"


def load_silver(columns: list[str] | None = None, verify: bool = True,
                unmask_holdout_for: str | None = None) -> pl.DataFrame:
    """Load silver with holdout-month DEP targets nulled.

    `unmask_holdout_for`: experiment id of a final (SUBMIT) run that trains on the
    holdout months; the unmasking is logged.
    """
    if verify:
        manifest = json.loads(SILVER_MANIFEST.read_text())
        if sha256_file(SILVER) != manifest["sha256"]:
            raise RuntimeError("silver.parquet does not match data/manifests/silver_manifest.json")
    df = pl.read_parquet(SILVER, columns=columns)
    if unmask_holdout_for is not None:
        with open(TASK_LEDGER, "a") as f:
            f.write(json.dumps({
                "event": "holdout_targets_unmasked_for_final_training",
                "experiment_id": unmask_holdout_for,
                "utc": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")}) + "\n")
        return df
    if "month" not in df.columns or "PHASE_mvt" not in df.columns:
        return df.drop([c for c in BLANKED_DEP_COLS if c in df.columns])
    hide = pl.col("month").is_in(list(holdout_months())) & (pl.col("PHASE_mvt") == "DEP")
    return df.with_columns(
        [pl.when(hide).then(None).otherwise(pl.col(c)).alias(c)
         for c in BLANKED_DEP_COLS if c in df.columns])
