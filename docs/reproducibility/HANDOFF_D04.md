# Hand-off at the end of Day 4 (for Days 5-7, owner laptop)

**Status: FINAL** (Day 4 phase close X-D04-S02-0001 ACCEPT; finalised per correction D4-C14 at 2026-10-01T01:59:14Z).
Written from branch `day-4`. The repository values below were read from files, or from `gate.py status`, `pytest` and `ruff` runs, at finalisation.

## 1. Purpose

Lets the owner continue on the laptop (WSL2, RTX 5060) from files alone: set up, re-download data, reproduce the champion's validation predictions, and know what governance carries over.

<!-- CHAMPION-FINAL -->
**Champion: E019** (H015 v2, routed LightGBM on FS2; `models/champion/CURRENT.json`).
- **Status.** Champion since the Day 3 phase close, and **held through Day 4 by rule** (X-D04-S02-0001). It is Day 5's phase-opening champion.
- **Figures.** Development mean 444.49 s. Holdout H was recorded once (Day 3: WIN, 375.93 against E005's 411.29).
- **Standing disclosures (read before building on it):**
  - **D3-C1.** 95 % of its margin over E005 is routed FS1 structure. Congestion as served is −1.90 s on all rows.
  - **D3-C2.** It makes out-of-range predictions on NM-missing rows at the nine non-LIRF airports: below 0 s, or above 3,600 s on normal taxis. That is 81 in the > 3 h `d_sched` band, and 44 % of rows over 5 h. **The cause is confirmed by E023's exact ablation** (Day 4): the LightGBM trains on the routed LIRF NM-missing convention rows.
  - **D3-C3.** January 2026 has 435 NM-missing rows with `d_sched` > 3 h and 92 > 5 h. That is 2.0–2.6 times the 2025 maximum. H does not test it.
  - **D4-C9.** S1 against E019 is decided by one row.
    - Row 192622644 (LIRF, NM-present, y 87,002 s) carries 8.2 % of E019's S1 SSE; E019 predicts 8,136 s there.
    - E023's W1 WIN is likewise carried by row 183910286.
  - **Consequence.** The submitted model carries D3-C2 and D3-C3 unless a later candidate is promoted.
<!-- /CHAMPION-FINAL -->

## 2. Repository state

- One branch per research phase, `day-N` (`day-1` ... `day-4`), branched from `main`. PRs go from `day-N` into `main`. Day 5 starts as `day-5` from `main` after the Day 4 PR merges.
- Read first: `docs/PROJECT_BRIEF.md` (v3.0), `AGENTS.md`, `docs/governance/COMMUNICATION_CONTRACT.md`, `research/STATE.md`, `research/day-04/DAY_SUMMARY.md` (FINAL) and `research/day-04/acks/PHASE_CLOSE_D04_ack_v1.md` (rulings and corrections D4-C7 to D4-C16).

## 3. Environment setup

Python 3.11 (`requires-python >=3.11`), `uv`, pinned `uv.lock`.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # if uv is missing
uv sync
sha256sum uv.lock
# 39df945cddc466202080bfed4af714c86cbae429fa0d86592bd4895a33f4b73b
uv run pytest -q          # cloud: 143 passed
uv run ruff check .       # cloud: All checks passed!
uv run python scripts/gate.py status
```

Expected `gate.py status` output (a mismatch blocks allocation and runs):

```text
advisor definition: 30fff5dd3c54 OK
frozen files: 32c41c0f9331 OK
experiments allocated: 24
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

A reproduction is a new experiment id with `purpose=reproduction`, the same H/version, and seed 43. `gate.py allocate` requires the existing proposal, review and ack files (present for H015 v2: `research/day-03/proposals/H015_v2.md`, `.../advisor/H015_review_v2.md`, `research/day-03/acks/H015_ack_v2.md`) and the hashes above.

**Gate semantics (D4-C14 (v), D4-C15):** `gate.py` copies `day` and `session` from the proposal's folder and front matter, not from the current phase. So a Day 5 reproduction of H015 v2 is recorded as `day-03` / D03-S01, and E024 shows D04-S01 although it was allocated in D04-S02. This is the tool's semantics; do not edit gate records. A **Day 5 holdout access needs a Day 5 allocation as NEW** (§7).

```bash
uv run python scripts/gate.py allocate H015 v2 --purpose reproduction   # prints the new id, call it E0XX (next is E025)
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

Resources: CLASS-M. E019 took 954 s (E022: 1,339 s on another CPU string); expect about 16-22 min on 4 vCPU, peak RSS 4.76 GB (about 5 GB). Timeout 45 min, hard RAM 11 GB. Laptop runtime is (unverified).

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

(Run from the repo root with `uv run`; expected 24 rows. Not executed here.)

## 7. Governance carried to Days 5-7

- Frozen (hash-checked by `gate.py`): `config/splits.yaml`, `src/prc/{__init__,metrics,splits,evaluate}.py`, `docs/methodology/DATASET_AUDIT.md`. Editing any blocks allocation and runs. Do not edit.
- Holdout H (Dec 2025): at most one access per phase, only via `evaluate.holdout_compare` / `scripts/holdout_check.py`, at the phase-close review. Record so far:
  - Day 1: used (WIN). Day 2: closed unused (ruling H). Day 3: used (WIN, E019 vs E005).
  - **Day 4: 0 of 1, closed unused (ruling H4; not a TIE).** There is no carry-over: **Day 5 has exactly one access.**
  - `holdout_compare` takes the phase from NEW's gate record, so a Day 5 access needs a Day 5 allocation as NEW.
  - **E012–E018 and E020–E024 may never be NEW** (rule 9). In particular, no `holdout_check.py` with E023 or E024 as NEW, in any phase, even though `day-04` still shows an unused access and the code would accept them.
- Leaderboard and submission bucket: zero reads and zero submissions until project state is `FROZEN` (`docs/governance/LEADERBOARD_POLICY.md`). No searching for other teams' solutions.
- Flow unchanged: proposal -> Advisor review (envelope first, `advisor` subagent gets the envelope path) -> ack -> `gate.py allocate`.
- Open incidents (`status:` lines): INC-0004 open (launch configuration D03; owner decision). INC-0005 closed at the Day 4 phase close; **any delegation to worker models on Days 5–7 needs a new incident.** INC-0001 accepted; INC-0002 and INC-0003 closed.
- Standing rules 1–12, batch conditions B1–B4, rulings H, B, R, H3 and H4, and the champion disclosures (D3-C1 to D3-C3, D4-C9) live in `research/STATE.md`.
- **Rule 10 (no re-adjudication)** covers the configurations of E020, E021, E023 and E024. A variant that differs only by compute backend or library build (e.g. GPU LightGBM) is a re-draw of the same configuration. It is admissible as a candidate only if its proposal pre-registers a mechanism for that difference (X-D04-S02-0001 (e)).
- **Ledger decisions** (D4-C11): E019 and E022 PROMOTE; E023 and E024 REJECT; E020 and E021 none by design.

## 8. Day 5 pointers

- Per brief §3/§4, GPU boosting comparisons moved to Day 5 (Tier 3 neural is also a Day 5 option). Use a proposal that declares the GPU backend and VRAM.
- `gbm.catboost` and `routed_catboost` are registered (`src/prc/models/__init__.py`, `gbm.py`, `routed.py`). They share LightGBM's category vocabulary.
- CPU calibration (`research/day-04/eda/catboost_calibration.json`, `catboost_calibration_ctr1.json`): default `max_ctr_complexity` cost 0.88-1.13 s/iteration on R3; `max_ctr_complexity=1` cost about 0.29-0.30 s/iteration, extrapolated 35-45 min for 8 folds x 1000 iterations (CLASS-L). A GPU may lift that restriction; unmeasured (unverified).
- `resource-usage` classes, the 11 GB RAM guard and the seed rule (42 primary, 43 reproduction) are CPU-era; changes to `config/resources.yaml` may only tighten them.
- **H020 v1 (CatBoost) was REJECTED in Day 4** (`research/day-04/advisor/H020_review_v1.md`, `acks/H020_ack_v1.md`), and CatBoost was deferred to Day 5. The review's objections, which any CatBoost proposal must answer (Missing Control 3 of X-D04-S02-0001):
  - **Boosting type.** The installed CatBoost 1.2.10 ran *plain*, not ordered, boosting. State and check the scheme via `get_all_params()`.
  - **CTR type.** Its RMSE categorical statistics are a border share and a frequency count, not a smoothed target mean. Do not claim a target-mean mechanism without checking.
  - **Pre-collapse levels.** FS1's `__RARE__` collapse removes the sparse levels that a sparse-level mechanism needs. Keep them if that mechanism is claimed.
  - **CTR complexity.** `max_ctr_complexity: 1` removes the stand × runway combination.
  - **Capacity control.** Include a contrast whose only difference is the categorical handling, at fixed capacity.
  - **Rationale.** A CLASS-L or GPU rationale must be tied to a decision.
  - **Calibration.** Commit the calibration script and its exact invocation: `scripts/calibrate_catboost.py` is committed, but the `max_ctr_complexity=1` addendum (`af21355`) committed only its JSON.

## 9. Open work from Day 4 (not results)

- **E023 (H018 v2): mechanism supported, "D3-C2 treated, not promoted"** (ledger REJECT).
  - Excluding the routed LIRF NM-missing rows from LightGBM training (`route_train_exclude: true`) cuts the > 3 h out-of-range band from 81 to 5. All rows −2.04 s against E019; development mean 442.46.
  - It failed criterion 2: S1 TIE, carried by the single row 192622644 (D4-C9).
- **E024 (H019 v2, FS3 priors): mechanism falsified** (ledger REJECT).
  - −0.29 s on `NM_present_excl_LIRF` against E023 (floor −3.0 s); −0.40 s on all rows. Development mean 442.06.
  - "LightGBM already holds the keys" is untested. Its controls are a within-key permuted prior and a K5-only block.
- **Hand-off base ruling (X-D04-S02-0001 (e), as written):**
  - Under ruling R, E023 is the matched reference for any candidate that keeps `route_train_exclude: true` on FS2, and E024 for FS3.
  - **E023 is not a default or recommended base, and not a de facto champion.** Choosing the base is a Day 5 proposal's decision.
  - Such a candidate is judged against **E019**. Its criterion 4 includes H018 v2's clauses 1–2 (both recorded as not met). Its rule 8 pre-registration states the single-row S1 exposure.
- **Single-row exposure (Missing Control 1).** A Day 5–7 candidate compared with E019, whose promotion needs S1 (or W1), states under rule 8:
  - its expected direction on rows 192622644 (S1) and 183910286 (W1);
  - the `NM_present_LIRF` cell expectation, read as a single-row statistic.

  This is a disclosure, not a new reading of criterion 2.

## 10. Producing submission predictions (note; not required by brief §3)

- `config/splits.yaml` defines the final folds `SUBMIT_JAN` (train 2025-01..12, predict 2026-01) and `SUBMIT_JUL` (predict 2026-07). There is one fold per ranking month, and no cross-month information.
- `run_experiment.py` accepts final folds, and `prc.data.load_silver` unmasks December 2025 targets only for a final (SUBMIT) run, logging the event.
- The exact Day 7 procedure (allocation, config and file format) is **not yet written or tested**. The submission bucket stays untouched until the project state is FROZEN (`docs/governance/LEADERBOARD_POLICY.md`).
