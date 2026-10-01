# CLAUDE.md

Follow `AGENTS.md` and `docs/PROJECT_BRIEF.md` (v3.0).

- Environment: `uv sync`, then `uv run ...`. Python 3.11. CPU only in the cloud container.
- Data: `uv run python scripts/fetch_data.py --list | --pull` (needs the env vars from `.env.example`).
- Tests: `uv run pytest`. Lint: `uv run ruff check .`
- Advisor reviews: write the envelope first, then spawn the `advisor` subagent with the envelope path only.
- Network: read `config/network.yaml` before researching. Fetch only from allowlisted hosts.
- Branches: one per research phase, named `day-N` (e.g. `day-1`, `day-2`), branched from `main`. PRs go from `day-N` into `main`.

## Reporting to the owner

How chat replies to the owner read. It does not change the research records (`DAY_SUMMARY.md`, analyses, journal), which keep their full detail.

- **Abstract and general.** Report progress at a broad level. Leave out experiment and hypothesis IDs, rule and clause numbers, per-fold figures, file paths and governance mechanics unless the owner asks for detail.
- **Status queries** ("Status?"): one or two sentences. What is happening now, what is next, and any issue.
- **Progress updates:** a few short bullets: setup, research, next step, issues.
- **End-of-phase (end-of-day) reports:** outcome, the ideas tested and what each showed in plain words, a small table of key metrics (champion validation RMSE, best run of the phase, baseline), holdout use, and what carries forward.
- **Always stated plainly,** even at this level: failures, my own mistakes, and anything that needs the owner's decision.
