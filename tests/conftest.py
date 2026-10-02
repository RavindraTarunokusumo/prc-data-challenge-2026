import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import prc  # noqa: F401  (sets the polars env var before polars is imported)
from prc.paths import SILVER, running_experiment


@pytest.fixture(scope="session")
def silver():
    if not SILVER.exists():
        pytest.skip("silver layer not built (uv run python scripts/build_silver.py)")
    if (eid := running_experiment()):
        pytest.skip(f"{eid} is running: real-silver tests stand down (INC-0008)")
    from prc.data import load_silver

    return load_silver()
