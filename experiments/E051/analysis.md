# E051 analysis: H038 v2 (candidate): E046 with the LIRF NM-missing subgroup predicted by the convention mixture

**Development reading: criterion 2 not met.** One development WIN (R3), with S1 a TIE. **H038 is not promotable.**
- Criteria 1 and 3 are met, as are criterion 4's decisive reading, criterion 6 and criterion 8.
- The development mean improves by 20.10 s (q95 −2.98), but the gain sits on a few rows that the fold-level bootstrap cannot call.
- Under the known-row reading (ruling (E)), no frozen WIN carries confirmatory weight: R3's WIN rests on its two known rows.

**Disclosures** (every Day 8–12 record):
- Leaderboard isolation for Days 8–12 rests on no recorded commitment; what was known at reopening is not stated; E050's upload is unverified (INC-0017).
- The Day 8 records written before the merge of `origin/day-7` stated that no leaderboard figure had been seen. That was wrong: one had been disclosed to the researcher on 2026-10-04 (INC-0020). The Advisor's context received it on 2026-10-06 (X-D08-S03-0001). It is not used.

## Run

| Item | Value |
|---|---|
| Config | `convention_mixture`, base E046, FS2, folds R1, R2, R3, S1, W1, S1c, W1c and H (predicted only; A1), seed 42, CLASS-M |
| Status | COMPLETE: 121.5 s, 4.55 GB peak; started 2026-10-06T23:03:00Z, ended 23:06:51Z; within class |
| Window | INC-0021 (owner): 2026-10-06T22:40:51Z to 2026-10-07T00:40:51Z. The first arming failed before start (INC-0022); re-armed at 23:02:52Z |
| Integrity | `mixture_check.py E051 E046`: **PASS on all 8 folds**. Max \|Δ\| outside the subgroup 0.0; subgroup against components 0.0; formula 0.0. Subgroup rows 168/115/52/337/58/337/58/88. The component files' manifest is in `research/comparisons/mixture_check_E051.json` |
| H | Predicted only. Never scored or truth-read (H8). No analysis of the H predictions beyond the mixture check |
| W&B | sync failed (CommError); not mirrored (INC-0009) |

## Development results against E046 (`research/comparisons/E051_vs_E046.json`)

| | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| E051 | 270.46 | 239.72 | 264.05 | 406.50 | 290.87 | 414.61 | 323.99 | **294.32** |
| E046 | 274.34 | 238.33 | 294.43 | 414.44 | 350.59 | 431.56 | 434.35 | 314.42 |
| ΔRMSE | −3.88 | +1.39 | −30.38 | −7.94 | −59.72 | −16.96 | −110.36 | **−20.10 (q95 −2.98)** |
| q10 / q90 | −10.98 / 3.28 | −3.65 / 6.59 | −47.51 / −5.40 | −26.65 / 11.50 | −122.92 / 1.51 | −34.34 / −1.40 | −207.84 / 4.38 | |
| Outcome | TIE | TIE | **WIN** | TIE | TIE | WIN | TIE | |

- **Criterion 1: met** (−20.10 ≤ −1.0; q95 −2.98 < 0).
- **Criterion 2: not met.** One WIN; S1 is a TIE; no LOSS.
- **Criterion 3: met.** Only LIRF changes, and no airport is beyond +3 %.

## Ruling (E): the known-row reading (`E051_vs_E046_known_rows.json`)

| | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| Known rows | 2 | 4 | 2 | 5 | 1 | 5 | 1 |
| Known rows' share of the fold's SSE change | −1.07 | −1.81 | **0.92** | −0.44 | **0.99** | | |
| Frozen outcome | TIE | TIE | WIN | TIE | TIE | WIN | TIE |
| ΔRMSE with known rows reverted | −8.10 | +3.90 | −2.42 | −11.50 | −0.45 | −8.64 | +1.63 |
| Reverted outcome | WIN | TIE | TIE | WIN | TIE | | |
| Confirmatory weight of a frozen WIN | | | **none** | | | | |

- **R3's WIN rests on its two known rows** (0.92 of its SSE change), so it carries no confirmatory weight.
- W1's gain is 0.99 one known row (183903219).
- **On R1, R2 and S1, the known rows go against the candidate** (negative shares). Reverting them turns R1 and S1 into WINs.
  - That reading is reported only. The frozen computation governs criterion 2, and the reading cannot create a WIN.
- **(E)(vi):** no development fold is LOSS after reversion.
- G5's consequence is moot, because criteria 1–3 do not pass as frozen.

## Criterion 4 (`E051_vs_E046_mixture_analysis.json`)

Subgroup SSE changes against E046 (s²):

| | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| Subgroup rows (convention rows) | 168 (73) | 115 (56) | 52 (32) | 337 (109) | 58 (44) | 337 (109) | 58 (44) |
| Subgroup SSE change | −3.9e8 | +1.2e8 | −2.8e9 | −1.2e9 | −5.5e9 | −2.7e9 | −1.2e10 |
| Convention rows (c = 1) | −7.8e8 | −1.6e8 | −2.9e8 | −1.8e9 | −5.5e9 | −1.6e9 | −1.2e10 |
| Non-convention rows, `d_sched` ≥ 3,600 s | +3.9e8 | +3.0e8 | **−2.5e9** | +5.6e8 | +4.5e7 | −9.8e8 | +6.5e7 |
| Non-convention rows, `d_sched` < 3,600 s | +5.6e6 | −2.2e7 | +1.4e7 | −3.5e7 | −3.1e6 | −1.5e8 | +2.3e7 |
| Tail / bulk | −4.2e8 / +3.2e7 | −1.3e8 / +2.5e8 | −2.8e9 / +6.9e7 | −1.2e9 / −6.4e7 | −5.5e9 / +4.4e7 | −3.1e9 / +3.9e8 | −1.2e10 / +5.4e7 |
| Classifier AUC (validation) | 0.86 | 0.87 | 0.93 | 0.84 | 0.86 | 0.78 | 0.61 |
| Rule 6 top-10 share | 0.62 | 0.62 | 0.95 | 0.54 | 0.98 | 0.54 | 0.98 |

- **Reading (a), the sign test (ruling (G)): holds.** On every development fold where the subgroup gains (R1, R3, S1, W1), the convention rows gain too. R2's subgroup does not gain, so the reading does not apply there.
- **Reading (b): holds** (mixture check, 0.0 s off the subgroup).
- **The majority-share reading** (reported, decides nothing): it fails on R3. There, the non-convention day-scale rows carry 0.90 of the gain (−2.5e9 of −2.8e9), mostly through its two known rows (0.92 of R3's SSE change; 200300302 is a non-convention day-scale row, D8-C10).
- **Classifier claim (secondary): holds.** The candidate's subgroup SSE is below constant p's on 5 of 5 development folds. The validation AUC (0.84–0.93 on development folds) is far above the pilot's 0.67–0.68.
- **Ablation against E046:**
  - the convention component alone beats the candidate on R3, W1 and W1c, but loses on R1 and R2 and is close on S1;
  - g alone loses on every fold.
- **Alternative explanations, read:**
  - On R1, R2 and S1, the non-convention rows with large `d_sched` **lose** (moving toward `d_sched` hurts them), and the convention rows win.
  - On R3, those rows carry the gain. That gain is unattributed to the convention.
- **The bulk** (y < 3,600 s) loses a little on 6 of 7 folds and gains on S1. **The tail** gains on every fold.

**S1 against the pre-registered statement.**
- The bulk was expected to be "uncertain in sign" (+5 to −9 s): it gained slightly (−6.4e7 s²).
- The tail was expected to gain −5 to −10 s: S1's total is −7.94 s.
- The S1 risk from July's lower convention rate did not appear as a bulk loss.

## Criterion 8 (ruling B) and rule 12

**Criterion 8: met.** `NM_missing_LIRF.delta_rmse_bulk`:

| | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| Against E033 | +2,869.8 | +2,399.6 | +2,941.9 | +4,263.3 | +1,767.3 | +4,061.2 | +1,971.7 |
| Against E028 | +2,869.8 | +2,399.6 | +2,928.1 | +4,262.9 | +1,767.1 | +4,061.2 | +1,971.6 |
| Against E046 | +46.1 | +765.6 | +608.8 | −29.1 | +700.7 | +186.6 | +808.6 |

Every value is ≤ +6,500 s against both E033 and E028.

**Rule 12:**
- Subgroup bulk rows predicted above 3,600 s, E051 against E046: R1 23/27, R2 7/10, R3 5/7, S1 81/104, W1 4/2, S1c 91/110, W1c 5/3.
- Subgroup predictions below 0 s: R1 2, R2 3, S1 7, S1c 6. They come from negative g values.

## Criterion 6

- `reproduce_check.py E052 E051 --champion E046`: RMSE difference 0.0 on every development fold; within tolerance.
- E052's prediction and component files are byte-identical to E051's (component SHA-256s equal, fold by fold).
- E052 reproduces E051's criteria outcomes, including criterion 2's failure.

## Rule 15 (G5)

**(a) The look count.**
- E051 is Day 8–12 look 1 and E052 look 2 (Days 1–7 baseline: 44).
- No other Day 8–12 analysis has read a validation-month target.

**(b) The margin against the draw spread.**
- The candidate is exactly E046 off the subgroup, and the subgroup spread is 0.
- E033's all-rows draw spread is R1 0.48, R2 0.25, R3 0.09, S1 0.27, W1 0.60, S1c 0.34, W1c 1.35 s. Every |ΔRMSE| above is larger than the spread on its fold.
- Even the smallest, R2's +1.39 s and R1's −3.88 s, are about 6 and 8 times their folds' spreads.

**(c) The footprint:** as H038 v2 § Rule 15 (c), with D8-C7 to D8-C9.

## Pre-registered expectations against the outcome

| Reading | Expected (P) | Outcome |
|---|---|---|
| Mixture check PASS | 0.95 | PASS |
| E052 byte-identical | 0.95 | yes |
| Development mean < 0 | 0.65 | yes (−20.10) |
| Criteria 1–3 | 0.35 | **no** (criterion 2) |
| S1 WIN | 0.5 | no (TIE, −7.94) |
| At least one development LOSS | 0.3 | no |
| Reading (a) | 0.65 | holds |
| Criterion 8 | 0.85 | holds |
| Classifier beats constant p on ≥ 3/5 | 0.3 | **yes (5/5)** |

The researcher's misses:
- **R2 gained nothing** (+1.39 s, against −5 to −13 central).
- **W1 was decided by its one row,** as stated: p ≈ 0.88 there, so the prediction was 115,037 s against y = 131,167 s.
- **The classifier was much better on the development folds than in the pilot.**

## Reading

- **The structure helps on average,** but criterion 2 needs fold-level WINs, and the subgroup's few rows rarely produce them.
- Only R3 wins, and on its known rows. Its gain is mostly not the convention.
- With the known rows removed, R1 and S1 look better (both WINs). Under the frozen rules, that cannot be credited.
- **No further variant is proposed here.** Any follow-up is a new proposal at the phase close's discretion.
- **The champion stays E046.**
