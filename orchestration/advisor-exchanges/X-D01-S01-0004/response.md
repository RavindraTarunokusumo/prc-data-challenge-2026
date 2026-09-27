Phase-close review for X-D01-S01-0004 is done. Decision: **ACCEPT** (confidence 0.85). The Day 1 decisions stand, and the one holdout access (E005 vs E001) is authorized once the acknowledgement is committed.

**Hash check:** the proposal's SHA-256 matches the envelope. The frozen files, the 11 ledger hash triples and the three earlier exchange mirrors all verify. Tests pass 90/90 and lint is clean. I read no December targets and did not run `holdout_check.py`. My only write is the review file.

**Champion E005:** I could not find a rule violation. Every criterion re-verifies from the stored predictions. The clip-attribution file has no committed producing code, so I recomputed it independently and got identical values. The strongest case against E005: on rows with NM data (98–99 % of each fold), E006 is 40–57 s better on every development fold.

**H006 INCONCLUSIVE:** the decision is correct, but two parts of the reasoning behind it are wrong and must be corrected in the record.
- **"99 % tail" is a netting artifact.** On rows with NM data, H006 beats ridge in the bulk by 31–40 s on every fold. Its bulk loss on S1 and R1 comes entirely from LIRF rows without NM data, which it predicts at a median of 2,545–3,856 s. DAY_SUMMARY §5 item 3 blames "tree models" in general, which is the wrong cause.
- **The NM-missing tail is not P-labelled.** At LIRF, 90 % of NM-missing tail rows (and 79 % of NM-present tail rows) have a block time within 120 s of the scheduled time. Their target therefore equals `d_sched`, which is label T.
- **This is a LIRF recording convention.** Block time equals schedule in 83 % of LIRF tail rows, against a 24.5 % base rate. At the other nine airports the tail share is at or below their base rate.

**Why Day 1 magnitude predictions missed:** rows without NM data are 0.8–2.1 % of each fold but carry 14–66 % of every model's SSE. The audit's 385 s proxy left these rows out.

**Holdout readiness** (checked without reading targets):
- Both H prediction files cover the 165,677 December rows exactly, with finite values, and no access has been logged yet.
- The command in the proposal is missing the required `--reason` argument; the review gives the exact command.
- The check will almost certainly be a WIN (every development-fold q90 is at or below −67 s), so it can only catch a gross failure.

**Required acknowledgement:** `research/day-01/acks/PHASE_CLOSE_D01_ack_v1.md`. It references both hashes and is committed before the access. It appends corrections C1–C7:
- **C1–C2:** the two H006 corrections above.
- **C3:** the finding on NM-missing rows and the magnitude misses.
- **C4:** there are three day-scale LIRF records, not two.
- **C5:** E006 also overlapped E007 and E008, not only E009; no effect on results.
- **C6:** STATE.md has not been updated since chain step 4.
- **C7:** the clip-attribution code is not committed.

The acknowledgement also adopts two new standing rules:
- **Rule 7:** comparisons are broken down by NM status and by LIRF against the other airports.
- **Rule 8:** a hypothesis states whether its mechanism is taxi duration or the block-at-schedule recording convention.

**Prediction:** WIN 0.97, TIE 0.03, LOSS under 0.01. dRMSE on H is expected between −60 and −125 s.

I did not write `response.md` in the exchange directory; that is your mirroring step.

Files are in /home/user/prc-data-challenge-2026/research:
- day-01/advisor/PHASE_CLOSE_D01_review_v1.md (the review; untracked, not committed)
- day-01/DAY_SUMMARY.md (needs C1–C4)
- STATE.md (stale, C6)
- comparisons/E005_vs_E004_clip_attribution.json (C7)

```yaml
schema: advisor-task-result-v1
exchange_id: X-D01-S01-0004
status: COMPLETE
decisions:
  - proposal_id: PHASE_CLOSE_D01
    proposal_sha256: 811b313c18a93a2f91751e145f961ed1cd8f253c3fda850c058f4872da7ef770
    decision: ACCEPT
    review_path: research/day-01/advisor/PHASE_CLOSE_D01_review_v1.md
    review_sha256: 5082a10e7c9f93b75bb90b1684bdc5b1f73656f709b686f029964267c737c402
completed_utc: 2026-09-27T13:40:28Z
```
