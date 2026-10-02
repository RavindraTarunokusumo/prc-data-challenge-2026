# E025 analysis: H015 v2 reproduction (Day 5 laptop compute check): RESOURCE_FAILURE

**Status: RESOURCE_FAILURE, not retried (brief §4).** A new reproduction id replaces it. No decision on any hypothesis depends on E025.

| Item | Value |
|---|---|
| Allocation | `gate.py allocate H015 v2 --purpose reproduction`, 2026-10-01T16:16:51Z, committed `590ebd8` |
| Config | identical to E022 (E019's configuration, seed 43, `num_threads: 4`, 8 folds) |
| Run | started 16:16:57Z on the owner's laptop (WSL2, 11 GB, swap 0), clean tree at `590ebd8` |
| Completed folds | **R1: RMSE 446.40 in 123.67 s**. E019 R1 is 446.40 (within the 1.0 s rule). `predictions/validation/E025/R1.parquet` SHA-256 `341715523a27…`, **not** E019's `32eb274461a3…` |
| Failure | 16:19:23Z: global OOM in the WSL VM; the kernel killed the E025 worker (anon-rss 4.14 GiB). The runner died too and wrote no record; `resource-usage.json` and the ledger row were reconstructed from the kernel log (fields `recorded_by`, `evidence`) |
| Cause | The researcher started `pytest` (feature tests including real-silver fixtures, 3.46 GB) while E025 ran. Together with the owner's other laptop processes in the same VM, memory ran out. **E025 was within its 11 GB guard.** See INC-0008 |

**R1 reading (one fold, no claim).** The RMSE matches E019 to 0.01 s, but the prediction file's hash differs. Hand-off §5 allowed for this on a different CPU architecture or build (Intel Xeon on the cloud, AMD Ryzen here). E019's prediction files are not on the laptop, so values could not be compared row by row. The replacing reproduction decides by the 1.0 s rule.
