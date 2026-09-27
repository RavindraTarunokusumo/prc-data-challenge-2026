---
schema: phase-close-proposal-v1
proposal_id: PHASE_CLOSE_D01
proposal_version: 1
day: 1
session: D01-S01
exchange_id: X-D01-S01-0004
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-09-27T13:21:05Z
---

# Day 1 phase close

## Request

1. **Adversarial review** of the Day 1 decisions (brief §10, advisor policy: "try to show that the current champion is wrong"). In particular:
   - the champion **E005 (H004 ridge)**;
   - the **INCONCLUSIVE** decision on E006 (H006 LightGBM), which passes criteria 1–3 but which I did not promote under standing rule 1.
2. **Authorisation of the single Day 1 holdout access** (`splits.yaml: phase_close`): `scripts/holdout_check.py E005 E001`, i.e. phase-closing champion E005 against phase-opening champion E001 (H001). A LOSS reverts the champion to E001.

## Decisions under review

| Step | Experiment | Hypothesis | Decision | Evidence |
|---|---|---|---|---|
| — | E001 | H001 global mean | incumbent | `experiments/E001/analysis.md` |
| 1 | E002 (+ repro E007) | H002 airport median | PROMOTE | `E002_vs_E001.json`, `repro_E007_of_E002.json` |
| 2 | E003 (+ repro E008) | H003 airport × hour median | PROMOTE | `E003_vs_E002.json`, `repro_E008_of_E003.json` |
| 3 | E004 | H005 raw anchor | REJECT (falsified) | `E004_vs_E003.json`, `E004_vs_E002.json` |
| 4 | E005 (+ repro E009) | H004 ridge | **PROMOTE → champion** | `E005_vs_E003.json`, `E005_vs_E004.json`, clip attribution, `repro_E009_of_E005.json` |
| 5 | E006 | H006 LightGBM | **INCONCLUSIVE** | `E006_vs_E005.json`, `E006_vs_E010.json`, `E006_vs_E005_tail_mechanism.json` |
| 6 | E011 | H007 XGBoost | REJECT (falsified) | `E011_vs_E005.json`, `E011_vs_E006.json`, tail mechanism |
| abl. | E010 | H008 | ablation | `E006_vs_E010.json` |

All comparisons are in `research/comparisons/` and all analyses in `experiments/E0xx/analysis.md`.
The ledger is `experiments/ledger.jsonl`, and the journal is `research/EXPERIMENT_JOURNAL.md`.

## Case for the champion E005 (ridge)

- **Criteria.** It passes 1–3 against E003 (mean −65.70 s, all 7 WIN). Its tail share is 0.254 and no row concentrates the change. The reproduction is exact.
- **Against the raw anchor.** It passes against H005 (all WIN). The rows beyond its clip carry 5–40 % of that margin, so the linear combination is the main mechanism.
- **Resources.** CLASS-S, 3.76 GB.

## Case on H006: my reasoning, and where I may be wrong

- **For not promoting.** The margin over ridge is 99 % tail. On the tail rows, the gain comes mainly from rows **without NM data** (0.40–1.04 of the SSE change), not from anchor rows. H006 is also worse than ridge in the S1 bulk (+46 s). Standing rule 1 therefore fails criterion 4, because the pre-registered tail mechanism (the anchor) does not account for the gain.
- **Against my decision:**
  - the competition metric is plain RMSE;
  - the NM-missing tail pattern is P-labelled (the absence of an NM match is known before off-block);
  - it is consistent on all 7 folds;
  - it is large at LIRF: 49 % tail rate among 1,400 unmatched departures, per `E006/analysis.md`.

  Keeping ridge as champion could therefore understate what is achievable.
- **Proposed path.** Pre-register the NM-missing tail mechanism as a Day 2 hypothesis rather than promote retroactively.

## Known weaknesses to attack

1. **Magnitude predictions missed.** Ridge came in at 482.7 against a predicted 400–470; H003 at 0.96 % against 1–3 %; H006's tail share at 0.991 against < 0.5.
2. **Day-scale records.** Two LIRF rows carry targets of about 87,000 s: one with an exact anchor, one with no NM data. Every development fold's RMSE is sensitive to a handful of such records.
3. **Concurrency.** E006 and E009 ran concurrently (runtime inflated; both within class).
4. **Timestamp inconsistency.** The SPLITS v2 ack's timestamp note says the envelope was created at "11:3x Z" (actual 11:34:45Z).

## Resource Estimate

The holdout check reads 165,677 rows once. It takes < 30 s and < 4 GB (CLASS-S).

## Decision Requested From Advisor

ACCEPT (the decisions stand and the holdout access is authorised) | REVISE | REJECT | HOLD
