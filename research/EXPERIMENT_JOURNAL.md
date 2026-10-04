# Experiment Journal

Append-only. One entry per experiment; negative results are kept.

## Day 1 — baselines (exchange X-D01-S01-0003)

### E001 · H001 global mean (incumbent) · COMPLETE
- Development mean RMSE **580.79** (R1 560.33, R2 437.07, R3 532.05, S1 746.06, W1 628.41; S1c 746.25, W1c 628.36).
- Matches the pre-registered expectation (RMSE ≈ fold std). The pipeline is validated end to end.
- Decision: incumbent by pre-registration. Analysis: `experiments/E001/analysis.md`.

### E002 · H002 airport median · COMPLETE → PROMOTE (champion)
- Development mean **553.74**. Against E001: mean dRMSE −27.05 s (q95 −24.51). All 7 folds WIN; tail share 0.037; no row concentration.
- Reproduction E007 (seed 43) is identical. LFPG shows the expected small forward exposure (S1 400.5 against S1c 412.6).

### E003 · H003 airport × hour median · COMPLETE → PROMOTE (champion)
- Development mean **548.42**. Against E002: mean dRMSE −5.31 s (q95 −4.90). Folds: 4 WIN, W1 TIE; twins WIN. Tail share 0.065.
- Reproduction E008 exact. The gain (0.96 %) is just below the predicted 1–3 %. The takeoff-hour effect mixes diurnal demand with taxi-duration mechanics (label T).

### E004 · H005 anchor `MVT − AOBT_3` · COMPLETE → REJECT
- Development mean 550.65. Against champion E003: mean +2.22 s; R1 and R2 LOSS, W1 WIN (−50 s); criterion 3 fails (EDDM, LTFM, EHAM). Falsified.
- **Dominant row:** the day-scale LIRF row (anchor 87,181 s) has target **87,002 s**. The raw anchor is exact on it, and bounded models miss by about 86,000 s. It alone decides the S1 outcome (S1 bulk +51.8 s).
- The anchor helps strongly in winter (W1 bulk −47 s) and hurts in the bulk elsewhere.

### E005 · H004 ridge FS0 · COMPLETE → PROMOTE (champion)
- Development mean **482.73** (predicted 400–470 s: a miss). Against E003: mean −65.70 s, all 7 WIN, tail share 0.254.
- Against H005: all WIN. Rows beyond the winsorisation clip carry 5–40 % of that margin, so the fitted combination is the main mechanism and clipping a secondary one.
- Reproduction E009 exact. CLASS-S (3.76 GB).

### E006 · H006 LightGBM FS0 · COMPLETE → INCONCLUSIVE (not promoted)
- Development mean **377.87**, the lowest of Day 1. Against ridge E005: mean −104.86 s, all 7 WIN; the ablation (H008) passes.
- **Standing rule 1 fails.** The tail share of the SSE change is 0.991. The bulk is worse on S1 (+46 s) and R1 (+5 s), and 10 rows carry 66–83 % of the change.
- **The gain comes from tail rows without NM data** (0.40–1.04 of the change), not from the pre-registered anchor mechanism.
- NM-unmatched DEP rows have a 4.9 % tail rate against 0.15 %. At LIRF the rate is 49 % (mean 6,457 s). Candidate hypothesis for Day 2.

### E010 · H008 LightGBM without deltas (ablation of H006) · COMPLETE
- Development mean 502.34. H006 beats it by 124.5 s (all WIN): the deltas are used. The Expected Result was inconsistent and is not scored.

### E011 · H007 XGBoost FS0 · COMPLETE → REJECT
- Development mean 424.67. Against ridge: S1 TIE, so criterion 2 fails. It is 12.4 % worse than H006 (configuration, per review).
- The same NM-missing tail pattern appears. S1's dominant row is a second day-scale LIRF record (target 87,186 s) without NM data.

### Day 1 chain result
Incumbent H001 → H002 PROMOTE → H003 PROMOTE → H005 REJECT → H004 PROMOTE → H006 INCONCLUSIVE → H007 REJECT. **Initial champion: E005 (H004 ridge FS0), development mean 482.73.** The phase-close holdout check is pending.

### Day 1 phase close (X-D01-S01-0004: ACCEPT)
- **Holdout access** (the single Day 1 access): E005 411.29 against E001 514.74 on December; dRMSE −103.45 (q10…q90 −122.60…−90.21) → **WIN**, and the promotions stand.
- **Record corrections C1–C7** (`research/day-01/acks/PHASE_CLOSE_D01_ack_v1.md`):
  - H006's tail share nets a real bulk gain on NM-present rows;
  - the LIRF tail is largely a block-at-schedule recording convention (label T);
  - NM-missing rows carry 14–66 % of the SSE;
  - there are 15 day-scale records in Jan–Nov.

## Day 2 — static and temporal structure (exchanges X-D02-S01-0001 to 0003)

Proposal history:
- H009: v1 REVISE, v2 REVISE, **v3 ACCEPT**.
- H010 v1: ACCEPT.
- H011: v1 REVISE, **v2 ACCEPT**.
- H012 v1: ACCEPT.

The chain runs sequentially: H009, then H010, then H012, then H011.

### E012 · H009 v3 LightGBM FS1 (candidate) · COMPLETE — chain step 1

- **Development mean 376.15** (E006: 377.87; E005: 482.73). 906 s, 4.14 GB, CLASS-M.
- **Clause 1 (against E005):** passes, −106.58 s (q95 −84.41), 7/7 WIN, criterion 3 met. NM-present bulk dRMSE −41 to −50 s (E006: −31 to −40).
- **Clause 2(a), M1** on NM-present rows outside LIRF: passes.
  - Mean −7.16 s (q95 −6.25). Four counted WINs.
  - W1c is LOSS, which voids the W1 WIN (flagged residual exposure).
  - No row concentration.
- **Clause 2(b):** passes. NM-present bulk dRMSE is −8 to −14 s on all five development folds.
- **v2's population would have falsified H009 through row 192622644 alone** (S1 TIE on NM-present rows, top-1 share −8.93).
- **LIRF NM-missing.** Static keys dilute the convention signal: bulk gains on 4/5 folds, losses on day-scale records.
- **Pending:** clause 3 (H010) and clause 4 (H012), then the conditional reproduction.

### E013 · H010 v1 LightGBM FS1 − `d_sched` (M3 ablation) · COMPLETE — clause 3

- **Development mean 415.03** (predicted 395–440). 843 s, 4.18 GB.
- **Clause 3 not met:** H009 − H010 on LIRF NM-missing rows is −314 to −2,493 s on all five development folds. **M3 is supported**, and exact `d_sched` adds well beyond the hour-resolution proxy.
- **The criterion 8 rule for H009 is satisfied, and the LIRF bulk-trade objection is resolved.**
- **Missed predictions:**
  - The LIRF NM-missing bulk was recovered only on R1 and S1; it got worse on R2, R3 and W1.
  - S1 was the largest net H010 loss, not the smallest.
- NM-present bulk: `d_sched` is worth 1–8 s (within the prediction).

### E014 · H012 v1 LightGBM FS1 − {`d_aobt3`, `d_eobt1`} (M2 ablation) · COMPLETE — clause 4

- **Development mean 413.40.** On NM-present rows, 305.9 (predicted 300–350).
- **Clause 4 not met:** H009 − H012 on NM-present rows is −51.30 s (q95 −47.49), 7/7 WIN. **M2 is supported.**
  - The anchor is worth about 51 s beyond `d_sched`, most in winter (W1 −84 s).
- The feared dominant row (192622644) carried only 0.16 on S1.
- **H009 v3 is not falsified on any clause (1–4).** The seed-43 reproduction is authorized.

**Ordering note (D02-S01).** The H009 reproduction was allocated as **E015** before H011 (step 4 of the registered chain), a researcher slip. The **run order** follows the registration: H011 (**E016**) runs before E015. The two are independent. H011's preconditions need only E012, E013 and E014, and the reproduction's condition (clauses 1–4 not met) was already settled. E-number order is therefore not run order for these two.

### E016 · H011 v2 LightGBM FS0-no-deltas + 4 static keys · COMPLETE — the Day 2 question

- **Development mean 474.33** (E010: 502.34; predicted 470–495).
- **Not falsified:** on rows excluding LIRF NM-missing, −30.03 s (q95 −28.46), 5/5 WIN; W1c TIE.
- **Answer.** Static keys are worth about 30 s without the anchor and about 7 s with it; the anchor absorbs roughly three-quarters of the static signal.
- **Missed rule 8 pre-registration.** The static keys still reach the LIRF convention (R3 and W1 tail share 0.5; bulk up to +3,082 s), likely via operator × destination × takeoff hour.

### E015 · H009 v3 reproduction (seed 43) · COMPLETE → criterion 6 FAILS

- **|Δ| against E012:** R1 0.35, R2 0.91, **R3 1.73**, **S1 3.50**, W1 0.07 s. The tolerance is 1.0 s, so it fails.
- The criteria against E005 still hold (7/7 WIN).
- **Localised.** Excluding LIRF NM-missing rows, R3 moves 0.23 s and S1 1.33 s. On NM-present rows outside LIRF, 0.21 and 0.91 s.
  - The seed variance is the bagged mixture prediction on a handful of day-scale LIRF convention records (e.g. 200300302: 16,148 against 13,746 s).

### H009 v3 · decision: **INCONCLUSIVE** (not promoted; E005 remains champion)

- Clauses 1–4 are not met, so H009 is not falsified. Criteria 1–3, 5 and 7 pass, and the criterion 8 LIRF objection is resolved.
- **Criterion 6 (reproduction) fails.**
- The failure is carried by LIRF convention records, not by the static or anchor mechanisms. It is a structural exposure of every bagged Tier 1 model that uses `d_sched` on those rows, for the phase-close review.

### X-D02-S01-0004 · H013 v1 REVISE, H014 v1 ACCEPT (conditional; lapses under H013 v2)

- **H013 v1's premise was false.** LightGBM without subsampling still consumes the seed above 200,000 training rows, through the bin-construction sample. Seven of eight folds exceed that.
- **The researcher's supporting check was a false negative** (small, simple synthetic data), and its commit citation was wrong: the check was never committed.
- **Corrections.** E015's instability is not attributable to subsampling alone. A committed test now covers the regime above the threshold.
- **Rulings.**
  - A training procedure with **no random component** satisfies criterion 6; one that fixes a random step independently of the seed does not.
  - E015's spread becomes a standing disclosure if an H013 version is promoted.

### E017 · H013 v2 LightGBM FS1, no random component (candidate) · COMPLETE → INCONCLUSIVE

- **Development mean 378.82.** 668 s, faster than the bagged model.
- **Clause 1:** −103.90 s against E005, 7/7 WIN.
- **Criterion 8 NOT resolved:** LIRF NM-missing bulk on S1 is +7,104 s, above +6,500. Without bagging, the convention-row predictions are more extreme (Alternative Explanation 1).
- **Clauses 2(a), 2(b), 3 and 4 are not met;** objection T does not stand. Not falsified, not promotable, and no reproduction run.
- **Deterministic against bagged on NM-present rows: −0.75 s** (every fold within ±2.4 s). All material differences are on LIRF NM-missing rows.

### E018 · H014 v2 LightGBM FS0, no random component (M1 reference) · COMPLETE

- **Development mean 380.95** (+3.08 s against the bagged E006).
- **M1 replicated:** H013 v2 − H014 v2 on NM-present rows outside LIRF is −7.27 s (bagged: −7.16), and W1c is LOSS again.

### Day 2 phase close (X-D02-S01-0006: ACCEPT)

- **No promotion. E005 remains champion by rule** (not the most accurate: the Tier 1 fits beat it by 51.5–59.6 s on NM-present rows on every development fold).
  - H009 v3: INCONCLUSIVE (criterion 6).
  - H013 v2: INCONCLUSIVE (criterion 8).
- **Holdout: Day 2 0 of 1, closed unused** (ruling H).
- **Record corrections D2-C1 to D2-C10** (`research/day-02/acks/PHASE_CLOSE_D02_ack_v1.md`). Among them:
  - on all rows, FS1 is not distinguishable from FS0 (−1.72 s, q95 +9.39);
  - the "30 s vs 7 s" comparison mixed populations; the matched NM-present figures are −29.6 s without deltas and −9.1 / −8.7 s with them;
  - static keys worsen July's convention statistic;
  - seed variance is not confined to LIRF NM-missing rows (S1 +1.33, W1 −1.94 s outside them);
  - deterministic training costs about 3 s on all rows.
- **Standing rules 9–11 adopted.** Rulings B (the +6,500 s bound stands) and R (comparison base = a matched reference).

## Day 3 (D03-S01)

### Exchanges X-D03-S01-0001 and -0002

- **X-D03-S01-0001** (attempt 2 after a container restart): H015 v1, H016 v1 and H017 v1 all REVISE.
  - H015's routing rationale rested on false monthly counts.
  - Row 192622644 could decide the C clause on S1.
  - Five P features read the row's own takeoff on 0.086 % of rows.
- **Commit `63923e2`:** the P features now remove the row's own contribution exactly. Masking invariance was re-verified on 1,919,370 rows.
- **X-D03-S01-0002:** all three v2 proposals ACCEPT. The C clauses are on `NM_present_excl_LIRF`, and code is frozen for the chain.

### E019 · H015 v2 routed LightGBM on FS2 (primary) · COMPLETE

- **Development mean 444.49** (pre-registered 432–447). 954 s, 4.76 GB.
- **Clause 1 not met:** −38.23 s against E005 (q95 −34.95), 7/7 WIN, criteria 1–3 pass, and no airport degraded.
- **Clause 2 not met:**
  - on `NM_present_excl_LIRF`, C is **−6.75 s** (q95 −5.97), 7/7 WIN, below the −6.0 s floor by 0.75 s;
  - the NM-present bulk improves on every development fold;
  - no dominant row (|top-1| ≤ 0.10).
  - The Advisor had forecast −3 to −5 s.
- **Clause 4 not met:** the criterion 8 statistic is 0.0 on every fold (routed).
- **Clause 3 open:** it needs H016 v2.
- **Reported:**
  - on all rows, E019 is +65.67 s against E017 (LOSS 7/7), as pre-registered: routing forgoes the convention tail gain;
  - on all rows, E019 is worse than E005 on the NM-missing rows at the other nine airports on four development folds, with extreme predictions there (e.g. −8,859 s on an EHAM row). This is a candidate Day 4 question.
- **The container restarted after the run.** The predictions were re-verified, and H016's determinism check will be cross-container.

### E020 · H016 v2 unrouted LightGBM on FS2 (R ablation) · COMPLETE

- **Development mean 321.95** (pre-registered 360–380: outside, better). 1,181 s, 4.62 GB. **Cross-container** relative to E019.
- **H015 v2 clause 3 not met:** routed rows equal E005 exactly, and E019 and E020 are **bit-identical outside the routed rows on all 8 folds across a container restart**. Cross-container determinism holds.
- **H016 − E017 on all rows: −56.87 s** (pre-registered −2 to −15: outside, larger).
  - Almost all of it is on LIRF NM-missing rows (tail share 0.72): FS2's in-taxi counts, anchored at SCHED for convention records, carry the schedule delay more finely.
  - On `NM_present_excl_LIRF` it equals H015 − E017 (−6.75 s).
- **R effect** (H015 − H016 on LIRF NM-missing): full > 0 on 5/5 development folds, bulk < 0 on all folds (S1 −4,292 s), as pre-registered.
- **Criterion 8 statistic S1 +4,292 s** (pre-registered +6,000 to +8,000). It is below the +6,500 bound on every development fold, the first unrouted Tier 1 fit to be so. **Observation only:** H016 is not a candidate.

### E021 · H017 v2 LightGBM on FS2_P (P/T decomposition) · COMPLETE

- **Development mean 372.14** (pre-registered 370–385). 1,071 s, 4.86 GB.
- **Reading 1, T given P** (E020 − E021 on `NM_present_excl_LIRF`): −3.28 s, 7/7 WIN, criteria 1–2 pass, but above the −6.0 s floor. **Not supported.**
- **Reading 2, P beyond E017:** −3.47 s, 7/7 WIN, above the floor. **"P effect not distinguishable from training noise".**
- **Reading 3, all rows:** −6.68 s (q95 −1.26); 3 WIN and 4 TIE, so criterion 2 fails.
- **The decomposition adds exactly:** −3.47 + −3.28 = C = −6.75 s. Each half is consistent (7/7 WIN) but about half the floor.
- **The EDA's T-dominance does not survive the anchor in the model.** For Days 5–7: about −3.5 s of the congestion gain is available at the off-block proxy (P).

### E022 · H015 v2 reproduction (seed 43) · COMPLETE

- **Criterion 6 PASS:** every development-fold RMSE equals E019's (Δ 0.0 s); criteria 1–3 hold against E005 (7/7 WIN).
- **All 8 prediction files are byte-identical to E019's,** across a seed change and a container restart. Real-data determinism is confirmed.

### H015 v2 outcome (pre-registered clauses and criteria)

- **Clauses 1–4 are all not met; criterion 6 passes; criterion 8 is 0.0.** H015 v2 is **not falsified**, and every promotion condition verifiable before the phase close holds.
- **Under authorization item 6, promotion is subject to the Day 3 phase-close review and to holdout access as that review names it (rule 9).** No promotion is recorded yet; the champion is still E005.

### Day 3 phase close (X-D03-S01-0003: ACCEPT, 0.82)

- **H015 v2 PROMOTE. E019 is champion.** Holdout H (December 2025), one access, E019 against E005: **WIN**, −35.36 s (375.93 against 411.29). No revert. The H figures are recorded only (ruling H3).
- **Standing disclosures on the champion:**
  - **D3-C1:** 95 % of the margin is routed FS1 structure; congestion as served is −1.90 s on all rows.
  - **D3-C2:** out-of-range predictions on non-LIRF NM-missing rows, caused by the congestion block.
  - **D3-C3:** January 2026 long-delay NM-missing counts are 2.0–2.6 times the 2025 maximum.
- **Other corrections:**
  - D3-C4: CPU strings; determinism held across two.
  - D3-C5: INC-0004 scope, and the restarts recorded late.
  - D3-C6: STATE.md stale.
  - D3-C7: a figure.
  - D3-C8: forecasts misquoted or omitted.
  - D3-C9: the Advisor's own miss.
- **Standing rule 12 adopted.** The routing answer allows an unrouted Day 4 candidate under conditions.

## Day 4 (D04-S01): historical priors and interactions

*Provenance: INC-0004 (open; launch `--effort medium`, metadata `high`) and INC-0005 (open; owner-instructed delegation to `claude-sonnet-5-5` workers) cover every Day 4 record. Items marked "worker" were implemented by a Sonnet worker to the researcher's specification and reviewed by the researcher.*

### Infrastructure (no experiment)

- **`scripts/range_check.py`** (worker) implements rule 12, with `--by-dsched` and `--bands`. It reproduces D3-C2 (E019 above 5 h 41/93 = 44 %) and D3-C3 (January 2026: 435 and 92) exactly.
- **Out-of-range bands** on `NM_missing_other` bulk rows, 5 development folds (`range_check_refs.json`):
  - every LightGBM has 60–83 below 1 h of schedule delay (a generic phenomenon);
  - the congestion (T) increment is in the > 3 h band: E019 81 against E021 18 and the other no-T fits' 13–41.
- **Prior EDA** (worker; never-validation months only):
  - stand × runway carries the prior signal (+0.19 R² over airport × hour in a linear model, stability 0.94, subsumes stand);
  - FS3's keys give 0.4570 against 0.4505 for [K1, K5];
  - there is no anchor control, so these are loose upper bounds.
- **FS3** (worker): FS2 plus 5 fold-local LOMO smoothed-mean priors (`src/prc/priors.py`). FS0–FS2 are byte-identical after the refactor.
- **`route_train_exclude`** (researcher). **`gbm.catboost` and `routed_catboost`** (worker).
- **CatBoost CPU calibration:** feature combinations make per-iteration cost grow; `max_ctr_complexity=1` makes it linear (0.29 s per iteration on R3).

### X-D04-S01-0001 (batch H018 v1, H019 v1, H020 v1)

- **H018 v1 REVISE (0.88).**
  - Clause 1 (total out-of-range count ≤ 93) did not test D3-C2: the increment sits in the > 3 h band, and the < 1 h band is generic.
  - The rule 8 sentence was false: LIRF NM-present convention tail rows stay in training.
- **H019 v1 REVISE (0.82).**
  - W1c is inert (a single training month), so it could not LOSS.
  - The key-selection rule and the joint figures were missing.
  - The same rule 8 error.
- **H020 v1 REJECT (0.80); CLASS-L declined. Kept as a negative result.**
  - The stated mechanism was false for the installed CatBoost 1.2.10: plain boosting, and RMSE CTRs that are a border share plus a count, not a smoothed mean.
  - FS1's `__RARE__` collapse and `max_ctr_complexity: 1` removed what the mechanism needed; capacity was confounded.
  - **No CatBoost experiment in Day 4.** The code and calibration are handed to Day 5.
- **Correction D4-C1:** the v1 `created_utc` values were written by hand, not measured, and post-dated their commit. They are measured from v2 on.

### X-D04-S01-0002 (H018 v2, H019 v2)

- **H018 v2 ACCEPT (0.86).**
  - Clause 1: > 3 h band ≤ 50 (E019 81, E021 18).
  - Clause 2: `NM_missing_other` bulk < 0 on at least 3 of R1, R2, R3 and W1.
  - Clause 3: route integrity.
  - Rule 8 `NM_present_LIRF` pre-registration, and S1 attribution recording.
- **H019 v2 ACCEPT (0.80).**
  - Clause 1: `NM_present_excl_LIRF` against H018, criterion 1, 3 counted WINs among R1–R3 and S1 (S1 required, frozen twin rule), no LOSS; mean ≤ −3.0 s.
  - Clause 2: all rows mean < 0.
  - W1c inert.
- **Advisor predictions:**
  - H018: mechanism holds 0.85 / 0.88; S1 WIN 0.20; promotion 0.12.
  - H019: mean ≤ −3.0 s 0.30; mechanism supported 0.27; promotion 0.10.
- **Corrections D4-C2 to D4-C6** (acks v2):
  - D4-C2, D4-C4: Implementation Plan version labels.
  - D4-C3: `range_check_refs.json` commit order.
  - D4-C5: H019 rule 8 wording.
  - D4-C6: the dropped twin-rule phrase, restored by reading 4(a).

### E023 · H018 v2 routed LightGBM on FS2, LIRF NM-missing rows excluded from training · COMPLETE

- **Development mean 442.46** (E019: 444.49). 925 s, 5.29 GB. Allocated in D04-S01, run in D04-S02 after a container restart.
- **Clause 3 not met:** the routed rows equal E005.
- **Clause 1 not met:** `NM_missing_other` out-of-range count in the > 3 h band is **5** (limit 50; E019 81, E021 18, E017 14). Fraction of the increment removed: 1.21. Pooled > 5 h share: 1/93 (E019: 41/93).
- **Clause 2 not met:** `NM_missing_other` bulk against E019 is −197.85, −230.47, −105.67 and −104.99 s on R1, R2, R3 and W1.
- **D3-C2's attribution to the LIRF NM-missing training rows is supported.**
- **Promotion against E019: criterion 2 FAILS** (S1 TIE, +0.20 s). The mean is −2.04 s (q95 −1.31), with 5 WIN and 2 TIE. S1's change is carried by `NM_present_LIRF` (share +3.84; row 192622644).
- **H018 promotion status (H018 review item 7): NOT PROMOTED.** Recorded as "D3-C2 treated, not promoted", with the clause 1–2 outcomes above. No reproduction is due. **E019 remains the champion in force for H019 v2.**
- Reported: against E005, −40.27 s, 7/7 WIN.

### E024 · H019 v2 routed LightGBM on FS3 (FS2 + 5 fold-local LOMO priors), matched reference E023 · COMPLETE

- **Development mean 442.06** (E023 442.46; E019 444.49). 1,026.9 s, 5.73 GB. No container restart since E023. Launched by the main session (INC-0005).
- **W1c byte-identical to E023** (SHA-256 `37857400ac9d…`): the block is inert on a single training month, as pre-registered.
- **Clause 1 MET** (`NM_present_excl_LIRF` against E023): mean **−0.29 s** (q95 +0.12); R1, R2, R3 WIN, **S1 TIE, W1 LOSS** (+1.63). 1(a) is met (criterion 1 fails, S1 not a counted WIN, W1 LOSS), and 1(b) is met (−0.29 > −3.0). 4-fold mean (R1–R3, S1) −0.77 s.
- **Clause 2 not met:** all rows against E023, −0.40 s (q95 −0.03). LFPG +0.35 s (named in advance); no airport degraded.
- **H019 v2 mechanism: FALSIFIED.** The EDA's stand × runway R² (+0.189) does not carry beyond FS2 in this learner.
- **Promotion against E019: criterion 2 FAILS** (S1 TIE, +0.72 s; mean −2.43 s, q95 −1.59). Criterion 4 also blocks it (B2). S1's `NM_present_LIRF` share is 1.95, with row 192622644 moved further from its target (8,136 → 5,780 s against y 87,002 s). **NOT PROMOTED; no reproduction is due.**
- **Attribution pair** (development mean, all rows): H018 − E019 −2.04 s; H019 − H018 −0.40 s.
- `NM_present_LIRF` against E023: full −2.80 to +6.12 (within ±8), bulk −1.27 to −3.41 (within −1 to −6) on every development fold.
- Route integrity holds (not INVALID). Rule 12: > 3 h band 6 (E023 5).
- Reported: against E005, −40.67 s (q95 −37.32), 7/7 WIN.
- **E019 remains champion. Neither Day 4 candidate is promotable.**

### X-D04-S02-0001 · Day 4 phase close · ACCEPT (0.85)

- **Decisions stand:**
  - **E019 remains champion, by rule.** Its disclosures are D3-C1 to D3-C3 and **D4-C9**: S1 against E019 is decided by row 192622644, which carries 8.2 % of E019's S1 SSE. Without that row (audit only), E023 meets criteria 1–3.
  - E023: REJECT ("D3-C2 treated, not promoted").
  - E024: REJECT (mechanism falsified).
  - H020 v1: closed.
- **Ruling H4: Day 4 holdout 0 of 1, closed unused** (not a TIE). There is no carry-over. E023 and E024 are never NEW, in any phase.
- **Hand-off base ruling:**
  - Under ruling R, E023 is the matched reference for `route_train_exclude` candidates on FS2, and E024 for FS3. Neither is a default base nor a de facto champion.
  - Candidates are judged against E019.
  - Rule 10 covers backend-only re-draws of E020, E021, E023 and E024.
- **Corrections D4-C7 to D4-C16** (`research/day-04/acks/PHASE_CLOSE_D04_ack_v1.md`). The main ones:
  - the prior block is a real −0.40 s on all rows, not "nothing";
  - E023's "no cost" is scoped to `NM_present_excl_LIRF`;
  - the single-row S1 and W1 quantification;
  - the Advisor's forecast misses;
  - the ledger decisions are filled;
  - the delegated-work list and process notes are completed.
- **INC-0005 closed; INC-0004 open.** Days 1–4 (the cloud scope) are complete. Day 5 starts on the laptop from `docs/reproducibility/HANDOFF_D04.md`.

## Day 5 (owner laptop)

### E025 · H015 v2 reproduction · RESOURCE_FAILURE

- Killed by a global OOM in the WSL VM after R1 (446.40, equal to E019), caused by a concurrent researcher `pytest` (INC-0008). Not retried; records reconstructed from the kernel log. An experiment lock now stops memory-heavy side work during runs.

### E026 · H015 v2 reproduction · PASS (laptop compute check)

- All development folds within 0.008 s of E019 (tolerance 1.0 s); 668.7 s, 5.22 GB.
- **Not byte-identical:** all 8 prediction files differ from E019's hashes. Deterministic LightGBM is bit-stable across Intel CPU strings (Day 3), but not from Intel Xeon to AMD Ryzen (observation).
- **E019's, E005's and E023's prediction files are absent on the laptop,** so row-level comparisons against them cannot run. Ruling needed (first Day 5 exchange).

### E027 · H015 v2 reproduction with learning curves · PASS

- **Byte-identical to E026 (all 8 files):** learning-curve recording does not change the model. 892 s (+33 % for recording), 5.19 GB.
- **Curves (observation):** development-fold validation RMSE is flat from about 500 iterations, and the 1,000 rounds sit within 0.03–0.78 s of each fold's minimum. W1c (one training month) overfits from 180 (+4.9 s by 1,000). Train RMSE about 200 s against validation 270–630 s. No round count is selected from this (selection hazard, INC-0009 addendum).

### E028 · H004 v1 reproduction (laptop instance of E005) · PASS

- Within 0.011 s of E005 on every development fold; not byte-identical (ridge/BLAS). 72.7 s.

### E029 · H018 v2 reproduction (laptop instance of E023) · PASS

- Within 0.0072 s of E023; not byte-identical. 893 s, 6.60 GB (E023 5.29 GB; cause not established). Learning curves recorded.
- Single rows on the laptop: 192622644 (S1): E027 8,136 s, E029 7,041 s. 183910286 (W1, y 13,865 s): E027 1,979 s, E029 7,938 s.

### X-D05-S04-0001 · submitted: LAPTOP_REFS v1, H021 v1, H022 v1, H023 v1

- Rule L (laptop instances E027/E028/E029 for E019/E005/E023); the CatBoost GPU mechanism (H021) and its codes control (H022); the equal-weight blend candidate (H023, promotion P 0.20).

### X-D05-S04-0001 · REVISE ×4 (LAPTOP_REFS 0.90, H021 0.90, H022 0.90, H023 0.93)

- **The science of H021–H023 is sound.** The chain was blocked mainly by an unattainable route-integrity reference: the laptop's routed-path ridge differs from E028 on every routed row (D5-C4).
- **Corrections D5-C1 to D5-C7:**
  - swap was on (unused), and the interpreter is 3.13, not 3.11 (owner decisions in INC-0010);
  - the instance differences sit in LIRF's routed rows, not in the LightGBM;
  - E027–E029 were outside their reviews' scope (E029 contrary to H018 v2 item 9);
  - E029's manifest names the wrong commit;
  - the H021 calibration table misattributed a row.
- **Verified by the Advisor:** E027 and E029 reproduce the cloud E023-vs-E019 comparison to 1e-4 s, and `FloatTargetMeanValue` averages the raw target.

### X-D05-S04-0002 / -0003 · LAPTOP_REFS v2 ACCEPT; H021–H023 v3 ACCEPT

- Rule L v2 adopted (E026/E029/E028 instances, E029's routed rows the integrity reference, environment bound). Cause of the laptop differences: polars' thread pool (16 against the cloud's 4) changes the ridge's statistics in the last bits.
- Chain authorized: H022, then H021 (CLASS-L), then H021r, then H023, then H023r if due. Freeze anchor `803ceeb`.

### E030 · H022 v3 (CatBoost GPU, codes control) · COMPLETE

- Development mean 446.50 s; against E029 +4.05 s (S1 TIE). Route integrity holds (bit-identical routed rows). 225 s, 6.40 GB, no swap, GPU about 2.9 GB.
- Out-of-range on `NM_missing_other` falls from 99 (E029) to 34; the < 1 h band falls from 82 to 25.

### E031 · H021 v3 (CatBoost GPU, CTRs on raw keys) · COMPLETE; clause 1 provisionally not met

- **Development mean 440.76 s, the best single run so far.** Against E029 (LightGBM, E023's instance): −1.69 s on all rows, WIN on R1–R3 and S1, W1 TIE, no airport degraded. **Not a candidate (pre-registered).**
- Clause 1 (against E030): −4.91 s, 5/5 counted WINs. The categorical statistics matter at fixed capacity. **Provisional: the noise condition needs H021r, paused (INC-0011).**
- Missed expectations: CatBoost was expected to lose to the LightGBM (+2 to +15 s) and to lower the day-scale rows' predictions; it won, and raised them. 25 min, 7.01 GB, no swap, GPU about 3.1 GB.
- **Experiments paused after E031 by the owner (INC-0011).**

### E032 · H021 v3 reproduction · COMPLETE; clause 1 final: NOT MET (mechanism supported)

- Development mean 440.91 (E031 440.76). Integrity holds. The noise condition holds: m = +0.68 s against the 1.5 s limit.
- **CatBoost's categorical statistics carry signal at fixed capacity: −4.91 s (re-draw −4.23 s) against the codes control, 5/5 WINs.**
- The frozen 1.0 s reproduction tolerance fails on R1 (+1.056 s). This is a genuine GPU and seed re-draw. H021 is not a candidate.
- Resumed by the owner (INC-0011 closed). 19 min, 7.08 GB, no swap.

### E033 · H023 v3 (equal-weight blend: routed LightGBM E029 + routed CatBoost E031) · criteria 1–8 MET; PROMOTE recommended at the phase close

- **Development mean 438.87 s.** Against E019 (instance E026): **−5.62 s (q95 −4.79), WIN on all 7 folds including S1**; every airport improves. **D3-C2 is treated** (> 3 h band 3 against E019's 81).
- Clause 1 (complementarity on normal taxis): −3.96 s; clause 2 (all rows): −3.58 s. Neither is met. Residual correlation is 0.84–0.92 on bulk rows.
- The S1 WIN is not convention-carried (`NM_present_LIRF` share 0.24). The single-row constraint (D4-C9) did not bind: the CatBoost half raised row 192622644's prediction.
- **Missed pre-registrations:** the single-row directions (Missing Control 1), and the expectation that S1 would most likely TIE.

### E034 · H023 v3 reproduction · PASS (criterion 6)

- Within 0.48 s on every development fold; criteria 1–3 hold against E026 (7/7 WIN). Clause 1 −3.70 s.

### X-D05-S05-0001 · Day 5 phase close · ACCEPT (0.88); holdout WIN; champion E019 → E033

- **The decisions stand.** H023 v3 (E033) meets criteria 1–8 against E019 (instance E026).
- **Holdout H: WIN.** E033 369.18 s against E026 375.93 s (−6.75 s; q10/q90 −9.83/−4.88). No revert. Ruling H5: recorded only; a joint test on one draw. Instance check: E026 375.92735 s against E019's recorded 375.92721 s.
- **E033 is champion; E019 is previous.** E033 and E034 are PROMOTE.
- **Disclosures:**
  - D3-C1 (lineage); D3-C3 restated (D5-C16);
  - D5-C8: margin composition, −2.04 s treatment and −3.58 s CatBoost half;
  - D5-C9: stochastic champion;
  - D5-C10: single rows;
  - the 1,000-iteration budget.

  D3-C2 is retired as a defect, and D4-C9 is superseded.
- **Corrections D5-C8 to D5-C16**, including D5-C11 (CatBoost alone's S1 WIN is 62 % one row) and D5-C12 (attribution scopes).
- **Standing rule 13** (stochastic components: disclose the re-draw spread). INC-0006 closed (no delegation).

## Day 6 (D06-S01): adversarial attribution ladder (batch X-D06-S01-0002; controls, no candidate)

Exchanges: X-D06-S01-0001 (v1, REVISE ×5: bounded readings, rung A relabelled, H027 seed refused, launcher pinning), X-D06-S01-0002 (v2, ACCEPT ×5, conditions C1–C7). All five runs inside the owner's 21:00–21:30 window (INC-0012); no deviation. Freeze diff empty. Never NEW (ruling). Readings on `NM_present_excl_LIRF` against E033 (D), all rows beside.

### E035 · H026 v2 · rung B (E029 + codes CatBoost E030) · statistics carry part

- D +1.34 s (q95 +1.65), LOSS 5/5 dev folds. G −2.62 s (66 % of E033's −3.96). All rows: −1.77 vs E029, +1.81 vs E033.
- E030 disagrees with E029 more than E031 does (RMS 93 against 81 s) but is 4.6 s less accurate: the statistics' contribution runs through accuracy.

### E036 · H024 v2 · CatBoost complexity 1 · own reading INCONCLUSIVE (closed set)

- `data_partition` DocParallel against E031's FeatureParallel (CatBoost's GPU choice): violation, pre-registered → INCONCLUSIVE.
- Values: +4.96 s against E031 (5/5 LOSS), +0.04 s against the codes arm E030. Per-key statistics alone recover none of E031's advantage on normal taxis. Dev mean 444.46; 354 s (E031 1,523 s).

### E037 · H025 v2 · rung C (E029 + E036) · combinations carry part (with the C6 disclosure)

- D +1.65 s (q95 +1.98), LOSS 5/5. G −2.31 s (58 %). All rows: −2.41 vs E029, +1.17 vs E033 (better than rung B on all rows, worse on normal taxis).
- Missed: expected D +0.1 to +1.4; Advisor P(carries) 0.60.

### E038 · H027 v2 · LightGBM twin (subsampling 0.8/0.8, seed 42)

- Dev mean 442.03 (E029 442.46); −0.42 s all rows. Residual correlation with E029 0.977–0.980 on normal taxis; RMS disagreement 46 s. 909 s (no speed-up).

### E039 · H028 v2 · rung A (E029 + twin) · the twin does not reproduce the gain

- D +2.43 s (q95 +2.99), LOSS 4/5 (W1 TIE). **Averaging floor at seed 42: G −1.53 s** (39 %), larger than expected (−0.2 to −1.2). Not evidence about learner families.

### Batch conclusion (bounded, H024 v2 §Batch; C5)

At equal weight, neither the codes CatBoost, nor the per-key CatBoost, nor a perturbation twin of E029 substitutes for E031 in the blend. Each rung keeps 39–66 % of E033's gain on normal taxis; the remainder needs E031's configuration, and the complexity-4 combinations are where E031's accuracy comes from (E036 values, with the closed-set disclosure). E033's performance claim was not under test. The Day 5 reading "this CatBoost configuration as a whole" survives; no family claim is made or widened.

## Day 6 (D06-S01), batch 2: champion draw-robustness (X-D06-S01-0003; controls, no candidate)

ACCEPT ×2 with conditions N1–N8. Run at once on the owner's instruction ("No, run now.", INC-0012 amendment) by direct `run_experiment.py` calls. Freeze diff empty.

### E040 · H029 v1 · seed-42 GPU refit of E031 · pure fixed-seed re-draw

- Not byte-identical; resolved parameters identical on every fold. Dev mean 440.97 (E031 440.76). Largest development-fold change +0.84 s (W1). S1 reproduced to floating point (max 5.7e-7 s); other folds RMS change 21–33 s.
- CatBoost-alone three-draw spread (E031, E032, E040): up to 1.06 s (R1) and 1.57 s (W1). 1,497 s, 7.13 GB (within CLASS-M as well).

### E041 · H030 v1 · E033's construction on E040 · robust to one further fixed-seed (GPU-only) draw

- Against E026: criteria 1–3 pass, −5.52 s (q95 −4.67), 7/7 WIN. Against E033: |Δ| ≤ 0.40 s on every development fold.
- Blend three-draw spread (E033, E034, E041): ≤ 0.60 s (W1). All three draws keep 7/7 WIN against E026.
- Not the Day 7 SUBMIT draw (N4; the SUBMIT fit trains on 12 months). Low-power test by design (review finding 3).

### X-D06-S01-0004 · Day 6 phase close · ACCEPT (0.84); holdout closed unused (ruling H6); E033 remains champion

- **The decisions stand.** No Day 6 result contradicts the Day 5 promotion; all three blend draws meet criteria 1–3 against E026 with 7/7 WIN (−5.62, −5.54, −5.52 s). Neither Day 6 batch had real power against the performance claim; the SUBMIT procedure and D3-C3 were not attacked.
- **Ruling H6:** "Day 6: 0 of 1, closed unused" (no comparison; not a TIE). No `holdout_check.py` with E035–E041 as NEW, in any phase.
- **Standing rule 14** (several draws of a stochastic reference: report the point contrast against each draw; disclosure only).
- **Appended corrections to the Day 6 entries above (D6-C6 to D6-C10; the entries themselves are unchanged):**
  - **D6-C6:** rung B is at its threshold and depends on the draw: D +1.07 s against E034, **+0.97 s against E041**, +1.13 s against the three-draw mean. Rungs A and C hold against every draw.
  - **D6-C7 / D6-C8:** "statistics" and "combinations" are not separated from `data_partition` (FeatureParallel appears only at complexity 4). "The complexity-4 combinations are where E031's accuracy comes from" (batch conclusion) is withdrawn: the E036 values are only *consistent with* it. Day 5 finding 1 is read "as CatBoost resolves the configuration, `data_partition` included".
  - **D6-C9:** "the remainder needs E031's configuration" is withdrawn; the batch conclusion is the pre-registered non-substitution sentence only.
  - **D6-C10:** rung C against rung B on all rows (−0.64 s) is exploratory.
  - **D6-C11:** clause 1's W1 gain on normal taxis by draw: −1.59, −0.31, +0.40 s (spread 2.00 s); 69 % of E033's W1 gain sits outside normal taxis. Updates D5-C9.
- **Incidents:** INC-0012 and INC-0013 closed; INC-0009 (W&B: E036–E039 never mirrored, D6-C13), INC-0010, INC-0004 open.

## Day 7 (D07-S01): the SUBMIT procedure (batch X-D07-S01-0001; procedure runs, no candidate)

ACCEPT ×3 (0.85, 0.83, 0.85) with conditions S1–S9. Owner window 21:00–22:00 CEST (INC-0014); pinned launcher; freeze diff empty. The champion's construction (E033) applied to the frozen final folds `SUBMIT_JAN` / `SUBMIT_JUL` (train 2025-01..12). No truth: nothing scored.

### E042 · H031 v1 · SUBMIT fit of E029's configuration (LightGBM half) · COMPLETE

- 279.7 s, 7.02 GB. Mean prediction JAN 1,062.7 s, JUL 1,002.8 s. W&B sync failed (INC-0009).

### E043 · H032 v1 · SUBMIT fit of E031's configuration (CatBoost GPU half; one draw) · COMPLETE

- 419.3 s, 7.69 GB, GPU peak 3,784 MiB. Route check against E042 PASS (0.0 s on 107 / 276 routed rows). Resolved parameters equal E031's (S5; `data_partition` FeatureParallel). W&B sync failed.

### E044 · H033 v1 · SUBMIT blend [E042, E043] 0.5/0.5 · COMPLETE; the submission

- `make_submission.py`: I1–I5 hold; 344,841 rows in the template's order and dtypes; nearest-integer rounding only (RMS 0.288 s). **Submission SHA-256 `d57ff7db7dfa34e13934aa524464ea13dbe9f5f904fae400a85f87e62c95af73`** (`research/day-07/submission/SUBMISSION_RECORD.json`).
- **No sanity flag.** January is close to two limits (0.219 % above 3,600 s, limit 0.25 %; mean 1,062.8 s, limit 1,070). Both halves agree on January's level. January 2026's delay inputs are near summer-peak levels (mean schedule delay 36.4 min; January 2025 30.0). D3-C3 rows (435 > 3 h, 92 > 5 h): none predicted above 3,600 s.
- **Missed:** "July's mean above January's" and both mean-prediction ranges (H031 §Batch, H033). Kept.
- The submission's accuracy is measured by no fold and not by H; it carries one CatBoost draw (S9).

## Day 7 (D07-S01), batch 2: the routing candidate (X-D07-S01-0002; H035 a candidate)

ACCEPT ×4 with U1–U10. Raised by the researcher from X-D03-S01-0003 (e) after the SUBMIT batch; the owner chose to test it and set the window (INC-0015). **U6 corrects the forward-risk wording** (the proposal's, the researcher's message to the owner and Day 3 (e)'s). **U7 pre-registers objection F:** only a WIN of the Day 7 holdout access promotes H035. Window 2026-10-04 00:00–01:00Z; freeze diff empty.

### E045 · H034 v1 · E020's configuration (laptop instance) · reproduces E020 exactly

- Per-fold RMSE equal to E020's to 0.0 s. 1,196 s (above its 1,100 s guard), 5.38 GB. Component; never NEW.

### E046 · H035 v1 · E033 with the LIRF NM-missing subgroup from E045 · development criteria met; objection F open

- Development mean **314.42** against E033's 438.87: −124.45 s (q95 −82.85), 7/7 WIN; only LIRF changes. The pre-registered derivation held to 0.05 s per fold.
- Criterion 4: tail-row share of the gain 1.003–1.127 on every development fold; non-subgroup rows unchanged. Criterion 8 rule: worst S1 +4,292 s (≤ +6,500) against E033 and E028.
- U8: recording-change break-even λ* 0.20–0.57; a convention-absent loss of 0.25–1.30 × the 2025 gain; W1 without row 183903219 −32.9 s; both ranking months' subgroup delay q90 above every 2025 month.
- **The development margin is not the submission's expected gain (U6).**

### E047 / E048 · reproductions · byte-identical / criterion 6 PASS

### E049, E050 · H036 / H037 · DEFERRED (572 s left against a 600 s guard); ALLOCATED; needed only if H035 is promoted

### X-D07-S01-0003 · Day 7 phase close · ACCEPT (0.85); holdout WIN; champion E033 → E046

- **Holdout (ruling H7; December 2025, E046 against E033, one access; the project's last H read):** WIN, −124.24 s (q10/q90 −190.37/−42.98). P2: E033's H RMSE reproduced exactly (369.1811742636602). **H035 promoted.** Objection F is resolved for December only; U6 stands.
- **P4 (pre-registered before the access):** E050's file is final only if E049/E050 complete, route-check, pass I1–I5 and leave no open or defect flag; otherwise E044's file (E033's procedure) is final.
- **Appended correction to the E046 entry above (D7-C7):** "both ranking months' subgroup delay q90 above every 2025 month" reads "January 2026 above every 2025 month; July 2026 at the 2025 maximum (July 2025, 14,939 s)".
- E049/E050: owner's word pending (INC-0016).
