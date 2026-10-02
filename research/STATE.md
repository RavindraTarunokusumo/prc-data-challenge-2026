# Research State

*Updated 2026-10-02T19:35:34Z (measured with `date -u` at writing; D06-S01, after the Day 6 ladder batch).*

- **Phase:** **Day 6 OPEN** (adversarial science day), branch `day-6`, session D06-S01.
  - Splits, metric and availability definition are FROZEN (`config/frozen.json`).
  - Days 1–5 are complete.
- **Last completed exchange:** X-D06-S01-0002 (H024–H028 v2 ACCEPT, conditions C1–C7). **Pending:** none.
- **Day 6 so far:** the attribution ladder (E035–E039, controls, all COMPLETE inside the owner's window). Readings: rung B (codes CatBoost) and rung C (per-key CatBoost) "carry part"; rung A (LightGBM twin) does not reproduce the gain (averaging floor −1.53 s at seed 42); H024's own reading INCONCLUSIVE (closed set: `data_partition`). See the journal's Day 6 section and `experiments/E035…E039/analysis.md`.
- **Never NEW, in any phase (added):** E035–E039 (X-D06-S01-0001 ruling); rule 10 covers their configurations; any Day 7 use states the selection.
- **Owner instructions:** INC-0012 (runs only 21:00–21:30 local), INC-0013 (Sonnet delegation of coding permitted; used once: `research/day-06/eda/d06_diagnostics.py`).
- **Next action:** further Day 6 work or the Day 6 phase close (one holdout access available, named by the phase close). **E033 remains champion.** Next experiment id: E040.

## Champion: E033 (H023 v3), since the Day 5 phase close

- **What it is:** a fixed 0.5/0.5 blend (`prc.blending`) of two routed models:
  - **E029:** routed LightGBM on FS2 with `route_train_exclude` (H018 v2's configuration; E023's laptop instance);
  - **E031:** routed CatBoost on GPU, FS2_RAW, CTRs Borders/FeatureFreq/FloatTargetMeanValue at complexity 4, depth 8, 1,000 iterations, learning rate 0.08 (H021 v3).

  The LIRF NM-missing rows are routed to the fold-local E005-class ridge in both halves.
- **Development mean 438.87 s:** R1 439.89, R2 264.88, R3 393.04, S1 627.92, W1 468.63; S1c 631.99, W1c 481.77.
- **Against E019 (laptop instance E026): −5.62 s (q95 −4.79), WIN on all 7 folds incl. S1;** every airport improves. Criteria 1–8 met. Reproduced by E034 (within 0.48 s; a GPU re-draw, not byte-identical).
- **Holdout H (Dec 2025): WIN,** 369.18 s against E026's 375.93 s (−6.75 s; q10/q90 −9.83/−4.88). Recorded only (ruling H5).
  - Instance check: E026's H RMSE is 375.92735 s, against E019's recorded 375.92721 s.
- **Pointer:** `models/champion/CURRENT.json`, with history.
- **Standing disclosures on the champion:**
  - **D3-C1 (lineage).** Most of the Day 3 champion's margin over E005 was routed FS1 structure.
  - **D3-C3 restated (D5-C16).**
    - January 2026 has 435 non-LIRF NM-missing rows with `d_sched` > 3 h and 92 > 5 h, 2.0–2.6 times the 2025 maximum. H does not test it.
    - E033's development out-of-range share in the > 3 h band is 0.57 %, against E019's 15.3 %.
  - **D5-C8 (composition).** Of the −5.62 s margin, −2.04 s is E029's D3-C2 treatment (E023's Day 4 margin) and −3.58 s is the CatBoost half. S1's WIN is entirely the CatBoost half (+0.20 s, then −4.38 s).
  - **D5-C9 (stochastic champion).**
    - The figures are one draw. The blend's re-draw is at most 0.48 s per development fold, with an RMS prediction change of 15–23 s (37 s on W1c).
    - Clause 1's W1 reading moved from WIN to TIE.
    - **SUBMIT predictions will be a further draw.**
  - **D5-C10 (single rows).**
    - S1 is −3.76 s without row 192622644; the blend predicts 9,008 s there (y 87,002).
    - W1 is −2.56 s without row 183910286 (blend 15,086 s; y 13,865), and that row's W1 prediction rests on post-validation months.
  - **The 1,000-iteration budget.** CatBoost was still improving at 1,000 (−0.73 s over iterations 800–1,000). A change of iterations is a new configuration.
  - **Retired:** D3-C2 is treated (> 3 h band 3 against 81) and kept as history. D4-C9 is superseded for E033 by D5-C10.
- **Previous champions:** E019 (H015 v2, Day 3; development mean 444.49); E005 (H004, Day 1; 482.73).

## Day 5 results (`research/day-05/DAY_SUMMARY.md`, FINAL)

- **H021 v3 (E031): clause 1 not met, final.** Within CatBoost at fixed capacity, the categorical statistics carry signal: −4.91 s against integer codes on `NM_present_excl_LIRF`. The noise condition is met by E032 (m = +0.68 s).
  - E031 alone: 440.76; −1.69 s against E029 on all rows, W1 TIE. Its S1 WIN is 62 % one row (D5-C11). Not a candidate.
- **H022 v3 (E030):** the codes control, 446.50.
- **H023 v3 (E033): PROMOTE.** Clauses 1–2 not met: −3.96 s on normal taxis, −3.58 s on all rows against E029.
- **Laptop reproducibility (rule L v2).**
  - Laptop runs equal the cloud runs except on LIRF's routed rows.
  - Cause: polars' thread pool (16 against 4) changes the ridge's statistics in the last bits.
  - Instances: **E026** for E019; **E029** for E023, also the route-integrity reference for FS2/FS2_RAW frames; **E028** for E005 in a reduced role; **E027** for curves only.
- **CPU against GPU.**
  - CatBoost on the laptop GPU is 0.16–0.25 s per iteration, against 0.88–1.13 s on Day 4's cloud CPU.
  - XGBoost on GPU is slower than CPU LightGBM; LightGBM has no GPU build here.
  - CatBoost on GPU is not deterministic.
- **Corrections D5-C1 to D5-C16:** `research/day-05/acks/` (LAPTOP_REFS v1 ack, H021 v1 ack, PHASE_CLOSE_D05 ack).

## Environment and incidents

- **Rule L v2 item 6 binds Days 6–7** to this environment:
  - CPython 3.13.15; `uv.lock` `efa4fd78…`; polars 1.44.2, default thread pool (16; `POLARS_MAX_THREADS` unset);
  - numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, LightGBM 4.7.0, CatBoost 1.2.10;
  - the owner's laptop: WSL2 11 GB, **4 GB swap (INC-0010)**, RTX 5060 8 GB.

  A change ends the instances and needs a new ruling. Every run records its environment in its manifest.
- **Open incidents:**
  - **INC-0012** (owner run window), **INC-0013** (Sonnet delegation, Day 6);
  - **INC-0004** (Day 3 launch configuration; owner decision);
  - **INC-0009** (W&B mirror and learning curves);
  - **INC-0010** (swap kept; CPython 3.13 kept: owner decisions).
- **Closed in Day 5:** INC-0006 (no delegation), INC-0007, INC-0008, INC-0011. Delegation on Days 6–7 needs a new incident.
- **Practice:** one experiment at a time under the experiment lock (INC-0008). No commit under `src/` or `scripts/` while an experiment runs (D5-C6). No allocation beyond a review's stated scope (D5-C5).

## Holdout

- Day 1: used (WIN). Day 2: closed unused (ruling H). Day 3: used (WIN, E019 against E005). Day 4: closed unused (ruling H4).
- **Day 5: 1 of 1 used (WIN, E033 against E026).**
- Day 6 has one access, which needs a Day 6 allocation as NEW (not E035–E039).
- Never NEW, in any phase:
  - E012–E018 and E020–E024 (rule 9; ruling H4);
  - E026–E032 and E034 (rule L v2; the H021 and H022 authorizations; the phase-close review).

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
- **Standing rule 13 (X-D05-S05-0001; from the next proposal on).** A candidate or champion with a non-deterministic component reports, beside criterion 6, per development fold and twin:
  - the reproduction's all-rows ΔRMSE;
  - its ΔRMSE on the mechanism population;
  - the RMS prediction change between the draws.

  It states that its evaluated and H figures are one draw. Disclosure only.

  Batch conditions B1–B4 are carried.
- **Rulings:**
  - **H:** Day 2 holdout closed unused.
  - **B:** the +6,500 s criterion 8 bound is not re-derived.
  - **R:** a comparison base is a matched reference sharing the candidate's training procedure; criterion 4 carries every mechanism claim.
  - **H3:** the Day 3 access (WIN); figures recorded only.
  - **H4:** the Day 4 holdout closed unused; no carry-over.
  - **H5:** the Day 5 access E033 against E026 (WIN). The figures are recorded only. H is a joint test on one draw, with the routed rows excluded by construction.
  - **Rule L v2** (X-D05-S04-0002): laptop instances, the route-integrity reference, the boundary-disclosure table, and the environment binding.
  - **Hand-off base ruling** (X-D04-S02-0001 (e)): E023 (now E029) is the matched reference for `route_train_exclude` candidates on FS2. Rule 10 covers backend-only re-draws.
- **Rule 10 now also covers** E030's, E031's and E033's configurations: no unchanged re-submission as a candidate. **E031 alone, any other weight or any other component** is a candidate only through a new proposal.
- **Known leakage hazards:**
  - P/T/F labels. `MVT − AOBT_3` and `d_sched` are T.
  - The hour-resolution schedule-delay proxy is T.
  - `ades` is F on diversions (~0.03 % of rows).
  - Cross-month information is inadmissible.
- **Key data facts:**
  - NM-missing rows are 0.8–2.1 % of each fold and carry 14–66 % of the SSE; there are 20,821 in Jan–Nov.
  - LIRF: 83 % of tail rows are block-at-schedule, and 931 of 932 NM-present ones have a normal anchor.
  - Every fold except W1c trains on more than 200,000 rows, the LightGBM bin-sample threshold.
- **Open questions for Days 6–7** (DAY_SUMMARY §9):
  1. CatBoost alone or other weights (selection hazard; new proposals only);
  2. submission reproducibility of a GPU re-draw (rule 13);
  3. D3-C3's January exposure;
  4. "LightGBM already holds the keys" (D4-C7) remains untested as stated;
  5. neural models (not attempted).
- **Open blockers:** none.
