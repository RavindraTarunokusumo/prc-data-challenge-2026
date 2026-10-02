# D06-S01 pre-window check (C1)

*Written 2026-10-02T18:14:05Z (measured), before arming the launcher.*

- **Allocations** (`gate.py allocate … v2`, purpose `primary`, in C1 order): H026 → E035, H024 → E036, H025 → E037, H027 → E038, H028 → E039. Each `gate.json` names its hypothesis and v2.
- **Configs:** each `experiments/E03x/config.yaml` equals its proposal's config block (parsed YAML equality) apart from `hypothesis_id`, `proposal_version` and `purpose`; `scripts/run_experiment.py::check_config` accepts all five (seed 42 for `primary`).
- **Launcher:** `research/day-06/sessions/D06-S01/run_window.sh`, SHA-256 `9da5b0c3700b6f2c294b2da6f0218e686a6f01711b20854ae4441aba97cf6a4d` (as pinned in H024 v2 §Batch).
- **Freeze:** `git diff --stat 4ad18a1 -- src scripts pyproject.toml uv.lock config` is empty.
- **Environment:** unchanged from SESSION_START (rule L v2 item 6).
- **Next:** commit and push, confirm a clean tree, arm the launcher in the background (it waits for 21:00 Europe/Amsterdam). No repository file is touched until the queue ends.
