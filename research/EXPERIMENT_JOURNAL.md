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
