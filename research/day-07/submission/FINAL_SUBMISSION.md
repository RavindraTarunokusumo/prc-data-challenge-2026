# Final submission manifest (P7 (a) of X-D07-S01-0003; DATA_POLICY §3)

Appended at the freeze. It completes the submission records without editing them: `SUBMISSION_RECORD_E050.json` lacks the code commit, creation time and producing command (D7-C12).

| Field | Value |
|---|---|
| File | `predictions/final/E050/submitting.parquet` (git-ignored) |
| SHA-256 | `f0dc2c7c40063e238ef57f51d31192008e37c5327afcdc67d563868af17d06e8` |
| Size | 1,094,599 bytes; 344,841 rows; columns `MVT_ID_mvt` (Float64), `TAXITIME_SEC_mvt` (Int32), in the template's order |
| Producing experiment | E050 (H037 v1): E044 with the LIRF NM-missing subgroup from E049 |
| Producing command | `uv run python scripts/make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050` |
| Code commit of the formatter run | `bb1815bbf60359d1783eca6d71fbc22809a5822a` (HEAD at formatting; clean tree) |
| `scripts/make_submission.py` SHA-256 | `7e6062b60b7fcb716c7014ef02a29e92b99b61f369c023a4e825b89ceaaeb958` (pinned in H035 §Batch) |
| Creation time | 2026-10-04T22:03:56Z (file modification time) |
| Template | `data/raw/prc-2026-datasets/submitting.parquet`, SHA-256 `0d383408ed5ac27bfcfd12d6b961cee77c8a6364b10dad9fe3ec81115c79652b` |
| Source predictions | E050 SUBMIT_JAN / SUBMIT_JUL, E044 and E049 (hashes in `SUBMISSION_RECORD_E050.json`) |
| Selected by | P4 of X-D07-S01-0003: E049/E050 COMPLETE within class; `route_check.py E050 E044 E049` PASS; I1–I5 pass; no P6 flag |
| Not selected | `predictions/final/submitting.parquet` (E044, E033's procedure), SHA-256 `d57ff7db7dfa34e13934aa524464ea13dbe9f5f904fae400a85f87e62c95af73`; kept and recorded |

## The upload (owner only; P7 (d))

- Once, by the owner, after FROZEN, with the file unmodified.
- Immediately before the upload, recompute the hash; it must equal the value above:

  ```bash
  sha256sum predictions/final/E050/submitting.parquet
  ```

- The challenge expects the file named `submitting.parquet` in the team's submission bucket.
- Afterwards, an appended record states the upload time, the hash and the FROZEN commit. The researcher neither uploads nor reads the leaderboard. A figure the owner supplies is appended as an external evaluation only.
- **Before deciding (U6, P6):** the file carries a bet that LIRF's block-at-schedule recording convention persists in 2026. On 383 rows it predicts hours where E044 predicts about 29 min. If the convention holds, this gains; if it does not, the loss is of similar size. December 2025 favoured it (one access); January and July are untested.
