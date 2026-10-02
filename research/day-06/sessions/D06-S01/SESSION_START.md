# D06-S01 session start

*Written 2026-10-02 (environment measured 2026-10-02T17:15–17:19Z with `date -u`).*

- **Why a new session:** Day 6 opens (owner: "Begin Day 6. Schedule experiment runs (both GPU and CPU) between 21:00 - 21:30."). The Day 5 PR is merged into `main` (`4ad18a1`). Branch `day-6` is cut from `origin/main` at `4ad18a1`; the tree is clean.
- **State recovered** from `research/STATE.md`, `research/day-05/DAY_SUMMARY.md` (FINAL), the ledgers and the mirrors:
  - **Champion E033** (H023 v3): fixed 0.5/0.5 blend of E029 (routed LightGBM, FS2, `route_train_exclude`) and E031 (routed CatBoost GPU, FS2_RAW, CTRs at complexity 4). Development mean 438.87 s; holdout H WIN against E026 (369.18 against 375.93 s).
  - **Accepted findings:** CatBoost's categorical statistics carry signal at fixed capacity (E031 against E030, −4.91 s on `NM_present_excl_LIRF`); the blend beats E029 by −3.58 s (all rows) and −3.96 s (`NM_present_excl_LIRF`).
  - **Rejected or not shown:** E031 alone not a candidate; the blend's gain has **not** been attributed to the categorical statistics (the E029 + H022 blend was named and not run, H023 v3 revision 6); "LightGBM already holds the keys" (D4-C7) untested.
  - **Standing disclosures on E033:** D3-C1, D3-C3 (restated D5-C16), D5-C8, D5-C9, D5-C10, the 1,000-iteration budget.
  - **Standing rules** 1–13, rulings H, B, R, H3, H4, H5, rule L v2, hand-off base ruling.
- **Remaining budget:** Day 6 holdout access 1 of 1 (needs a Day 6 allocation as NEW, named by the phase close). Next experiment id **E035**. Last exchange **X-D05-S05-0001**; none pending.
- **Freeze:** `git diff --stat 803ceeb HEAD -- src scripts config` shows only `src/prc/tracking.py` (one line; the D5-C15 W&B lineage fix, which touches no prediction). Frozen-file hashes verify (`gate.py status`: frozen `32c41c0f9331`, advisor definition `30fff5dd3c54`).
- **Environment (rule L v2 item 6):**
  - CPython 3.13.15; polars thread pool 16; no `*_THREADS` variables set;
  - numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, polars 1.44.2, LightGBM 4.7.0, CatBoost 1.2.10, XGBoost 3.4.1, pandas 3.0.6; `uv.lock` `efa4fd78eaa6`;
  - RAM 10,951 MiB, swap 4 GiB unused (INC-0010); RTX 5060 Laptop 8,151 MiB, 921 MiB used at idle; boot `cf2c705b…` (unchanged since D05-S04).

  **This matches item 6.**
- **Owner instruction:** runs only 21:00–21:30 CEST (19:00–19:30Z), GPU and CPU. Recorded as **INC-0012**.
- **Open incidents:** INC-0004, INC-0009, INC-0010, INC-0012.
- **Resolved model ID:** researcher `claude-opus-5-5` (`--effort high`); Advisor `advisor` subagent, definition `30fff5dd3c54`.
- **Open questions carried** (Day 5 §9): CatBoost alone or other weights; submission reproducibility of a GPU re-draw; D3-C3's January exposure; D4-C7; neural models.
- **Day 6 theme (brief §3; advisor policy):** adversarial science. Try to show that the champion's claims are wrong.
- **First planned action:** a batched proposal set (H024–H028) of adversarial controls on E033's mechanism claim, sized to fit the 30-minute window; review X-D06-S01-0001; allocate E035–E039; commit; launch at 21:00.
