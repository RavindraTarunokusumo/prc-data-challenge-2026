# E044 analysis: H033 v1 (the SUBMIT blend: E033's construction on E042 and E043) and the batch reading (H031–H033 v1)

**Outcome: the submission exists and passes every blocking check.** Integrity readings 1–4 of H031 §Batch hold (with S4's reading), `make_submission.py`'s I1–I5 hold, and no sanity flag (a)–(c) is breached. Two pre-registered expectations on the mean prediction were missed (§Missed). No flag analysis is open (S6).

## Runs (INC-0014 window, 2026-10-03 19:00–20:00Z)

| Run | Status | Runtime | Peak RSS | Start → finish (UTC) | `git_dirty_at_run` |
|---|---|---|---|---|---|
| E042 (H031, LightGBM) | COMPLETE | 279.7 s | 7.02 GB | 19:00:05 → 19:04:46 | false |
| E043 (H032, CatBoost GPU) | COMPLETE | 419.3 s | 7.69 GB | 19:06:38 → 19:13:38 | true (S3) |
| E044 (H033, blend) | COMPLETE | 11.2 s | 3.54 GB | 19:15:21 → 19:15:32 | true (S3) |

- The queue ended at 19:15:43Z, inside the window. **No INC-0014 deviation.** All runs within class; no swap.
- **S3:** each post-checkpoint WARNING lists only `orchestration/task-ledger.jsonl`. The three unmasking lines were committed in the first commit after the window. E043 and E044: "`git_dirty_at_run: true` (task-ledger append from the final-fold unmasking only; S3)". No clean-tree-at-each-run claim is made for this batch.
- **S4:** exactly one `holdout_targets_unmasked_for_final_training` event each for E042 (19:00:12Z), E043 (19:06:44Z) and E044 (19:15:28Z), each inside its run span; no other experiment has the event. E044's: unmasked silver loaded; no target used (blend; the FS0 frame supplies row ids only).
- **S5:** E043's resolved parameters equal E031's key by key; `data_partition` FeatureParallel in both. No flag.
- **W&B (INC-0009):** E042 and E043 mirror attempts failed (CommError); E044 mirrored. Records unaffected.
- **Freeze:** `git diff --stat eedcd47 c59212a -- src scripts config pyproject.toml uv.lock research/day-07/sessions/D07-S01/run_window.sh` is empty. Environment as rule L v2 item 6 (python 3.13.15, polars 16).
- Launcher log: `research/day-07/sessions/D07-S01/run_window.log`.

## Integrity (blocking)

1. E042, E043, E044 COMPLETE within class. **Holds.**
2. `route_check.py E043 - E042` PASS (routed rows 107 / 276; max |diff| 0.0 s). **Holds.**
3. `make_submission.py E044 E042 E043 --ref E033 E029 E031` (run at 20:00Z after the window closed, lock free; S8): **I1–I5 all hold**. 344,841 rows; template ids, order and dtypes (Float64, Int32). **Holds.**
4. S4 reading above. **Holds.**

**The submission file:** `predictions/final/submitting.parquet` (git-ignored), **SHA-256 `d57ff7db7dfa34e13934aa524464ea13dbe9f5f904fae400a85f87e62c95af73`**, 1,091,362 bytes. Record: `research/day-07/submission/SUBMISSION_RECORD.json` (template hash, source prediction hashes, I1–I5, readings, references). Post-processing: nearest-integer rounding (half to even) only; max |change| 0.49999 s, RMS 0.288 s.

## Sanity readings (non-blocking; thresholds pre-registered in H031 §Batch)

| Reading | SUBMIT_JAN | SUBMIT_JUL | Flag limit | Reference (E033, 8 folds) |
|---|---|---|---|---|
| (a) predictions < 0 s | 19 (0.012 %) | 22 (0.011 %) | > 0.05 % | 5–35 (≤ 0.024 %) |
| (a) predictions > 3,600 s | 335 (0.219 %) | 120 (0.062 %) | > 0.25 % | 62–215 (≤ 0.113 %) |
| (b) mean prediction | 1,062.8 s | 1,002.0 s | outside 940–1,070 | 977–1,026 |
| (b) median prediction | 976.8 s | 952.1 s | outside 880–1,010 | 918–970 |
| (c) RMS(E042 − E043) | 110.0 s | 100.9 s | > 205 s | 85.9–136.7 |

**No flag.** January sits close to two limits ((a) above 3,600 s, at 0.219 % against 0.25 %; (b) mean, at 1,062.8 against 1,070) and is disclosed:

- Both halves give the same January level (E042 1,062.7 s; E043 1,062.9 s), so it is not one learner's artefact.
- January 2026's inputs differ from every 2025 winter month (target-free, DEP rows): mean schedule delay 36.4 min and 13.5 % of departures more than 1 h late, against January 2025's 30.0 min and 9.1 % (2025 range 26.2–38.5 min and 5.9–14.9 %, the maxima in July 2025). January 2026 is a winter month with near-peak-summer delay levels, and its NM-missing share is 1.61 %.
- January's predictions above 3,600 s are on NM-present rows (325 of 335) with a median schedule delay of 123 min. They are at LFPG 102, EHAM 81, LTFM 48, EDDF 38 and EGLL 30.
- Per-airport January means are above H's (December 2025) most at LTFM (+199 s), LSZH (+140 s), EDDF (+132 s) and EHAM (+125 s). They are within 51 s of H at EGLL, LEBL, LEMD, LFPG and LIRF.
- July 2026's schedule delays are below July 2025's (34.6 against 38.5 min), and its per-airport means sit within 69 s of S1's (largest EGLL −69 s, LFPG −60 s, LTFM −57 s).

| Airport | JAN rows | JAN mean | H mean | W1 mean | JUL rows | JUL mean | S1 mean |
|---|---|---|---|---|---|---|---|
| EDDF | 15,667 | 1,018 | 886 | 847 | 20,650 | 874 | 886 |
| EDDM | 10,953 | 991 | 925 | 837 | 15,013 | 783 | 797 |
| EGLL | 19,283 | 1,341 | 1,387 | 1,299 | 20,557 | 1,378 | 1,447 |
| EHAM | 16,232 | 903 | 778 | 799 | 21,950 | 846 | 809 |
| LEBL | 12,201 | 904 | 931 | 911 | 17,879 | 990 | 1,000 |
| LEMD | 16,802 | 1,017 | 1,008 | 978 | 20,152 | 1,032 | 1,045 |
| LFPG | 18,129 | 1,062 | 1,034 | 999 | 21,743 | 988 | 1,048 |
| LIRF | 11,061 | 1,053 | 1,078 | 1,047 | 15,838 | 1,265 | 1,285 |
| LSZH | 9,995 | 889 | 749 | 736 | 13,155 | 754 | 751 |
| LTFM | 22,396 | 1,210 | 1,011 | 1,140 | 25,185 | 1,026 | 1,083 |

(H, W1, S1: E033's mean predictions on those folds; predictions only, no truth.)

**Rule 7 split of (a):** January below 0 s: 19, all `NM_missing_other`; above 3,600 s: `NM_present_other` 325, `NM_present_LIRF` 2, `NM_missing_other` 8, routed 0. July below 0 s: 22, all `NM_missing_other`; above 3,600 s: `NM_present_other` 49, `NM_present_LIRF` 70, `NM_missing_other` 1, routed 0.

**D3-C3 rows (rule 12):** January 2026's NM-missing non-LIRF rows with `d_sched` > 3 h number 435 (mean prediction 1,373.8 s) and > 5 h number 92 (1,274.5 s). **None is predicted above 3,600 s** (E033's development out-of-range share in the > 3 h band: 0.57 %). Their accuracy is untested (no truth).

## Missed expectations (kept)

- H031 §Batch: "2026-07's mean prediction above 2026-01's (as S1 above H/W1)". **Missed:** January 1,062.8 s, July 1,002.0 s.
- H033: mean prediction "2026-01 about 975–1,000 s; 2026-07 about 1,010–1,040 s". **Both missed** (1,062.8; 1,002.0). The forecast carried 2025's seasonal pattern forward; January 2026's delay inputs do not follow it.
- The Advisor's E042 range (2026-01 960–1,010 s) was also missed; its runtime forecast (300–480 s) was missed low (279.7 s).
- Expected and met: integrity 1–4 (P 0.9), no flag (P 0.8), rounding RMS about 0.29 s, routed rows, runtimes and RAM within the stated ranges except E042's runtime (5–8 min forecast; 4.7 min).

## Disclosures (S9)

- **What the submission is:** E033's construction refit on all 12 months of 2025, carrying **one GPU draw** of the CatBoost half. Its accuracy is **not measured by any fold or by H** (ruling H6 (f)). No figure here is an expected error. E033's development mean (438.87 s) and H figure (369.18 s) are E033's, not the submission's.
- **Reading (c)** is the halves' disagreement, not a draw change; rule 13's quantities cannot be computed on final folds.
- **Asymmetries (§6.5):**
  - the six-month gap between the last training month (December 2025) and July 2026;
  - the 1 July month edge (no 30 June context for the first hours);
  - the NM-missing share: 1.61 % (Jan) and 1.48 % (Jul), against 0.62–2.06 % by 2025 month (January 2025 0.93 %, H 1.00 %, W1 0.77 %);
  - January 2026's delay level, above.
- **Role:** E042–E044 are not candidates, never NEW, never scored; no holdout; ledger decision null.
