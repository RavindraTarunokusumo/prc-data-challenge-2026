# Acknowledgement — H012 v1 (exchange X-D02-S01-0002)

- proposal: `research/day-02/proposals/H012_v1.md`, sha256 `d4ad80e4a91f7bd68d5a8583420001b995981da4c43c089ab7519ba59e399e85`
- review: `research/day-02/advisor/H012_review_v1.md`, sha256 `293d1fba0e0802ca48eda0f6c4a8ff25b35f114f95ea6b25175366813dbe1818`
- decision received: **ACCEPT** (confidence 0.80), conditional. Both hashes verified by the researcher.

**Adopted preconditions.** All of these must hold before `gate.py allocate H012 v1`:
- (a) An H009 version ≥ 3 has decision ACCEPT, and its acknowledgement is committed.
- (b) That version keeps FS1 exactly (`src/prc/features.py: fs1` as at `cba278d`, or byte-identical output), with H009 v2's model, parameters, folds and seed.
- (c) That version keeps clause 4 exactly: `scripts/mechanism_check.py <H009> <H012> NM_present`. H009 is falsified if it fails frozen criterion 1 or criterion 2 there.
- (d) The H009 and H010 primary runs are COMPLETE.
- (e) No other experiment runs concurrently.

**Lapse rule adopted.** If (b) or (c) does not hold, this ACCEPT lapses and `H012_v2` is required.

**Recorded corrections.**
- **Expected Result inconsistency.** The expected development mean (430–480 s) does not follow from the expected NM-present range (300–350 s), which implies about 407–445 s. The NM-present range is the operative expectation.
- **Rule 8 is engaged by one NM-present record:** 192622644 (LIRF, y = 87,002 s, `d_aobt3` = 87,181 s, `d_sched` = 87,001 s) on S1 and S1c. There the anchor is exact and the row is also a block-at-schedule record. Its effect on clause 4 is disclosed through the rule 6 output of `mechanism_check.py`.
