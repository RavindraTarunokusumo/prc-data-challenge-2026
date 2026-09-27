# Acknowledgement — PHASE_CLOSE_D01 v1 (exchange X-D01-S01-0004)

- proposal: `research/day-01/proposals/PHASE_CLOSE_D01_v1.md`, sha256 `811b313c18a93a2f91751e145f961ed1cd8f253c3fda850c058f4872da7ef770`
- review: `research/day-01/advisor/PHASE_CLOSE_D01_review_v1.md`, sha256 `5082a10e7c9f93b75bb90b1684bdc5b1f73656f709b686f029964267c737c402`
- decision received: **ACCEPT** (confidence 0.85). Both hashes were verified by the researcher.
- acknowledged: 2026-09-27T13:42:27Z, committed **before** the holdout access

Authorized: the single Day 1 holdout access, exactly
`uv run python scripts/holdout_check.py E005 E001 --reason "Day 1 phase close (X-D01-S01-0004): phase-closing champion E005 vs phase-opening champion E001"`.
The Day 1 decisions stand. The champion is E005, and H006 remains INCONCLUSIVE.

## Record corrections (appended; earlier records are not edited)

- **C1. Tail-share netting.**
  - E006's 0.991 tail share against E005 nets three pieces:
    - a bulk **gain** on NM-present rows (−31 to −40 s on every development fold);
    - a bulk **loss** on LIRF NM-missing rows (pooled LIRF bulk +210.9 s; the other nine airports −14.5 to −57.8 s);
    - the tail gain.
  - "H006 is worse than ridge in the bulk on S1/R1" holds only because of LIRF NM-missing rows. DAY_SUMMARY's "tree models are worse in the bulk" misdiagnosed the cause.
  - On NM-present rows (98–99 % of each fold), E006 beats E005 by 40–57 s on every development fold.
- **C2. The NM-missing tail mechanism is label T, not P.**
  - It runs through `d_sched`, and it is predominantly LIRF's **block-at-schedule recording convention**.
  - Researcher verification (Jan–Nov, no December): at LIRF, block time is within 120 s of the scheduled time in **83.3 %** of tail rows (y ≥ 3,600 s), against a base rate of 25.7 %. The rates are 90.1 % for NM-missing tail rows and 79.3 % for NM-present tail rows.
  - At the other nine airports the in-tail rate is at or below the base rate.
  - The "P-labelled" claim in PHASE_CLOSE_D01_v1 is withdrawn.
- **C3. NM-missing rows carry the metric.**
  - They are 0.77–2.06 % of rows but carry 0.14–0.66 of the SSE of E004, E005 and E006, which explains the magnitude misses.
  - E005's RMSE on NM-present rows is 289 / 288 / 271 / 395 / 307 s (R1, R2, R3, S1, W1). The audit's 385 s proxy RMSE covered NM-present rows only.
- **C4. Day-scale records.** The review lists three LIRF records: 87,002 s (anchor-exact), 87,186 s (no NM data) and 131,167 s (no NM data). **Researcher amendment: that is still an undercount.**
  - Jan–Nov contains **15** DEP rows with targets ≥ 80,000 s: 13 at LIRF, 1 at LFPG and 1 at LSZH.
  - 14 of the 15 have no NM data. **5 fall in July 2025** (S1 and S1c validation).
  - Only 2 of the 15 have block time at schedule, so the day-scale records are mostly a separate phenomenon from the block-at-schedule convention.
  - The three records above are those that surfaced as dominant rows.
- **C5. Concurrency.** E006 overlapped E007, E008 and E009 and several comparison runs, not only E009. The reproductions are exact and every run was within class, so there is no numerical effect.
- **C6. STATE.md was stale** since chain step 4 (commit `917a03f` skipped §13 step 3). It is updated in this commit.
- **C7. Clip-attribution code.** Now committed as `scripts/clip_attribution.py`. Re-running it reproduces `research/comparisons/E005_vs_E004_clip_attribution.json` **byte-identically** (sha256 `0574ca27…`).

## Standing rules adopted (from the next proposal onward)

- **Rule 7, subgroup disclosure.** Every promotion or criterion-4 comparison reports SSE-change shares and bulk dRMSE by NM status × (LIRF against the other nine airports), per development fold and twin. Where subgroup and pooled bulk signs differ, the tail share is not read alone.
- **Rule 8, recording-convention disclosure.**
  - A hypothesis whose margin concentrates on LIRF tail rows or NM-missing rows states whether its mechanism is taxi duration or the block-at-schedule convention.
  - It labels `d_sched`-derived inputs T.
  - It pre-registers separate tail and bulk expectations for that subpopulation, plus an S1 expectation.
  - The convention is admissible, but it is not evidence about taxi-out dynamics and is outside the causal-only variant.
