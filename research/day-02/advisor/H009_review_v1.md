---
schema: advisor-review-v1
hypothesis_id: H009
proposal_version: 1
proposal_sha256: c5927ce1c589a0b85c50331ab11e3396ca6e552c2c72cb7dc1e219349af2242d
exchange_id: X-D02-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.85
created_utc: 2026-09-28T18:43:40Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE.**

**The candidate itself is sound.**
- It is LightGBM with H006's fixed configuration, on FS1: FS0 plus four row-own categoricals and the local scheduled hour and weekday.
- The rare-level collapse is fold-local and count-only, and there is no search.
- I found no leakage.
- M3 is pre-registered as standing rule 8 requires (label T, recording convention, separate tail, bulk and S1 expectations). That is the path X-D01-S01-0004 set.

**Two of the three criterion-4 clauses are not decisive about the mechanism they name.** A pre-registered clause cannot be repaired after the runs, so these need a new version.
1. **M1, clause 2(a)** (criterion 1 against E006, full population) can be decided by the LIRF NM-missing subgroup rather than by static structure.
   - That subgroup is under 1 % of rows but carries **0.18–0.56 of E006's own SSE** on the development folds (0.58 on S1c).
   - The proposal expects H009 to change it by up to ±15 % ("M3 changes little"). A ±15 % change alone moves the fold RMSE by **±3.7 to ±22.5 s** (S1c ±24 s).
   - The expected M1 effect is −5 to −25 s, so the clause cannot separate the two.
2. **M2** (H009 against H011, criteria 1–2) removes `d_sched` together with the anchor. X-D01-S01-0004 raised exactly this confound against H008.
   - By the batch's own numbers, removing `d_sched` alone (H010) costs 23–85 s of development mean.
   - The clause therefore passes whether or not the anchor correction exists.

**Also.**
- FS1 contains a route to `d_sched` that bypasses the `d_sched` column: the takeoff hour and weekday (T) against the scheduled local hour and weekday (P). The M3 clause and H011 do not account for it.
- Several evidence statements are wrong (details under Validation Quality).

**Envelope rulings (Validation Quality):**
- Reusing E006 and E010 as ablation references is **permitted**, with conditions.
- The EDA target-hygiene claim **holds in substance**.

**Verified here.** All checks were read-only: no December target was read, no model was fitted or scored, and nothing was allocated.
- **Hashes.**
  - All three proposal hashes match the envelope.
  - The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json`.
  - `.claude/agents/advisor.md` matches `config/agents.yaml` (`30fff5dd…`).
  - The tree is clean at `55429aa`.
- **Tests and lint.** `pytest` passes 96/96 (the Day 1 90 plus 6 new), and `ruff` is clean.
- **Code.**
  - `fs1` joins the row-own keys 1:1 on `MVT_ID_mvt`.
  - `collapse_rare` counts only `role == 'train'` rows and never touches `y`.
  - `gbm._frames` builds category vocabularies from training rows.
  - The `fs0` function is unchanged since `866b902`. Later commits changed the module docstring, added the FS1 functions and extended `columns()`, which still returns FS0's order for FS0 frames.
- **Rule 7 instrument.** `prc.attribution.subgroup_disclosure` reproduces the X-D01-S01-0004 figures for E006 against E005 exactly:
  - NM-present bulk dRMSE: −32.9, −32.0, −39.3, −31.4, −40.2, −31.6, −17.2 s;
  - LIRF NM-missing bulk rows: 94, 58, 16, 218, 14, 218, 14;
  - their dRMSE: +5,514, +3,591, +1,985, +5,782, +2,761, +6,229, +2,343 s.
- **Secrets.** No configured secret value appears in any of the 241 tracked files.
- **State.** No Day 2 experiment is allocated, and there has been no Day 2 holdout access.

## Scientific Validity

**M1 (static structure).**
- The mechanism is plausible, and the EDA supports it in the bulk against the airport median.
- On NM-present rows the anchor `MVT − AOBT_3` already measures the realised taxi, stand-to-runway distance included. There the static keys can only correct the anchor's error and bias (for example operator-specific `AOBT_3` reporting) and the part of taxi time the trees do not yet explain.
- The relevant prior is the EDA's anchor-residual column: 4.8–14.6 s per key, with the keys correlated. It should shrink on E006's much better residual.

**M3 (recording convention).**
- The L2 mixture argument is right, and M3 is admissible (label T).
- **The EDA §5 "0 %" bin is definitional.** A convention-tail row needs y ≥ 3,600 s and |y − `d_sched`| < 120 s, which forces `d_sched` > 3,480 s. The 0 % for `d_sched` ≤ 1 h is therefore guaranteed, not observed. The informative contrast is 1–2 h (0.43) against more than 2 h (0.70).
  - Recomputed on FIT months: n = 473, rate 0.499, bins 0.000 / 0.433 / 0.697 (n = 47 / 231 / 195).
  - The ≤ 1 h bin still has a tail rate of 0.36.
- **FS1 carries a schedule-delay proxy that bypasses `d_sched`.**
  - FS1 keeps `hour_utc` and `weekday` (takeoff, T) and adds `sched_hour_local` and `sched_weekday_local` (P).
  - Trees can therefore form (`hour_utc` − `sched_hour_local`) mod 24, which is the delay at hour resolution offset by the UTC+1/+2 zone, plus a day-crossing bit.
  - Descriptive check: shrunken cell means fitted on FIT months and evaluated out of time on August, LIRF NM-missing rows (197 August rows).

    | Proxy bin: (`hour_utc` − `sched_hour_local`) mod 24 | 0 | 1 | 2–3 | 4–12 | 13–23 |
    |---|---|---|---|---|---|
    | Rows (FIT) | 177 | 99 | 42 | 15 | 140 |
    | Convention-tail rate | 0.50 | 0.69 | 0.69 | 1.00 | 0.25 |
    | Mean y (s) | 4,057 | 6,482 | 11,820 | 30,703 | 5,636 |

  - Out-of-time RMSE: 9,289 s for a constant, **8,855 s with the proxy**, and 8,758 s with exact `d_sched` in 1-hour bins.
  - Either key alone gives only 9,213 or 9,232 s, so the gain comes from the interaction.
  - On NM-present LIRF rows the proxy does nothing (613 → 608 s).
  - Consequence: H010 (FS1 minus `d_sched`) keeps part of M3's channel. Clause 3 measures what exact `d_sched` adds beyond that proxy.

**Criterion 8 and the LIRF bulk trade** (X-D01-S01-0004 called E006's pooled LIRF bulk +210.9 s an unresolved objection). This proposal turns the objection into a disclosed, pre-registered trade. For an accepted H009 version I will treat it as resolved if both of the following hold:
1. the M3 clause holds;
2. the LIRF NM-missing bulk dRMSE against E005 does not exceed the pre-registered upper bound (+6,500 s) on any development fold.

Otherwise it remains unresolved under criterion 8.

**Implementation note (non-blocking).** LightGBM 4.7.0 lumps rare categories itself.
- Test: a synthetic 1,316-level categorical over 1.5 M rows, at least 100 rows per level.
- It kept 1,150 bins with the default 200,000-row bin-construction sample.
- Levels beyond about 99 % cumulative coverage (about 1 % of rows) share the "other" bin.
- So the model's effective stand vocabulary is smaller than FS1's. The 100-row threshold is not what fixes it. There is no leakage consequence.

## Novelty Relative to Existing Research

- **Not redundant.**
  - FS0 has none of the six keys.
  - H006 is INCONCLUSIVE and H007 is REJECT; no earlier hypothesis tests static keys.
  - The proposal answers brief §11 Day 2 and DAY_SUMMARY open questions 1 and 4.
- **Not a retroactive promotion of E006.** The M3 pre-registration is the Day 2 path that X-D01-S01-0004 asked for. It stays non-retroactive only if the promotion rests on the Day 2 run and on clauses that can fail.

## Experimental Isolation

| Contrast | What changes | What it can attribute | Defect |
|---|---|---|---|
| H009 − E006 (M1) | + 6 keys | Static structure on NM-present rows; re-routing of convention rows at LIRF | Clause 2(a) is on the full population. The LIRF NM-missing swing is ±3.7 to ±22.5 s per fold |
| H009 − H011 (M2) | − `d_aobt3`, `d_eobt1`, `d_sched`, `flt_missing` | Anchor and convention **jointly** | Cannot isolate the anchor (the H008 confound). Passes on `d_sched` alone |
| H009 − H010 (M3) | − `d_sched` | Exact `d_sched` beyond the hour-resolution proxy | A lower bound on M3. Stated in H010, but not in H009's M3 clause |

**Wrong contrast in Alternative Explanations.** Alternative Explanation 2 says H009 − H010 would show whether `op_prefix` and `ades` identify convention rows. It cannot: both models contain both keys. The contrast that can is H009 − E006 on the LIRF NM-missing subgroup.

## Validation Quality

**Folds and chain.**
- The frozen folds are used unchanged: seven scored folds plus H, with H predicted only. S1 is a required WIN.
- B1–B4 apply, and B3 is adopted.
- Twin signs are pre-registered: against E006, S1c < 0 and W1c ≤ 0; against E005, < 0 on both twins.

**Ruling on reusing E006 and E010 (envelope request).** **Permitted** as criterion-4 ablation references. No Day 2 re-run of FS0 is required.
- **Standing rule 3** governs the promoted candidate and its reproduction, which must be allocated from Day 2 proposals.
  - The incumbent (E005) and the ablation references may come from earlier phases.
  - The phase-close check takes its phase from the candidate's `gate.json`, so reuse cannot cause a refused or skipped check.
- **Environment identity (verified).**
  - `uv.lock` has SHA-256 `39df945c…`, equal to `uv_lock_sha256` in both E006's and E010's `gate.json`.
  - `src/prc/models/gbm.py` and the `fs0` function are unchanged since `866b902`. E006 and E010 were allocated after that commit.
  - Silver is pinned (`efde4262…`).
  - `compare.py` re-verifies both experiments' prediction hashes against their manifests.
- **Conditions.**
  1. The reuse lapses if `uv.lock`, `gbm.py`, the FS0 code path or silver changes before the H009 primary run. The analysis must record that H009's `gate.json` `uv_lock_sha256` equals `39df945c…`.
  2. **Correct the determinism evidence.**
     - E007–E009 reproduce E002, E003 and E005 (Tier 0 and ridge, whose `sparse_cg` ignores the seed), so they are not evidence for LightGBM.
     - E006 has no reproduction.
     - E006 and E010 ran with `git_dirty_at_run: true`.
     - The residual risk is small next to the pre-registered contrasts (≥ 5 s). H009's own seed-43 reproduction will give the seed scale for this model family.

**EDA target hygiene (envelope request).** **The claim holds in substance.** No EDA statistic uses a target from February, July, September–November or December.
- `eda_day2.py` reads `TAXITIME_SEC_mvt` only after filtering to FIT (January, March–June) and EVAL (August).
- Its vocabulary frame selects no target column, ranking DEP targets are blank, and December is masked.
- EDA finding 5 is not produced by the script, but it **reproduces exactly from FIT months**: n = 473, rate 0.499, bins 0.000 / 0.433 / 0.697, and RYR with 68 rows at 0.46.

**Record defects in the EDA and the proposal:**
- **(a) Ranking coverage is an artifact.**
  - The vocabulary frame spans every DEP row in silver, from January 2025 to July 2026, including December and both ranking months. "Levels (Jan–Nov)" are therefore all-silver counts (stand 1,930; in January–November it is 1,895).
  - The ranking-unseen shares are 0 by construction, so "every new key has 0 % unseen levels" (Observation 1, Competition Availability) is false.
  - True shares against the January–December 2025 vocabulary, consistent with frozen audit §5:

    | Key | Ranking DEP rows unseen | July 2026 only |
    |---|---|---|
    | `stand` | 0.082 % | 0.133 % |
    | `actype` | 0.005 % | |
    | `op_prefix` | 0.262 % | 0.434 % |
    | `ades` | 0.051 % | |

  - The conclusion survives, because unseen levels map to `__RARE__`.
- **(b) The NM-missing count has the wrong scope.** "27,760 NM-missing rows in Jan–Nov" is the all-silver count.
  - January–November has 20,821 (1.085 %).
  - The quoted presence shares are also all-silver. For January–November they are: flight 99.74 %, destination 99.82 %, stand 99.95 %, type 93.19 %.
- **(c) Producing code is missing.** The code behind finding 5 and the FS1 build check is not committed (the Day 1 C7 precedent). The build check materialises S1's training targets, September–November included, but reports only target-free quantities.

**Is each falsification clause decisive?**

| Clause | Verdict |
|---|---|
| 1 | Decisive |
| 2(b) | On the right population |
| 2(a) | Not insulated from the LIRF NM-missing subgroup |
| M2 | Not decisive |
| 3 | Decisive for exact `d_sched` beyond the proxy, but few rows decide it (rule 6): 14–218 bulk and 36–119 tail LIRF NM-missing rows per fold |

**Tooling gap.**
- The pre-registered "share of SSE change carried by LIRF NM-missing tail rows" is not produced by `compare.py` or `prc.attribution`, which report whole-subgroup shares.
- E006's cited 0.40–1.04 are tail-row shares. The tool's whole-subgroup shares for E006 − E005 are 0.18–0.77.

## Leakage Review

### Target Leakage

PASS

- No target statistics are used.
- The rare collapse counts training rows only, and the vocabularies come from training rows.
- Validation `y` is null (tested on real silver, R1 and W1c).
- There is no early stopping.

### Temporal Leakage

CONCERN

Every input is admissible under §6.2. The concerns are about labels, not admissibility.
- **Stand (P holds on target-free evidence).**
  - No DEP stand with at least 100 rows has 80 % or more of its rows in December–February or January 2026.
  - There are no de-icing-like stand names.
  - Null share is ≤ 0.01 % at every airport.
- **Destination (partly F).**
  - For 641 of 2,070 diverted NM-matched flights, `ADES_mvt` equals the flown destination rather than the filed one, which is label F. That is about 0.03 % of DEP rows.
  - 2,193 rows have `ADES_mvt` = `ADEP_mvt`.
  - Label `ades` "P, with an F exception for diversions" for the Days 5–7 causal-only variant.
- **Operator prefix.**
  - 78 % of callsigns are ICAO-style. 21 % are IATA-style (`KL1`, `CZ4`), where the prefix mixes the carrier with the first digit of the flight number.
  - `AIRCRAFT_OPERATOR_flt` is a hashed code, so `op_prefix` is the only readable operator key.
  - The §6.2 identifier exclusion is not engaged.
- **Schedule-delay proxy.** The T × P proxy takes label T by precedence. It matters for M3 attribution and for the causal-only variant.

### Competition Availability

PASS

- Every input is present for ranking DEP rows.
- `SCHED_TIME_UTC_mvt` has 0 nulls across all 2,429,888 DEP rows.
- Unseen levels are 0.005–0.26 % (0.43 % for `op_prefix` in July 2026) and map to `__RARE__`.
- LIRF NM-missing DEP rows: 107 in January 2026 and 276 in July 2026.

## Compute Review

### RAM

PASS

- E006 peaked at 3.74 GB, and the FS1 build at 3.1 GB on S1.
- Fold H is about 21 % larger; its FS0 build measured 3.45 GB.
- Expect about 4–5 GB, inside CLASS-M (8 GB).

### Runtime

PASS

- E006 took 676 s, with R3 contended.
- With 17 features against 11, plus the categorical split search, expect 11–18 minutes.
- The timeout is 45 minutes. The reproduction costs the same again.

### Disk

PASS

About 10 MB of predictions, covered by the manifest.

## Weakest Assumption

**The assumption.** The full-population contrast H009 − E006 measures static structure.

**Why it fails.**
- Fewer than 1 % of rows (LIRF NM-missing) carry 18–56 % of E006's SSE on the development folds (58 % on S1c).
- The convention records in that subgroup are reached through `d_sched`, through the FS1 proxy, and plausibly through `op_prefix` and `ades`.
- Any re-routing of those rows shows up at the same scale as M1.

## Missing Control or Ablation

- **M1** needs a test insulated from the LIRF NM-missing subgroup.
- **M2** needs a contrast that holds `d_sched` fixed. The batch already contains a pair of runs with `d_sched` absent on both sides. Which contrast and which population to use is the researcher's choice.
- **M3** has no ablation that removes the convention channel entirely (`d_sched` and the proxy). This is not required if clause 3 is interpreted as stated in Revision item 3.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- No FS1-family run (H009, H010 or H011) may be allocated before an H009 version ≥ 2 is ACCEPTED and acknowledged. Any earlier FS1 outcome would reveal the M1 result before its clause is fixed.

Required acknowledgement path: none for v1. Submit `research/day-02/proposals/H009_v2.md` in a new exchange.

## Revision

**Required (minimal):**
1. **M1.** Replace or supplement clause 2(a) with a pre-registered test whose outcome the LIRF NM-missing subgroup cannot decide. The population and statistic are the researcher's choice. Keep clause 2(b).
2. **M2.** Re-specify it so that the contrast holds `d_sched` fixed, and state the population. A contrast that also removes `d_sched` cannot attribute a gain to the anchor.
3. **M3.**
   - State that FS1 without `d_sched` keeps the hour-resolution schedule-delay proxy.
   - State that clause 3 therefore tests exact `d_sched` beyond that proxy, and that a failed clause 3 does not show the convention is absent.
   - Correct Alternative Explanation 2: the relevant contrast is against E006.
4. **Code before the first FS1-family run.**
   - Every pre-registered quantity must be computable by committed code. That includes the LIRF NM-missing tail-row share and the tests from items 1–2.
   - Commit the producing code of EDA finding 5 and of the FS1 build check.
5. **Evidence corrections in v2.**
   - (a) The ranking-unseen shares above.
   - (b) The January–November NM-missing count (20,821) and the scope of the presence shares.
   - (c) The definitional ≤ 1 h 0 %.
   - (d) E007–E009 are not LightGBM.
   - (e) The `ades` label exception.
   - (f) `created_utc` 18:24:00Z postdates both the commit (18:22:24Z) and the envelope (18:22:07Z), so it is not a measured time.
6. **Implementation Plan.** Make the seed-43 reproduction conditional on passing criteria 1–3 against E005 without being falsified, as H006's authorization did.

**Acceptable as is:** FS1, the model, parameters, folds, seed and class; the rule 8 pre-registration of M3; the twin expectations.

**Process.** `research/STATE.md` is stale again. Last written at `11b3474`, it still shows the Day 1 holdout check as pending. Refresh it before the first Day 2 allocation.

## Advisor Prediction

Probability of improvement, for the v1 configuration (features and model unchanged):

| Event | P |
|---|---|
| Passes criteria 1–3 against E005 | 0.93 |
| NM-present bulk dRMSE against E006 < 0 on ≥ 4 of 5 development folds | 0.85 |
| Criterion 1 against E006, full population | 0.60 |
| H009 − H010 < 0 on the LIRF NM-missing subgroup on ≥ 3 of 5 folds | 0.80 |
| H009 against H011 passes criteria 1–2 (the M2 clause as written) | 0.98 |

Expected magnitude:

| Quantity | Expected |
|---|---|
| Development mean | 360–380 s |
| NM-present bulk dRMSE against E006 | −3 to −12 s per fold |
| Full-population dRMSE against E006 | −2 to −15 s mean, with swings of ±10–20 s per fold from the LIRF NM-missing subgroup (largest on S1 and S1c) |

Primary expected failure mode:
- The M1 margin is carried or cancelled by LIRF NM-missing tail rows rather than by static structure.
- Secondary: W1c, trained on January alone, comes out TIE against E006 because of the high-cardinality categoricals.
