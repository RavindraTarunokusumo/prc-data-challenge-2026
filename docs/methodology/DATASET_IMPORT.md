# Dataset Import Confirmation (preamble)

**Imported:** 2026-09-26T18:29:57Z · **Source:** `s3://prc-2026-datasets` on `s3.opensky-network.org`
**Manifest:** `data/manifests/raw_manifest.json` (SHA-256 `7ca4254268f7328f588205629d7c6783f9bdd06ebba9620c75c4a3d24d6fd2c8`)
**Local path:** `data/raw/prc-2026-datasets/` (git-ignored, 315 MB)

This is a structural integrity check only. Scientific EDA and the
prediction-time availability audit belong to Day 1 (`DATASET_AUDIT.md`).

## Files

14 objects, 0.33 GB, sizes verified against the bucket listing and SHA-256
recorded per file:

- `training_2025-MM-01_….parquet` × 12 (Jan–Dec 2025)
- `ranking.parquet` (Jan + Jul 2026)
- `submitting.parquet` (submission template)

## Checks

| Check | Result |
|---|---|
| Training rows | 4,167,797, which **matches** the data page count exactly |
| `MVT_ID_mvt` unique in training | yes (4,167,797 distinct) |
| Training time span (`MVT_TIME_UTC_mvt`) | 2025-01-01 00:01:04Z → 2025-12-31 23:57:36Z |
| Phase split (training) | DEP 2,085,047 · ARR 2,082,750 |
| Airports | EDDF, EDDM, EGLL, EHAM, LEBL, LEMD, LFPG, LIRF, LSZH, LTFM (10, **matches** the page) |
| Columns | 30, identical schema in training and ranking |
| Ranking rows / months | 689,534 · 2026-01 and 2026-07 only |
| Ranking DEP rows | 344,841. `TAXITIME_SEC_mvt` and `BLOCK_TIME_UTC_mvt` are null for all of them, as documented |
| Submitting template | 344,841 × [`MVT_ID_mvt`, `TAXITIME_SEC_mvt`]. ID set **equals** the ranking DEP IDs |

## Notes for Day 1

- Target: `TAXITIME_SEC_mvt` (= `MVT_TIME_UTC_mvt − BLOCK_TIME_UTC_mvt`) for DEP rows. Metric: RMSE.
- The ranking file blanks only the two DEP columns above. Which of the remaining columns are legitimately usable at prediction time is an **open question for the Day 1 availability audit**. It is not decided here.
- `MVT_ID_mvt` and `FLIGHT_ID_mvt` are stored as Float64. Cast carefully when joining the submission.
- Polars emits a benign `arrow.r.vctrs` extension-type warning, because the files were written from R.

## Re-import

```bash
uv run python scripts/fetch_data.py --pull --bucket prc-2026-datasets
```
