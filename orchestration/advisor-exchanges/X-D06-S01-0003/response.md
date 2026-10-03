## Advisor result, X-D06-S01-0003 (batch H029–H030 v1)

**Both proposals are accepted (H029 at 0.80 confidence, H030 at 0.83), so the batch can run in tonight's 19:00–19:30Z window.** Each acceptance carries eight binding conditions, N1–N8. They are written once, in the H029 review; the H030 review adopts them by reference. None of them changes a design, threshold, population or fold. They govern how the results are worded, what is recorded, and the operational checks before the run.

**Checks done first.** Everything was read-only: no fit, no score, no target read from data, no holdout, and `holdout_check.py` was not run.
- **Hashes.**
  - Both proposal hashes match the envelope.
  - The launcher `run_window_2.sh` is `edfe11df…dadf3e`, on disk and at `9d245c0`. Its diff against the pinned launcher covers only the header comment, the date, the log name and the queue.
  - The frozen files, the Advisor definition and the diagnostics script `5fc21113…10b7` are intact.
  - Nothing frozen has changed since the Day 5 merge.
- **Lock, memory and GPU.**
  - No lock is held on `runtime/experiment.lock`; its "E039" text only names the last holder. I took and released one non-blocking shared lock as a probe.
  - About 9 GiB of RAM is available.
  - The GPU has 673 of 8,151 MiB in use (driver 591.91, CUDA 13.1).
- **Allocation state.** The next id is E040. No acks or E04x allocations exist yet.
- **Configs and inputs.**
  - H029's config equals E031's apart from the header fields. H030's differs from E033's only in its second component.
  - All 40 stored prediction files the batch depends on match their manifests.
  - The proposals' figures reproduce.

### Main findings

1. **E040 is not "the draw Day 7's submission will be".**
   - The submission fit trains on 12 months, so its CatBoost half is a fresh draw whatever the seed. The Day 5 phase close already ruled this.
   - Fixing seed 42 against E031 also fixes everything the seed drives: the Bayesian bootstrap, the score noise and the CTR permutations. E040 − E031 therefore measures only GPU run-to-run variation.
   - That variation should be no larger than the seed + GPU variation E032 already sampled, which is the kind a fresh submission draw carries.
   - So a pass is weaker evidence than it sounds. It is recorded as "robust to one further fixed-seed (GPU-only) draw" (N4, N5).
2. **Whether the refit is byte-identical is already known.**
   - Day 5's calibration fitted E031's exact parameters twice at seed 42 on R3's real training rows, and the prediction hashes differed (`h021_exact` in `gpu_calibration.json`).
   - The proposal gives P 0.10 for a byte-identical refit; I give 0.01.
   - N5 adds a "no further draw" outcome, so that a byte-identical refit cannot produce a "draw-robust" reading.
3. **The attack on the champion's performance claim has almost no power.**
   - The narrowest per-fold margin over E026 is W1's q90 of −1.98 s; S1's q90 is −3.29 s.
   - The largest blend re-draw so far moved a fold by 0.48 s.
   - I put P("draw-fragile") at 0.01.
   - The batch is a reproducibility measurement and a third draw for rule 13. It is worth one window, but it cannot realistically show E033 is wrong. The untested part of the Day 7 claim is the 12-month composite submission procedure, which no development-fold re-draw tests.
4. **CLASS-L cannot be inherited.**
   - H021's CLASS-L ruling was scoped to H021 and its reproduction only.
   - I ruled CLASS-L justified for H029 alone, as a confirmation run of a CLASS-L configuration whose measured peak RAM is within 0.9 GB of CLASS-M's limit.
   - The cost: E040's overrun limit becomes 8,100 s instead of INC-0012's 2,700 s, so a run could in principle continue to about 23:15 local. This must be recorded before the window (N2).

**H030-specific finding:** S1's 1.0 s tolerance check is close to a single-row test.
- About +0.24 s of E034's +0.27 s movement on S1 came from row 192622644. This is computed from stored predictions plus the recorded target and S1 RMSE.
- An E040 prediction below about 7,900 s, or above about 14,100 s, on that row would by itself put S1 past 1.0 s. The two CatBoost draws so far gave 10,976 and 10,237 s.

### What the conditions require

- **N1:** allocate H029 first (E040), then H030 (E041). Before arming, check each `gate.json` and that each config is identical to its reference.
- **N2:** use the launcher pinned by hash. Write a pre-window record covering the freeze diff, the environment, the GPU driver and memory in use, and E040's 8,100 s overrun limit.
- **N3:** no re-attempts. Deferral depends only on run status.
- **N4:** no record may identify E040 or E041 with the Day 7 draw, split the spread into seed and GPU parts, or read a WIN/LOSS between draws as an effect.
- **N5:**
  - "Criteria 1–3 hold" means the frozen check in `compare.py`, not the loose paraphrase in the proposal.
  - The 1.0 s tolerance is read per fold from `compare.py`.
  - The labelled three-draw min–max is reported beside the reading.
  - No outcome reopens criterion 6, E033's promotion or ruling H5.
- **N6:** before any reading, compare E040's resolved parameters with E031's, key by key on every fold. The script's built-in `max_ctr_complexity` exemption does not apply.
- **N7:** E032's and E034's side-by-side figures are recomputed with the same scripts and populations.
- **N8:** the usual records:
  - INC-0012 deviations;
  - the freeze diff from `9d245c0`;
  - diagnostics run after the window, memory-light;
  - the CLASS-M comparison and any swap use;
  - E040 and E041 never NEW.

**Recommended, not required:**
- Check GPU memory at arming and arm close to the window. The external 4.3–5.2 GB holder seen on 2 Oct could cause a GPU out-of-memory failure, and failures are not retried.
- Run `range_check.py E040`.

**My predictions:**
- E040: development mean about 440.8. Largest per-fold change against E031 about 0.6 s. RMS prediction change about 28 s.
- E041 against E026: mean about −5.6 s, all 7 folds WIN with P 0.95.
- H030 readings: "robust to one further fixed-seed draw" 0.93, "spread above tolerance" 0.05, "fragile" 0.01, "no further draw" 0.01.
- Operations: E041 runs tonight with P 0.78. E040 is still running at 21:30 local with P 0.06.

Files written (only these two):
- /home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H029_review_v1.md
- /home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H030_review_v1.md

Acknowledgements are due at:
- /home/rvindra/Projects/prc-data-challenge-2026/research/day-06/acks/H029_ack_v1.md
- /home/rvindra/Projects/prc-data-challenge-2026/research/day-06/acks/H030_ack_v1.md

```yaml
schema: advisor-task-result-v1
exchange_id: X-D06-S01-0003
status: COMPLETE
decisions:
  - proposal_id: H029
    proposal_sha256: 8511f3a17462e52634efcbe58aa7b141b40a277b10dadb6a3288df5c8944a802
    decision: ACCEPT
    review_path: research/day-06/advisor/H029_review_v1.md
    review_sha256: d6eaf072026d4824aee894f2fe39b9e2d27dbfb28dade1a0799dc53159bd91dd
  - proposal_id: H030
    proposal_sha256: 7695dc11a594aafec0e45149cdda3b94bcbab8f17e5614be6a5bfd08faeefd8a
    decision: ACCEPT
    review_path: research/day-06/advisor/H030_review_v1.md
    review_sha256: 5aae8ef025af235e09cc9e90fb630b72ac45aa04bddbce1f99ef807946fc92a1
completed_utc: 2026-10-03T08:44:33Z
```
