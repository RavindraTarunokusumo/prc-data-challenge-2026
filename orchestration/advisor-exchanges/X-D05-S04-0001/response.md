All four decisions are **REVISE**, so nothing in this batch can run yet. The main reason: as written, the chain would mark its own runs INVALID. Each proposal's hash matches the envelope, and I wrote only in `research/day-05/advisor/`.

**Decisive finding: on the laptop, the E028 route check cannot pass.**
- E027 and E029 give identical predictions on every routed row (the LIRF rows without an NM match), on all 8 folds. Both differ from E028 on every one of those rows: by up to 190.9 s on R3, 63.3 s on W1 and 60.1 s on S1.
- On the cloud the same check gave 0.0 on every fold.
- The ridge is scikit-learn's `sparse_cg`, stopped at tolerance 1e-4, so small numerical differences between the two code paths move single predictions a lot. The cause is not established.
- So `route_check.py <X> - E028` at 1e-6 s will almost surely make H021 and H022 INVALID, and makes H023 INVALID with certainty, because its routed rows are half E029's.
- For H021 and H022 the stated consequence is also mis-scoped: clause 1's population contains no LIRF rows, so routed rows cannot move it.

**What holds:**
- Per-airport RMSE of E027 against E019, and of E029 against E023, is exactly equal at all nine non-LIRF airports on every scored fold. Only LIRF differs.
- I ran the frozen `compare(E029, E027)` from the scratchpad: it reproduces the committed E023-vs-E019 comparison to 1e-4 s on every fold, the mean, q95 and every outcome.
- So E027 and E029 work as instances of E019 and E023. Rule L items 2, 3 and 5 are acceptable.
- I checked on a synthetic GPU fit that `FloatTargetMeanValue` averages the raw target (predictions 6.9 / 50.3 / 500.0 against means 5 / 50 / 500). A `Borders` CTR (CatBoost's one-border share statistic) cannot separate those levels (117.9 for all three). H021's mechanism statement is correct.

**Record problems for the owner and researcher** (corrections D5-C1 to D5-C6 in the LAPTOP_REFS review):
- **Swap.** The VM has had 4 GiB of swap since boot `cf2c705b` at 16:33:25Z (`.wslconfig` changed at 16:30:17Z). It was never used. STATE.md, the D05-S04 session record, the E026 analysis and the envelope all say "swap 0". This needs an incident and an owner decision.
- **Python version.** The laptop runs CPython 3.13.15, so the same lock gives numpy 2.5.3, scipy 1.18.1 and xgboost 3.4.1. The cloud ran 3.11.15 with 2.4.6, 1.17.1 and 3.2.0. The brief says Python 3.11, and the lock hash also differs. "Same uv.lock, different CPU" is wrong.
- **Run authorization.** E027, E028 and E029 ran without authorization from their reviews' scope. E029 is contrary to H018 v2 review item 9; `gate.py` does not enforce reproduction scope. E026 is byte-identical to E027 and covered by the hand-off, so it can serve as E019's instance without ratification.
- **E029 code commit.** E029's manifest names `ed5151f`, which was committed during its run; its run commit was `f89dc60`. The predictions are from `f89dc60`'s code.
- **Attribution.** The E026 analysis and journal blame LightGBM on the AMD CPU; the evidence puts the difference in the ridge's routed rows. E028 against E005 is not "low-order bits": W1c differs by 0.339 s.

**Other required changes:**
- **H021:**
  - Name a source for the resolved `get_all_params()`; nothing in the run records it.
  - Correct the calibration table: the `gpu_ram_part` 0.4 row used default CTRs. H021's exact configuration was never calibrated.
  - Re-estimate RAM from the worker path: E029 used 6.60 GB, so expect about 7–8 GB against the 8 GB CLASS-M target, which H023's criterion 7 inherits.
  - Define clause 1's WIN count (precedent is the twin-rule `fold_outcome_counted`).
  - Pre-register that a GPU memory failure is recorded as RESOURCE_FAILURE. The runner would record it as INVALID.
- **H022:** the same parameter-source and RAM fixes. Its class wording is wrong, its calibration figure was measured on FS2, and its mechanism text should state the 254-border binning of the codes.
- **H023:**
  - Evaluate B3 against E027, not E028.
  - Pre-register how the CatBoost half's re-draw noise enters clause 1.
  - State that only run status, never H021's or H022's accuracy, gates H023 and its reproduction.
  - Either narrow the "same keys used differently" claim, or pre-register the equal-weight blend of E029 and H022 as the control.

My forecasts for v2 runs: H021's mechanism clause not met (CTRs help by at least 3 s) P 0.60. H023's complementarity clause not met P 0.35. H023's S1 fold against E027 is a WIN with P 0.07 and a LOSS with P 0.25. H023 promotion P 0.04.

Files are in `/home/rvindra/Projects/prc-data-challenge-2026/research/day-05/advisor/`:
- LAPTOP_REFS_review_v1.md
- H021_review_v1.md
- H022_review_v1.md
- H023_review_v1.md

```yaml
schema: advisor-task-result-v1
exchange_id: X-D05-S04-0001
status: COMPLETE
decisions:
  - proposal_id: LAPTOP_REFS
    proposal_sha256: e6d76c9c1729cdde8fa3cec9012052bc42b0866ac0306eee25888552bfcfbb94
    decision: REVISE
    review_path: research/day-05/advisor/LAPTOP_REFS_review_v1.md
    review_sha256: 7d505b6ed857d0e5044210d534427c6eb4c21ebcbee1e4a5bae60d28e70e38c2
  - proposal_id: H021
    proposal_sha256: a46c916ae3e363ff963a8074111a4c67dee126a43acfdc7c8c26259a5e5d13c7
    decision: REVISE
    review_path: research/day-05/advisor/H021_review_v1.md
    review_sha256: 26665aa7dda73f37dbf553592e2193dd8f8de44e39e2eda90d503de877b1a268
  - proposal_id: H022
    proposal_sha256: 043f9625010775991ac5a558073867a83dad45696faa8d1fcdf2fb89bfd22121
    decision: REVISE
    review_path: research/day-05/advisor/H022_review_v1.md
    review_sha256: befbbf633f42abad1bf8420e96c6c54b2fd3e2f2668565effa68c335252eeb9c
  - proposal_id: H023
    proposal_sha256: 2e79f8b1f18bc4039428aded8a0e847742ec04d41dbc738a99c7439fc7beccb8
    decision: REVISE
    review_path: research/day-05/advisor/H023_review_v1.md
    review_sha256: 42b0e77589db74737d64128e8344c1c51279aa3200cdc9b1ba57dc60d7d92e97
completed_utc: 2026-10-01T19:28:22Z
```
