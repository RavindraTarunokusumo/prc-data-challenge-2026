"""Learning-curve diagnostics (Day 5, owner request; mirrored to W&B under INC-0009).

For tree learners, one fold at a time:
- the learner's own training RMSE at every iteration (its training loss on its training
  rows; no validation row is involved);
- staged validation predictions every STEP iterations, taken from the finished model.

Nothing here feeds back into training: no early stopping, no validation set inside the
learner, no change to parameters. Predictions are identical with or without recording
(tests/test_models.py). The worker scores the staged predictions against truth through
prc.evaluate.truth_frame after training, for development and diagnostic folds only; the
protected holdout never gets a validation curve.
"""

from __future__ import annotations

import numpy as np

STEP = 10
_state: dict = {"on": False}


def start() -> None:
    _state.clear()
    _state["on"] = True


def active() -> bool:
    return bool(_state.get("on"))


def grid(rounds: int) -> list[int]:
    """Iterations at which staged predictions are taken: 1, STEP, 2*STEP, ..., rounds."""
    return sorted({1, rounds, *range(STEP, rounds + 1, STEP)})


def record(learner: str, train_rmse, ids, iterations: list[int], staged: np.ndarray) -> None:
    """train_rmse: per iteration (index 0 = iteration 1); staged: (n_val, len(iterations))."""
    if active():
        _state.update(learner=learner, train_rmse=[float(v) for v in train_rmse],
                      ids=np.asarray(ids), iterations=list(iterations), staged=staged)


def note_params(params: dict) -> None:
    """Record the learner's resolved parameters for this fold (written by the worker to
    resolved_params.json)."""
    if active():
        _state["resolved_params"] = params


def override(ids, values) -> None:
    """Hold rows (e.g. routed rows) at a fixed prediction across every stage."""
    if active() and "staged" in _state:
        pos = {int(m): i for i, m in enumerate(_state["ids"])}
        rows = np.array([pos[int(m)] for m in ids], dtype=np.int64)
        if rows.size:
            _state["staged"][rows, :] = np.asarray(values, dtype=np.float64)[:, None]


def take() -> dict | None:
    out = dict(_state) if "staged" in _state else None
    _state.clear()
    return out
