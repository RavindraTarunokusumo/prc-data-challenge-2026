# Acknowledgement — H030 v1 (exchange X-D06-S01-0003)

- proposal: `research/day-06/proposals/H030_v1.md`, sha256 `7695dc11a594aafec0e45149cdda3b94bcbab8f17e5614be6a5bfd08faeefd8a`
- review: `research/day-06/advisor/H030_review_v1.md`, sha256 `5aae8ef025af235e09cc9e90fb630b72ac45aa04bddbce1f99ef807946fc92a1`
- decision received: **ACCEPT**. Both hashes verified by the researcher at 2026-10-03T08:46Z.

The researcher adopts the review's Execution Authorization as written, including conditions **N1–N8** in `research/day-06/advisor/H029_review_v1.md` (allocation order H029 → E040, H030 → E041; config identity checks before arming; the pinned launcher `run_window_2.sh` and the pre-window record with E040's 8,100 s CLASS-L overrun bound; no re-attempt; status-only deferral; the N4 wording limits; the N5 reading rules on `passes_criteria_1_to_3` and per-fold |`fold_delta_rmse`| ≤ 1.0 s, with the labelled three-draw min–max; the N6 every-key resolved-parameter comparison without exemptions; the N7 same-script side-by-side figures; the N8 records). **This proposal maps to E041.**

**Correction accepted (review finding 1):** the proposal's description of E040 as "the draw Day 7's submission will be" is wrong. The SUBMIT fit trains on 12 months and is a fresh draw whatever the seed; E040 against E031 measures fixed-seed GPU run-to-run variation only. The proposal's sentence that a byte-identical refit would mean "Day 7's seed-42 fit reproduces E031 exactly" is withdrawn (N4). The batch is recorded as a reproducibility measurement and a third draw for rule 13; the review's assessment that it has almost no power to show E033 wrong is adopted for the record.
