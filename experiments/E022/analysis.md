# E022 analysis: H015 v2 reproduction (seed 43)

**Criterion 6: PASS. The prediction files are byte-identical to E019 on all 8 folds.**

## Run

| Item | Value |
|---|---|
| Configuration | E019's exactly, with `purpose: reproduction` and `seed: 43` (Validation Plan step 4; allocated only after clauses 1–4 were all found not met) |
| Status | COMPLETE: 1,339.1 s, peak RSS 4.63 GB (CLASS-M: within class) |

**Provenance (item 8).**
- **CPU:** Intel(R) Xeon(R) Processor @ 2.10GHz.
- **Container restart since E021: no.**
- **Relative to E019, the primary it reproduces: cross-container.** The container restarted after E019.
- **INC-0004** open.

## Criterion 6 (`reproduce_check.py E022 E019 --champion E005`)

- **Every development-fold RMSE equals E019's:** difference 0.0 s on every fold, against a 1.0 s tolerance. `within_tolerance: true`.
- **Criteria 1–3 against E005 hold on the reproduction:** criterion 1, criterion 2 and criterion 3 all true, with a WIN on all 7 folds. `criteria_hold: true`, `passes: true`.

## Prediction-file SHA-256 (Missing Control 2)

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | H |
|---|---|---|---|---|---|---|---|---|
| E022 = E019 | yes | yes | yes | yes | yes | yes | yes | yes |

- **The determinism premise holds on real data,** across a seed change (42 → 43) and across container instances. The seed has no effect on the deterministic procedure: `bagging_fraction` 1.0, `feature_fraction` 1.0, and `bin_construct_sample_cnt` 5,000,000 above every fold's training size.
- This closes Missing Control 2 and the Day 2 open question ("its real-data determinism is untested").
