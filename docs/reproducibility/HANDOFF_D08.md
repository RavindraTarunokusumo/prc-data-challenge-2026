# Handover after Day 8, and the plan for Days 9–12

*Written 2026-10-07 by the researcher at the close of session D08-S03, after the owner's decision to continue (Branch B; X-D08-S03-0004 acknowledgement). This file changes no record. Its plan is non-binding: every item needs its own proposal and review.*

## 1. State at handover

| Item | Value |
|---|---|
| Phase | OPEN (Days 8–12). Day 8 closed (X-D08-S03-0004, ACCEPT 0.85) |
| Champion | **E046**, development mean 314.42 s. Unchanged since Day 7 |
| Submission | E050's file, `f0dc2c7c…06e8`. **At most one new upload, before 2026-10-11T12:00:00Z** (G7) |
| Holdout | Closed for Days 8–12 (H8). No H read remains |
| Looks (G5 (a)) | 2 in Days 8–12 (E051, E052). Days 1–7 baseline: 44 |
| Next IDs | E053, H039, INC-0024, X-D09-S01-0001 |
| Branch | `day-8` (pushed). Its PR into `main` is not open yet: the GitHub CLI here is not logged in |
| Open incidents | INC-0004, INC-0009, INC-0010, INC-0017, INC-0018 (D8), INC-0023 |
| Weather | Bronze data for ten airports, kept and not used (INC-0019 closed; the IEM licence is unsettled) |

**Before Day 9 starts (owner):** merge `day-8` into `main`. The merge is content-neutral: no frozen file changes. Then the Day 9 session cuts `day-9` from `main`.

## 2. What binds every Day 9–12 proposal (X-D08-S03-0004 Q5)

- **B1. Not admissible:**
  - any change to the LIRF NM-missing subgroup's predictions (it carries G5's consequence);
  - weather;
  - a non-LIRF recording-convention candidate.
- **B2. Design.**
  - Design and pilot on 2025-01, 04, 05 and 06 only, with the parameters and decision rule committed before the pilot runs.
  - State the G5 (c) footprint, and rely on no row-level validation-month record, including Day 8's comparison files.
  - **Leave E046's subgroup predictions exactly unchanged,** through an override from E045's stored predictions, checked as in `mixture_check.py`.
  - Judged against E046 by criteria 1–8 and rules 1–15, with rule 13 if stochastic.
- **B3. The CatBoost iteration count** is not read off validation curves, and needs a stated reason to expect ≥ 1.0 s on the development mean.
- **B4. Upload.**
  - A promotion leads to an upload only if its SUBMIT file is complete and checked before 2026-10-11T12:00:00Z, through its own reviewed SUBMIT proposals (as H031–H037).
  - The promoting phase close pre-registers the final-file rule.
  - Otherwise: no new upload, and E050 stands.
- **B5.** Each phase close repeats the H8 ledger check, the look count, G1's status and the delegated-work list.
- **Owner questions (Q3).** The owner is asked only "continue or refreeze".
- **The Advisor's estimate:** P(promotion) ≈ 0.06. The plan below is written to be stopped early.

## 3. Where the remaining error is

From HANDOFF_D07 §2 (E046, development folds; read from stored predictions, fold aggregates):
- the NM-present bulk at the nine non-LIRF airports holds **about 0.41** of each fold's SSE;
- the LIRF NM-missing subgroup holds about 0.32, and it is closed by B1;
- the rest is small and scattered.

**So the only open lever of size is ordinary taxi-outs at the nine airports.** Days 3–6 already put congestion counts, static keys and two learners on it. A new mechanism has to bring information the models do not yet have.

## 4. Plan (researcher's recommendation; each step needs its own review)

### 4.1 Primary idea: the airport's recent realised taxi state (H039, to be written)

**The gap.** The congestion block (Day 3) counts movements, but no feature measures **how long** recent movements took. The admissible information set (DATASET_AUDIT §6.2) contains:
- **arrival taxi-in times** (`BLOCK − MVT` on ARR rows), which are complete in training, validation and ranking alike;
- **other departures' `MVT − AOBT_3`**: their takeoff time against their NM off-block estimate. It is a noisy proxy of their taxi-out, built without any blanked column.

A de-icing queue, a closed taxiway or a runway-configuration change lengthens all of these at once, before and while the row taxis. That is what the counts miss.

**Candidate features.** Proposed, not designed yet. Windows and statistics are fixed a priori in the params file:
- median taxi-in of arrivals in-blocked in [t_off − 30 min, t_off) at the airport, and their count. Label **P**;
- median `MVT − AOBT_3` of other departures airborne in [t_off − 30 min, t_off), at the airport and on the row's runway. Label **P**: other rows only, never the row's own;
- the same over (t_off, t_to] as a **T** group, reported separately, as Day 3 did.

**Leakage checks.**
- No DEP block time or target of any validation row is used. Other departures' `MVT − AOBT_3` uses only unblanked columns.
- A synthetic test asserts that a P feature is invariant to the row's own takeoff (as `test_p_features_invariant_to_own_takeoff`).
- An isolation test asserts that no blanked column enters.

**Known risk.** Day 3 noted that the row's own `d_aobt3` "already encodes the realised waiting" (H017). The new block may add little beyond it. The design pilot decides this.

**Construction (B2).**
- Refit E029's configuration (routed LightGBM) and E031's (routed CatBoost, GPU) on FS2 or FS2_RAW plus the block.
- Blend them 0.5/0.5, as E033.
- **Override the LIRF NM-missing subgroup from E045's stored predictions**, so the subgroup equals E046's exactly.
- The matched reference is E046.
- Rule 13 applies (CatBoost on GPU is stochastic). Report the draw spread (rule 15 (b)).

**Design pilot (before the proposal is reviewed).**
- LightGBM (E045 / E020's configuration) on FS2 against FS2 plus the block, P1 and P2 as in Day 8.
- Proposed rule: **≥ 1.0 s better on all rows in both pilots**, committed with the params before the pilot runs.
- If it fails, H039 is not proposed and the plan goes to §4.3.

### 4.2 Secondary (only if 4.1 is promoted and time remains)

**Nothing.** The phase-open review judged item 4 (iterations) unlikely to clear criterion 1, and draw averaging changes variance, not the mean. Neither is worth a phase in the time left.

### 4.3 Stop rule

The project refreezes with E050 standing if either holds:
- the 4.1 pilot fails its rule;
- E053 (or the next primary ID) is not promotable by **2026-10-10T12:00Z**, which leaves 24 h for the SUBMIT path.

The refreeze follows X-D08-S03-0004 Q6 at that phase close.

### 4.4 Schedule (UTC; the owner sets each run window)

| Day | When | Work | Compute |
|---|---|---|---|
| **D9** | 8 Oct | Session start; `day-9` from `main`. Build the block, with tests. **Commit the params and the rule, then run the design pilot.** If it passes: write the H039 proposal and get the review. | Pilot about 5 min, CPU |
| **D10** | 9 Oct | Allocate. Run the candidate and its reproduction (rule 13 and criterion 6) in the owner's window, then the analysis. | LightGBM half about 15 min; CatBoost half about 25 min (GPU); the reproduction about the same. **About 80 min in total** |
| **D11** | 10 Oct, by 12:00Z | Phase close (promote or not). On a promotion: the final-file rule, the SUBMIT proposals and their review. | — |
| **D11–D12** | 10 Oct to 11 Oct 06:00Z | SUBMIT fits (LightGBM about 5 min, CatBoost about 7 min on GPU, blend, override about 5 min, formatter), I1–I5 and the final record. | About 20 min |
| **D12** | 11 Oct, before 12:00Z | The owner uploads `genuine-cabbage_v2.parquet` once, after recomputing its SHA-256. Then FROZEN (P7, G2). | — |

Every step after the pilot depends on the one before. A slip of more than half a day reaches the stop rule.

## 5. Risks

- **The only evidence is the development folds,** because H is closed. A v2 would rest on weaker evidence than v1's December WIN. Criterion 2 (3 WINs including S1) is the guard.
- **Fold reuse.** Each look adds to G5 (a). A neighbour-duration block is a new mechanism, but the folds have been read 46 times.
- **Time.** The CatBoost half needs the GPU and the owner's window. One failed arming (as INC-0022) costs a day.
- **The SUBMIT draw.** The CatBoost SUBMIT fit is a new GPU draw (D5-C9). The submission is one draw of the procedure.
- **The convention bet (U6) carries over unchanged,** because the subgroup is E046's.

## 6. How the next session starts

1. AGENTS.md session start: read the brief, STATE, this file, `research/day-08/DAY_SUMMARY.md`, the X-D08-S03-0004 review and acknowledgement, and the ledger tails.
2. Session D09-S01: append to the registry and write `research/day-09/sessions/D09-S01/SESSION_START.md`.
3. Confirm that `day-8` is merged into `main`, then cut `day-9`.
4. Begin with §4.1's block and tests, then the params commit, then the pilot.
