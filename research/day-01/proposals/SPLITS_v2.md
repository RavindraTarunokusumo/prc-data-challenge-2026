---
schema: split-freeze-proposal-v1
proposal_id: SPLITS
proposal_version: 2
parent_review: research/day-01/advisor/SPLITS_review_v1.md
day: 1
session: D01-S01
exchange_id: X-D01-S01-0002
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-09-27T12:20:00Z
---

# Split, metric and availability freeze — version 2

v1 received **REVISE** (`research/day-01/advisor/SPLITS_review_v1.md`, sha256
`f82eba5d45b0de1b1a9a173b2329b5383910c118154c7b83c102bc3c2f96e34e`, ack
`research/day-01/acks/SPLITS_ack_v1.md`). This version addresses R1–R6 and most of the
recommendations. After an ACCEPT, `scripts/gate.py freeze` hashes the files below into
`config/frozen.json`.

## Artifacts to freeze (pinned SHA-256)

| File | SHA-256 |
|---|---|
| `config/splits.yaml` | `4a5e97a116101846d1b20e88f08be983d2a9f0538008b51416371472a75e3db7` |
| `src/prc/__init__.py` | `284ffb4bae5b598969c711c2e8faf49a6c75e3e4e73b5aef1b1b3b564d0fdf2a` |
| `src/prc/metrics.py` | `13d5f90917b0756d57afb17c52108ed9dc03fd6a3b8a98af47eadf549e76dd89` |
| `src/prc/splits.py` | `9e380eee64e9474960b384836fff02bff4183e7d873ab99b286ab38fc7305c18` |
| `src/prc/evaluate.py` | `256a87ec3fad5b2cbdcc5dacf8b1390ce72ad0050d373262643b3da3101e9005` |
| `docs/methodology/DATASET_AUDIT.md` | `56b3b49dcc6bf102315ea574aa8dc8e3b68e07319383744a15c118274b0a13d3` |

Supporting, not frozen:
- `research/day-01/audit/regime_stats.json` (`c48ad51daf6687119b6744479e5ff765a4fa610e03845a7abb5b15e7d32e3366`, from `scripts/audit_regimes.py`, which excludes December);
- `scripts/gate.py` (`59ecadef4cce4cffffa46d4f231236a0aea68bf0dc31c551c99492e45784a4ef`);
- `src/prc/data.py` (`922f7b6d079ad37aa0fb38c45b712ab799e51875fb20083547462c79a8b5b032`);
- tests: 83 pass (`uv run pytest`), `uv run ruff check .` clean.

## Response to the required revisions

### R1: evaluation population pinned; frozen boundary closed
- **Silver and row counts are pinned.** `splits.yaml: evaluation_population` pins the silver SHA-256 (`efde4262…`) and the evaluation row count of every scored fold. `evaluate.py` loads silver **itself** from a path resolved relative to its own file. It verifies the SHA-256 once per process and verifies the row count on every truth read. It no longer accepts a caller-supplied frame.
- **The frozen modules are self-contained.**
  - `splits.py` resolves `config/splits.yaml` from its own location and imports no prc module.
  - `metrics.py` imports only `prc.splits`.
  - `evaluate.py` imports only `prc.metrics` and `prc.splits`.
  - `src/prc/__init__.py`, which runs on every `prc` import, is added to the frozen set.
  - `tests/test_isolation.py` asserts this import closure with an AST check.
- **`data.py` is outside the frozen boundary on purpose.** It feeds feature code, not the evaluator. Truth is read only by the frozen evaluator.

### R2: holdout guard
1. **Phase and limit.** The phase is no longer a caller string. `evaluate.holdout_compare(new_eid, ref_eid, reason)` takes it from `experiments/<new_eid>/gate.json` (`day`, written by `gate.py`). It requires both experiments to be COMPLETE in `experiments/ledger.jsonl`, and it enforces the frozen `max_access_per_phase` against the append-only task ledger.
2. **No per-row truth.**
   - `evaluate()` and `truth_frame()` refuse holdout and final folds.
   - The worker only *predicts* H and never scores it.
   - `holdout_compare` logs the access **before** reading truth. It returns only aggregate scores for both experiments, the paired dRMSE with its bootstrap interval, the outcome and the revert flag (tested).
3. **Scope stated plainly (DATASET_AUDIT §6.6).**
   - The pre-freeze audit and the v1 fold table read December's target distribution, and the v1 tests scored real December truth.
   - From the freeze onward:
     - `prc.data.load_silver` nulls December DEP targets by default. Only SUBMIT training may unmask them, and that is logged.
     - `audit_dataset.py` refuses to run.
     - The holdout tests use synthetic truth, and no test reads December targets.

### R3: noise-aware, binding promotion rule (`splits.yaml: promotion`, `metrics.promotion_check`)
- **Paired cluster bootstrap.**
  - dRMSE = RMSE(candidate) − RMSE(champion) on identical rows.
  - Clusters are airport × UTC day, with 2,000 resamples and seed 20260927.
  - Each fold's stream is seeded by the fold ID, so draws do not depend on which folds are passed (tested).
- **Fold outcome.** WIN if q0.90 of dRMSE < 0; LOSS if q0.10 > 0; otherwise TIE.
- **Criterion 1.** The mean dRMSE over the development folds must be ≤ −1.0 s **and** its q0.95 must be < 0. Folds are resampled independently. The 1.0 s minimum is set at the tail-only sensitivity measured in the review (0.75–1.62 s), and the bootstrap interval carries the tail variability, because disruptions cluster in airport-days.
- **Criterion 2.** At least 3 of 5 development folds must WIN, S1 must WIN, and no development fold may be LOSS. An S1 or W1 WIN counts only if its causal twin is not LOSS (R5).
- **Criterion 3.** No airport may be more than 3 % worse on pooled development-fold rows. Per-airport bulk (y < 3,600 s) deltas are reported as a diagnostic.
- **Reproduction (criterion 6).**
  - A gate-allocated `reproduction` run uses seed 43, with everything else identical.
  - Every development-fold RMSE must be within 1.0 s of the primary run.
  - Criteria 1–3 must also hold for the reproduction against the champion.
  - For deterministic Tier 0 models the seed has no effect, so the reproduction checks pipeline determinism.
- **Binding.** `promotion_check(candidate, champion)` has no overridable parameters. It reads everything from the frozen config and requires every development fold and causal twin. `evaluate.compare(cand_eid, champ_eid)` builds its inputs from the stored predictions, whose hashes it checks against each experiment manifest.

### R4: winter in model selection. Both options are adopted.
- **A winter development fold.** **W1** validates Feb 2025 (143,732 rows). It trains on Jan 2025 + Apr–Nov 2025 with March embargoed, mirroring S1.
- **Why February, justified with training data.** The evidence is in `regime_stats.json`, which excludes December; the audit's §6.5 has the details.
  - Jan–Feb 2025 has a heavier upper tail than the v1 development months at 5 of 10 airports (p90 up to +253 s at EDDM).
  - It holds 12 of the 21 disrupted airport-days of Jan–Nov.
  - January itself cannot be validated without leaving no prior training data, and **only February leaves Jan 2025 as a winter training month before validation**. That is closest to the real Jan 2026 situation, where the model has seen the previous winter.
- **Pre-registered decision use of H** (`splits.yaml: phase_close`).
  - At each phase close, one access compares the phase-closing champion with the phase-opening champion on H (on Day 1, with the global-mean baseline), using the same paired bootstrap.
  - LOSS means the phase's promotions are reverted and the phase-opening champion is restored.
  - WIN or TIE means the promotions stand.

### R5: S1 forward exposure controlled
- **Evidence recorded** (DATASET_AUDIT §6.5), with a new finding. The LFPG 27R/09L configuration of Aug–Nov 2025 is **temporary**. Both ranking months use the Jan–Jun layout again (27L 29.5 % in Jan 2026 and 20.4 % in Jul 2026, 27R ≤ 0.1 %). S1's post-validation months therefore teach a regime that is absent at test time.
- **Control, frozen now.** The diagnostic causal twins are **S1c** (Jul 2025, trained on Jan–Jun only) and **W1c** (Feb 2025, trained on Jan only). They are not promotion folds, but an S1 or W1 WIN counts only if its twin is not LOSS (criterion 2). The rule applies to **every** hypothesis, not only to regime-sensitive ones, because the worker scores all seven folds.

### R6: availability labels usable (DATASET_AUDIT §6.2)
1. **Two reference instants.** Labels are defined against the row's own off-block time *t_off* and its takeoff *t_to*:
   - **P**: known at or before *t_off*;
   - **T**: known in (*t_off*, *t_to*], which includes the row's own takeoff and everything during its own taxi interval;
   - **F**: known after *t_to*.

   A feature takes its latest input label. *t_off* is proxied by `AOBT_3` → `EOBT_1` → `SCHED` for labelling. The causal-only variant is then definable as P-only. Example: `MVT − AOBT_3` is T.
2. **Cross-month information (Jan ↔ Jul 2026) is inadmissible.** This is enforced structurally by splitting the final fold into `SUBMIT_JAN` and `SUBMIT_JUL`, each containing one ranking month.

## Recommendations adopted
- **Import-isolation test.** `tests/test_isolation.py` forbids `prc.data`, `prc.evaluate`, `eval_rows`, `truth_frame` and `load_silver` in `features.py` and `models/*`.
- **Gate hash.** The `gate.py` SHA-256 is recorded in every allocation record (`gate_sha256`).
- **Holdout experiment verification.** Holdout experiment IDs are verified against the ledger and gate record.
- **Bulk diagnostic.** Per-airport RMSE on rows with y < 3,600 s (`by_airport_bulk` in every score, plus the bulk deltas in `promotion_check`).
- **Identifier wording.** Identifiers are join keys only, and the ordering claim is softened (§6.2).
- **Nits.** The traffic-tercile comparability caveat is documented in `metrics.py`. The envelope is now written after this proposal.

Deferred, not required: the target-free covariate comparison of ranking vs training by airport-month. It is planned as Day 2 infrastructure.

## Fold table (v2)

| Fold | Role | Train months | Validation | Eval rows |
|---|---|---|---|---|
| R1 | development, rolling | 01…08 | 2025-09 | 183,950 |
| R2 | development, rolling | 01…09 | 2025-10 | 185,674 |
| R3 | development, rolling | 01…10 | 2025-11 | 162,332 |
| S1 | development, seasonal | 01…06, 09…11 (08 embargoed) | 2025-07 | 190,713 |
| W1 | development, winter | 01, 04…11 (03 embargoed) | 2025-02 | 143,732 |
| S1c | diagnostic twin of S1 | 01…06 | 2025-07 | 190,713 |
| W1c | diagnostic twin of W1 | 01 | 2025-02 | 143,732 |
| H | protected holdout | 01…11 | 2025-12 | 165,677 |
| SUBMIT_JAN / SUBMIT_JUL | final (no truth) | 2025-01…12 | 2026-01 / 2026-07 | 152,719 / 192,122 |

Development and diagnostic folds never contain December (tested).

## Resource Estimate

The evaluator verifies silver in about 0.6 s. One truth read takes < 1 s and < 2.5 GB, and the bootstrap over 7 folds takes < 10 s. That is CLASS-S. Each experiment now scores 7 folds instead of 4, about 1.75× the per-experiment cost measured in calibration.

## Decision Requested From Advisor

ACCEPT | REVISE | REJECT
