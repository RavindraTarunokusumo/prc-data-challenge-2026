---
schema: advisor-review-v1
hypothesis_id: H035
proposal_version: 1
proposal_sha256: ece127cbbec41fa96bc91950add8d6604be548e9607cf85522ef91f095cfff81
exchange_id: X-D07-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-10-03T20:46:22Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.80), with binding conditions U1–U10, including one pre-registered Advisor objection under criterion 8 (objection F, U7).** This file holds the shared findings for H034–H037. `H034_review_v1.md`, `H036_review_v1.md` and `H037_review_v1.md` adopt U1–U10 by reference.

**The candidate is admissible and cleanly built.**
- It answers the question X-D03-S01-0003 (e) left open: should the routing's 2025 price (E019 − E020 = +122.54 s on the development mean) also be paid in 2026? Days 4–6 did not test it; the journal confirms this.
- (e)'s four conditions are met:
  1. **New configuration.** It is E033 with a different subgroup model, not E020's configuration. E020's model never serves a non-subgroup row here.
  2. **Rule 8.** The convention exposure is pre-registered, with S1 at July's rate.
  3. **Criterion 8.** H009 v3's rule is kept, with no new threshold. E028 is added as a second, stricter reference, the role rule L v2 ratified for it.
  4. **Forward-risk rationale.** It cites the break-even figures as Day 3 outcomes and states the 2026 counts (107 and 276; verified). Its reading of those figures is corrected by U6.
- **It is a fixed combiner of stored, manifest-verified predictions.** Only subgroup rows can differ from E033, and the route check proves this row by row.

**Verified here, read-only.**
- **What was not touched:** no target column, no block-time column, no December row, no feature build, no fit, no score.
- **Hashes:**
  - the four proposals match the envelope;
  - the launcher's SHA-256, recomputed here, is `f76db6fa15abf5c8a3712cea39e6454f1f4290295a25b3a109505076ada05eed`, equal to the envelope's;
  - its diff against `run_window.sh` is exactly what the envelope states (date, window, log name, queue, a two-argument route check, message strings);
  - the tree is clean at `76e80f1`.
- **Tests and lock:**
  - `uv run pytest`: 165 passed. `ruff check .`: clean.
  - The experiment lock is free: the inode of `runtime/experiment.lock` is not in `/proc/locks`, and its `E044` text is a stale stamp.
- **Code:**
  - `prc.blending.override` and the worker's `model: override` dispatch;
  - `make_submission.py`'s override mode and `--tag`;
  - `route_check.py`, whose `ROUTED UNROUTED CHAMPION` arguments read as `OVERRIDE BASE SOURCE`. So `route_check.py E046 E033 E045` checks the subgroup against E045 within 1e-6 s, and every other row against E033 exactly. No change to the script is needed.
- **Real-file smoke test** of `prc.blending.override` (scratchpad; nothing written to the repository), with E033 as base:
  - on R1, S1 and W1c, the output equals E033 exactly off the subgroup and the source on it (168, 337 and 58 rows);
  - on R1 and W1, an in-memory +1,000 s shift of the real source file moved exactly the 168 and 58 subgroup rows.
  - **Side finding:** E033 and E029 are bit-identical on the subgroup. E033's routed rows are therefore exactly the laptop ridge.
- **Records:**
  - The proposal's expectation table recomputes from `metrics.json` to 0.1 s (development mean 314.4).
  - H034's and H036's `params`, `model` and `feature_set` equal E020's (parsed YAML).
  - E020's prediction files are absent on the laptop (stored predictions begin at E025), so the E045 instance is needed.
  - The three earlier holdout records hold all-rows aggregates only. December's subgroup has never been exposed, so H is a fresh test of it.
  - The seven Day 3 break-even rates are reproduced exactly from `E020_vs_E005.json` by the formula given under Scientific Validity.

**Six findings.** U1–U10 settle them. None changes a configuration, fold, population or the criterion 8 threshold.
1. **The development folds cannot test this candidate.**
   - Criteria 1–3 and criterion 4 are arithmetic consequences of Day 3's recorded E020 − E019, re-run on the laptop; criterion 6 is a determinism check of E045. The candidate was formed after that result was known.
   - Only a defect, or a failure of E045 to reproduce E020, can change them.
   - The protected holdout is the only evidence on the bet outside the 2025 months that selected it (U6, U7).
2. **The forward-risk statement understates the downside, and the Advisor's Day 3 (e) wording is the source** (U6).
   - The break-even rates 0.009–0.099 are mixture weights at fixed per-row gains and losses. They describe a change in the subgroup's composition.
   - Under a change in how the same kind of row is recorded:
     - a row's break-even is about half its 2025 convention probability;
     - if the convention were absent, the loss is of the same order as the 2025 gain.
3. **Rule 12's forward-support sentence is not pre-registered for this subgroup.**
   - It applies, because the subgroup's new predictions use `d_sched` and SCHED-anchored windows.
   - I computed it target-free (Scientific Validity). January 2026's subgroup has the heaviest schedule-delay tail of any month (U8 (a)).
4. **Row concentration is known in advance and not pre-registered** (U8 (c)).
   - One 36-hour record carried 79 % of W1's and 57 % of W1c's subgroup SSE change on Day 3.
   - R3's top-1 share was 0.45.
5. **The id-mapping sentence conflicts with the pinned launcher.**
   - The proposal says "the ack records the mapping and the configs use the allocated ids".
   - But the pinned queue hard-codes E045–E050 (U1).
6. **S8 of X-D07-S01-0001 names the uploaded file.** Promotion of H035 would change it (U9).

**What the batch cannot show.** It cannot show whether LIRF records block times for NM-unmatched departures in January and July 2026 as it did in 2025.
- The ranking months blank the block time, and no input reveals it.
- H tests December 2025 only, on 88 rows.

## Scientific Validity

### The mechanism, and what the development folds can show

- **The claim** is that the unrouted FS2 fit predicts the subgroup's block-at-schedule records (y ≈ `d_sched`), which the winsorised ridge cannot.
  - This is the Day 1 convention (C2). On 2025 it is real and large: the recorded subgroup SSE change of E020 against E005 is −2.5 × 10⁹ s² (R2) to −4.2 × 10¹⁰ s² (S1) per development fold.
  - It is a better forecast of the recorded target, not of taxi duration, as the proposal says.
- **Criterion 4's reading (a) is an identity of this construction.**
  - `share_of_sse_change_tail` is the subgroup's tail SSE change divided by the fold's total change (`prc.attribution.subgroup_disclosure`). Only subgroup rows change here.
  - So "total < 0 and tail share > 1.0" holds if and only if the fold improves and the subgroup's bulk rows lose.
  - Day 3 recorded both on every fold: bulk +1,067 to +4,292 s of subgroup bulk RMSE.
  - The reading is valid attribution. It is not a test that could plausibly fail.
- **Reading (b)** isolates the population exactly.

### The break-even figures describe a change of composition, not of recording (U6)

**A model of one subgroup row.**
- The recorded target is D (`d_sched`) under the convention, and a normal taxi time T otherwise.
- The routed ridge predicts R ≈ T on every subgroup row. Verified on stored files: E033's subgroup means are 1,687–1,802 s on the seven scored folds, E044's are 1,760 s in both ranking months, the maximum is 2,263 s, and none is above 3,600 s.
- Write the unrouted fit's prediction as T + a(D − T).
- If the row's convention probability in a ranking month is p′, the fit's expected squared-error excess over the ridge is

  (D − T)² · a · (a − 2p′).

- **Consequences for that row:**
  - it gains a(2 − a)(D − T)² on a convention record and loses a²(D − T)² on a normal one;
  - it loses in expectation if and only if p′ < a/2;
  - for a fit calibrated to 2025 (a equal to the row's 2025 probability p), it loses if and only if p′ < p/2.

**What Day 3 computed.**
- r* = L / (L + |G|), with G and L the 2025 mean per-row SSE change on the subgroup's tail and bulk rows. Recomputed from `E020_vs_E005.json`, this reproduces all seven rates. On S1, G = −4.02 × 10⁸ and L = +2.47 × 10⁷ s², so r* = 0.058.
- Varying r at fixed G and L means the 2026 subgroup holds fewer rows of the kind the fit predicts high, and its other rows behave like 2025's bulk. That is a change in composition.
- Under a change in how the same kind of row is recorded, the rows that leave the tail are exactly those the fit predicts high. Each then carries a²(D − T)², not L.
- The proposal's formula ("gain on tail rows × r/r₂₀₂₅ + loss on bulk rows × (1 − r)/(1 − r₂₀₂₅)") is the composition model.
- Day 3's "the unrouted bet would lose only if the convention nearly vanished" has the same limit. That wording was the Advisor's, and U6 corrects it.

**The stakes, stated plainly.**
- **Break-even under a recording change.**
  - The convention must keep more than about half its 2025 strength on the rows the fit reads as convention rows, not more than "a sixth of the lowest month".
  - Under a proportional decline and a calibrated fit, the break-even tail rate is about half the observed one:

    | Fold | Day 3 r* | About half the observed rate |
    |---|---|---|
    | S1 | 0.058 | 0.18 |
    | W1 | 0.009 | 0.38 |
    | R1 | 0.039 | 0.22 |
    | R2 | 0.099 | 0.25 |
    | R3 | 0.030 | 0.35 |

- **Downside if the convention were absent.**
  - Per row, loss/gain = a/(2 − a): 0.33 at a = 0.5, 0.82 at a = 0.9.
  - On S1's recorded figures (tail −4.78 × 10¹⁰, bulk +5.4 × 10⁹ s²), that is a subgroup loss of about 2.1–4.5 × 10¹⁰ s². This is half to all of the 2025 net gain (−4.24 × 10¹⁰).
  - The bet's stakes are of the same order on both sides. U8 (b) measures them on E045's actual predictions.
- **What 2025 does show.**
  - S1 (July 2025) has the lowest 2025 tail rate (0.35), yet it is the fold the fit gains most on (−211 s).
  - The 2025 month-to-month variation is therefore within what the fit reads, consistent with a change in composition.
  - Nothing in 2025 samples a change in recording practice.

### The subgroup in 2026, target-free (rule 12; U8 (a))

LIRF DEP rows with `AOBT_3` missing; `d_sched` = MVT − SCHED. December is excluded, and no target or block-time column was read.

| Month | Rows | `d_sched` > 1 h | > 3 h | > 5 h | > 12 h | Median (s) | q90 (s) | Max (s) |
|---|---|---|---|---|---|---|---|---|
| 2025 range (Jan–Nov) | 52–337 | 81–96 % | 9.6–22.3 % | 3.0–10.0 % | 0–3.8 % | 6,001–6,810 | 10,623–14,939 | 22,794–131,163 |
| January 2025 | 60 | 90 % | 8 | 6 | 2 | 6,688 | 13,677 | 60,118 |
| July 2025 (S1) | 337 | 95 % | 75 | 23 | 9 | 6,783 | 14,939 | 93,535 |
| **January 2026** | **107** | 83 % | 21 (19.6 %) | **11 (10.3 %)** | 3 | **7,141** | **17,816** | 56,520 |
| July 2026 | 276 | 94 % | 53 (19.2 %) | 21 (7.6 %) | 8 | 6,897 | 14,945 | 111,654 |

- **Long schedule delays are the norm in this subgroup.** 81–96 % of its rows are more than an hour behind schedule in every month, against tail rates of 0.35–0.83 by 2025 month.
  - Most bulk rows are therefore long-delay rows recorded with a normal taxi time, and the fit must tell them apart from convention rows.
  - The per-row stakes are large on most of the subgroup, not only on its tail.
- **January 2026 is above every 2025 month** in median (7,141 s) and q90 (17,816 s), and just above the 2025 maximum share above 5 h (10.3 % against 10.0 %). Its stakes per row are the largest of any month, in both directions.
- **July 2026 is inside the 2025 range** on every measure except the median (6,897 s against 6,810) and q90 (14,945 s against 14,939), which sit just above it.
- The 2026 subgroup's size and delay profile match 2025's. This is consistent with an unchanged recording process, but it is not evidence of one: `d_sched` does not depend on how the block time is recorded.

## Novelty Relative to Existing Research

- **Not redundant.**
  - No Day 4–6 proposal tested an unrouted subgroup (journal; STATE).
  - E020 was a Day 3 ablation, never a candidate. Rule 10 bars its configuration, and backend-only re-draws of it (X-D04-S02-0001 (e)), as a candidate. H035 is neither; H034 re-runs it as a component only (U5).
- **It is the largest priced, unexploited contrast in the record.** The selection hazard is not noise-chasing: one binary structural choice, made on a 122.5 s difference. Its hazard is that the evidence for it was all seen before it was proposed (finding 1).

## Experimental Isolation

- **Exact by construction.**
  - E046 differs from E033 only on rows where `ADEP_mvt == LIRF` and `flt_missing == 1`.
  - `blending.OVERRIDE_SUBGROUPS` equals `routed.route_mask` (unit test), and the formatter uses the same key (`AOBT_3_flt` null).
  - The route check enforces exact equality off the subgroup.
- **Rule 13.** No stochastic component is added. E046's non-subgroup rows are E033's single draw, and E048 carries the same draw. Criterion 6 is therefore a determinism check of E045, as Day 3 ruled for this learner (D3-C4).
- **Rule 14.** The point contrasts against E034 and E041 carry the draw differences, at most 0.60 s per fold.
- **The construction combines training procedures.** It takes a fit trained on every row, including the convention rows, for the subgroup, and E033's `route_train_exclude` halves elsewhere. That is the point: D3-C2 stays treated on the rows that are served by E033.

## Validation Quality

- **Folds.** The frozen folds are used unchanged: seven scored folds and H, with H predicted only. S1 must WIN; B1–B4 carry.
- **Criteria 1–3 against E033.** They are pre-registered, but known in advance to within E045's reproduction of E020 (finding 1).
- **Criterion 4:** readings (a) and (b) as proposed, with the scope stated above.
- **Criterion 6:** `reproduce_check.py E048 E046 --champion E033`.
  - The script checks purpose and hypothesis version, not config identity.
  - The pre-arming record must show that E048's config equals E046's except for `purpose`, `seed` and `override` (U1).
- **Criterion 8.**
  - **H009 v3's rule is unchanged.** `NM_missing_LIRF.delta_rmse_bulk` must be ≤ +6,500 s on every development fold, read against E033 and against E028; both must hold.
    - E028's role here is the one rule L v2 ratified: it differs from the laptop ridge by up to about 191 s on single routed rows.
    - The recorded statistic is +1,067 to +4,292 s, leaving a 2,208 s margin on S1.
  - **Objection F (U7) is separate from that rule** and changes neither the rule nor its threshold.
- **The protected holdout.**
  - E046 and E033 differ on 88 H rows only, so H isolates the bet in a month outside the selection.
  - **Under the frozen phase-close rule, a TIE lets a promotion stand.** That rule assumes the development folds already carry the evidence; here they do not. U7 therefore pre-registers that a TIE does not resolve objection F.
  - The access itself is for the Day 7 phase close to name (rule 9). This review authorizes none.

## Leakage Review

### Target Leakage

PASS

- **The combiner fits nothing.** It reads two manifest-verified prediction files and the target-free routing key.
- **E045's and E049's fits are H016 v2's,** reviewed on Day 3: fold-local training rows only, and no target statistics.
- **December targets** enter only E049's final-fold training and E050's unmasked load, through the logged path (U4). E050 uses no target. No December figure appears in any artifact of the batch.

### Temporal Leakage

CONCERN

Label notes, not blocking.
- **The mechanism is the T channel.** For a convention record, y = MVT − SCHED = `d_sched`.
  - MVT and SCHED are ranking columns, so the channel is admissible (DATASET_AUDIT §6.2).
  - It falls outside the causal-only variant (rule 8).
- **The FS2 in-taxi counts and SCHED-anchored windows are T,** as H016 v2. No cross-month input is used.

### Competition Availability

CONCERN

Not blocking.
- **Every input is present for ranking DEP rows.** The routing key is P; there are 107 and 276 subgroup rows, verified.
- **January 2026's subgroup sits above every 2025 month** in median and q90 of `d_sched` (table above).
- **The quantity the gain depends on, the 2026 recording practice, is not observable in the ranking data.**
- **SUBMIT_JUL lacks June 2026 context for the first minutes of 1 July,** as for E044 (S9).

## Compute Review

### RAM

PASS

- **The combiners** (E046, E048, E050) load silver and build FS0: E033 3.38 GB and E044 3.54 GB, under CLASS-S's 4 GB.
- **The fits** are under CLASS-M's 8 GB: E045 and E047 6.3–6.8 GB (E029 6.60 GB); E049 about 7.0 GB (E042 7.02 GB).
- **The hard limit is 11 GB.** Swap is recorded beside RSS (INC-0010).

### Runtime

PASS

- **Expected:** E045 and E047 about 900 s each (E029 893 s); E049 about 300 s (E042 280 s); each combiner about 10–20 s.
- **W&B overhead is not in the guards.** In the first Day 7 window, the failed W&B syncs added about 100 s per run after `runtime_s`: E042's runtime was 280 s but its span was 390 s; E043's was 419 s against 519 s.
- **Window arithmetic:**
  - the expected queue ends about 00:45Z, and the pessimistic one about 00:53Z;
  - E049 must start by 00:50:00 (600 s guard). It is deferred only if E045 and E047 each run more than about 40 % longer than E029.
- **Timeouts:** 2,700 s (CLASS-M) and 450 s (CLASS-S). The launcher never kills a run.

### Disk

PASS

About 200 MB of predictions over the six runs, all covered by manifests. A tagged submission file of about 1 MB, if formatted.

## Weakest Assumption

**That LIRF's 2026 recording of block times for NM-unmatched departures follows 2025's practice.**
- The gain rests on it entirely, and the stakes are symmetric in order (U6).
- No Day 7 evidence can observe it for January or July.
- H (December, 88 rows) tests one adjacent month.
- The 2026 subgroup's size and delay profile match 2025's, but they would match whether or not the practice changed.

## Missing Control or Ablation

None blocks.

**Named, not required: the convention split.** This would split the subgroup's SSE change by the Day 1 convention definition (block time within 120 s of schedule) instead of the y ≥ 3,600 s proxy.
- On Day 1, 17 % of LIRF tail rows were not block-at-schedule.
- The split would show how much of the gain is the recording convention and how much is genuine long taxis, which a recording change would not touch.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

**For the batch as a whole:**
- six allocations, in the U1 order;
- one run each, in the queue of `research/day-07/sessions/D07-S01/run_window_2.sh` (SHA-256 `f76db6fa15abf5c8a3712cea39e6454f1f4290295a25b3a109505076ada05eed`), in the 2026-10-04 00:00–01:00Z window (INC-0015), or later under U10;
- the launcher's route checks;
- after the queue, the comparisons below;
- the formatter only under U9.

Nothing else.

**H035 v1:**
- **Allocations:** one `primary` allocation (expected **E046**) and one `--purpose reproduction` allocation (expected **E048**), with the configs of U1.
- **After the queue, from a clean tree with no experiment running:**
  - `compare.py E046 E033`, which governs criteria 1–3 and carries rules 1, 6, 7 and 11;
  - `compare.py E046 E034` and `compare.py E046 E041` (rule 14);
  - `compare.py E046 E028` (criterion 8 against E005's instance);
  - `mechanism_check.py E046 E033 LIRF_NM_missing`;
  - `range_check.py E046 E033` and `range_check.py --forward` (rule 12);
  - `reproduce_check.py E048 E046 --champion E033`.
- **No holdout access is authorized here** (U7).

**U1. Allocation order, ids and configs.**
- **Order:**
  1. H034 v1 `primary`;
  2. H035 v1 `primary`;
  3. H034 v1 `--purpose reproduction`;
  4. H035 v1 `--purpose reproduction`;
  5. H036 v1 `primary`;
  6. H037 v1 `primary`.

  The ids must be **E045–E050** in that order.
- **If any id differs, do not arm.** The pinned queue would run the wrong ids. The batch would then need a new launcher, which means a new proposal version. The proposal's sentence "the ack records the mapping and the configs use the allocated ids" does not apply to the pinned launcher.
- **Before arming, verify and record** (parsed YAML):
  - each `config.yaml` equals its proposal block;
  - E046: `base: E033`, `override: E045`;
  - E048: equals E046 except `purpose: reproduction`, `seed: 43` and `override: E047`;
  - E047: equals E045 except `purpose` and `seed`;
  - E050: `base: E044`, `override: E049`;
  - each `gate.json` names its hypothesis, `v1` and its purpose.

**U2. Pre-arming record.** It is committed before arming, and nothing in the tree changes from that commit until the window opens. It states:
- the U1 checks;
- the launcher's SHA-256, recomputed at arming, equal to the pin `f76db6fa15abf5c8a3712cea39e6454f1f4290295a25b3a109505076ada05eed`, and its diff against `run_window.sh`;
- the freeze diff from `76e80f1` over `src/`, `scripts/`, `config/`, `pyproject.toml`, `uv.lock` and the launcher (expected empty);
- the rule L v2 item 6 environment;
- the overrun bounds:
  - class timeouts 2,700 s (E045, E047, E049) and 450 s (E046, E048, E050);
  - the launcher never kills a run;
  - any run still executing after 01:00Z is an INC-0015 deviation, reported with its end time.

**U3. The dirty tree (as S3).**
- **Expected:**
  - after E049's checkpoint, the launcher logs `WARNING: tree not clean … M orchestration/task-ledger.jsonl`, and the same follows E050's checkpoint;
  - E050 records `git_dirty_at_run: true`;
  - E045–E049 record `false`.
- **Any other entry is an INC-0015 deviation.** Nothing is edited, staged or committed by hand during the window.
- **After the queue:**
  - the two unmasking lines go into the first commit after the queue;
  - E050's records say "`git_dirty_at_run: true` (task-ledger append from the final-fold unmasking only; U3)".

**U4. Unmasking events (as S4).**
- The task ledger shows `holdout_targets_unmasked_for_final_training` exactly once each for E049 and E050, timestamped inside that run's span.
- No event exists for E045–E048 or any other new id.
- E050's event is recorded as "unmasked silver loaded; no target used (override; the FS0 frame supplies row ids and the subgroup key only)".

**U5. Status of each run.**
- **E045 and E047 (H034) and E049 (H036)** are components:
  - never candidates and never NEW, in any phase;
  - no promotion reading uses them;
  - rule 10 bars E020's configuration and its re-draws, these included, as a candidate.
- **E048** is a reproduction: never NEW.
- **E050 (H037)** is not a candidate, never NEW and never scored.
- **E046 is the batch's only candidate, and the only run that may be NEW:** in the Day 7 access only, and only if the Day 7 phase close names it.

**U6. Forward-risk correction.** It is recorded in the ack and carried into the E046 analysis, the Day 7 DAY_SUMMARY and the final report. It is also an Advisor-record correction to X-D03-S01-0003 (e).
- **The Day 3 break-even rates (0.009–0.099)** are mixture-weight break-evens at fixed 2025 per-row tail gains and bulk losses. They describe a change in the subgroup's composition.
- **Under a change in how the same kind of row is recorded:**
  - a row predicted at T + a(D − T) loses in expectation once its convention probability falls below a/2 (for a calibrated fit, below half its 2025 value);
  - if the convention were absent, the loss is of the same order as the 2025 gain;
  - the bet's stakes are therefore of comparable size on both sides.
- **The statements this corrects:**
  - H035 §Batch's "loses … only for r below the fold-wise break-even" and "under a sixth of the lowest 2025 month" are read with this qualification;
  - Day 3 (e)'s "would lose only if the convention nearly vanished" is corrected likewise.
- **"A bet on the convention persisting" stands.**
- **Criteria 1–3, 4 and 6 have no power on the bet:** criteria 1–4 recompute Day 3's recorded contrast on laptop instances, and criterion 6 checks determinism. **No record may quote E046's development margin as the submission's expected gain.**

**U7. Objection F (Advisor objection under criterion 8; pre-registered before any result).**
- **The statistic:** the outcome of the Day 7 phase-close access, if the phase close names it as `holdout_check.py E046 E033` (the frozen phase-close comparison: the phase-closing candidate against the phase-opening champion).
- **WIN** resolves objection F, for December only. A WIN does not test July's seven-month distance or January's heavier delay tail, and it does not discharge U6.
- **TIE** does not resolve it.
  - H035 is then INCONCLUSIVE ("phase-close holdout TIE; forward bet not confirmed").
  - E033 stays champion, and E044's file stands.
- **LOSS:** the frozen revert applies, and H035 is INCONCLUSIVE ("phase-close holdout LOSS, frozen revert").
- **Without an access,** objection F stands, and H035 is not promotable.
- **Objection F changes neither H009 v3's rule nor its threshold** (ruling B).

**U8. Disclosures for the E046 analysis and the phase close.** These are disclosure only and change no fold outcome or criterion.
- **(a) Rule 12 forward support** for `LIRF_NM_missing`, from `range_check.py --forward`, against the 2025 monthly range. The figures above are the Advisor's verification.
- **(b) Exposure** on the subgroup, per development fold and twin.
  - **Quantities:**
    - X_t = Σ (E046 − E033)² over tail rows (y ≥ 3,600 s);
    - X_b = Σ (E046 − E033)² over bulk rows;
    - the top-1 and top-10 shares of X_t + X_b;
    - beside them, the realized subgroup tail and bulk SSE changes S_t and S_b from `compare.py`;
    - the recording-change break-even λ* = (X_t + S_b)/(X_t − S_t);
    - the "convention absent" loss X_t + S_b. Here the tail rows' target is taken to be the ridge's prediction, which slightly understates the loss.
  - **Per ranking month,** target-free: Σ (E050 − E044)² on the subgroup, its RMS, and its top-1 and top-10 shares.
- **(c) Rule 6, pre-registered from `E019_vs_E020_mech_LIRF_NM_missing.json`.**
  - Row 183903219 (W1; y 131,167 s; `d_sched` 131,163 s) carried 0.79 of W1's and 0.57 of W1c's subgroup SSE change. R3's top-1 share was 0.45.
  - W1 and W1c are also reported without that row (audit only, as D5-C10).
- **(d) Rules 11 and 14,** as the proposal states.

**U9. Formatting and upload.**
- **The formatter** `make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050` runs only:
  - after the Day 7 phase close promotes H035 with objection F resolved;
  - with no window running and the lock free.

  It never writes `predictions/final/submitting.parquet` or `SUBMISSION_RECORD.json`.
- **If, and only if, H035 is promoted,** S8's file clause (X-D07-S01-0001) is replaced: the uploaded file is `predictions/final/E050/submitting.parquet`, unmodified, with the SHA-256 in `research/day-07/submission/SUBMISSION_RECORD_E050.json`. Any formatter re-run must reproduce that hash. Otherwise S8 stands unchanged.
- **S6 applies to E050:**
  - the H035 §Batch SUBMIT flag is non-blocking;
  - a flag analysis that finds a defect makes E050 INVALID;
  - nothing is uploaded while a flag analysis is open.
- **The subgroup mean prediction** that the flag reports is not in the formatter's record. It is computed from the stored files (target-free).
- **The owner's upload decision** receives the U6 statement in plain words: the gain is a bet on the recording convention, with a downside of similar size.

**U10. Deferral, failure and reruns (as S7).**
- **Deferral.** This covers a run DEFERRED by the launcher or refused before RUNNING.
  - The run keeps its id, stays ALLOCATED, and runs unchanged in a later owner-set window. That window needs a new incident record.
  - It runs by a direct `run_experiment.py` call, or by a new launcher recorded before that window.
  - No new allocation is made.
- **RESOURCE_FAILURE or TIMEOUT.**
  - At most one `--purpose rerun` per hypothesis, with a config equal to the failed run's (parsed YAML).
  - If an override's source was re-run, a new `--purpose rerun` allocation of H035 or H037 replaces the failed id in the same field. The original override stays ALLOCATED and is recorded "superseded; never run". Committed configs are never edited.
- **INVALID.** This covers a code defect, a failed route check, or a failed I1–I5.
  - There is no rerun; a fix needs a new proposal version.
  - E044's recorded file is untouched in every case.

**Required acknowledgement path:** `research/day-07/acks/H035_ack_v1.md`.
- It references the proposal hash `ece127cbbec41fa96bc91950add8d6604be548e9607cf85522ef91f095cfff81` and this review's hash.
- It adopts U1–U10 as binding, and records U6 and U7 in full.

## Revision

None required for this version. U1–U10 are execution and record conditions under ACCEPT.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| E045 equals E020 within 0.01 s on every fold | 0.92 |
| E047's eight prediction files are byte-identical to E045's | 0.95 |
| `route_check.py` PASS for E046 and E048, given COMPLETE | 0.97 |
| Criteria 1–3 against E033 hold, 7/7 WIN | 0.93 |
| Criterion 8 rule holds against E033 and E028 on every development fold | 0.95 |
| Criterion 4 readings (a) and (b) hold on every development fold | 0.95 |
| Criterion 6 (E048 against E046) passes | 0.95 |
| All six runs COMPLETE inside the window | 0.85 |
| If the access is named, E046 against E033 on H: WIN / TIE / LOSS | 0.85 / 0.09 / 0.06 |
| H035 promoted at the Day 7 phase close | 0.75 |
| E050 has a lower true RMSE than E044 in January 2026 / July 2026 | 0.85 / 0.80 |

Expected magnitude:
- **Development folds:** as the proposal's table, within 1 s per fold. The mean is 314.4 s (−124.5 s against E033), with W1 about 80 % one row.
- **Criterion 8 statistic on S1:** about +4,290 s against E033, and within 200 s of that against E028.
- **H, if named:** E046 − E033 between −15 and −150 s, central −60 s.
- **The ranking months, unobservable within Day 7:**
  - a gain of the order of 100–200 s of month RMSE if the convention holds at its 2025 strength;
  - a loss of the same order if it is absent;
  - January carries the larger per-row stakes.

Primary expected failure mode:
- **Primary: the margin read as a measured gain.** The development and holdout readings pass, because they test 2025 and December. H035 is promoted, and the record carries the −124.5 s development margin as the submission's gain. In a ranking month where LIRF's block-time recording for NM-unmatched departures has changed, the submission then loses by about as much as it would otherwise gain, and nothing in Day 7 can detect it (U6).
- **Secondary: a TIE on H.** December's subgroup gain sits on one or two airport-day clusters, as W1's did in 2025, so H returns TIE. Objection F then leaves H035 INCONCLUSIVE.
- **Operational: deferral.** E045 or E047 runs long, and E049 and E050 are deferred to another owner window.
