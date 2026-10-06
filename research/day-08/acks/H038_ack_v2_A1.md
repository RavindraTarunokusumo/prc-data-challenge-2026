# Acknowledgement: H038 v2, scope amendment A1 (exchange X-D08-S03-0003)

*Written 2026-10-06T22:50:11Z (measured with `date -u`).*

- **Request:** `research/day-08/proposals/H038_v2_scope_A1.md`, SHA-256 `a3cc9bc7139dedd24ba00c3bf9719fb99b6efcec16c65f72f9caae960ef02a66`.
- **Review:** `research/day-08/advisor/H038_review_v2_A1.md`, SHA-256 `542fb59b8da7ec88e826af4d8e14efabd1586d3b53ff197b2b52e99dbf3c1d6f`.
- **Decision received: ACCEPT (0.85).** Both hashes verified at 2026-10-06T22:49Z.
- **Mirror:** `orchestration/advisor-exchanges/X-D08-S03-0003/`.

## The two config diffs (nothing else changed)

```diff
--- a/experiments/E051/config.yaml
+++ b/experiments/E051/config.yaml
@@ -35,5 +35,6 @@ folds:
 - W1
 - S1c
 - W1c
+- H
 seed: 42
 job_class: CLASS-M
--- a/experiments/E052/config.yaml
+++ b/experiments/E052/config.yaml
@@ -35,5 +35,6 @@ folds:
 - W1
 - S1c
 - W1c
+- H
 seed: 43
 job_class: CLASS-M
```

`gate.json` (still citing v2), the ledgers, the launcher (`54ee5ab8…`) and the frozen files are unchanged.

## The two scope lines of ack v2, restated

- **Configs:** as ack v2, with folds R1, R2, R3, S1, W1, S1c, W1c **and H (predicted only; never scored)**.
- **Not authorized:** in place of "any H fold": **any H score**; **any December target read by any path**, including direct silver reads; holdout_check or holdout_compare on any experiment (H8); **any analysis of E051/E052's H predictions beyond the mixture check's record**; and any other change, fold, rerun or experiment.

## Re-arm rule (binding)

- Same arguments only: START 2026-10-06T22:40:51Z, END 2026-10-07T00:40:51Z.
- **Re-arm only by 2026-10-07T00:12:51Z** (END − 2 × 840 s). After that, nothing is re-armed and both runs wait for a new owner window.
- A mixture-check FAIL on any fold, H included, makes the run INVALID.
- The phase close repeats the H8 check: no `holdout_access` line in the task ledger after 2026-10-04T17:57:38Z.

## Correction D8-C13 (appended)

- **(i)** H038 v1 and v2 say "No H fold (ruling H8)" and "E046 has no H dependency here". X-D08-S03-0002 repeated "no H fold (H8)" and "Not authorized: any H fold". H8 closes H **access**; the runner requires H **prediction** (`check_config`, SPLITS v2 review). Under A1, E051's H fold depends on E046's H file.
- **(ii)** A1's "No H read follows" leaves out `compare.py`, `range_check.py` and `reproduce_check.py`. All three are fixed to R1–W1c and read truth only through `truth_frame`, so the claim holds.
