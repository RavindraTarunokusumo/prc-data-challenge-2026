# E027 analysis: H015 v2 reproduction with learning curves (champion curve)

**PASS. Byte-identical to E026 on all 8 prediction files**, so the curve recording does not change training on real data. The development folds are within 0.008 s of E019 (as E026).

| Item | Value |
|---|---|
| Purpose | the champion configuration's learning curve (owner request, INC-0009 addendum), and a real-data check that recording leaves the model unchanged |
| Config | identical to E022/E026 (E019's configuration, seed 43, `num_threads: 4`) |
| Status | COMPLETE: **892.0 s** (E026 668.7 s; recording costs +33 %), peak RSS 5.19 GB, CLASS-M within class |
| Curves | `curves.json`: training RMSE per iteration (all 8 folds), validation RMSE every 10 iterations (7 scored folds; **none for H**). The last stage equals the evaluator's RMSE within 4e-12 s on every scored fold |
| W&B | run E027: 101 history points, `iteration` 1 → 1000 |

## What the curves show (observation; nothing is selected from them)

| Fold | train RMSE it 1 → 1000 | val RMSE it 1 | val min (iteration) | val at 1000 | 1000 − min |
|---|---|---|---|---|---|
| R1 | 547.6 → 214.8 | 544.1 | 446.24 (830) | 446.40 | +0.16 |
| R2 | 546.8 → 211.2 | 421.6 | 274.46 (920) | 274.49 | +0.03 |
| R3 | 535.1 → 208.3 | 518.0 | 396.86 (560) | 397.25 | +0.39 |
| S1 | 507.4 → 195.2 | 729.2 | 631.31 (520) | 632.09 | +0.78 |
| W1 | 534.1 → 207.0 | 614.5 | 472.00 (900) | 472.22 | +0.22 |
| S1c | 513.2 → 202.1 | 728.9 | 636.70 (290) | 638.38 | +1.68 |
| W1c | 593.2 → 243.6 | 614.0 | 483.67 (180) | 488.59 | +4.92 |

- **The development-fold validation curves are flat from about 500 iterations.** The fixed 1,000 rounds sit within 0.03–0.78 s of each fold's minimum: there is no material overfitting in the rounds, and no material gain from more rounds.
- **The diagnostic folds with less training data overfit sooner.** W1c trains on one month: its minimum is at 180, and it gives back 4.9 s by 1,000.
- **The train–validation gap is large** (train about 200 s against validation 270–630 s). The training loss keeps falling while validation is flat, which fits a heavy-tailed target whose tail rows the model memorises without generalising.
- **Selection hazard (INC-0009 addendum).** These minima are taken on validation folds. Choosing `num_boost_round` from them would be validation-guided tuning. Nothing is chosen here; a proposal that uses this information must pre-register it.
