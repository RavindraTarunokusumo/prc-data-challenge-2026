## X-D06-S01-0004: Day 6 phase-close review

**Decision: ACCEPT (confidence 0.84).** This comes with binding corrections D6-C6 to D6-C15, ruling H6 (holdout closed unused) and a new disclosure-only standing rule 14. The decisions stand, but the draft `DAY_SUMMARY.md` may not be marked FINAL as written.

Review file: `/home/rvindra/Projects/prc-data-challenge-2026/research/day-06/advisor/PHASE_CLOSE_D06_review_v1.md`

**What stands**
- **E033 remains champion.** The phase-opening and phase-closing champion are the same run. No Day 6 result contradicts the Day 5 promotion. All three blend draws meet criteria 1–3 against E026 with 7/7 WIN: E033 −5.62 s, E034 −5.54 s, E041 −5.52 s.
- **Ruling H6.**
  - Record "Day 6: 0 of 1, closed unused", not a TIE. There is no carry-over and no substitute comparison.
  - No `holdout_check.py` run with any of E035–E041 as NEW is authorized, in any phase.
  - H cannot test the SUBMIT procedure, because SUBMIT trains on December.
- **Readings.** Every reading follows its pre-registered rule, and every figure I recomputed matches. Rung C keeps its reading with the disclosure, as pre-registered; relabelling it INCONCLUSIVE now would break rule 10.

**What I found against the Day 6 records.** All are disclosures, not reversals.
1. **Rung B depends on which champion draw is the reference (D6-C6).**
   - E033 is the most favourable of the three draws on normal taxis: −3.96 s, against −3.70 s (E034) and −3.60 s (E041).
   - Against E041, rung B's contrast is +0.97 s, below the +1.0 s "carries part" line.
   - Rungs A and C hold against every draw.
   - With E041 included, the noise reference is 2.8× the larger blend re-draw, not 4×.
2. **`data_partition` confounds the "statistics" and "combinations" labels (D6-C7, D6-C8).**
   - E036 has 9 categorical features and CTRs, yet resolved DocParallel. This refutes the premise Day 5 used to exempt the key ("FeatureParallel with categorical features").
   - E030 and E031 both started at 853 MiB of GPU memory and resolved differently. So the partition follows the CTR configuration, not memory, which disfavours case-against item 7.
   - Every FeatureParallel run in the repository is a complexity-4 run.
   - Despite this, the records state from E036's INCONCLUSIVE values that "the combinations hold all of it".
3. **The January-analogue gain depends on the draw (D6-C11).**
   - On normal taxis, clause 1's W1 gain over E029 is −1.59, −0.31 and +0.40 s across the three draws.
   - On normal taxis the W1 spread is 2.00 s. The proposed disclosure quotes only the all-rows spread (≤ 0.60 s), and rule 13 requires the mechanism-population figures.
   - 69 % of E033's W1 gain sits in the LIRF and NM-missing rows, which are 8.2 % of W1 rows.
4. **Overclaims (D6-C9, D6-C10, D6-C12).**
   - "Survives both attacks": the ladder did not test the performance claim, and batch 2 had almost no power.
   - "Needs E031's configuration" is a necessity claim the ladder cannot make.
   - Finding 3 is an unregistered, un-bootstrapped difference of two means.
5. **Record errors (D6-C13 to D6-C15).**
   - E036–E039 never reached W&B ("failed to init run"), but the record says the runs "were mirrored at completion".
   - The delegated script and the closed-set output were written about 21 s before the window closed, after the queue had ended. This had no consequence.
   - The test file lacks the INC-0013 provenance line.
   - The largest missed forecasts are not recorded: E036 − E030 was forecast near −3.6 s and came in at +0.04 s, and the Advisor gave the closed-set violation P 0.08.

**Incidents.** INC-0012 and INC-0013 close. INC-0009 (updated with the W&B facts), INC-0010 and INC-0004 stay open.

**Carried forward to Day 7 (named, not required):**
- a pre-registered check of the SUBMIT procedure;
- D3-C3, the January long-delay exposure;
- a run with `data_partition` equalized between complexity 1 and 4;
- a second draw of E030;
- the causal-only variant anticipated by the dataset audit.

**Checks.** All read-only. The lock was checked first (no lock held; the `E041` text is a stale stamp). There was no fit and no truth read, and `holdout_check.py` was not run. The frozen hashes, the empty Day 6 diff over code and config, and the task ledger (no Day 6 holdout access) are all intact. I wrote only the review file. `response.md` and `checksums.sha256` are for you to mirror.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D06-S01-0004
status: COMPLETE
decisions:
  - proposal_id: PHASE_CLOSE_D06
    proposal_sha256: b777deb6ef9faf6de2f9339b131aabde1d765e9f2726abb113b14e61b27347f7
    decision: ACCEPT
    review_path: research/day-06/advisor/PHASE_CLOSE_D06_review_v1.md
    review_sha256: 80cab9817e18dbe124771c46853aeb95633726fa63a3505710e3879061e5cc08
completed_utc: 2026-10-03T16:26:37Z
```
