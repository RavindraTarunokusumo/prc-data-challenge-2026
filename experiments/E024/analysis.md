# E024 analysis: H019 v2 primary (routed LightGBM on FS3 = FS2 + 5 fold-local LOMO priors; matched reference E023)

**Outcome: "mechanism FALSIFIED, not promoted."** Clauses 1(a) and 1(b) are both met; clause 2 is not met. Promotion also fails frozen criterion 2 against E019 (S1 TIE). No reproduction is due (authorization item 5), and E019 remains the champion.

## Run

| Item | Value |
|---|---|
| Configuration | E023's, with `hypothesis_id: H019`, `proposal_version: 2`, `feature_set: FS3` (authorization item 2). `route_train_exclude: true`, seed 42, all 8 folds, CLASS-M |
| Allocation | `gate.py allocate H019 v2` at `5e8ec98`, clean tree, after E023's checkpoint (`b424afb`) and the journal's "NOT PROMOTED" record (precondition 1(b)) |
| Status | COMPLETE: 1,026.9 s, peak RSS 5.73 GB (CLASS-M: within class) |
| Development mean | **442.06 s** (E023 442.46; E019 444.49). R1 442.74, R2 268.30, R3 395.29, S1 632.82, W1 471.15; S1c 637.03, W1c 486.95 |

**Recording (item 8(a)).**
- **CPU:** Intel(R) Xeon(R) Processor @ 2.80GHz.
- **Container restart since E023's run: no** (same kernel boot id `f948bf23-…`).
- **INC-0004** open.
- **Launched by** the main session (`claude-opus-5-5`), not delegated (INC-0005).

**Item 8(b): W1c.** E024's W1c prediction file is **byte-identical** to E023's (SHA-256 `37857400ac9d…` for both). The block is inert on a single training month, as pre-registered (Advisor P 0.99). All other folds differ.

## Clause 1: the block on `NM_present_excl_LIRF` against E023 (MET)

`mechanism_check.py E024 E023 NM_present_excl_LIRF`:

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| dRMSE | −0.62 | −1.37 | −1.04 | −0.03 | **+1.63** | −1.12 | 0.00 |
| Counted outcome | WIN | WIN | WIN | **TIE** | **LOSS** | — | — |

- **1(a) is met, on three counts:**
  - criterion 1 fails: mean −0.29 s, **q95 +0.12** (not < 0), and the mean is above −1.0 s;
  - S1 is not a counted WIN (TIE), so the "3 WINs among R1, R2, R3 and S1, S1 required" condition fails, although R1–R3 are WINs;
  - W1 is a LOSS.
- **1(b) is met:** the mean point estimate, −0.29 s, is above −3.0 s.
- **Item 8(c):** 4-fold mean (R1–R3, S1) **−0.77 s**, beside the 5-fold mean of −0.29 s. Even without W1, the block is a quarter of the floor.
- **Rule 6.** S1 has a dominant row on a near-zero net change: **191606727** (EHAM, NM-present, y 10,972 s; E024 1,981 s against E023 2,985 s; top-1 share −6.05). As rule 6 reading (b) expects for a fold with |dRMSE| < 1.5 s. R1 and R3 have top-1 shares 0.24 and 0.29, with no dominant row.

## Clause 2: all rows against E023 (not met)

`mechanism_check.py E024 E023 all`: **mean −0.40 s** (q95 −0.03). R1 −0.65, R2 −1.40, R3 −0.65 WIN; S1 +0.52, W1 +0.21 TIE; S1c −0.20; W1c 0.00.
- The point estimate is below 0, so **clause 2 is not met.**
- **Rule 6.** Dominant rows sit on the TIE folds:
  - S1: **192622644** (LIRF, NM-present, y 87,002 s; E024 5,780 s against E023 7,041 s; top-1 share 1.63);
  - W1: **183667483** (LSZH, y 257 s; E024 7,307 s against E023 6,150 s; top-1 share 0.53).
- **Per-airport disclosure** (pooled all-rows RMSE against E023): no airport degraded beyond tolerance. **LFPG**, named in advance, is +0.35 s (+0.13 %); its bulk is −0.48 s. The largest gains are LTFM −1.94, LEBL −1.76 and EDDF −1.50 s. The proposal expected the largest gains at LFPG, EGLL and LTFM: only LTFM matches.

## Promotion against E019 (comparator in force, item 4(b)): fails

`compare.py E024 E019`: **mean −2.43 s** (q95 −1.59).

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| dRMSE | −3.66 | −6.20 | −1.95 | +0.72 | −1.07 | −1.35 | −1.64 |
| Counted outcome | WIN | WIN | WIN | **TIE** | TIE | WIN | TIE |

- **Criterion 1 passes. Criterion 2 FAILS: S1 is TIE.** Criterion 3 passes. `passes_criteria_1_to_3: false`.
- **Criterion 4 (B2)** also blocks it: H019's clauses 1(a) and 1(b) are met. (H018 v2's clauses 1–2 were not met.)
- **Item 4(c), S1 recording.** S1 is not a WIN, so no WIN is attributed. The `NM_present_LIRF` share of S1's SSE change is **1.95** (≥ 0.5). The dominant row is again **192622644** (top-1 share 2.16; E024 5,780 s against E019 8,136 s; y 87,002 s). The prior block moves this convention-mixture row further from its target. That matches D4-C5: the block adds no convention row to any prior, but the fit on the retained LIRF NM-present tail rows still changes.
- Pooled tail share of the SSE change: −0.05.

## Item 8(d): `NM_present_LIRF` against E023

The values are derived exactly as (E024 − E019) − (E023 − E019) from the two `compare.py` outputs (same rows):

| Fold | R1 | R2 | R3 | S1 | W1 |
|---|---|---|---|---|---|
| Full (expected within ±8 s) | −2.80 | −1.72 | −1.31 | +6.12 | −2.04 |
| Bulk (expected −1 to −6 s) | −3.41 | −1.27 | −3.25 | −1.27 | −3.07 |

- Every value is inside its expectation. The Advisor's P 0.40 of "full outside ±8 s on at least one fold" did not occur. S1 (+6.12) comes closest, carried by row 192622644.
- **The block helps LIRF NM-present bulk rows by 1.3–3.4 s on every development fold,** more than on `NM_present_excl_LIRF`. This is an observation, not a clause.

## Item 8(e): attribution pair (development mean, all rows)

| Contrast | Mean dRMSE | R1 | R2 | R3 | S1 | W1 |
|---|---|---|---|---|---|---|
| H018 − E019 (E023 − E019) | −2.04 | −3.00 | −4.80 | −1.30 | +0.20 | −1.28 |
| H019 − H018 (E024 − E023, all rows) | −0.40 | −0.65 | −1.40 | −0.65 | +0.52 | +0.21 |
| Sum (E024 − E019) | −2.43 | −3.66 | −6.20 | −1.95 | +0.72 | −1.07 |

84 % of E024's margin over E019 is H018's training exclusion. The prior block adds −0.40 s, and it moves S1 the wrong way.

## Integrity and range

- **`route_check.py E024 - E005`:** the routed rows equal E005 on all 8 folds. **Not INVALID.**
- **`range_check.py E024 E023`** (rule 12; `NM_missing_other` bulk, out-of-range by `d_sched` band, 5 development folds):

| Model | < 1 h | 1–3 h | > 3 h |
|---|---|---|---|
| E024 | 82 | 11 | 6 |
| E023 | 82 | 12 | 5 |

The block leaves the D3-C2 treatment intact (> 3 h stays far below E019's 81).

## Against E005 (reported)

`compare.py E024 E005`: WIN on 7/7, criteria 1–3 pass. E024 is the best development mean so far (442.06), but it is not a candidate.

## Against the forecasts

| Forecast | Outcome |
|---|---|
| Advisor: mean < 0 on `NM_present_excl_LIRF` (P 0.80) | −0.29: **yes** |
| Advisor: mean ≤ −3.0 (P 0.30) | **no** |
| Advisor: 1(a) not met (P 0.50) | **met** (fails) |
| Advisor: mechanism supported (P 0.27) | **no: falsified** |
| Advisor: W1c byte-identical (P 0.99) | **yes** |
| Advisor: all rows < 0 against H018 (P 0.70) | −0.40: **yes** |
| Advisor: `NM_present_LIRF` full outside ±8 on ≥ 1 fold (P 0.40) | **no** (max +6.12) |
| Proposal: the EDA's incremental R² (stand × runway +0.189 over airport × hour) carries into the model | **Not borne out**: −0.29 s on the clause population |

## Reading

1. **The prior block does not carry beyond FS2 in this learner.** Fold-local LOMO target statistics over stand × runway and four other keys add −0.29 s on the insulated population, with W1 a LOSS. That is about one tenth of the pre-registered floor.
2. **A likely reason (not tested).** LightGBM on FS1 already sees stand, runway and operator as categoricals, and it can learn their main effects and interactions directly. The EDA's R² was measured over an airport × hour prior in a linear model, not over FS2 in a tree learner. Like the Day 3 T-dominance picture, this is an EDA effect that a stronger baseline absorbs. The claim is made for the block; K5 is not separated (Required Ablation).
3. **E019 remains champion.** Neither Day 4 candidate is promotable: H018 v2 fails S1 against E019, and H019 v2 is falsified. Both S1 TIEs are carried by row 192622644 (LIRF, NM-present convention mixture).
4. **Next:** the Day 4 phase close. No promotion is proposed, so the Day 4 holdout access is proposed to close unused.
