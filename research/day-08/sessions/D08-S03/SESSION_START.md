# D08-S03 session start

*Written 2026-10-06 (measured 2026-10-06T18:57:28Z with `date -u`).*

- **Why:** the owner's instruction (2026-10-06): "Yes, fix the merge and open the day-8 session". This is the first Day 8–12 session on the owner's laptop. The project is OPEN since the `reopened` event (2026-10-05T14:15:05Z).
- **Where:** the owner's laptop, WSL2 (boot `cf2c705b…`), 16 threads, 10 GiB RAM + 4 GiB swap, RTX 5060 Laptop 8 GB.
  - **Rule L v2 item 6 holds:** CPython 3.13.15, `uv.lock` `efa4fd78…`.
- **Git:** branch `day-8`, at `4337a6b` (`main` `35d9bda` + the merge of `origin/day-7`). The tree was clean.
- **The merge (INC-0020).**
  - `origin/day-7`'s three post-freeze commits had never reached `main`: D7-C15, `LICENSE` (GPLv3), the upload record, INC-0017 (D7), INC-0018 (D7) and `HANDOFF_D07.md`. They are now merged into `day-8` unchanged.
  - The two conflicting files keep both versions: `UPLOAD_RECORD.md` holds both records with a merge note, and the session registry keeps lines in time order.
  - INC-0020 records the duplicate IDs (INC-0017/0018 used by both lineages; labels "(D7)") and the contradicting records. **Leaderboard isolation did not hold at the reopening:** a leaderboard figure had been disclosed to the researcher on 2026-10-04. It is not used (G2).
- **State recovered** from `research/STATE.md` (Phase: OPEN, Days 8–12), the Day 8 ack and review (X-D08-S01-0001), INC-0017, INC-0019, `HANDOFF_D07.md`, and the ledger and registry tails.
  - **Champion: E046** (H035 v1). Development mean 314.42 s. H (December 2025) is closed for Days 8–12 (ruling H8).
  - **Submission v1:** E050's file, `genuine-cabbage_v1.parquet`, SHA-256 `f0dc2c7c…`. At most one new upload (G7), before 2026-10-11T12:00:00Z.
  - **Binding:** G2–G12, ruling H8, rule 15 (G5), rules 1–14, B1–B4, rule L v2.
- **Accepted findings:** as in STATE (Days 1–7). **Rejected:** none new.
- **Budget:** H: none (H8). Uploads: one (G7). Experiments: next ID **E051**. `gate.py status`: 50 allocated; advisor definition `30fff5dd3c54` OK; frozen `32c41c0f9331` OK.
- **Open incidents:** INC-0004, INC-0009, INC-0010, INC-0017, INC-0018, INC-0018 (D7), INC-0019, **INC-0020** (new).
- **Resolved model IDs:** researcher `claude-opus-5-5`; Advisor: `advisor` subagent, definition `30fff5dd3c54`.
- **Last exchange:** X-D08-S01-0001.
- **Open questions (the agenda, non-binding):** recording conventions in the tail beyond LIRF; the routed LIRF subgroup (a convention-mixture model); LTFM winter with weather; the CatBoost iteration budget.
- **First planned action:**
  1. Target-free data analysis for the LIRF NM-missing subgroup and for the tail outside LIRF. Its footprint is stated under rule 15 (c).
  2. The batch-1 proposal(s). The first envelope cites INC-0020, so the Advisor is told of the exposure before any allocation.
