# D05-S02 data and environment verification (owner laptop, WSL2)

*Measured 2026-10-01T16:12–16:15Z. Commit `9f202b7`, clean tree.*

| Check | Expected (hand-off §3–§4) | Laptop | Result |
|---|---|---|---|
| `fetch_data.py --list` | 14 objects in `prc-2026-datasets` | 14 objects, 0.33 GB | OK |
| `fetch_data.py --pull` vs committed `raw_manifest.json` | 14 files, 330,216,990 bytes | same 14 paths; size, SHA-256 and ETag identical on every file; 330,216,990 bytes | **OK** |
| `build_silver.py` | 4,857,331 rows, SHA-256 `efde426225040cd6…9e9ec9c60` | 4,857,331 rows, `efde426225040cd657e2a8c1be7576c6dd03cb2729fea5b303b6c4b9e9ec9c60` | **byte-identical** |
| Silver build resources | (not recorded) | 27 s wall, peak RSS 6.06 GB | measured |
| `pytest -q` | 143 passed (cloud) | 143 passed | OK |
| `ruff check .` | clean | clean | OK |
| Ledger rebuild from `experiments/ledger.jsonl` | 24 rows | 24 rows | OK |

- Hand-off §4 listed whether a rebuild on another OS or polars version gives the same silver hash as (unverified). **It does** on this laptop with the same `uv.lock`.
- `fetch_data.py` and `build_silver.py` rewrite the tracked manifests with new timestamps and the current commit. The data is identical, so the committed manifests (`remote_inventory.json`, `raw_manifest.json`, `silver_manifest.json`) were restored with `git checkout` and not rewritten (immutable history). This file is the Day 5 verification record.
- The silver build's 6.06 GB peak is close to the current 7.4 GiB WSL limit (2 GiB swap on). **No experiment runs before the WSL restart with `memory=11GB`, `swap=0`** (INC-0007).
