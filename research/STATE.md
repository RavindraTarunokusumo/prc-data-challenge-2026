# Research State

*Updated 2026-09-30T07:05:02Z (measured with `date -u` at writing; D03-S01 closing, Day 3 CLOSED).*

- **Phase:** **Day 3 CLOSED** (X-D03-S01-0003: ACCEPT, 0.82). Day 4 (historical priors and interactions) is next, on branch `day-4`. Splits, metric and availability definition are **FROZEN** (`config/frozen.json`).
- **Last session:** D03-S01 (ended at this commit). **Last completed exchange:** X-D03-S01-0003 (phase close). **Pending:** none.
- **Champion: E019, H015 v2, since the Day 3 phase close.**
  - It is a routed LightGBM on FS2: congestion on top of FS1, with deterministic training. LIRF NM-missing rows are routed to a fold-local E005 ridge.
  - Development mean 444.49 (R1 446.40, R2 274.49, R3 397.25, S1 632.10, W1 472.22). −38.23 s against E005, with a WIN on all 7 folds.
  - **Holdout H (Dec 2025): WIN,** 375.93 against E005's 411.29 (−35.36 s). Recorded only (ruling H3).
  - Reproduced byte-for-byte by E022 (criterion 6).
  - **Standing disclosures on the champion (D3-C1 to D3-C3):**
    - **D3-C1.** 95 % of the margin over E005 is routed FS1 structure (rE017 − E005 −36.33 s). Congestion as served (E019 − rE017, all rows) is −1.90 s, with R1 and R2 TIE and EHAM +7.2 % (criterion 3 fails on that contrast). The mechanism figure C = −6.75 s is on `NM_present_excl_LIRF` only.
    - **D3-C2.** Out-of-range predictions on NM-missing rows at the nine non-LIRF airports (below 0 s, or above 3,600 s on normal taxis). E019 loses to E005 in bulk there on 4 development folds. Cause: the LightGBM trains on the LIRF convention rows, and SCHED-anchored T windows carry that pattern to non-routed rows.
    - **D3-C3.** January 2026 has 435 NM-missing rows with `d_sched` > 3 h and 92 > 5 h, against a 2025 monthly maximum of 222 and 36. Expected cost about 0–5 s of January margin, heavy-tailed. H does not test it.
- **Previous champion:** E005 (H004 ridge on FS0), development mean 482.73. Day 1 holdout: WIN.
- **Day 3 results:**
  - **H015 v2 PROMOTE** (E019; E022 reproduction).
  - **H016 v2** (E020, R ablation): development mean 321.95. −56.87 s against E017 on all rows, via the convention channel. Criterion 8 S1 +4,292, inside the bound. Not a candidate.
  - **H017 v2** (E021, P/T): P −3.47 s, T given P −3.28 s on `NM_present_excl_LIRF`. Both are below the −6.0 s floor, and they add to C = −6.75 s.
  - **Deterministic LightGBM is deterministic on real data:** identical across processes, a container restart, two CPU model strings and a seed change.
- **Routing answer (X-D03-S01-0003 (e)).** An unrouted Day 4 candidate is admissible if:
  - it is a new configuration (rule 10);
  - it pre-registers its convention exposure under rule 8, with the S1 expectation at July's rate;
  - it keeps H009 v3's criterion 8 rule unchanged;
  - it pre-registers any forward-risk rationale citing the break-even figures (S1 0.058 against 2025's lowest 0.35) and the 2026 counts (107 and 276 rows).
- **Holdout:** Day 1 used (WIN); Day 2 0 of 1 (closed unused, ruling H); **Day 3 1 of 1 used (WIN, E019 vs E005).** E012–E018, E020, E021 and E022 may never be NEW (rule 9).
- **Day 2 decisions:**
  - **H009 v3 INCONCLUSIVE:** E012, development mean 376.15; E015 reproduction failed criterion 6 (R3 1.73 s, S1 3.50 s).
  - **H013 v2 INCONCLUSIVE:** E017, 378.82; criterion 8 not resolved (S1 +7,104 > +6,500); not reproduced.
  - **Ablations and references:**
    - E013 (H010): M3 supported.
    - E014 (H012): M2 supported, −51.3 s on NM-present rows.
    - E016 (H011 v2): static keys without deltas, −29.6 s on NM-present rows and −28.0 s on all rows.
    - E018 (H014 v2): M1 replicated.
- **Day 2 headline** (rule 11: restricted next to all rows):
  - Static FS1 keys on top of the delta set: **−9.1 s** on NM-present rows (bagged), but **−1.72 s (q95 +9.39) on all rows**. FS1 is not distinguishable from FS0 on the metric.
  - Deterministic training: −0.75 s on NM-present rows against **+2.67 s on all rows**. Its real-data determinism is now confirmed (Day 3, finding 3).
- **Earlier:** Day 1 accepted H002, H003 and H004; rejected H005 and H007; H006 INCONCLUSIVE.
- **Standing Advisor rules:**
  1. tail attribution;
  2. forward exposure;
  3. holdout only via phase close;
  4. calendar-month identity;
  5. all folds + H;
  6. row concentration;
  7. NM × LIRF subgroup disclosure;
  8. recording-convention disclosure;
  9. holdout access named by the phase-close review; NEW allocated in that phase; an unused access does not carry over;
  10. no re-adjudication (no unchanged re-submission of E006/E012/E015/E017/E018 configurations as candidates; no post-hoc threshold, population or counting changes, including any criterion 8 threshold);
  11. headline figures: restricted next to all rows, one population per comparison, all development folds when localising;
  12. out-of-range predictions and forward support (X-D03-S01-0003): report counts below 0 s and above 3,600 s on bulk rows by fold and rule 7 subgroup; with schedule-delay-driven inputs, report ranking-month NM-missing counts with `d_sched` > 3 h and > 5 h against the 2025 range. Disclosure only.

  Batch conditions B1–B4 are carried.
- **Rulings (X-D02-S01-0006; H3 from X-D03-S01-0003):**
  - **H:** Day 2 holdout closed unused.
  - **B:** the +6,500 s criterion 8 bound is not re-derived. An alternative resolution needs a forward-risk rationale that does not rest on E006–E018.
  - **R:** a comparison base is a matched reference sharing the candidate's training procedure. Criterion 4 carries every mechanism claim.
  - **H3:** Day 3 holdout access E019 vs E005 (done: WIN). The H figures are recorded only and inform nothing.
- **Known leakage hazards:**
  - P/T/F labels. `MVT − AOBT_3` and `d_sched` are T.
  - The hour-resolution schedule-delay proxy is T.
  - `ades` is F on diversions (~0.03 % of rows).
  - Cross-month information is inadmissible.
- **Key data facts:**
  - NM-missing rows are 0.8–2.1 % of each fold and carry 14–66 % of the SSE; there are 20,821 in Jan–Nov.
  - LIRF: 83 % of tail rows are block-at-schedule, and 931 of 932 NM-present ones have a normal anchor.
  - Every fold except W1c trains on more than 200,000 rows, the LightGBM bin-sample threshold.
- **Open incidents:** **INC-0004** (launch arguments against session metadata). From about 05:35Z on 30 September, after the second container restart, the process carries `--model claude-opus-5-5 --effort medium` (D3-C5); the metadata says `high`. Open, non-blocking, owner to decide. INC-0003 closed.
- **Open blockers:** none.
- **Next action:** Day 4 session start (D04-S01) on branch `day-4` from `main` after the Day 3 PR merges. Day 4 is historical priors and interactions (brief §11). Candidate questions (DAY_SUMMARY §8):
  1. the out-of-range predictions on non-LIRF NM-missing rows (D3-C2), treated as its own hypothesis with an isolating ablation;
  2. fold-local target statistics and interactions, with CatBoost;
  3. optionally an unrouted candidate under the routing answer's conditions.
  Rule 12 applies from the next proposal. Then the Day 4 hand-off package (brief §3: `HANDOFF_D04.md`).
