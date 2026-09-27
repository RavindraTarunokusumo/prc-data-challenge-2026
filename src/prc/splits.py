"""Interpretation of the frozen config/splits.yaml and the validation masking protocol.

Frozen together with config/splits.yaml, src/prc/metrics.py and src/prc/evaluate.py
(hashes checked by scripts/gate.py). Imports no other prc module: its config path is
resolved from this file's own location. See docs/methodology/DATASET_AUDIT.md §6.4.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import polars as pl
import yaml

SPLITS_PATH = Path(__file__).resolve().parents[2] / "config" / "splits.yaml"
TARGET = "TAXITIME_SEC_mvt"
BLANKED_DEP_COLS = ("BLOCK_TIME_UTC_mvt", "TAXITIME_SEC_mvt")
SECTIONS = ("development_folds", "diagnostic_folds", "protected_holdout", "final")


@dataclass(frozen=True)
class Fold:
    fold_id: str
    kind: str
    train_months: tuple[str, ...]
    val_months: tuple[str, ...]
    embargo_months: tuple[str, ...] = ()

    @property
    def months(self) -> tuple[str, ...]:
        return self.train_months + self.val_months


@lru_cache(maxsize=1)
def load_splits() -> dict:
    return yaml.safe_load(SPLITS_PATH.read_text())


def promotion_config() -> dict:
    return load_splits()["promotion"]


def development_folds() -> tuple[str, ...]:
    return tuple(promotion_config()["development_folds"])


def holdout_months() -> tuple[str, ...]:
    cfg = load_splits()["protected_holdout"]
    return tuple(str(m) for f in cfg.values() for m in f["val_months"])


def get_fold(fold_id: str) -> Fold:
    cfg = load_splits()
    for section in SECTIONS:
        if fold_id in cfg.get(section, {}):
            f = cfg[section][fold_id]
            fold = Fold(
                fold_id=fold_id,
                kind=f["kind"],
                train_months=tuple(str(m) for m in f["train_months"]),
                val_months=tuple(str(m) for m in f["val_months"]),
                embargo_months=tuple(str(m) for m in f.get("embargo_months", [])),
            )
            overlap = set(fold.train_months) & set(fold.val_months + fold.embargo_months)
            if overlap:
                raise ValueError(f"fold {fold_id}: train overlaps val/embargo: {overlap}")
            return fold
    raise KeyError(f"unknown fold {fold_id}")


def masked_view(silver: pl.DataFrame | pl.LazyFrame, fold: Fold) -> pl.LazyFrame:
    """Feature-building input for a fold, reproducing the ranking information set.

    Rows of training months are complete; rows of validation months have the DEP
    block time and target nulled (ARR rows stay complete); all other months are
    absent. Adds `role` = 'train' | 'val'.
    """
    lf = silver.lazy() if isinstance(silver, pl.DataFrame) else silver
    is_val = pl.col("month").is_in(list(fold.val_months))
    hide = is_val & (pl.col("PHASE_mvt") == "DEP")
    return (
        lf.filter(pl.col("month").is_in(list(fold.months)))
        .with_columns(
            [pl.when(hide).then(None).otherwise(pl.col(c)).alias(c) for c in BLANKED_DEP_COLS]
        )
        .with_columns(pl.when(is_val).then(pl.lit("val")).otherwise(pl.lit("train")).alias("role"))
    )


def train_targets(silver: pl.DataFrame | pl.LazyFrame, fold: Fold) -> pl.LazyFrame:
    """DEP rows of the fold's training months, with target. The only source of target
    statistics for the fold (DATA_POLICY §5, §9)."""
    lf = silver.lazy() if isinstance(silver, pl.DataFrame) else silver
    return lf.filter(
        pl.col("month").is_in(list(fold.train_months)) & (pl.col("PHASE_mvt") == "DEP")
    )


def eval_rows(silver: pl.DataFrame | pl.LazyFrame, fold: Fold) -> pl.LazyFrame:
    """The fixed evaluation population: all DEP rows of the validation months.

    Used by prc.evaluate; feature and model code must not import it (tests/test_isolation.py).
    """
    lf = silver.lazy() if isinstance(silver, pl.DataFrame) else silver
    return lf.filter(
        pl.col("month").is_in(list(fold.val_months)) & (pl.col("PHASE_mvt") == "DEP")
    )
