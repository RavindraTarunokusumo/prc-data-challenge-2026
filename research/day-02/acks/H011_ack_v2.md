# Acknowledgement — H011 v2 (exchange X-D02-S01-0002)

- proposal: `research/day-02/proposals/H011_v2.md`, sha256 `a39d91bad0b4ddb3b88fe101fe70904f4800bf1f06e177724830b8c04adc42b0`
- review: `research/day-02/advisor/H011_review_v2.md`, sha256 `bf7bf927894d1fbb0a8992cc13195df81e062369ca03527ab022cc7a1d002c17`
- decision received: **ACCEPT** (confidence 0.80), conditional. Both hashes verified by the researcher.

**Adopted preconditions.** All of these must hold before `gate.py allocate H011 v2`:
- (a) An H009 version ≥ 3 has decision ACCEPT, and its acknowledgement is committed.
- (b) The primary runs that the accepted H009 version's chain places before H011 are COMPLETE (in the v2 chain: H009, H010 and H012).
- (c) No other experiment runs concurrently.
- (d) The E010 reuse conditions hold at allocation:
  - `uv.lock` is `39df945c…`;
  - `gbm.py` and the FS0 path are unchanged;
  - silver is pinned.

  H011's `gate.json` `uv_lock_sha256` is recorded in the analysis.

**Lapse rule adopted.** If the output of `fs1_static_no_deltas` changes (through `fs1`, `fs0` or `collapse_rare`), or (d) fails, this ACCEPT lapses and `H011_v3` is required.

**Residual exposures recorded (not a change of claim).** Inside the falsification population `excl_LIRF_NM_missing`, against E010:

| Subgroup | Share of E010's SSE in that population | ±15 % of that subgroup's SSE moves the fold by |
|---|---|---|
| LIRF NM-present tail | 2.0–10.2 % (R1–R3, W1, W1c); 30.4 % on S1 and 29.7 % on S1c, of which row 192622644 alone is 20.1 % | ±0.6 to ±2.5 s; S1 ±10 s |
| NM-missing rows at the other nine airports | 2.9–4.7 % (R1–R3, S1); 15.6 % on W1 and 14.4 % on W1c | ±0.7 to ±1.9 s; W1 ±5 s |

- Row 192622644 is not a decider here, because neither model has the anchor or `d_sched`.
- The residual route to the schedule delay (operator × destination × takeoff hour) is coarse: it pins the scheduled hour for about 37 % of rows.
