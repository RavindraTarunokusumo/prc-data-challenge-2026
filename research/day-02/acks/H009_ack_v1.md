# Acknowledgement — H009 v1 (exchange X-D02-S01-0001)

- proposal: `research/day-02/proposals/H009_v1.md`, sha256 `c5927ce1c589a0b85c50331ab11e3396ca6e552c2c72cb7dc1e219349af2242d`
- review: `research/day-02/advisor/H009_review_v1.md`, sha256 `de8fa7b64b5e9427878d79403c9c00f0b6c1b374b7cd8d5d205fd22ffcb71de8`
- decision received: **REVISE** (confidence 0.85). Both hashes verified by the researcher.

This acknowledgement confers **no authority**. `gate.py allocate H009 v1` will not be run, and no FS1-family run (H009, H010, H011) is allocated before an H009 version ≥ 2 is ACCEPTED and acknowledged.

The researcher accepts all six required revisions and will submit `H009_v2.md` in a new exchange:
1. **M1** gets a test that the LIRF NM-missing subgroup cannot decide. Clause 2(b) is kept.
2. **M2** is re-specified with `d_sched` held fixed, on a stated population.
3. **M3** states the hour-resolution schedule-delay proxy and the lower-bound reading, and corrects Alternative Explanation 2.
4. **Code:** every pre-registered quantity will be computable by committed code before the first run, including the producing code of EDA finding 5 and of the FS1 build check.
5. **Evidence corrections (a)–(f).**
6. **The reproduction is conditional** on criteria 1–3 passing against E005 without falsification.

Acknowledged rulings:
- Reusing E006 and E010 as ablation references is permitted. It lapses if `uv.lock`, the model code, `fs0` or silver change before H009 runs. E006 and E010 ran from a dirty working tree (`git_dirty_at_run`), and that is recorded here.
- `research/STATE.md` is refreshed before the first Day 2 allocation.
