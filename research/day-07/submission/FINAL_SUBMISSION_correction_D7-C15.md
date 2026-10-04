# Appended correction D7-C15 (after FROZEN; P7 (c))

*Written 2026-10-04T22:24:41Z. `FINAL_SUBMISSION.md` is not edited.*

- **Wrong statement:** `FINAL_SUBMISSION.md` says "The challenge expects the file named `submitting.parquet` in the team's submission bucket".
- **Correct rule:** the ranking page's submission instructions, read by the owner and pasted to the researcher on 2026-10-05; the researcher did not read the ranking page (P7 (d)). They state:
  - `submitting.parquet` is the template, and `TAXITIME_SEC_mvt` is filled in for each `MVT_ID_mvt`;
  - each team submits to its own bucket under the name `<team-name>_v<incremental integer>.parquet`;
  - each row must match its `MVT_ID_mvt`.
- **For this project:** the first upload is named **`genuine-cabbage_v1.parquet`**. It is a byte-for-byte copy of `predictions/final/E050/submitting.parquet`, so the SHA-256 is unchanged: `f0dc2c7c40063e238ef57f51d31192008e37c5327afcdc67d563868af17d06e8`.
- **Re-checked against those rules (read-only, 2026-10-04T22:24:41Z):**
  - schema `MVT_ID_mvt` Float64 and `TAXITIME_SEC_mvt` Int32, equal to the template's;
  - 344,841 rows, with IDs equal to the ranking dataset's DEP IDs and in the template's row order;
  - no nulls, no duplicates, no ARR IDs.
