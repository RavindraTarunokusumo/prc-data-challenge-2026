---
schema: incident-v1
incident_id: INC-0007
type: infrastructure
created_utc: 2026-10-01T16:10:00Z
status: closed
---

# Day 5 start on the owner's laptop: memory below the brief's guard, data and credentials absent

**Raised by:** the researcher, at the D05-S01 session start. Days 5–7 move to the owner's laptop as planned (brief §3); this records what the laptop looked like at the start and the owner's decision.

## Evidence (measured 2026-10-01T15:59Z)

| Item | Brief / `config/resources.yaml` (cloud) | Laptop at D05-S01 start |
|---|---|---|
| CPU | 4 vCPU | AMD Ryzen 7 260, 8 cores / 16 threads |
| RAM | 15 GB, no swap; hard guard 11 GB per experiment | **WSL2 7.4 GiB** (host 16 GB, no `.wslconfig`, WSL default 50 %), **2 GiB swap**; 4.2 GiB available |
| GPU | none | NVIDIA RTX 5060 Laptop, 8 GB, CUDA 13.1 driver |
| Data | `data/raw` 14 files, silver built | **empty** (fresh clone) |
| Credentials | env vars or `.env` | **none set** |

- Measured peaks: E019 4.76 GB, E024 5.73 GB. On 7.4 GiB with 4.2 GiB available those runs would swap or be OOM-killed.
- GPU probe on synthetic data (200k × 20; no project data): XGBoost 3.4.1 `device=cuda` **works**; CatBoost 1.2.10 `task_type=GPU` **works**; LightGBM 4.7.0 has **no GPU** (no OpenCL device; CUDA learner not built).
- Environment: `uv.lock` SHA-256 `39df945c…` (matches the hand-off); `gate.py status` OK (advisor `30fff5dd3c54`, frozen `32c41c0f9331`, 24 allocated); ruff clean; pytest 115 passed, 20 skipped, 7 failed + 1 error, **all 8 `FileNotFoundError` on `data/processed/silver.parquet`**.
- Researcher process launch arguments: `--model claude-opus-5-5 --effort high`, matching the brief (contrast INC-0004).

## Owner decision (D05-S01)

- **Raise WSL2 memory to 11 GB with swap 0** (`%USERPROFILE%\.wslconfig`: `[wsl2]` `memory=11GB`, `swap=0`), then `wsl --shutdown` and relaunch. This restores the brief's no-swap rule and makes the 11 GB per-experiment guard physically reachable. D05-S01 ends at the shutdown; D05-S02 starts from the committed records.
- **Credentials:** the owner provides them in a git-ignored `.env` (names in `.env.example`). Data is then re-downloaded per `docs/reproducibility/HANDOFF_D04.md` §4 and verified against the manifests and the frozen silver hash.

## Impact

- Infrastructure only. No frozen artifact, split, metric or gate check changes. No experiment has run on the laptop.
- `config/resources.yaml` describes the cloud host. The laptop's measured values go into a Day 5 calibration record; limits may only be tightened (brief §4).

## Resolution required

Closes when D05-S02 confirms WSL memory ≥ 11 GB with swap 0, the raw data matches `raw_manifest.json`, and the silver hash matches `config/splits.yaml`.

## Update (D05-S02, 2026-10-01T16:15Z, appended)

- The restart after D05-S01 came up unchanged (7.4 GiB, 2 GiB swap): `C:\Users\rvind\.wslconfig` had not been created. With the owner's permission the researcher wrote it (`[wsl2]`, `memory=11GB`, `swap=0`) at 16:12Z. It takes effect at the next `wsl --shutdown`.
- Credentials: `.env` provided by the owner. Data: re-downloaded and verified, and the silver rebuild is byte-identical (`research/day-05/sessions/D05-S02/DATA_VERIFICATION.md`). Two of the three closing conditions are met. **Memory ≥ 11 GB with swap 0 is still open.**

## Closure (2026-10-01T16:16:18Z)

All three closing conditions are met (D05-S03 start, boot ID `71605e21…`):
- **Memory:** WSL2 10,951 MiB total (`memory=11GB`), **swap 0** (`swapon --show` empty). The brief's 11 GB per-experiment guard is physically reachable, and the no-swap rule holds.
- **Raw data** matches `raw_manifest.json`, and the **silver hash** matches `config/splits.yaml` (`efde4262…`; re-checked after the restart). See `research/day-05/sessions/D05-S02/DATA_VERIFICATION.md`.
- Laptop compute calibration (runtime, GPU) goes into a Day 5 calibration record, starting with the E019 reproduction.

## Pointer (appended 2026-10-02; D5-C15 (d))

The swap-0 closure above held only for boot `71605e21` (16:16–16:33Z). From boot `cf2c705b` (16:33:25Z) the VM has 4 GiB of swap (`.wslconfig` changed at 16:30:17Z). The owner decided to keep it: see **INC-0010**.
