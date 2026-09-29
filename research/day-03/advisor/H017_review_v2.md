---
schema: advisor-review-v1
hypothesis_id: H017
proposal_version: 2
proposal_sha256: 0ab06ef90d017dea8c6cbab4dac6f5bf221a29f9b1a7cf52eb5c31bfff151b83
exchange_id: X-D03-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.85
created_utc: 2026-09-29T16:29:41Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.** H017 v2 runs as H015 v2's chain step 3. It is a reference for decomposing C: not a candidate, not reproduced, and never NEW in a holdout access.

| v1 required revision | Status in v2 | How it was verified |
|---|---|---|
| 1. Readings not decidable by one record; rule 6 pre-registered for reading 1 | **Done** | Both readings are on `NM_present_excl_LIRF`, which excludes row 192622644. The largest in-taxi count in the population is 93–129 per fold, against 486 for that row. The pre-registered S1 and S1c shares (at most 0.052 in the Day 2 real-effect contrasts) match the committed JSONs |
| 2. Noise scale on that population | **Done** | Floor 6.0 s. The largest development-fold shift is 1.957 s (W1, E018 − E006), and W1c +4.93 s enters only through the twin rule. Verified against the committed JSONs |
| 3. P labels | **Done** | The re-implementation is verified by diff, by the tests on the old and new code, by a brute-force real-data recomputation (0 mismatches on 3,262 rows) and by a real-data perturbation (`H015_review_v2.md` (e)). The leakage text and the risk line are corrected. The Days 5–7 claim is bounded correctly |
| 4. Chain | **Done** | Third, after H015 v2 and H016 v2 |

- **The "acceptable as is" items are unchanged** (diff against v1): FS2_P apart from item 3, E017's parameters, the seed, the folds, the role, the noise-floor wording and reading 3.
- **Changed expectations.** P −1 to −4 s; T on top of P −4 to −12 s, with a WIN on at least 3 of 5 folds, S1 included. They were changed before any run, which is permitted.
- **Verified here** (target-free, on real W1c and S1 views): `fs2_p` is exactly `fs2` minus the five T columns. The other checks are in `H015_review_v2.md`.

## Scientific Validity

**Reading 1 is now a test of T, not of one record.**
- The five T columns are the only difference between H016 and H017.
- Inside the population, their largest values come from long NM-present taxis at LTFM, EHAM and EGLL (93–129 takeoffs during taxi).
- The largest top-row change seen on this population (4.5 × 10⁷ s²) moves a fold by about 0.7 s and the five-fold mean by about 0.15 s. Even a change twice that size moves the mean by about 0.3 s at most (`H015_review_v2.md` (a)).

**The "not decisive" rule needs one reading** (for the ack; not a revision).
- The proposal says that if one row carries ≥ 0.5 of a fold's change, "the reading on that fold is reported as not decisive". The consequence for reading 1's support is not stated.
- **The reading I adopt:**
  - a fold reported as not decisive cannot count toward "supported";
  - if S1, the required WIN, is such a fold, reading 1 is recorded as "not decisive (not supported)";
  - the frozen outputs (fold outcomes, criteria 1–2) are reported unchanged (B4).

**Reading 2 will probably show dominant rows. This is expected, not a defect.**
- The P effect is expected below the floor.
- In the three noise contrasts on this population, whose development-fold net changes are all within ±2 s, 7 of the 15 cells have |top-1| ≥ 0.5.
- Reading 2's pre-registered outcome ("not distinguishable from training noise") is unaffected.

**What the decomposition can say.**
- RMSE differences on identical rows add exactly: (H016 − H017) + (H017 − E017) = H016 − E017 per fold.
- The split is ordered, however. "P without T" (H017 − E017) may credit P with information that T would also carry, and "T given P" may understate T alone. There is no T-only arm.
- The proposal words the readings correctly as "P beyond E017" and "T on top of P".

**The Days 5–7 claim is bounded correctly.**
- H017 estimates the congestion block's P part.
- It does not estimate the causal-only model, because FS1's T inputs (`hour_utc`, `weekday`, the `d_*` deltas) stay in both arms.

**A dependency on H015's clause 3.**
- Reading 1 compares two separate FS2-family processes.
- If `route_check.py` 3(b) fails, so that the determinism premise is recorded as false, reading 1 carries the same cross-process caveat. The record must say so.

## Novelty Relative to Existing Research

- **A P/T decomposition of a congestion block** has no Day 1 or Day 2 counterpart.
- **Standing rule 10 is not engaged.**

## Experimental Isolation

| Reading | Contrast | Only difference | Status |
|---|---|---|---|
| 1: T carries C | H016 − H017 on `NM_present_excl_LIRF` | The five T columns | **Isolated. Not decidable by a known record** |
| 2: P beyond E017 | H017 − E017 on `NM_present_excl_LIRF` | The ten P columns (verified P) | Isolated. The effect is expected below the floor |
| 3: rule 11 | H017 − E017 on all rows | Same | Disclosure |

## Validation Quality

- **Folds.** The frozen folds are used unchanged, and H is predicted only.
- **Status.** H017 is a reference, not reproduced and never NEW.
- **One population per comparison (rule 11).** The three C contrasts of the batch (H015 − E017, H016 − H017, H017 − E017) all use `NM_present_excl_LIRF`, so they can be compared.
- **The noise-floor statement holds.** The mean shifts of the three noise contrasts on this population are −0.24, −0.12 and +0.25 s, against a floor of 6.0 s.

## Leakage Review

### Target Leakage

PASS

- No input reads a DEP block time or target.
- No target statistic is used.

### Temporal Leakage

PASS

**The ten added inputs are P,** verified by code, by test and on real data (`H015_review_v2.md` (e)). The label notes that remain are not blocking:
- the labels are relative to the proxy for *t_off*;
- the runway is P by assumption;
- FS1's inherited T inputs are admissible and unchanged from E017.

### Competition Availability

PASS

Every input is present for ranking DEP rows.

## Compute Review

### RAM

PASS

5–6.5 GB expected.

### Runtime

PASS

14–22 min (27 inputs against E017's 17), within CLASS-M.

### Disk

PASS

About 10 MB of predictions.

## Weakest Assumption

**That the P/T split of C is readable at all.**
- If C itself is about −4 s on this population (`H015_review_v2.md`, Advisor Prediction), both readings fall below the 6.0 s floor. Both are then recorded as "not distinguishable from training noise".
- The decomposition would then say little beyond "most of C, if any, is T".

## Missing Control or Ablation

**None required.**

**Named, not required:** a T-only arm (FS1 plus the five T columns) would make the decomposition symmetric. It is not needed for the pre-registered readings.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Preconditions:** those of `H015_review_v2.md` 1(a)–(d). In addition, H016 v2's primary run and its chain step 2 checks are complete.
2. **One primary run.**
   - `model: lightgbm`, `feature_set: FS2_P`.
   - `params`: E017's exactly (as listed in `H016_review_v2.md`).
   - `folds: [R1, R2, R3, S1, W1, S1c, W1c, H]`, `seed: 42`, `job_class: CLASS-M`.
3. **Comparisons:**
   - `mechanism_check.py <H017> E017 NM_present_excl_LIRF` (reading 2);
   - `mechanism_check.py <H016> <H017> NM_present_excl_LIRF` (reading 1);
   - `compare.py <H017> E017` (reading 3).
4. **Infrastructure failure.** One identical re-run with `--purpose rerun`, logged, only after an infrastructure failure. A RESOURCE_FAILURE or TIMEOUT is recorded and not retried.
5. **Recording:** as in `H015_review_v2.md` item 8.
6. **Not authorized:**
   - a reproduction;
   - any use as a candidate or as NEW;
   - scoring H;
   - any change to features, parameters, folds or seed;
   - any code change during the chain (`H015_review_v2.md` item 9).

Required acknowledgement path: `research/day-03/acks/H017_ack_v2.md`.
- It references the proposal hash (`0ab06ef9…`) and this review's hash.
- It adopts the preconditions and the scope limit.
- It records the "not decisive" reading and the clause 3 dependency under Scientific Validity.

## Revision

None required for this version.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| Reading 2 supported: H017 − E017 mean ≤ −6.0 s with criteria 1–2 on `NM_present_excl_LIRF` | 0.04 |
| H017 − E017 mean within −1 to −4 s | 0.45 |
| H017 − E017 mean above −4 s (including positive) | 0.85 |
| Reading 1 supported: H016 − H017 mean ≤ −6.0 s with criteria 1–2 | 0.20 |
| At least one development-fold cell with \|top-1\| ≥ 0.5 in reading 2 | 0.55 |
| \|top-1\| ≥ 0.5 on S1 or S1c in reading 1 | 0.10 |
| Development mean on all rows within 370–385 s | 0.75 |

Expected magnitude:
- **P** (H017 − E017, clause population): −0.5 to −3 s.
- **T on top of P** (H016 − H017): −1 to −6 s.
- **Development mean on all rows:** 372–383 s.

Primary expected failure mode:
- Both readings come back "not distinguishable from training noise". The anchor and the other `d_*` deltas already carry most of what either block adds, and the part of C that is T lands below the 6.0 s floor.
