# Handover after Day 7 (FROZEN) and a plan for a six-day extension

*Written 2026-10-05 by the researcher at the close of session D07-S01. Appended after FROZEN under INC-0018. This file changes no frozen record.*

## 1. State at handover

| Item | Value |
|---|---|
| Project state | **FROZEN** at `4c21eff` (branch `day-7`, pushed); appended files after it: D7-C15, `LICENSE` (GPLv3), the upload record, INC-0017/0018, this file |
| Champion | **E046** (H035 v1): E033 (0.5/0.5 blend of the routed LightGBM E029 and the routed CatBoost GPU E031), with the LIRF NM-missing subgroup predicted by E045 (E020's unrouted LightGBM on FS2) |
| Development mean (R1, R2, R3, S1, W1) | 314.42 s (E033: 438.87) |
| Holdout H (Dec 2025) | 244.94 s (E046 against E033, one access; ruling H7: no H reads remain) |
| Submitted | `prc-2026-genuine-cabbage/genuine-cabbage_v1.parquet`, SHA-256 `f0dc2c7c40063e238ef57f51d31192008e37c5327afcdc67d563868af17d06e8` (uploaded by the owner) |
| Records | `docs/reports/FINAL_REPORT.md`, `research/day-07/DAY_SUMMARY.md`, `research/STATE.md`, `models/champion/CURRENT.json`, `research/day-07/submission/` |
| Pending | PR `day-7` → `main` (content-neutral; the GitHub CLI here is not logged in) |
| Open incidents | INC-0004, INC-0009, INC-0010, INC-0018 |

**Reproducing the submission.**
- Environment: rule L v2 item 6 (CPython 3.13.15, `uv.lock` `efa4fd78…`, polars 16 threads, the RTX 5060 laptop). `docs/reproducibility/HANDOFF_D04.md` §§2–4 covers setup and the data download.
- Run order: E029-config and E031-config SUBMIT fits (E042, E043; CatBoost on GPU, not bit-reproducible), blend (E044), E020-config SUBMIT fit (E049), override (E050). Then `scripts/make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050`.
- A re-run of E043 is a new GPU draw, so only the LightGBM parts and the override reproduce bit for bit.

## 2. Where the champion's error is (development folds, E046)

Read-only analysis of stored predictions on R1–W1 (2026-10-05):

| Population | Rows (5 folds) | Mean share of fold SSE |
|---|---|---|
| NM-present, other nine airports, bulk (y < 3,600 s) | 789,259 | **0.41** |
| LIRF NM-missing, tail (y ≥ 3,600 s; the convention rows) | 330 | **0.26** |
| LIRF NM-present (bulk 0.077 + tail 0.077) | 65,321 | 0.15 |
| LIRF NM-missing, bulk | 400 | 0.06 |
| NM-present other, tail | 1,039 | 0.05 |
| NM-missing other (bulk 0.015 + tail 0.048) | 10,052 | 0.06 |

- The top 0.1 % of rows carry 23–60 % of each fold's SSE.
- Bulk RMSE (y < 3,600 s) is 203–294 s.
- **Two levers dominate:**
  - about 730 LIRF NM-missing rows still hold about a third of the error;
  - the NM-present bulk at the nine other airports holds two fifths.

## 3. Plan for 11 October (deadline 23:59:59 CET)

### 3.1 Decisions the owner must make first

1. **Leaderboard policy for the extension.** This is the key choice, and the researcher recommends **A**.
   - **A (protocol-preserving):** the extension keeps the governance. Every change goes through proposal, Advisor review and gate. Selection uses pre-registered development-fold criteria only, and **one** further submission (v2) is made at the end. Leaderboard figures, including "214" and any score of ours, are recorded only and choose nothing. Results are reported as an extension beside the frozen run.
   - **B (leaderboard-guided):** several variants are submitted, and the best by leaderboard is kept. It is faster, but it is leaderboard-guided optimisation. It overfits the ranking months, which are also the scoring months, and it falls outside this project's research claim. Every B submission must be labelled as such.
2. **Run windows** for each batch (CPU and GPU), as on Days 6–7.
3. **The session:** a new researcher session (D08-S01) on branch `day-8`, from `main` after the Day 7 PR merges.

### 3.2 Science, by expected value

Magnitudes are researcher estimates on development folds, not leaderboard forecasts. Each is a hypothesis to be pre-registered.

| # | Idea | Targets | Why | Expected (dev) | Cost |
|---|---|---|---|---|---|
| 1 | **Convention-mixture model for LIRF NM-missing rows:** a classifier for P(block-at-schedule), then p · f(`d_sched`) + (1 − p) · normal-taxi prediction (Tier 2 two-stage) | 0.32 of SSE (730 rows) | Under squared error the best point forecast is the conditional mean. E045 is a general model that learned the convention indirectly, so it predicts in between on ambiguous rows. A dedicated mixture should cut both the tail misses and the bulk over-predictions (criterion 8's +1,000 to +4,300 s bulk cost). | −10 to −60 s on folds with many subgroup rows; noisy (few rows; rule 6) | CPU, minutes |
| 2 | **The same structure for LIRF NM-present tail rows** (0.077) and **NM-missing rows at other airports** (0.048), only if a target-free and development check shows block-at-schedule there too | 0.13 | It may be the same mechanism, unrouted elsewhere. | 0 to −15 s | CPU |
| 3 | **CatBoost at 2,000–3,000 iterations** (it was still improving at 1,000), as the blend's second half | the NM-present bulk (0.41) | A known open question (Day 6 §9). | −1 to −4 s | GPU, about 30–45 min |
| 4 | **Average of 3 CatBoost draws** in the blend | variance (D5-C9) | Removes draw noise in the SUBMIT fit. | −0.5 to −1.5 s | GPU, 3 × 20 min |
| 5 | **Convention-aware CatBoost on the subgroup** (an unrouted E031 config) averaged with E045 there | the subgroup | Two learners of the convention. | −5 to −20 s | GPU |

Not recommended in six days: neural models; new congestion features (Days 3–4 found small gains); any threshold tuned on the ranking months.

### 3.3 Schedule (the owner sets each run window)

| Day | Date | Work |
|---|---|---|
| D8 | Mon 5–Tue 6 Oct | Merge Day 7; open `day-8`. **Advisor governance review** of the extension rules (policy A/B, no holdout, selection rule, one v2). Target-free EDA for ideas 1–2. Proposals for batch 1 (ideas 1, 2). |
| D9 | Wed 7 Oct | Batch 1 runs (CPU, about 30 min) and analysis. Proposals for batch 2 (ideas 3–5). |
| D10 | Thu 8 Oct | Batch 2 runs (GPU, about 60–90 min; may need two windows) and analysis. |
| D11 | Fri 9 Oct | Combined candidate, reproduction, SUBMIT fits; extension phase-close review, which selects by the pre-registered rule. |
| D12 | Sat 10 Oct | Format, freeze v2, owner uploads `genuine-cabbage_v2.parquet`. |
| — | Sun 11 Oct | **Buffer only.** No new runs after noon; the deadline is 23:59:59 CET. |

### 3.4 Risks

- **No holdout is left.** Under A, any v2 rests on development folds alone. That is weaker evidence than v1's December WIN, so the governance review should require a large, broad development margin before replacing v1.
- **The LIRF convention bet (U6) is already in v1.** Ideas 1, 2 and 5 deepen it: if the convention is gone in 2026, they lose more.
- **Leaderboard-score comparisons:** our development and H figures are not comparable to leaderboard RMSE (different months; the 2026 inputs shift, D3-C3, D7-C7).
- **Time:** each Advisor review takes 20–35 min, and two of Day 7's runs exceeded their time guards. The schedule keeps a buffer day.

## 4. How to start the next session

1. Merge the `day-7` PR (description: `research/day-07/PR_DESCRIPTION.md`).
2. Launch the researcher session and say: "Begin Day 8 (post-freeze extension, INC-0018). Leaderboard policy: A (or B). Run windows: …".
3. The session reads AGENTS.md's start list, then this file, then INC-0018.
