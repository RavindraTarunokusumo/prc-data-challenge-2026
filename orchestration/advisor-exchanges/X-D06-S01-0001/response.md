## Advisor result, X-D06-S01-0001 (batch H024–H028 v1)

**All five proposals get REVISE, so nothing is authorized to run yet.** Every required change is text, except one config value in H027. None needs new compute. A v2 that changes only the listed items can be reviewed against those lists.

**Checks done first (read-only):**
- All five proposal hashes match the envelope.
- The experiment lock is free: no lock is held on `runtime/experiment.lock`, and its `E034` stamp only names the last holder. About 9.9 GB of RAM was available.
- No fit, no score, no truth read, no holdout access.

### What blocks execution

1. **H027 cannot run as written.** The runner (`scripts/run_experiment.py`, `check_config`) only accepts seed 42 for primary or rerun runs and 43 for reproductions (`config/splits.yaml`). It refuses seed 44 before the run starts. The launcher would log `rc=1 status=ALLOCATED` and defer E039, so rung A would be lost. Changing the seed does no harm: E029's seed has no effect, and the routed ridge gives identical rows across seeds.
2. **The readings are lopsided (shared batch text).**
   - "Rung X carries the gain" needs only a point estimate, D(X) < +1.0 s. There is no INCONCLUSIVE zone below +1.0 s.
   - The opposite reading needs a mean of at least +1.0 s and LOSS on 3 or more folds.
   - The bootstrap does not include the GPU draw.
   - The lenient side is the one that would write disclosures on E033 and that matters for Day 7 selection (rung C as a cheaper substitute).
   - The fix is a bound of comparable strength, for example the bootstrap q95 of D's mean below +1.0 s. H024's own "no measurable signal" reading needs the same.
3. **Rung A is mislabelled, and the falsification list overclaims.**
   - Rung A swaps out the whole CatBoost half: the learner, the raw keys (FS2_RAW against FS2's `__RARE__` collapse), the categorical statistics and most of the disagreement.
   - Its expected LOSS (P 0.90) follows from its construction, since the twin is built to stay close to E029.
   - So that LOSS cannot be recorded as "the different family carries part" or "each removed ingredient is needed".
   - Day 5's accepted scope is "this CatBoost configuration as a whole" (H023 v3, revision 6). The DAY_SUMMARY §1 phrase "a second learner family adds signal" is broader than that, and this batch cannot widen it.
4. **Noise reference.** A blend-level re-draw has already been measured. E034 against E029, compared with E033's file, moved the 5-fold mean by +0.26 s, and W1 alone by +1.28 s. Separately, the re-draw E032 against E031, with no treatment at all, gave LOSS on R1 and W1.
5. **"Ordered boosting" is wrong.** Every CatBoost arm runs `boosting_type: Plain` with Bayesian bootstrap. This appears in the batch text and in H026.
6. **Population mismatch.** The readings use `NM_present_excl_LIRF`, but the residual correlations are planned only for all rows and bulk rows. They must also be reported on the readings' population.
7. **Deferral must not depend on results.** A deferred run goes ahead at the owner's next window whatever the other rungs show. If no window comes before the phase close, it is recorded as "not run (window)".
8. **Launcher.**
   - **Pinning.** Pin it by path and SHA-256 (`6bd1f1248225f856ef0d2b131e269aba38755c53f98860a75c3aab045a449c45`), and include it in the freeze diff. It is currently outside the tools freeze.
   - **Overrun.** State the overrun bound. The launcher never kills a run, and the CLASS-M timeout is 2,700 s, so E035 could run to 21:45 and E038 to 21:59. Any run still going at 21:30 is reported as an INC-0012 deviation.
9. **H024 only.**
   - Pre-register a closed exempt set for its resolved parameters against E031, as H022 v3 did.
   - Its 1.0 s threshold is 1.47× the measured full-size re-draw (+0.68 s), while H021 v3 required at least 2×. Justify it or restate it.

**Binding ruling (no revision needed):**
- The batch's experiments join the "never NEW" list.
- Rule 10 covers their configurations: no unchanged re-submission as a candidate.
- Any Day 7 use is a new configuration that states the selection.

### What stands

- H024 is a clean single-parameter ablation in the right class.
- Rung B (H026) is the control Day 5 named and never ran. It is the decisive rung and costs no training.
- Gating is by status only, there is no holdout access, and stating the readings against E033 directly (on D) is the right design.
- All cited figures reproduce from `research/comparisons/`, and 24 of 24 component prediction files match their manifests.

### Recommended (non-blocking)

- Stage only each run's own paths at checkpoint, not `git add -A`.
- Re-check for a clean tree when the window opens, not only at arming.
- Pin the time zone, and make the push non-interactive with a timeout.
- Consider running rung B first. Under the v1 order, an E035 overrun past about 21:29 defers it.
- E038's 950 s worst-case figure is only 6 % above E029's measured 893 s.
- Report the exact accuracy/disagreement split per rung (½ MSE₁ + ½ MSE₂ − ¼ mean((p₁ − p₂)²)).
- Have the H026 acknowledgement attest that no E029 + E030 blend figure was computed before the run.
- Cite H027's subsampling values, or state them as a choice.

### Review files

- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H024_review_v1.md` (contains the shared batch findings)
- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H025_review_v1.md`
- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H026_review_v1.md`
- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H027_review_v1.md`
- `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/H028_review_v1.md`

I did not write `response.md` or `checksums.sha256`. Per the communication contract, you store this message verbatim.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D06-S01-0001
status: COMPLETE
decisions:
  - proposal_id: H024
    proposal_sha256: abdaba7806b306347db048a070cb9cd7baa9a865a133fdc40fb3da88cae05c7d
    decision: REVISE
    review_path: research/day-06/advisor/H024_review_v1.md
    review_sha256: 68904b081ae3e3da22c74f056d931a6dee04a45c5556a533daaa6371a6fc2cf7
  - proposal_id: H025
    proposal_sha256: de55d6af78decf148b089518b3815c33af91cf3ec2121378016931997354395f
    decision: REVISE
    review_path: research/day-06/advisor/H025_review_v1.md
    review_sha256: 43a476902e98fa566c1ac8c4efbea373de260ad23b717adcf47e4c33a0cd23cf
  - proposal_id: H026
    proposal_sha256: dbcef1904ffc6ce28c70fecdf6f57d1ebe7323c806707a9ed507e85eebfdcd71
    decision: REVISE
    review_path: research/day-06/advisor/H026_review_v1.md
    review_sha256: 7db3204fad6e0263ede6ec0c81de0ec2ab7535cadab9a25709e9a07dd3079140
  - proposal_id: H027
    proposal_sha256: 361b317e712dde78a59bc32ba62cb1469849f524e5626f3553c4bbc9ebc802bf
    decision: REVISE
    review_path: research/day-06/advisor/H027_review_v1.md
    review_sha256: ac3dee47fe32a6bf3a034dda2f6e685c014477790276e2c874aa016bc08bb5b3
  - proposal_id: H028
    proposal_sha256: 172b45ad51e788879cf90ccd5187dc3e6cd4972cb96bd30312404d6896622675
    decision: REVISE
    review_path: research/day-06/advisor/H028_review_v1.md
    review_sha256: 05bf484b48cfc17fbdd5761e8040beb6ea113fd40b511b7147f6c7eb628a2d2e
completed_utc: 2026-10-02T17:47:36Z
```
