# E019 analysis: H015 v2 primary (routed LightGBM on FS2)

**Chain step 1 complete. Clauses 1, 2 and 4 are not met. Clause 3 (routing integrity) needs H016 v2 and is still open.** No decision on H015 is recorded until the chain finishes.

## Run

| Item | Value |
|---|---|
| Configuration | `routed_lightgbm` on FS2 (`63923e2`), E017's parameters, `route_ridge_params` {α 1.0, winsor [0.005, 0.995]}, seed 42 |
| Allocation | `gate.py allocate H015 v2` at `7e9c431`, clean tree |
| Status | COMPLETE: 954.1 s, peak RSS 4.76 GB (CLASS-M: within class) |
| Development mean | **444.49 s** (pre-registered 432–447). R1 446.40, R2 274.49, R3 397.25, S1 632.10, W1 472.22; S1c 638.38, W1c 488.59 |

**Provenance (authorization item 8).**
- **CPU:** Intel(R) Xeon(R) Processor @ 2.10GHz. The kernel boot id is in `provenance.yaml`.
- **Container restarts:** this is the first chain experiment. One restart occurred earlier in D03-S01, before X-D03-S01-0001 attempt 2, and none between allocation and completion.
- **INC-0004** (launch configuration disclosure) is open and covers this run.
- **Tooling interruption:** server-side command approval failed transiently for about 10 minutes after the run finished. The comparisons were run once it recovered. No comparison was attempted twice.

## Clause 1: promotion criteria against E005 (not met)

`compare.py E019 E005`: **mean dRMSE −38.23 s** (q95 −34.95). Criteria 1, 2 and 3 all pass.

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| dRMSE | −31.41 | −49.03 | −34.36 | −37.91 | −38.45 | −32.61 | −21.32 |
| Outcome | WIN | WIN | WIN | WIN | WIN | WIN | WIN |

- **Pre-registration:** −36 to −50 s; WIN on all development folds and S1c; W1c WIN or TIE. **All met.**
- **No airport** is degraded beyond the tolerance.
- **Rule 6.** Top-row shares are at most 0.10 in magnitude (S1 +0.10, S1c +0.06). Row 192622644 was pre-registered as the likely top row on S1 and S1c; the shares are consistent with it being so, but nothing dominates.
- **Rule 7.**
  - NM-present bulk is −48.9 to −55.4 s on the development folds.
  - NM-missing LIRF is **+0.0 on every fold**, because those rows are routed.
  - NM-missing at the other nine airports is a *loss* against E005 on R1, R2, R3 and W1 (+27.5 to +78.0 s bulk) and on W1c (+279.8 s). That is a sign disagreement. See Observations.
- **Tail share** of the SSE change (development folds): 0.300.

## Clause 2: congestion against the matched reference E017 (not met)

**2(a), 2(b):** `mechanism_check.py E019 E017 NM_present_excl_LIRF`. **Mean −6.75 s** (q95 −5.97); criterion 1 True, criterion 2 True.

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| dRMSE | −5.88 | −6.67 | −6.31 | −5.35 | −9.52 | −5.72 | −7.66 |
| Outcome | WIN | WIN | WIN | WIN | WIN | WIN | WIN |
| Top-1 share | −0.03 | +0.04 | +0.10 | +0.06 | −0.01 | +0.05 | +0.05 |

- **2(a) is not met:** criteria 1 and 2 pass, with 5 of 5 development WINs, S1 WIN and S1c WIN.
- **2(b) is not met:** the mean −6.75 s is below the −6.0 s floor. **The margin is 0.75 s.**
  - The floor is about three times the largest development-fold perturbation on this population (1.96 s).
  - The bootstrap q95 of the mean is −5.97 s, just inside the floor.
- **Rule 6 on the clause population:** no dominant row; |top-1| ≤ 0.10 on every fold (review (b)).

**2(c):** `mechanism_check.py E019 E017 NM_present`. The bulk dRMSE is −5.68, −5.46, −5.63, −5.48 and −5.22 s: **< 0 on every development fold. Not met.**

**Against the forecasts.**
- **The proposal** forecast C at −4 to −15 s on this population. The result, −6.75 s, is inside that range.
- **The Advisor** forecast −3 to −5 s, falling short of the floor (P(promotable) 0.20). The result is 1.75 s beyond the edge of that range.
- **Consistency.** All seven folds are within −5.35 to −9.52 s, and the bulk agrees on every fold. The effect is uniform, not driven by one fold or one row.

**Disclosure** (`excl_LIRF_NM_missing`, not a clause): mean −3.35 s (q95 −1.91); criteria 1 and 2 pass. R1 and R2 are TIE with near-zero net change (+0.52 and −0.04 s), and each has a dominant row. Per the rule 6 reading (b), a dominant row on a fold with |dRMSE| < 1.5 s is expected. Both rows are NM-missing at non-LIRF airports:
- R1: 196787086 (LEBL). y 1,315 s; E019 predicts 11,267 s and E017 6,258 s.
- R2: 197540199 (EHAM). y 482 s; **E019 predicts −8,859 s** and E017 −11 s; `d_sched` 19,981 s.

## Clause 4: criterion 8 (not met)

`NM_missing_LIRF.delta_rmse_bulk` against E005 is **+0.0 on every fold**, as expected by construction (routed rows).

## Clause 3: routing integrity (open)

Needs H016 v2 (chain step 2: `route_check.py E019 <H016> E005`). The reproduction, if due, follows clause 3.

## Reported: all rows against E017 (rule 11)

`compare.py E019 E017`: **mean dRMSE +65.67 s** (q95 +89.90), with a LOSS on all seven folds. Criteria 1–3 fail; airports degraded: LIRF (+26.2 %) and EHAM (+7.2 %).
- **This was pre-registered:** "worsen against E017 on all rows (the routing forgoes the learned convention tail gain)".
- NM-missing LIRF bulk is −1,225 to −7,104 s against E017. This is E017's learned convention mixture winning on the rows H015 routes away.
- H016 v2 gives the matched unrouted all-rows figure, and H015 − H016 on `LIRF_NM_missing` isolates R exactly.

## Observations (not clauses)

1. **Unbounded predictions on NM-missing rows at the nine non-LIRF airports.**
   - E019 predicts −8,859 s on an EHAM row with `d_sched` 19,981 s, and 11,267 s on a LEBL row with y 1,315 s.
   - This group (1–2 % of rows) is where FS2 loses to E005 in bulk on four development folds, and where both Tier 1 fits extrapolate on extreme `d_sched`.
   - It is a candidate Day 4 question. Code is frozen for this chain, so nothing is changed here.
2. **EHAM degradation against E017 on all rows (+7.2 %)** coincides with observation 1 (the R2 dominant row). It does not appear against E005 (no degraded airport).

## Next

Allocate H016 v2 (chain step 2), then `route_check.py` and `mechanism_check.py <H015> <H016> LIRF_NM_missing`. Then H017 v2. Then the conditional reproduction of H015 v2 if clause 3 is not met.

## Post-run container restart (recorded 2026-09-30T05:35:36Z)

- The container restarted after E019 completed and before this analysis was committed. The kernel boot id is now `b973b4fe-…` against the run's `ac2b2cff-…`.
- The working tree and data persisted. All 8 E019 prediction files re-verified against `manifest.json` (SHA-256 match).
- **Consequence (authorization item 8):** H016 v2 runs in a different container instance from E019. A clause 3(b) finding (identical predictions outside the routed subgroup) is therefore a **cross-container** determinism result, and is recorded as such.

## Phase-close corrections (appended 2026-09-30T07:06:50Z; X-D03-S01-0003)

- **D3-C1.** The `excl_LIRF_NM_missing` disclosure above omitted `criterion_3: false` (EHAM +7.2 %). Congestion as served (E019 − rE017, all rows) is −1.90 s (q95 −0.98), with R1 and R2 TIE. 95 % of the −38.23 s margin over E005 is routed FS1 structure.
- **D3-C2.** Observation 1's explanation ("`d_sched` extremes") is withdrawn. The out-of-range predictions are caused by the congestion block carrying the LIRF convention learned in training to non-routed NM-missing rows.
- **D3-C7.** The NM-present bulk range against E005 is −47.9 to −55.4 s (R2 −47.91), not −48.9 to −55.4 s.
- **Outcome.** H015 v2 PROMOTE: phase close ACCEPT, holdout WIN (−35.36 s). E019 is champion.
