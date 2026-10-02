---
schema: advisor-review-v1
hypothesis_id: H024
proposal_version: 1
proposal_sha256: abdaba7806b306347db048a070cb9cd7baa9a865a133fdc40fb3da88cae05c7d
exchange_id: X-D06-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.88
created_utc: 2026-10-02T17:43:40Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.88).**

- **H024's own design is sound.** It changes one parameter against E031 (`max_ctr_complexity` 4 → 1), and its class is right.
- **The REVISE comes from two sources:**
  - the shared **H024 §Batch**, which H025–H028 adopt unchanged (revisions 1–7 below);
  - two gaps specific to H024 (revisions 8–9).
- **Every required change is text,** except one config value in H027. None needs new compute.

**Batch verdict.**
- **Rungs B and C test the Day 5 attribution properly.**
- **As written, two readings point the wrong way for an adversarial day:**
  - a noisy point estimate would be recorded as "the removed ingredient is not needed";
  - rung A, as labelled, would record a twin that is expected to fail as support for "a second learner family adds signal".

**Verified here.** All checks were read-only: no fit, no score, no truth read, no holdout.

- **Hashes.** All five proposal hashes match the envelope.
- **Lock and memory.** The experiment lock is free. `/proc/locks` holds no `flock` on the inode of `runtime/experiment.lock`, and its `E034` stamp is the last holder's. 9.9 GB was available.
- **Anchor `9045fc5`** holds:
  - the five proposals;
  - the launcher (SHA-256 `6bd1f1248225f856ef0d2b131e269aba38755c53f98860a75c3aab045a449c45`);
  - INC-0012 and the envelope.

  E034 is the last allocation, so the next id is E035.
- **Prediction files.** All 24 prediction files of E029, E030 and E031 match their manifests.
- **Parameter pass-through:**
  - `gbm.catboost` pops only `cat_mode`, so `max_ctr_complexity` reaches `CatBoostRegressor` unchanged;
  - `gbm.lightgbm` passes the subsampling keys and adds `seed`, `deterministic=True` and `force_row_wise=True`.
- **Truth and holdout:**
  - the worker never scores H;
  - `prc.evaluate.truth_frame` refuses holdout and final folds;
  - `prc.blending` reads only prediction files verified against their manifests.
- **The routed ridge does not depend on the seed in practice.** E030 and E031 (seed 42) equal E029 (seed 43) on the routed rows: 0.0 on all 8 folds (`route_check_E030.json`, `route_check_E031.json`).
- **Launcher:**
  - `status()` calls `prc.ledger.get`, which exists, and the status strings match the runner's (`ALLOCATED`, `RUNNING`, `COMPLETE`, `INVALID`, `RESOURCE_FAILURE`, `TIMEOUT`);
  - its log is git-ignored;
  - the zone is Europe/Amsterdam, so 21:00–21:30 local is 19:00–19:30Z;
  - the remote is SSH with no credential helper.
- **`scripts/run_experiment.py::check_config` refuses H027's seed 44 under every purpose.**
  - `primary` and `rerun` require 42, and `reproduction` requires 43 (`config/splits.yaml`, `promotion.reproduction`).
  - See `H027_review_v1.md`.
- **The runner's CLASS-M timeout is 2,700 s** (30 min × `timeout_factor` 1.5). That bounds any overrun of the window.

**The cited figures reproduce:**

| Proposal figure | Source (`research/comparisons/`) | Recomputed |
|---|---|---|
| G(E033) = −3.96 s, WIN on 7 folds | `E033_vs_E029_mech_NM_present_excl_LIRF.json` | −3.960 (q95 −3.521); 7/7 WIN; development-fold mean (−3.905 − 4.468 − 4.029 − 5.808 − 1.592)/5 |
| E033 − E029, all rows −3.58 s | `E033_vs_E029.json` | −3.582 (q95 −3.070); 7/7 WIN |
| Re-draw m = +0.68 s | `E032_vs_E031_mech_NM_present_excl_LIRF.json` | +0.683 (q95 +1.075); **R1 LOSS, W1 LOSS**; W1 +2.77 s |
| E031 − E030 = −4.91 s | `E031_vs_E030_mech_NM_present_excl_LIRF.json` | −4.915 (q95 −4.283); 7/7 WIN |
| E030 − E029, all rows +4.05 s, LOSS on 5 of 7 | `E030_vs_E029.json` | +4.046; LOSS on R1, R2, R3, W1 and W1c |
| Residual correlation E029–E031 | `residual_corr_E029_E031.json` | all rows 0.945–0.985; bulk 0.839–0.920 |
| Runtime and RAM | `experiments/E0xx/resource-usage.json` | E029 893 s / 6.60 GB; E030 225 s / 6.40 GB; E031 1,523 s / 7.01 GB; E032 1,131 s; E033 8 s / 3.38 GB |

## Scientific Validity

### (a) H024 itself

- **It is a clean ablation of E031.** At complexity 1, CatBoost builds the three CTR types per raw key and no products of keys. That also removes the binarized float splits that enter combinations.
- **E031's resolved parameters show where a complexity change could leak into other settings.** The per-fold `resolved_params.json` (R1) records:
  - `simple_ctr`: Borders with 3 priors, FeatureFreq, FloatTargetMeanValue;
  - `one_hot_max_size` 2, `model_size_reg` 0.5;
  - `data_partition` FeatureParallel;
  - 9 categorical features.

  This is why revision 8 asks for a closed exempt set.
- **The question (per-key against interaction statistics) is worth asking.** It splits E031's −4.91 s, and its cost is CLASS-M.

### (b) §Batch: the readings are asymmetric (revision 1)

- **"Rung X carries the blend's gain" needs only D(X) mean < +1.0 s.** No INCONCLUSIVE zone exists below +1.0 s, however wide the interval is.
- **The opposite reading needs more:** mean ≥ +1.0 s *and* LOSS on ≥ 3 of 5 folds.
- **The paired cluster bootstrap does not contain the GPU draw.**
- **The lenient side is the one that would write disclosures on E033.** Examples are "the CatBoost half helps through its learner, not through categorical statistics" and "the combinations are not needed".
- **It is also the side with Day 7 selection value:** rung C as a cheaper substitute.

A claim that an ingredient is *not needed* is a non-inferiority claim, and it needs a bound. "Disclosure only" does not lower that bar. Disclosures on the champion are what Day 7 reasons from.

### (c) §Batch: rung A is mislabelled, and the falsification list overclaims (revision 2)

- **What rung A removes.** It replaces the whole CatBoost half:
  - the learner;
  - FS2_RAW's raw keys (E029 and the twin use FS2's `__RARE__` collapse);
  - the categorical statistics and the CatBoost hyperparameters;
  - most of the disagreement.

  The table's "the different learner family: averaging only" is not what it removes.
- **Its outcome is fixed by design.** The batch cites Krogh & Vedelsby: for a fixed 0.5/0.5 blend, the gain is an exact function of the two components' errors and their disagreement. H027 is built to have little disagreement with E029, with a predicted residual correlation of 0.995–0.999. So its failure follows from its construction, and the researcher gives P 0.03 that it carries the gain.
- **What a rung A LOSS can and cannot show.** It shows that "a perturbation twin at this disagreement is not enough". It cannot show that "a different learner family is needed".
- **H028 labels the expected outcome "the different family carries part" (P 0.90).** It would therefore enter the record as confirmation of the claim under attack.
- **The Day 5 claim it would confirm is broader than what was accepted.** H023 v3 restricted the claim to "this CatBoost configuration as a whole" (revision 6; `H023_review_v3.md`, Experimental Isolation). DAY_SUMMARY §1's "A second learner family adds signal" is broader than that scope. No outcome of this batch can widen it.
- **The other direction stays valid.** "Rung A carries → generic averaging" is a correct inference.

### (d) §Batch: the noise reference (revision 3)

- **The blend re-draw is measured.** "The only measured CatBoost re-draw is E032 against E031" is true of a CatBoost alone, but not at the level of a rung. Comparing `E034_vs_E029_mech_NM_present_excl_LIRF.json` with E033's file shows that the blend re-draw moved:
  - the 5-fold mean by **+0.26 s**;
  - per fold: R1 +0.24, R2 −0.07, R3 −0.08, S1 −0.07, **W1 +1.28**.
- **The 1.0 s threshold is supported:** it is about 4× the measured mean shift.
- **The per-fold rule is not protected against the draw:**
  - W1 alone moved 1.28 s in a blend re-draw;
  - the full-size re-draw E032 against E031, with no treatment at all, was LOSS on R1 and W1 (2 of 5).

### (e) §Batch: "ordered boosting" is wrong (revision 4)

- **Every CatBoost arm here runs `boosting_type: Plain`.** The resolved values are `Plain`, `bootstrap_type: Bayesian` and `random_strength: 1`.
- **What rung B keeps:** oblivious (symmetric) trees with plain boosting and Bayesian bootstrap, on FS2_RAW integer codes.
- **It keeps no ordered boosting.** E030 has no categorical statistics, so it has no permutation-based statistics either. The same error appears in H026's Research Question.

### (f) What the ladder tests

- **Rung B** is the control H023 v3 named and did not run. It decides whether Day 5 finding 1 (the categorical statistics) explains the blend's gain at E033's construction. It is the decisive rung.
- **Rung C** splits finding 1 into per-key statistics and combinations.
- **Rung A** measures the floor that generic averaging reaches with a perturbation twin.
- **The batch attacks attribution only.** E033's performance claim (criteria 1–8 and the H WIN) is not under test here. That is legitimate for this batch, and the Day 6 record should say so.

### (g) H024's own reading (revisions 8 and 9)

- **The threshold is close to the noise.** At full size, 1.0 s is 1.47× the measured re-draw (+0.68 s).
- **The project's own precedent asks for more.** H021 v3's noise condition read clause 1 as INCONCLUSIVE when "the −3.0 s floor would then be less than twice the GPU and seed noise".
- **Both of H024's readings sit within reach of one draw:**
  - a pure re-draw gave 2 LOSSes and moved W1 by +2.77 s;
  - H024 holds one draw.

## Novelty Relative to Existing Research

- **H024 is not redundant.** Day 4's H020 v1 used complexity 1 as a confounded capacity choice, together with the `__RARE__` collapse, and was rejected (journal, X-D04-S01-0001). Here complexity is the isolated variable, on FS2_RAW, with E031 as the partner. No run separates per-key from combination statistics.
- **Rung B is new as an experiment.** It is the control named in `H023_review_v3.md` (Missing Control) and excluded from that chain's authorization (item 6). A new proposal is the right route.
- **Rung A is the first same-family averaging control.** Its information value is modest (Scientific Validity (c)).

## Experimental Isolation

- **H024 against E031:** one parameter plus the GPU draw. Revision 8's closed set makes this checkable before the reading.
- **Ladder, against E033:**
  - rungs B and C differ only in the second half's categorical handling (plus one draw);
  - rung A differs in everything about the second half.
- **The identity G(X) = G(E033) + D(X) is exact.** Both sides are means of per-fold RMSE differences on identical rows. Stating the readings on D(X), a direct paired comparison against E033, is the right design.
- **The launcher is a tool that decides start and deferral, but it sits outside the tools freeze** (revision 7(a)).

## Validation Quality

**Correct:**
- the frozen folds, unchanged, with all 8 folds predicted and H never scored;
- readings on the 5 development folds, with the twins reported through `mechanism_check.py` and `compare.py`;
- rule 11's two populations, one per comparison;
- rule 12 through `range_check.py`;
- gating by status only, with no accuracy condition;
- weights fixed a priori.

**Gaps:**
- the asymmetric readings (revision 1);
- rung A's labelling (revision 2);
- the noise reference (revision 3);
- the diversity diagnostic's population (revision 5);
- deferral (revision 6).

## Leakage Review

### Target Leakage

PASS

- There is no new input.
- CTRs are computed by CatBoost from the fold's training rows (`FloatTargetMeanValue` on the raw target, Advisor-verified on Day 5).
- Blends read only manifest-verified predictions, with weights fixed before any component exists.

### Temporal Leakage

CONCERN

This is inherited and not blocking, as in `H023_review_v3.md`: FS2's T features, and CTRs over post-validation months in S1 and W1. The causal twins S1c and W1c bound them, and both are reported.

### Competition Availability

PASS

FS2_RAW is available at prediction time. Every component can predict SUBMIT_JAN and SUBMIT_JUL.

## Compute Review

### RAM

PASS

- Expected 6.3–7.1 GB, against E030's 6.40 and E031's 7.01 GB. That is inside CLASS-M's 8 GB and the 11 GB hard limit.
- INC-0012 already forbids running a GPU and a CPU fit concurrently.
- VRAM is at most 4 GB (E031's device-wide peak was 3,956 MiB).

### Runtime

PASS

- CLASS-M is right. E030 took 225 s and E031 1,523 s, and the Day 4 calibration found cost linear in iterations at complexity 1.
- The 1,000 s pessimistic figure is a plausible upper bound. The overrun bound (2,700 s timeout) is revision 7(b).

### Disk

PASS

About 60 MB of prediction files.

## Weakest Assumption

**That one GPU draw can place H024 − E031 on the right side of a 1.0 s threshold.** The threshold is 1.47× the measured full-size re-draw, and that re-draw alone produced 2 LOSSes.

## Missing Control or Ablation

- **For H024:** none beyond E031 (the partner) and E030 (the lower bound), provided revision 8's closed set is added.
- **For any "learner family" claim in the batch:** a same-family second half that matches E031's inputs (FS2_RAW's raw keys) or E031's disagreement with E029.
  - This is named, not required here.
  - It is also D4-C7's open question ("LightGBM already holds the keys").

## Decision

REVISE

## Execution Authorization

Authorized scope:
- **None.** REVISE never permits execution.
- No allocation of E035–E039 under v1.

Required acknowledgement path:
- None for v1.
- v2 goes to a new exchange. After an ACCEPT, its acknowledgement is `research/day-06/acks/H024_ack_v2.md`.

## Revision

**Required: §Batch.** These apply to H025–H028 through their pointer.

1. **Make every "not needed" reading a bounded statement.**
   - "Rung X carries the blend's gain" needs a condition of strength comparable to the opposite reading's. One example is the bootstrap q95 of D(X)'s mean below +1.0 s. Another is a stated per-fold condition.
   - Everything else becomes INCONCLUSIVE.
   - State that the bootstrap excludes the GPU draw.
2. **Restate rung A.**
   - **(a) The ladder table.** Rung A removes the whole CatBoost half: learner, raw keys, statistics and hyperparameters. It keeps a perturbation twin of E029 whose disagreement is small by design.
   - **(b) Its LOSS reading.** It reads: "a perturbation twin of E029 at its measured disagreement does not reproduce the gain; G(H028) is the generic-averaging floor at that disagreement".
     - It is not labelled "the different family carries part".
     - It is not counted as support for "a second learner family adds signal".
   - **(c) The batch conclusion.** Replace "No rung carries it → each removed ingredient is needed; the Day 5 reading survives three attacks" with a conclusion that claims nothing about "family".
     - Any family claim stays at H023 v3's accepted scope, "this CatBoost configuration as a whole".
     - No outcome of this batch widens DAY_SUMMARY §1's broader phrase.
   - **(d)** "Rung A carries → generic averaging" stays as written.
3. **Noise reference.**
   - For the blend rungs, cite the measured blend re-draw: +0.26 s on the 5-fold mean, W1 +1.28 s (from `E034_vs_E029_mech_NM_present_excl_LIRF.json` against E033's file).
   - Correct "the only measured CatBoost re-draw".
   - State that the per-fold outcome rule does not include the draw. A treatment-free re-draw (E032 against E031) gave LOSS on R1 and W1.
4. **Correct "ordered boosting".** Use plain boosting, Bayesian bootstrap and oblivious trees on FS2_RAW codes, in the rung B bullet of "What would falsify".
5. **Diversity diagnostic on the readings' population.** Report the residual correlation on `NM_present_excl_LIRF` for each second half: E030, H024, H027, and E031 for reference. Keep all rows and bulk beside it. Rung A's restated reading (2(b)) cites it.
6. **Deferral is status-only in both directions.**
   - A deferred allocation runs at the owner's next window, whatever the other rungs show.
   - If no window comes before the Day 6 phase close, it is recorded "not run (window)". The batch conclusion is then stated without that rung, and nothing is inferred about it.
7. **Launcher (criterion 7, isolation).**
   - **(a) Pin it.** Give the launcher's path and SHA-256 in the batch text, and add its path to each analysis's freeze diff.
   - **(b) Bound the overrun.** State how far a run can overrun and how that is handled.
     - The launcher never kills, and the CLASS-M timeout is 2,700 s.
     - E035 started at 21:00 may therefore run to 21:45, and E038 started at 21:14:10 to 21:59.
     - Any run still executing at 21:30 is reported, with its end time, as an INC-0012 deviation in the session record.

**Required: H024 only.**

8. **Closed exempt set against E031** (the H022 v3 precedent; rule (i) of `H022_review_v2.md`). Fix before the run which resolved keys may differ.
   - **Expected difference:** `max_ctr_complexity` only.
   - **Expected equal:** the `combinations_ctr` text, `data_partition`, `one_hot_max_size`, the CTR descriptions, `model_size_reg`, `border_count`, `bootstrap_type` and `n_cat_features`.
   - **If violated:** a difference outside the set on any fold makes H024's own reading INCONCLUSIVE. Rung C's reading then carries the disclosure.
9. **H024's own thresholds against the measured re-draw.**
   - Justify 1.0 s, which is 1.47× +0.68 s, against H021 v3's 2× noise precedent, or restate it.
   - The "no measurable signal" side takes revision 1's bound.
   - Its label must say what one draw can show, for example "combinations not shown to carry more than X s".

**Ruling (binding on every version of this batch; no revision needed).**
- The batch's experiments (E035–E039, or whatever ids they take) join STATE's "never NEW, in any phase" list.
- Rule 10 covers their configurations: no unchanged re-submission as a candidate.
- A Day 7 proposal built on a rung reading is a new configuration and states the selection (Day 5 phase close (g)).

**Recommended (non-blocking).**
- **Staging.** `checkpoint` should stage only the run's own paths (`experiments/<E###>/`, `experiments/ledger.jsonl`, `research/comparisons/route_check_<E###>.json`), not `git add -A`.
- **Clean tree.** Re-check a clean tree at window open, not only at arming.
- **Time zone.** Pin `TZ=Europe/Amsterdam`, or compute the window from UTC.
- **Push.** Use `GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=10'` and a push timeout, so a push cannot stall the queue.
- **Order** (the researcher's choice). Under the v1 order, an E035 overrun past about 21:29 defers rung B, the cheapest and most decisive rung (about 1 min, no dependency). Running it first costs about a minute.
- **E038's pessimistic 950 s** is 6 % above E029's measured 893 s, and the speed-up from subsampling is assumed.
- **The exact ambiguity decomposition, per fold, for each rung.**
  - For a fixed 0.5/0.5 blend on the same rows, MSE_blend = ½ MSE₁ + ½ MSE₂ − ¼ mean((p₁ − p₂)²). This is an identity.
  - It separates "less accurate" from "less different", which is what H026's and H028's alternative explanations ask.
  - It can be computed after the window from stored predictions and development truth.
- **INC-0012 wording.** Its "No file under the repository changes during the window" should read "no file outside the running experiment's own records".
- **Delta review.** A v2 that changes only these items can be reviewed against this list.

## Advisor Prediction

These are for H024's run once the batch is revised. Nothing below changes with the text revisions.

Probability of improvement:

| Event | P |
|---|---|
| H024 − E031 > 0 on `NM_present_excl_LIRF` (combinations help; point) | 0.80 |
| v1 "combinations carry signal" (≥ +1.0 s and LOSS on ≥ 3 development folds) | 0.40 |
| v1 "no measurable signal" (point < +1.0 s) | 0.42 |
| The same, with the bootstrap q95 of the mean < +1.0 s (bounded form) | 0.22 |
| H024 development mean below E030's 446.50 | 0.93 |
| H024 development mean below E029's 442.46 | 0.40 |
| Resolved parameters differ from E031 outside `max_ctr_complexity` | 0.10 |
| Runtime above the 1,000 s window guard | 0.08 |
| Run INVALID from a parameter or fit error | 0.03 |

Expected magnitude:
- **Development mean:** 441.0–445.5 s (central 442.9).
- **On `NM_present_excl_LIRF`:**
  - H024 − E031: +0.2 to +3.0 s (central +1.3);
  - H024 − E030: −1.9 to −4.7 s (central −3.6).
- **H024 − E029, all rows:** −1.2 to +2.5 s (central +0.4).
- **Resources:** runtime 300–750 s (central 480 s), peak RAM 6.3–7.0 GB, VRAM at most 4 GB.
- **Batch:**
  - P(at least one rung meets a bounded "carries" reading) is 0.40, mostly rung C;
  - P(E038 runs in today's window, under the v1 order) is 0.65.

Primary expected failure mode:
- **The combinations carry a modest part of E031's −4.91 s,** about a quarter.
- **One GPU draw then lands H024 − E031 near the 1.0 s threshold,** within about one re-draw of it. The own reading is INCONCLUSIVE under a bounded rule, and draw-dependent under v1's point rule.
