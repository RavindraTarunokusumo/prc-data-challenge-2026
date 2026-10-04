# Research State

*Updated 2026-10-04T18:03:01Z (measured with `date -u`; D07-S01, after the Day 7 phase close and holdout WIN; the freeze is pending).*

- **Phase:** **Day 7 closed** (phase close X-D07-S01-0003 ACCEPT 0.85; holdout **WIN**). **Not yet FROZEN.**
  - Splits, metric and availability definition are FROZEN (`config/frozen.json`).
  - **Champion E046** (H035 v1) since the Day 7 phase close: E033 with the LIRF NM-missing subgroup predicted by E045 (E020's configuration). December 2025, E046 against E033, one access: WIN, −124.24 s (E046 244.94, E033 369.18). Objection F is resolved for December only; U6 stands (the gain is a bet on LIRF's recording convention, with a downside of similar size).
  - **Final submission file (P4):** E050's (`predictions/final/E050/submitting.parquet`) if E049 and E050 complete and pass every check; otherwise E044's (`predictions/final/submitting.parquet`, SHA-256 `d57ff7db…`, E033's procedure).
- **Sessions:** D07-S01, on branch `day-7`. **Last completed exchange:** X-D07-S01-0003. **Pending:** E049 and E050 (ALLOCATED), which start on the owner's word (INC-0016, script `run_e049_e050.sh`).
- **Next action:** on the owner's word, run the script; then `make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050`, the P6 flag, then FROZEN (P7). If the owner declines, P4's fallback applies (E044's file) and FROZEN follows. Then the owner uploads once. Next experiment id: **E051** (none planned).

## Champion: E046 (H035 v1), since the Day 7 phase close

- See Phase above and `models/champion/CURRENT.json`. Standing disclosures: E033's (below), plus U6, U7 (December only), rule 6 (W1 0.79 one row), rule 12 (subgroup bulk rows above 3,600 s), D7-C7, and the H exposure (88 rows on 26 days).

## Previous champion: E033 (H023 v3), Day 5 phase close to Day 7 phase close

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
  - **D5-C9 (stochastic champion), updated by D6-C11.**
    - Three draws exist: E033; E034 (seed + GPU); E041 (fixed seed, Day 6). On all rows the per-fold spread is ≤ 0.60 s and every draw has 7/7 WIN against E026 (−5.62, −5.54, −5.52 s).
    - **On the mechanism population the W1 spread is 2.00 s:** clause 1's W1 gain over E029 is −1.59, −0.31, +0.40 s by draw. 69 % of E033's W1 gain sits outside normal taxis (8.2 % of W1 rows). CatBoost alone: W1 spread 1.57 s all rows, 3.94 s normal taxis.
    - The evaluated and H figures are one draw. **SUBMIT predictions will be a further draw** (and SUBMIT trains on 12 months).
  - **D5-C10 (single rows).**
    - S1 is −3.76 s without row 192622644; the blend predicts 9,008 s there (y 87,002).
    - W1 is −2.56 s without row 183910286 (blend 15,086 s; y 13,865), and that row's W1 prediction rests on post-validation months.
  - **The 1,000-iteration budget.** CatBoost was still improving at 1,000 (−0.73 s over iterations 800–1,000). A change of iterations is a new configuration.
  - **Day 6 attribution (X-D06-S01-0004 item 3).** At equal weight, three substitutes for E031 fall short (D against E033 on normal taxis: codes CatBoost +1.34 s, per-key CatBoost +1.65 s, LightGBM twin +2.43 s). They keep 39–66 % of E033's gain against the most favourable of three champion draws (41–70 % against their mean). Rung B is at its threshold (+0.97 s against E041; D6-C6). "Statistics" and "combinations" are not separated from CatBoost's `data_partition` (D6-C7). No necessity claim (D6-C9): scope "this CatBoost configuration as a whole".
  - **Retired:** D3-C2 is treated (> 3 h band 3 against 81) and kept as history. D4-C9 is superseded for E033 by D5-C10.
- **Previous champions:** E019 (H015 v2, Day 3; development mean 444.49); E005 (H004, Day 1; 482.73).

## Day 6 results (`research/day-06/DAY_SUMMARY.md`, FINAL)

- **No Day 6 result contradicts the champion's promotion; neither batch had real power against its performance claim** (D6-C12). The SUBMIT procedure and D3-C3 were not attacked.
- **Ladder (E035–E039, controls):** rung B (E029 + codes CatBoost) "statistics carry part" (draw-dependent, D6-C6); rung C (E029 + per-key CatBoost E036) "combinations carry part" (with the `data_partition` disclosure); rung A (E029 + LightGBM twin) does not reproduce the gain (averaging floor −1.53 s at seed 42). E036's own reading INCONCLUSIVE (closed set: `data_partition`); its values (+0.04 s vs codes, +4.96 s vs complexity 4) are only consistent with the combinations carrying E031's advantage (D6-C8).
- **Draw robustness (E040–E041):** robust to one further fixed-seed (GPU-only) draw on all rows; W1 normal-taxi spread 2.00 s (D6-C11).
- **Corrections D5-… and D6-C1 to D6-C15:** `research/day-06/acks/PHASE_CLOSE_D06_ack_v1.md`. D6-C5 corrects Day 5 §1's "a second learner family adds signal" (broader than the accepted scope).

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
  - **INC-0015** (owner decision to test the routing candidate; window 02:00–03:00 CEST, no deviation; E049/E050 deferred);
  - **INC-0016** (E049/E050 start on the owner's word);
  - **INC-0004** (Day 3 launch configuration; owner decision);
  - **INC-0009** (W&B mirror and learning curves; **E036–E039, E042, E043, E045–E048 never mirrored**);
  - **INC-0010** (swap kept; CPython 3.13 kept: owner decisions).
- **Closed in Day 5:** INC-0006 (no delegation), INC-0007, INC-0008, INC-0011.
- **Closed in Day 6:** INC-0012 (owner run window; no deviation), INC-0013 (Sonnet delegation; one script). **Any owner instruction on run timing or delegation in Day 7 needs a new incident.**
- **Practice:** one experiment at a time under the experiment lock (INC-0008). No commit under `src/` or `scripts/` while an experiment runs (D5-C6). No allocation beyond a review's stated scope (D5-C5).

## Holdout

- Day 1: used (WIN). Day 2: closed unused (ruling H). Day 3: used (WIN, E019 against E005). Day 4: closed unused (ruling H4).
- **Day 5: 1 of 1 used (WIN, E033 against E026).**
- **Day 6: 0 of 1, closed unused (ruling H6).**
- **Day 7: 1 of 1 used (WIN, E046 against E033). Ruling H7: the project's last H read.**
- **Day 7 has one access,** through a Day 7 allocation as NEW, named by the Day 7 phase close.
- Never NEW, in any phase:
  - E012–E018 and E020–E024 (rule 9; ruling H4);
  - E026–E032 and E034 (rule L v2; the H021 and H022 authorizations; the phase-close review);
  - **E035–E041** (X-D06-S01-0001 ruling, extended by X-D06-S01-0003; ruling H6 (e));
  - **E042–E044** (the SUBMIT fits; X-D07-S01-0001);
  - **E045, E047–E050** (components, reproductions and SUBMIT fits; U5). **E046** may be NEW in the Day 7 access only, if the phase close names it.

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
- **Standing rule 14 (X-D06-S01-0004).** When several draws of a stochastic reference exist, any reading against that reference also reports the point contrast against each draw (exact identity, same rows). The pre-registered reference governs. Disclosure only. Batch conditions B1–B4 are carried.
- **Rulings:**
  - **H:** Day 2 holdout closed unused.
  - **B:** the +6,500 s criterion 8 bound is not re-derived.
  - **R:** a comparison base is a matched reference sharing the candidate's training procedure; criterion 4 carries every mechanism claim.
  - **H3:** the Day 3 access (WIN); figures recorded only.
  - **H4:** the Day 4 holdout closed unused; no carry-over.
  - **H5:** the Day 5 access E033 against E026 (WIN). The figures are recorded only. H is a joint test on one draw, with the routed rows excluded by construction.
  - **H6:** the Day 6 holdout closed unused ("0 of 1, closed unused"; not a TIE); no carry-over; no substitute comparison; no `holdout_check.py` with E035–E041 as NEW in any phase; H does not test the SUBMIT procedure.
  - **Rule L v2** (X-D05-S04-0002): laptop instances, the route-integrity reference, the boundary-disclosure table, and the environment binding.
  - **Hand-off base ruling** (X-D04-S02-0001 (e)): E023 (now E029) is the matched reference for `route_train_exclude` candidates on FS2. Rule 10 covers backend-only re-draws.
- **Rule 10 now also covers** E030–E041's configurations (and E033's): no unchanged re-submission as a candidate. **E031 alone, any other weight or any other component** is a candidate only through a new proposal.
- **Known leakage hazards:**
  - P/T/F labels. `MVT − AOBT_3` and `d_sched` are T.
  - The hour-resolution schedule-delay proxy is T.
  - `ades` is F on diversions (~0.03 % of rows).
  - Cross-month information is inadmissible.
- **Key data facts:**
  - NM-missing rows are 0.8–2.1 % of each fold and carry 14–66 % of the SSE; there are 20,821 in Jan–Nov.
  - LIRF: 83 % of tail rows are block-at-schedule, and 931 of 932 NM-present ones have a normal anchor.
  - Every fold except W1c trains on more than 200,000 rows, the LightGBM bin-sample threshold.
- **Open questions for Day 7** (Day 6 DAY_SUMMARY §9):
  1. **the SUBMIT procedure** (12 training months, a fresh draw): untested by any development fold; H cannot test it;
  2. **D3-C3's January exposure** (untested);
  3. the causal-only variant anticipated by the dataset audit;
  4. the 1,000-iteration budget;
  5. CatBoost alone, other weights or draw averages (selection hazards; new proposals stating the selection);
  6. neural models (not attempted);
  7. named, not required: `data_partition` equalised between complexity 1 and 4; a second draw of E030.
- **Open blockers:** none.
