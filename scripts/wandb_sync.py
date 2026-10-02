"""Mirror experiment records to Weights & Biases (INC-0009). Idempotent: run id == E###.

    uv run python scripts/wandb_sync.py            # every experiment in the ledger
    uv run python scripts/wandb_sync.py E026 ...   # selected experiments
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prc import ledger, tracking


def main() -> None:
    if not tracking.enabled():
        sys.exit("WANDB_API_KEY not set (environment or .env), or PRC_WANDB=0")
    eids = sys.argv[1:] or [r["experiment_id"] for r in ledger.all_rows()]
    for eid in eids:
        if ledger.get(eid) is None:
            print(f"{eid}: not in the ledger, skipped")
            continue
        print(f"{eid}: {tracking.sync(eid)}", flush=True)


if __name__ == "__main__":
    main()
