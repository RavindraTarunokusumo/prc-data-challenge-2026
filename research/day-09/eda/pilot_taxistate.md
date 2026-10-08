# Taxi-state design pilot (HANDOFF_D08 §4.1): rule not met

*Written 2026-10-08T00:22:17Z (D09-S01, laptop).*

- **Run:** `scripts/pilot_taxistate_D09.py`, on the owner's go-ahead ("Go"; INC-0024), after a first start without it had been stopped with no result.
- **Pre-registration:** parameters and rule in `research/day-09/proposals/TX_pilot_params.yaml`, committed at `0969550` before the run. Output: `research/day-09/eda/pilot_taxistate.json` and `.log`.
- **Targets read:** the design months only (2025-01, 04, 05, 06), at row level. No validation-month target and no December target was read.
- **Model:** LightGBM (E045 / E020's configuration), FS2 against FS2 plus the 7 taxi-state columns.

| Pilot | Predicted month | Reference RMSE | With taxi state | Difference | P features only (reported) |
|---|---|---|---|---|---|
| P1 | 2025-06 | 373.26 | 376.15 | **+2.90** | +2.21 |
| P2 | 2025-05 | 327.05 | 323.96 | **−3.10** | −0.93 |

**Decision rule (pre-registered): not met.** It needed at least 1.0 s better in both pilots.
- H039 is not written.
- Under HANDOFF_D08 §4.3 the plan's stop rule applies: the project refreezes, and E050 stands, unless the owner decides otherwise ("continue or refreeze"; X-D08-S03-0004 Q3).

Segment readings, reported only (the rule says they do not override it):

| Segment | P1 | P2 |
|---|---|---|
| NM-present | −1.00 s | −1.15 s |
| NM-missing | +39.70 s | −33.90 s |
| Tail (y ≥ 3,600 s) | +76.34 s (395 rows) | −75.39 s (219 rows) |
| Bulk | +0.58 s | −1.77 s |

- **LIRF:** +18.21 s in P1 and −17.05 s in P2.
- **The other nine airports:** mostly −1 to −4 s in both pilots. EHAM is +1.76 s in P1; LSZH and LTFM are about 0 in P2.
- **Reading:** the block helps ordinary rows by about 1 s. The sign of the all-rows change is set by a few hundred tail and NM-missing rows, mostly at LIRF, and it flips between the two months.
- **Not a lead under the rule.** Any restriction (NM-present only, non-LIRF only) would choose its population after seeing these readings (rule 10). It would also offer a route around a pre-registered rule (INC-0023), so none is proposed.

## Corrections (2026-10-08T18:07:50Z; X-D09-S01-0001)

- **D9-C1. The reading above is too strong.** "The block helps ordinary rows by about 1 s" and the segment table are pilot readings of one unrouted learner on all rows. They are not a claim about the mechanism.
  - The rule's population (all rows, unrouted training) did not match the construction Q5 B2 binds a candidate to: the LIRF NM-missing subgroup overridden from E045, with routed halves.
  - In P1, the LIRF rows' SSE increase exceeds the whole result.
  - The decision stands as the rule's output (rule 10).
  - **The mechanism is untested in a candidate's form.** No record may say that it was shown not to help, or that it would have passed.
- **D9-C3. Clerical.**
  - P2's EDDF (−0.13 s) is also about 0.
  - P1's LSZH (−4.30 s) lies outside "−1 to −4 s".
  - NM-present in P1 is −0.996 s, shown as −1.00.
