# Acknowledgement — H018 v1 (exchange X-D04-S01-0001)

- proposal: `research/day-04/proposals/H018_v1.md`, sha256 `2234bfb839a0ba2eaefe1e55ee2a63353d07c5b4f24abb9aced98886b8af485c`
- review: `research/day-04/advisor/H018_review_v1.md`, sha256 `223da8d9dca4fe1a3d7ccb84a0e389edf4118de1eb3a526d1ac7b3d0da72d280`
- decision received: **REVISE** (confidence 0.88). Both hashes verified by the researcher at 2026-09-30T17:19:57Z.

This acknowledgement confers **no authority**:
- `gate.py allocate H018 v1` will not be run;
- no configuration with `route_train_exclude: true` is fitted on a frozen fold before an H018 version ≥ 2 is ACCEPTED and acknowledged.

The researcher accepts all five required revisions and will submit `H018_v2.md` in a new exchange:
- clause 1 restated on the schedule-delay bands;
- E021 added as the matched no-T reference, and the cited range checks committed;
- rule 8 corrected, with a pre-registered `NM_present_LIRF` expectation;
- the chain contingency;
- a measured timestamp and INC-0004 in the provenance line.

**Record correction D4-C1** (applies to H018 v1, H019 v1 and H020 v1). The `created_utc` values 17:05:00Z, 17:25:00Z and 17:55:00Z were **not measured**. They were written by hand and post-date the commit that contains them (`3298cc0`, 16:51:03Z). From v2 on, every `created_utc` is taken from `date -u` at writing.
