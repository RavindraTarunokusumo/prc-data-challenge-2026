# Upload record (P7 (d) of X-D07-S01-0003; appended after FROZEN)

*Written 2026-10-04T22:34:22Z (measured).*

- **Uploaded by:** the owner, by hand, using the researcher's `boto3` instructions. The researcher's own attempt was blocked by the permission system (INC-0017).
- **Owner's report (verbatim):** "Alright, done." Received by the researcher at 2026-10-04T22:34:22Z. The owner did not state the exact upload time; it lies between the instructions (about 2026-10-05) and this record.
- **Object:** `prc-2026-genuine-cabbage/genuine-cabbage_v1.parquet` (the first submission; naming per D7-C15).
- **Content:** a byte copy of `predictions/final/E050/submitting.parquet`, SHA-256 `f0dc2c7c40063e238ef57f51d31192008e37c5327afcdc67d563868af17d06e8`. The procedure had the owner recompute the hash before uploading; the researcher did not observe that step.
- **FROZEN commit:** `4c21eff`.
- **External evaluation:** none recorded. The owner has not supplied this team's score.

## Leaderboard information disclosed to the researcher (recorded; not used)

- With the report of the upload, the owner stated: "the No. 1 ranked submission is 214". That is another team's leaderboard figure (RMSE, presumably seconds, on the ranking months).
- It is recorded here as **leaderboard exposure of the researcher's context**. It does not alter any frozen record or decision. Any later work that might be influenced by it is marked as such (INC-0018).

---

*Merge note (2026-10-06, D08-S03): two upload records were written independently. The section above was written on branch `day-7` after FROZEN (commit `8c02282`), on the owner's laptop. The section below was written on branch `day-8` (cloud session D08-S01) without sight of it. Neither is edited; the disagreement between them is recorded in INC-0020.*

# Upload record: E050 (P7 (d) of X-D07-S01-0003; appended after FROZEN)

*Written 2026-10-05T09:31:17Z by the researcher (D08-S01, cloud) from the owner's report. The researcher did not upload, did not access the submission bucket and did not read the leaderboard.*

| Field | Value |
|---|---|
| Uploaded by | the owner |
| What was uploaded | the owner reports "Submission already submitted to the bucket" (D08-S01). The record of the freeze names `predictions/final/E050/submitting.parquet` |
| Expected SHA-256 | `f0dc2c7c40063e238ef57f51d31192008e37c5327afcdc67d563868af17d06e8` (FINAL_SUBMISSION.md) |
| Hash recomputed at upload | **not stated by the owner**; the file is on the owner's laptop and absent from this container, so the researcher cannot verify it |
| Upload time | **not stated**; before 2026-10-05T09:22Z (the owner's message) |
| Object name in the bucket | **not stated**. The owner states the convention `<group_name>_<version_number>.parquet` (INC-0017; correction D8-C1 to FINAL_SUBMISSION.md) |
| FROZEN commit | `4c21eff` (merged into `main` at `88cdb22`) |
| Leaderboard figure | none seen (owner: "No score yet"). Under LEADERBOARD_POLICY, a figure is appended only as an external evaluation and is never fed back |

**Owner action requested (append-only):** add a line below with the upload time (UTC), the object name and the output of `sha256sum predictions/final/E050/submitting.parquet`. Do not add the leaderboard figure during Days 8–12 (PHASE_OPEN_D08).
