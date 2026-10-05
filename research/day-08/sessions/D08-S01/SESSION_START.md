# D08-S01 session start

*Written 2026-10-05 (measured 2026-10-05T09:31:17Z with `date -u`).*

- **Why a new session:** the owner reopens the project after FROZEN (INC-0017): "Please begin Day 8", and then "New research phase. We have 5 more days to bump our scores to AT LEAST < 250 s". The Day 7 PR is merged into `main` (`88cdb22`). Branch `day-8` is cut from `main` at `88cdb22`; the tree was clean.
- **Where:** the Claude Code cloud container (4 vCPU, 15 GB, no GPU). Days 8–12 compute runs on the owner's laptop (INC-0017). This session does governance and text work only.
  - **This container's `runtime/ledger.sqlite` is a Day 4 copy** (`gate.py status`: 24 allocated). No allocation is made here.
  - Stored predictions here go up to E024 only.
- **State recovered** from `research/STATE.md` (Phase: FROZEN), `research/day-07/DAY_SUMMARY.md` (FINAL), the ledgers and the mirrors:
  - **Champion E046** (H035 v1): E033 with the LIRF NM-missing subgroup from E045. Development mean 314.42 s. December 2025 (E046 against E033, one access): WIN, −124.24 s.
  - **Submission:** E050's file (`f0dc2c7c…`), uploaded by the owner (owner's report; `research/day-07/submission/UPLOAD_RECORD.md`). **No leaderboard figure seen.**
  - **Standing disclosures:** E033's, plus U6 (the convention bet), U7, rule 6, rule 12, D7-C7 and the H exposure.
  - **Standing rules** 1–14; rulings H, B, R, H3–H7; rule L v2; P1–P9 of X-D07-S01-0003.
- **Remaining budget:** none defined. Ruling H7 made Day 7's access the last H read. The next experiment ID is **E051** (laptop).
- **Freeze:** `gate.py status`: frozen `32c41c0f9331` OK, advisor definition `30fff5dd3c54` OK.
- **Open incidents:** INC-0004, INC-0009, INC-0010; new: **INC-0017** (reopening), **INC-0018** (Sonnet delegation).
- **Resolved model ID:** researcher `claude-opus-5-5` (served model per the session API); Advisor `advisor` subagent, definition `30fff5dd3c54`.
- **Facts checked (target-free, or from recorded metrics):**
  - The challenge closes 2026-10-11 23:59:59 CET (challenge index page; allowlisted host). The ranking page was not opened, because it carries the leaderboard.
  - E046's recorded segment metrics: rows ≥ 3,600 s are 0.14–0.53 % of each fold and 20–65 % of its SSE. The analysis is in PHASE_OPEN_D08 §3.
- **First planned action:** governance request PHASE_OPEN_D08 v1 (reopening rules, leaderboard isolation under 5 uploads a day, holdout, fold reuse, refreeze); review X-D08-S01-0001. No hypothesis is proposed before that review is acknowledged.
