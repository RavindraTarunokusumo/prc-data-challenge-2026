# D07-S01 session start

*Written 2026-10-03 (environment measured 2026-10-03T16:51–16:57Z with `date -u`).*

- **Why a new session:** Day 7 opens (owner: "Begin Day 7. Schedule experiment runs between 21:00 - 22:00"). The Day 6 PR is merged into `main` (`7d4d4df`, 2026-10-03T16:44:57Z). Branch `day-7` is cut from `origin/main` at `7d4d4df`; the tree was clean.
- **State recovered** from `research/STATE.md`, `research/day-06/DAY_SUMMARY.md` (FINAL), the ledgers and the mirrors:
  - **Champion E033** (H023 v3): fixed 0.5/0.5 blend of E029 (routed LightGBM, FS2, `route_train_exclude`) and E031 (routed CatBoost GPU, FS2_RAW, CTRs at complexity 4). Development mean 438.87 s; −5.62 s against E026, 7/7 WIN; holdout H WIN (369.18 against 375.93 s).
  - **Accepted findings (Day 6):** no result contradicts the promotion; the margin holds over three draws (−5.62, −5.54, −5.52 s, 7/7 WIN each); the CatBoost half's advantage is scoped to "this CatBoost configuration as a whole" (no necessity claim).
  - **Rejected or not shown:** E031 alone, other weights, draw averages (rule 10; new proposals only); the SUBMIT procedure and D3-C3's January exposure untested.
  - **Standing disclosures on E033:** D3-C1, D3-C3 (restated D5-C16), D5-C8, D5-C9 (updated D6-C11), D5-C10, the 1,000-iteration budget, the Day 6 attribution.
  - **Standing rules** 1–14; rulings H, B, R, H3, H4, H5, H6; rule L v2; hand-off base ruling.
- **Remaining budget:** Day 7 holdout access 1 of 1 (needs a Day 7 allocation as NEW, named by the phase close). Next experiment id **E042**. Last exchange **X-D06-S01-0004**; none pending.
- **Freeze:** `gate.py status`: frozen `32c41c0f9331` OK, advisor definition `30fff5dd3c54` OK.
- **Environment (rule L v2 item 6):**
  - CPython 3.13.15; polars thread pool 16; no `*_THREADS` variables set;
  - numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, polars 1.44.2, LightGBM 4.7.0, CatBoost 1.2.10, XGBoost 3.4.1, pandas 3.0.6; `uv.lock` `efa4fd78eaa6`;
  - RAM 10,951 MiB, swap 4 GiB unused (INC-0010); RTX 5060 Laptop 8,151 MiB, **2,864–2,883 MiB in use at idle** by a process outside WSL (not listed by `nvidia-smi` here); boot `cf2c705b…` (unchanged).

  **This matches item 6.** The GPU's external use is higher than Day 6's 635 MiB; E031's configuration takes `gpu_ram_part: 0.4` (about 3.2 GB), so about 6.1 GB would be in use. Re-measured at arming.
- **Owner instruction:** runs only 21:00–22:00 CEST (19:00–20:00Z). Recorded as **INC-0014**.
- **Open incidents:** INC-0004, INC-0009, INC-0010, INC-0014.
- **Resolved model ID:** researcher `claude-opus-5-5` (`--effort high`); Advisor `advisor` subagent, definition `30fff5dd3c54`.
- **Facts checked before the proposal (target-free, no model run):**
  - `submitting.parquet` (SHA-256 matches the raw manifest) has 344,841 rows, `MVT_ID_mvt` Float64 (integer-valued, unique) and `TAXITIME_SEC_mvt` **Int32** (all null). Its ID set equals silver's DEP rows of 2026-01 (152,719) and 2026-07 (192,122) exactly.
  - The challenge's data page (allowlisted host) states the file is Parquet, named `submitting.parquet`, with those two columns, for ranking DEP rows only.
  - Training-target minimum is −12 s, so a floor at 0 s is not weakly dominant; E033 has 159 predictions below 0 s over its 8 folds.
- **Day 7 theme (brief §3):** final synthesis, submission, freeze.
- **First planned action:** a batched proposal set (H031–H033) for the SUBMIT fits of E033's construction (E029's and E031's configurations on `SUBMIT_JAN`/`SUBMIT_JUL`, then the 0.5/0.5 blend), with the target-free formatter `scripts/make_submission.py` (tested); review X-D07-S01-0001; allocate E042–E044; commit; arm the launcher for 21:00.
