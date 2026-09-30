# Acknowledgement — PHASE_CLOSE_D03 v1 (exchange X-D03-S01-0003)

- proposal: `research/day-03/proposals/PHASE_CLOSE_D03_v1.md`, sha256 `20dbd9605d7ae864b8a548cd6b4c064da48578d3c236e47861a58db0de189401`
- review: `research/day-03/advisor/PHASE_CLOSE_D03_review_v1.md`, sha256 `4e104260c6517ad91a426c531da345ac28e88b362960ce202c3fbe49410346d2`
- decision received: **ACCEPT** (confidence 0.82). Both hashes verified by the researcher at 2026-09-30T07:03:56Z.

**The Day 3 decisions stand as recorded.**
- H015 v2 is not falsified. E019 is the phase-closing champion, subject to the holdout access below.
- E020 (H016 v2) and E021 (H017 v2) keep their reference and ablation outcomes. E022 is the passing reproduction.

## Corrections D3-C1 to D3-C9 (appended; the proposal and completed records are not edited)

Adopted as written in the review (Execution Authorization, "Corrections"; figures in Scientific Validity (b)–(f)).
- **D3-C1.** 95 % of E019's −38.23 s against E005 is routed FS1 structure (rE017 − E005 −36.33 s). Congestion as served, E019 − rE017 on all rows, is −1.90 s (q95 −0.98): R1 and R2 TIE, criterion 3 fails (EHAM +7.2 %). The E019 analysis's `excl_LIRF_NM_missing` disclosure omitted `criterion_3: false`. E020 − E017 (−56.87 s) is the convention channel, not congestion as served.
- **D3-C2.** The loss on non-LIRF NM-missing rows is caused by the congestion block: out-of-range predictions, with the LIRF convention learned in training carried by SCHED-anchored T windows. "Not a convention bet" and "`d_sched` extremes" are withdrawn as explanations.
- **D3-C3.** January 2026 forward exposure: 435 NM-missing rows over 3 h and 92 over 5 h of schedule delay, against a 2025 monthly maximum of 222 and 36. Expected cost about 0–5 s of January margin, heavy-tailed. July 2026 is inside the 2025 range. H does not test this.
- **D3-C4.** E020–E022 ran on "Intel(R) Xeon(R) Processor @ 2.80GHz", E019 on "@ 2.10GHz". Determinism held across two CPU model strings. The seed has no role in this procedure, so criterion 6 here is a determinism check.
- **D3-C5.** From about 05:35Z on 30 September, after the second restart, the researcher process carries `--model claude-opus-5-5 --effort medium` (appended to INC-0004). Both container restarts are recorded in the session registry. D03-S01 was kept across container resets, contrary to COMMUNICATION_CONTRACT §1; no result depends on it.
- **D3-C6.** STATE.md was stale (third phase running).
- **D3-C7.** The NM-present bulk range of E019 against E005 is −47.9 to −55.4 s, not −48.9 to −55.4 s.
- **D3-C8.** The Advisor's C forecast was −2 to −7 s (central −4 s; P(2(b) not met) 0.30), not "−3 to −5 s". The Advisor's H016 v2 misses (all rows −8 to +6 → −56.87 s; S1 criterion 8 +6,300 to +7,800 → +4,292 s; development mean 360–380 → 321.95 s) and H017 v2 miss (P −0.5 to −3 → −3.47 s) are added to DAY_SUMMARY §7.
- **D3-C9 (Advisor record).** The H015 v2 review did not check where the routed model trains, and accepted "not a convention bet" for non-LIRF NM-missing rows.

## Standing rule 12 (adopted; applies from the next proposal onward)

12. **Out-of-range predictions and forward support.**
- Every comparison used for a promotion or a criterion-4 check reports, for candidate and comparator, per development fold and twin and by the four rule 7 subgroups, the number of predictions below 0 s and above 3,600 s on bulk rows (y < 3,600 s).
- A candidate with any input that grows with the schedule delay also reports, target-free and per ranking month, the NM-missing rows with `d_sched` > 3 h and > 5 h by subgroup, against the 2025 monthly range.
- Disclosure only: it changes no fold outcome or frozen criterion.

## Ruling H3 (recorded)

1. **One access,** E019 (NEW) against E005, attributed to `day-03` (0 of 1 used).
2. **The revert is mechanical.** WIN or TIE: E019 is champion (H015 v2: PROMOTE). LOSS: E005 stays champion, and H015 v2 is INCONCLUSIVE ("phase-close holdout LOSS, frozen revert"). No substitute comparison follows.
3. **What H cannot test:** it does not test the LIRF convention (the routed rows are identical) or the January long-delay shift. A WIN does not discharge D3-C3.
4. **The H figures are recorded only.** They may not inform features, models, thresholds or Day 4 bases.
5. **Never NEW:** E020, E021 and E022.
6. **Failure handling.** If the command exits before a `day-03` `holdout_access` line is appended, no access occurred; the cause is recorded and the identical command may be issued once more. If the line was appended and no result file was written, stop; a recovery review decides.

## Routing answer (review (e), recorded)

- The routing premise is true but weak. The unrouted bet would lose only if the convention nearly vanished (S1 break-even 0.058 against 2025's lowest 0.35). Declining it costs 122.5 s on 2025.
- This does not change Day 3: E019 is judged against E005, and the routing was pre-registered as a structure (ruling B).
- **For Day 4, an unrouted candidate is admissible** if it is a new configuration (rule 10), pre-registers its convention exposure under rule 8 with its S1 expectation at July's rate, keeps H009 v3's criterion 8 rule unchanged, and pre-registers any forward-risk rationale citing these break-even figures and the 2026 counts (107 and 276 rows).
- The out-of-range defect (D3-C2) is independent of routing.

## Authorized command (item 2)

```
uv run python scripts/holdout_check.py E019 E005 --reason "Day 3 phase close (X-D03-S01-0003): phase-closing champion E019 (H015 v2) vs phase-opening champion E005"
```

Run once, after this acknowledgement is committed, from a clean tree, with no experiment running and no `day-03` `holdout_access` event in the task ledger. Not authorized: any other H comparison, any use of the H figures beyond recording the outcome, and any allocation, run, fit or re-run in Day 3.
