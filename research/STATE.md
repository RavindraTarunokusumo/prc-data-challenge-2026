# Research State

*Updated 2026-09-29T16:32:41Z (measured with `date -u` at writing; D03-S01, Day 3 in progress).*

- **Phase:** **Day 3 in progress** (congestion reconstruction), session D03-S01, branch `day-3` (PR #5). Day 2 CLOSED (X-D02-S01-0006: ACCEPT). Splits, metric and availability definition are **FROZEN** (`config/frozen.json`).
- **Last session:** D03-S01 (open). **Last completed exchange:** X-D03-S01-0002 (H015 v2, H016 v2, H017 v2: all ACCEPT). **Pending:** none; next is the H015 v2 chain.
- **Day 3 exchanges:**
  - X-D03-S01-0001 (attempt 2 after a container restart): H015 v1, H016 v1 and H017 v1 all **REVISE**. The blocking defects were false LIRF NM-missing forward-risk figures, and row 192622644 able to decide the C clause on S1.
  - Commit `63923e2`: the five P counts that included the row itself now remove its own contribution exactly (no P feature depends on the row's own takeoff). Masking invariance was re-verified on 1,919,370 rows (`scripts/check_fs2_v2.py`).
  - X-D03-S01-0002: H015 v2 (0.85), H016 v2 (0.88) and H017 v2 (0.85) all **ACCEPT**. The C clauses are on `NM_present_excl_LIRF`. Code is frozen under `src/`, `scripts/`, `pyproject.toml` and `uv.lock` from the H015 allocation to the chain's last comparison.
  - Advisor's pre-run forecast: clause 1 passes (0.93); C probably −3 to −5 s, above the −6.0 s floor; P(H015 promotable) 0.20.
- **Day 3 so far (no experiment yet):** congestion block `prc.congestion` (10 P + 5 T features; FS2, FS2_P), verified bit-identical under DEP block/target masking on real data; EDA `research/day-03/eda/congestion.json`; routed Tier 2 model `models/routed.py` (LIRF NM-missing rows → fold-local E005 ridge; byte-identical to E005 on W1c and R2); `scripts/route_check.py`.
- **Champion: E005, H004 ridge on FS0, by rule. It is not the most accurate model.**
  - Development mean 482.73 (R1 477.8, R2 323.5, R3 431.6, S1 670.0, W1 510.7). Day 1 holdout: WIN.
  - **Deficit.** On NM-present rows, every Day 2 Tier 1 fit beats E005 by 51.5–59.6 s on every development fold.
  - On all rows the margin is −60.9 to −131.9 s. On S1 and S1c it rests on a few LIRF convention rows (DAY_SUMMARY §5).
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
  - Deterministic training: −0.75 s on NM-present rows against **+2.67 s on all rows**. Its real-data determinism is untested.
- **Earlier:** Day 1 accepted H002, H003 and H004; rejected H005 and H007; H006 INCONCLUSIVE.
- **Holdout:** Day 1 used (WIN). **Day 2: 0 of 1, closed unused** (ruling H). E012–E018 may never be NEW in a holdout access (rule 9).
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
  11. headline figures: restricted next to all rows, one population per comparison, all development folds when localising.

  Batch conditions B1–B4 are carried.
- **Rulings (X-D02-S01-0006):**
  - **H:** Day 2 holdout closed unused.
  - **B:** the +6,500 s criterion 8 bound is not re-derived. An alternative resolution needs a forward-risk rationale that does not rest on E006–E018.
  - **R:** a comparison base is a matched reference sharing the candidate's training procedure. Criterion 4 carries every mechanism claim.
- **Known leakage hazards:**
  - P/T/F labels. `MVT − AOBT_3` and `d_sched` are T.
  - The hour-resolution schedule-delay proxy is T.
  - `ades` is F on diversions (~0.03 % of rows).
  - Cross-month information is inadmissible.
- **Key data facts:**
  - NM-missing rows are 0.8–2.1 % of each fold and carry 14–66 % of the SSE; there are 20,821 in Jan–Nov.
  - LIRF: 83 % of tail rows are block-at-schedule, and 931 of 932 NM-present ones have a normal anchor.
  - Every fold except W1c trains on more than 200,000 rows, the LightGBM bin-sample threshold.
- **Open incidents:** **INC-0004** (D03 launch arguments `--model claude-sonnet-5-5 --effort medium` against session metadata: served `claude-opus-5-5`, effort `high`). Open, non-blocking, owner to decide. INC-0003 closed.
- **Open blockers:** none.
- **Holdout:** Day 3: 0 of 1 used.
- **Next action:** `gate.py allocate H015 v2`, then the H015 primary run and chain step 1. After that, H016 v2 (chain step 2: `route_check.py`), then H017 v2. Reproduce H015 only under clause conditions. Checkpoint after each experiment.