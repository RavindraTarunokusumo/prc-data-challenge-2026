# PRC Data Challenge 2026: final report (team genuine-cabbage)

*DRAFT for the Day 7 phase close (X-D07-S01-0003). Items marked {{…}} depend on the Day 7 holdout outcome and are filled in at the freeze.*

## 1. What this project was

An autonomous research run predicting departure **taxi-out time** (RMSE, seconds) at ten European airports. Training data are January–December 2025; predictions are for January and July 2026. A Claude research agent (`claude-opus-5-5`) proposed, implemented, ran and analysed every experiment. A fixed Claude Advisor subagent at maximum reasoning effort reviewed every proposal and every phase close before anything ran. Repository scripts enforced the rules: frozen splits and metric, hash-verified gating, resource limits and append-only history. The owner started and stopped the run, set run windows and made the decisions recorded in `docs/incidents/`; the owner did no feature selection, tuning or interpretation.

## 2. Validation design (frozen on Day 1)

- **Development folds:** three rolling months (R1–R3: Sep, Oct, Nov 2025), a seasonal analogue of July (S1: Jul 2025) and a winter analogue of January (W1: Feb 2025). S1 and W1 have causal twins (S1c, W1c) that train only on earlier months.
- **Protected holdout H:** December 2025, at most one access per phase, named by the phase-close review.
- **Promotion (brief §10):** overall RMSE improves under a paired airport-day bootstrap; WIN on a majority of folds including S1; no airport worse by more than 3 %; an ablation supporting the claimed mechanism; no leakage; reproduction within tolerance; resources within class; Advisor objections resolved.
- **Final folds:** `SUBMIT_JAN` and `SUBMIT_JUL`, each training on all of 2025 and predicting one ranking month (no cross-month information).

## 3. What each phase found

| Day | Theme | Result |
|---|---|---|
| 1 | Infrastructure, audit, baselines | Frozen splits and metric. Ridge on row-level deltas (E005, 482.73 s) became champion; holdout WIN against the global mean. The tail decides RMSE, and at LIRF the long "taxi-outs" without an NM match are largely a **block-at-schedule recording convention**. |
| 2 | Static and temporal structure | Static keys carry about 9–30 s on NM-matched rows, but on all rows they could not be separated from the convention records. No promotion. |
| 3 | Congestion reconstruction | Traffic state helps modestly (−6.75 s on NM-matched rows outside LIRF). Champion E019 (444.49 s): LightGBM on FS2 with the LIRF NM-missing subgroup **routed** to the ridge; holdout WIN (375.93 against 411.29 s). Day 3 also priced the routing: **+122.5 s** on the development folds. |
| 4 | Historical priors | Fold-local target priors add almost nothing to a tree learner on FS2 (−0.3 s). Excluding the routed rows from LightGBM's training fixed an out-of-range defect (−2.0 s). No promotion. |
| 5 | Model architecture (laptop, GPU) | Champion E033 (438.87 s): an equal blend of the routed LightGBM and a routed CatBoost with categorical statistics; −5.62 s against E019, 7/7 WIN; holdout WIN (369.18 against 375.93 s). |
| 6 | Adversarial science | Seven controls found nothing contradicting E033; its margin held over three GPU draws. |
| 7 | Synthesis, submission, freeze | The champion's SUBMIT procedure (E042–E044) gives a complete submission that passes every check. A routing candidate (H035, E046: E033 with the LIRF NM-missing rows predicted by an unrouted LightGBM) meets every development criterion at 314.42 s, but its gain is a bet on the LIRF convention; it is promoted only on a December WIN (objection F). Outcome: {{WIN/TIE/LOSS; champion}}. |

## 4. Champion and submission

| | Development mean (5 folds) | Holdout H (Dec 2025) | Submission file |
|---|---|---|---|
| E005 (Day 1 champion) | 482.73 | 411.29 | — |
| E019 (Day 3 champion) | 444.49 | 375.93 | — |
| E033 (Day 5 champion) | 438.87 | 369.18 | E044: `predictions/final/submitting.parquet`, SHA-256 `d57ff7db7dfa34e13934aa524464ea13dbe9f5f904fae400a85f87e62c95af73` |
| E046 (Day 7 candidate) | 314.42 | {{…}} | E050 (if promoted): {{…}} |

Final champion and submitted file: {{…}}.

**What the submission's accuracy rests on.** No development fold or holdout measures the submission itself. It is refit on all 12 months and carries one GPU draw of the CatBoost half. The figures above belong to the evaluated champion, not to the submission.

## 5. The recording-convention bet (LIRF)

- At LIRF, departures without a network-manager match often carry a block time equal to the scheduled time, so their recorded "taxi-out" is really takeoff minus schedule: hours, not minutes (Day 1: 83 % of LIRF tail rows).
- The champion E033 predicts those rows with a ridge that cannot represent this. Day 3 priced that choice at about 122 s of development RMSE.
- The Day 7 candidate predicts them with a tree model that has learned the convention.
- **It wins only if the convention persists.** On the 2025 folds it keeps an advantage only if the 2026 convention rate stays above about 20–57 % of the 2025 level. If the convention disappeared, it would lose 0.25–1.3 times what it gains in 2025. Day 3's earlier wording ("loses only if the convention nearly vanishes") understated this, and was corrected on Day 7 (U6).
- The development folds cannot test the bet. December 2025 was the only fresh month: {{outcome}}.

## 6. Limitations

- January 2026's inputs sit outside the 2025 winter range (mean schedule delay 36.4 min against 30.0 in January 2025; NM-missing share 1.61 % against 0.93 %). Its 435 long-delay NM-missing rows outside LIRF were untestable (D3-C3).
- July 2026 is seven months after the last training month; the 1 July month edge has no previous-day context.
- Several pre-registered magnitudes were missed, and those misses are kept in the journal. Single rows decide single folds (rule 6 disclosures).
- Environment: Days 1–4 ran on a 4-vCPU cloud container and Days 5–7 on the owner's laptop. Laptop instances replaced cloud references under rule L v2. Incidents INC-0004, INC-0009 and INC-0010 remain open.

## 7. Governance record

- 50 experiments allocated by the gate (E001–E050); one resource failure (E025); {{E049, E050 status}}.
- 27 Advisor exchanges (X-D01-S01-0001 to X-D07-S01-0003); every proposal reviewed before execution, with every decision and condition mirrored under `orchestration/advisor-exchanges/`.
- Holdout: Day 1 WIN; Day 2 closed unused; Day 3 WIN; Day 4 closed unused; Day 5 WIN; Day 6 closed unused; Day 7 {{…}}.
- Zero leaderboard reads and zero submissions before FROZEN. The submission bucket was never listed or read.
- 15 incident records, including every owner intervention. INC-0004, INC-0009 and INC-0010 remain open.

## 8. Provenance statement

> Days 1–4 of this project were conducted as an autonomous ML research run in a Claude Code cloud session. A Claude model served as primary researcher and generated hypotheses, implemented features and models, ran experiments and analysed results. A fixed Claude Advisor subagent at maximum reasoning effort reviewed every proposed experiment before execution and could accept, revise, reject or hold it, but could not implement experiments or access leaderboard results. Deterministic scripts enforced frozen validation splits, resource limits, hash-verified review gating and append-only history. The substitution of Claude for the originally planned Gemini/Codex pair is recorded as protocol deviation INC-0001. Days 5–7 were continued on the project owner's laptop under the same governance, with the same researcher and Advisor arrangement; the owner set run windows and made the recorded decisions in `docs/incidents/`.
