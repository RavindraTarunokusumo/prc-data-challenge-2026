---
schema: advisor-review-v1
hypothesis_id: H024
proposal_version: 2
proposal_sha256: 483ed0ab9995a2b067905062213b628b63f85d8f4cebdb10e25aa2188a1b71db
exchange_id: X-D06-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.86
created_utc: 2026-10-02T18:08:13Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.86).** This is a delta review of v2 against `H024_review_v1.md`. This file also holds the shared batch findings and the binding conditions C1–C7, which H025–H028 v2 adopt by reference.

- **All nine required revisions are made, and the binding ruling is acknowledged.** A sentence-level diff of v1 against v2 contains only:
  - those items;
  - the recommended items the researcher adopted;
  - the new run order.

  Two v1 bullets were removed: "Selection hazard" and "none is a holdout NEW". The ruling bullet now covers both, and covers them more strictly.
- **H024 is still a clean single-parameter ablation of E031.** Its config block is E031's `config.yaml` with `max_ctr_complexity` changed from 4 to 1. The only other change is `job_class` (CLASS-L to CLASS-M). That is a supervisory setting (timeout 2,700 s), not a CatBoost parameter.
- **The shared §Batch is now sound for an adversarial day:**
  - both reading types are bounded;
  - rung A can no longer confirm a family claim;
  - the noise reference is measured;
  - deferral is status-only;
  - the launcher is pinned and inside the freeze.
- **The authorization carries seven binding conditions (C1–C7, Execution Authorization).** They cover:
  - the id mapping;
  - failure handling and later windows;
  - where the diagnostic code lives;
  - the wording of "carries" readings;
  - how the closed set counts a key present in one arm only.

  None of them changes a design, threshold, population or fold.

**Verified here.** All checks were read-only: no fit, no score, no truth read, no holdout.

- **Hashes.**
  - All five proposals match the envelope.
  - The launcher `research/day-06/sessions/D06-S01/run_window.sh` is `9da5b0c3700b6f2c294b2da6f0218e686a6f01711b20854ae4441aba97cf6a4d` on disk and at `377143d`, as pinned in §Batch.
  - The five v1 review files still have the hashes returned in X-D06-S01-0001.
  - The Advisor definition is `30fff5dd…` (unchanged).
- **Anchor `377143d`** is the commit that submits this envelope. It holds the five v2 proposals, launcher v2, the INC-0012 amendment, INC-0013 and the envelope.
  - `git diff --stat 4ad18a1 377143d -- src scripts pyproject.toml uv.lock config` is empty, so nothing frozen has changed since the Day 5 merge.
- **Lock and memory.**
  - `/proc/locks` holds no lock on `runtime/experiment.lock` (inode 214027). Its `E034` text is the last holder's stamp.
  - No experiment process is running. `free -m` shows 9,899 MiB available.
- **Allocation state.** No acks and no `experiments/E035`–`E039` exist yet. The last allocation in `orchestration/task-ledger.jsonl` is E034, so the next id is E035.
- **Runner.**
  - `check_config` reads the purpose from `gate.json`. Every purpose except `reproduction` requires `primary_seed` 42, and `gate.py allocate` defaults to `primary`. All five configs use seed 42, so all pass.
  - Timeouts are 2,700 s for CLASS-M and 450 s for CLASS-S. The hard RAM limit is 11 GB.
- **Configs.**
  - H027 differs from E029 only in `feature_fraction`, `bagging_fraction`, `bagging_freq` and `seed`.
  - The three blends have E033's structure.
  - `gbm.lightgbm` sets LightGBM's `seed` from the config seed, so seed 42 drives H027's bagging and feature fraction.
- **Inputs to the blends.**
  - All 32 prediction files of E029, E030, E031 and E033 match their manifests (byte hashes only).
  - E030 is COMPLETE, and `route_check_E030.json` passes on all 8 folds.
  - `prc.blending` refuses a component that is not COMPLETE, or whose file does not match its manifest.
- **Truth and holdout.**
  - `route_check.py` reads prediction files and three target-free silver columns (`MVT_ID_mvt`, `ADEP_mvt`, `AOBT_3_flt`).
  - `mechanism_check.py` reads truth only through `prc.evaluate.truth_frame`, which raises on holdout and final folds.
- **Launcher.**
  - Queue, pessimistic times and dependencies match the §Batch table.
  - The latest E038 start is 19:11:40Z (21:11:40 CEST).
  - `TZ` is pinned, and the window is computed from UTC epochs.
  - The clean-tree check runs at arming and at window open.
  - The checkpoint stages only the run's own paths, pushes over BatchMode SSH under a 60 s timeout, and logs "ENDED AFTER WINDOW".
  - `runtime/*` (including the launcher log), `catboost_info/` and `wandb/` are git-ignored.
- **Figures reproduced from `research/comparisons/`:**

| v2 figure | Recomputed |
|---|---|
| Blend re-draw (E034 against E033, via their E029 files): +0.26 s mean; R1 +0.24, R2 −0.07, R3 −0.08, S1 −0.07, W1 +1.28 | +0.263; +0.242, −0.068, −0.075, −0.067, +1.282 |
| Full-size re-draw E032 − E031: +0.68 s (q95 +1.075); LOSS on R1 and W1 | +0.683 (q95 +1.075); LOSS R1, W1; W1 +2.768 |
| "1.0 s is about 4× the mean shift" | 3.8× |
| "1.5 s is 2.2× the full-size re-draw" | 2.20× |
| DAY_SUMMARY §1: "A second learner family adds signal" | `research/day-05/DAY_SUMMARY.md` line 14, verbatim |

## Scientific Validity

### Revision checklist (v1 to v2)

| v1 revision | v2 | Status |
|---|---|---|
| 1. Bounded readings | "Carries" requires the bootstrap q95 of D(X)'s mean < +1.0 s. Everything else is INCONCLUSIVE. The bootstrap is stated to exclude the GPU draw | Met; C5 fixes the label wording |
| 2. Rung A | (a) The table now lists the whole CatBoost half as removed, with a twin close to E029 by design. (b) A LOSS reads only as "the generic-averaging floor at the measured disagreement", explicitly not family support. (c) "No rung carries" concludes non-substitution only, and no outcome makes or widens a family claim. (d) Kept | Met |
| 3. Noise reference | The blend re-draw is cited. The per-fold rule is stated not to contain the draw. A reading resting on W1 alone is flagged | Met |
| 4. Ordered boosting | Corrected to plain boosting, Bayesian bootstrap and oblivious trees (§Batch table; H026) | Met |
| 5. Diversity diagnostic | Reported on `NM_present_excl_LIRF`, all rows and bulk, for E030, H024, H027 and E031. The exact decomposition is adopted | Met; C4 states where the code lives |
| 6. Deferral | Status-only in both directions; "not run (window)" | Met; C2 and C3 complete it |
| 7. Launcher | Pinned and inside the freeze diff, with the overrun bound and deviation reporting. Every recommended launcher item is adopted | Met |
| 8. Closed exempt set (H024) | Expected to differ: `max_ctr_complexity` only. The expected-equal list is given. A violation makes H024's own reading INCONCLUSIVE, and H025 discloses it | Met; C6 closes one ambiguity |
| 9. Thresholds (H024) | 1.5 s, which is 2.2× the full-size re-draw and meets H021 v3's ≥ 2× precedent. Both sides are bounded and labelled "one draw" | Met |
| Ruling | Restated in §Batch, Status of the batch | Met |

### Remaining points (none blocking; C5 and C6 bind the two that matter)

**(a) A "carries" reading is a non-inferiority statement, and two labels drop its bound.**
- **The definition is right:** "the removed ingredient is not shown to be needed, at equal weight", with q95 of D(X)'s mean < +1.0 s.
- **Two labels state more than that:**
  - "E033's margin needs no CatBoost" (the rung A line in §Batch, and H028's Research Question);
  - "is a substitute" (the rung B line).

  Both drop the 1.0 s bound.
- **A "carries" reading can coexist with per-fold LOSSes.**
  - A blend-against-blend contrast moves only half the component's prediction difference. Its bootstrap spread is therefore about half the full-size one: q95 − mean ≈ 0.2–0.25 s, against 0.39 s for E032 against E031.
  - So D ≈ +0.5 s can give q95 < +1.0 s together with LOSS on several folds.
  - Recorded as "not shown to be needed", that would hide a measurable part of the gain.
- **C5 fixes the wording only.** No threshold changes.

**(b) The closed set does not say how a key present in only one arm counts.**
- Day 5's `resolved_params_E031_vs_E030.json` listed such keys under `only_one_arm`, outside `outside_closed_set`.
- If CatBoost omits or rewrites `combinations_ctr` at complexity 1, reusing that convention would exempt the key after the fact.
- The proposal's own expected-equal list implies the stricter reading. C6 fixes it.

**(c) Clerical: "more than 75 %" is 74.7 %** (2.96 / 3.96).

**(d) The CTR leakage sentence lost "with ordered permutations".** This is harmless.
- Under `boosting_type: Plain`, CatBoost still computes training-row CTRs over permutations: E031's resolved parameters show `permutation_count` 4 and `counter_calc_method` SkipTest.
- The leakage statement stays correct. Revision 4 concerned the boosting scheme, not the statistics.

**(e) Rung A is reproducible, but it is still one draw.**
- H027 is one realization of the subsampling at seed 42.
- Given D(H028)'s expected distance from both thresholds (about +3.5 s), this cannot move rung A's reading. Record the floor as "at seed 42".

**(f) Operational: the W&B mirror has no timeout of its own.**
- `tracking.sync_safely` runs inside the runner's lock after the worker ends.
- A stalled sync would delay the queue. The start rule turns that delay into deferral, never into a result-dependent choice. It is noted, not required.

### H024 itself

- **The design is unchanged and sound.** The own thresholds now meet the ≥ 2× precedent, and both own readings are bounded and labelled "one draw".
- **INCONCLUSIVE is a likely outcome, and an honest one.** The expected effect (researcher central +1.5 s; mine +1.3 s) sits at the 1.5 s boundary.
- **The bottom line on combinations will usually come from H025's blend-level reading.** It is about half as noisy.

## Novelty Relative to Existing Research

Unchanged from v1:
- No run separates per-key from combination statistics.
- H020 v1's complexity 1 was confounded with the `__RARE__` collapse, and it was rejected.
- Rung B is the control H023 v3 named and did not run. Rung A is the first same-family averaging control.

The batch is not redundant with any completed or rejected work in the journal.

## Experimental Isolation

- **H024 against E031:** one parameter plus the GPU draw. C6 makes the closed-set check closed in fact.
- **The ladder against E033:**
  - rungs B and C differ only in the second half's categorical handling, plus one draw each;
  - rung A replaces the second half and says so.
- **The identity G(X) = G(E033) + D(X) is exact** on identical rows and folds. The readings are stated on D(X), a direct paired comparison.
- **The launcher is now inside the tools freeze.** Its path is in each analysis's freeze diff, and its SHA-256 is pinned.

## Validation Quality

- **Folds:** the frozen folds, unchanged (`config/` diff empty). All 8 folds are predicted, H is never scored, and S1c and W1c are reported.
- **The frozen bootstrap applies unchanged** (`config/splits.yaml`, `promotion`):
  - 2,000 resamples, clustered by airport × UTC day;
  - LOSS when q0.10 > 0;
  - the mean's q0.95, with folds resampled independently.
- **The two reading types are now of comparable strength:** "carries part" needs a mean ≥ +1.0 s and LOSS on at least 3 folds; "carries" needs q95 < +1.0 s.
- **Unchanged and correct:**
  - rule 11, one population per comparison;
  - rule 12 through `range_check.py`;
  - status-only gating;
  - a-priori weights.

## Leakage Review

### Target Leakage

PASS

- There is no new input.
- CTRs are computed by CatBoost from the fold's training rows (`FloatTargetMeanValue` on the raw target; permutation-ordered on training rows). Validation rows use training statistics only.
- The blends read manifest-verified predictions, with weights fixed a priori.

### Temporal Leakage

CONCERN

Inherited and not blocking: FS2's T features, and CTRs over post-validation months in S1 and W1. The causal twins S1c and W1c bound them, and both are reported.

### Competition Availability

PASS

FS2_RAW is available at prediction time. Every component predicts SUBMIT_JAN and SUBMIT_JUL.

## Compute Review

### RAM

PASS

- Expected peak 6.3–7.1 GB (E030 6.40, E031 7.01 GB), against about 9.7 GiB available (9,899 MiB) and the 11 GB hard limit.
- Runs are serialized by the flock, and INC-0012 forbids a concurrent GPU and CPU fit.
- VRAM is at most 4 GB (`gpu_ram_part` 0.4).

### Runtime

PASS

- CLASS-M is right. My central estimate is 420 s (300–700 s); the 1,000 s guard is a safe upper bound.
- The 2,700 s timeout bounds any overrun: started at about 21:01, E036 ends by 21:46 at the latest.

### Disk

PASS

About 60 MB of prediction files.

## Weakest Assumption

**That one GPU draw places H024 − E031 on the right side of 1.5 s.**
- A treatment-free full-size re-draw moved the mean by 0.68 s and W1 by 2.77 s.
- With the expected effect near +1.3 s, the draw alone can decide which own reading is recorded.

## Missing Control or Ablation

- **For H024:** none beyond E031 (the partner) and E030 (the lower bound).
- **For any learner-family claim:** a same-family second half on E031's inputs, or at E031's disagreement level.
  - This was named in v1 and is not required.
  - v2 no longer makes any family claim, so the gap does not bias a reading.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **H024 v2: exactly one allocation,** `uv run python scripts/gate.py allocate H024 v2` (purpose `primary`).
  - It is made second in the batch, so it is expected to be **E036**.
  - The config is the Proposed Change block (seed 42, CLASS-M, folds R1, R2, R3, S1, W1, S1c, W1c, H).
  - It runs by the pinned launcher inside the INC-0012 window, or at a later window under C3.
  - Its own reading follows the Falsification Criterion, with C6. It is a disclosure only: no candidate, no holdout access.
- **The batch conditions below bind every run of H024–H028 v2.** The H025–H028 reviews adopt them by reference.

**C1. Allocation order and id mapping.**
- One allocation per proposal, purpose `primary`, in this order:
  - H026 v2 → E035;
  - H024 v2 → E036;
  - H025 v2 → E037;
  - H027 v2 → E038;
  - H028 v2 → E039.
- Before arming, verify that each `experiments/E03x/gate.json` names that hypothesis and `v2`. Also verify that each `config.yaml` equals the proposal's config block, apart from the header fields `hypothesis_id`, `proposal_version` and `purpose`.
- If any id or config differs, do not arm. The pinned launcher hard-codes the queue and its dependencies, so a mismatch goes back to the Advisor.

**C2. No re-attempt under this ACCEPT.**
- A run ending INVALID, RESOURCE_FAILURE or TIMEOUT, or failing its route check, is recorded as such.
- No `rerun` allocation, and no further allocation of any H024–H028 v2, is authorized here.
- A blend whose component did not end COMPLETE and route-checked is recorded as "not run (component E### <status>)". The batch conclusion is then stated without that rung, as for "not run (window)".
- A run refused before RUNNING (status still ALLOCATED, for example a held lock) counts as deferred.

**C3. A later window.** A deferred allocation runs at the owner's next run window, in batch order, with the same status-only gating and start rule. It is launched in one of two ways:
- by a direct `scripts/run_experiment.py E###` call; or
- by a new launcher whose path and SHA-256 are recorded in the session record before that window opens. It may differ from the pinned file only in the date, the window times and the remaining queue.

The pinned file itself is never edited, because the tools freeze holds until the batch's last comparison.

**C4. Code for the diagnostics and the closed-set check.**
- These cover the residual correlations, the exact decomposition and the resolved-parameter comparison against E031.
- **When:** they are computed after the window, never while the experiment lock is held, and kept memory-light (INC-0008).
- **Where:** no file is added or changed under `src/` or `scripts/` before the batch's last comparison. The code is committed with its output, and the analysis cites it by path and SHA-256.
- **Inputs:** predictions through the manifest-verified loaders, and truth only through `prc.evaluate.truth_frame` (development and diagnostic folds).
- **Delegation:** if the code is delegated under INC-0013, the worker provenance line applies.

**C5. Wording of the readings.**
- A "carries" reading is recorded in its bounded form: "rung X keeps more than about three quarters of E033's −3.96 s at q95 (D(X) q95 < +1.0 s; one draw; at equal weight)". D(X)'s mean, its q95 and the per-fold outcomes are reported beside it.
- If any development fold of D(X) is LOSS, the record adds: "the removed ingredient carries a measurable part smaller than the 1.0 s bound".
- Two phrases are replaced by bounded ones:
  - "E033's margin needs no CatBoost" becomes "a CatBoost half is not shown to be needed beyond the 1.0 s bound, at equal weight";
  - "is a substitute" becomes "is a substitute within the 1.0 s bound".
- No threshold, population or count changes (rule 10).

**C6. The closed exempt set (H024).**
- The comparison covers every key of `resolved_params.json`, on every fold.
- "Expected equal" means present in both arms, with equal values.
- A key present in only one arm is a difference outside the set: the Day 5 `only_one_arm` listing does not exempt it.
- The result, a per-fold list as in Day 5, is written before any H024 or H025 reading.

**C7. Records.**
- Every run still executing at 21:30 is reported as an INC-0012 deviation, with its end time.
- The launcher log is copied into the session record.
- Each analysis states the freeze diff, launcher path included (expected empty).
- The H026 acknowledgement carries the attestation planned in H026 v2.
- The binding ruling of X-D06-S01-0001 stands: E035–E039 are never NEW, rule 10 covers their configurations, and any Day 7 use states the selection.

Required acknowledgement path:
- `research/day-06/acks/H024_ack_v2.md`, referencing the proposal hash `483ed0ab9995a2b067905062213b628b63f85d8f4cebdb10e25aa2188a1b71db` and this review's hash.

## Revision

**None required.**

Non-blocking: points (c) and (e) of Scientific Validity can be corrected in the analysis record.

## Advisor Prediction

Probability of improvement:

| Event (H024 = E036) | P |
|---|---|
| H024 − E031 > 0 on `NM_present_excl_LIRF` (combinations help; point) | 0.82 |
| Own reading "not shown to carry more than 1.5 s" (q95 < +1.5 s) | 0.35 |
| Own reading "combinations carry signal" (mean ≥ +1.5 s, LOSS on ≥ 3 development folds) | 0.30 |
| Own reading INCONCLUSIVE (closed-set violations included) | 0.35 |
| Closed set violated under C6 on any fold | 0.08 |
| Development mean below E030's 446.50 | 0.93 |
| Development mean below E029's 442.45 | 0.42 |
| Runtime above the 1,000 s window guard | 0.06 |
| Status other than COMPLETE | 0.04 |

Expected magnitude:
- **Development mean:** 441.0–445.0 s (central 442.6).
- **On `NM_present_excl_LIRF`:**
  - H024 − E031: −0.2 to +3.0 s (central +1.3); q95 − mean about 0.45 s;
  - H024 − E030: −1.9 to −4.7 s (central −3.6).
- **H024 − E029, all rows:** −1.5 to +2.0 s (central +0.2).
- **Residual correlation with E029, bulk:** 0.84–0.92, about E031's.
- **Resources:** runtime 300–700 s (central 420 s), peak RAM 6.3–7.0 GB, VRAM at most 4 GB.
- **Batch:**
  - P(at least one rung meets the bounded "carries" reading) is 0.60, mostly rung C;
  - P(E038 and E039 both run in today's window) is 0.50: E038 needs E036 done in about 9.5 min, including overheads;
  - P(any run still executing at 21:30) is 0.05.

Primary expected failure mode:
- **The combinations carry about a quarter of E031's −4.91 s.** One draw then lands H024 − E031 between +1.05 and +1.5 s, or above 1.5 s with fewer than 3 LOSSes, so the own reading is INCONCLUSIVE.
- **The usable answer then comes from H025's blend-level D,** whose spread is about half.
