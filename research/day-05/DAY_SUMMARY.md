# Day 5 summary: model architecture, CPU against GPU (DRAFT for the phase close X-D05-S05-0001)

**Sessions:** D05-S01 to D05-S05, on the owner's laptop. **Branch:** `day-5`.

**Provenance:**
- The researcher is `claude-opus-5-5` (`--effort high`). The Advisor is the fixed `advisor` subagent (definition `30fff5dd3c54`).
- **INC-0006** (delegation to `claude-sonnet-5-5` workers) was permitted but **not used**: no Day 5 work was delegated (§8).
- Environment and process incidents: INC-0007 (closed), INC-0008 (closed), INC-0009 (open), INC-0010 (open), INC-0011 (closed); INC-0004 remains open (§7).

## 1. The Day 5 question and its answer

**Question (brief §3, §11):** the model architecture day, CPU against GPU. Does a different learner family, or a combination of learners, improve on the champion's routed LightGBM?

**Answer: yes. A second learner family adds signal, and the equal-weight blend of the two meets every promotion criterion against the champion.**
- **CatBoost on GPU with categorical statistics on raw keys (H021, E031)** reaches a development mean of **440.76 s**. That beats the routed LightGBM with the same D3-C2 treatment (E029, 442.46 s) by −1.69 s on all rows, with an S1 WIN. **This was expected to lose** (+2 to +15 s; H020's Day 4 review expected worse).
- **Its categorical statistics are the reason** (H021 clause 1, final): against the same CatBoost with categorical columns as integer codes (H022, E030), it gains **−4.91 s** on `NM_present_excl_LIRF`, with 5/5 counted WINs. The GPU and seed re-draw (E032) moves this by +0.68 s, inside the 1.5 s noise limit.
- **The blend (H023, E033)** is a fixed 0.5/0.5 average of E029 and E031:
  - **438.87 s**; −3.58 s against E029 on all rows, and −3.96 s on normal taxis;
  - **against E019 (laptop instance E026): −5.62 s (q95 −4.79), WIN on all 7 folds, S1 included**, every airport improved;
  - **D3-C2 is treated** (> 3 h band 3, against E019's 81);
  - reproduced by E034 (within 0.48 s).
- **The single-row S1 constraint (D4-C9) did not bind.** The CatBoost half *raised* the prediction on row 192622644 (E031 10,976 s; blend 9,008 s; E019 8,136 s). The S1 WIN is not carried by the LIRF NM-present convention mixture (share 0.24).

## 2. What was built

| Artifact | Purpose |
|---|---|
| Laptop environment and data verification | Silver rebuilt byte-identical (`sessions/D05-S02/DATA_VERIFICATION.md`) |
| Experiment lock (`prc.paths.experiment_lock`) | One experiment at a time; real-silver tests and calibrations stand down (INC-0008) |
| W&B mirror (`prc.tracking`, `scripts/wandb_sync.py`) | Experiment records mirrored, with no holdout figures (INC-0009) |
| Learning curves (`prc.curves`, `curves.json`) | Train RMSE per iteration, and staged validation RMSE scored after training (no feedback; prediction-invariant; never H) |
| `FS2_RAW` | FS2 without the `__RARE__` collapse |
| `gbm.catboost` `cat_mode` ctr/codes; `resolved_params.json` | The matched categorical-handling contrast, and the parameter record |
| `prc.blending` | Fixed-weight blend of stored component predictions (outside `prc.models`; isolation-tested) |
| Runner records | GPU memory, GPU failure as RESOURCE_FAILURE, swap pages, start commit, environment (lock, libraries, thread variables, polars threads) |
| `scripts/calibrate_gpu.py`, `diag_ridge_paths.py`, `diag_cb_params.py` | GPU calibration; the laptop ridge-path diagnosis; the comparability evidence |
| Tests | 158 pass; ruff clean |

## 3. Advisor exchanges

| Exchange | Content | Decision |
|---|---|---|
| X-D05-S04-0001 | LAPTOP_REFS v1, H021 v1, H022 v1, H023 v1 | **REVISE ×4** (0.90, 0.90, 0.90, 0.93). The route-integrity reference E028 was unattainable on the laptop (D5-C4). Corrections D5-C1 to D5-C7 |
| X-D05-S04-0002 | v2 of all four | **LAPTOP_REFS ACCEPT** (0.88): rule L v2 and ratification of E027–E029. H021–H023 REVISE (closed comparability set, freeze anchor, reproduction integrity) |
| X-D05-S04-0003 | H021 v3, H022 v3, H023 v3 | **ACCEPT ×3** (0.88, 0.90, 0.88). CLASS-L for H021 justified |

## 4. Experiments (sequential, within class)

| E | Purpose | Model | Dev mean | Runtime / RAM | Result |
|---|---|---|---|---|---|
| E025 | H015 v2 reproduction | routed LightGBM | — | killed after R1 | **RESOURCE_FAILURE**: global OOM from a concurrent researcher pytest (INC-0008) |
| E026 | H015 v2 reproduction (hand-off) | routed LightGBM | 444.49 | 669 s / 5.22 GB | PASS (≤ 0.0072 s); **E019's laptop instance** |
| E027 | H015 v2 reproduction with curves | routed LightGBM | 444.49 | 892 s / 5.19 GB | byte-identical to E026; curves only (outside scope, ratified) |
| E028 | H004 v1 reproduction | ridge | 482.72 | 73 s / 3.50 GB | E005's instance, reduced role (outside scope, ratified) |
| E029 | H018 v2 reproduction | routed LightGBM, exclusion | 442.46 | 893 s / 6.60 GB | **E023's instance** (contrary to H018 v2 item 9; ratified) |
| E030 | H022 v3 | routed CatBoost GPU, codes | 446.50 | 225 s / 6.40 GB | Control; integrity holds |
| E031 | H021 v3 | routed CatBoost GPU, CTRs | **440.76** | 1,523 s / 7.01 GB | Clause 1 not met (mechanism supported); not a candidate |
| E032 | H021 v3 reproduction | as E031, seed 43 | 440.91 | 1,131 s / 7.08 GB | Noise m = +0.68 s; R1 1.0 s tolerance fails (+1.056) |
| E033 | **H023 v3** | blend 0.5 E029 + 0.5 E031 | **438.87** | 8 s / 3.38 GB | **Criteria 1–8 met against E019 (E026)** |
| E034 | H023 v3 reproduction | blend 0.5 E029 + 0.5 E032 | 438.95 | 7 s / 3.40 GB | Criterion 6 PASS |

No swap was used in any Day 5 run (INC-0010 records).

## 5. Champion

- **E019 is the phase-opening champion.** **H023 v3 (E033) meets criteria 1–8 against it** (E033 analysis), with promotion recommended.
- The champion change and the Day 5 holdout access (E033 as NEW, a Day 5 allocation; E026's H file as the reference, rule L v2 item 5) are requested in the phase close.

## 6. Findings

1. **CatBoost's categorical statistics carry signal at fixed capacity:** −4.91 s on normal taxis against integer codes (re-draw −4.23 s). `FloatTargetMeanValue` averages the raw target (Advisor-verified). The Day 4 H020 objections are answered.
2. **A second learner family beats the LightGBM alone on this problem** (E031 against E029: −1.69 s, S1 WIN). Its errors are partly decorrelated: residual correlation 0.84–0.92 on bulk rows, 0.94–0.99 on all rows.
3. **The blend is better than either half** (−3.58 s against E029, −1.89 s against E031 by development mean), and beats E019 by −5.62 s, the largest single-phase gain since Day 3.
4. **Symmetric trees do not bound day-scale predictions here.** Both CatBoost arms predict *higher* than the LightGBM on the two LIRF NM-present day-scale rows. The H020-era reasoning was wrong for them. It holds for the `NM_missing_other` out-of-range counts: the codes arm cuts the generic < 1 h band from 82 to 25.
5. **CPU against GPU (the brief's Day 5 theme):**
   - CatBoost on GPU is about 5× faster per iteration than on CPU, with full CTR combinations, which makes the Day 4 configuration feasible.
   - XGBoost on GPU is slower than CPU LightGBM.
   - LightGBM has no GPU build here.
   - **CatBoost on GPU is not deterministic:** an identical re-fit differs, and the seed-43 re-draw moved R1 by 1.06 s.
6. **Laptop reproducibility.**
   - Routed LightGBM runs equal their cloud originals exactly at the nine non-LIRF airports. The difference sits in LIRF's routed rows.
   - **Cause:** polars' thread pool (16 here, 4 on the cloud) changes the ridge's fitted statistics in the last bits, and `sparse_cg` (tol 1e-4) amplifies that on single routed rows.
7. **Learning curves:**
   - LightGBM's validation RMSE is flat from about 500 iterations, within 0.03–0.78 s of an oracle minimum on the development folds;
   - CatBoost is still improving at 1,000 (E031 −0.73 s over iterations 800–1,000).

   Nothing was tuned from the curves.

## 7. Missed or corrected predictions (kept)

| Prediction | Outcome |
|---|---|
| H021: CatBoost worse than E029 by +2 to +15 s; development mean 443–458 | **−1.69 s; 440.76: better** |
| H021 clause 1 central −12 s (−6 to −25) | **−4.91 s: smaller effect** |
| H021/H023: CatBoost lowers row 192622644 (1,500–7,000 s) and row 183910286 | **Both raised** (10,976 s; 22,233 s) |
| H023: S1 TIE most likely; promotion P 0.20 | **S1 WIN; criteria 1–8 met** |
| H023: `NM_present_LIRF` S1 cell +8 to +28 s | small and favourable (share 0.24) |
| H022: +8 to +35 s against E029 | +4.05 s: favourable side |
| Advisor (X-D05-S04-0003): H023 promotion P 0.04; S1 WIN P 0.07 | criteria 1–8 met; S1 WIN |
| Advisor: H021 clause 1 not met P 0.60; H023 clause 1 not met P 0.35 | not met; not met |

**Corrections and process slips:**
- **D5-C1:** "swap 0" was wrong. 4 GiB of swap existed from 16:33Z, unused.
- **D5-C2:** CPython 3.13.15 was unrecorded against the brief's 3.11.
- **D5-C3:** the laptop differences were wrongly attributed to LightGBM and the CPU.
- **D5-C4:** E028 differs on routed rows.
- **D5-C5:** E027–E029 were allocated outside their reviews' scope.
- **D5-C6:** E029's manifest named the wrong commit (the worker now records it at start).
- **D5-C7:** a calibration row was misattributed.
- **INC-0008:** the researcher ran real-silver tests beside E025 and caused the OOM.
- **Unmeasured timestamps,** corrected: H022 v1's `created_utc` (before submission), and one STATE.md header (committed, then corrected).
- **Owner methodological suggestion** (early stopping on the evaluation curve): logged and not adopted (D05-S04 session record).

## 8. Delegated work (INC-0006)

**None.** INC-0006 permitted delegation to `claude-sonnet-5-5` workers. Every Day 5 artifact, proposal, run and interpretation is the main session's. INC-0006 closes at this phase close.

## 9. Open questions for Days 6–7

1. **CatBoost alone (E031's configuration) was not a candidate.** Whether it, or another weight, would beat the blend is untested and would be selection on development results. Any such candidate needs its own proposal (rule 10 does not cover it, but the selection hazard does).
2. **Submission reproducibility.** The blend's CatBoost half is a GPU re-draw, so Day 7's SUBMIT predictions will not reproduce bit for bit. The 1.0 s tolerance held for the blend (0.48 s), but not for CatBoost alone on R1.
3. **D3-C3 (January long-delay rows) and forward risk** for the new configuration: the > 3 h band on development folds is 3, but January 2026 has 2.0–2.6 times the 2025 maximum.
4. **"LightGBM already holds the keys"** (D4-C7): still untested as stated. Day 5 shows CatBoost's statistics add signal *in CatBoost*, and the blend adds signal *beyond* the LightGBM.
5. **Neural models** (optional in the brief): not attempted.
6. **The environment binding** (rule L v2 item 6; INC-0010) carries into Days 6–7.

*Draft written 2026-10-02 (D05-S05).*
