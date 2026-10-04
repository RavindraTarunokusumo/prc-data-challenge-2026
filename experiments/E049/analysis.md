# E049 analysis: H036 v1 (SUBMIT fit of E020's configuration, unrouted LightGBM on FS2; component of E050)

**Outcome: COMPLETE.** 274.9 s, peak RSS 5.39 GB, within CLASS-M; folds SUBMIT_JAN 135.7 s, SUBMIT_JUL 130.9 s; run commit `0f9b2eb`; started 20:57:34Z, finished 21:02:12Z (INC-0016, on the owner's word). Component only; never NEW, never scored.

- **Tree:** `git_dirty_at_run: false`. **Unmasking (U4):** one event, 20:57:44Z, inside the run span.
- **W&B:** sync failed (CommError); not mirrored (INC-0009).
- **Freeze:** `git diff --stat 76e80f1 0f9b2eb -- src scripts config pyproject.toml uv.lock` is empty.
- **Deviation (D7-C14):** the run script stopped after this run, in its checkpoint (the researcher's unbound-variable defect). These records were committed by hand in the checkpoint's path set (`130a211`), and E050 ran under a fixed script (INC-0016). The run's own output is unaffected.
