# E052 analysis: H038 v2 reproduction of E051 (seed 43)

- **COMPLETE:** started 2026-10-06T23:06:56Z, ended 23:10:49Z. `mixture_check.py E052 E046`: PASS on all 8 folds.
- **Criterion 6: PASS.** `reproduce_check.py E052 E051 --champion E046` gives an RMSE difference of 0.0 on every development fold.
  - The prediction and component files are byte-identical to E051's: component SHA-256s are equal fold by fold, and `cmp` finds S1's prediction files identical.
  - LightGBM is deterministic here and the seed is unused (a determinism check, as D3-C4).
- **It reproduces E051's criteria outcomes:** criterion 1 and 3 met, criterion 2 not met. See `experiments/E051/analysis.md`.
- Day 8–12 look 2. W&B sync failed (INC-0009).
- Disclosures: as E051 (INC-0017, INC-0020).
