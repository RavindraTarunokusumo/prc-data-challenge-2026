# PRC Data Challenge 2026 — team genuine-cabbage

Taxi-out-time prediction for the [PRC Data Challenge 2026](https://prc-data-challenge-2026.netlify.app/),
run as an autonomous ML research experiment: a Claude researcher and a fixed
Claude Advisor, operating under repository-enforced governance.

- Brief: [`docs/PROJECT_BRIEF.md`](docs/PROJECT_BRIEF.md)
- Governance: [`docs/governance/`](docs/governance/)
- Research record: [`research/`](research/)

```bash
uv sync
cp .env.example .env   # fill in credentials locally; never commit .env
uv run python scripts/fetch_data.py --list
uv run python scripts/fetch_data.py --pull
```
