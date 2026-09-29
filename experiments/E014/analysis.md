# E014 — H012 v1 (LightGBM on FS1_NO_ANCHOR), M2 ablation · COMPLETE

**Run.** 861.4 s, peak 4.115 GB, CLASS-M, `within_class: true`. Preconditions 1(a)–(e) of `H012_review_v1.md` held at allocation:
- the H009 v3 ACCEPT and its ack were committed;
- FS1 and clause 4 were unchanged;
- E012 and E013 were COMPLETE;
- nothing else was running.

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| E014 | 383.62 | 293.34 | 357.19 | 567.77 | 465.06 | 572.09 | 508.69 | **413.40** |

| Development mean on NM-present rows | R1 | R2 | R3 | S1 | W1 | Mean |
|---|---|---|---|---|---|---|
| E014 | 271.0 | 270.5 | 275.6 | 380.6 | 331.9 | **305.9** |
| E012 | 237.8 | 233.9 | 216.5 | 336.8 | 248.1 | 254.6 |
| E013 | 242.3 | 242.2 | 224.2 | 342.0 | 261.1 | 262.4 |
| E006 | 249.0 | 246.7 | 226.1 | 338.2 | 258.9 | 263.8 |

Computed with the frozen evaluator's join, NM status from `AOBT_3_flt`.

The operative expectation was the NM-present range 300–350 s (`H012_ack_v1.md`), and 305.9 **met** it. The all-rows mean, 413.40, lies inside the implied 407–445 s and outside the proposal's inconsistent 430–480 s.

## Clause 4 of H009 v3 (`research/comparisons/E012_vs_E014_mech_NM_present.json`): not met, M2 supported

- H009 − H012 on NM-present rows: mean **−51.30 s** (q95 −47.49). Criteria 1 and 2 are True, **7/7 WIN** (predicted −40 to −100, 5/5 WIN).
- **Folds:** R1 −33.2, R2 −36.6, R3 −59.1, S1 −43.9, W1 −83.8, S1c −42.3, W1c −95.9.
- **Bulk:** −30 to −83 s on every fold.
- **Rule 6.** The pre-registered risk was that row 192622644 might carry ≥ 0.5 on S1 and S1c. It did not: top-1 shares are 0.16 (S1) and 0.11 (S1c), and ≤ 0.02 elsewhere. The flagged W1 exposure (183910286) did not materialise either (W1 top-1 0.02).
- **Reading.** The NM off-block anchor is the largest single mechanism in the model, worth about 51 s of NM-present RMSE beyond `d_sched` and the static keys. The loss is largest in winter (W1, W1c): the anchor matters most when off-block delays (de-icing, holds) are large.

## Rules 1, 6 and 7, all rows (`E012_vs_E014.json`): reported

- Mean −37.25 s (q95 −33.46), criteria 1–3 pass. Attribution only; H012 is not a candidate.
- Tail share 0.291, so the margin is mostly bulk. As expected, the anchor mechanism acts on taxi duration.
