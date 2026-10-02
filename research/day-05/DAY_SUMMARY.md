# Day 5 summary: model architecture, CPU against GPU (FINAL; phase close X-D05-S05-0001 ACCEPT; holdout WIN; new champion E033)

**Sessions:** D05-S01 to D05-S05, on the owner's laptop. **Branch:** `day-5`.

**Provenance:**
- The researcher is `claude-opus-5-5` (`--effort high`). The Advisor is the fixed `advisor` subagent (definition `30fff5dd3c54`).
- **INC-0006** (delegation to `claude-sonnet-5-5` workers) was permitted but **not used**: no Day 5 work was delegated (§8).
- Environment and process incidents: INC-0007 (closed), INC-0008 (closed), INC-0009 (open), INC-0010 (open), INC-0011 (closed); INC-0004 remains open (§7).

## 1. The Day 5 question and its answer

**Question (brief §3, §11):** the model architecture day, CPU against GPU. Does a different learner family, or a combination of learners, improve on the champion's routed LightGBM?

**Answer: yes. A second learner family adds signal, and the equal-weight blend of the two meets every promotion criterion against the champion.** It was promoted at the phase close: X-D05-S05-0001 ACCEPT (0.88), then **holdout H (December 2025) WIN**, E033 369.18 s against E026 375.93 s (−6.75 s; recorded only, ruling H5). **E033 is champion.**
- **CatBoost on GPU with categorical statistics on raw keys (H021, E031)** reaches a development mean of **440.76 s**.
  - Against the routed LightGBM with the same D3-C2 treatment (E029, 442.46 s): **−1.69 s on all rows (q95 −0.74), W1 TIE.**
  - **Its S1 WIN is 62 % one row** (D5-C11): −4.14 s with row 192622644, −1.66 s without it. The diffuse effect is the blend's.
  - **This was expected to lose** (+2 to +15 s; H020's Day 4 review expected worse).
- **Within CatBoost at fixed capacity, the categorical statistics carry signal** (H021 clause 1, final): against the same CatBoost with categorical columns as integer codes (H022, E030), **−4.91 s** on `NM_present_excl_LIRF`, with 5/5 counted WINs.
  - The GPU and seed re-draw (E032) moves this by +0.68 s, inside the 1.5 s noise limit.
  - This does not attribute E031's all-rows advantage over E029, which is a different contrast and population (D5-C12 (a)).
- **The blend (H023, E033)** is a fixed 0.5/0.5 average of E029 and E031:
  - **438.87 s**; −3.58 s against E029 on all rows, and −3.96 s on normal taxis;
  - **against E019 (laptop instance E026): −5.62 s (q95 −4.79), WIN on all 7 folds, S1 included**, every airport improved. Against E019's own cloud metrics it is −5.620 s;
  - **composition (D5-C8):** −2.04 s is E029's D3-C2 treatment (E023's Day 4 margin) and −3.58 s is the CatBoost half. On S1 they are +0.20 s and −4.38 s, so **S1's WIN is entirely the CatBoost half**;
  - **D3-C2 is treated** (> 3 h band 3, against E019's 81);
  - reproduced by E034 (within 0.48 s).
- **The single-row S1 constraint (D4-C9) did not bind.** The CatBoost half *raised* the prediction on row 192622644 (E031 10,976 s; blend 9,008 s; E019 8,136 s).
  - The S1 WIN is not carried by the LIRF NM-present convention mixture (share 0.24).
  - **Single rows (D5-C10):** without row 192622644, S1 is still −3.76 s. W1 is −2.56 s without row 183910286, and that row's W1 prediction rests on post-validation months (W1c reverses it).
- **One draw (D5-C9).** The champion's CatBoost half is a GPU re-draw. The blend's reproduction moved at most 0.48 s per development fold (RMS prediction change 15–23 s; 37 s on W1c), and clause 1's W1 reading moved from WIN to TIE. The SUBMIT predictions will be a further draw.

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

## 5. Champion: E033 (H023 v3), from this phase close

- **E019 was the phase-opening champion.** H023 v3 (E033) met criteria 1–8 against it (laptop instance E026), and the phase close accepted it (X-D05-S05-0001, 0.88).
- **Holdout H (December 2025), one access, E033 against E026: WIN.** −6.75 s (q10/q90 −9.83/−4.88); E033 369.18 s against E026 375.93 s. No revert.
  - **Ruling H5:** recorded only. H is a joint test of both mechanisms, on one draw, with the routed rows excluded by construction.
  - **Instance check:** E026's H RMSE is 375.92735 s, against E019's recorded 375.92721 s (+0.00014 s).
- **E033 is champion; E019 is previous.** H023 v3 (E033) and its reproduction (E034) are PROMOTE.
- **Standing disclosures on E033:**
  - D3-C1 (lineage);
  - **D3-C3 restated (D5-C16):** the January 2026 count fact and "H does not test it" stand; E033's development out-of-range share in the > 3 h band is 0.57 %, against E019's 15.3 %;
  - **D5-C8** (margin composition), **D5-C9** (stochastic champion), **D5-C10** (single rows), and the **1,000-iteration budget** (CatBoost still improving at 1,000).
- **D3-C2 is retired** as a defect of the champion (treated: > 3 h band 3 against 81), and kept as history. **D4-C9 is superseded** for E033 by D5-C10.

## 6. Findings

1. **CatBoost's categorical statistics carry signal at fixed capacity:** −4.91 s on normal taxis against integer codes (re-draw −4.23 s). `FloatTargetMeanValue` averages the raw target (Advisor-verified). The Day 4 H020 objections are answered.
2. **A second learner family competes with the LightGBM on this problem** (D5-C11). E031 against E029: −1.69 s on all rows (q95 −0.74), W1 TIE; its S1 WIN is 62 % one row; the diffuse effect is the blend's. The errors are partly decorrelated: residual correlation 0.84–0.92 on bulk rows, 0.94–0.99 on all rows.
3. **The blend beats E029 by −3.58 s (bootstrapped, pre-registered).** Against E031 it is better by point estimates only (−1.89 s by development mean; S1 −0.23 s), which were neither pre-registered nor bootstrapped (D5-C12 (b)). It beats E019 by −5.62 s, the largest single-phase gain since Day 3.
4. **Symmetric trees do not bound day-scale predictions here.** Both CatBoost arms predict *higher* than the LightGBM on the two LIRF NM-present day-scale rows; the H020-era reasoning was wrong for them. **The out-of-range reduction holds for the codes arm only** (D5-C12 (c)): E030's < 1 h band is 25, against 86 for E031, 82 for E029 and 82 for the blend.
5. **CPU against GPU (the brief's Day 5 theme):**
   - **Across hosts** (D5-C12 (d)): CatBoost on the laptop GPU (0.16–0.25 s per iteration) is about 4–7× faster than Day 4's cloud CPU (4 vCPU, 0.88–1.13 s per iteration at depth 6). No laptop-CPU run at full combinations exists. This makes the Day 4 configuration feasible.
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
| **Advisor (D5-C13), H023 v3:** `NM_present_excl_LIRF` −1.8 to +0.3 s; all rows −1.5 to +0.5; against E026 −1.5 to −3.5; S1 against E026 −0.3 to +1.8; row 192622644 4,500–8,000 s; H023r due P 0.05 | −3.96; −3.58; −5.62; −4.17; 9,008; due |
| **Advisor (D5-C13), H021 v3:** development mean 446–458; runtime 28–35 min; row 192622644 below 7,041 s P 0.60 | 440.76; 25.4 min; 10,976 |
| **Advisor (D5-C13), H022 v3:** development mean 448–468; runtime 8–14 min | 446.50; 3.7 min |
| **Advisor record (D5-C13):** the H021–H023 reviews carried H020's "CatBoost worse and bounded" premise | wrong in sign on both counts; the blend arithmetic was right on the realised inputs |
| Advisor (phase close): H WIN P 0.87; E033 − E026 on H −3 to −10 s (central −6) | WIN; −6.75 s |

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
- **D5-C8 to D5-C16** (`research/day-05/acks/PHASE_CLOSE_D05_ack_v1.md`): applied here.
  - D5-C14: ledger decisions E033 and E034 PROMOTE; E026–E032 null with roles in `notes`.
  - D5-C15: E033's rule 12 call named E033 only; the E019 bands came from `range_check_E023.json`. The W&B champion lineage was fixed (E003, E033). The phase-close proposal's "reads only `metrics.json`" was imprecise, but no H figure reaches W&B. INC-0007 got its pointer to INC-0010.

## 8. Delegated work (INC-0006)

**None.** INC-0006 permitted delegation to `claude-sonnet-5-5` workers. Every Day 5 artifact, proposal, run and interpretation is the main session's. INC-0006 closes at this phase close.

## 9. Open questions for Days 6–7

1. **CatBoost alone (E031's configuration) was not a candidate.** Whether it, or another weight, would beat the blend is untested and would be selection on development results. Any such candidate needs its own proposal (rule 10 does not cover it, but the selection hazard does).
2. **Submission reproducibility.** The blend's CatBoost half is a GPU re-draw, so Day 7's SUBMIT predictions will not reproduce bit for bit. The 1.0 s tolerance held for the blend (0.48 s), but not for CatBoost alone on R1.
3. **D3-C3 (January long-delay rows), restated for E033 (D5-C16):** the January 2026 count (435 non-LIRF NM-missing rows over 3 h, 2.0–2.6 times the 2025 maximum) and "H does not test it" stand. E033's development out-of-range share in the > 3 h band is 0.57 %, against E019's 15.3 %.
4. **"LightGBM already holds the keys"** (D4-C7): still untested as stated. Day 5 shows CatBoost's statistics add signal *in CatBoost*, and the blend adds signal *beyond* the LightGBM.
5. **Neural models** (optional in the brief): not attempted.
6. **The environment binding** (rule L v2 item 6; INC-0010) carries into Days 6–7.

## 10. Phase close (X-D05-S05-0001)

- **ACCEPT** (confidence 0.88). The Day 5 decisions stand.
- **Holdout: WIN** (E033 against E026, −6.75 s). **E033 is champion.**
- **Ruling H5** and **standing rule 13** (stochastic components: disclose the re-draw spread beside criterion 6; from the next proposal on).
- **Incidents:** INC-0006 closed (no delegation). INC-0009 (W&B, curves) and INC-0010 (swap, interpreter; environment binding) stay open. INC-0004 stays open (owner decision).

*Finalised 2026-10-02 (D05-S05).*
