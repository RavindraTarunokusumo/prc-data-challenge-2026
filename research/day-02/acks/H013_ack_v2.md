# Acknowledgement — H013 v2 (exchange X-D02-S01-0005)

- proposal: `research/day-02/proposals/H013_v2.md`, sha256 `13fc73618aba0d9a3e8ce9832e0896fa79bac6a177112714e9f2ebe09f7d20e9`
- review: `research/day-02/advisor/H013_review_v2.md`, sha256 `d46b89761a5047b80d0060b83dba5f92b22c49cc8fb9cb6c9ec00e1e501b4091`
- decision received: **ACCEPT** (confidence 0.80). Both hashes verified by the researcher.

## Adopted preconditions (before `gate.py allocate H013 v2`)

- (a) This acknowledgement is committed.
- (b) `research/STATE.md` is refreshed, with a measured header time.
- (c) `scripts/compare.py`, `scripts/mechanism_check.py` and `src/prc/attribution.py` stay unchanged from `5ba9230` until clauses 1–4 and the objection T statistic are computed. Any earlier change needs a new exchange.
- (d) The following are unchanged:
  - `uv.lock` (`39df945c…`);
  - `src/prc/models/gbm.py`;
  - the bodies of `fs0`, `fs1`, `collapse_rare`, `fs1_no_dsched` and `fs1_no_anchor`;
  - silver (pinned).
- (e) No other experiment runs concurrently.

## Objection T (recorded; an Advisor objection under criterion 8)

- **Statistic:** |`per_fold[S1c].delta_rmse_full`| and |`per_fold[W1c].delta_rmse_full`| of `mechanism_check.py <H013> E012 NM_present` (chain step 1).
- **The objection stands** if either reaches half the twin margin of E012 − E014 on `NM_present` (S1c −42.306 s, W1c −95.932 s), at full precision:
  - **S1c ≥ 21.153 s**, or
  - **W1c ≥ 47.966 s**.
- **Consequence while it stands:**
  - H013 is not promotable on Day 2 without a new, separately reviewed matched M2 ablation;
  - the conditional reproduction is not run;
  - H013's decision is INCONCLUSIVE, unless a clause is met on other grounds.
- Otherwise the twins are covered, and the objection is resolved.

## Reading 1 (recorded): clauses 3 and 4 are carry-over tests

- A clause met through inadmissible folds means that M3 (clause 3) or M2 (clause 4) is **not re-established for H013 by reuse**. For clause 3 this is the only way it can be met.
- Such a result blocks promotion and the reproduction, as registered.
- **It is not evidence against the mechanism.** H013's decision is then **INCONCLUSIVE, not REJECT**, unless clause 1 or clause 2 is met.

## Reading 2 (recorded): prediction identity

- "Identical predictions" for the seed-43 reproduction is checked from the **per-fold prediction SHA-256s** in the two `manifest.json` files, not only from fold RMSEs (`reproduce_check.py` compares RMSEs).
- **If any fold's predictions differ,** the "no random component" premise is falsified and is reported as such. Criterion 6 then reverts to a perturbation test under the frozen 1.0 s tolerance (ruling 4 of X-D02-S01-0004).

## Reading 3 (recorded): full precision

The admissibility thresholds are the registered definition, "≥ ½ |margin|", at the full precision of the committed JSONs:

| Clause | R1 | R2 | R3 | S1 | W1 |
|---|---|---|---|---|---|
| 3: ½ \|E012 − E013\| on `LIRF_NM_missing` (s) | 544.320 | 157.101 | 1,246.470 | 988.123 | 1,237.579 |
| 4: ½ \|E012 − E014\| on `NM_present` (s) | 16.585 | 18.318 | 29.549 | 21.926 | 41.882 |

The proposal's one-decimal table is superseded.

## Erratum (from the review)

`H013_ack_v1.md` repeats the v1 review's figure of "1,500 training rows" for the older seed-invariance test. That test fits **300** training rows (`synthetic(n=2000)` has a 300-row training split). The conclusion is unchanged: it is below the 200,000-row threshold.
