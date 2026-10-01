# Acknowledgement — PHASE_CLOSE_D04 v1 (exchange X-D04-S02-0001)

- proposal: `research/day-04/proposals/PHASE_CLOSE_D04_v1.md`, sha256 `1c7609037e02a42e7c185adff73354194b0dcd94eb5d1141966d0ae5e60a5ee5`
- review: `research/day-04/advisor/PHASE_CLOSE_D04_review_v1.md`, sha256 `c809853a0fa97efce1135feb899262ee2713b615aa378110c403f9d17460eb6f`
- decision received: **ACCEPT** (confidence 0.85). The researcher verified both hashes at 2026-10-01T01:56:37Z.

## Adopted

The researcher adopts **Execution Authorization items 1–3 and every condition on the phase-closing commit**, verbatim.

**1. The Day 4 decisions stand.**
- **E019 (H015 v2)** is the phase-closing champion, by rule. Its standing disclosures are D3-C1 to D3-C3 and D4-C9.
- **H018 v2 (E023):** mechanism supported; D3-C2 treated, not promoted (criterion 2).
- **H019 v2 (E024):** mechanism falsified; not promoted (criterion 2; criterion 4 under B2).
- **H020 v1:** REJECT, closed.
- There is no retroactive promotion and no re-adjudication (rule 10). The audit figures in Scientific Validity (b) are attribution only.

**2. Ruling H4: no Day 4 holdout access.**
- The record reads "Day 4: 0 of 1, closed unused". It is not a TIE.
- There is no carry-over and no substitute comparison.
- **No `holdout_check.py` invocation with E023 or E024 as NEW is authorized, in any phase.**
- E019 is Day 5's phase-opening champion. A Day 5 access needs a Day 5 allocation as NEW. E012–E018 and E020–E024 may never be NEW.

**3. The hand-off base ruling (Scientific Validity (e)), recorded as written.**
- **What may be stated.** Under ruling R, E023 is the matched reference for any candidate that keeps `route_train_exclude: true` on FS2, and E024 is the matched reference for FS3.
- **What may not be stated.** E023 is not a default or recommended base, and not a de facto champion. Choosing the base is a Day 5 proposal's decision.
- **How such a candidate is judged.** It is judged against E019. Its criterion 4 includes H018 v2's clauses 1–2, both recorded as not met. Its rule 8 pre-registration states the single-row S1 exposure.
- **Rule 10** applies to the configurations of E020, E021, E023 and E024. A variant that differs only by compute backend or library build is a re-draw of the same configuration. It is admissible only if its proposal pre-registers a mechanism for that difference.

**Missing controls named for Day 5 (not designed here).**
1. Single-row exposure disclosure under rule 8: rows 192622644 (S1) and 183910286 (W1).
2. The H019 controls: a within-key permuted prior, and a K5-only block.
3. The H020 controls for any CatBoost proposal.

## Corrections appended

The proposal and the completed records (analyses, comparisons, gate records) are not edited. DAY_SUMMARY.md, STATE.md and HANDOFF_D04.md are corrected as the conditions require.

**D4-C7. The prior block's size and scope.**
- The block gives −0.29 s on `NM_present_excl_LIRF` (q95 +0.12; R1–R3 WIN, S1 TIE, W1 LOSS) and **−0.40 s on all rows** (q95 −0.03; R1–R3 WIN).
- The gain is real but small: a tenth of the −3.0 s floor, and below criterion 1. The mechanism is falsified as pre-registered.
- "LightGBM already holds the keys" is **untested**. The controls that would test it are a within-key permuted prior and a K5-only block.
- W1's LOSS sits at LTFM (share 0.58) and EHAM (0.42); LFPG carries 0.10. Staleness is untested.
- "Not worth a further variant" is a planning judgement, not a finding.

**D4-C8. "At no cost elsewhere"** holds only on `NM_present_excl_LIRF` (±0.56 s; R2 LOSS +0.37 s). Elsewhere the treatment has two costs:
- S1 `NM_present_LIRF` +7.76 s. This is one row, and it blocks the promotion.
- W1c `NM_missing_other` full +106.33 s, from tail rows.

**D4-C9. Single-row outcomes against E019** (a standing disclosure on the champion).
- **Row 192622644** (LIRF, NM-present, y 87,002 s) carries 8.2 % of E019's S1 SSE.
  - Committed predictions on it range from 2,513 to 22,473 s. E019's 8,136 s is the FS2 family's highest.
  - Audit only: without this row, S1 is a WIN for both E023 and E024 against E019, and E023 meets criteria 1–3 (mean −2.19 s, q95 −1.53).
- **E023's W1 WIN** is carried by row 183910286 in the same way. Without it, W1 is TIE.
- **The other LIRF NM-present tail rows** net to about 0 s.
- **The narrower Day 4 finding.** Both Day 4 changes lowered the prediction on the day-scale record (8,136 → 7,041 → 5,780 s). So the S1 constraint binds changes that lower predictions on day-scale records. The earlier wording, "any treatment moves this row", was too broad.
- **H018 v2's rule 8 S1 cell forecast** held numerically, but its stated mechanism (tail predictions falling) did not occur.
- No reading of criterion 2 changes.

**D4-C10. Advisor forecast misses** (added to DAY_SUMMARY §7).

| Forecast | Predicted | Outcome |
|---|---|---|
| H018: > 3 h band | central 22 (80 % interval 12–40) | 5 |
| H018: W1 | 0 ± 1 s | −1.28 s |
| H018: W1c | 0 to +7 s | −1.64 s (wrong sign) |
| H019: `NM_present_excl_LIRF` | −0.5 to −4 s | −0.29 s |
| H019: all rows | −0.5 to −3 s | −0.40 s |
| H019: largest fold gain | W1 most likely | W1 the only LOSS |
| H019: leading airports | LFPG, EGLL and LTFM | LTFM only |

Both primary failure modes were correct.

**D4-C11. Ledger decisions** (`experiments/ledger.jsonl`, re-exported from the SQLite ledger through `prc.ledger.export`).

| Experiment | Decision | Note |
|---|---|---|
| E019 | PROMOTE | Day 3 record gap |
| E022 | PROMOTE | Passing reproduction, as for E007–E009 |
| E020, E021 | none | No promotion decision by design; recorded in the notes |
| E023 | REJECT | Notes as in review (f) |
| E024 | REJECT | Notes as in review (f) |

**D4-C12. Delegated-work list** (DAY_SUMMARY §8).
- **`e4c57f8` is added.** It is a main-session commit, and it also committed `range_check_refs.json`, the output of the worker's `--bands` code, without the provenance line.
- **The D04-S01 pipeline digest was never committed.** No record depends on it.
- Otherwise the list is complete and the delegation boundary held.

**D4-C13. STATE.md was stale** in Day 4, the fourth phase running. It is rebuilt at this close.

**D4-C14. HANDOFF_D04.md** is finalised:
- its stale values are updated;
- it now covers H020's deferral and objections, E023 and E024 as open work, the champion's disclosures, the Day 5 holdout facts, the `gate.py` day/session semantics and the ledger decisions;
- it notes the SUBMIT_JAN/SUBMIT_JUL procedure as non-blocking.

**D4-C15. Process.**
- E024's `gate.json` and ledger row say D04-S01, because `gate.py` copies `day` and `session` from the proposal. The gate record is not edited.
- E023's allocation records stayed uncommitted for about 7 h across a container restart, against brief §4. No result depends on it. A same-second allocation commit, as for E024, is the practice to keep.

**D4-C16. Advisor record.**
- `H018_review_v2.md` did not identify that one day-scale row would decide S1. It also accepted H018's rule 8 tail mechanism, which did not occur.
- `H019_review_v2.md` forecast W1 as the largest gain while recording W1's staleness.
- No decision would have changed.

## INC-0005

**Closed at this phase close,** with D4-C12 appended. If delegation recurs on Days 5–7, it needs a new incident. **INC-0004 stays open** (owner decision).

## Authorized next steps

- Commit this ack.
- Finalise STATE, DAY_SUMMARY, HANDOFF_D04, the journal and the ledger.
- Close INC-0005.
- Commit the mirror and the session-registry end event for D04-S02.

No allocation, run, fit or holdout access is authorized in Day 4.
