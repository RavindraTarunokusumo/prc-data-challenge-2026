# Advisor response — X-D03-S01-0003 (phase close)

Final message of the `advisor` subagent, mirrored verbatim below the rule. No secrets present.

---

## Phase close X-D03-S01-0003: **ACCEPT** (confidence 0.82)

E019 (H015 v2) is the Day 3 phase-closing champion, subject to one holdout access against E005. On a LOSS the promotion reverts and E005 stays champion. The proposal hash matches the envelope (`20dbd960…`).

### Holdout access (rule 9)
Run it only after `research/day-03/acks/PHASE_CLOSE_D03_ack_v1.md` is committed, from a clean tree, with no experiment running:
```
uv run python scripts/holdout_check.py E019 E005 --reason "Day 3 phase close (X-D03-S01-0003): phase-closing champion E019 (H015 v2) vs phase-opening champion E005"
```
- **WIN or TIE:** E019 is champion.
- **LOSS:** revert to E005; H015 v2 is recorded INCONCLUSIVE.
- **If it exits before a `day-03` access line is logged:** no access happened; record the cause and you may issue the same command once more.
- **If the line was logged but no result file was written:** stop. No re-run; a recovery review decides.
- **Never NEW:** E020, E021 and E022. The H figures are recorded only and must not inform any choice.

### The attack on E019
I could not show E019 is worse than E005. Every decisive figure matches the committed JSONs to 0.01 s when re-derived from the prediction files. But the record overstates Day 3 in three places:
- **D3-C1: congestion is about 5 % of the margin.**
  - A routed E017 (E017 with E005's predictions on the routed rows) is already −36.33 s against E005.
  - E019 improves on it by only −1.90 s on all rows (q95 −0.98). R1 and R2 are TIE, and EHAM is worse by +7.2 %, which fails the 3 % airport tolerance.
  - The committed `excl_LIRF_NM_missing` disclosure already shows that criterion 3 failure; the E019 analysis omitted it.
- **D3-C2: the congestion block causes bad predictions on NM-missing rows at the nine non-LIRF airports.**
  - E017 beats E005 on that group's bulk on all five development folds; E019 loses on four.
  - E019 predicts negative taxi times, or values above 3,600 s for normal taxis, on 44 % of rows delayed more than 5 h (E017 4.3 %, E005 0).
  - Cause: the LightGBM part trains on the LIRF convention rows (routing only swaps predictions), and schedule-anchored in-taxi counts carry that pattern to other airports. So "not a convention bet" is wrong for these rows.
- **D3-C3: January 2026 is outside the 2025 range for those rows.**
  - Target-free counts, December excluded: 435 rows delayed more than 3 h and 92 more than 5 h, against 2025 monthly maxima of 222 and 36.
  - Expected cost is about 0–5 s of E019's January margin, with a heavy tail. The development margins are 21–49 s, and the December holdout cannot test this.

### Answer to your routing question
Routing costs 122.5 s on 2025. The unrouted E020 would lose to E005 on the routed rows only if the convention rate fell below 0.009–0.099 per fold; 2025 rates were 0.35–0.76. E019's promotion is unaffected. An unrouted Day 4 candidate is admissible if it:
- is a new configuration (rule 10);
- pre-registers its convention exposure under rule 8;
- keeps H009 v3's criterion 8 rule unchanged.

### Other corrections (D3-C4 to D3-C9)
- **CPU strings:** E020–E022 ran on "@ 2.80GHz", not the 2.10 GHz their analyses state. Determinism therefore held across two CPU model strings.
- **INC-0004:** the researcher process running since about 05:35Z carries `--model claude-opus-5-5 --effort medium`.
- **Session record:** neither container restart is in the session registry, and the session number was not advanced as the contract requires.
- **STATE.md:** stale again.
- **Figure:** the NM-present bulk range starts at −47.9 s, not −48.9 s.
- **Forecasts:** DAY_SUMMARY §7 misquotes my C forecast and omits my H016 v2 and H017 v2 misses.
- **My own record:** the H015 v2 review missed the NM-missing issue in D3-C2.

**Standing rule 12 (new):** report out-of-range prediction counts, and ranking-month counts of long-delay NM-missing rows. The acknowledgement must contain both hashes, D3-C1 to D3-C9, rule 12, ruling H3 and the command above.

### Verified
- **Hashes:** frozen files, agent definition, `uv.lock`, the E019–E022 gate records and three exchange mirrors all match.
- **Code freeze:** empty diff from `7e9c431` and from `2671dd3`, tests included.
- **Predictions:** all prediction files match their manifests; E019 and E022 are byte-identical on all 8 folds.
- **Tests and lint:** 123/123 pass; ruff clean.
- **Secrets:** no credential value in tracked files or commit messages.
- **Holdout:** Day 3 has 0 of 1 accesses used.
- **Limits observed:** no December target read, `holdout_check.py` not run, no model fitted. I wrote only the review file; scratch scripts stayed outside the repository.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D03-S01-0003
status: COMPLETE
decisions:
  - proposal_id: PHASE_CLOSE_D03
    proposal_sha256: 20dbd9605d7ae864b8a548cd6b4c064da48578d3c236e47861a58db0de189401
    decision: ACCEPT
    review_path: research/day-03/advisor/PHASE_CLOSE_D03_review_v1.md
    review_sha256: 4e104260c6517ad91a426c531da345ac28e88b362960ce202c3fbe49410346d2
completed_utc: 2026-09-30T07:02:34Z
```
