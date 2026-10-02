# D06-S01 pre-window check (C1)

*Written 2026-10-02T18:14:05Z (measured), before arming the launcher.*

- **Allocations** (`gate.py allocate … v2`, purpose `primary`, in C1 order): H026 → E035, H024 → E036, H025 → E037, H027 → E038, H028 → E039. Each `gate.json` names its hypothesis and v2.
- **Configs:** each `experiments/E03x/config.yaml` equals its proposal's config block (parsed YAML equality) apart from `hypothesis_id`, `proposal_version` and `purpose`; `scripts/run_experiment.py::check_config` accepts all five (seed 42 for `primary`).
- **Launcher:** `research/day-06/sessions/D06-S01/run_window.sh`, SHA-256 `9da5b0c3700b6f2c294b2da6f0218e686a6f01711b20854ae4441aba97cf6a4d` (as pinned in H024 v2 §Batch).
- **Freeze:** `git diff --stat 4ad18a1 -- src scripts pyproject.toml uv.lock config` is empty.
- **Environment:** unchanged from SESSION_START (rule L v2 item 6).
- **Next:** commit and push, confirm a clean tree, arm the launcher in the background (it waits for 21:00 Europe/Amsterdam). No repository file is touched until the queue ends.

## After the window (appended)

- All five runs COMPLETE between 19:00:05Z and 19:29:17Z; each passed its route check and was committed and pushed by the launcher (`2657659`, `563891b`, `1e01158`, `2a7d2b2`, `50fb392`). **No run executed past 21:30: no INC-0012 deviation.** Launcher log: `run_window.log` here.
- GPU memory of 4.3–5.2 GB was held during the window by a process outside the WSL VM's view (921 MiB at the session start); E036's own share was about 2.2 GB. No GPU failure.
- The W&B mirror synced each run at completion; a re-sync after the analyses timed out (`api.wandb.ai` deadline) and will be retried.
- Delegated (INC-0013): `research/day-06/eda/d06_diagnostics.py` and its test, implemented by a `claude-sonnet-5-5` worker to the researcher's specification; reviewed by the researcher. SHA-256 `5fc21113613c675ec772390672132e78556ca6336bc736e10f7d8bc90c4e10b7`.
