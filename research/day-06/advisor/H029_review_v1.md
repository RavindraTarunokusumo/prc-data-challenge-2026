---
schema: advisor-review-v1
hypothesis_id: H029
proposal_version: 1
proposal_sha256: 8511f3a17462e52634efcbe58aa7b141b40a277b10dadb6a3288df5c8944a802
exchange_id: X-D06-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-10-03T08:41:46Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.80), with binding conditions N1–N8.** This file also holds the shared batch findings. `H030_review_v1.md` adopts N1–N8 by reference.

**The design is clean and cheap.**
- The config block equals `experiments/E031/config.yaml` apart from the header fields (parsed YAML comparison). It uses the same seed and covers all 8 folds.
- Gating is status-only. Deferral, overrun and failure handling are pre-registered.
- Nothing is a candidate, nothing touches the holdout, and E040 and E041 are never NEW.

**The batch claims more than a seed-42 refit can show.** There are four findings. Conditions on the records settle all four. None changes a design, threshold, population or fold.

1. **E040 is not "the draw Day 7's submission will be".**
   - SUBMIT fits train on 12 months (`SUBMIT_JAN`, `SUBMIT_JUL`). The phase close already ruled that their CatBoost half "will be a fresh draw" (X-D05-S05-0001, Competition Availability). The integer 42 does not carry a draw from one training set to another.
   - Holding the seed fixed against E031 holds every seeded part of the fit fixed. In E031's resolved parameters these are the Bayesian bootstrap (`bagging_temperature` 1), the score perturbation (`random_strength` 1) and the 4 CTR permutations.
   - E040 − E031 therefore isolates GPU run-to-run variation. That should be no larger than the seed + GPU variation that E032 − E031 already sampled, and seed + GPU variation is what a fresh SUBMIT draw carries.
   - N4 and N5 fix the wording.
2. **The byte-identity question is already answered.**
   - Day 5's calibration fitted E031's exact parameters twice at `random_seed=42`, on R3's real training rows (1,757,038 rows, permuted target). The record is `h021_exact` in `research/day-05/eda/gpu_calibration.json`.
   - The two prediction hashes differ: `bc3d6aa3dfb6` against `96d5675b6981`.
   - The proposal's P 0.10 ignores this evidence; my estimate is 0.01.
   - If a byte-identical outcome did occur, H030's "draw-robust" reading would be reached without any new draw. N5 closes this branch.
3. **The attack on the performance claim has almost no power.**
   - E033's narrowest margin over E026 is W1 (q90 −1.98 s). S1's q90 is −3.29 s. Criterion 1's mean is −5.62 s (q95 −4.79).
   - The largest blend re-draw movement so far is 0.48 s.
   - P("draw-fragile") ≈ 0.01.
   - The batch is a measurement for rule 13 and for Day 7's reproducibility statement (open question 2). It cannot realistically show that E033 is wrong. It is worth one window at this cost, provided the record does not present a pass as more than that.
4. **The CLASS-L justification cannot be inherited.**
   - `H021_review_v3.md` granted CLASS-L "for H021 and H021r only".
   - I rule CLASS-L justified for H029 v1 only (Compute Review). Two conditions come with it: H021's reporting conditions (N8) and a recorded overrun bound (N2).

**Verified here.** All checks were read-only: no fit, no score, no target column read on any fold, no holdout access, and `holdout_check.py` was not run.
- **Hashes.**
  - Both proposals match the envelope.
  - The launcher `research/day-06/sessions/D06-S01/run_window_2.sh` hashes to `edfe11dfd7e5f690a722fd05e5050213fbede60b3a8ede00355c8a3e08dadf3e` on disk and at `9d245c0`. Its diff against the pinned `run_window.sh` touches only the header comment, the date, the log name and the queue.
  - That hash is recorded in INC-0012's 2026-10-03 amendment. It is not in the envelope's constraints, although H029 §Batch says it is (clerical; N2 pins it).
  - `research/day-06/eda/d06_diagnostics.py` is `5fc21113…10b7`.
  - The Advisor definition is `30fff5dd3c54`, as in `config/agents.yaml`.
  - The six frozen files match `config/frozen.json`. That file's own hash, `32c41c0f9331`, is the one recorded in E031's and E032's `gate.json`.
- **Anchor `9d245c0`** is the commit that submits this envelope.
  - `git diff 4ad18a1 9d245c0`, and the working tree against `9d245c0`, are both empty on `src`, `scripts`, `pyproject.toml`, `uv.lock`, `config`, `d06_diagnostics.py` and `run_window_2.sh`.
  - `uv.lock` is `efa4fd78…`, as rule L v2 item 6 requires.
- **Lock, memory and GPU.**
  - `/proc/locks` shows no lock on `runtime/experiment.lock` (inode 214027). The `E039` text in the file is the last holder's stamp.
  - No experiment process is running. I took and released one non-blocking shared `flock` as a probe.
  - About 9 GiB of RAM is available.
  - The GPU is an RTX 5060 Laptop (driver 591.91, CUDA 13.1), with 673 of 8,151 MiB in use at 08:32Z.
- **Allocation state.** No `experiments/E04x` directory and no ack exist. The task ledger has no E04x allocation, so the next id is E040.
- **Configs and inputs.**
  - H030's block differs from E033's config only in the second component.
  - All 40 stored prediction files of E029, E031, E032, E033 and E034 match their manifests (byte hashes only).
  - `prc.blending` refuses a component that is not COMPLETE or whose file does not match its manifest. It computes a fixed linear sum, so E041 − E033 = ½ (E040 − E031) row by row.
- **Runner.**
  - `check_config` requires seed 42 for purpose `primary`.
  - The CLASS-L timeout is 90 × 60 × 1.5 = 8,100 s. The hard RAM limit is 11 GB.
- **Diagnostics.** `d06_diagnostics.py` defines "ambiguity" as mean((p1 − p2)²), so √A is the full RMS prediction change. I checked this because the usual ensemble convention would halve it.
- **Figures reproduced:**

| Proposal figure | Recomputed |
|---|---|
| E033 − E026: −5.62 s (q95 −4.79), 7/7 WIN | −5.618 (q95 −4.787); 7/7 WIN |
| E034 within 0.48 s of E033 on every development fold | largest: R1 +0.478 |
| E032 − E031: R1 +1.06, W1 −0.73 | +1.056, −0.725 |
| Clause 1's W1 reading moved from WIN to TIE | −1.592 (WIN), then −0.310 (TIE) |
| E031 1,523 s / 7.01 GB; E032 1,131 s / 7.08 GB | as stated |
| (context) E032 − E031 on `NM_present_excl_LIRF` | +0.683 (q95 +1.075); LOSS on R1 and W1 from a pure re-draw |
| (context) E031 against E032 resolved parameters | only `random_seed` differs, on all 8 folds; `data_partition` is FeatureParallel in both |
| (context) D5-C10 rows, stored predictions | 192622644 (S1): E031 10,976, E032 10,237, E033 9,008, E034 8,639. 183910286 (W1): E031 22,233, E032 18,605, E033 15,086, E034 13,272 |

## Scientific Validity

**(a) What a same-seed refit measures.**
- Only two things can differ between E040 and E031:
  - the order of the GPU's floating-point reductions;
  - any change to the environment outside rule L v2 item 6. The GPU driver is not recorded in any manifest (see Experimental Isolation).
- Everything seeded is shared: bootstrap weights, score noise and CTR permutations.
- E040 − E031 is therefore the fixed-seed part of the draw spread. E032 − E031 sampled the seed + GPU spread.
- Once E040 exists, the three draws give:
  - two seed + GPU pairs: E032 − E031 and E040 − E032;
  - one fixed-seed pair: E040 − E031.

  With one or two pairs of each type, the spread cannot be split into a seed part and a GPU part (N4).
- **What this gives Day 7:** a full-size, real-target measurement of how closely a re-run of a fixed-seed fit reproduces its predictions in this environment. That belongs in the final report's reproducibility statement. It does not measure the SUBMIT draw's performance variance.

**(b) Byte-identity.**
- The reading is decisive and costs nothing extra, so it stays as registered.
- Its expectation (P 0.10) and the Alternative Explanations sentence are not supported:
  - Day 5 already showed that this exact configuration is non-deterministic at a fixed seed;
  - "Day 7's seed-42 fit reproduces E031 exactly" would be false even if the fit were deterministic, because the SUBMIT folds train on other months.
- N4 keeps that sentence out of every record.

**(c) Draw variation is not bootstrap variation.**
- The frozen bootstrap resamples airport × day clusters for one fixed pair of prediction vectors. It does not include the draw.
- E032 − E031, a pure re-draw, came out LOSS on R1 and W1 on `NM_present_excl_LIRF`.
- `compare.py E040 E031` will label folds WIN, TIE or LOSS. Between two draws of one configuration these labels are descriptive. They are never evidence of a configuration difference (N4).

**(d) H029's own readings** are descriptive, pre-registered and exhaustive: either byte-identical, or the spread reported beside E032's. The expectations are concrete enough to score afterwards.

**(e) Single rows (D5-C10).**
- Reporting E040's predictions on rows 192622644 and 183910286 beside E031's and E032's is the right check. These rows carry part of the margins:
  - row 192622644 carries −0.41 s of S1's −4.17 s;
  - row 183910286 carries −1.03 s of W1's −3.59 s.
- E032's values come from its stored predictions, without truth (table above). The two CatBoost draws so far differ by −739 s and −3,628 s on these rows.
- The consequence for H030's S1 tolerance clause is in `H030_review_v1.md`.

## Novelty Relative to Existing Research

- **Byte-identity:** redundant with Day 5's `h021_exact` calibration, which the proposal does not cite.
- **New:** the full-size spread at a fixed seed, on the real target, across all 8 folds. It also gives a third draw of the CatBoost half for rule 13's min–max.
- **Not a re-submission.** Rule 10 covers E031's configuration as a candidate. This run is a control and never NEW, and the X-D06-S01-0001 ruling extends to it.
- It is not redundant with any rejected work in the journal.

## Experimental Isolation

- **Against E031, everything is equal by construction:**
  - the config (parsed-equal);
  - the seed, silver, `uv.lock` and libraries.

  The intended single difference is GPU run-to-run variation.
- **Two things could break this.**
  - **A resolved-parameter difference.** CatBoost picks some GPU settings itself: E036 resolved `DocParallel` where E031 resolved `FeatureParallel`. E031 and E032 agreed on every key except the seed, so I put this at P ≈ 0.04. N6 requires the check before any reading.
  - **An environment change outside rule L v2 item 6.** No manifest records the GPU driver. INC-0007 records only "CUDA 13.1 driver", so E031's exact driver is unknown. Today it is 591.91 with CUDA 13.1. N2 records it, and any known change is disclosed beside the H029 reading.
- **Against E032:** the seed and the draw both change. This gives the second seed + GPU pair.

## Validation Quality

- **Folds:** the frozen folds, unchanged (the `config/` diff is empty). All 8 folds are predicted. H is never scored. S1c and W1c are reported.
- **Comparisons:** `compare.py` and `mechanism_check.py` with the frozen bootstrap, read as in (c).
- **Rule 13** (per development fold and twin: all rows, `NM_present_excl_LIRF`, RMS prediction change) is covered.
  - √A from the d06 `diversity` subcommand is the correct RMS change.
  - The script reads truth only through `truth_frame`, and never reads H.
- **Rule 11:** E032's figures shown beside E040's must come from the same script and the same populations. The phase-close table used non-routed rows (N7).
- **`reproduce_check.py`** is correctly not used. It requires the same hypothesis version.

## Leakage Review

### Target Leakage

PASS

- There is no new input.
- CatBoost computes the CTRs within each fold's training rows: `FloatTargetMeanValue` on the raw target, permutation-ordered, with `counter_calc_method` SkipTest. Validation rows use training statistics only.

### Temporal Leakage

CONCERN

Inherited, not blocking, and unchanged here:
- FS2's T features (`MVT − AOBT_3`, `d_sched`);
- CTRs computed over post-validation months in S1 and W1.

The causal twins bound both: E033 is WIN against E026 on S1c (−6.39 s) and on W1c (−6.82 s).

### Competition Availability

PASS

- FS2_RAW is available at prediction time.
- The configuration can predict SUBMIT_JAN and SUBMIT_JUL.
- Raw levels unseen before 2026 are at most 0.43 % of rows.

## Compute Review

### RAM

PASS

- Expected peak 7.0–7.1 GB (E031 7.01, E032 7.08), against the 11 GB hard limit and about 9 GiB available.
- One run at a time (flock), and no concurrent CPU fit (INC-0012).
- About 3.1 GB of VRAM is attributable to the run (E031: 3,956 − 853 MiB).
- **GPU risk:** an external holder like 2026-10-02's (4.3–5.2 GB) would leave about 3.0–3.9 GB, so a GPU allocation failure is possible. That would end as RESOURCE_FAILURE, with no re-attempt (N3). I recommend a check at arming (Revision).

### Runtime

PASS

**CLASS-L ruling (brief §4): justified, for H029 v1 only.**
- **The proposal's justification does not carry over.**
  - `H021_review_v3.md` granted CLASS-L "for H021 and H021r only".
  - That ruling rested on P(> 30 min) ≈ 0.65, with a promotion's criterion 7 at stake.
  - Measurements have since replaced the estimate (25.4 and 18.8 min), and E040 is a control, with no criterion 7.
- **CLASS-L is justified on other grounds.**
  1. Brief §4 names confirmation runs as a use of CLASS-L. E040 is a confirmation draw of a CLASS-L configuration.
  2. Measured peak RSS is 0.9 GB under CLASS-M's 8 GB, and runtime used up to 85 % of CLASS-M's 30 min. A CLASS-M `within_class` failure is plausible (P ≈ 0.09) and would carry no information.
  3. Keeping E031's `job_class` keeps every config field equal to E031's, so N1's identity check is exact.

  CLASS-M would also have been acceptable.
- **The cost is a longer overrun bound.**
  - The launcher never kills a run. For E040, CLASS-L's 8,100 s timeout therefore replaces the 2,700 s bound written in INC-0012's first amendment.
  - A run that starts at 21:00 could in principle continue to about 23:15 local. N2 records this before the window.
- **Window arithmetic:**
  - E040 must start by 19:03:20Z;
  - a 1,131–1,523 s run ends about 19:19–19:26Z;
  - P(runtime > 1,600 s) ≈ 0.12, and P(still running at 21:30 local) ≈ 0.06;
  - E041 needs E040 finished, route-checked, checkpointed and W&B-synced by 19:29:00Z: P ≈ 0.78.
- **Conditions:** items 2–4 of `H021_review_v2.md`, applied through N8.

### Disk

PASS

About 60 MB of predictions, curves and resolved parameters, covered by the manifest.

## Weakest Assumption

**That a fixed-seed refit on the development folds informs the variance of the Day 7 SUBMIT predictions.**
- At best it gives a lower bound on that variance.
- The SUBMIT fit differs in three ways:
  - its training months (12, including December);
  - how its seeded random stream plays out on that data;
  - its procedure: the composite SUBMIT path does not exist yet (X-D05-S05-0001, Weakest Assumption).
- What the batch honestly produces is a reproducibility measurement and one more draw.

## Missing Control or Ablation

- **For H029's own readings:** none. E031 is the identical-configuration reference, and E032 is the seed + GPU reference.
- **Named, not required:**
  - **For a fresh draw, the relevant pair is a different-seed pair.** With E040 present, that pair is E040 − E032. It is reported through N5's labelled min–max.
  - **The untested part of the champion's Day 7 claim is the 12-month composite SUBMIT procedure.** No re-draw on the development folds can test it, and Day 7 must pre-register it.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **H029 v1: exactly one allocation,** `uv run python scripts/gate.py allocate H029 v1` (purpose `primary`).
  - It is made first in the batch, so it is expected to be **E040**.
  - The config is the Proposed Change block: seed 42, CLASS-L (ruled above), folds R1, R2, R3, S1, W1, S1c, W1c, H.
  - It runs by `run_window_2.sh` (SHA-256 `edfe11df…dadf3e`) in the 2026-10-03 19:00–19:30Z window, or at a later owner window under N3.
  - Its readings follow H029 §Batch, with N4–N6.
  - It is a control only: no candidate, never NEW, no holdout access, and its ledger decision is null.
- **No reproduction, `rerun` or further allocation** of H029 v1 or H030 v1 is authorized.
- **N1–N8 bind every run of the batch.** `H030_review_v1.md` adopts them.

**N1. Allocation order, ids and config identity.**
- Allocate H029 v1 first (expected E040), then H030 v1 (expected E041). Each gets one allocation, purpose `primary`.
- Before arming, verify:
  - each `gate.json` names its hypothesis and `v1`;
  - E040's `config.yaml` equals `experiments/E031/config.yaml` apart from `hypothesis_id` and `proposal_version` (parsed YAML);
  - E041's `config.yaml` equals the H030 block, apart from the header fields.
- If any id or config differs, do not arm. The launcher hard-codes E040, then E041.

**N2. Launcher and pre-window record.**
- **Launcher:** `run_window_2.sh`, SHA-256 `edfe11dfd7e5f690a722fd05e5050213fbede60b3a8ede00355c8a3e08dadf3e`.
  - It is not edited before the batch's last comparison.
  - A later window uses either a direct `run_experiment.py` call or a new launcher recorded beforehand, as in C3 of `H024_review_v2.md`.
- **Pre-window record.** Written for this batch before arming, it states:
  - the N1 checks;
  - the launcher hash and its diff against `run_window.sh`;
  - the freeze diff from `9d245c0` (expected empty);
  - the rule L v2 item 6 environment;
  - the GPU name, driver and CUDA version, and the GPU memory in use at arming;
  - **E040's overrun bound:** the CLASS-L timeout of 8,100 s, which replaces INC-0012's 2,700 s bound for this run.

**N3. Failures and deferral.** As in H029 §Batch:
- There is no re-attempt and no `rerun`.
- If E040 does not end COMPLETE and route-checked, E041 is recorded as "not run (component E040 <status>)".
- A refusal before RUNNING counts as a deferral.
- Deferral depends on status only, and moves the run to the owner's next window. If no window comes before the phase close, the run is recorded as "not run (window)".

**N4. How every record describes E040.**
- E040 is one further draw of E031's configuration. Against E031 it measures fixed-seed GPU run-to-run variation, plus any environment change disclosed under N2.
- No record may:
  - identify E040 or E041 with the Day 7 SUBMIT draw;
  - repeat H029's statement that a byte-identical refit would mean "Day 7's seed-42 fit reproduces E031 exactly";
  - split the spread into a seed part and a GPU part from one pair of each type;
  - read a WIN, TIE or LOSS between draws as an effect of configuration.

**N5. Reading rules (H030, plus H029's byte-identity branch).**
- **"Criteria 1–3 hold"** means the `passes_criteria_1_to_3` field of `compare.py E041 E026`, under the frozen text, not §Batch's paraphrase:
  - criterion 1: point estimate ≤ −1.0 s and q95 < 0;
  - criterion 2: at least 3 WIN, S1 WIN, no LOSS, and the twin rule;
  - criterion 3: the airport tolerance.
- **The tolerance clause** reads |`fold_delta_rmse`| ≤ 1.0 s from `compare.py E041 E033`, on R1, R2, R3, S1 and W1.
- **"Draw-robust" is recorded as "robust to one further fixed-seed (GPU-only) draw".** Beside it goes the per-fold min–max over the three draws, for the blend and for CatBoost alone. Each pair is labelled by type: E034 − E033 and E041 − E034 are seed + GPU; E041 − E033 is fixed-seed.
- **If E040 is byte-identical to E031 on all 8 folds,** H030's reading is "no further draw (the fixed-seed refit is deterministic)". The robustness record then rests on E034 alone.
- **No outcome reopens criterion 6, E033's PROMOTE or ruling H5.**
  - X-D05-S05-0001 (f) stands: rule 10 forbids re-reading criterion 6.
  - A "draw-fragile" or "spread above tolerance" reading is a D5-C9 disclosure and a question for the Day 6 phase close.

**N6. Resolved parameters (H029).**
- Before any H029 or H030 reading, compare E040's `resolved_params.json` with E031's: every key, on every fold.
- A key present in only one arm counts as a difference. `random_seed` is expected to be equal.
- If `d06_diagnostics.py closed-set` is used, its built-in exemption for `max_ctr_complexity` does not apply: every `differ` entry counts.
- Any difference is stated beside both readings as "not a pure fixed-seed re-draw: <keys>". No threshold changes.

**N7. One population for each side-by-side comparison (rule 11).**
- E032's figures shown beside E040's, and E034's shown beside E041's, come from the same scripts and the same populations:
  - `d06_diagnostics.py diversity E031 E032 E040` and `d06_diagnostics.py diversity E033 E034 E041`;
  - `mechanism_check.py` for each pair.
- They are not taken from the phase-close table, which used non-routed rows.

**N8. Records.**
- Any run still executing at 21:30 local is an INC-0012 deviation and is reported with its end time. The launcher log is copied into the session record.
- Each analysis states the freeze diff from `9d245c0` over `src`, `scripts`, `pyproject.toml`, `uv.lock`, `config`, `d06_diagnostics.py` and `run_window_2.sh` (expected empty).
- **Diagnostics:**
  - run after the window, never while the lock is held, and stay memory-light (INC-0008);
  - read truth only through `truth_frame`;
  - never read H or a final fold.
- **The CLASS-L reporting of `H021_review_v2.md` applies:**
  - beside `within_class`, state whether E040 also stayed within CLASS-M (≤ 30 min and ≤ 8 GB);
  - disclose any peak RSS above 8 GB and any swap-out;
  - change no parameter to fit a class.
- E040 and E041 are never NEW, and rule 10 covers their configurations. Any Day 7 use states its selection, including any average of draws.

Required acknowledgement path:
- `research/day-06/acks/H029_ack_v1.md`, citing the proposal hash `8511f3a17462e52634efcbe58aa7b141b40a277b10dadb6a3288df5c8944a802` and this review's hash.

## Revision

**None required.**

Non-blocking clerical items, to correct in the analysis record:
- (a) The launcher's hash is in INC-0012's amendment, not in the envelope's constraints.
- (b) "3,956 MiB at an idle start": E031 started at 853 MiB, so about 3.1 GB is attributable to it.
- (c) §Batch paraphrases criteria 1–2 more loosely than the frozen text. N5 governs.

Recommended, not required:
- Check GPU memory at arming, and arm close to the window. If an external process holds several GB, not arming is a deferral that depends on status only.
- Run `range_check.py E040`, to match `range_check_E031.json`.
- The W&B sync has no timeout of its own (`H024_review_v2.md`, point (f)). A stall after E040 would defer E041.

## Advisor Prediction

Probability of improvement:

| Event (H029 = E040; against E031 unless stated) | P |
|---|---|
| Byte-identical on all 8 folds | 0.01 |
| Development mean below E031's 440.76 (no direction expected) | 0.50 |
| \|ΔRMSE\| ≤ 1.0 s on all five development folds | 0.70 |
| RMS prediction change below E032 − E031's on at least 4 of 5 development folds (same script, N7) | 0.65 |
| Resolved parameters equal on every key and fold (N6) | 0.96 |
| Status COMPLETE | 0.94 |
| Runtime above 1,600 s | 0.12 |
| Still running at 21:30 local | 0.06 |

Expected magnitude:
- **Development mean:** 440.2–441.4 s (central 440.8).
- **Largest per-fold |ΔRMSE|, all rows:** 0.2–1.4 s (central 0.6).
- **On `NM_present_excl_LIRF`:** the 5-fold mean ΔRMSE stays within ±0.7 s (P 0.75).
- **RMS prediction change** (all rows, development folds): 12–45 s (central 28). W1c is the largest, at 25–75 s.
- **Single rows:**
  - row 192622644 (S1): 8,500–13,500 s (E031 10,976; E032 10,237);
  - row 183910286 (W1): 17,000–27,000 s (E031 22,233; E032 18,605).
- **Resources:** runtime 1,100–1,600 s (central 1,350); peak RSS 6.9–7.2 GB; about 3.1 GB of attributable VRAM.

Primary expected failure mode:
- **Scientific:** none. The run measures the fixed-seed spread whatever its size.
- **Interpretive:** a modest fixed-seed spread gets recorded as "the variance Day 7's submission will carry". N4 and N5 prevent this.
- **Operational:** either a GPU memory conflict at 21:00 (RESOURCE_FAILURE, with no re-attempt), or a run long enough to push E041 to the next window.
