---
schema: incident-v1
incident_id: INC-0020
type: protocol_deviation
created_utc: 2026-10-06T18:56:45Z
status: open
---

# Day 8: the post-freeze Day 7 commits never reached `main`; duplicate incident IDs; contradicting records on leaderboard exposure and the upload

**Raised by:** the researcher at the start of D08-S03 (owner's laptop), on pulling `main` (`35d9bda`).

## What happened

- After FROZEN (`4c21eff`), session D07-S01 appended three commits on branch `day-7`, on the owner's laptop: `28f27e6` (correction D7-C15), `652eff0` (`LICENSE`, GNU GPLv3) and `8c02282` (upload record, two incidents, `HANDOFF_D07.md`, a session-registry line).
- They were pushed to `origin/day-7` but were **not** in PR `day-7` → `main` (merged at `88cdb22`), which ended at `4c21eff`.
- Day 8 was opened from `main` at `88cdb22` by cloud sessions D08-S01 and D08-S02, **without those three commits**. Their records were written without sight of them.
- The owner instructed the merge on 2026-10-06 (D08-S03): "Yes, fix the merge and open the day-8 session". `origin/day-7` is merged into `day-8` in the commit that adds this incident. No file from either lineage is edited. The two conflicting files are resolved by keeping both versions in full (below).

## 1. Duplicate incident IDs

Both lineages allocated INC-0017 and INC-0018 independently. Both sets of files are kept unchanged. From this incident on, records refer to them by the following labels:

| Label | File | Lineage | Subject |
|---|---|---|---|
| **INC-0017 (D7)** | `INC-0017-owner-licence-and-upload-after-freeze.md` | `day-7`, created 2026-10-04T22:26:33Z, closed | GPLv3 licence; the researcher's upload attempt blocked by the permission system |
| **INC-0018 (D7)** | `INC-0018-owner-post-freeze-extension.md` | `day-7`, created 2026-10-04T22:35:39Z, open | owner's extension request; leaderboard figure disclosed to the researcher |
| **INC-0017** | `INC-0017-owner-reopen-after-freeze-D08.md` | `day-8`, created 2026-10-05T09:31:17Z, open | reopening after FROZEN; G1 waiver |
| **INC-0018** | `INC-0018-owner-instruction-sonnet-delegation-D08.md` | `day-8`, created 2026-10-05T09:31:17Z, open | Sonnet delegation |

Unlabelled references in Day 8 records, and in X-D08-S01-0001, mean the `day-8` files. References inside the `day-7` files and `HANDOFF_D07.md` mean the (D7) files. The next free ID is INC-0021.

## 2. Records that contradict each other

| Topic | `day-7` record (2026-10-04, laptop) | `day-8` record (2026-10-05, cloud) |
|---|---|---|
| **Leaderboard exposure** | The owner told the researcher another team's leaderboard figure with the upload report. It is recorded as exposure of the researcher's context, not used (INC-0018 (D7), UPLOAD_RECORD). | "No leaderboard figure has been seen by the owner or the researcher. Leaderboard isolation still holds." (INC-0017 facts; SESSION_START D08-S01; UPLOAD_RECORD's second section) |
| **Uploaded object** | `prc-2026-genuine-cabbage/genuine-cabbage_v1.parquet`, a byte copy of E050's file. The procedure had the owner recompute the hash; the researcher did not observe it. | Object name, upload time and hash "not stated" |
| **File naming** | D7-C15: the file must be named `genuine-cabbage_v1.parquet` | D8-C1: the same disagreement with FINAL_SUBMISSION.md, found again independently |
| **Licence** | `LICENSE` (GPLv3) added for prize eligibility | not mentioned; `main` had no `LICENSE` until this merge |

**Reading.**
- **The `day-7` record is the earlier first-hand record on all four topics, and it governs.** The `day-8` statements were true of what the cloud sessions could see, not of the project.
- **Leaderboard isolation did not hold at the reopening.** A leaderboard figure entered the researcher's context on 2026-10-04, before Day 8 opened. The owner's target of "< 250 s" (INC-0017) was set after that disclosure.
- **The phase-open review X-D08-S01-0001 (ACCEPT) was made on the `day-8` statement** that isolation held and no figure had been seen. Its G2 and G3 already forbid any leaderboard figure or the owner's target as an input, and the G1 waiver already disclosed that isolation "rests on no recorded commitment". The researcher judges that the review's binding conditions are unchanged by this incident, but its factual premise was wrong. **The Advisor is told in the envelope of the next exchange**, which cites this incident, and may rule on it before any allocation.
- **The researcher's context in D08-S03 again holds the figure**, read from the `day-7` records while diagnosing the merge. It is not repeated here and is not used in any proposal, criterion, threshold or decision (G2).
- **G1 (c), the upload line, was already on record** on `origin/day-7` (object name and expected hash; the recomputed hash not observed by the researcher). The owner's waiver of G1 stands; this only corrects the statement that the upload was entirely unrecorded.

## Disclosure (every Day 8–12 record, beside INC-0017's)

The `day-8` records written before this merge stated that no leaderboard figure had been seen. That was wrong: one had been disclosed to the researcher on 2026-10-04 (INC-0018 (D7)). It was not used.

## Resolution

Open. It closes when the Advisor has been told (the next exchange's envelope) and any ruling on it is acknowledged.
