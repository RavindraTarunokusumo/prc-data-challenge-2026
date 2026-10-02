# Research State

## Day 5 in progress (owner laptop; updated 2026-10-02T12:46Z, D05-S05)

- **Sessions:** D05-S01 to D05-S04, on branch `day-5`. Laptop: WSL2 11 GB, swap 0, RTX 5060 8 GB. INC-0007 is closed. Delegation is allowed under INC-0006 (open).
- **E025** (H015 v2 reproduction): RESOURCE_FAILURE, a global OOM from a concurrent researcher pytest (INC-0008, closed; experiment lock added).
- **E026** (H015 v2 reproduction): **PASS**. All development folds are within 0.008 s of E019, in 669 s at 5.22 GB. **The prediction files are not byte-identical to E019's** (AMD against Intel).
- **Blocker for Day 5 comparisons:** E019's, E005's and E023's prediction files are not on the laptop, so row-level comparisons against them cannot run. This needs an Advisor ruling in the first Day 5 exchange.
- **Champion: E019, unchanged.** Day 5 holdout: 1 of 1 available. Last completed exchange: X-D04-S02-0001.
- **Done since:**
  - GPU calibration (`research/day-05/eda/gpu_calibration.json`). CatBoost on GPU is 0.16–0.20 s per iteration with full CTR combinations, and not deterministic. XGBoost on GPU is slower than CPU LightGBM.
  - W&B mirror (INC-0009) with learning curves (E027 on). The owner's early-stopping suggestion was logged, not adopted (D05-S04 session record).
  - Laptop instances: **E027** (E019, curves), **E028** (E005), **E029** (E023). All pass `reproduce_check`; none is byte-identical.
- **X-D05-S04-0001: REVISE ×4** (LAPTOP_REFS, H021, H022, H023). Corrections D5-C1 to D5-C7 are in `research/day-05/acks/`. **The "swap 0" statements above are wrong** (D5-C1: 4 GiB swap since 16:33Z, unused). **The interpreter is CPython 3.13.15, not 3.11** (D5-C2). Owner decisions: keep both (INC-0010, open).
- **X-D05-S04-0002:** LAPTOP_REFS v2 **ACCEPT** (0.88); H021–H023 v2 REVISE.
  - **Rule L v2 adopted:**
    - E026 is E019's instance and E029 is E023's;
    - E028 is E005's instance in a reduced role;
    - E027 is cited for curves only;
    - E029's routed rows are the route-integrity reference.
  - **Ratified:** E027, E028, E029.
  - **Cause of the laptop differences:** polars' thread pool (16 here, 4 on the cloud) changes the ridge's fitted statistics in the last bits. `sparse_cg` amplifies that on routed rows.
  - The environment is bound to CPython 3.13.15, lock `efa4fd78…` and the default polars threads.
- **X-D05-S04-0003: H021 v3, H022 v3, H023 v3 ACCEPT** (0.88, 0.90, 0.88).
  - Tools-freeze anchor `803ceeb`.
  - Chain: H022 (CLASS-M), then H021 (CLASS-L, GPU), then H021r (unconditional), then H023 (blend, gated on status only), then H023r if due.
  - Advisor forecast: H023 promotion P 0.04.
- **E030 (H022 v3, codes control):** 446.50; integrity holds.
- **E031 (H021 v3, CTRs): 440.76, the best single run so far** (−1.69 s against E029 on all rows; S1 WIN). Not a candidate by pre-registration. Clause 1 is provisionally not met (−4.91 s); the noise condition needs H021r.
- Paused after E031 by the owner (INC-0011), and resumed on 2026-10-02 (D05-S05; INC-0011 closed).
- **E032 (H021r):** 440.91. The noise condition holds (m = +0.68 s), so **H021 clause 1 is final: NOT MET** (the categorical statistics carry signal, −4.91 s). Its own 1.0 s reproduction tolerance fails on R1 (+1.056 s); H021 is not a candidate.
- **E033 (H023 v3, blend 0.5 E029 + 0.5 E031): development mean 438.87.** Against E019 (instance E026): **−5.62 s, WIN on all 7 folds incl. S1, criteria 1–8 MET.** E034 (reproduction) passes criterion 6. **PROMOTE recommended**; the champion change is recorded at the Day 5 phase close, with the Day 5 holdout access (H023 as NEW, a Day 5 allocation; reference E026).
- **The authorized chain is complete.** Next: the Day 5 phase close. Next experiment id: E035.

*The Day 4 close state below is unchanged.*

*Updated 2026-10-01T01:58:22Z (measured with `date -u` at writing; D04-S02, at the Day 4 phase close).*

- **Phase:** **Day 4 CLOSED** (historical priors and interactions). Phase close X-D04-S02-0001: **ACCEPT** (0.85), with no promotion and no holdout access. Splits, metric and availability definition are **FROZEN** (`config/frozen.json`). **Days 1–4 (cloud scope) are complete.**
- **Sessions:** D04-S01 (ended at a container reset) and D04-S02 (ended at the phase close). **Last completed exchange:** X-D04-S02-0001. **Pending:** none.
- **Next action:** **Day 5 on the owner's laptop, starting from `docs/reproducibility/HANDOFF_D04.md`.** Day 5 opens a new branch `day-5` from `main` after PR #6 merges, and E019 is its phase-opening champion.
- **Day 4 decisions (X-D04-S02-0001 item 1):**
  - **H018 v2 (E023): mechanism supported; "D3-C2 treated, not promoted"** (criterion 2: S1 TIE against E019). Ledger: REJECT. Excluding the routed LIRF NM-missing rows from LightGBM training cuts the > 3 h out-of-range band from 81 to 5. All rows −2.04 s against E019; development mean 442.46.
  - **H019 v2 (E024): mechanism falsified; not promoted** (criterion 2; criterion 4 under B2). Ledger: REJECT. The FS3 prior block gives −0.29 s on `NM_present_excl_LIRF` (q95 +0.12; floor −3.0) and −0.40 s on all rows (q95 −0.03): real, but a tenth of the floor (D4-C7). Development mean 442.06.
  - **H020 v1 (CatBoost): REJECT, closed.** No run. Handed to Day 5 with the review's objections.
- **Hand-off base ruling (X-D04-S02-0001 (e)):**
  - Under ruling R, E023 is the matched reference for candidates that keep `route_train_exclude: true` on FS2, and E024 for FS3.
  - Neither is a default base or a de facto champion.
  - Such candidates are judged against E019, and their criterion 4 includes H018 v2's clauses 1–2.
  - Rule 10 covers the configurations of E020, E021, E023 and E024, including backend-only or build-only variants unless they pre-register a mechanism for the difference.
- **Open incidents:** **INC-0004** (launch `--effort medium` against metadata `high`): open, non-blocking, owner to decide. **INC-0005** (Sonnet delegation): **closed** at the Day 4 phase close; delegation on Days 5–7 needs a new incident. INC-0003 closed.
- **Corrections in Day 4:**
  - D4-C1 to D4-C6 (acks of X-D04-S01-0001 and -0002);
  - D4-C7 to D4-C16 (`research/day-04/acks/PHASE_CLOSE_D04_ack_v1.md`).
- **Champion: E019, H015 v2, since the Day 3 phase close. It holds through Day 4 by rule** (X-D04-S02-0001).
  - It is a routed LightGBM on FS2: congestion on top of FS1, with deterministic training. LIRF NM-missing rows are routed to a fold-local E005 ridge.
  - Development mean 444.49 (R1 446.40, R2 274.49, R3 397.25, S1 632.10, W1 472.22). −38.23 s against E005, with a WIN on all 7 folds.
  - **Holdout H (Dec 2025): WIN,** 375.93 against E005's 411.29 (−35.36 s). Recorded only (ruling H3).
  - Reproduced byte-for-byte by E022 (criterion 6).
  - **Standing disclosures on the champion (D3-C1 to D3-C3):**
    - **D3-C1.** 95 % of the margin over E005 is routed FS1 structure (rE017 − E005 −36.33 s). Congestion as served (E019 − rE017, all rows) is −1.90 s, with R1 and R2 TIE and EHAM +7.2 % (criterion 3 fails on that contrast). The mechanism figure C = −6.75 s is on `NM_present_excl_LIRF` only.
    - **D3-C2.** Out-of-range predictions on NM-missing rows at the nine non-LIRF airports (below 0 s, or above 3,600 s on normal taxis). E019 loses to E005 in bulk there on 4 development folds. Cause: the LightGBM trains on the LIRF convention rows, and SCHED-anchored T windows carry that pattern to non-routed rows.
    - **D3-C3.** January 2026 has 435 NM-missing rows with `d_sched` > 3 h and 92 > 5 h, against a 2025 monthly maximum of 222 and 36. Expected cost about 0–5 s of January margin, heavy-tailed. H does not test it.
    - **D3-C2 cause confirmed** by E023's exact ablation (Day 4).
    - **D4-C9.** S1 against E019 is decided by one row.
      - Row 192622644 (LIRF, NM-present, y 87,002 s) carries 8.2 % of E019's S1 SSE. E019 predicts 8,136 s there, the FS2 family's highest.
      - Without that row (audit only, rule 10), E023 meets criteria 1–3 against E019.
      - E023's W1 WIN is likewise carried by row 183910286.
      - Day 5–7 candidates whose promotion needs S1 or W1 pre-register their direction on these rows under rule 8 (Missing Control 1).
    - **The submitted model carries D3-C2 and D3-C3 unless a later candidate is promoted.**
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
- **Holdout:**
  - Day 1: used (WIN).
  - Day 2: 0 of 1 (closed unused, ruling H).
  - Day 3: 1 of 1 used (WIN, E019 vs E005).
  - **Day 4: 0 of 1, closed unused (ruling H4; not a TIE).**
  - Day 5 has one access, which needs a Day 5 allocation as NEW.
  - E012–E018 and E020–E024 may never be NEW (rule 9). **No `holdout_check.py` invocation with E023 or E024 as NEW is authorized, in any phase.**
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
- **Rulings (X-D02-S01-0006; H3 from X-D03-S01-0003; H4 from X-D04-S02-0001):**
  - **H:** Day 2 holdout closed unused.
  - **B:** the +6,500 s criterion 8 bound is not re-derived. An alternative resolution needs a forward-risk rationale that does not rest on E006–E018.
  - **R:** a comparison base is a matched reference sharing the candidate's training procedure. Criterion 4 carries every mechanism claim.
  - **H3:** Day 3 holdout access E019 vs E005 (done: WIN). The H figures are recorded only and inform nothing.
  - **H4:** Day 4 holdout closed unused. No substitute comparison, and no carry-over.
- **Known leakage hazards:**
  - P/T/F labels. `MVT − AOBT_3` and `d_sched` are T.
  - The hour-resolution schedule-delay proxy is T.
  - `ades` is F on diversions (~0.03 % of rows).
  - Cross-month information is inadmissible.
- **Key data facts:**
  - NM-missing rows are 0.8–2.1 % of each fold and carry 14–66 % of the SSE; there are 20,821 in Jan–Nov.
  - LIRF: 83 % of tail rows are block-at-schedule, and 931 of 932 NM-present ones have a normal anchor.
  - Every fold except W1c trains on more than 200,000 rows, the LightGBM bin-sample threshold.
- **Open blockers:** none.
