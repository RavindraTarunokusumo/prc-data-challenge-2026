---
schema: advisor-review-v1
hypothesis_id: PHASE_CLOSE_D03
proposal_version: 1
proposal_sha256: 20dbd9605d7ae864b8a548cd6b4c064da48578d3c236e47861a58db0de189401
exchange_id: X-D03-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.82
created_utc: 2026-09-30T07:00:14Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT.**
- **E019 (H015 v2) is the Day 3 phase-closing champion,** subject to exactly one protected-holdout access: E019 against E005, with the command named under Execution Authorization.
  - WIN or TIE: the promotion stands.
  - LOSS: it reverts, and E005 stays champion.
- **The access runs only after the acknowledgement is committed.** The acknowledgement:
  - appends record corrections D3-C1 to D3-C9;
  - adopts standing rule 12 (Revision);
  - records the answer on the routing question (Validation Quality, (e)).
- **None of the corrections changes a Day 3 decision.** Three change what Day 3 is recorded as having shown (D3-C1 to D3-C3).

**Attack on the candidate.** As asked, I tried to show that E019 should not replace E005. I could not show that it is worse than E005 on any evidence. What I found is where its advantage comes from, and a new defect whose forward exposure the record understates.

1. **The frozen criteria hold and re-verify.**
   - I re-derived every decisive figure from the prediction files and development-fold truth, and each matches the committed JSONs to 0.01 s:
     - E019 − E005: −38.23 s (q95 −34.95), 7/7 WIN;
     - C: −6.75 s (q95 −5.97), 7/7 WIN;
     - routing integrity: exact on all 8 folds;
     - E022: byte-identical to E019 on all 8 folds.
   - Rule 10 forbids moving a pre-registered floor after the fact, in either direction. So the 0.75 s margin in clause 2(b) stands.
2. **Congestion is about 5 % of the champion's margin.**
   - A routed E017 (E017 with E005's predictions on the routed rows, an exact composition of existing files) is −36.33 s against E005.
   - On all rows, E019 against it is −1.90 s (q95 −0.98), with R1 and R2 TIE. Criterion 3 fails on that contrast: EHAM is +7.2 %.
   - **What is being promoted is the routed Day 2 FS1 structure, gated by a congestion clause measured on a population that excludes the rows where congestion hurts.** (D3-C1)
3. **The congestion block adds out-of-range predictions on NM-missing rows at the nine non-LIRF airports.**
   - These rows show negative taxi times, and convention-scale values above 3,600 s on normal taxis. E005 makes none of either on this group.
   - Congestion causes it. On this group's bulk, E017 beats E005 on all five development folds (pooled −100.4 s). E019 loses on four (pooled +5.25 s).
   - The out-of-range rows carry more than all of that loss.
   - The mechanism: the LightGBM part trains on the LIRF convention rows (routing acts only at prediction), and SCHED-anchored T windows carry that convention to non-routed NM-missing rows. H015 v2's "this is not a convention bet" does not hold for the model's behaviour. (D3-C2)
4. **January 2026 is outside the 2025 range exactly where that defect lives.**
   - Checked target-free: non-LIRF NM-missing departures more than 3 h late number 435 in January 2026, against 78 in January 2025 and a 2025 monthly maximum of 222. More than 5 h late: 92, against 19 and 36.
   - On the development folds, E019 predicts out of range on 44 % of the > 5 h rows (E017 4 %, E005 0 %).
   - My estimate of the cost to E019's January margin over E005 runs from about 0 s to 5 s, with a heavy upper tail. The development-fold margins are 21–49 s. (D3-C3)
5. **The routing is priced far from break-even.**
   - The unrouted twin E020 would lose to E005 on the routed subgroup only if the 2026 convention (tail) rate fell below 0.009–0.099, per development fold. The observed 2025 rates on those folds are 0.35–0.76.
   - The price of routing is 122.5 s on the 2025 folds. That is a Day 4 governance question, answered in (e). It does not bear on E019 against E005.
6. **H cannot test items 3 and 4.** December's access tests E019's general advantage on a fresh month. It cannot test the January shift.

**Conclusion.**
- E019 is better than E005 on every fold, and pooled at every airport, in both full and bulk RMSE.
- On the routed subgroup it is identical to E005, so it carries no convention bet there.
- Its one weakness against E005 is small on the 2025 evidence and bounded in expectation for January.
- Holding E005 would keep a model that is 21–49 s worse on every fold. The promotion stands under the frozen rules. Items 2–4 are disclosures carried on the champion into Day 4.

**Where the record is wrong** (figures in Scientific Validity):

| Correction | Finding |
|---|---|
| D3-C1 | E019's margin over E005 is 95 % routed FS1 structure. Congestion on all rows in the champion is −1.90 s (q95 −0.98), with R1 and R2 TIE and criterion 3 failing at EHAM (+7.2 %). The E019 analysis omits criterion 3's failure on the `excl_LIRF_NM_missing` disclosure |
| D3-C2 | The loss on non-LIRF NM-missing rows is caused by the congestion block, through out-of-range predictions and the LIRF convention learned in training. It is not "`d_sched` extremes" alone |
| D3-C3 | January 2026's forward exposure is understated: counts of long-delay NM-missing rows are 2.0–2.6 times the 2025 maximum |
| D3-C4 | E020–E022 ran on "Intel(R) Xeon(R) Processor @ 2.80GHz", not 2.10 GHz as their analyses state. Determinism therefore held across two CPU model strings. The seed has no role in this procedure |
| D3-C5 | The researcher process relaunched after the second restart with `--model claude-opus-5-5 --effort medium` (INC-0004 scope). Neither restart is in the session registry, and the session number was not advanced (contract §1) |
| D3-C6 | `research/STATE.md` is stale for the third phase running |
| D3-C7 | The NM-present bulk range against E005 is −47.9 to −55.4 s, not −48.9 to −55.4 s |
| D3-C8 | DAY_SUMMARY §7 misquotes the Advisor's C forecast and omits the Advisor's H016 v2 and H017 v2 misses |
| D3-C9 | Advisor record: the H015 v2 review did not check where the routed model trains, and accepted "not a convention bet" for non-LIRF NM-missing rows |

**Verified here.** All checks were read-only.
- **What I did not do.** No December DEP target was read. I did not run `holdout_check.py`, and no model was fitted.
- **What I read.** Development-fold truth was read only through the frozen `prc.evaluate.truth_frame`, which refuses H and the final folds. The forward counts use target-free silver columns, with December excluded.
- **What I wrote.** Only this file in the repository; scratch scripts stayed outside it. The tree is clean before and after.

The checks:
- **Hashes.**
  - The proposal matches the envelope (`20dbd960…`).
  - The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json` (`32c41c0f…`).
  - `.claude/agents/advisor.md` is `30fff5dd…`, matching `config/agents.yaml`. `uv.lock` is `39df945c…`.
  - In the gate records of E019–E022, the proposal, review, ack, `gate.py`, advisor definition, `uv.lock` and frozen hashes all match their files.
- **Mirrors.** X-D03-S01-0001 (6/6), X-D03-S01-0002 (9/9) and X-D02-S01-0006 (4/4) verify.
- **Code freeze.**
  - `git diff --stat 7e9c431 HEAD -- src scripts pyproject.toml uv.lock` is empty.
  - It is also empty from `2671dd3` (precondition 1(d)), including `tests/`.
  - Every chain commit touches only `experiments/`, `research/` and `orchestration/`.
  - All four allocations and runs were from clean trees, strictly sequential, each after the previous checkpoint.
- **Predictions.**
  - All eight files of E005, E009, E017, E018 and E019–E022 match their manifests.
  - E019 = E022 byte for byte on all 8 folds, including H. Silver matches its frozen pin (the evaluator loaded it).
- **Holdout.** The task ledger holds one `holdout_access` event, `day-01`. Day 3 has 0 of 1 used, and `research/day-03/holdout/` does not exist.
- **Tests and lint.** `pytest`: 123/123 with caches disabled. `ruff`: clean.
- **Secrets.**
  - No credential value (S3 access key, S3 secret key, OpenSky password) appears in the 468 tracked files or in any commit message.
  - The OpenSky username occurs only inside the public repository owner's handle, in the brief and in merge-commit messages. DATA_POLICY §1 does not list it as a credential.
- **INC-0004, measured at 06:58Z.**
  - One `claude` process is running, started about 05:35Z (elapsed 1 h 24 min), with `--model claude-opus-5-5 --effort medium`.
  - The host is "@ 2.80GHz", boot id `b973b4fe…`, the same as E020–E022.

## Scientific Validity

### (a) The Day 3 decisions re-verify

| Decision | Check (committed JSONs, re-derived from prediction files and development truth) | Result |
|---|---|---|
| Clause 1 not met | E019 − E005: R1 −31.41, R2 −49.03, R3 −34.36, S1 −37.91, W1 −38.45, S1c −32.61, W1c −21.32; mean −38.23 (q95 −34.95); 7/7 WIN. No airport degraded (LIRF 1,449.3 against 1,485.8 s, −2.5 %) | Confirmed |
| Clause 2(a), 2(b) not met | E019 − E017 on `NM_present_excl_LIRF`: −5.88, −6.67, −6.31, −5.35, −9.52 (S1c −5.72, W1c −7.66); mean −6.746 (q95 −5.968); 7/7 WIN; \|top-1\| ≤ 0.10; criterion 3 passes on that population | Confirmed. The 2(b) margin is 0.75 s on the point estimate, as pre-registered |
| Clause 2(c) not met | `NM_present` bulk −5.68, −5.46, −5.63, −5.48, −5.22 | Confirmed |
| Clause 3 not met | `route_check_E019.json`: 3(a) max \|Δ\| 0.0 and 3(b) max \|Δ\| 0.0 on all 8 folds (routed rows 168, 115, 52, 337, 58; twins 337, 58; H 88) | Confirmed. The file hashes match the manifests |
| Clause 4 not met | `NM_missing_LIRF.delta_rmse_bulk` against E005 = 0.0 on every fold | Confirmed |
| Criterion 6 | `repro_E022_of_E019.json`: Δ 0.0 on all development folds; criteria 1–3 hold. SHA-256 equal on all 8 files (recomputed) | Confirmed |
| Criterion 7 | E019 954.1 s / 4.76 GB; E022 1,339.1 s / 4.63 GB (CLASS-M 1,800 s / 8 GB) | Confirmed |
| B3 | S1c −32.61 against E005; −5.72 against E017 | No objection |
| E020 (H016 v2), E021 (H017 v2) | As recorded: the R effect as pre-registered; readings 1 and 2 at −3.28 and −3.47 s, below the floor | Confirmed |

**The C clause at 0.75 s** (proposal, "Case against" 1).
- The clause is decided on the point estimate. The floor was set at about three times the largest development-fold perturbation measured on this population (1.96 s), and it is decisive as written.
- The frozen bootstrap does not model training perturbation, so C's true value could plausibly lie between about −5 and −9 s.
- Rule 10 forbids reading the q95 (−5.97 s) as a failure after the fact, just as it would forbid moving the floor to rescue a −5.9 s result. The clause stands.

### (b) Where E019's margin comes from (D3-C1)

All rows, dRMSE (s). "rE017" is E017 with E005's predictions on the routed rows: a composition of existing prediction files, and the baseline the H015 v2 proposal itself cited (−36.3 s). The frozen paired bootstrap and `promotion_check` were applied unchanged.

| Contrast | R1 | R2 | R3 | S1 | W1 | S1c | W1c | Dev mean |
|---|---|---|---|---|---|---|---|---|
| E019 − E005 | −31.41 | −49.03 | −34.36 | −37.91 | −38.45 | −32.61 | −21.32 | **−38.23** |
| rE017 − E005 | −31.69 | −49.00 | −32.60 | −33.85 | −34.50 | −29.96 | −10.55 | **−36.33** |
| E019 − rE017 (congestion, as served) | +0.28 TIE | −0.03 TIE | −1.77 WIN | −4.06 WIN | −3.95 WIN | −2.65 WIN | −10.77 WIN | **−1.90** (q95 −0.98) |
| E019 − E020 (the routing's price) | +161.73 | +25.52 | +97.23 | +211.37 | +116.85 | +197.52 | +46.69 | **+122.54** |

- **95 % of the margin over E005 is the routed FS1 deterministic structure.** Day 2 could not promote it (E017: criterion 8). Day 3's routing made it promotable.
- **Congestion is worth 1.9 s on the metric the champion is scored on,** with no gain on R1 or R2. Two things shrink −6.75 s to −1.90 s:
  - the all-rows RMSE scale, where LIRF convention rows dominate the error;
  - the loss on non-LIRF NM-missing rows ((c)).
- **Criterion 3 fails on E019 − rE017: EHAM is +7.2 %** (pooled development RMSE 180.99 → 194.04 s).
  - The committed disclosure `E019_vs_E017_mech_excl_LIRF_NM_missing.json` already shows it (`criterion_3: false`, EHAM +0.0721).
  - The E019 analysis reports that disclosure as "criteria 1 and 2 pass" and does not mention criterion 3.
- **DAY_SUMMARY §1 therefore needs the matched all-rows figure beside C** (standing rule 11).
  - The −56.87 s (E020 − E017) it carries is the convention channel on rows the champion routes away. It is not congestion as served.
  - "Consistently" holds on the clause population only.

### (c) The out-of-range defect on non-LIRF NM-missing rows (D3-C2)

**Bulk dRMSE (s) on `NM_missing_other`** (rule 7). The comparator is E005 unless the row says otherwise.

| | R1 | R2 | R3 | S1 | W1 | Pooled dev |
|---|---|---|---|---|---|---|
| E017 − E005 | −117.7 | −171.5 | −92.7 | −75.2 | −36.3 | **−100.4** |
| E019 − E005 | +78.0 | +62.3 | +27.5 | −106.8 | +40.6 | **+5.25** |
| E019 − E017 | +195.7 | +233.8 | +120.2 | −31.5 | +76.9 | |

**Predictions out of range on this group's bulk rows** (y < 3,600 s), counted per development fold, R1 to W1:

| Model | pred > 3,600 s | pred < 0 s |
|---|---|---|
| E005 | 0, 0, 0, 0, 0 | 0, 0, 0, 0, 0 |
| E017 | 9, 3, 1, 10, 3 | 9, 6, 5, 29, 17 |
| E019 | 20, 8, 7, 4, 5 | 40, 25, 14, 43, 20 |

- **These rows carry the whole loss.** They carry 2.7, 3.2, 4.5 and 3.4 times E019's bulk SSE loss against E005 on R1, R2, R3 and W1. Without them, E019 would beat E005 on this group.
- **They concentrate on long schedule delays.** Pooled over the development folds, by `d_sched` band:

| `d_sched` | Rows | Out of range: E019 / E017 / E005 | Mean excess SE against E005 (10⁶ s²): E019 / E017 |
|---|---|---|---|
| ≤ 1 h | 2,765 | 3.0 % / 2.2 % / 0 | −0.08 / −0.13 |
| 1–3 h | 6,721 | 0.3 % / 0.3 % / 0 | −0.18 / −0.15 |
| 3–5 h | 473 | 8.9 % / 2.3 % / 0 | +0.70 / +0.24 |
| > 5 h | 93 | **44 % / 4.3 % / 0** | **+9.05** / +0.27 (E019 median +1.88) |

- **EHAM** (which gives D3-C1's criterion 3 failure).
  - Its NM-missing rows (1,913 of 102,823) carry +602 × 10⁶ s² of E019 − rE017, against −99 × 10⁶ on its NM-present rows.
  - Examples:
    - R2 197540199: y 482 s, E017 −11 s, E019 −8,859 s, `d_sched` 19,981 s;
    - R1 195553337: y 728 s, E017 898 s, E019 −7,894 s;
    - R1 195560125: y 1,036 s, E017 1,225 s, E019 +7,564 s.
  - The top five rows carry 0.56. Without them, EHAM is still +3.2 %.
- **Mechanism.**
  - `routed_lightgbm` fits `gbm.lightgbm` on all training rows, including the routed subgroup's convention rows. Routing replaces only validation predictions. That is why E019 = E020 outside the routed rows (clause 3(b)).
  - For NM-missing rows, FS2's T windows start at `SCHED`. Their counts grow with the schedule delay, far beyond the NM-present range (93–129 per fold on the clause population).
  - The ensemble learned "long SCHED-anchored window → convention-scale target" from LIRF, and applies it where the convention does not hold. Interactions then drive some predictions below zero.
- **Consequences for the record.**
  - H015 v2's rule 2 sentence, "This is not a convention bet", is contradicted by the model's behaviour on these rows.
  - DAY_SUMMARY §8.1's "a feature problem (`d_sched` extremes)" is incomplete: the congestion block is the cause (E017 has `d_sched` and does not show it). Also, the R1 dominant row, LEBL 196787086, has `d_sched` of only 1,970 s (y 1,315, E019 11,267 s).
  - The proposal's "no convention bet … removed there" is true of the routed subgroup only.

### (d) Forward support in the ranking months (D3-C3)

Target-free, from silver: non-LIRF DEP rows with `AOBT_3` missing, and `d_sched` = MVT − SCHED. December is excluded.

| Month | NM-missing rows (share) | `d_sched` > 3 h | > 5 h | Airport-days with ≥ 50 such rows (largest) |
|---|---|---|---|---|
| Jan 2025 | 1,375 (0.97 %) | 78 | 19 | 1 (53) |
| 2025 monthly range, Jan–Nov | 1,015–3,601 | 27–222 (Jul) | 9–36 (Jul) | 0–11 (32–107) |
| **Jan 2026** | 2,346 (1.66 %) | **435** | **92** | **7 (123)** |
| Jul 2026 | 2,561 (1.45 %) | 159 | 39 | 0 (37) |

- **January 2026 is 5.6× (> 3 h) and 4.8× (> 5 h) January 2025, and 2.0× and 2.6× the 2025 monthly maximum,** clustered in more disruption airport-days than any 2025 month but July.
- **July 2026 lies inside the 2025 range,** and on S1 E019 beats E005 on this group (full −84.3 s).
- **The expected January cost to E019 against E005,** using the development-fold per-row excess by band on about 152,700 January DEP rows at a champion RMSE of about 470 s:
  - mean-based: about +0.8 × 10⁹ s², or about +5 s of January RMSE;
  - median-based: near zero.
  - The difference is the heavy tail: one row like 197540199 costs about 0.7 s of January RMSE on its own.
- **Against development margins of 21–49 s, E019 is expected to stay ahead of E005 in January,** but by less than the 2025 folds suggest.
- **H (December) cannot show this, and the ranking targets are unseen.** Rule 2's "1.66 % against 0.97 %" understates the shift and is replaced by this table.

### (e) The routing's price, and the question the proposal asks ("Case against" 2 and 3)

**Break-even convention rate for the unrouted twin.** On `LIRF_NM_missing`, write E020 − E005 as tail and bulk mean squared errors, with y ≥ 3,600 s as the convention proxy (Day 1: 83 % of LIRF tail rows are block-at-schedule). The unrouted fit loses to E005 on the subgroup only if the tail rate falls below:

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c |
|---|---|---|---|---|---|---|---|
| Break-even rate | 0.039 | 0.099 | 0.030 | 0.058 | 0.009 | 0.052 | 0.022 |
| Observed rate | 0.44 | 0.50 | 0.69 | 0.35 | 0.76 | 0.35 | 0.76 |

**The judgement the proposal requests.**
- **The routing premise is true but weak.**
  - The 2026 rate is not estimable.
  - The unrouted bet would lose only if the convention nearly vanished: to under a sixth of the lowest 2025 month on S1 (0.058 against 0.35).
  - Declining it costs 122.5 s on 2025.
- **This does not change Day 3.**
  - E020 is not a candidate and never NEW (rule 9).
  - E019 is judged against E005, not against E020.
  - The routing was pre-registered as a structure (ruling B), and it did what it claimed.
- **For Day 4, an unrouted candidate is admissible.** It must meet all of the following. They are governance conditions, not a design:
  - it is a new configuration, since E020's configuration cannot be re-submitted unchanged (rule 10);
  - it pre-registers its convention exposure under rule 8, with its S1 expectation at July's rate;
  - it keeps H009 v3's criterion 8 rule unchanged (ruling B; no new threshold);
  - any forward-risk rationale it rests on is pre-registered, cites these break-even figures as Day 3 outcomes, and states the 2026 counts (107 and 276 rows).
- **The out-of-range defect in (c) is independent of routing.** It sits on non-routed rows and is shared by E019 and E020.

### (f) Determinism and provenance (D3-C4, D3-C5)

- **Determinism.**
  - `provenance.yaml` records "Intel(R) Xeon(R) Processor @ 2.10GHz" for E019 and "@ 2.80GHz" for E020, E021 and E022. The current host is "@ 2.80GHz" with boot id `b973b4fe…`.
  - The E020, E021 and E022 analyses all state 2.10 GHz, which is wrong. Authorization item 8 required the CPU string.
  - The correction strengthens the finding: byte identity held across two CPU model strings, not only across a restart.
  - "Across a seed change" is by construction. No component of this procedure consumes the seed: `bagging_fraction` and `feature_fraction` are 1.0, and `bin_construct_sample_cnt` exceeds every training set.
  - Criterion 6 is therefore a determinism check, as ruled on Day 2, not an estimate of training variance.
- **INC-0004.**
  - The incident describes the launch at the start of D03-S01 (`claude-sonnet-5-5`, `medium`).
  - The process running since about 05:35Z, after the second restart, carries `--model claude-opus-5-5 --effort medium`. It produced E020–E022, the DAY_SUMMARY and this proposal. The model argument now agrees with the registry; the effort argument still does not.
  - The owner decides the incident. It does not block, following the Day 2 precedent (INC-0003).
- **Restarts and the session number.**
  - Both container restarts are recorded only indirectly: the X-D03-S01-0001 `retry.yaml`, and the E019 analysis and chain provenance files. `orchestration/session-registry.jsonl` has no event for either.
  - COMMUNICATION_CONTRACT §1: "A new session number is used after a container reset". D03-S01 was kept across both.
  - No result depends on it: allocations were clean, the code was frozen and every prediction file matches its manifest. It is a procedural deviation to record.

### (g) The proposal's other items

- **Researcher evidence failures** (v1 counts, the P-label defect, the noise population). They were corrected before any run and are recorded in DAY_SUMMARY §7. No residue remains in E019–E022.
- **Process slips.**
  - The approval outage and the post-restart E019 checkpoint changed nothing: the comparison JSONs were produced at 17:02Z on 29 September, and I reproduced their figures from the files.
  - The v1-code EDA P figures (0.086 % of rows) are immaterial.
- **The code freeze held.** Verified.

## Novelty Relative to Existing Research

- **This exchange proposes no experiment.**
- **Day 3's contribution, stated at the right size:**
  - C: −6.75 s on NM-present rows at the nine airports, about half P and half T;
  - a routing structure that makes the Day 2 FS1 fit promotable without a convention bet on the routed subgroup;
  - real-data determinism across hosts;
  - on all rows, congestion adds 1.9 s to the champion and a new out-of-range defect on NM-missing rows.
- **Brief §11 items not tested:** the same-runway and pressure variants beyond the 15 features, and queue-length proxies. They are coverage notes, not gaps in the decisions.

## Experimental Isolation

- **The phase close changes and runs nothing.**
- **The attributions above are exact compositions of existing prediction files,** with RMSE differences on identical rows adding exactly:
  - rE017 is E017 plus E005 on the routed rows, so E019 − rE017 isolates congestion as served;
  - the break-even rate isolates the routed subgroup.
- **The defect in (c) is isolated to the congestion block by E019 − E017,** a matched, deterministic pair differing only by the 15 columns (plus routing, which does not touch these rows).
- **H015's clauses remain correctly isolated as pre-registered.** The corrections concern populations the clauses excluded by design.

## Validation Quality

**Folds and frozen artifacts.**
- The frozen folds were used unchanged in all four Day 3 runs, S1 and both twins included.
- The frozen hashes are intact.
- H was predicted only: 88 routed rows, identical to E005.

### Ruling H3: the Day 3 holdout access

1. **One access, E019 against E005, as proposed.**
   - E005 is the phase-opening champion, since Day 2 closed with E005.
   - E019 is the phase-closing champion by this review, and is allocated in `day-03` (rule 9).
   - `holdout_compare` attributes the access to `day-03`, which has 0 of 1 used.
   - E019 and E005 are COMPLETE in the ledger, and their H files match their manifests.
2. **NEW is the primary, E019.**
   - E022 is byte-identical on H, but it is a reproduction.
   - E020 and E021 may never be NEW (rule 9; H016 and H017 authorizations).
3. **The revert is applied mechanically** (`phase_close.revert_on: LOSS`).
   - On a LOSS, H015 v2 is recorded INCONCLUSIVE ("phase-close holdout LOSS, frozen revert"), and E005 remains champion.
   - No substitute comparison follows.
4. **What H can and cannot test.**
   - It tests E019's general advantage on a month outside every development fold.
   - It cannot test the LIRF convention: the routed rows are identical.
   - It cannot test the January long-delay shift ((d)).
   - A WIN does not discharge D3-C3.
5. **The printed H figures are recorded only.** They may not inform features, models, thresholds or Day 4 bases.

**Bootstrap and noise.** Fold outcomes on margins of 1–2 s (E019 − rE017 on R1 and R2; the P/T halves) are not mechanism evidence beyond what the pre-registered clauses say.

## Leakage Review

### Target Leakage

PASS

- **No input reads another DEP row's block time or target.** This holds by masking invariance on 1,919,370 rows, by unit tests, and by `_dep_frame`'s column selection.
- **No target statistic is used.** Both fits are fold-local.
- **The routed model's LightGBM trains on the fold's training rows only.** It includes the routed subgroup's training rows, which is admissible. This is a behavioural exposure ((c)), not leakage.
- No December target was read by any Day 3 run, comparison or this review.

### Temporal Leakage

CONCERN

These are label notes carried from Day 3; they are not blocking.
- **T** (admissible under DATASET_AUDIT §6: the ranking file carries each row's own takeoff and every other movement): the five in-taxi features, all `d_*` deltas and the hour-resolution proxy.
- **P** (verified): the ten P features.
- **SCHED-anchored T windows on NM-missing rows** carry the schedule delay, and with it the M3 convention channel. They are T, outside the causal-only variant (rule 8).

### Competition Availability

CONCERN

Not blocking. It bears on how the champion is read.
- **Every input is present for ranking DEP rows.**
- **January 2026's long-delay NM-missing rows at the nine airports exceed the 2025 range** by 2.0–2.6 times ((d)). On those rows, E019 predicts out of range at 9–44 % on the 2025 evidence.
- **SUBMIT_JUL lacks June 2026 context** for the first 30 minutes of 1 July (0.008 % of rows).

## Compute Review

### RAM

PASS

No experiment. The re-derivations read prediction files and development-fold truth, plus target-free silver columns, all within the container's memory without incident.

### Runtime

PASS

- The test suite took about 37 s.
- Five read-only scripts each took a few minutes; one included a single frozen 2,000-resample bootstrap.
- No model was fitted.

### Disk

PASS

One review file. The scratch files are outside the repository.

## Weakest Assumption

**That E019's advantage over E005 carries into January 2026.** The concern is the rows where E019 is structurally weak.
- On the 2025 evidence, E019's out-of-range rate on non-LIRF NM-missing rows delayed more than 5 h is 44 %, against 0 % for E005.
- January 2026 has 2.6 times the 2025 maximum of such rows.
- The expected damage is a few seconds, well below the margin. But the per-row cost is heavy-tailed (up to about 0.7 s of January RMSE per row), and neither H nor any development fold samples a month like it.

## Missing Control or Ablation

None blocks the phase close. Three are named for Day 4; they are named, not designed.
1. **Out-of-range predictions.** Any Day 4 candidate built on FS2, or on any count that grows with the schedule delay, reports standing rule 12. Its treatment of NM-missing rows at the nine airports, if any, is its own hypothesis, with an isolating ablation.
2. **The congestion contrast as served.** A candidate whose mechanism clause excludes rows it serves also reports the matched all-rows contrast on the rows it actually predicts. For H015 that is E019 − rE017, not E020 − E017.
3. **The permuted-column control** stays named, not required: C's floor still rests on proxy perturbations.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **The Day 3 decisions stand as recorded.**
   - H015 v2 is not falsified. Clauses 1–4 are not met; criteria 1–3, 5, 6 and 7 hold; B1–B4 hold.
   - **Criterion 8.** This review raises two objections, both resolved for the promotion by disclosure:
     - O1: the out-of-range defect, (c);
     - O2: January forward support, (d).
   - Neither makes E019 worse than E005 on the 2025 evidence or in expectation for either ranking month.
   - **E019 is the phase-closing champion, subject to item 2.**
   - E020 (H016 v2) and E021 (H017 v2) keep their recorded reference and ablation outcomes. E022 is the passing reproduction.
2. **Exactly one protected-holdout access,** after the acknowledgement below is committed, from a clean tree, with no experiment running, and with no `day-03` `holdout_access` event in the task ledger:

   ```
   uv run python scripts/holdout_check.py E019 E005 --reason "Day 3 phase close (X-D03-S01-0003): phase-closing champion E019 (H015 v2) vs phase-opening champion E005"
   ```

   - **WIN or TIE:** E019 is champion (H015 v2: PROMOTE).
   - **LOSS:** revert. E005 is champion, and H015 v2 is recorded INCONCLUSIVE (phase-close holdout LOSS).
   - **If the command exits before a `day-03` `holdout_access` line is appended,** no access occurred. Record the cause; the identical command may then be issued once more.
   - **If the line was appended and no result file was written,** stop. There is no re-run, and a recovery review decides.
   - Commit `research/day-03/holdout/holdout_E019_vs_E005.json` and the task-ledger line.
3. **Not authorized:**
   - any other H comparison, including E020, E021 or E022 as NEW, or E022 in place of E019;
   - use of the H figures for anything except recording the outcome;
   - any allocation, run, fit or re-run in Day 3;
   - any change to frozen files, reviews or completed records (corrections are appended).

Required acknowledgement path: `research/day-03/acks/PHASE_CLOSE_D03_ack_v1.md`

**Contents of the acknowledgement:**
- the proposal hash (`20dbd960…`) and this review's hash;
- corrections D3-C1 to D3-C9, appended (the proposal and completed records are not edited);
- standing rule 12, adopted;
- Ruling H3 and the routing answer ((e)), recorded;
- the command in item 2.

**Corrections.** Figures are in Scientific Validity.
- **D3-C1. Where the champion's margin comes from** (DAY_SUMMARY §1, §5, §6.1; E019 analysis; journal; STATE).
  - rE017 − E005 is −36.33 s, so 95 % of E019's −38.23 s is routed FS1 structure.
  - E019 − rE017 on all rows is −1.90 s (q95 −0.98): R1 +0.28 TIE, R2 −0.03 TIE, R3, S1, W1 WIN. Criterion 3 fails (EHAM +7.2 %).
  - Report this beside C (rule 11). The −56.87 s E020 − E017 figure is the convention channel, not congestion as served.
  - The E019 analysis's `excl_LIRF_NM_missing` disclosure omits `criterion_3: false` (EHAM +7.2 %).
- **D3-C2. The non-LIRF NM-missing defect is caused by the congestion block** (DAY_SUMMARY §6.6, §8.1; E019 analysis Observation 1; H015 v2 rule 2).
  - E017 beats E005 there in bulk on all five development folds (pooled −100.4 s). E019 loses on four (pooled +5.25 s). E019 − E017 bulk is +76.9 to +233.8 s on R1, R2, R3 and W1.
  - Out-of-range predictions (below 0 s, or above 3,600 s on normal taxis) carry all of it. They concentrate above 3 h of schedule delay (> 5 h: 44 %, against E017 4.3 % and E005 0).
  - The LightGBM trains on the routed convention rows, and SCHED-anchored T windows carry the learned mixture to non-routed NM-missing rows.
  - "This is not a convention bet" and "`d_sched` extremes" are withdrawn as explanations.
- **D3-C3. Forward exposure, January 2026** (rule 2; DAY_SUMMARY §6.6; STATE).
  - Replace "1.66 % against 0.97 %" with the (d) table: 435 rows over 3 h and 92 over 5 h, against a 2025 maximum of 222 and 36.
  - The expected cost is roughly 0–5 s of January margin against E005, heavy-tailed.
  - July 2026 is inside the 2025 range.
  - H does not test it.
- **D3-C4. CPU strings and determinism** (E020, E021, E022 analyses; DAY_SUMMARY §6.3).
  - E020–E022 ran on "@ 2.80GHz", E019 on "@ 2.10GHz". Determinism held across two CPU model strings.
  - The seed plays no role in this procedure, so criterion 6 here is a determinism check.
  - The analyses are corrected by appended notes, not edited.
- **D3-C5. INC-0004 scope and session procedure.**
  - Append to INC-0004: from about 05:35Z on 30 September, after the second restart, the researcher process carries `--model claude-opus-5-5 --effort medium`. This covers E020–E022, the DAY_SUMMARY and this proposal.
  - Record both container restarts (UTC, boot ids `ac2b2cff…` → `b973b4fe…`, launch arguments) as events in `orchestration/session-registry.jsonl`.
  - Record that D03-S01 was kept across container resets, contrary to COMMUNICATION_CONTRACT §1, with no result depending on it.
- **D3-C6. STATE.md is stale** (brief §13 step 3; repeats Day 1 C6 and D2-C6).
  - The 06:40:20Z version still says "Pending: none; next is the H015 v2 chain" and "Day 3 so far (no experiment yet)".
  - It carries two separate holdout lines.
- **D3-C7. Figure.** The NM-present bulk range of E019 against E005 is −47.9 to −55.4 s (R2 −47.91), not −48.9 to −55.4 s (E019 analysis; proposal "Case for").
- **D3-C8. Missed forecasts** (DAY_SUMMARY §7).
  - The Advisor's C forecast was −2 to −7 s (central −4 s; P(2(b) not met) 0.30). "−3 to −5 s" was its failure-mode band, and the outcome lies at the edge of the stated range.
  - Add the Advisor's H016 v2 misses:
    - all rows: −8 to +6 s → −56.87 s;
    - S1 criterion 8 statistic: +6,300 to +7,800 s → +4,292 s;
    - development mean 360–380 s (P 0.75) → 321.95 s.
  - Add the Advisor's H017 v2 miss: P −0.5 to −3 s → −3.47 s.
- **D3-C9. Advisor record.**
  - The H015 v2 review assessed R's residual exposure on LIRF NM-present rows only.
  - It accepted "not a convention bet" for non-LIRF NM-missing rows without checking that the routed model trains on the routed rows.
  - The out-of-range predictions were visible in rule 7 and in the committed disclosure's `criterion_3: false`, and were not flagged before this review.

**Conditions on the phase-closing commit:**
- **The acknowledgement** is committed before the access.
- **The holdout result** and its task-ledger line are committed.
- **`research/STATE.md`** is current, with a measured header time. It records:
  - the champion per the H outcome, with D3-C1 to D3-C3 as standing disclosures on it;
  - Day 3 holdout 1 of 1 used;
  - INC-0004 open, with D3-C5;
  - standing rules 1–12 and B1–B4, and rulings H, B, R and H3;
  - the next action.
- **DAY_SUMMARY** is corrected per D3-C1 to D3-C8 and marked final, with the H outcome recorded.
- **Journal and ledger.** A Day 3 phase-close journal entry exists, and the ledger records the outcomes.
- **Mirror.** The exchange is mirrored: `envelope.yaml`, `response.md` and `checksums.sha256`.
- **Session registry.** It has the restart events (D3-C5) and an end event for D03-S01.

## Revision

None required for this version.

**Standing review rule added from this exchange.** It applies from the next proposal onward.

12. **Out-of-range predictions and forward support.**
    - Every comparison used for a promotion or a criterion-4 check reports, for candidate and comparator, per development fold and twin, and by the four rule 7 subgroups, the number of predictions below 0 s and the number above 3,600 s on bulk rows (y < 3,600 s).
    - A candidate with any input that grows with the schedule delay (windows anchored at `SCHED` or `EOBT_1`, or `d_sched` itself) also reports target-free, per ranking month, the NM-missing rows with `d_sched` > 3 h and > 5 h by subgroup, against the 2025 monthly range.
    - This is disclosure only. It changes no fold outcome or frozen criterion.

## Advisor Prediction

Probability of improvement:

| Event | P |
|---|---|
| The Day 3 decisions are correct under the frozen rules | 0.97 |
| Holdout outcome E019 against E005: WIN | 0.90 |
| Holdout outcome: TIE | 0.07 |
| Holdout outcome: LOSS (revert) | 0.03 |
| E005's H RMSE equals its Day 1 value, 411.29 s (same file, same truth) | 0.99 |
| E019 has a lower true RMSE than E005 on January 2026 | 0.88 |
| E019 has a lower true RMSE than E005 on July 2026 | 0.93 |
| A Day 4 FS2-based model without an explicit NM-missing treatment has ≥ 10 negative predictions on `NM_missing_other` bulk rows on some development fold (rule 12) | 0.90 |

Expected magnitude:
- **The H access:** E019 − E005 of −25 to −45 s (central −35 s), so E019's H RMSE is about 366–386 s against E005's 411.29 s.
- **January 2026, unobservable within Days 1–7:** E019's margin over E005 is a few seconds smaller than its development margins, because of the long-delay NM-missing rows.
- **Congestion as served in the champion:** about −2 s of all-rows RMSE, with R1 and R2 TIE.

Primary expected failure mode:
- **Primary.** The access returns WIN, because December does not carry January's long-delay cluster. E019 becomes champion, and its out-of-range predictions on non-LIRF NM-missing rows then cost part of its January margin. Every Day 1–4 check cannot see this, since the ranking targets are unseen, and D3-C3 is the only record of it.
- **Secondary.** The record carries "congestion helps" as a metric-level Day 3 result. On the champion's metric the gain is −1.9 s with two TIE folds and an EHAM degradation. Day 4 then builds on the congestion block without treating the defect in D3-C2.
