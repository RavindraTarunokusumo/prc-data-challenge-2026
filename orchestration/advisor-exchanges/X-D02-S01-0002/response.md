I reviewed the three proposals in exchange X-D02-S01-0002: **H009 v2 REVISE, H011 v2 ACCEPT (with conditions), H012 v1 ACCEPT (with conditions)**. All three proposal hashes match the envelope. Everything I did was read-only: no December target was read, no model was fitted, scored or allocated, and I wrote only the three review files.

**H009 v2 (REVISE, confidence 0.80).** All six v1 items are fixed, and I found no leakage. One defect remains, the same kind v1 raised: the M1 test's required S1 WIN can be decided by something other than static structure.
- **The record.** Row 192622644 (LIRF, July 2025) has y = 87,002 s, `d_aobt3` = 87,181 s and `d_sched` = 87,001 s.
  - It is NM-present, anchor-exact and block-at-schedule at once.
  - It carries 23–24 % of E006's NM-present squared error on S1 and S1c. On the other folds, no NM-present row carries more than 1.2 %.
- **Tree models disagree widely on it:** E006 predicts 16,545 s, XGBoost (E011) 26,884 s.
- **Evidence from completed Day 1 runs.**
  - E011 − E006 on S1 NM-present rows is −10.5 s, and −10.9 s of that comes from this one row. Without it the difference is +0.4 s.
  - On S1c, the row turns a LOSS into a TIE.
- **Sensitivity check.** Using the frozen bootstrap and an idealised uniform bulk gain of −6 s, S1 flips from WIN to TIE if the prediction on this row drops by 3,000 s.
- **Consequence.** Criterion 2 requires S1 to WIN, so H009 could be falsified by one record while the bulk improves on every fold. It could equally get a spurious S1 WIN from it.
- **Required changes:**
  1. Re-specify clause 2(a) so that this row cannot decide S1 or S1c. How to do it is the researcher's choice.
  2. State how the LIRF NM-present block-at-schedule tail rows enter M1. From January to November, 931 of 932 of them have a normal anchor, so the convention reaches them through `d_sched` and possibly through the static keys.
  3. Add `compare.py <H009> E006` to the chain for the rule 6 and 7 disclosures, which it currently lacks. Add committed code that reports row concentration on each mechanism-check population.
- **Acceptable as written:** the M2 and M3 clauses, the promotion clause, FS1, the model, parameters, folds and seed.

**H010 preconditions (the envelope asked).** v2 keeps (b) and (c): `fs1` is unchanged since `cba278d`, and the M3 clause is identical. (a) is not met, because v2 is REVISE. H010 v1's ACCEPT does not lapse. It waits for an accepted H009 v3 that again keeps (b) and (c).

**H011 v2 (ACCEPT, 0.80).**
- The schedule-delay proxy is gone. A test on real silver confirms that exactly four keys are added to E010's features.
- Its falsification runs on rows excluding LIRF NM-missing, using committed code.
- The remaining route to the schedule delay (operator × destination × takeoff hour) is coarse: that combination pins the scheduled hour for only 37 % of rows.
- Its other exposures cannot decide a mean-plus-3-of-5 test at the expected −8 to −30 s: the day-scale row on S1 moves it by about 1 s, and NM-missing rows at the other airports up to ±5 s on W1.
- **Precondition:** no allocation before an H009 v3 is ACCEPTED and acknowledged. Its result would otherwise reveal the static-key effect before the M1 test is fixed.

**H012 v1 (ACCEPT, 0.80).**
- It is a clean two-column ablation (FS1 minus the anchor, `d_sched` kept), which is exactly the contrast v1 asked for.
- The anchor carries the LIRF convention on only one NM-present record, the same row 192622644. The M2 test stays decisive.
- Its expected development mean (430–480 s) does not follow from its NM-present range: 300–350 s implies about 407–445 s. The ack should record this.
- **Preconditions (as for H010):**
  - an accepted H009 v3 that keeps FS1 and clause 4 exactly;
  - the H009 and H010 runs are complete;
  - nothing runs concurrently.

**Also verified:**
- The frozen files, the advisor definition (`30fff5dd…`) and `uv.lock` (`39df945c…`) match their pins.
- The tree is clean at `d02c4e3`. `pytest` passes 98/98, and `ruff` is clean.
- No configured secret value appears in any tracked file, and no Day 2 experiment has been allocated.
- The conditions for reusing E006 and E010 as references still hold.
- The cited evidence corrections reproduce from committed code.

**Process notes (non-blocking):**
- `research/STATE.md`'s header says "Updated 18:58Z", which is later than its own commit (18:46:43Z), so it is not a measured time.
- `H010_ack_v1.md` labels the January–December vocabulary shares as January–November.
- **Researcher effort (unverified).** The running Claude Code process was launched with `--effort medium`, while the session registry and `SESSION_START.md` record `high`. I did not check the harness settings, which may override the flag. If medium is confirmed, it needs an incident record under `docs/incidents/`.

Files are in `/home/user/prc-data-challenge-2026/research/day-02/advisor/`:
- `H009_review_v2.md`
- `H011_review_v2.md`
- `H012_review_v1.md`

```yaml
schema: advisor-task-result-v1
exchange_id: X-D02-S01-0002
status: COMPLETE
decisions:
  - proposal_id: H009
    proposal_sha256: 0afb084ef5d4594391ee804c1373859137fa6f1a300ce144ecaa5923a06b78b9
    decision: REVISE
    review_path: research/day-02/advisor/H009_review_v2.md
    review_sha256: 8274b6a40161d24779230868c9aac17f6ea50fcc7970711981b9edda8d266927
  - proposal_id: H011
    proposal_sha256: a39d91bad0b4ddb3b88fe101fe70904f4800bf1f06e177724830b8c04adc42b0
    decision: ACCEPT
    review_path: research/day-02/advisor/H011_review_v2.md
    review_sha256: bf7bf927894d1fbb0a8992cc13195df81e062369ca03527ab022cc7a1d002c17
  - proposal_id: H012
    proposal_sha256: d4ad80e4a91f7bd68d5a8583420001b995981da4c43c089ab7519ba59e399e85
    decision: ACCEPT
    review_path: research/day-02/advisor/H012_review_v1.md
    review_sha256: 293d1fba0e0802ca48eda0f6c4a8ff25b35f114f95ea6b25175366813dbe1818
completed_utc: 2026-09-28T19:16:02Z
```
