---
schema: incident-v1
incident_id: INC-0017
type: protocol_deviation
created_utc: 2026-10-05T09:31:17Z
status: open
---

# Day 8: owner reopens the project after FROZEN, for Days 8–12

**Raised by:** the researcher, recording owner instructions in D08-S01 (cloud session). The brief (v3.0 §3) defines Days 1–7 only. P7 (c) of X-D07-S01-0003 allows only appended records after FROZEN: no allocation, run, fit, holdout read, formatter run or code change. Reopening is therefore a protocol deviation, made on the owner's decision (brief §1: the owner may start, stop or recover the run). This incident records it.

## Instructions (owner, D08-S01, verbatim)

> Submission already submitted to the bucket. Please begin Day 8. Same as before if you need to spawn Sonnet or Max subagents.

The researcher asked what Day 8 should be (post-freeze records only, a new research phase, or a retrospective). The owner answered:

> New research phase. We have 5 more days to bump our scores to AT LEAST < 250 s

Asked whether a leaderboard score had been seen: **"No score yet".**

Asked where Day 8–12 compute runs (the champion's CatBoost half is GPU-trained, and the cloud container is CPU-only and holds stored predictions only up to E024): **"Your laptop, as on Days 5–7".**

Asked about resubmission (the researcher did not open the challenge's ranking page, because it carries the leaderboard):

> Max 5 submissions per day, naming convention is <group_name>_<version_number>.parquet, nothing is overwritten.

## Facts at the instruction

- **E050's file was uploaded by the owner** (owner's report). Upload time, object name and the hash recomputed at upload were not stated. See `research/day-07/submission/UPLOAD_RECORD.md`.
- **No leaderboard figure has been seen by the owner or the researcher.** Leaderboard isolation still holds.
- **The challenge closes 2026-10-11 23:59:59 CET** (challenge index page, allowlisted host `prc-data-challenge-2026.netlify.app`, read 2026-10-05). "5 more days" fits that deadline.
- The challenge's submission rules as stated by the owner (5 a day, `<group_name>_<version_number>.parquet`, no overwrite) are not verified by the researcher. The page that holds them also holds the leaderboard. **Correction D8-C1:** `FINAL_SUBMISSION.md` said "the challenge expects the file named `submitting.parquet`", which disagrees with the owner's statement. Which file counts towards the ranking when there are several (latest, best or a designated one) is **unknown**.

## Reading

- **The owner's target (< 250 s) is an aspiration on the leaderboard metric, which no one in the run may read.** It is recorded here, and it does not become a promotion criterion, a stopping rule or a mapping from any development figure (brief §1: "no leaderboard-guided optimisation").
- **Days 8–12 are research phases** (brief §3: a day is a phase, not a wall-clock day) that end before the challenge deadline. Their governance is the phase-open request `research/day-08/proposals/PHASE_OPEN_D08_v1.md`, reviewed by the Advisor (X-D08-S01-0001). **The project stays FROZEN in effect until that review is ACCEPTED and acknowledged:** no allocation, run or code change before then.
- **Compute:** the owner's laptop under rule L v2 item 6, as in Days 5–7. This cloud session (D08-S01) does governance and text work only. This container's `runtime/ledger.sqlite` is a Day 4 copy (`gate.py status`: 24 allocated), so **no `gate.py allocate` may run here**: it would reissue E025 onward.
- **Delegation** to `claude-sonnet-5-5` workers ("Sonnet subagents") is recorded separately as INC-0018. "Max subagents" is read as the fixed `advisor` subagent (Opus, effort max), which is unchanged.

## Resolution

Open. Closes at the last Day 8–12 phase close (the refreeze), with the final upload record.

## Amendment (2026-10-05T09:56:49Z): G1 (d), the owner's words (X-D08-S01-0001)

The researcher listed G1's four items: commitments, what was known at reopening, the upload line, and the "submit once" deviation. The owner answered (D08-S01, verbatim):

> I'll do the first two later, the last one should be the best score that counts.

**Reading:**
- **G1 (d) is recorded:** going beyond the leaderboard policy's "submit once" is the owner's decision. The owner's stated reason is that the challenge counts a team's best score.
- **The owner's statement of the ranking rule ("best score counts") is recorded as the owner's statement, not verified.**
  - Under G2, no proposal, phase close or final-file rule may cite it as a motivation or an input.
  - G7's final-file rule is unchanged: at most one new upload, the latest Day 8–12 champion's checked SUBMIT file; otherwise "no new upload; E050 stands"; no hedge.
  - Under a "best" rule, the external evaluation discloses that the ranked figure may be the better of two files (G2).
- **G1 (a) and (b) are pending** ("later"). The owner's G1 (b) statement should say where the ranking rule was read.
- **G1 (c), the upload line, is still missing.**
- **The  event stays unwritten.**

Appended by the cloud session D08-S01 after its session-end line (records only; no laptop session had started).
