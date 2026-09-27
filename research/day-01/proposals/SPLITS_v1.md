---
schema: split-freeze-proposal-v1
proposal_id: SPLITS
proposal_version: 1
day: 1
session: D01-S01
exchange_id: X-D01-S01-0001
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-09-27T11:07:30Z
---

# Split, metric and availability freeze (Day 1)

## Request

Freeze the validation design, the metric and the prediction-time availability definition
(brief §9, DATA_POLICY §4–§6, §10). After an ACCEPT, `scripts/gate.py freeze` hashes the
files below into `config/frozen.json`. From then on every experiment allocation verifies
them, and any later change needs an incident record.

## Artifacts to freeze (pinned SHA-256)

| File | SHA-256 |
|---|---|
| `config/splits.yaml` | `fe92f496f946982595f4945735310f805963543453723532fc168b525103def0` |
| `src/prc/metrics.py` | `89587901cc57d674ec6b54309c04fe95b4e911673859c23fc51077034c34a470` |
| `src/prc/splits.py` | `4a701a608f0f5af9f94120654d51b1f962d99da8563b8c25de52e0140a848592` |
| `src/prc/evaluate.py` | `bcc46d7e40d5932cd2e89774860ce33d082d19cc65bc059d14be04d61a7398ef` |
| `docs/methodology/DATASET_AUDIT.md` | `af1d2c9b4292be3feffc5804f3d61f5bc575efeb0899a644a4996749477b5456` |

Supporting evidence (not frozen): `research/day-01/audit/audit_stats.json`
(`4ac6b0d39b2e0817dbc79898e37665ce701e944cfcb4b5c444396ff97f7881c3`), produced by
`scripts/audit_dataset.py`; `data/manifests/silver_manifest.json`
(`c999f26c2e078d1e4e3588413ec98211b851115f1808635b0fad22f871bfd9a4`), produced by
`scripts/build_silver.py`; tests `tests/test_{metrics,splits,masking,evaluator,gate}.py`
(35 pass).

## 1. Availability definition (DATASET_AUDIT §6)

The ranking file is a retrospective snapshot. It gives each scored DEP row its **actual
takeoff time** and withholds only its block time and target. No wall-clock prediction
instant reproduces this information set, so admissibility is defined by the information
set itself. It covers all 2025 training data plus every ranking column except the two
blanked DEP columns. Identifiers (`MVT_ID_mvt`, `FLIGHT_ID_mvt`) are excluded as features.
Cross-row features carry a mandatory **backward / forward / static** label, and forward
(post-takeoff) information is admissible but must be declared.

Key evidence the Advisor should check:
- `AOBT_3_flt` is admissible and is not a copy of the withheld off-block time. `MVT − AOBT_3` has RMSE 384.9 s against the target (constant: 546.4 s). `BLOCK − AOBT_3` has IQR −122…+183 s and is minute-rounded in 97.7 % of rows.
- `MVT_ID_mvt` follows schedule order and encodes no off-block order (the rank-gap correlation with the target is −0.008).

## 2. Masking protocol (DATASET_AUDIT §6.4, `splits.masked_view`)

Model code receives only `masked_view(fold)` and `train_targets(fold)`:
- training months are complete;
- in validation months, DEP block time and target are nulled and ARR rows are untouched (as in ranking);
- all other months are absent.

Only `evaluate.py` reads validation truth (`eval_rows`). `tests/test_masking.py` checks
the protocol on real silver data for every fold.

## 3. Folds (`config/splits.yaml`)

| Fold | Kind | Train months | Validation | Eval DEP rows | Target std (s) |
|---|---|---|---|---|---|
| R1 | rolling | 2025-01…08 | 2025-09 | 183,950 | 560.3 |
| R2 | rolling | 2025-01…09 | 2025-10 | 185,674 | 437.1 |
| R3 | rolling | 2025-01…10 | 2025-11 | 162,332 | 532.0 |
| S1 | seasonal | 2025-01…06 + 09…11 (08 embargoed) | 2025-07 | 190,713 | 745.0 |
| H | protected holdout | 2025-01…11 | 2025-12 | 165,677 | 514.7 |
| SUBMIT | final (no truth) | 2025-01…12 | 2026-01, 2026-07 | 344,841 | — |

Rationale:
- **R1–R3** are expanding-window folds with no gap, the analogue of Jan 2026, which directly follows the training year.
- **S1** is the analogue of Jul 2026: it validates on the peak-summer month and trains on the rest of the development year. The brief's example allows training months after the validation month. August is embargoed so that no training month directly follows the validation month, which removes the most persistent post-validation operational regimes (such as a runway closure spanning Jul–Aug). The alternative, training on Jan–Jun only, would remove future months entirely, but the model would then never see IATA-summer data after June. I chose the brief's pattern. The Advisor should weigh this.
- **H = December** is the winter month adjacent to the Jan 2026 test. It is never used by development folds (enforced by test). It is accessed at most once per phase, and each access is logged by the evaluator guard.

Known limitation (DATASET_AUDIT §6.5): no 2025 fold reproduces the Jul 2026 situation, where the training data is 6 months old and a prior-year same-season month exists.

## 4. Metric (`src/prc/metrics.py`)

- RMSE in seconds over **all** DEP rows of the fold (DATA_POLICY §10), with no clipping. The tail matters: the top 0.1 % of rows contribute 46.6 % of the SSE of a constant model. This is deliberate, because the competition metric is plain RMSE.
- Segment reports: airport, month, traffic regime (per-airport terciles of the count of same-hour DEP takeoffs, counted over the evaluation population), wake category (`UNK` for missing), and taxi-time band on the true target (edges 300/600/900/1200/1800/3600 s).
- Promotion (brief §10, items 1–3) is implemented in `promotion_check`:
  1. "overall RMSE improves" means the **mean of the four development-fold RMSEs** decreases;
  2. the candidate wins on ≥ 3 of 4 folds, and S1 must be one of them;
  3. no airport's RMSE, pooled over the development folds' rows, degrades by more than +3 %.
- Reproduction tolerance: 1.0 s RMSE (`splits.yaml: promotion`).

## 5. Enforcement

- `scripts/gate.py freeze` writes `config/frozen.json` only if this proposal's review is ACCEPT, the ack references both hashes, and every frozen file matches a hash pinned above. Freezing can happen only once.
- `gate.py allocate` refuses to allocate if a frozen file or the Advisor definition hash changed.
- The evaluator requires explicit holdout metadata, logs every access and refuses a second access in the same phase.

## 6. Leakage review requested

1. Is the snapshot-based availability definition faithful to the competition, and are the labelling rules for forward features sufficient?
2. Is S1's use of post-validation months (Sep–Nov, with Aug embargoed) acceptable?
3. Is the masking protocol complete? In particular, ARR rows of validation months stay visible. They carry taxi-in and in-block times, exactly as in the ranking file.
4. Are there any gaps in the evaluator or gate that would let model code see validation truth?

## Resource Estimate

Evaluation of one fold takes < 5 s and < 2 GB (CLASS-S). No experiment is requested.

## Decision Requested From Advisor

ACCEPT | REVISE | REJECT
