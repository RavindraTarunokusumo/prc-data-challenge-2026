---
schema: advisor-review-v1
hypothesis_id: H017
proposal_version: 1
proposal_sha256: 4ee136f3117209499f92be160e006a0c8172de80c04a5c515392426f0934b1d7
exchange_id: X-D03-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.85
created_utc: 2026-09-29T15:53:21Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE.**

**What is right.**
- Splitting C into what is known at pushback (P) and what is observed during the taxi (T) is the right question for Days 5–7.
- The proposal bounds its claim correctly: FS1's own T inputs remain, so H017 is not the causal-only variant.
- The noise-floor handling is good: a P effect below the floor is recorded as "not distinguishable from training noise", not as "no P effect".

**Three defects.**
1. **Reading 1 is the contrast in this batch most exposed to row 192622644.**
   - H016 − H017 differs only by the five T columns, and on that row they take the most extreme values in S1's view: 486, 466 and 473 against a q99 of 33.
   - On `excl_LIRF_NM_missing`, this row's signed share of S1's change had magnitude ≥ 0.5 in all four Day 2 Tier 1 contrasts (`H015_review_v1.md` (c)).
   - As written, reading 1's required S1 WIN is a test of one record.
2. **The leakage section's "the added inputs are P" is false for five of the ten.** They read the row's own takeoff time on rows that take off before their *t_off* proxy (`H015_review_v1.md` (e)).
3. **Coupling.** H017's chain position and populations are H015 v1's and H016 v1's, and both are REVISED.

**Verified here.**
- The proposal hash matches the envelope.
- `fs2_p` is `fs2` minus the five T columns (`features.py`; `tests/test_features_fs2.py`).
- The EDA's P figures match `congestion.json`: 0.3–1.7 s after the anchor, and 0.9–9.3 s after the airport median.

## Scientific Validity

**The expectation is consistent with the evidence.**
- After the anchor, the P features reduce the EDA residual by 0.3–1.7 s each (univariate, binned).
- "P adds little beyond E017" is therefore the likely outcome.
- Stating that the expected P effect lies below the 6.0 s floor, and is informational, satisfies Missing Control 4 in form.

**The P labels.**
- **What leaks.** The five affected features are `cg_dep_taxiing`, `cg_dep_taxiing_rwy`, `cg_dep_to_p15`, `cg_dep_to_rwy_p15` and `cg_dep_to_p30`. They encode 1{*t_to* ≤ *t_off*} and 1{*t_to* in [*t_off* − 15 or 30 min, *t_off*)} on 2,091 DEP rows (0.086 %). Of those, 856 are NM-missing (3.1 % of NM-missing rows), and there are 119 and 168 in the two ranking months.
- **H017 − E017 is not confounded.** Those bits are functions of `flt_missing`, `d_aobt3` and `d_sched`, which E017 already has.
- **But the stated purpose does not hold as written.** "tells Days 5–7 how much of the congestion gain survives a causal-only restriction" needs the P block to be P, or the claim narrowed.

**Reading 1's population.**
- Reading 1 needs criteria 1–2 on `excl_LIRF_NM_missing`, S1 WIN included.
- Row 192622644's inputs are exactly what H016 has and H017 lacks, so this contrast inherits H015's defect in its strongest form.
- Reading 2 (H017 − E017) is less exposed, because the row's P values are ordinary (`cg_dep_taxiing` = 6). Any change of tree structure can still move the prediction on it.

## Novelty Relative to Existing Research

- **New:** a P/T decomposition of a congestion block, which has no Day 1 or Day 2 counterpart.
- **Rule 10:** not engaged.

## Experimental Isolation

| Reading | Contrast | Only difference | Status |
|---|---|---|---|
| 1: T carries C | H016 − H017 | The five T columns | Isolated. **Not decisive on S1 and S1c as written** (row 192622644) |
| 2: P beyond E017 | H017 − E017 | The ten P columns (five with T bits on 0.086 % of rows; redundant with FS1) | Isolated in information. The label is wrong |
| 3: rule 11 | H017 − E017, all rows | Same | Disclosure |

## Validation Quality

- **Folds.** The frozen folds are used unchanged, and H is predicted only.
- **Status.** H017 is a reference, not reproduced and never NEW.
- **One population per comparison (rule 11).** Readings 1 and 2 must use the population that H015's revised clause 2 uses. The three C contrasts of the batch (H015 − E017, H016 − H017, H017 − E017) can then be compared.
- **Noise scale on that population.** The floor statement must cite the measured shifts on the chosen population, as in `H015_review_v1.md` Revision 3.
  - On `excl_LIRF_NM_missing`, E018 − E006 is −5.73 s on S1.
  - All of that is row 192622644.

## Leakage Review

### Target Leakage

PASS

No input reads a DEP block time or target, and no target statistic is used.

### Temporal Leakage

CONCERN

- **Five of the ten added inputs** carry the row's own takeoff time on 0.086 % of DEP rows. This is admissible under §6.2, but "low (the added inputs are P)" is not accurate.
- **FS1's own T inputs remain,** as the proposal says.

### Competition Availability

PASS

Every input is present for ranking DEP rows.

## Compute Review

### RAM

PASS

Under 7 GB.

### Runtime

PASS

About 14–22 min.

### Disk

PASS

About 10 MB.

## Weakest Assumption

**That reading 1's S1 outcome measures the T mechanism.** The only inputs that differ are the ones on which row 192622644 is an extreme outlier.

## Missing Control or Ablation

None beyond `H015_review_v1.md`. E017 is the zero-congestion reference, and H016 is the full block.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution.
- No allocation of H017 v1.
- No FS2_P model may be fitted on a frozen fold before an H015 version ≥ 2 is ACCEPTED and acknowledged (`H015_review_v1.md`).

Required acknowledgement path: none for v1. Submit `research/day-03/proposals/H017_v2.md` in the same exchange as H015 v2.

## Revision

**Required (minimal):**
1. **Readings 1 and 2** use the population, statistic or decision rule that H015's revised clause 2 uses, so that no single known record can decide a required fold outcome. Pre-register the expected rule 6 dominant rows for reading 1 on S1 and S1c.
2. **Noise scale.** Restate the floor statement with the measured shifts on that population.
3. **P labels.** Follow H015's choice (relabel or re-implement), and correct the Leakage Analysis and the Temporal Leakage Risk line. If the labels are kept as they are, narrow the claim about what H017 tells the causal-only variant.
4. **Chain.** Re-point to H015 v2 and H016 v2.

**Acceptable as is:**
- FS2_P, apart from item 3;
- E017's parameters, the seed and the folds;
- the role (not a candidate, not reproduced, never NEW);
- the noise-floor wording ("not distinguishable from training noise");
- reading 3.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| H017 − E017 mean ≤ −6.0 s with criteria 1–2 on the clause population (reading 2 supported) | 0.08 |
| H017 − E017 mean within −1 to −5 s | 0.45 |
| H016 − H017 mean ≤ −6.0 s with criteria 1–2 on a population without row 192622644 (reading 1 supported) | 0.25 |
| Row 192622644 carries \|share\| ≥ 0.5 of S1's change in H016 − H017 on `excl_LIRF_NM_missing` (v1 design) | 0.85 |

Expected magnitude:
- **P** (H017 − E017): −0.5 to −4 s.
- **T on top of P** (H016 − H017): −1 to −8 s on the clause population.
- **Development mean on all rows:** 372–385 s.

Primary expected failure mode:
- As written, reading 1 is a test of one record on S1.
- Once that is fixed, both readings come back "not distinguishable from training noise": the anchor and the other `d_*` deltas already carry most of what either block adds.
