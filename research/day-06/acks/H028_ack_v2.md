# Acknowledgement — H028 v2 (exchange X-D06-S01-0002)

- proposal: `research/day-06/proposals/H028_v2.md`, sha256 `65b8f3fbc816a7bde428c7f39a8c40525dfb1ea4c9595b56444e14d4567d70a2`
- review: `research/day-06/advisor/H028_review_v2.md`, sha256 `8f6aa94cf127b98350c85dc246639df7f0370ac8c36e3a7fe1908dec9e647433`
- decision received: **ACCEPT**. Both hashes verified by the researcher at 2026-10-02T18:13Z.

The researcher adopts the review's Execution Authorization as written, including the batch conditions **C1–C7** in `research/day-06/advisor/H024_review_v2.md`:
- C1: allocation order H026 → E035, H024 → E036, H025 → E037, H027 → E038, H028 → E039, all `primary`; each `gate.json` and `config.yaml` checked against its proposal before arming; no arming on any mismatch. **This proposal maps to E039.**
- C2: no re-attempt or `rerun`; a blend whose component did not end COMPLETE and route-checked is recorded "not run (component E### <status>)"; a refusal before RUNNING counts as deferred.
- C3: a deferred run goes at the owner's next window by a direct `run_experiment.py` call or a new launcher recorded by hash beforehand; the pinned launcher is never edited.
- C4: diagnostic code outside `src/` and `scripts/` while the freeze holds, committed with its output, cited by hash, run after the window, memory-light.
- C5: bounded wording of every "carries" reading (and the measurable-part sentence when any fold is LOSS); no threshold, population or count changes.
- C6: the closed-set comparison covers every resolved key; a key in one arm only is a violation (H024 and H025).
- C7: runs past 21:30 reported as INC-0012 deviations with end times; the launcher log copied into the session record; freeze diff (launcher included) in each analysis.

The binding ruling of X-D06-S01-0001 stands: E035–E039 are never NEW in any phase; rule 10 covers their configurations; any Day 7 use is a new configuration that states the selection. The non-blocking notes are adopted for the records (74.7 % in place of "more than 75 %"; rung A's floor recorded "at seed 42").
