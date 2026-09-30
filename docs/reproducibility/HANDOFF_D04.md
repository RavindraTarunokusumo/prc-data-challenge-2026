# Hand-off at the end of Day 4 (for Days 5-7, owner laptop)

**Status: DRAFT — champion section to be finalised at the Day 4 phase close.**
Written 2026-09-30 from branch `day-4`; repository values below were read from files or from `gate.py status`, `pytest` and `ruff` runs on that date.

## 1. Purpose

Lets the owner continue on the laptop (WSL2, RTX 5060) from files alone: set up, re-download data, reproduce the champion's validation predictions, and know what governance carries over.

<!-- CHAMPION-FINAL -->
**Champion (provisional): E019** (H015 v2, routed LightGBM on FS2; `models/champion/CURRENT.json`). Development mean 444.49 s. Holdout H recorded once (WIN, 375.93 vs E005 411.29). Replace this block at the Day 4 phase close if the champion changes.
<!-- /CHAMPION-FINAL -->

## 2. Repository state

- One branch per research phase, `day-N` (`day-1` ... `day-4`), branched from `main`. PRs go from `day-N` into `main`. Day 5 starts as `day-5` from `main` after the Day 4 PR merges.
- Read first: `docs/PROJECT_BRIEF.md` (v3.0), `AGENTS.md`, `docs/governance/COMMUNICATION_CONTRACT.md`, `research/STATE.md`, latest `research/day-NN/DAY_SUMMARY.md` (Day 3 exists; `day-04/DAY_SUMMARY.md` is written at the phase close (not yet present)).

## 3. Environment setup

Python 3.11 (`requires-python >=3.11`), `uv`, pinned `uv.lock`.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # if uv is missing
uv sync
sha256sum uv.lock
# 39df945cddc466202080bfed4af714c86cbae429fa0d86592bd4895a33f4b73b
uv run pytest -q          # cloud: 141 passed
uv run ruff check .       # cloud: All checks passed!
uv run python scripts/gate.py status
```

Expected `gate.py status` output (a mismatch blocks allocation and runs):

```text
advisor definition: 30fff5dd3c54 OK
frozen files: 32c41c0f9331 OK
experiments allocated: 22
```

The `uv.lock` hash and counts will change if later commits alter them; compare with the committed `HEAD`. CPU-only `uv sync` is what was tested; GPU-enabled wheels on the laptop are (unverified).

## 4. Data re-download

Variable names (values never stored in the repo; see `.env.example`; put them in a git-ignored `.env` or the shell):
`PRC_TEAM_NAME`, `PRC_SUBMISSION_BUCKET`, `PRC_S3_ENDPOINT`, `PRC_S3_ACCESS_KEY`, `PRC_S3_SECRET_KEY`; optional `PRC_DATA_BUCKET`, `OPENSKY_USERNAME`, `OPENSKY_PASSWORD`.

```bash
uv run python scripts/fetch_data.py --list    # inventory -> data/manifests/remote_inventory.json
uv run python scripts/fetch_data.py --pull    # data/raw/, verifies sizes, writes raw_manifest.json
uv run python scripts/build_silver.py         # data/processed/silver.parquet (verifies raw hashes first)
```

Network hosts must be on `config/network.yaml`. `fetch_data.py` refuses the submission bucket.

- Verify against `data/manifests/raw_manifest.json` (schema: path, source, size, etag, sha256): **14 files, 330,216,990 bytes** (12 monthly `training_*.parquet`, `ranking.parquet`, `submitting.parquet`). `build_silver.py` uses the 12 training files plus `ranking.parquet`.
- Expected silver: 4,857,331 rows x 32 columns, SHA-256 `efde426225040cd657e2a8c1be7576c6dd03cb2729fea5b303b6c4b9e9ec9c60` (`config/splits.yaml` `evaluation_population.silver_sha256`, also `data/manifests/silver_manifest.json`). The evaluator refuses a mismatch. Whether a rebuild on another OS or polars version is byte-identical to this hash is (unverified).
- Disk: `data/raw` 315 MB, `data/processed` 223 MB (measured on the cloud container). Brief budget for `data/` is 20 GB.
- Always read silver through `prc.data.load_silver` (it masks December 2025 DEP targets); never read the parquet directly.

## 5. Champion reproduction (E019 predictions)

A reproduction is a new experiment id with `purpose=reproduction`, the same H/version, and seed 43. `gate.py allocate` requires the existing proposal, review and ack files (present for H015 v2: `research/day-03/proposals/H015_v2.md`, `.../advisor/H015_review_v2.md`, `research/day-03/acks/H015_ack_v2.md`; the proposal/review/ack paths are taken from the `day` folder, verify it finds them) and the hashes above.

```bash
uv run python scripts/gate.py allocate H015 v2 --purpose reproduction   # prints the new id, call it E0XX (next is E023)
cp experiments/E022/config.yaml experiments/E0XX/config.yaml            # E022 was the Day 3 reproduction: purpose reproduction, seed 43
uv run python scripts/run_experiment.py E0XX
uv run python scripts/reproduce_check.py E0XX E019 --champion E005
```

The `config.yaml` is the E019 config (routed_lightgbm, FS2, learning_rate 0.05, num_leaves 255, min_data_in_leaf 100, num_boost_round 1000, `num_threads: 4`, all 8 folds) with `purpose: reproduction` and `seed: 43` (the seed is a no-op for deterministic LightGBM). Keep `num_threads: 4`. `check_config` refuses a run that omits any of R1,R2,R3,S1,W1,S1c,W1c,H.

Expected E019 RMSE (s); pass = each development fold within **1.0 s**:

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| RMSE | 446.40 | 274.49 | 397.25 | 632.10 | 472.22 | 638.38 | 488.59 | 444.49 |

(Dev mean is over R1,R2,R3,S1,W1 only; S1c, W1c are diagnostic; H is predicted only and never re-scored here.)

E019 prediction SHA-256 (`experiments/E019/manifest.json`; files `predictions/validation/E019/<fold>.parquet`):

| Fold | SHA-256 |
|---|---|
| R1 | 32eb274461a35ea29d158d948795e6c93cd6fd2d45cd80f80680570d6a1b77f7 |
| R2 | 1285d926ccbc7ea705da8ce347454a97bed64d42640d8c9eed3e7e7feef139d1 |
| R3 | c5c607c76c0ddf7131b99fac57da8b16d1fc60a208b5de652b7e7446dc6e8a67 |
| S1 | 48be32eba66c251b5649ae3f6c1f60ef88be3e4c4c1ab542710fad0b8721e289 |
| W1 | e70f403bee9633e671a85548c6f671592b08724d34f564bcb7f0a40b424902fc |
| S1c | 609a2a0a5dddf24f8ba7c928737ac0f3059dd785c6c6283c128d00fa4f301268 |
| W1c | 7dc49256bd4d1409c97d04ad946f3df905df488986956f4234da90115e223e6b |
| H | 464cb57a01e55921d51eaa848f2c0c30baaa857b74f021df3eb227a57efc9a1a |

LightGBM is deterministic here: E022 was byte-identical to E019, and Day 3 found identical output across two CPU model strings. On the same lockfile expect byte-identical files. A different OS, CPU architecture or LightGBM build may differ; then the 1.0 s rule decides, not the hash. Also note the silver hash must match first.

Resources: CLASS-M. E019 took 954 s (E022: 1,339 s on a slower CPU); expect about 16-22 min on 4 vCPU, peak RSS 4.76 GB (about 5 GB). Timeout 45 min, hard RAM 11 GB. Laptop runtime is (unverified).

## 6. Git-ignored artifacts and their manifests

| Ignored path | Covered by |
|---|---|
| `data/raw/*` | `data/manifests/raw_manifest.json` (and `remote_inventory.json`) |
| `data/processed/*` (silver) | `data/manifests/silver_manifest.json`, `config/splits.yaml` silver hash |
| `predictions/validation/*`, `predictions/final/*` | per-experiment `experiments/E###/manifest.json` (sha256 per file) |
| `runtime/ledger.sqlite` | tracked export `experiments/ledger.jsonl`; schema `runtime/ledger.sqlite.schema.sql` |
| `models/champion/*` except `CURRENT.json`, `models/candidates/*` | `CURRENT.json` (pointer only) |
| `.env`, `.env.*` | `.env.example` (names only) |

Ledger rebuild: there is no separate function, but `prc.ledger.connect()` does it automatically. If `runtime/ledger.sqlite` is missing it creates it from the schema and loads every row of `experiments/ledger.jsonl`. Any ledger call triggers it, for example:

```bash
uv run python -c "from prc import ledger; print(len(ledger.all_rows()))"
```

(Run from the repo root with `uv run`; expected 22 rows. Not executed here.)

## 7. Governance carried to Days 5-7

- Frozen (hash-checked by `gate.py`): `config/splits.yaml`, `src/prc/{__init__,metrics,splits,evaluate}.py`, `docs/methodology/DATASET_AUDIT.md`. Editing any blocks allocation and runs. Do not edit.
- Holdout H (Dec 2025): at most one access per phase, only via `evaluate.holdout_compare` / `scripts/holdout_check.py`, at the phase-close review. Day 3's access is used; Day 4's is (unverified, see `research/STATE.md`).
- Leaderboard and submission bucket: zero reads and zero submissions until project state is `FROZEN` (`docs/governance/LEADERBOARD_POLICY.md`). No searching for other teams' solutions.
- Flow unchanged: proposal -> Advisor review (envelope first, `advisor` subagent gets the envelope path) -> ack -> `gate.py allocate`.
- Open incidents (`status:` lines): INC-0004 open (launch configuration D03); INC-0005 open (owner's delegation instruction, Day 4). INC-0001 accepted; INC-0002 and INC-0003 closed.
- Standing rules and disclosures (D3-C1, D3-C2, D3-C3) live in `research/STATE.md`.

## 8. Day 5 pointers

- Per brief §3/§4, GPU boosting comparisons moved to Day 5 (Tier 3 neural is also a Day 5 option). Use a proposal that declares the GPU backend and VRAM.
- `gbm.catboost` and `routed_catboost` are registered (`src/prc/models/__init__.py`, `gbm.py`, `routed.py`). They share LightGBM's category vocabulary.
- CPU calibration (`research/day-04/eda/catboost_calibration.json`, `catboost_calibration_ctr1.json`): default `max_ctr_complexity` cost 0.88-1.13 s/iteration on R3; `max_ctr_complexity=1` cost about 0.29-0.30 s/iteration, extrapolated 35-45 min for 8 folds x 1000 iterations (CLASS-L). A GPU may lift that restriction; unmeasured (unverified).
- `resource-usage` classes, the 11 GB RAM guard and the seed rule (42 primary, 43 reproduction) are CPU-era; changes to `config/resources.yaml` may only tighten them.
