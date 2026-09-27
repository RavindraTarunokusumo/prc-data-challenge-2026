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
