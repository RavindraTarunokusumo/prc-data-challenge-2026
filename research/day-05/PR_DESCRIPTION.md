## Day 5: model architecture, CPU against GPU (phase close X-D05-S05-0001 ACCEPT; holdout WIN; new champion E033)

**Outcome.** E033 becomes champion; E019 is previous. E033 (H023 v3) is a fixed equal-weight blend of the routed LightGBM (E029, with the D3-C2 treatment) and a routed CatBoost on GPU with categorical statistics on raw keys (E031).

| | Validation RMSE (development mean) |
|---|---|
| E033, new champion | **438.87 s** |
| E019, previous champion | 444.49 s |
| E005, Day 1 baseline | 482.73 s |

- **Against E019 (laptop instance E026):** −5.62 s, WIN on all 7 folds including S1, every airport improved. Criteria 1–8 met. Reproduced by E034.
- **Holdout (December 2025):** WIN, 369.18 s against 375.93 s (−6.75 s), recorded only.
- **Disclosures:**
  - D5-C8: of the margin, −2.04 s is the D3-C2 treatment and −3.58 s is the CatBoost half;
  - D5-C9: a stochastic champion (GPU re-draw);
  - D5-C10: single rows;
  - D3-C3 restated: the January long-delay rows.

**Advisor exchanges:**
- X-D05-S04-0001: REVISE ×4;
- X-D05-S04-0002: LAPTOP_REFS ACCEPT (rule L v2);
- X-D05-S04-0003: H021–H023 v3 ACCEPT;
- X-D05-S05-0001: phase close ACCEPT (0.88).

**Infrastructure:**
- laptop data re-download, with silver rebuilt byte-identical;
- experiment lock;
- W&B mirror with learning curves;
- FS2_RAW; CatBoost `cat_mode`; `prc.blending`;
- runner records: GPU memory, GPU failure, swap, environment, start commit;
- the cause of the laptop differences (polars thread pool).

**Incidents:**
- INC-0006: closed, no delegation;
- INC-0007: closed;
- INC-0008: closed; E025 OOM caused by a concurrent researcher pytest;
- INC-0009: open; W&B;
- INC-0010: open; owner decisions to keep 4 GB swap and CPython 3.13;
- INC-0011: closed; owner pause.

**Records:**
- corrections D5-C1 to D5-C16 (`research/day-05/acks/`);
- standing rule 13 and ruling H5;
- `research/day-05/DAY_SUMMARY.md` (FINAL), `research/STATE.md` (rebuilt).

Tests: 158 passed; ruff clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
