# PRC Data Challenge 2026: final report (team genuine-cabbage)

*FINAL, at the project freeze (Day 7; phase close X-D07-S01-0003 ACCEPT). Corrections D7-C8 to D7-C14 are applied.*

## 1. What this project was

- **The task:** an autonomous research run predicting departure **taxi-out time** (RMSE, seconds) at ten European airports. The training data cover January–December 2025; the predictions are for January and July 2026.
- **The researcher:** a Claude research agent (`claude-opus-5-5`, effort `high`) proposed, implemented, ran and analysed the experiments, with these recorded exceptions:
  - **Delegation.** On the owner's instruction, for budget reasons, Day 4 implementation work and experiment launches were delegated to `claude-sonnet-5-5` workers under the researcher's review (INC-0005). One Day 6 analysis script was delegated in the same way (INC-0013).
  - **Launch arguments.** On Day 2 (effort `medium`, INC-0003) and on Day 3 (model and effort, INC-0004, still open), the launch arguments differed from the registered configuration, and the effective tier cannot be determined.
- **The Advisor:** a fixed Claude subagent at maximum reasoning effort reviewed every proposal before its runs, and every phase close after that phase's runs.
- **Enforcement:** repository scripts enforced frozen splits and metric, hash-verified gating, resource limits and append-only history.
- **The owner's role:** started and stopped the run, set run windows, and made the decisions recorded in `docs/incidents/`. On Day 7 that included choosing, among options the researcher wrote and recommended, to test the routing candidate (INC-0015). The owner did no feature selection, tuning or interpretation.

## 2. Validation design (frozen on Day 1)

- **Development folds:**
  - three rolling months: R1–R3 (September, October, November 2025);
  - a seasonal analogue of July: S1 (July 2025);
  - a winter analogue of January: W1 (February 2025).

  S1 and W1 have causal twins (S1c, W1c) that train only on earlier months.
- **Protected holdout H:** December 2025, at most one access per phase, named by the phase-close review.
- **Promotion (brief §10):**
  1. overall RMSE improves under a paired airport-day bootstrap;
  2. at least 3 WIN among the 5 development folds, S1 WIN, and no development-fold LOSS; an S1 or W1 WIN counts only if its causal twin is not LOSS;
  3. no airport worse by more than 3 %;
  4. an ablation supporting the claimed mechanism;
  5. no leakage;
  6. reproduction within tolerance;
  7. resources within class;
  8. Advisor objections resolved.
- **Final folds:** `SUBMIT_JAN` and `SUBMIT_JUL`. Each trains on all of 2025 and predicts one ranking month (no cross-month information).

## 3. What each phase found

| Day | Theme | Result |
|---|---|---|
| 1 | Infrastructure, audit, baselines | Frozen splits and metric. A ridge on row-level deltas (E005, 482.73 s) became champion, with a holdout WIN against the global mean. The tail decides RMSE. At LIRF, the long "taxi-outs" without an NM match are largely a **block-at-schedule recording convention**. |
| 2 | Static and temporal structure | Static keys carry about 9–30 s on NM-matched rows. On all rows they could not be separated from the convention records. No promotion. |
| 3 | Congestion reconstruction | Traffic state: −6.75 s on NM-matched rows outside LIRF (the mechanism figure). Congestion as served in the champion: **−1.90 s on all rows** (q95 −0.98; R1 and R2 TIE; criterion 3 fails at EHAM, +7.2 %). Champion E019 (444.49 s): LightGBM on FS2, with the LIRF NM-missing subgroup **routed** to the ridge; holdout WIN (375.93 against 411.29 s). 95 % of E019's margin over E005 was routed FS1 structure (D3-C1). Day 3 also priced the routing: **+122.5 s** on the development folds. |
| 4 | Historical priors | Fold-local target priors add almost nothing to a tree learner on FS2: −0.29 s on NM-matched rows outside LIRF (q95 +0.12; S1 TIE, W1 LOSS; mechanism falsified) and −0.40 s on all rows (q95 −0.03). Excluding the routed rows from LightGBM's training fixed an out-of-range defect (−2.0 s). No promotion. |
| 5 | Model architecture (laptop, GPU) | Champion E033 (438.87 s): an equal blend of the routed LightGBM and a routed CatBoost with categorical statistics. −5.62 s against E019, 7/7 WIN; holdout WIN (369.18 against 375.93 s). |
| 6 | Adversarial science | No Day 6 result contradicts E033's promotion, but neither batch had real power against the performance claim, and the attacks able to overturn it (the SUBMIT procedure, D3-C3) were not run (D6-C12). E035–E039 were an attribution ladder and E040–E041 were further draws. The margin held over three draws on all rows (spread ≤ 0.60 s), with a W1 mechanism-population spread of 2.00 s (D6-C11). |
| 7 | Synthesis, submission, freeze | The champion's SUBMIT procedure (E042–E044) gives a complete submission that passes every check. A routing candidate (H035, E046: E033 with the LIRF NM-missing rows predicted by an unrouted LightGBM) met every development criterion at 314.42 s; its gain is a bet on the LIRF convention. December 2025 (one access): **WIN**, so E046 was promoted. |

## 4. Champion and submission

| | Development mean (5 folds) | Holdout H (December 2025) | Submission file |
|---|---|---|---|
| E005 (Day 1 champion) | 482.73 | 411.29 | — |
| E019 (Day 3 champion) | 444.49 | 375.93 | — |
| E033 (Day 5 champion) | 438.87 | 369.18 | E044: `predictions/final/submitting.parquet`, SHA-256 `d57ff7db7dfa34e13934aa524464ea13dbe9f5f904fae400a85f87e62c95af73` |
| **E046 (Day 7 champion)** | 314.42 | 244.94 (December 2025, E046 against E033, one access) | **E050: `predictions/final/E050/submitting.parquet`, SHA-256 `f0dc2c7c40063e238ef57f51d31192008e37c5327afcdc67d563868af17d06e8`** |

**Final champion: E046. Submission: E050's file.** P4 (pre-registered before the December access) selected it because E049 and E050 completed, the route check passed, I1–I5 passed and no flag was raised. E044's file (E033's procedure) is kept and recorded, not submitted. Manifest: `research/day-07/submission/FINAL_SUBMISSION.md`.

**What the submission's accuracy rests on.**
- No development fold and no holdout measures the submission itself.
- It is refit on all 12 months and carries one GPU draw of the CatBoost half.
- **It also carries the recording-convention bet on 383 rows** (107 in January, 276 in July; §5). On those rows it predicts hours where E033's procedure predicts about 29 minutes. The squared difference is of the order of each month's whole squared error, so the bet moves each month's RMSE by tens to hundreds of seconds, in either direction.
- The figures above belong to the evaluated models, not to the submission. Neither E046's development margin nor its December ΔRMSE is the submission's expected gain.

## 5. The recording-convention bet (LIRF)

- **The convention.** At LIRF, departures without a network-manager match often carry a block time equal to the scheduled time. Their recorded "taxi-out" is then takeoff minus schedule: hours, not minutes (Day 1: 83 % of LIRF tail rows).
- **The two models.** E033 predicts those rows with a ridge that cannot represent this; Day 3 priced that choice at about 122 s of development RMSE. E046 predicts them with a tree model that has learned the convention.
- **The bet.** E046 wins only if the convention persists:
  - on the 2025 folds, it keeps an advantage only if the 2026 convention rate stays above about 20–57 % of the 2025 level;
  - if the convention disappeared, it would lose 0.25–1.3 times what it gains in 2025.

  Day 3's earlier wording ("loses only if the convention nearly vanishes") understated this. The Advisor corrected it on Day 7 (U6).
- **The evidence.** The development folds cannot test the bet. December 2025 was the only fresh month:
  - **WIN, −124.24 s** (q10/q90 −190.37/−42.98) on its 88 subgroup rows (26 days);
  - this resolves the Advisor's objection for December only;
  - it does not test July's seven-month distance or January 2026's subgroup delay tail, which lies above every 2025 month (July 2026's is at the 2025 maximum);
  - the downside stays of similar size to the gain.

## 6. Limitations

- **January 2026's inputs sit outside the 2025 winter range:** mean schedule delay 36.4 min against 30.0 in January 2025, and an NM-missing share of 1.61 % against 0.93 %. Its 435 long-delay NM-missing rows outside LIRF were untestable (D3-C3).
- **July 2026** is seven months after the last training month, and the 1 July month edge has no previous-day context.
- **Missed magnitudes and single rows:** several pre-registered magnitudes were missed, and the misses are kept in the journal. Single rows decide single folds (rule 6 disclosures).
- **Environment:** Days 1–4 ran on a 4-vCPU cloud container and Days 5–7 on the owner's laptop. Laptop instances replaced cloud references under rule L v2.
- **Open incidents:**
  - **INC-0004:** Day 3 launch configuration (model and effort against the registered configuration); open, owner decision.
  - **INC-0009:** the W&B mirror. E036–E039, E042, E043 and E045–E050 were never mirrored; the repository records are complete.
  - **INC-0010:** laptop swap and CPython 3.13 kept by owner decision; the rule L v2 environment binding.
- **FROZEN is enforced by records only** (STATE, the task ledger and append-only history). No code lock prevents a later change.

## 7. Governance record

- **Experiments:** 50 allocated by the gate (E001–E050), all run; one resource failure (E025). E049's run script failed after the run, in its checkpoint (the researcher's defect, D7-C14, INC-0016); no output was affected.
- **Advisor exchanges:** 27 (X-D01-S01-0001 to X-D07-S01-0003). Every proposal was reviewed before its runs, and every decision and condition is mirrored under `orchestration/advisor-exchanges/`.
- **Holdout:** Day 1 WIN; Day 2 closed unused; Day 3 WIN; Day 4 closed unused; Day 5 WIN; Day 6 closed unused; **Day 7 WIN** (E046 against E033). The Day 7 access is the project's last H read (ruling H7).
- **Leaderboard and bucket:** zero leaderboard reads and zero submissions before FROZEN. The submission bucket was never listed or read.
- **Incidents:** 16 incident records, including every owner intervention. INC-0004, INC-0009 and INC-0010 remain open.

## 8. Provenance statement

Brief §15, verbatim:

> Days 1–4 of this project were conducted as an autonomous ML research run in a Claude Code cloud session. A Claude model served as primary researcher and generated hypotheses, implemented features and models, ran experiments and analysed results. A fixed Claude Advisor subagent at maximum reasoning effort reviewed every proposed experiment before execution and could accept, revise, reject or hold it, but could not implement experiments or access leaderboard results. Deterministic scripts enforced frozen validation splits, resource limits, hash-verified review gating and append-only history. The substitution of Claude for the originally planned Gemini/Codex pair is recorded as protocol deviation INC-0001. Days 5–7 were continued by the project owner on local hardware under the same governance.

Facts beside it (D7-C10):
- **Days 5–7** ran on the owner's laptop with the same researcher and Advisor arrangement. The researcher remained the Claude model, and the owner set run windows.
- **Delegation:** Day 4 implementation work and experiment launches were delegated to `claude-sonnet-5-5` workers under the researcher's review, on the owner's instruction (INC-0005). One Day 6 analysis script was delegated (INC-0013).
- **Launch arguments** differed from the registered configuration on Day 2 (INC-0003) and Day 3 (INC-0004).
- **The Day 7 routing candidate** was tested by the owner's choice among options the researcher wrote and recommended (INC-0015). Its runs started in owner-set windows (INC-0015, INC-0016).
