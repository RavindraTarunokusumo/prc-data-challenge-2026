# Acknowledgement — H019 v2 (exchange X-D04-S01-0002)

- proposal: `research/day-04/proposals/H019_v2.md`, sha256 `df74347ccaeeb6f1b48b5089744010ce8951b943365792f49e74c3664e1d2c6d`
- review: `research/day-04/advisor/H019_review_v2.md`, sha256 `9f85d2e93b1f951fc3bce5453f276938c931ea8c3c0ab45576a6bcfdf97dc914`
- decision received: **ACCEPT** (confidence 0.80). Both hashes verified by the researcher at 2026-09-30T17:48:35Z.

**Adopted:** the review's Execution Authorization items **1** (preconditions: H018 v2 COMPLETE, not INVALID, checkpointed; H018's promotion status recorded in the journal; tools freeze), **4** (readings), **7** (promotion), **8** (recording (a)–(e)) and **9** (not authorized), verbatim. In particular:
- **4(a) Clause 1(a).**
  - WINs are read from `fold_outcome_counted` (the frozen twin rule), among R1, R2, R3 and S1. At least 3 are needed, and S1 must be a counted WIN.
  - No development fold R1–W1 may be a LOSS.
  - Criterion 1 is read from the same output. The tool's `criterion_2` field is not the clause.
- **4(b) Comparator.**
  - The H018 run is the champion in force only if it is recorded "promoted first in this chain". Criterion 4 is then clauses 1–2.
  - Otherwise E019 is. Criterion 4 is then H019's clauses 1–2 plus H018 v2's clauses 1–2, under B2.
- **4(c) S1 recording.** H018 v2's `NM_present_LIRF` rule applies, and so does `H018_review_v2.md` item 8(d) with "the prior block" in place of "the D3-C2 treatment".

**Authorized next step (after the preconditions):**
- `gate.py allocate H019 v2`.
- The config is H018's run config with `hypothesis_id: H019`, `proposal_version: 2` and `feature_set: FS3`.
- Then the comparisons of item 3. The reproduction runs only under item 5.

**Record corrections:**
- **D4-C4.** The Implementation Plan of `H019_v2.md` reads "`gate.py allocate H019 v1`". It means **`v2`**.
- **D4-C5.** Rule 8's "The prior block adds no convention exposure" is replaced by: *"The prior block adds no convention row to any prior. The fitted model can still change its fit on the retained LIRF NM-present tail rows (E016; E017 − E018 +36.9 s on S1 in this cell)."*
- **D4-C6** (Advisor record note). v2 rewrote clause 1(a)'s WIN count and dropped v1's "twin rule included" without saying so. Reading 4(a) restores the frozen twin rule.
