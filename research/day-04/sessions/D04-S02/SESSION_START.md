# D04-S02 session start

*Written 2026-10-01T00:50:29Z (measured with `date -u`).*

- **Why a new session:** the container restarted after E023 was allocated in D04-S01 (boot id `dd719b28-…` → `f948bf23-…`). COMMUNICATION_CONTRACT §1 requires a new session number after a reset (the D3-C5 lesson). State is rebuilt from the repository only.
- **State recovered** (`research/STATE.md` 17:48:59Z; commit `da47b81`):
  - Day 4 in progress.
  - Last exchange X-D04-S01-0002: H018 v2 ACCEPT 0.86, H019 v2 ACCEPT 0.80.
  - Champion E019 (H015 v2).
- **Open allocation:** **E023**, H018 v2 primary, allocated 17:49:07Z at `da47b81` from a clean tree.
  - Status ALLOCATED; no `config.yaml`, not run.
  - Its `gate.json` and ledger lines were uncommitted and survived the restart. They are committed now.
- **Checks at start:**
  - `gate.py status`: advisor definition and frozen files OK.
  - Raw data: 14/14 files match the manifest.
  - Silver hash verified on load.
  - **Tools freeze** (H018 review, item 1(e)): `git diff d1cc43b HEAD -- src scripts pyproject.toml uv.lock` is empty.
- **Provenance.**
  - **CPU:** Intel(R) Xeon(R) Processor @ 2.80GHz.
  - **Researcher process:** `--model claude-opus-5-5 --effort medium`, relaunched 2026-10-01T00:49:13Z (INC-0004, open).
  - **Delegation:** INC-0005 in force.
- **Champion:** E019. **Incidents:** INC-0004 and INC-0005, both open and non-blocking.
- **First action:** write E023's `config.yaml` per the H018 review's authorization item 2 (E019's config with `hypothesis_id: H018`, `proposal_version: 2` and `params.route_train_exclude: true`), then run it, then chain step 1.
