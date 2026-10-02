# Acknowledgement — H026 v2 (exchange X-D06-S01-0002)

- proposal: `research/day-06/proposals/H026_v2.md`, sha256 `a4a9ae5000626b1eb92b110ddb4a0f6d3813729b012b8a89352cf78ebc5d6bbc`
- review: `research/day-06/advisor/H026_review_v2.md`, sha256 `939ed3c2b72b52f970b08097648fb5c569fe3dcbfe6f979b50291e72b9b6cd40`
- decision received: **ACCEPT**. Both hashes verified by the researcher at 2026-10-02T18:13Z.

The researcher adopts the review's Execution Authorization as written, including the batch conditions **C1–C7** in `research/day-06/advisor/H024_review_v2.md`:
- C1: allocation order H026 → E035, H024 → E036, H025 → E037, H027 → E038, H028 → E039, all `primary`; each `gate.json` and `config.yaml` checked against its proposal before arming; no arming on any mismatch. **This proposal maps to E035.**
- C2: no re-attempt or `rerun`; a blend whose component did not end COMPLETE and route-checked is recorded "not run (component E### <status>)"; a refusal before RUNNING counts as deferred.
- C3: a deferred run goes at the owner's next window by a direct `run_experiment.py` call or a new launcher recorded by hash beforehand; the pinned launcher is never edited.
- C4: diagnostic code outside `src/` and `scripts/` while the freeze holds, committed with its output, cited by hash, run after the window, memory-light.
- C5: bounded wording of every "carries" reading (and the measurable-part sentence when any fold is LOSS); no threshold, population or count changes.
- C6: the closed-set comparison covers every resolved key; a key in one arm only is a violation (H024 and H025).
- C7: runs past 21:30 reported as INC-0012 deviations with end times; the launcher log copied into the session record; freeze diff (launcher included) in each analysis.

The binding ruling of X-D06-S01-0001 stands: E035–E039 are never NEW in any phase; rule 10 covers their configurations; any Day 7 use is a new configuration that states the selection. The non-blocking notes are adopted for the records (74.7 % in place of "more than 75 %"; rung A's floor recorded "at seed 42").

**Attestation (H026 v2; review condition C7; Scientific Validity (c) of `H026_review_v1.md`).** The researcher attests that no E029 + E030 blend prediction, blend RMSE, ambiguity term or E029–E030 residual-correlation figure was computed, in any form, before this acknowledgement. The only E029/E030 figures seen are those already in the repository (`research/comparisons/E030_vs_E029.json` and the Day 5 records).
