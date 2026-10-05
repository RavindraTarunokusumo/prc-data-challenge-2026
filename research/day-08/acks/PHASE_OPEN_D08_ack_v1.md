# Acknowledgement: PHASE_OPEN_D08 v1 (exchange X-D08-S01-0001)

*Written 2026-10-05T09:55:18Z (measured with `date -u`).*

- **Proposal:** `research/day-08/proposals/PHASE_OPEN_D08_v1.md`, SHA-256 `6c91822f5a6d5456575f3f65f83b8a4b06a2078e909852aa934dba4db4ee1a3b`.
- **Review:** `research/day-08/advisor/PHASE_OPEN_D08_review_v1.md`, SHA-256 `21b8391f0bc874f704cafe10afaeeea36e7f2ab581d3c63e13745aa9428de1b6`.
- **Decision received: ACCEPT (0.80).** The researcher verified both hashes at 2026-10-05T09:55Z.
- **Mirror:** `orchestration/advisor-exchanges/X-D08-S01-0001/` (`envelope.yaml`, `response.md` verbatim, `checksums.sha256`).

The researcher adopts the following as binding: **G1–G12**, **ruling H8** and **rule 15 as amended (G5)**.

## State after this acknowledgement

- **The `reopened` event is NOT written.** G1 (a)–(d) need the owner's own words and the completed upload line. Until those are committed:
  - the project stays FROZEN in effect;
  - there is no allocation, run, fit or code change.
- **G6:** this cloud session (D08-S01) ends and pushes before any laptop session writes to the task ledger or allocates.

## G5 (rule 15), recorded in full

Every Day 8–12 candidate's analysis reports:

**(a) The look count.**
- Every run from E051 on that has development-fold scores (any purpose), and every Day 8–12 analysis that read validation-month targets. Listed in order, with IDs.
- The candidate's position in that sequence.
- The Days 1–7 baseline is 44 scored experiments.

**(b) The margin against the draw spread.** Per development fold and twin:
- the all-rows ΔRMSE against E046;
- the ΔRMSE on the mechanism population;
- beside both, the spread of E046's draw analogues on the same rows (E033, E034 and E041 off the subgroup; rules 13 and 14).

**(c) The discovery footprint, stated in the proposal.**
- Which months' targets the analyses behind the mechanism read.
- At what granularity: fold or segment aggregates, or row, flight or airport-day level.
- This includes the earlier records the design relies on.

**The consequence (the proposal's review rules on it before allocation).**
- A fold has no confirmatory weight for the mechanism if either holds:
  - the design read that fold's validation-month targets at row, flight or airport-day level;
  - the candidate re-measures a contrast already recorded on the same folds.
- If this leaves S1, or the third WIN of criterion 2, without confirmatory weight:
  - the candidate carries an objection of objection F's type, which H8 makes unresolvable;
  - it ends INCONCLUSIVE and is never uploaded.

Rules 1–14 and batch conditions B1–B4 carry over.

## Ruling H8

- H stays closed for all of Days 8–12; H7 stands.
- Each phase close records "H: closed (H8)".
- `holdout_check.py` is not run.
- SUBMIT fits may unmask December targets for training only, with logged events.

## G3: the challenge pages read on 2026-10-05 (D08-S01, before the review)

All reads were from the allowlisted host `prc-data-challenge-2026.netlify.app`, with HTML stripped to text and filtered with `grep` before display.

| Page | What the researcher saw |
|---|---|
| Index page (`/`) | <ul><li>Overview text: the 10 airports, 2025 learning data, RMSE ranking on January and July 2026.</li><li>The timeline: 1 September to **11 October 2026 23:59:59 CET**.</li><li>The prize amount, the JOAS outreach text, and the site navigation.</li></ul>The navigation shows the menu labels "Leaderboard" and "Ranking" and an alphabetical list of registered **team names** (for example "adventurous-ant"). **No rank, score, ordering by performance, or submission content.** |
| `/data.html` | <ul><li>Dataset description: file list and sizes; ranking and submitting datasets (BLOCK_TIME and TAXITIME blanked for DEP rows); column descriptions.</li><li>The same navigation.</li><li>Its link list (`href`s only) includes `./ranking.html` and `./ranking.html#submission-instructions`.</li></ul> |
| `/rules.html`, `/submission.html`, `/submissions.html`, `/instructions.html` | Requested; the filter printed nothing (no matching content). |
| `/ranking.html` | **Not requested.** It carries the leaderboard. |

The researcher judges that no ranking content was seen, so no incident is recorded.

Under G3, no challenge page is opened again in Days 8–12 by the researcher or by workers.

## Corrections (appended; the proposal is not edited)

- **D8-C2. §3, the bulk.**
  - Non-LIRF bulk RMSE is 149–309 s, not "about 180–310 s".
  - LIRF bulk RMSE is 279–710 s (W1 279 s), not 297–710 s.
  - E046's LIRF bulk is largely its own subgroup's bulk cost: rows predicted at hours, below 3,600 s (rule 12). The increase over E033 is R1 45 %, R2 19 %, R3 16 %, S1 72 % and W1 5 % of E046's LIRF bulk SSE. E033's LIRF bulk was 273–374 s.
- **D8-C3. §3, the tail.**
  - "Many of those are recording conventions" holds for LIRF only. Outside LIRF, 0–16.7 % of tail rows are block-at-schedule, at or below the base rates of 11.1–19.4 % (PHASE_CLOSE_D01 review (c)).
  - LIRF holds 12–68 % of each fold's ≥ 3,600 s rows. In W1 it holds 88 of 763, and LTFM holds 615.
- **D8-C4. §2 (e).**
  - 44 experiments have development-fold scores, not 50. E025 is a RESOURCE_FAILURE; E042–E044, E049 and E050 are SUBMIT fits without fold scores.
  - The folds' reuse also includes target-reading analyses.
- **D8-C5. §3, the heading.** "What this means for the owner's aspiration (plain words, not a prediction)" is withdrawn (G3).
  - The researcher's chat message to the owner at about 2026-10-05T09:34Z, sent before the review, set segment figures beside the 250 s target. It also said the tail is "many ... recording conventions" without D8-C3's LIRF restriction.
  - Both are withdrawn under G3 and D8-C3, and the owner is told so.
- **D8-C6. Clerical.**
  - SESSION_START, INC-0017, INC-0018 and UPLOAD_RECORD carry 09:31:17Z, the session start's measured time, not each file's writing time.
  - PHASE_OPEN_D08 v1's header first carried a pre-written 09:40:00Z, replaced with the measured 09:32:47Z before hashing.
