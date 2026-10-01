---
schema: governance-request-v1
request_id: LAPTOP_REFS
proposal_version: 2
day: 5
session: D05-S04
exchange_id: X-D05-S04-0002
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-10-01T19:55:16Z
---

# Request LAPTOP_REFS v2: laptop instances, a route-integrity reference the laptop can meet, and the environment they hold in

Batch X-D05-S04-0002 (with H021 v2, H022 v2 and H023 v2). This is a governance request, not a hypothesis.

## Changes from v1 (review `LAPTOP_REFS_review_v1.md`, REVISE 0.90; ack with corrections D5-C1 to D5-C6)

| Revision | v2 |
|---|---|
| 1. E028 in route integrity | **E028 is removed from route integrity.** The reference is **E029's routed rows**, at 1e-6 s. Committed target-free evidence shows a correctly routed run on the candidates' paths meets it (below). The criterion 8 expectation against E028 is restated as non-zero |
| 2. Premises | Replaced with the facts: CPython 3.13.15; lock `efa4fd78…` (E027–E029) or `39df945c…` (E026); numpy 2.5.3, scipy 1.18.1, xgboost 3.4.1; against the cloud's 3.11.15, 2.4.6, 1.17.1, 3.2.0. **The cause of the routed-row difference is now established, target-free** (below) |
| 3. Where the differences sit | Stated, twin folds included (table below) |
| 4. Environment validity | Item 6 below: the binding environment, the events that end it, and per-run recording |
| 5. Ratification | **E026** is E019's instance (hand-off scope; no ratification needed). **Ratification is requested for E029** (contrary to H018 v2 item 9) **and for E028** in its reduced role. E027 is byte-identical to E026 and is used only for its learning curves |
| 6. Boundary disclosure | Item 4 below: every statistic decided against an instance, with a margin per instance |
| 7. Operational records | INC-0010 (swap kept at 4 GB; CPython 3.13 kept: owner decisions); appended corrections in STATE.md, the D05-S04 session record, and the E026, E028 and E029 analyses (commit `9dac3fc`) |

## Facts

**Where the instance differences sit** (instance minus original, committed `metrics.json`; Advisor-verified):

| | Fold-level, development | Twin folds | Non-LIRF airports | LIRF |
|---|---|---|---|---|
| E026 (≡ E027) − E019 | ≤ 0.0072 s | S1c −0.0001, W1c +0.0003 | **0 exactly** at all nine, all 7 scored folds | ≤ 0.0276 s (S1) |
| E029 − E023 | ≤ 0.0072 s | as E026 (to 1e-5) | **0 exactly** | as E026 |
| E028 − E005 | ≤ 0.0113 s | **W1c +0.339 s** | differs everywhere (LTFM +1.94 s on W1c) | differs |

- The routed rows of E026, E027 and E029 are bit-identical to each other on all 8 folds.
- They differ from E028's on every routed row, by up to 190.9 s (R3).

**Cause (established target-free; `scripts/diag_ridge_paths.py`, `research/day-05/eda/ridge_paths.json` and `ridge_paths_polars4.json`).**

- **Method.** R3, permuted training target (no metric). E005's ridge is fitted on the frames of each code path, and the ridge's design matrix and target are hashed at `Ridge.fit`.
- **Default polars thread pool (16 on the laptop):**
  - **Frame values:** the FS0 columns of `fs0(view)`, `fs2(view)` and `fs2_raw(view)` are **value-equal** (`DataFrame.equals`).
  - **Ridge inputs:** the design matrix's sparsity pattern and target are identical, but its **values differ** between `fs0` (standalone ridge: E005, E028) and `fs2`/`fs2_raw` (routed path).
  - **Predictions:** they differ by up to 0.022 s on this permuted target. `fs2` and `fs2_raw` give **identical** design matrices.
  - **Ruled out:** refitting `fs0` is bit-identical, and a LightGBM fit earlier in the same process changes nothing (`fs0_after_lgb`, `fs2_after_lgb`).
- **`POLARS_MAX_THREADS=4`** (the cloud's vCPU count): **all paths are bit-identical.** The 4-thread design matrix differs from the 16-thread one.
- **Reading.**
  - The ridge's fitted statistics (quantiles, median, mean, std; `prc.models.linear`) are computed by polars. Their summation order depends on the thread pool and the frame's chunk layout, and `fs2`'s joined frame is laid out differently from `fs0`'s.
  - The last-bit differences pass into the standardized design. scikit-learn's `sparse_cg` (tol 1e-4) on that ill-conditioned design amplifies them on poorly determined directions, so up to 190.9 s on single routed rows with the real target.
  - On the 4-vCPU cloud, the paths agreed.
  - **Whether a 4-thread laptop run reproduces the cloud's bits is untested** (numpy and scipy differ too). It is not requested here.

## Requested ruling (rule L, v2)

1. **Instances.** In the environment of item 6:
   - **E026 is E019's instance** (allocated under the hand-off procedure). E027 is byte-identical to E026 on all 8 files and may be cited for its curves only.
   - **E029 is E023's instance.**
   - **E028 is E005's instance only** for the criterion 8 statistic, B3 where E005 is the comparator, and reported comparisons against E005. It is never a route-integrity reference.
2. **Identity and restrictions** (v1 item 2, accepted).
   - E019 stays the champion of record.
   - E026, E027, E028 and E029 are never NEW and never candidates. E029 carries E023's restrictions: rules 9 and 10, and the hand-off base ruling (the matched reference for `route_train_exclude` candidates on FS2).
3. **E029's configuration inside a new blend** (v1 item 3, accepted): rule 10 is not engaged.
4. **Boundary disclosure, per statistic and per instance.** A statistic decided against an instance is flagged "instance-sensitive" if its value lies within the instance's margin of its threshold. It is decided as computed; the flag is disclosure.

| Statistic | Threshold | Margin vs E026 / E029 | Margin vs E028 |
|---|---|---|---|
| Fold outcome (deciding q10 or q90) | 0 | 0.02 s | 0.35 s |
| Criterion 1: point; q95 | −1.0 s; 0 | 0.02 s | 0.35 s |
| Criterion 3: airport RMSE ratio | 1.03 | LIRF only: 0.0001 (relative); other airports 0 | 0.01 (relative) |
| Criterion 8: `NM_missing_LIRF` bulk dRMSE | +6,500 s | n/a | 200 s |
| B3: S1c point dRMSE | 0 | 0.02 s | 0.35 s |
| H018 v2 clause 2 (`NM_missing_other` bulk; no LIRF rows) | 0 | **0** (the population excludes LIRF, where the differences sit) | n/a |
| Rule 12 counts (`NM_missing_other`) | the H018 limit 50 | 0 | n/a |

5. **Holdout reference side** (v1 item 5, accepted): E026's H file.
   - It equals E027's, and differs from E019's only on the 88 routed rows (the mechanism above).
6. **Environment of validity.** The instances, the route-integrity reference and every run of the H021–H023 chain hold in **one environment**:
   - CPython 3.13.15, lock `efa4fd78…` (E026 ran on `39df945c…`, but is byte-identical to E027 on `efa4fd78…`);
   - polars 1.44.2 with its **default thread pool (16; `POLARS_MAX_THREADS` unset)**;
   - numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, LightGBM 4.7.0, CatBoost 1.2.10;
   - this host (WSL2, 11 GB, 4 GB swap per INC-0010).

   **Ending events:** any change to the interpreter, the lock, a library build, the polars thread pool or the host, and any fix to the ridge path. Every chain run records its interpreter and polars thread count in its manifest (`python`, `polars_threads`; `prc.worker`). A run whose record differs from item 6 is not compared against the instances without a new ruling.
7. **Route integrity on the laptop.**
   - The reference is **E029's prediction files on the routed rows**, at **1e-6 s**: `route_check.py <X> - E029`.
   - The evidence that a correctly routed run meets it: `fs2_raw`'s ridge design matrix is bit-identical to `fs2`'s (above), and E029 = E026 on every routed row. So a correctly routed CatBoost run on FS2_RAW gives E029's routed rows exactly.
   - **E029 is not a route-integrity reference for frames other than FS2 or FS2_RAW.**

## Ratification requested

| Run | Outside scope because | Use requested |
|---|---|---|
| **E029** | contrary to H018 v2 review item 9 (D5-C5) | E023's instance (item 1), H023's LightGBM component, the route-integrity reference (item 7) |
| **E028** | beyond H004 v1's single conditional reproduction | the reduced role in item 1 |
| E027 | a second laptop reproduction of H015 v2 | curves only (no decision rests on it) |

The researcher allocated these believing the hand-off covered them. From now on, any allocation beyond a review's stated scope is requested in a proposal first (D5-C5).

## Alternatives considered

- **Set `POLARS_MAX_THREADS=4` for the chain.** That could make the paths agree, and might restore cloud bit-identity. But it changes the environment of every instance, needs a new laptop reproduction of each reference (more allocations outside scope), and its cloud bit-identity is untested. Not requested now. It is named for Day 7, where submission reproducibility matters.
- **Edit manifests:** refused (v1). **Compare metrics only:** refused (v1).

## Decision Requested From Advisor

ACCEPT (adopt rule L v2 and the ratifications), or REVISE.
