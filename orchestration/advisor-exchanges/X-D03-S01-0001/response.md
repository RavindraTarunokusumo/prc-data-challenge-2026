# Advisor response — X-D03-S01-0001 (attempt 2)

Final message of the `advisor` subagent, mirrored verbatim below the rule. No secrets present.

---

I've written the three reviews. **All three proposals are REVISE, and nothing is authorized to run.**

**Decisions**
- **H015 v1: REVISE** (confidence 0.88). The overall design is sound: C is tested against the matched reference E017, and H016 isolates the routing exactly. No feature reads a DEP block time or target. Routing the LIRF NM-missing rows to E005's model class is the kind of fix ruling B allows. Two defects block it.
  1. **The routing's forward-risk figures are false.** The proposal says LIRF NM-missing rows ran "52–115 in Jan–Nov 2025" and that July 2026's 276 is "2.4 to 5.3 times any 2025 month".
     - Silver, a target-free count, gives 185, **337**, 197 and 168 for June–September 2025. So July 2025 had more such rows than July 2026.
     - The Day 1 phase-close review already recorded July's 337, and H015 itself cites "S1's 337 subgroup rows".
     - What survives is that the 2026 rate cannot be estimated, which is still an admissible reason under ruling B. The claim of an unprecedented count does not.
  2. **One known record can decide the congestion test on S1 (clause 2).** This is the same defect that made H009 v2 REVISE.
     - Row 192622644 (S1, LIRF, NM-present, target 87,002 s) sits inside the clause 2 population.
     - In all four Day 2 Tier 1 contrasts on that population, this one row carried at least half the size of S1's net change.
     - E017 − E018 on S1 is +1.59 s with the row and −18.50 s without it. My derivation reproduces a committed comparison file to within 0.001 s on all seven folds.
     - FS2 makes the row more extreme: its in-taxi counts are 486, 466 and 473, against a fold q99 of 33. Only 4 NM-present training rows exceed 100.
  - **Three smaller defects:**
    - The noise scale is quoted on the wrong population. On the clause population, E018 − E006 is −5.73 s on S1, the size of the −6.0 s floor, and all of it comes from that row.
    - Five of the ten "P" features read the row's own takeoff time when it takes off before its off-block proxy. That affects 2,091 DEP rows (0.086 %); I confirmed it with a synthetic check. The information is already in FS1, so no contrast is confounded, but the leakage section and the `congestion.py` docstring are wrong.
    - Clause 3 does not say what its failure means for H015's decision.
- **H016 v1: REVISE** (confidence 0.80). Its content is sound, but it is tied to H015 v1. Outside the routed rows its predictions are identical to H015's, so running it early would reveal H015's congestion result before clause 2 is re-registered. The changes needed are to point it at H015 v2 and to report on H015 v2's clause population.
- **H017 v1: REVISE** (confidence 0.85). Reading 1 (H016 − H017) differs only in the five in-taxi columns, which are exactly this row's extreme inputs. It also carries the same "P" label error and the same coupling to H015.

**What was verified (all read-only or synthetic)**
- All proposal hashes match the envelope. Frozen files, `frozen.json`, `advisor.md`, `uv.lock` and silver hashes are intact.
- The "unchanged since" code claims hold, and the E005, E006, E012, E017 and E018 prediction files match their manifests.
- The routed-E017 margins and the EDA figures reproduce exactly.
- `pytest` passes 113/113 and ruff is clean. No credential value appears in the 394 tracked files, and no December target was read.
- The working tree was clean apart from the three new review files. INC-0004 is noted and does not block this review.

**Authorization:** none. No FS2 or FS2_P model may be fitted on a frozen fold until an H015 version ≥ 2 is accepted and acknowledged. Submit H015_v2, H016_v2 and H017_v2 in a new exchange.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D03-S01-0001
status: COMPLETE
decisions:
  - proposal_id: H015
    proposal_sha256: 2218b3eec778fbd4961c194bf2f0b0db32e31ee0d98efec0b02f7a77bc142334
    decision: REVISE
    review_path: research/day-03/advisor/H015_review_v1.md
    review_sha256: 8c79cfd483fe81c84e62d7f9ffdbe1f365573f0da7346db27999c242c1c57122
  - proposal_id: H016
    proposal_sha256: 604801ba34586a34965db0d669cec12a63c47de590b20a92241b39f8ab17902e
    decision: REVISE
    review_path: research/day-03/advisor/H016_review_v1.md
    review_sha256: ca566a251d16bc5fb56b81a83b29e5c49cd94db0155af98a4b3f9e776fdee45d
  - proposal_id: H017
    proposal_sha256: 4ee136f3117209499f92be160e006a0c8172de80c04a5c515392426f0934b1d7
    decision: REVISE
    review_path: research/day-03/advisor/H017_review_v1.md
    review_sha256: df8433fa7a541ae47ca00327b47b6d8575c98e7e78e4c3f36582003edb345691
completed_utc: 2026-09-29T15:57:15Z
```
