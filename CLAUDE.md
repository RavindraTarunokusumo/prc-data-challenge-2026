# CLAUDE.md

Follow `AGENTS.md` and `docs/PROJECT_BRIEF.md` (v3.0).

- Environment: `uv sync`, then `uv run ...`. Python 3.11. CPU only in the cloud container.
- Data: `uv run python scripts/fetch_data.py --list | --pull` (needs the env vars from `.env.example`).
- Tests: `uv run pytest`. Lint: `uv run ruff check .`
- Advisor reviews: write the envelope first, then spawn the `advisor` subagent with the envelope path only.
- Network: read `config/network.yaml` before researching. Fetch only from allowlisted hosts.
- Branches: one per research phase, named `day-N` (e.g. `day-1`, `day-2`), branched from `main`. PRs go from `day-N` into `main`.
