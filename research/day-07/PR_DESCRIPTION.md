# Day 7: final synthesis, submission, freeze

**Outcome.** The project is FROZEN. The champion is **E046** (H035 v1): E033 with the LIRF NM-missing subgroup predicted by an unrouted FS2 LightGBM. The final submission is **E050's file** (`predictions/final/E050/submitting.parquet`, SHA-256 `f0dc2c7c40063e238ef57f51d31192008e37c5327afcdc67d563868af17d06e8`). The owner uploads it once.

## What happened

- **SUBMIT procedure (E042–E044, X-D07-S01-0001).** E033's construction was refit on all 12 months for January and July 2026. The file passes I1–I5, with no flag.
- **Routing candidate (E045–E050, X-D07-S01-0002; INC-0015).** It came out of Day 3's routing price, and the owner chose to test it.
  - Development mean 314.42 against 438.87 (7/7 WIN). Criteria 1–4, 6 and the criterion 8 rule are met.
  - The Advisor corrected the forward risk (U6): the gain is a bet on LIRF's recording convention, with a downside of similar size. It made promotion conditional on a December WIN (U7).
- **Phase close (X-D07-S01-0003, ACCEPT 0.85).** December 2025 (one access, the project's last): **WIN, −124.24 s** (244.94 against 369.18). H035 was promoted. P4, pre-registered before the access, selected E050's file once E049 and E050 had completed and passed their checks.

## Key metrics

| | Development mean | Holdout H (Dec 2025) |
|---|---|---|
| E046 (final champion) | 314.42 | 244.94 |
| E033 (Day 5 champion) | 438.87 | 369.18 |
| E005 (Day 1 baseline champion) | 482.73 | 411.29 |

Neither figure is the submission's expected error (U6, P8).

## Deviations and corrections

- **D7-C14:** the E049/E050 run script stopped after E049 (the researcher's defect). E049's records were committed by hand, and E050 ran under a fixed script (INC-0016).
- **D7-C1 to D7-C13:** in `research/day-07/DAY_SUMMARY.md` §7 and the phase-close acknowledgement.

## Merge

This PR must be content-neutral (P7 (b)): the merged tree of `main` must equal the FROZEN commit's tree.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
