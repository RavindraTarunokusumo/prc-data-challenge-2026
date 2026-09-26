# Leaderboard Policy

- During the autonomous run (Days 1–7): **zero submissions and zero leaderboard reads.**
- The submission bucket `prc-2026-genuine-cabbage` is never listed, read or written until the project state is `FROZEN`. `scripts/fetch_data.py` hard-refuses any operation on it.
- After `FROZEN`: generate predictions, commit the final state, then submit once. The leaderboard score is recorded as an **external evaluation** in the final report and is never fed back into methodology.
- Searching for other PRC 2026 teams' repositories, feature engineering, published solutions or leaderboard discussions is forbidden. General methodological literature is allowed and is cited in the journal.
- Enforcement: literature access is limited to the hosts in `config/network.yaml`, and web searches always exclude github.com and kaggle.com.
