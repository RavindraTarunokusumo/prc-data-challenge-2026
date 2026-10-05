---
schema: governance-request-v1
request_id: PHASE_OPEN_D08
proposal_version: 1
day: 8
session: D08-S01
exchange_id: X-D08-S01-0001
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-10-05T09:32:47Z
---

# Request PHASE_OPEN_D08 v1: reopen the project after FROZEN for Days 8–12

This is a governance request, not a hypothesis. It asks the Advisor to rule on whether, and under what conditions, research may resume after the Day 7 freeze. Nothing is allocated, run or changed before this request is ACCEPTED and acknowledged.

## 1. Why this request exists

- The owner reopened the project after FROZEN (INC-0017, verbatim instructions there): "New research phase. We have 5 more days to bump our scores to AT LEAST < 250 s".
- P7 (c) of X-D07-S01-0003 allows only appended records after FROZEN. The brief (v3.0 §3) defines no Day 8. Reopening is a protocol deviation on the owner's decision, and it needs rules that the Day 7 freeze did not foresee.
- E050's file has been uploaded (owner's report; `research/day-07/submission/UPLOAD_RECORD.md`). **No leaderboard figure has been seen** by the owner or the researcher.
- The challenge closes 2026-10-11 23:59:59 CET. The owner states that the challenge accepts up to 5 submissions a day, named `<group_name>_<version_number>.parquet`, with no overwrite. Which submission counts towards the ranking is unknown.

## 2. Requested rulings

### (a) Reopening

The state moves from FROZEN to **OPEN (Days 8–12)** at the commit of this request's acknowledgement, with a task-ledger event `{"event": "reopened", "basis": "INC-0017; X-D08-S01-0001"}`. Days 8–12 are research phases (brief §3). Each closes with a `DAY_SUMMARY.md` and a phase-close review, and a phase may end early. **The last phase close must be committed by 2026-10-11T12:00:00Z** to leave the owner time to upload. Days 8–12 may be fewer than five phases.

### (b) The owner's target is not a criterion

- "< 250 s" is the leaderboard RMSE, which no one in the run reads. It is recorded as the owner's aspiration (INC-0017) and **is not a promotion criterion, a stopping rule or a mapping from any development figure.**
- Proposals may cite it only as motivation. A proposal's pre-registered prediction is stated on the development folds, as before.
- **No figure may be presented as "the expected leaderboard score".** S9 and U6 (Day 7) carry over.

### (c) Leaderboard isolation for Days 8–12

- The researcher never reads the leaderboard or the submission bucket.
- **The owner neither reads E050's leaderboard figure nor relays it until the final refreeze's commit** (owner commitment requested in the acknowledgement). If the owner reads or relays it earlier, the researcher records an incident and the Advisor rules on whether any later promotion stands.
- **No intermediate upload.** Five uploads a day are a test-set query budget. Using more than the final one to choose between candidates would be leaderboard-guided selection. **Exactly one new file is uploaded, by the owner, after the refreeze,** under the owner's naming convention. Its hash is recorded before upload, as P7 (d).
- **Question for the Advisor (ranking rule unknown):** if the challenge ranks a team by its best submission, uploading a hedge (for example E044's file next to E050's, or next to a Day 8–12 file) gains without anyone reading a figure. It is still selection on the test set, made by the organiser's rule instead of by us. The researcher proposes that **no hedge is uploaded unless the Advisor rules it admissible**, and then only with the ranking rule confirmed from the challenge page by the owner, not by the researcher.

### (d) Holdout

- **Ruling H7 called the Day 7 access "the project's last H read".** H has been read four times (Days 1, 3, 5, 7), each time by a phase-closing comparison.
- The researcher proposes that **H stays closed for Days 8–12 by default.** Promotion is decided on the development folds under criteria 1–8, with the standing rules.
- The Advisor may instead grant **at most one H access in total for Days 8–12,** at the last phase close and named by that review (rules 3 and 9). The access would be recorded as the fifth read, with an explicit adaptive-reuse disclosure. The researcher does not request it.

### (e) The development folds are heavily reused

- Fifty experiments have been scored on the same seven folds. A five-phase push raises the risk of fitting the folds.
- The researcher proposes **one additional disclosure (rule 15, disclosure only):** every Day 8–12 candidate reports how many Day 8–12 candidates were scored before it, and its margin against the reference's draw spread on the same folds (rule 13 for E046's non-deterministic CatBoost half).
- Batch conditions B1–B4 carry over.

### (f) Champion, references and compute

- **Phase-opening champion: E046** (H035 v1). Promotion is judged against E046's stored laptop predictions (rule R, matched references where a candidate shares a component's training procedure).
- **Compute runs on the owner's laptop** (INC-0017) under rule L v2 item 6, which the Day 7 environment met. A change of environment needs a new ruling, as before.
- **This cloud session (D08-S01) does governance and text work only.** Its `runtime/ledger.sqlite` is a Day 4 copy (`gate.py status`: 24 allocated). No `gate.py allocate`, no run and no holdout script may be executed here. The next experiment ID is **E051**, issued on the laptop.
- Run windows, if any, are owner instructions recorded as incidents, as INC-0012 and INC-0014.

### (g) Refreeze

The last phase close defines the final state exactly as P7 did:
- STATE with **Phase: FROZEN**, the champion, the final file's path and SHA-256;
- a `frozen` event;
- `FINAL_REPORT.md`, with a Day 8–12 section appended (not rewritten);
- the final `DAY_SUMMARY.md`.

The final file is selected by a rule pre-registered at that phase close (as P4), never by an external figure. If no candidate is promoted in Days 8–12, **no new file is uploaded**, and E050's upload stands as the submission.

### (h) Delegation

`claude-sonnet-5-5` workers are permitted under INC-0018, within the INC-0013 boundary.

## 3. Where the remaining error is (development folds, recorded metrics only)

This comes from `experiments/E046/metrics.json`: E046's per-fold scores, by segment. SSE share is the segment's share of the fold's squared error. No new computation on targets was made.

| Fold | All rows RMSE | Rows ≥ 3,600 s: share of rows / of SSE | LIRF share of SSE | Wake `UNK` (NM-missing proxy): rows / SSE | Bulk RMSE, worst airport |
|---|---|---|---|---|---|
| R1 (Sep) | 274.3 | 0.17 % / 30 % | 44 % | 1.3 % / 33 % | LIRF 426 |
| R2 (Oct) | 238.3 | 0.17 % / 20 % | 30 % | 1.0 % / 13 % | LIRF 346 |
| R3 (Nov) | 294.4 | 0.14 % / 53 % | 55 % | 0.8 % / 51 % | LFPG 252 |
| S1 (Jul) | 414.4 | 0.34 % / 50 % | 67 % | 2.1 % / 41 % | LIRF 710 |
| W1 (Feb) | 350.6 | 0.53 % / 65 % | 42 % | 0.8 % / 55 % | LTFM 309 |

**What this means for the owner's aspiration (plain words, not a prediction):**
- On the bulk of rows, the champion is already at about 180–310 s by airport, except LIRF (bulk 297–710 s by fold).
- The all-rows figure is dominated by a fraction of a percent of rows, mostly NM-missing rows and taxi-out values over an hour. Many of those are recording conventions (block-at-schedule at LIRF: STATE "Key data facts"), not taxiing.
- A large all-rows gain can come only from that tail. That is also where U6's forward risk lies: the convention rate in 2026 is unobservable.
- The ranking months are not like the folds: January 2026's schedule delays are heavier than any 2025 winter month (D7 SUBMIT sanity), and S1, the July analogue, is the worst fold.

## 4. Research agenda (non-binding; each item needs its own H proposal)

Ordered by the share of squared error each could address.

1. **Recording conventions beyond LIRF's routed subgroup.**
   - Characterise, target-free first and then on the folds, the non-LIRF NM-missing rows (wake `UNK`) and the ≥ 3,600 s band. Which share are block-at-schedule (or another computable anchor), by airport and month?
   - Where the takeoff time and a candidate anchor are both known at prediction time, an explicit mixture *p·(takeoff − anchor) + (1 − p)·normal* is the squared-loss-optimal form. *p* comes from a target-free or fold-local classifier.
   - Known hazards: `d_sched` and `MVT − AOBT_3` are T-labelled; the D3-C3 January exposure (435 rows over 3 h); rule 8 and rule 12 disclosures.
2. **The routed LIRF subgroup itself** (E046's U6 bet): only a mechanism that lowers the downside, not a re-adjudication of E046 (rule 10).
3. **LTFM winter (W1 bulk 309 s; LTFM is 34 % of W1's SSE).** A weather or de-icing signal is not in the competition data, and external data needs an owner decision and an allowlisted host. First, a target-free check of what the competition data shows.
4. **CatBoost's 1,000-iteration budget** (still improving: −0.73 s over iterations 800–1,000). A new configuration, so a new proposal; small expected gain.
5. Neural models: not planned, since the expected gain is small against the tail.

## 5. Corrections

- **D8-C1:** `FINAL_SUBMISSION.md` states "the challenge expects the file named `submitting.parquet` in the team's submission bucket". The owner states `<group_name>_<version_number>.parquet` (INC-0017). Neither is verified by the researcher, because the page carries the leaderboard. Appended, not rewritten.

## 6. Decision requested from the Advisor

ACCEPT (with any conditions), REVISE or REJECT on (a)–(h). Specifically:
- (c): the question on hedge uploads;
- (d): H closed or one final access;
- (e): whether rule 15 is adopted.

The Advisor may also rule that reopening is not admissible under the research question (brief §1). The owner's decision would then be recorded as a deviation that the final report must carry.
