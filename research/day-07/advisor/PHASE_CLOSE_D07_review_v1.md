---
schema: advisor-review-v1
hypothesis_id: PHASE_CLOSE_D07
proposal_version: 1
proposal_sha256: 5c5011cc144e4a0f4fd469cfceafdd49f0bebce6b881d33ed00cd44bb722dd63
exchange_id: X-D07-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-10-04T17:53:11Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.85), with binding conditions P1–P9, ruling H7 and corrections D7-C6 to D7-C13.** The Day 7 decisions stand. The Day 7 holdout access is named exactly as requested. The U7 outcome mapping applies unchanged. The FROZEN definition is adopted with additions (P7). The draft `DAY_SUMMARY.md` and `FINAL_REPORT.md` may not be marked FINAL until D7-C1 to D7-C13 are applied.

**What stands.**
- **Batch 1 (E042–E044).** The champion's SUBMIT procedure ran as authorized. The file `predictions/final/submitting.parquet` has SHA-256 `d57ff7db…af73` (recomputed here: equal, 1,091,362 bytes). I1–I5 hold and no flag was raised. S3, S4 and S5 hold.
- **Batch 2 (E045–E048).** H035's development reading is correct as recorded. Criteria 1–4 and 6 hold, and so does the criterion 8 rule. **Objection F (U7) is open.** These figures recompute Day 3's contrast, so they have no power on the bet (U6).
- **E049 and E050** were correctly deferred by the pinned launcher (572 s left against a 600 s guard). They stay ALLOCATED under U10.
- **E033 is champion** at the phase opening. Under U7, only a WIN of the named access changes that.

**What this review adds.** Seven findings, all settled by conditions and corrections. None changes a fold, threshold, population, statistic or the U7 mapping.
1. **The outcome mapping has no terminal fallback under WIN (P4).**
   - E046 can be promoted and still produce no valid E050 file. This happens if no owner window is set, or if E049/E050 fail, are INVALID, or find a defect under S6. The proposal does not say which file is then final.
   - Left open, that choice would be made after the access, with the H figure known. P4 pre-registers it now: E044's file, with the mismatch stated plainly.
2. **"Direct `run_experiment.py` calls" for E049/E050 have no checkpoint step (P5).**
   - The pinned launcher commits each run's own paths between runs. Direct calls do not.
   - Without that step, E050 would record a dirty tree that includes E049's uncommitted records. U3 calls that a deviation, and U3 also forbids hand commits during the window.
3. **A forward-support statement is wrong (D7-C7).** July 2026's subgroup delay tail is *not* above every 2025 month.
   - It sits at the 2025 maximum (July 2025): 6 s above it by the record's nearest-rank quantile, and below it by linear or lower interpolation.
   - Only January 2026 lies clearly above every 2025 month.
4. **The final report repeats corrected overclaims and omits deviations (D7-C8 to D7-C11, D7-C13).**
   - Day 3's congestion figure appears without its all-rows figure. This is the exact rule 11 omission that the Day 3 phase close corrected.
   - Day 6 appears without D6-C12.
   - "claude-opus-5-5 … implemented, ran … every experiment" contradicts INC-0005 and INC-0013, and leaves out INC-0003, INC-0004 and INC-0015.
5. **The final file's manifest is incomplete (D7-C12, P7 (a)).** `SUBMISSION_RECORD.json` has no code commit, creation time or reproduction command (DATA_POLICY §3). The formatter would write the same gaps for E050.
6. **Target-free exposure on H (pre-registered disclosure; Scientific Validity (a)).**
   - The 88 subgroup rows fall on 26 LIRF days.
   - Σ(E046 − E033)² is 53 % of E033's whole-month H SSE. The access is decided by these rows, and the swing is large in both directions.
7. **The champion's January level tracks its inputs (Scientific Validity (c)).**
   - Per airport, the January 2026 excess of the SUBMIT predictions over H follows the January increase in schedule delay (Spearman 0.89).
   - The four largest prediction excesses (LTFM, LSZH, EDDF, EHAM) are at the four largest delay increases.
   - This is target-free consistency evidence against a defect shared by both halves (H031's Weakest Assumption). It does not measure accuracy.

**Verified here, read-only.**
- **What was not touched:** no target or block-time column of any month (silver was read with a column projection that excludes both), no fit, no score, no `holdout_check.py`, and no formatter run.
- **Hashes.**
  - The proposal matches the envelope.
  - The Advisor definition is `30fff5dd…0d19`.
  - The six frozen files match `config/frozen.json` (`32c41c0f9331`).
  - The launchers equal their pins (`1975bbba…`, `f76db6fa…`).
  - Both committed launcher logs equal their `runtime/` originals byte for byte.
- **Lock, memory and tree.**
  - `runtime/experiment.lock` (inode 214027) is not in `/proc/locks`, and its `E048` text is a stale stamp. The only held flock is an unrelated daemon lock. No experiment process is running, and 9.7 GB is available.
  - The tree is clean at `650c785`. `git diff 76e80f1 HEAD -- src scripts config pyproject.toml uv.lock .claude tests` plus the launcher is empty.
  - `ruff` is clean. Tests were not re-run: the code is unchanged since the 165-test pass at `76e80f1`.
- **Environment (rule L v2 item 6):** CPython 3.13.15, polars 1.44.2 at 16 threads, no `*_THREADS` variables, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, LightGBM 4.7.0, CatBoost 1.2.10, `uv.lock` `efa4fd78…`.
- **Ledgers.**
  - The task ledger has `holdout_access` events for `day-01`, `day-03` and `day-05` only.
  - It has unmasking events for E042, E043 and E044 only, each inside its run span.
  - Allocations E042–E050 are as recorded.
  - E046's gate record is `day-07`, `primary`, H035 v1. E046 and E033 are COMPLETE, E049 and E050 are ALLOCATED, and `CURRENT.json` names E033.
- **Prediction files.**
  - All eight files of E033, E045–E048, E026, E028, E029, E031, E034 and E041 match their manifests.
  - On H, E046 ≡ E048 and E045 ≡ E047 (equal SHA-256).
  - `holdout_compare` verifies these hashes before it appends the access line (`evaluate._predictions`).
- **Runs.**
  - The seven checkpoint commits each stage only their run's own paths.
  - `git_dirty_at_run` is false for E042 and E045–E048 and true for E043 and E044, as S3 and U3 require.
- **Figures recomputed** from `metrics.json` and `research/comparisons/`:
  - E046 per fold, and its mean of 314.424;
  - E045 equals E020's 321.95;
  - ΔRMSE −124.45 (q95 −82.85), 7/7 WIN;
  - the criterion 4 shares (1.003–1.127);
  - the criterion 8 statistic against E033 and E028 (worst S1, +4,292.4 and +4,292.0);
  - the rule 12 counts, rule 14 (E034 −124.53, E041 −124.54), the U8 (b) table, and the reproduction (0.0 s per fold).
- **No H figure in any Day 7 file.** No Day 7 comparison file holds an H-fold target figure, and no `metrics.json` scores H.

**Answers to the proposal's "Case against".**
1. **The gain is a recording convention.** Stated correctly. U6 stands, and P8 extends it to the H figure.
2. **88 rows; December is adjacent.** Stated correctly, and quantified in (a) below.
   - December's subgroup delay tail is ordinary: q90 11,642 s (January–November 10,623–14,939 s) and 85 % of rows more than 1 h late (81–96 %). Its median, 6,898 s, is just above January–November's 6,001–6,810 s.
   - So H tests the convention's persistence one month forward. It does not test January's heavier tail (q90 17,816 s).
3. **Selection.** Stated correctly. H is fresh for this contrast:
   - the Day 1 convention statistics used January–November only (`PHASE_CLOSE_D01_review_v1.md` (c));
   - the pre-freeze audit read December only at distribution level (month standard deviation 514.7 s, typical of 2025);
   - both earlier H comparisons routed the subgroup to a ridge in both arms, so no earlier holdout record isolates it.
4. **The SUBMIT procedure is untested.** Stated correctly. Finding 7 is consistency evidence only.
5. **Process.** Stated correctly. D7-C6 adds STATE's pre-written timestamp.
6. **The criterion 8 reference.** Verified: the rule holds against both E033 and E028.

**Answers to the "Known weaknesses".**
- **The override code.** The route checks pass on all eight folds. My own recomputation agrees: max |E046 − E033| off the subgroup is exactly 0 on R1–R3, S1, W1 and H. The formatter's override mode (I4) will first run on E050. Its byte-for-byte reproduction of E044's file was not re-run here, because this exchange allows no formatter run.
- **The scripted checkpoints.** Verified above.
- **FROZEN.** It is procedural only. `gate.py` guards `config/frozen.json` and has no project-freeze check. A post-FROZEN allocation would therefore show up as a deviation in the task ledger; it would not be refused. Stated in P7; no code change is required (the code is frozen).

## Scientific Validity

### (a) What the named access tests, and its power (target-free)

E046 and E033 differ on H only on the 88 LIRF NM-missing rows. Below are their prediction differences, from stored files only (no target).

| Fold | Subgroup rows | LIRF days | Σ(E046 − E033)² (s²) | RMS diff (s) | top-1 row | top-10 rows | top day | E046 > 3,600 s |
|---|---|---|---|---|---|---|---|---|
| R1 | 168 | 30 | 1.93 × 10¹⁰ | 10,725 | 0.17 | 0.84 | 0.18 | 86 (0.51) |
| R2 | 115 | 28 | 3.18 × 10⁹ | 5,259 | 0.19 | 0.70 | 0.26 | 52 (0.45) |
| R3 | 52 | 23 | 4.05 × 10⁹ | 8,826 | 0.34 | 0.88 | 0.35 | 34 (0.65) |
| S1 | 337 | 31 | 4.98 × 10¹⁰ | 12,151 | 0.08 | 0.63 | 0.21 | 204 (0.61) |
| W1 | 58 | 24 | 5.08 × 10⁹ | 9,361 | 0.57 | 0.89 | 0.59 | 36 (0.62) |
| **H** | **88** | **26** | **1.20 × 10¹⁰** | **11,659** | **0.28** | **0.91** | **0.29** | **57 (0.65)** |

- **The subgroup decides the access.** E033's whole-month H SSE is 369.18² × 165,677 = 2.26 × 10¹⁰ s². The exposure is 53 % of it.
- **If the convention were absent in December:** E046's H RMSE would be about √((2.26 + 1.20) × 10¹⁰ / 165,677) ≈ 457 s, a ΔRMSE of about +88 s (LOSS). This slightly understates the loss, as in U8 (b).
- **If the convention held at its 2025 strength:**
  - On the development folds, the realized gain is 0.78–2.74 times the exposure: R2 0.78, S1 0.85, R1 1.13, R3 2.72, W1 2.74.
  - At the R2–R1 ratios, ΔRMSE on H is about −86 to −135 s.
  - The R3 and W1 ratios cannot apply in full: they would exceed E033's whole-month SSE.
- **A TIE needs a decline to near the recording-change break-even** (λ* 0.20–0.57 of the 2025 strength on the development folds), or a gain confined to the top day. The top day's share (0.29) is moderate: between R2 and R3, and far below W1's.
- **December's delay tail is ordinary.** H's `d_sched` q90 (11,642 s) is mid-range for January–November (10,623–14,939 s). Its median (6,898 s) is just above January–November's 6,001–6,810 s. The access therefore tests persistence, not January's tail.
- **H is not pristine (DATASET_AUDIT §6.6)**, but it is fresh for this contrast.
  - December's marginal target distribution was read before the freeze, and E033's H RMSE has been known since Day 5.
  - Neither isolates the subgroup, and no Day 1 statistic on the convention used December.

### (b) The outcome mapping and its gap

- **The U7 mapping is applied unchanged.** It was committed (`d42ca57`, 20:54Z on 2026-10-03) before any run of the batch.
- **WIN promotes, but the promoted champion can lack a valid SUBMIT file.** The causes:
  - no owner window;
  - E049 RESOURCE_FAILURE or TIMEOUT, then a failed or unrun U10 rerun;
  - E050 INVALID (failed route check or I1–I5);
  - a flag analysis that finds a defect (S6).
- **The proposal is silent on that case.** The file would then be chosen after the access, with the H figure known, and possibly with the U8 (b) per-month exposure in view. That is a post-hoc selection channel. P4 closes it.

### (c) The champion's SUBMIT level in January (target-free)

DEP rows by airport: the mean schedule delay (`MVT − SCHED`, clipped to [−2, 10] h), January 2026 against December 2025. Beside it, E044's January mean prediction minus E033's H mean prediction (from the E044 analysis table).

| Airport | Delay change (min) | Share > 1 h late (Jan 2026 / Dec 2025) | Prediction change (s) |
|---|---|---|---|
| EHAM | +16.4 | 0.196 / 0.091 | +125 |
| LTFM | +7.9 | 0.135 / 0.085 | +199 |
| LSZH | +7.7 | 0.129 / 0.059 | +140 |
| EDDF | +5.8 | 0.158 / 0.082 | +132 |
| LFPG | +3.8 | 0.189 / 0.145 | +28 |
| LEMD | +2.1 | 0.110 / 0.090 | +9 |
| EDDM | +1.8 | 0.108 / 0.082 | +66 |
| LIRF | +0.8 | 0.093 / 0.078 | −25 |
| LEBL | −0.8 | 0.089 / 0.088 | −27 |
| EGLL | −2.2 | 0.108 / 0.111 | −46 |

- **The rank correlation is 0.89.** The four airports with the largest prediction excess have the four largest delay increases. The airports with no excess (EGLL, LEBL, LIRF) have flat or falling delays.
- **No time-zone artefact.** EGLL (UTC+0) and LEBL, LIRF and LEMD (UTC+1) move with their own delays, not with their offsets.
- **What this shows:** January's level close to the limits is input-driven. It is not evidence of a defect shared by E042 and E043. It says nothing about accuracy: S9 and ruling H6 (f) stand.

### (d) The candidate's development reading

- Recomputed exactly (Summary).
- **Criterion 4 reading (a) is an identity of the construction** (the H035 review). The pass is valid attribution, not a test that could have failed.
- **Criterion 6 is a determinism check:** E047 is byte-identical to E045.
- **E046's non-subgroup rows are E033's single draw** (rule 13, D5-C9).
- **None of this bears on 2026** (U6).

### (e) Forward support (D7-C7)

LIRF DEP rows with `AOBT_3` missing; `d_sched` q90 by quantile method; target-free.

| Month | Nearest rank (the record's method) | Linear | Lower |
|---|---|---|---|
| 2025 maximum | 14,939 (July 2025) | 15,035 (July 2025) | 14,939 (July 2025) |
| February 2025 | 13,865 | 15,033 | 13,865 |
| December 2025 (H) | 11,642 | 11,732 | 11,642 |
| **January 2026** | **17,816** | **19,592** | **17,816** |
| July 2026 | 14,945 | 14,461 | 13,977 |

- **The E046 analysis gives the 2025 maximum as 13,865 s.** That is February's value. The maximum is July 2025's 14,939 s, as the H035 review and `E046_exposure_U8.json` both show.
- **At q90, July 2026 is inside the 2025 range.** It is above July 2025 by 6 s at the nearest rank, and below it by the other two methods. Its median (6,897 s) is just above January–November's maximum (6,810 s).
- **January 2026 is above every 2025 month by every method.** The proposal's "Case against" 2 states this correctly.
- **The share of rows more than 1 h late is 81–96 % by month,** not 81–94 %. September 2025 is 95.8 %.

### (f) The FROZEN definition

- The proposal's four elements are adequate as the closing state:
  - STATE with **Phase: FROZEN**, the champion, and the file's path and hash;
  - the ledger event;
  - FINAL_REPORT final;
  - DAY_SUMMARY final.
- **It needs four additions (P7):**
  - the missing manifest fields of the final file;
  - a merge into `main` that changes no content;
  - the upload's own appended record, with the hash recomputed at upload;
  - a statement that FROZEN is enforced by records only.
- **Event name.** `frozen` is distinct from the Day 1 split `freeze` event and may stay as proposed.

## Novelty Relative to Existing Research

Not applicable as a proposal: the phase close allocates nothing and runs nothing.
- **The named access is the project's first measurement of the routing contrast outside the months that selected it.** Day 3 priced it on development folds only (E019 − E020 = +122.54 s), and no H record isolates it.
- **No comparison is repeated.** Rule 10 is not engaged.

## Experimental Isolation

- **On H, E046 and E033 differ on exactly 88 rows.** This is the route check, and my recomputation agrees: max |Δ| off the subgroup is 0.
- **The access therefore isolates the subgroup contrast.**
  - Other airports' clusters enter both arms identically.
  - They affect ΔRMSE only through the bootstrap's common denominator, which is second order.
- **One draw.** E046's non-subgroup rows are E033's draw, which was already scored on H on Day 5.

## Validation Quality

- **The frozen phase-close comparison is used unchanged:**
  - the paired cluster bootstrap over airport × UTC day, with 2,000 resamples and seed 20260927 combined with the fold id;
  - WIN if q0.90 < 0 and LOSS if q0.10 > 0.
- **The access is enforced by code:**
  - the phase comes from E046's gate record (`day-07`), with 0 of 1 accesses used;
  - prediction hashes are verified before the access line is appended;
  - the silver hash and H's 165,677 rows are verified before scoring.
- **The statistic and its mapping (U7) were pre-registered before any result.** U7 is stricter than the frozen rule: a TIE does not promote. That is justified, because the development folds carry no confirmatory weight (finding 1 of the H035 review). Changing U7 now would be a post-hoc change.
- **Instance check (P2).** The reference arm must reproduce E033's recorded H RMSE, 369.1811742636602 s. This is target-free in advance.
- **No other H read follows** (H7).

## Leakage Review

### Target Leakage

PASS

- **The access reads H truth once,** through the logged path.
- **E046 fits nothing.** E045's H-fold model trained on January–November rows only, with December masked.
- **December's targets enter only:**
  - the final-fold training of E042 and E043, already logged;
  - under WIN, E049's final-fold training and E050's unmasked load (U4).
- **This review read no target or block-time column,** and wrote no H figure.

### Temporal Leakage

CONCERN

This is inherited and not blocking.
- **The candidate's mechanism is the T channel:** for a convention record, y = `d_sched` = MVT − SCHED. It is admissible (DATASET_AUDIT §6.2), but it lies outside the causal-only variant (rule 8).
- **H is predicted from January–November training,** so the access shows no post-validation-month effect.

### Competition Availability

CONCERN

This is not blocking.
- **Every input exists for ranking DEP rows.** There are 107 and 276 subgroup rows.
- **The quantity the bet depends on, LIRF's 2026 recording practice, is unobservable:** block time is blanked in the ranking months.
- **January 2026's subgroup delay tail is above every 2025 month (D7-C7),** so its per-row stakes are the largest in both directions.

## Compute Review

### RAM

PASS

- The access loads two prediction files and one fold of truth: well under 1 GB.
- If promoted, E049 is about 7 GB (E042 7.02 GB) and E050 about 3.4 GB (E046 3.35 GB), within CLASS-M and CLASS-S.

### Runtime

PASS

- The access takes seconds.
- E049: about 280–600 s (E042 280 s; guard 600 s). E050: about 30 s.
- A failed W&B sync adds about 100 s per run after `runtime_s` (INC-0009). The window arithmetic must include it (P5).

### Disk

PASS

One JSON file for the access. Under WIN, about 10 MB of predictions and a tagged submission file of about 1 MB.

## Weakest Assumption

**That a December 2025 WIN on 88 rows carries information about January and July 2026.**
- H tests persistence one month forward, on rows whose delay tail is ordinary for 2025 (q90 mid-range; median just above January–November's).
- **January 2026's subgroup has the heaviest delay tail on record.** Its q90 is 17,816 s, against a 2025 maximum of 14,939 s.
- **July 2026 is seven months past the last training month.**
- **A change at the turn of the year would be invisible to H.** This covers a recording change at LIRF, or a provider-side cleaning of the ranking targets.
- **The stakes in each ranking month are of the order of the 2025 gain, in both directions** (U6). U8 (b)'s λ* is 0.20–0.57; the convention-absent loss is 0.25–1.30 times the 2025 gain.

## Missing Control or Ablation

None is required. No new run is authorized.
- **Named, still not done: the convention split** (the H035 review). It would separate the gain carried by block-at-schedule records from the gain on genuine long taxis.
- **Partly discharged here: the target-free feature-path check** (the H031 review), as consistency evidence only ((c)).

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **The Day 7 decisions stand as recorded:**
   - E042–E044 are the champion's SUBMIT procedure, with no flag;
   - E045 and E047 are components;
   - E046 is H035's candidate, with criteria 1–4 and 6 and the criterion 8 rule met, and objection F open;
   - E048 is the passing reproduction;
   - E049 and E050 are DEFERRED and ALLOCATED.

2. **Exactly one protected-holdout access (P1).** It runs under these conditions:
   - the acknowledgement below is committed and pushed first;
   - the tree is clean;
   - `runtime/experiment.lock` is held by no process;
   - the task ledger has no `day-07` `holdout_access` line;
   - E046 and E033 are COMPLETE in `experiments/ledger.jsonl`;
   - the rule L v2 item 6 environment is unchanged, as verified above.

   ```bash
   uv run python scripts/holdout_check.py E046 E033 --reason "Day 7 phase close (X-D07-S01-0003): phase-closing candidate E046 (H035 v1) vs phase-opening champion E033; objection F (U7 of X-D07-S01-0002)"
   ```

   **Failure handling (as on Day 5):**
   - If the command exits before a `day-07` `holdout_access` line is appended, no access occurred. Record the cause; the identical command may then be issued once more.
   - If the line was appended but no result file was written, stop. There is no re-run; a recovery review decides.

3. **P2. Instance check.** The result's `rmse_reference` must equal E033's recorded H RMSE, 369.1811742636602 s (`research/day-05/holdout/holdout_E033_vs_E026.json`), within 1e-9 s.
   - If it does not, stop. No promotion reading is made, and a recovery review decides.
   - Record the check beside the result. It is disclosure, unless it fails.

4. **P3. The outcome mapping (U7, unchanged).**
   - **WIN.** Objection F is resolved for December only, and H035 is promoted.
     - **Ledger:** E046 PROMOTE, and E048 PROMOTE as its reproduction. E045 and E047 stay null (components, U5).
     - **`models/champion/CURRENT.json`:** a new record, with the previous content kept as history. It holds:
       - champion E046 (H035 v1), previous E033;
       - model `override`: base E033 (E029 and E031 at 0.5/0.5), with source E045 on `LIRF_NM_missing`;
       - reproduction E048 (byte-identical);
       - the SUBMIT path `E049 + E044 → E050`;
       - environment rule L v2 item 6.
     - **Standing disclosures on E046:**
       - E033's: D3-C1; D3-C3 (D5-C16); D5-C8; D5-C9 (D6-C11); D5-C10; the 1,000-iteration budget; the Day 6 attribution;
       - U6;
       - U7 (WIN for December only);
       - rule 6: W1 is 0.79 one row (183903219), and the top-10 share of the SSE change is 0.73–0.97 (R2 0.726);
       - rule 12: subgroup bulk rows predicted above 3,600 s, e.g. S1 104 of 218, against E033's 0;
       - D7-C7 (January 2026's subgroup tail is above every 2025 month);
       - the H exposure of (a) (88 rows, 26 days; top day 0.29; 53 % of E033's H SSE).
     - **Task ledger:** a `champion_change` event from E033 to E046, whose basis cites this exchange and the H result.
   - **TIE.** E046 and E048 are INCONCLUSIVE ("phase-close holdout TIE; forward bet not confirmed"). E033 stays champion, and E044's file is final.
   - **LOSS.** E046 and E048 are INCONCLUSIVE ("phase-close holdout LOSS, frozen revert"). E033 stays champion, and E044's file is final.
   - **Under TIE or LOSS:**
     - E049 and E050 stay ALLOCATED and are recorded "never run (not needed: H035 not promoted)";
     - no substitute comparison follows;
     - INC-0015 closes with the phase-close records.

5. **P4. The terminal fallback under WIN (pre-registered here, before the access).**
   - **The final file is `predictions/final/E050/submitting.parquet` if and only if all of these hold:**
     - E049 and E050 are COMPLETE within class;
     - `route_check.py E050 E044 E049` passes;
     - `make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050` passes I1–I5;
     - no flag analysis is open, and none found a defect (S6).
   - **In every other case, E044's file is final.** This includes:
     - no owner window being set, or the owner declining one;
     - INVALID;
     - a failed check;
     - a RESOURCE_FAILURE or TIMEOUT whose single U10 rerun fails or is not run.

     E046 then stays champion. CURRENT.json, STATE and the final report say plainly that **the submitted file implements E033's procedure, not the champion's.**
   - **Nothing else may select between the two files:** not U8 (b)'s per-month exposure, not E050's flag reading (non-blocking unless a defect is found), and not any H figure.
   - **A fix by a new proposal version** needs a new Advisor review before FROZEN. This review authorizes none.

6. **P5. The E049/E050 window, under WIN only (U10, made concrete).**
   - **A new incident is recorded before the window.** It states the owner-set window and one of the procedures below, with the exact command sequence.
     - **(a) A new launcher** derived from `run_window_2.sh`. Its diff is limited to the date, window, log name and queue (E049, then E050), and its SHA-256 and diff go in the incident before arming.
     - **(b) Direct calls with a scripted checkpoint.** `run_experiment.py E049`, then the launcher's own-path checkpoint, then `run_experiment.py E050`, then `route_check.py E050 E044 E049`, then the checkpoint. The script is committed and hashed in the incident before the window.
   - **In both cases:**
     - **Tree state.** E049 records `git_dirty_at_run: false`. E050 records `true`, with `orchestration/task-ledger.jsonl` as the only porcelain entry (U3). Nothing is edited, staged or committed by hand during the window.
     - **Unmasking.** Exactly one unmasking event each for E049 and E050, inside their run spans (U4).
     - **Freeze.** The freeze diff from `76e80f1` over `src`, `scripts`, `config`, `pyproject.toml` and `uv.lock` is empty.
     - **Environment.** Rule L v2 item 6 holds.
     - **Window arithmetic.** It counts about 100 s of W&B overhead per run.
     - **No other run.**

7. **P6. E050's formatting and flags (U9, S6), with the bounds fixed now.**
   - **When:** after the window, with the lock free.
   - **The H035 §Batch SUBMIT flag.**
     - E045's development-fold subgroup share above 3,600 s is 0.452 (R2) to 0.654 (R3); the twins are 0.603–0.614.
     - **A ranking month flags if its E050 subgroup share is below 0.226 or above 0.981.** The flag is non-blocking (S6).
   - **Disclosure only:** U8 (b) per month, i.e. Σ(E050 − E044)², its RMS, and its top-1 and top-10 shares.
   - **Before any upload,** the owner receives:
     - U6 in plain words (the gain is a bet on the recording convention, with a downside of similar size);
     - every flag analysis.

8. **P7. FROZEN.** The proposal's definition is adopted, with these additions.
   - **(a) Manifest.** The FROZEN commit appends, for the final file, the fields DATA_POLICY §3 requires and the submission records lack:
     - the producing command;
     - the code commit of the formatter run and `make_submission.py`'s SHA-256;
     - the creation time.

     They are appended (STATE, the final report or a new file), never by editing `SUBMISSION_RECORD*.json`.
   - **(b) Branch and merge.** The FROZEN commit is pushed to `day-7`. The PR into `main` changes no tracked file relative to it: the merged tree equals the FROZEN commit's tree.
   - **(c) After FROZEN,** the tree changes only by appended files: corrections, the upload record and the external-evaluation record. There is no allocation, run, fit, holdout read, formatter run or code change.
   - **(d) The upload.**
     - It happens once, by the owner, with the recorded file unmodified. Its SHA-256 is recomputed immediately before upload and must equal the recorded one.
     - An appended record states the upload time, that hash and the FROZEN commit.
     - The researcher neither uploads nor reads the leaderboard. A figure the owner supplies is appended as an external evaluation only and is never fed back.
   - **(e) Timing under WIN.** FROZEN comes only after P4 has determined the final file.
   - **(f) Enforcement.** FROZEN is enforced by records only (Summary). This is stated in the final report.

9. **P8. Ruling H7 (recorded with this exchange).**
   - **What the access decides.** The Day 7 access is E046 against E033, and its outcome decides U7 only.
   - **The H figures are otherwise recorded only.** They inform no other choice (P4).
   - **No substitute comparison** follows any outcome.
   - **This is the project's last access.** There is no further H truth read in Day 7 or after FROZEN, including any audit of the result (concentration, or variants without a row).
   - **U6 is extended.** Under WIN, neither E046's development margin nor its H ΔRMSE is quoted as the submission's expected gain or error. The H figure is labelled "December 2025, E046 against E033, one access".
   - **What H does not test:** the SUBMIT procedure (H6 (f)), July's seven-month distance, or January's tail.

10. **P9. Records and incidents.**
    - **INC-0014** closes now: the window is complete, with no deviation.
    - **INC-0015** closes:
      - under TIE or LOSS, with this phase close's records;
      - under WIN, when E049 and E050 are COMPLETE or P4's fallback is invoked.
    - **INC-0004, INC-0009 and INC-0010 stay open.** The final report lists each with its state in one line. For INC-0009, the runs never mirrored are E036–E039, E042, E043 and E045–E048.
    - **`DAY_SUMMARY.md` and `FINAL_REPORT.md`** are marked FINAL only with D7-C1 to D7-C13 applied. Completed records (analyses, journal) take corrections by appended notes.

**Not authorized:**
- any other H comparison, or any run other than E049 and E050 (WIN only);
- the formatter, except under P6;
- any use of H figures beyond P3 and P4;
- any change to frozen files, reviews or completed records.

Required acknowledgement path: `research/day-07/acks/PHASE_CLOSE_D07_ack_v1.md`

**Contents of the acknowledgement:**
- the proposal hash (`5c5011cc…dd63`) and this review's hash;
- P1–P9 adopted as binding, with **P4 recorded in full** (the only new pre-registration);
- ruling H7;
- corrections D7-C1 to D7-C5 (DAY_SUMMARY §7) and D7-C6 to D7-C13 below, appended;
- the command in item 2.

**Corrections** (appended; the proposal and completed records are not edited):

- **D7-C6. STATE timestamp.** STATE's "Updated 2026-10-04T17:45Z" is later than the commit that contains it (`4fc1678`, 17:33:38Z). It is a pre-written timestamp, as D7-C2. The next STATE update carries the measured time.
- **D7-C7. Forward support.** This corrects the E046 analysis U8 (a), the journal's E046 entry and DAY_SUMMARY §4.
  - The 2025 maximum subgroup q90 is July 2025's 14,939 s, not 13,865 s (February).
  - At q90, July 2026 (14,945 s) is inside the 2025 range. It is above July 2025 by 6 s at the nearest rank, and below it by linear interpolation (14,461 against 15,035 s) or by the lower method (13,977 against 14,939 s).
  - Only January 2026 lies above every 2025 month: 17,816 s at the nearest rank, 19,592 s linear.
  - The share of rows more than 1 h late is 81–96 %, not 81–94 %.
  - "Both ranking months … above every 2025 month" becomes "January 2026 above every 2025 month; July 2026 at the 2025 maximum".
- **D7-C8. Final report §3, rule 11.**
  - **Day 3.** −6.75 s is the mechanism figure on `NM_present_excl_LIRF`. Congestion as served in the champion is **−1.90 s on all rows** (q95 −0.98), with R1 and R2 TIE and criterion 3 failing at EHAM (+7.2 %). 95 % of E019's margin over E005 was routed FS1 structure (D3-C1).
  - **Day 4.** −0.3 s is the restricted figure: −0.29 s, q95 +0.12, S1 TIE, W1 LOSS, mechanism falsified. On all rows it is −0.40 s (q95 −0.03).
- **D7-C9. Final report §3, Day 6.** Replace "Seven controls found nothing contradicting E033" with D6-C12:
  - no Day 6 result contradicts the promotion, but neither batch had real power against the performance claim;
  - the attacks able to overturn it (the SUBMIT procedure, D3-C3) were not run;
  - E035–E039 were the attribution ladder and E040–E041 were draws;
  - the margin held over three draws on all rows (spread ≤ 0.60 s), with a W1 mechanism-population spread of 2.00 s (D6-C11).
- **D7-C10. Final report §1 and §8, provenance.**
  - "claude-opus-5-5 … proposed, implemented, ran and analysed every experiment" overstates what happened:
    - by owner instruction for budget reasons, Day 4 implementation work and experiment launches were delegated to `claude-sonnet-5-5` workers under the researcher's review (INC-0005), and one Day 6 analysis script was delegated (INC-0013);
    - launch arguments differed from the registered configuration on Day 2 (effort `medium`, INC-0003) and on Day 3 (model and effort, INC-0004, open), and the effective tier cannot be determined;
    - the Day 7 candidate was tested by the owner's choice among researcher-written options, with the researcher's recommendation (INC-0015).
  - "Reviewed … every phase close before anything ran" is wrong: phase-close reviews follow their phase's runs.
  - Keep brief §15's statement verbatim, and state these facts beside it.
- **D7-C11. Final report §2, criterion 2.** It reads: at least 3 WIN among the 5 development folds; S1 WIN; no development fold LOSS; an S1 or W1 WIN counts only if its causal twin is not LOSS.
- **D7-C12. Submission manifests.** `SUBMISSION_RECORD.json` lacks the code commit, creation time and reproduction command (DATA_POLICY §3), and the formatter writes the same gaps. P7 (a) appends them for the final file.
- **D7-C13. Final report outcome branches** (§4, §5, §7).
  - **Under WIN:**
    - §4's "What the submission's accuracy rests on" adds the recording-convention bet on the 383 subgroup rows;
    - §5 states that the WIN is December only and does not discharge U6;
    - §7 counts the new incident.
    - If P4's fallback is invoked, §4 states that the submitted file is E044's.
  - **Under TIE or LOSS:** §5 states that E033's routing is the same bet in reverse.
    - If the convention persists in 2026, the routing pays its 2025 price (+122.5 s of development RMSE).
    - If it does not, the routing avoids a loss of similar size.
    - In RMSE terms, neither file is the safe choice.

## Revision

None required for this version. P1–P9, H7 and D7-C6 to D7-C13 are execution and record conditions under ACCEPT.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| The access completes on the first issue, and P2's instance check holds | 0.97 |
| E046 against E033 on H: WIN / TIE / LOSS | 0.85 / 0.07 / 0.08 |
| H035 promoted at this phase close | 0.85 |
| Given WIN: E050's file is final under P4 (owner window, all checks pass) | 0.88 |
| Given WIN: E050's H035 SUBMIT flag is raised in either month | 0.05 |
| Given WIN: E050's true RMSE is below E044's in January 2026 / July 2026 (unobservable within the project) | 0.85 / 0.82 |

Expected magnitude:
- **H, if WIN:** ΔRMSE between −40 and −160 s, central −100 s. E046's H RMSE would be about 210–330 s, against E033's 369.18 s.
- **If LOSS:** up to about +90 s if the convention were absent in December; less under a partial decline.
- **The ranking months:** of the order of 100–200 s of month RMSE in either direction, depending on the 2026 convention rate. January carries the larger per-row stakes.

Primary expected failure mode:
- **Primary: the December WIN read as confirmation of the bet.** H returns WIN on rows whose delay profile is ordinary, and the record then quotes the December or development gain as the submission's. A turn-of-year change in LIRF's recording, or in the provider's ranking targets, would cost about as much as it would otherwise gain, and nothing in the project can detect it (U6; P8).
- **Secondary: P4's fallback.** No owner window is set for E049 and E050, or E050 fails a check. The champion is E046, but the file submitted is E044's.
- **Tertiary: a TIE.** December's gain is confined to the top day (0.29 of the exposure), and objection F leaves H035 INCONCLUSIVE.
