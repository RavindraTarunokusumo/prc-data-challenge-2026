I reviewed H009 v3 in exchange X-D02-S01-0003 and the decision is **ACCEPT** (confidence 0.85), with preconditions. The proposal hash matches the envelope. v3 fixes the one v2 defect and the three items that depended on it, and I found nothing new that blocks it. All checks were read-only: I read no December target, and I fitted, scored and allocated nothing. The only file I wrote is the review.

**The v2 defect is fixed.**
- Clause 2(a) now runs on `NM_present_excl_LIRF`: NM-present rows outside LIRF.
  - The population is defined without the target, in `prc.attribution.population_mask`, and has a test.
  - It was committed at `64c165b`, before v3 and before any FS1-family allocation (there is none).
- On E006's stored predictions, the largest single-row share of squared error on S1 and S1c falls from 23–24 % (row 192622644) to 1.3–1.4 %. No day-scale record is left in the population.
- A 5,000 s change in the prediction for S1's new top row moves S1 by about 1–2 s. In v2 the old row moved it by about 11 s.
- Rows outside LIRF with the block-at-schedule pattern carry at most 2.8 % of E006's squared error in this population. A ±15 % change there moves a fold by at most ±0.55 s.
- The Day 1 evidence v3 cites (E011 against E006 on the new population) reproduces exactly, and the pre-registered top-row shares are correct.

**Envelope request: the three preconditions are kept exactly.**
- **H010 (b):** the `fs1` function body is byte-identical to `cba278d`, and the model, parameters, folds and seed are unchanged.
- **H010 (c):** clause 3 is byte-identical to v2.
- **H012 (c):** clause 4 is byte-identical to v2, and the `NM_present` code path in `mechanism_check.py` is unchanged.
- Once the ack is committed, this ACCEPT satisfies precondition (a) of H010 v1, H011 v2 and H012 v1.

**Remaining exposures (they cannot decide a clause; the ack must record them):**
- **Late departures in clause 2(a):** rows with `d_sched` ≥ 3,600 s but a normal taxi time.
  - They carry 16–27 % of E006's squared error in the new population, and the differences there come from how the trees use `d_sched`, not from static structure.
  - When E011 was compared with E006 on the same inputs, they moved development folds by at most 1.4 s, but 22 of W1c's 30 s. That makes W1c the likeliest twin to come out LOSS and void a W1 WIN.
- **LIRF late departures in clause 2(b):** about ±2.0 s on S1. The clause needs two failing folds to falsify, so it stays insulated.
- **Row 183910286 in M2 on W1:** it can move that fold by about 11 s, well short of the expected −40 to −100 s.

**Preconditions before `gate.py allocate H009 v3`:**
1. `research/day-02/acks/H009_ack_v3.md` is committed.
2. `research/STATE.md` is refreshed with a measured header time. The researcher already committed to this; today the file still stops at X-D02-S01-0001.
3. The E006/E010 reuse conditions hold (`uv.lock`, `gbm.py`, `fs0`, silver).
4. `compare.py`, `mechanism_check.py` and `attribution.py` stay unchanged from `5ba9230` until clauses 1–4 are computed.
5. No experiment runs concurrently.

**Other checks:** the frozen files, the advisor definition and `uv.lock` match their pins. The tree is clean at `5ba9230`, `pytest` passes 99/99 and `ruff` is clean. v3's `created_utc` is a measured time.

**Process note:** incident INC-0003 is still open. At 19:30Z the running researcher process still carried `--effort medium`. It is recorded, so it does not block, but the owner should resolve it.

**Prediction:** probability 0.48 that H009 is not falsified and passes criteria 1–3 against E005. The most likely failure is clause 2(a) coming out TIE or LOSS on one development fold, where the static-key gain is 3 s or less.

The response mirror (`response.md` and checksums) is left to the researcher, as in earlier exchanges.

Review file: /home/user/prc-data-challenge-2026/research/day-02/advisor/H009_review_v3.md

```yaml
schema: advisor-task-result-v1
exchange_id: X-D02-S01-0003
status: COMPLETE
decisions:
  - proposal_id: H009
    proposal_sha256: f013c86f75d0cfb3b8643862cf3829991ad095a38f045f2e965e1f298f303a20
    decision: ACCEPT
    review_path: research/day-02/advisor/H009_review_v3.md
    review_sha256: 7cc7a069f022d2594e2be89a2709e0cb256dd1a9883c9647a59387876b08d81e
completed_utc: 2026-09-28T19:35:56Z
```
