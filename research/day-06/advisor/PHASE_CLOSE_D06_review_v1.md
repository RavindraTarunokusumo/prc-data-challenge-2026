---
schema: advisor-review-v1
hypothesis_id: PHASE_CLOSE_D06
proposal_version: 1
proposal_sha256: b777deb6ef9faf6de2f9339b131aabde1d765e9f2726abb113b14e61b27347f7
exchange_id: X-D06-S01-0004
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.84
created_utc: 2026-10-03T16:24:05Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.84), with binding corrections D6-C6 to D6-C15, ruling H6 and standing rule 14.** The decisions stand. Several Day 6 records claim more than the runs show, so the draft `DAY_SUMMARY.md` may not be marked FINAL as written.

**What stands.**
- **E033 remains champion.** Day 6 had no candidate, so the phase-opening and phase-closing champion are the same run.
  - No Day 6 result contradicts the Day 5 promotion.
  - Against E026, all three blend draws meet criteria 1–3 with 7/7 WIN: E033 −5.62 s, E034 −5.54 s, E041 −5.52 s.
- **The holdout stays closed (ruling H6).** Record "Day 6: 0 of 1, closed unused", not a TIE.
- **Every reading follows its pre-registered rule, and every recomputed figure matches the records.** No reading changes.

**What this review adds.** Five adversarial findings. All are disclosures, not reversals.
1. **Rung B sits on its threshold, and its reading depends on which champion draw is the reference (D6-C6).**
   - On normal taxis, the pre-registered reference E033 is the most favourable of the three measured draws.
   - Against E041, a fixed-seed re-draw of E033's own configuration, D(rung B) is **+0.97 s**, below the +1.0 s "carries part" line.
   - Rungs A and C hold against every draw.
2. **The "statistics" and "combinations" labels are not separated from CatBoost's `data_partition` (D6-C7, D6-C8).**
   - E036 has 9 categorical features with CTRs, and it still resolved DocParallel.
   - That refutes the premise on which Day 5 exempted the key: "FeatureParallel with categorical features, DocParallel without" (H022 v3).
   - Every FeatureParallel run in the repository is a complexity-4 run.
   - Yet the records conclude, from E036's INCONCLUSIVE values, that "the combinations hold all of it".
3. **On the January analogue, the champion's normal-taxi gain depends on the draw (D6-C11).**
   - Clause 1's W1 gain over E029 is −1.59 s (E033), −0.31 s (E034) and **+0.40 s** (E041).
   - The proposed draw record quotes only the all-rows spread (≤ 0.60 s). On the mechanism population the W1 spread is 2.00 s, and rule 13 requires the mechanism figures.
4. **"The champion survives both attacks" overclaims (D6-C12).**
   - The ladder did not test the performance claim, by design. Batch 2 had almost no power.
   - The attacks able to overturn the claim (the 12-month SUBMIT procedure, D3-C3) were not run.
5. **A record misstatement (D6-C13).** E036–E039 never reached W&B, but the record says the runs "were mirrored at completion".

**Answers to the proposal's "Case against".**
- **Item 2 (rung C):** the reading stands with its disclosure, as pre-registered (H024 v2 Falsification Criterion). Relabelling it INCONCLUSIVE now would be a post-hoc change (rule 10). Its label must carry D6-C7.
- **Item 3 (noise):** the figures are stale. With E041 included:
  - the largest measured blend re-draw on normal taxis is +0.36 s (q95 +0.58), and +2.00 s on W1;
  - so 1.0 s is 2.8× the larger mean shift, not "about four times".
- **Item 7 (GPU memory):** disfavoured. E030 and E031 both started at 853 MiB, and resolved DocParallel and FeatureParallel respectively. The partition follows the CTR configuration (D6-C7 (a)).
- **Items 1, 4, 5 and 6:** stated correctly.

**Verified here.** All checks were read-only:
- no fit, no score, and no target read on any fold;
- no December target read, and `holdout_check.py` not run;
- the lock was checked first.

- **Hashes.**
  - The proposal matches the envelope.
  - The six frozen files match `config/frozen.json` (whose own hash is `32c41c0f9331`).
  - The Advisor definition is `30fff5dd…`.
  - `d06_diagnostics.py` is `5fc21113…10b7`, as cited.
- **Lock and memory.**
  - `runtime/experiment.lock` (inode 214027) has no entry in `/proc/locks`. Its `E041` text is the last holder's stamp.
  - No experiment process is running; about 9.6 GiB is available.
- **Tree and freeze.**
  - The tree is clean at `1bf72b6`.
  - `git diff 4ad18a1 day-6 -- src scripts config pyproject.toml uv.lock .claude tests` is empty.
  - Local `main` is stale at `562e29f`; `origin/main` is `4ad18a1`.
- **Holdout.**
  - The task ledger has no `day-06` `holdout_access` event.
  - No Day 6 `metrics.json` scores H: H is predicted only. The `by_wake/H` keys are the Heavy wake class.
- **Allocations and ledger.**
  - E035–E041 follow C1 and N1.
  - Their ledger decisions are null, with roles in `notes`. E033 and E034 remain PROMOTE.
  - `models/champion/CURRENT.json` names E033.
- **Runs.**
  - All seven are COMPLETE, within class, with 0 swap pages. E040 also stayed within CLASS-M (1,497 s, 7.13 GB).
  - Batch 1 ran from 19:00:05Z to 19:29:17Z.
  - The launcher's checkpoint commits stage only each run's own paths.
- **Delegated code** (`d06_diagnostics.py`):
  - The decomposition is exact. The blend residual is (r₁ + r₂)/2 and A = mean((p₁ − p₂)²), with a direct check at a relative 1e-9.
  - The closed-set check counts a key present in one arm only as a violation (C6).
  - Truth is read only through `truth_frame`, on the seven non-holdout folds.
  - The test uses fakes only.
- **Figures recomputed** (from `research/comparisons/` and `research/day-06/eda/`):

| Record figure | Recomputed |
|---|---|
| D(B) +1.34 (q95 +1.65), 5/5 LOSS; G −2.62 | +1.335 (+1.649), 5/5 LOSS; −2.625 |
| D(C) +1.65 (q95 +1.98), 5/5 LOSS; G −2.31 | +1.652 (+1.982), 5/5 LOSS; −2.309 |
| D(A) +2.43 (q95 +2.99), 4/5 LOSS, W1 TIE; G −1.53 | +2.425 (+2.993), 4/5 LOSS, W1 −0.86 TIE; −1.535 |
| E036 − E031 +4.96 (q95 +5.62); E036 − E030 +0.04 | +4.957 (+5.624); +0.042 (q95 +0.898) |
| E041 − E026 −5.52 (q95 −4.67), criteria 1–3, 7/7 WIN | −5.524 (−4.671); `passes_criteria_1_to_3` True; 7/7 WIN |
| \|E041 − E033\| ≤ 0.40 s per development fold | max 0.40 (W1) |
| Blend three-draw spread ≤ 0.60 s (all rows) | R1 0.48, R2 0.25, R3 0.09, S1 0.27, W1 0.60 |
| CatBoost alone up to 1.57 s (W1) | R1 1.06, R2 0.39, R3 0.14, S1 0.65, W1 1.57 |
| Diversity on normal taxis: E030 +4.62 s, RMS 93; E031 −0.30 s, RMS 81; E038 RMS 46 | +4.62, 93; −0.30, 81; 45.5 |
| Closed sets: E036 differs in `data_partition` on all 8 folds; E040 identical (58 keys) | as stated |
| Development means (7 runs, §4 table) | all match `metrics.json` |

## Scientific Validity

### (a) Rung B and the reference draw (D6-C6)

Every ladder contrast D(X) is taken against **E033**. On the same rows and folds, a contrast against any other draw R of the champion is exact by identity: D_R(X) = D(X) − (R − E033). The table uses the stored comparison files only.

| Rung (mean D on `NM_present_excl_LIRF`) | vs E033 (pre-registered) | vs E034 (seed + GPU) | vs E041 (fixed seed) | vs three-draw mean |
|---|---|---|---|---|
| B (E035, codes CatBoost) | **+1.335** | +1.073 | **+0.972** | +1.127 |
| C (E037, complexity 1) | +1.652 | +1.389 | +1.289 | +1.444 |
| A (E039, LightGBM twin) | +2.425 | +2.163 | +2.062 | +2.217 |

- **E033 is the luckiest of the three champion draws on normal taxis.** Its G is −3.96 s, against −3.70 s (E034) and −3.60 s (E041); the three-draw mean is −3.75 s.
  - So every "keeps X % of E033's gain" figure uses the most favourable denominator.
  - Against the three-draw mean, the rungs keep 41–70 %, not 39–66 %.
- **Rung B against E041:** mean +0.97 s; R1 +1.09, R2 +1.84, R3 +1.12, S1 +0.78, W1 +0.03.
  - By the pre-registered rule, that point would be INCONCLUSIVE: the mean is below +1.0 s, and q95 is above +1.0 s.
  - The swing is W1: E033's W1 draw is 2.00 s more favourable than E041's.
- **Rung B's margin over its threshold (+0.34 s) is smaller than one measured fixed-seed blend re-draw (+0.36 s).**
  - E030 is itself one GPU draw, and its re-draw spread is unmeasured.
- **What stands:**
  - the recorded reading, against E033 (rule 10);
  - non-substitution ("no rung carries the gain"), which holds against every draw;
  - rungs A and C, whose readings hold against every draw (all per-fold point contrasts positive except rung A's W1).
- **What must be disclosed:** rung B's "statistics carry part" is at the threshold and depends on the draw.

### (b) Rung C, E036 and `data_partition` (Case against 2 and 7; D6-C7, D6-C8)

| Run | CTR configuration | `n_cat_features` | GPU MiB at start | `data_partition` |
|---|---|---|---|---|
| E030 (Day 5) | none (codes) | 0 | 853 | DocParallel |
| E031 (Day 5) | complexity 4 | 9 | 853 | FeatureParallel |
| E032 (Day 5) | complexity 4 | 9 | 422 | FeatureParallel |
| E036 (Day 6, external holder) | complexity 1 | 9 | 5,150 | DocParallel |
| E040 (Day 6) | complexity 4 | 9 | 688 | FeatureParallel |

- **(a) The memory explanation is disfavoured.** At an identical GPU state (853 MiB), CatBoost resolved DocParallel without CTRs and FeatureParallel at complexity 4.
  - FeatureParallel appears only at complexity 4. That points to the CTR configuration (complexity > 1), not to memory.
  - It cannot be excluded entirely: E036 is the only run made under the external holder.
- **(b) The Day 5 exemption premise is contradicted.**
  - H022 v3 exempted `data_partition` because CatBoost resolves FeatureParallel "with categorical features, DocParallel without". `H022_review_v3.md` (b) accepted this as "CatBoost sets the key from the presence of categorical features".
  - E036 declares 9 categorical features and resolved DocParallel.
  - The exemption's remaining argument ("on one device a layout, not capacity") is reasoned but was never tested on real data.
- **(c) Consequence.** No run varies the partition with the CTR configuration fixed. Three contrasts therefore change the partition together with their treatment:
  - Day 5 finding 1 (E031 − E030, −4.91 s);
  - rung B (E030 against E031 in the blend);
  - rung C and E036 against E031.

  The decomposition is exact on the stored files:

  | Step | Contrast | On normal taxis | `data_partition` |
  |---|---|---|---|
  | per-key CTRs vs codes | E036 − E030 | +0.04 s | matched (Doc / Doc) |
  | complexity 4 vs 1 | E031 − E036 | −4.96 s | changed (Feature / Doc) |

  - Under the Day 5 argument, a partition difference is draw-sized (the full-size re-draw is about 0.7 s), so combinations are the likely carrier of the −4.96 s.
  - The pre-registered closed set nonetheless fired. H024's own reading is INCONCLUSIVE precisely so that this attribution is not recorded as a finding.
- **(d) Records that state the voided attribution.**
  - E036 analysis: "the combinations hold all of it".
  - Journal, batch conclusion: "the complexity-4 combinations are where E031's accuracy comes from".
  - DAY_SUMMARY §6, finding 2: its heading, and "in the blend (rung C) the combinations carry +1.65 s".

  These read INCONCLUSIVE values as a finding, which is a soft re-adjudication (rule 10). They must become values-only wording (D6-C8).
- **(e) The champion is unaffected.** Day 5's accepted scope, "this CatBoost configuration as a whole", attributes nothing to either parameter.

### (c) What the ladder can claim (D6-C9, D6-C10)

- **The pre-registered conclusion when no rung carries the gain:** "at equal weight, neither the codes CatBoost, nor the per-key CatBoost, nor a perturbation twin of E029 substitutes for E031 in the blend. Nothing more is inferred" (H024 §Batch).
- **Three statements infer more than that.** They turn "these three substitutes fall short" into necessity:
  - "the remainder needs E031's configuration" (journal; DAY_SUMMARY §5);
  - "the rest needs E031" (E039 analysis);
  - "each removed ingredient carries a measurable part" (DAY_SUMMARY §1). This one also covers rung B, which sits at its threshold, (a).
- **Finding 3 ("population split", E037 − E035 = −0.64 s on all rows) is a difference of two means.**
  - It is not pre-registered, not bootstrapped, and rests on two GPU draws (E030, E036).
  - Rows outside `NM_present_excl_LIRF` carry the heavy tails (rules 6 and 7).
  - "The per-key statistics help on rows outside `NM_present_excl_LIRF`" is therefore an exploratory observation, not a finding. Rule 11 allows one population per comparison; inferring a subgroup effect from two populations must be labelled as such.

### (d) The draw record and the January analogue (D6-C11)

Clause 1 on `NM_present_excl_LIRF`, the gain over E029 per draw (point estimates; exact identities on the stored files):

| Draw | R1 | R2 | R3 | S1 | **W1** | S1c | W1c | 5-fold mean |
|---|---|---|---|---|---|---|---|---|
| E033 | −3.90 | −4.47 | −4.03 | −5.81 | **−1.59** | −7.29 | −8.29 | −3.96 |
| E034 | −3.66 | −4.54 | −4.10 | −5.87 | **−0.31** | −7.70 | −8.45 | −3.70 |
| E041 | −3.84 | −4.65 | −4.09 | −5.81 | **+0.40** | −7.43 | −8.21 | −3.60 |
| Spread | 0.24 | 0.18 | 0.08 | 0.07 | **2.00** | 0.41 | 0.24 | 0.36 |

- **W1 validates February 2025, the January analogue (`config/splits.yaml`).** On its normal taxis the blend's gain over E029 is present in one draw, near zero in one, and reversed in one.
  - CatBoost alone shows why: E031 is the most favourable of its three draws on W1's normal taxis, by 2.77 s (E032) and 3.94 s (E040; LOSS from a pure fixed-seed re-draw).
- **On all rows, W1 improves over E029 in all three draws:** −2.31, −2.51 and −1.91 s.
  - **69 % of E033's W1 gain sits outside normal taxis.** The ΔSSE shares are: `NM_present_LIRF` 0.30, `NM_missing_other` 0.39 (of which tail 0.23), and normal taxis 0.31. The rows outside normal taxis are 11,755 of 143,732 (8.2 %).
  - The causal twin W1c is stable (−8.21 to −8.45 s). W1 trains on post-validation months; W1c does not.
- **The promotion is not at risk.** Every criterion is against E026 on all rows, and W1 is WIN against E026 in all three draws (−3.19 to −3.79 s).
- **The disclosure is still material.** It updates D5-C9 ("clause 1's W1 reading moved from WIN to TIE"), and Day 7's January claim must not rest on the all-rows spread alone.
- **Rule 13 requires the mechanism-population ΔRMSE per development fold.**
  - The E041 analysis gives only its mean (+0.36 s), and the proposed disclosure omits it.

### (e) "Survives both attacks" (D6-C12)

- H024 §Batch states: "E033's performance claim (criteria 1–8 and the H WIN) is not under test". The ladder could only show that a cheaper construction matches E033. That would be a cost finding, not evidence that E033 is wrong.
- Batch 2 was rated P("draw-fragile") ≈ 0.01, a measurement rather than an attack (`H029_review_v1.md` finding 3, adopted in the acks).
- An accurate §1 says three things:
  - no Day 6 result contradicts the promotion;
  - neither batch had real power against the performance claim;
  - the attacks that do (the 12-month SUBMIT procedure, D3-C3) were not run.
- The attribution part of §1 holds at Day 5's scope, with D6-C6 and D6-C7.

### (f) Process and records (D6-C13, D6-C14)

- **W&B (D6-C13).** The launcher log and `runtime/wandb/` show what happened:
  - E036, E037, E038 and E039 failed to initialise their W&B runs at completion ("runupserter: failed to init run", context deadline exceeded);
  - only E035 (at completion), E040 and E041 synced;
  - the two E035 re-sync attempts after the window (19:34Z, 19:37Z) also failed.

  Two statements are wrong for E036–E039:
  - "The W&B mirror synced each run at completion" (`PRE_WINDOW.md`, after-window section);
  - "runs were mirrored at completion" (DAY_SUMMARY §7).

  The proposal's INC-0009 line is incomplete. The repository records are unaffected.
- **Window timing (D6-C14 (a)).**
  - `d06_diagnostics.py` and the launcher-log copy were written at 19:29:37Z, and `closed_set_E036_vs_E031.json` at 19:29:39Z.
  - That is after the queue ended (19:29:21Z), but about 21 s before the window closed.
  - So "placed after the window" (§8) is inexact, and C4's "after the window" was missed by 21 s for the closed-set output. That output reads two JSON files, no truth, with no lock held and no run in progress, so the slip has no consequence.
  - The truth-reading diversity diagnostic ran at 19:31:49Z, after the window.
- **Provenance (D6-C14 (b)).** `d06_diagnostics_test.py` lacks INC-0013's provenance line. The script carries it, and DAY_SUMMARY §8 covers both files.
- **Checked, with no finding:**
  - the checkpoint commits: own paths only;
  - INC-0012 batch 1: all runs ended by 19:29:17Z; batch 2 ran on the owner's recorded instruction, as an amendment rather than a deviation;
  - the acks: the N4 withdrawals are recorded;
  - D6-C1 to D6-C5: accurate; D6-C5 quotes Day 5 §1 verbatim;
  - no secret appears in any file read.

### (g) Missed forecasts (D6-C15; as D5-C13)

DAY_SUMMARY §7 omits the largest misses, the Advisor's included:
- **E036 − E030:** Advisor −1.9 to −4.7 s (central −3.6); researcher −1.5 to −4.5 (central −3.4). Realised **+0.04**.
- **Closed set violated:** Advisor P 0.08. Violated.
- **Rung C:** Advisor P("carries part") 0.12, with D −0.15 to +1.4 s (central +0.55). Realised +1.65, above the whole range. §7 cites only P("carries") 0.60.
- **H029:** Advisor ±0.7 s on the normal-taxi mean (P 0.75). Realised +0.74, just outside.
- **Advisor record.** The Day 6 reviews expected per-key statistics to carry most of E031's advantage over codes, and rung C most likely to carry. Both were wrong in the same direction.

## Novelty Relative to Existing Research

- **The ladder is not redundant.** It ran the controls H023 v3 named and never ran (the E029 + E030 blend, the per-key split, a same-family twin).
- **Batch 2 is incremental:** a third champion draw for rule 13.
- **Rule 10 is respected.** No configuration was re-submitted as a candidate.
- **Day 6 did not attempt** the open items with the most power against the final claim: SUBMIT, D3-C3, and the audit's causal-only variant (Missing Control).

## Experimental Isolation

- **Rungs A–C each change only the second half** of E033's construction, with E029 byte-identical and manifest-verified. The identity G(X) = G(E033) + D(X) is exact.
- **Rungs B and C carry an unseparated `data_partition` change** with their treatments, (b).
  - For rung C this is disclosed as pre-registered.
  - For rung B it was exempted on a premise that E036 now contradicts.
- **Rung A is deterministic in its own half.** Its floor is "at seed 42".
- **E040 is a pure fixed-seed re-draw.** All 58 resolved keys are equal on every fold. The GPU driver was recorded (N2).
  - Its unevenness (S1 to floating point, the other folds fully re-drawn) is recorded with no seed/GPU split drawn (N4). That is correct.

## Validation Quality

- **Folds and freeze.**
  - The frozen folds were used unchanged; the frozen hashes are intact.
  - All 8 folds were predicted, and H was never scored. S1c and W1c are reported for every contrast.
- **Bootstrap and readings.**
  - The frozen bootstrap applies.
  - The reading rules were pre-registered and applied as written, including C5, C6, N5 and N6.
- **Two gaps, both disclosures:**
  - the noise reference predates E041 (D6-C6);
  - rule 13's per-fold mechanism ΔRMSE is missing from the draw record (D6-C11).
- **The bootstrap excludes the draw, so per-fold labels between draws are descriptive (N4).**
  - Pure re-draws produced LOSS labels: E041 − E033 on R1 and W1c, and E040 − E031 on W1 for normal taxis.
  - The "≥ 3 LOSS" leg of a "carries part" reading therefore adds little beyond the mean leg. That leg is the binding one, and it is the one rung B fails against E041.

## Leakage Review

### Target Leakage

PASS

- Day 6 added no input.
- CatBoost's CTRs are fold-local (`FloatTargetMeanValue` on the raw target, permutation-ordered, SkipTest).
- The blends read manifest-verified predictions, with weights fixed a priori.
- The diagnostics read truth only through `truth_frame`, which refuses H and the final folds.
- No Day 6 record contains an H figure.

### Temporal Leakage

CONCERN

Inherited and not blocking:
- FS2's T features (`MVT − AOBT_3`, `d_sched`);
- CTRs over post-validation months in S1 and W1, bounded by S1c and W1c.

Day 6 adds a related observation: W1's normal-taxi gain varies with the draw, while W1c's is stable, (d).

### Competition Availability

PASS

- Unchanged: FS2/FS2_RAW are available at prediction time.
- The composite SUBMIT path is still to be built and pre-registered on Day 7. H cannot test it, because SUBMIT trains on December.

## Compute Review

### RAM

PASS

- Peaks were 3.37–7.13 GB, none above 8 GB, with 0 swap pages, under the 11 GB hard limit.
- The runs were serialized under the lock.

### Runtime

PASS

All seven runs stayed within class:
- E040 used CLASS-L as ruled, and also stayed within CLASS-M;
- E038 took 909 s against its 1,100 s guard.

### Disk

PASS

About 60 MB per GPU run, covered by the manifests. This review is read-only.

## Weakest Assumption

**That a champion validated on development folds carries its margin into the 12-month SUBMIT fit.**
- The development folds are one draw each, with 8–11 training months. The SUBMIT fit is a fresh draw with all 12 months.
- Day 6 measured the draw spread on development folds only.
- On W1, the January analogue, the CatBoost half's normal-taxi contribution is the least stable quantity measured (−1.59 to +0.40 s).

## Missing Control or Ablation

Named, not required for this close:
- **For any attribution of E031's advantage:** a run that equalizes `data_partition` between complexity 1 and complexity 4.
  - Day 5's synthetic GPU fits showed that both values are accepted in both modes (`H021_review_v2.md`).
  - Without it, "combinations" and "statistics" stay unseparated from the partition mode.
- **For rung B:** a second draw of E030 and its blend. Rung B's reading is within one re-draw of its threshold.
- **For the final claim (Day 7):**
  - a pre-registered check of the SUBMIT procedure;
  - D3-C3's January exposure;
  - the causal-only (P-labelled) variant that `DATASET_AUDIT.md` §6 anticipates for Days 5–7. E021's Day 3 P/T decomposition is the only one, and none exists for E033.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **The Day 6 decisions stand as recorded,** with the disclosures and corrections below.
   - E033 is the phase-closing champion, unchanged.
   - The readings stand as pre-registered:
     - E035 "statistics carry part" (with D6-C6 and D6-C7);
     - E036 own reading INCONCLUSIVE (closed set);
     - E037 "combinations carry part" (with the C6 disclosure and D6-C7);
     - E039 "the twin does not reproduce the gain" (averaging floor −1.53 s at seed 42);
     - E040 "pure fixed-seed re-draw";
     - E041 "robust to one further fixed-seed (GPU-only) draw" (with D6-C11).
   - No ledger decision changes.
2. **Ruling H6: the Day 6 holdout is closed unused.**
   - (a) No access. The frozen `phase_close` comparison would set E033 against itself.
   - (b) Record "Day 6: 0 of 1, closed unused". Do not record a TIE: no comparison was made.
   - (c) No carry-over (rule 9). Day 7 has one access, through a Day 7 allocation as NEW, named by the Day 7 phase close.
   - (d) No substitute comparison. E041 against E026, or any of E035–E041 against E033, on H would be holdout-guided selection.
   - (e) The rule 9 loophole, restated as in ruling H4 item 5. **No `holdout_check.py` invocation with any of E035–E041 as NEW is authorized, in any phase.**
   - (f) H validates December after training on January–November, and SUBMIT trains on December. No H comparison tests the SUBMIT procedure itself.
3. **Disclosures on E033.** These replace the two Day 6 bullets in the draft DAY_SUMMARY §5. Required content:
   - **(attribution)** At equal weight, three substitutes for E031 fall short:
     - each rung's D against E033, with the per-fold outcomes;
     - "keeps 39–66 % of E033's gain on normal taxis, against the most favourable of three champion draws (41–70 % against their mean)";
     - rung B at its threshold (D6-C6);
     - the labels "statistics" and "combinations" not separated from `data_partition` (D6-C7);
     - no necessity claim (D6-C9). The scope remains "this CatBoost configuration as a whole".
   - **(draw record)** Three draws, each pair labelled by type (N5):
     - all rows: the per-fold spread (≤ 0.60 s) and 7/7 WIN against E026 in every draw;
     - **on the mechanism population: the per-fold spread (W1 2.00 s), and clause 1's W1 gain by draw (−1.59, −0.31, +0.40 s), updating D5-C9;**
     - CatBoost alone (W1 1.57 s all rows; 3.94 s on normal taxis);
     - "the evaluated and H figures are one draw; SUBMIT is a further draw" (rule 13).
4. **Corrections.** D6-C1 to D6-C5 (researcher) are accepted. D6-C6 to D6-C15 below are appended. Completed records (E035–E041 analyses, journal entries, Day 5 records, reviews) are not edited; the DAY_SUMMARY draft is.
5. **Incidents.**
   - **INC-0012 closes,** by its own resolution clause. Batch 1 ran inside the window, and batch 2 ran at the owner's recorded instruction.
   - **INC-0013 closes,** with the delegated-work list (script and test) and D6-C14 (b).
   - **INC-0009 stays open,** with D6-C13's facts. **INC-0010 and INC-0004 stay open.**
   - Any new owner instruction on run timing or delegation in Day 7 needs a new incident.
6. **Not authorized:**
   - any holdout access in Day 6;
   - any further allocation, run or fit in Day 6;
   - re-reading any Day 6 reading against another reference as a decision (D6-C6 and rule 14 are disclosures);
   - re-labelling rung C;
   - any edit to a completed record or review;
   - any Day 7 use of an E030–E041 configuration, an average of draws or another weight as a candidate without a new proposal that states the selection (rule 10).

Required acknowledgement path: `research/day-06/acks/PHASE_CLOSE_D06_ack_v1.md`
- It cites the proposal hash (`b777deb6…`) and this review's hash.
- It appends D6-C6 to D6-C15, and records ruling H6 and standing rule 14.

**Corrections** (appended; figures in Scientific Validity):
- **D6-C6. Rung B and the reference draw** (DAY_SUMMARY §1, §4, §6.1; STATE; E035 analysis by appended note; journal by appended note). Record beside rung B's reading:
  - D against E034 +1.07, E041 +0.97 and the three-draw mean +1.13 s;
  - "at the threshold; depends on the draw";
  - E033 is the most favourable draw on normal taxis (G −3.96 against −3.70 and −3.60).

  Also update the noise reference: blend re-draws on normal taxis are +0.26 and +0.36 s (W1 +1.28 and +2.00), so 1.0 s is 2.8× the larger shift.
- **D6-C7. `data_partition`** (journal and STATE pointer beside Day 5 finding 1; E036 and E037 analyses by appended note; DAY_SUMMARY §6):
  - (a) the partition follows the CTR configuration, not GPU memory (same 853 MiB start for E030 and E031);
  - (b) H022 v3's exemption premise is contradicted by E036, and its "layout, not capacity" argument is untested on real data;
  - (c) Day 5 finding 1, rung B and rung C are each "as CatBoost resolves the configuration, `data_partition` included". Day 5's clause 1 reading stands under its closed set (rule 10).
- **D6-C8. INCONCLUSIVE values read as a finding.** Replace with values-only wording ("consistent with"; "not separated from `data_partition`"):
  - "the combinations hold all of it" (E036 analysis);
  - "the complexity-4 combinations are where E031's accuracy comes from" (journal batch conclusion);
  - finding 2's heading, and "the combinations carry +1.65 s" (DAY_SUMMARY §6).
- **D6-C9. No necessity claim.** "Needs E031's configuration" (journal; DAY_SUMMARY §5), "the rest needs E031" (E039 analysis) and "each removed ingredient carries a measurable part" (DAY_SUMMARY §1) become the pre-registered non-substitution sentence, plus the per-rung readings with their disclosures.
- **D6-C10. Finding 3** (DAY_SUMMARY §6; E037 analysis): exploratory. It is a difference of two all-rows means: not pre-registered, not bootstrapped, two draws, heavy-tailed rows. "Per-key statistics help outside `NM_present_excl_LIRF`" is not a finding.
- **D6-C11. The draw record on the mechanism population** (DAY_SUMMARY §5, §6.6; STATE D5-C9; E041 analysis by appended note): the table in (d), and the W1 subgroup shares. Finding 6 adds "on all rows; on normal taxis W1 spreads 2.00 s".
- **D6-C12. §1 wording:** as (e). The "39–66 %" carries its denominator, as in item 3.
- **D6-C13. W&B facts** (`PRE_WINDOW.md` by appended note; DAY_SUMMARY §7; INC-0009 by amendment): as (f).
- **D6-C14. Clerical:**
  - (a) the window timing in (f), in §8 and `PRE_WINDOW.md`;
  - (b) the test file's missing provenance line;
  - (c) the lock file's `E041` text is a stale stamp (no lock held).
- **D6-C15. Missed forecasts** (DAY_SUMMARY §7): add the misses and the Advisor record in (g).

**Standing rule 14 (from this exchange; disclosure only).**
- When several draws of a stochastic reference exist, any reading against that reference also reports the point contrast against each draw, using the exact identity on the same rows.
- The pre-registered reference governs. No threshold, population or count changes.
- Batch conditions B1–B4 are carried.

**Conditions on the phase-closing commit:**
- **DAY_SUMMARY.md** is corrected per D6-C6 to D6-C15 and marked FINAL. §10 records this exchange and ruling H6.
- **STATE.md** is current, with a measured header time. It records:
  - champion E033, with the standing disclosures and item 3's Day 6 additions;
  - "Day 6: 0 of 1, closed unused";
  - the never-NEW list, including E035–E041;
  - standing rules 1–14, and rulings H, B, R, H3, H4, H5, H6, rule L v2 and the hand-off base ruling;
  - the incident states (item 5);
  - the Day 7 next action and open questions (SUBMIT, D3-C3, the causal-only variant, iterations, neural).
- **Journal and ledger.** A Day 6 phase-close journal entry exists, with the appended corrections. The ledger is unchanged.
- **Mirror and registry.**
  - The exchange is mirrored: `envelope.yaml`, `response.md` and `checksums.sha256`.
  - The session registry has an end event for D06-S01.

## Revision

None required for this version. The corrections above are appended under the ACCEPT, as the proposal's item 4 requests.

## Advisor Prediction

These are not about promotion: no candidate and no access are authorized. They concern how the Day 6 findings carry into Day 7.

Probability of improvement:

| Event | P |
|---|---|
| E033 is champion at the Day 7 freeze | 0.80 |
| A fresh draw of E030, blended with E029, gives rung B's D ≥ +1.0 s against E033 | 0.75 |
| The same, against the three-draw champion mean | 0.55 |
| A fourth champion draw has clause 1's W1 gain ≤ −1.0 s | 0.35 |
| A partition-equalized complexity-1 run, if made, recovers ≥ half of E036's +4.96 s gap to E031 | 0.15 |
| The Day 7 SUBMIT procedure is checked by a pre-registered development-fold analogue before submission | 0.60 |

Expected magnitude:
- **Rung B's D against a fresh champion draw:** +0.85 to +1.45 s (central +1.12).
- **Clause 1's W1 gain in a fresh draw:** −1.8 to +0.8 s (central −0.5).
- **All-rows blend spread per development fold over further draws:** ≤ 0.7 s, with 7/7 WIN against E026 in more than 95 % of draws.

Primary expected failure mode:
- The final report quotes the Day 6 labels ("statistics carry part", "the combinations hold E031's advantage") as mechanism findings, without D6-C6 to D6-C8.
- Day 7's January statement rests on W1's all-rows stability, while the January analogue's normal-taxi gain depends on the draw.
