# Day 4 summary: historical priors and interactions (DRAFT; phase close X-D04-S02-0001 pending)

**Sessions:** D04-S01 (ended at a container reset), D04-S02. **Branch:** `day-4` (PR #6).
**Provenance:**
- INC-0004 (launch `--effort medium` against metadata `high`) is open and covers every Day 4 artifact.
- INC-0005 (owner-instructed delegation to `claude-sonnet-5-5` workers) covers Day 4. The delegated work is listed in §8.
- One container restart: between E023's allocation (D04-S01) and its run (D04-S02), in the same window as the owner's usage-limit pause. D04-S02 was opened as a new session under COMMUNICATION_CONTRACT §1.

## 1. The Day 4 question and its answer

**Question (brief §11):** do historical priors (fold-local target statistics over static keys) and interactions reduce error beyond FS1 and congestion?

**Answer: not measurably, in this learner.**
- **H019 v2 (E024).** FS3 adds 5 fold-local LOMO priors (stand × runway, runway × hour, operator, aircraft type, and a count) to FS2. Against its matched reference E023, on `NM_present_excl_LIRF`, it gives **−0.29 s** (q95 +0.12), with S1 TIE and W1 LOSS. The pre-registered floor was −3.0 s. **The mechanism is falsified** (clauses 1(a) and 1(b)). All rows: −0.40 s.
- **The EDA signal did not carry over.** Stand × runway gave +0.189 R² over an airport × hour prior in a linear model. LightGBM on FS1 already holds stand, runway and operator as categoricals, so a smoothed mean of the same keys adds about one tenth of the floor. This repeats Day 3's lesson (the T-dominance EDA): **univariate or linear EDA over a weak base overstates what a tree learner on FS1/FS2 leaves unexplained.**
- **Interactions via CatBoost (H020 v1) were rejected before any run** (§3). CatBoost is handed to Day 5 with the review's design objections.

**The Day 3 open question 1 was answered as well (H018 v2, E023).** D3-C2's out-of-range predictions are caused by training the LightGBM on the routed LIRF NM-missing rows. Excluding them from training:
- cuts the > 3 h out-of-range band from 81 to **5** (`NM_missing_other` bulk, 5 development folds);
- improves the treated subgroup's bulk by 105–230 s on every fold where E019 had lost to E017;
- improves all rows by **−2.04 s** against E019 (development mean 442.46).
- **It is not promotable:** S1 is TIE (+0.20), carried by LIRF NM-present row 192622644.

## 2. What was built

| Artifact | Purpose |
|---|---|
| `scripts/range_check.py` | Rule 12: out-of-range counts by fold × rule 7 subgroup, `--by-dsched`, `--bands`, forward support. Reproduces D3-C2 and D3-C3 exactly |
| `src/prc/priors.py`, `features.fs3` | 5 fold-local LOMO smoothed-mean priors (M = 50); FS0–FS2 byte-identical after the refactor; inert on a single training month (tested) |
| `routed_lightgbm` `route_train_exclude` | Removes the routed rows from LightGBM training (H018). The default reproduces E019 |
| `scripts/route_check.py` `-` | Routed-subgroup-only integrity check for routed candidates without an unrouted twin |
| `gbm.catboost`, `routed_catboost` | CatBoost Tier 1 and its routed variant (shared routing helper). Not used in Day 4; handed to Day 5 |
| CatBoost CPU calibration | `max_ctr_complexity=1` makes per-iteration cost linear (0.29 s/it on R3) |
| EDA | `research/day-04/eda/`: priors, joint keys, forward support, range-check baselines and references |
| Tests | 143 pass; ruff clean |

## 3. Advisor exchanges

| Exchange | Content | Decision |
|---|---|---|
| X-D04-S01-0001 | H018 v1, H019 v1, H020 v1 | **REVISE, REVISE, REJECT** (0.88, 0.82, 0.80). H018's clause 1 did not test D3-C2 (the increment is in the > 3 h band). H019's W1c was inert. H020's mechanism was false for the installed CatBoost (plain boosting; RMSE CTRs are a border share and a count), and CLASS-L was declined |
| X-D04-S01-0002 | H018 v2, H019 v2 | **ACCEPT ×2** (0.86, 0.80), with a tools freeze for the chain and recording conditions |
| X-D04-S02-0001 | Phase close | Pending |

## 4. Experiments (sequential, within class)

| E | Hypothesis | Model / features | Dev mean | Runtime / RAM | Result |
|---|---|---|---|---|---|
| E023 | H018 v2 (candidate) | routed LightGBM, FS2, routed rows excluded from training | **442.46** | 925 s / 5.29 GB | Clauses 1–3 not met (mechanism holds). Criterion 2 fails against E019 (S1 TIE). **Not promoted** |
| E024 | H019 v2 (candidate) | as E023, FS3 | **442.06** | 1,027 s / 5.73 GB | **Mechanism falsified** (clauses 1(a), 1(b)). Criterion 2 fails against E019 (S1 TIE). **Not promoted** |

No reproduction was due for either (criteria 1–3 failed against the champion in force).

**Attribution pair** (development mean, all rows): H018 − E019 −2.04 s; H019 − H018 −0.40 s; together E024 − E019 −2.43 s.

## 5. Champion: E019 (H015 v2), unchanged

- No Day 4 candidate met criteria 1–8. **E019 remains champion.** Development mean 444.49; −38.23 s against E005; Day 3 holdout WIN.
- **Holdout:** the phase-opening and phase-closing champions are both E019. The phase close proposes to close the Day 4 access unused (as ruling H on Day 2).
- **Standing disclosures D3-C1 to D3-C3 still apply to the champion.** E023 shows that D3-C2 has a working treatment that the frozen criteria do not admit (§6, finding 3).

## 6. Findings

1. **Priors over static keys add nothing measurable beyond FS2 in LightGBM** (−0.29 s on the clause population, −0.40 s on all rows). The best development mean so far is E024's 442.06, but 84 % of its margin over E019 is H018's training exclusion.
2. **W1 is the one LOSS** for the prior block (+1.63 s). Its validation priors come from 8 post-February source months, including LFPG's August–November runway regime. The proposal disclosed this staleness exposure. The other causal check (S1c) is a WIN (−1.12 s).
3. **D3-C2 is caused by training on the routed LIRF convention rows,** and excluding them fixes it (81 → 5 in the > 3 h band) at no cost elsewhere (`NM_present_excl_LIRF` within ±0.56 s on every development fold). It cannot be promoted because S1 does not WIN.
4. **S1 is decided by one row.** Row 192622644 (LIRF, NM-present, y 87,002 s, `d_sched` 87,001 s) carries S1's change in every Day 4 comparison against E019:
   - E023: `NM_present_LIRF` share +3.84;
   - E024: share 1.95, top-1 share 2.16 (prediction 8,136 → 5,780 s).
   Any treatment that changes the LightGBM's training set or features moves this convention-mixture row, and with it S1. That makes an S1 WIN against E019 hard to obtain for any non-routing change. This is a property of the frozen rule and the fold, recorded and not proposed for change.
5. **The prior block helps LIRF NM-present bulk rows** by 1.3–3.4 s on every development fold against E023, more than it helps the clause population. Observation only.
6. **Determinism held again:** E024's W1c predictions are byte-identical to E023's, as pre-registered (inert block).

## 7. Missed or corrected predictions (kept)

| Prediction | Outcome |
|---|---|
| H018 v2: > 3 h band 10–35 | **5: outside, better** |
| H018 v2: `NM_present_LIRF` full against E019 within −10 to +15 | **W1 −14.93: outside, more favourable**; others inside |
| H018 v2: `NM_missing_other` bulk S1 within ±30 | **−34.99: just outside** |
| H018 v2: all rows −0.5 to −3.0; S1 most likely TIE; development mean 441–444; perturbation within ±2 s | −2.04; S1 TIE; 442.46; max 0.56 s: **all inside** |
| H018 v2: promotion P 0.25 | Not promoted |
| H019 v2: mechanism −2 to −7 s (central −4), ≥ 3 WINs including S1 | **−0.29 s, S1 TIE: outside** |
| H019 v2: all rows −1 to −6 s | **−0.40 s: outside** |
| H019 v2: development mean 437–443; W1c identical | 442.06; identical: inside |
| H019 v2: promotion P 0.45 | Not promoted |
| H019 v2: largest gains at LFPG, EGLL, LTFM | Only LTFM (−1.94 s); LFPG +0.35 s, EGLL −0.12 s |
| Advisor (X-D04-S01-0002), H019: mean < 0 (P 0.80); ≤ −3.0 (0.30); 1(a) not met (0.50); mechanism supported (0.27); W1c identical (0.99); all rows < 0 (0.70) | Yes; no; no; no; yes; yes |
| Advisor, H018: mechanism holds (0.85/0.88); S1 WIN (0.20); promotion (0.12) | Holds; TIE; not promoted |
| H020 v1: the stated CatBoost mechanism | **False** for the installed version (X-D04-S01-0001) |

**Corrections and process slips.**
- **D4-C1:** the v1 proposals' `created_utc` values were written by hand, not measured. Measured from v2 on.
- **D4-C2 to D4-C6:** version labels in two Implementation Plans, the `range_check_refs.json` commit order, H019's rule 8 wording, and a dropped twin-rule phrase restored by reading 4(a).
- **Container restart and usage-limit pause:** E023 was allocated in D04-S01 and run in D04-S02, with its allocation records committed at D04-S02's start. No result depends on it.

## 8. Delegated work (INC-0005)

Implemented by `claude-sonnet-5-5` workers to the researcher's specification and reviewed by the researcher before commit:

| Commit | Work |
|---|---|
| D04-S01 start | Environment and data verification; pipeline digest (`sessions/D04-S01/SESSION_START.md`) |
| `ec8c5ad` | `scripts/range_check.py` (rule 12), baseline figures |
| `0794612` | Day 4 prior EDA (key coverage, incremental R², stability) |
| `7ae934f` | FS3 (`src/prc/priors.py`) and tests |
| `e9120a9` | `gbm.catboost`, `routed_catboost`, resource calibration |
| `99db208` | `range_check --bands`, joint-key EDA, single-training-month prior test |

Kept with the main session: every proposal, envelope, ack, allocation, interpretation and promotion decision; `route_train_exclude` (`7ea6b55`); the `route_check.py` `-` option (`8597e19`); the CatBoost calibration addendum (`af21355`); and both experiment launches (E023, E024). The Advisor was not delegated or substituted. **INC-0005 closes at this phase close.**

## 9. Open questions for Days 5–7

1. **The S1 constraint (finding 4).** A change to the LightGBM's training set or features moves row 192622644 and with it S1. A candidate that keeps D3-C2's treatment needs either an S1 WIN from elsewhere, or a proposal that routes or otherwise insulates LIRF NM-present convention rows, pre-registered under rule 8.
2. **D3-C2 and D3-C3 remain in the champion.** January 2026 has more extreme NM-missing rows than any 2025 month. E023's treatment is the known fix, but it is not promoted.
3. **CatBoost on GPU** (Day 5), with the H020 review's objections: ordered boosting, pre-collapse levels, CTR complexity and a capacity control.
4. **Priors:** not worth a further variant in LightGBM on FS2. A per-key ablation was not run.

*Draft written 2026-10-01T01:31:06Z (measured). Finalised after the phase-close review.*
