# E018 — H014 v2 (LightGBM on FS0, no random component), M1 reference · COMPLETE

**Run.** 420.0 s, peak 3.723 GB, CLASS-M, `within_class: true`.
- Preconditions (a)–(e) of `H014_review_v2.md` held:
  - H013 v2 ACCEPT and its ack were committed;
  - E017 ran with exactly the authorized configuration (checked in its `config.yaml`);
  - H014 v2 is H013's M1 reference;
  - E017 was COMPLETE with clause 1 not met;
  - the code was unchanged, and nothing ran concurrently.
- The config is E017's with `feature_set: FS0` and `hypothesis_id: H014`.

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| E018 | 376.92 | 274.87 | 316.21 | 532.43 | 404.34 | 546.51 | 421.50 | **380.95** |
| E006 | 375.3 | 277.8 | 306.2 | 524.5 | 405.5 | — | — | 377.87 |

- Inside the predicted 370–390 s.
- **The effect of removing randomness on FS0** (`E018_vs_E006.json`, reported): mean +3.08 s (q95 +7.29). The analogous effect on FS1 (E017 − E012) is +2.67 s.

## H013 v2 clauses 2(a) and 2(b)

**Clause 2(a)** (`E017_vs_E018_mech_NM_present_excl_LIRF.json`): not met.
- Mean **−7.27 s** (q95 −6.49); criteria 1 and 2 True.
- Development folds R1 −7.19, R2 −6.40, R3 −6.54, S1 −7.44 and W1 −8.80, all WIN. S1c −4.61 WIN; **W1c +5.15 LOSS**, which voids the W1 WIN, leaving 4 counted WINs.
- Predicted: mean −4 to −15 s, ≥ 3 counted WINs including S1. **Met.**
- No row concentration (|top-1| ≤ 0.11).

**Clause 2(b)** (`E017_vs_E018_mech_NM_present.json`): not met. NM-present bulk dRMSE is −10.69, −10.35, −9.01, −16.40 and −10.11 s, all < 0.

**Replication of M1.** Deterministic −7.27 s against bagged −7.16 s (E012 − E006 on the same population), with the same W1c LOSS. The static-structure effect does not depend on the training procedure.

**All rows** (`E017_vs_E018.json`, reported): mean −2.13 s (q95 +13.09), dominated by LIRF convention rows, as for E012 − E006.
