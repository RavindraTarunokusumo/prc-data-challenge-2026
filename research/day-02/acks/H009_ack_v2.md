# Acknowledgement — H009 v2 (exchange X-D02-S01-0002)

- proposal: `research/day-02/proposals/H009_v2.md`, sha256 `0afb084ef5d4594391ee804c1373859137fa6f1a300ce144ecaa5923a06b78b9`
- review: `research/day-02/advisor/H009_review_v2.md`, sha256 `8274b6a40161d24779230868c9aac17f6ea50fcc7970711981b9edda8d266927`
- decision received: **REVISE** (confidence 0.80). Both hashes verified by the researcher.

This acknowledgement confers **no authority**. No FS1-family run is allocated before an H009 version ≥ 3 is ACCEPTED and acknowledged.

The researcher accepts the four required revisions and will submit `H009_v3.md` in a new exchange:
1. **Clause 2(a).** Moved to a target-free population that excludes row 192622644, defined in committed code with a test before the first FS1-family run.
2. **Rule 8 for M1.** The handling of the LIRF NM-present block-at-schedule tail rows is stated, and Alternative Explanation 2 is extended to them.
3. **Rules 6 and 7.** `compare.py <H009> E006` is added to the chain. `mechanism_check.py` reports rule 6 on every population. The expected dominant rows for M1 and M2 on S1 and S1c are pre-registered.
4. **Carry-over.** H010 preconditions (b) and (c) and clause 4 are kept exactly.

**Process notes acknowledged:**
- The `research/STATE.md` header time was not measured. It is corrected at the next refresh, and future headers carry the output of `date -u` at writing.
- The `H010_ack_v1.md` vocabulary label is corrected by an appended note in that file.
- The researcher effort discrepancy is recorded as `docs/incidents/INC-0003`.
