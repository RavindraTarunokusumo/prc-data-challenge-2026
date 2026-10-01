# Day 4 summary: historical priors and interactions (FINAL; phase close X-D04-S02-0001 ACCEPT; no promotion, no holdout access)

**Sessions:** D04-S01 (ended at a container reset), D04-S02. **Branch:** `day-4` (PR #6).
**Provenance:**
- INC-0004 (launch `--effort medium` against metadata `high`) is open and covers every Day 4 artifact.
- INC-0005 (owner-instructed delegation to `claude-sonnet-5-5` workers) covers Day 4. The delegated work is listed in §8. **Closed at this phase close.**
- One container restart: between E023's allocation (D04-S01) and its run (D04-S02), in the same window as the owner's usage-limit pause. D04-S02 was opened as a new session under COMMUNICATION_CONTRACT §1.

## 1. The Day 4 question and its answer

**Question (brief §11):** do historical priors (fold-local target statistics over static keys) and interactions reduce error beyond FS1 and congestion?

**Answer: a small, real gain, far below what was pre-registered (D4-C7).**
- **H019 v2 (E024).** FS3 adds 5 fold-local LOMO priors (stand × runway, runway × hour, operator, aircraft type, and a count) to FS2. Against its matched reference E023, on `NM_present_excl_LIRF`, it gives **−0.29 s** (q95 +0.12), with S1 TIE and W1 LOSS. The pre-registered floor was −3.0 s. **The mechanism is falsified** (clauses 1(a) and 1(b)). All rows: **−0.40 s** (q95 −0.03; R1–R3 WIN). Both are about a tenth of the floor and below criterion 1's 1.0 s.
- **The EDA signal did not carry over.** Stand × runway gave +0.189 R² over an airport × hour prior in a linear model. A smoothed mean of the same keys adds about a tenth of the floor in LightGBM. One explanation is that LightGBM on FS1 already holds stand, runway and operator as categoricals. **That explanation is untested** (D4-C7): the controls would be a within-key permuted prior and a K5-only block. The pattern repeats Day 3's lesson (the T-dominance EDA): **univariate or linear EDA over a weak base overstates what a tree learner on FS1/FS2 leaves unexplained.**
- **Interactions via CatBoost (H020 v1) were rejected before any run** (§3). CatBoost is handed to Day 5 with the review's design objections.

**The Day 3 open question 1 was answered as well (H018 v2, E023).** D3-C2's out-of-range predictions are caused by training the LightGBM on the routed LIRF NM-missing rows. Excluding them from training:
- cuts the > 3 h out-of-range band from 81 to **5** (`NM_missing_other` bulk, 5 development folds);
- improves the treated subgroup's bulk by 105–230 s on every fold where E019 had lost to E017;
- improves all rows by **−2.04 s** against E019 (development mean 442.46).
- **It is not promotable:** S1 is TIE (+0.20), carried by LIRF NM-present row 192622644 (D4-C9).

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
| X-D04-S02-0001 | Phase close | **ACCEPT** (0.85). Ruling H4 (no Day 4 access); corrections D4-C7 to D4-C16; INC-0005 closed |

## 4. Experiments (sequential, within class)

| E | Hypothesis | Model / features | Dev mean | Runtime / RAM | Result |
|---|---|---|---|---|---|
| E023 | H018 v2 (candidate) | routed LightGBM, FS2, routed rows excluded from training | **442.46** | 925 s / 5.29 GB | Clauses 1–3 not met (mechanism holds). Criterion 2 fails against E019 (S1 TIE). **Not promoted** |
| E024 | H019 v2 (candidate) | as E023, FS3 | **442.06** | 1,027 s / 5.73 GB | **Mechanism falsified** (clauses 1(a), 1(b)). Criterion 2 fails against E019 (S1 TIE). **Not promoted** |

No reproduction was due for either (criteria 1–3 failed against the champion in force).

**Attribution pair** (development mean, all rows): H018 − E019 −2.04 s; H019 − H018 −0.40 s; together E024 − E019 −2.43 s.

## 5. Champion: E019 (H015 v2), unchanged

- No Day 4 candidate met criteria 1–8. **E019 remains champion.** Development mean 444.49; −38.23 s against E005; Day 3 holdout WIN.
- **Holdout (ruling H4): Day 4 0 of 1, closed unused.** The phase-opening and phase-closing champions are both E019, so no comparison was made.
- **Standing disclosures on the champion: D3-C1 to D3-C3, and D4-C9** (§6, finding 4). E023 shows that D3-C2 has a working treatment that the frozen criteria do not admit (§6, finding 3), so E019 holds by rule.

## 6. Findings

1. **Priors over static keys add a small gain beyond FS2 in LightGBM** (D4-C7). On all rows it is −0.40 s (q95 −0.03; R1–R3 WIN), real but a tenth of the floor. On the clause population it is −0.29 s (q95 +0.12), not distinguishable from zero. The best development mean so far is E024's 442.06, but 84 % of its margin over E019 is H018's training exclusion.
2. **W1 is the one LOSS** for the prior block (+1.63 s). By airport, the loss sits at **LTFM (share 0.58) and EHAM (0.42)**; LFPG, named in advance, carries 0.10 (D4-C7). W1's validation priors come from 8 post-February source months, but **staleness as the cause is untested**. LTFM is both the largest pooled gain (−1.94 s) and the largest W1 loss, which fits non-stationary priors there (observation). The other causal check (S1c) is a WIN (−1.12 s).
3. **D3-C2 is caused by training on the routed LIRF convention rows,** and excluding them fixes it (81 → 5 in the > 3 h band) with no cost on `NM_present_excl_LIRF` (within ±0.56 s on every development fold; R2 LOSS +0.37 s). **Elsewhere it has costs (D4-C8):** S1 `NM_present_LIRF` +7.76 s (one row; this blocks the promotion), and W1c `NM_missing_other` full +106.33 s (tail rows; bulk −133.27 s). It cannot be promoted because S1 does not WIN.
4. **S1 is decided by one row (D4-C9; a standing disclosure on the champion).**
   - **Row 192622644** (LIRF, NM-present, y 87,002 s, `d_sched` 87,001 s) carries 8.2 % of E019's S1 SSE. Committed predictions on it range from 2,513 to 22,473 s. E019's 8,136 s is the FS2 family's highest.
   - **Both Day 4 changes lowered that prediction** (E019 8,136 → E023 7,041 → E024 5,780 s), and S1 moved against them. The S1 constraint therefore binds changes that lower predictions on day-scale records; the D3-C2 treatment is one of them. A plausible cause (untested) is that removing convention rows with targets up to 131,167 s lowers the leaf values that reach day-scale records.
   - **Audit only (rule 10).** Without that row, S1 is a WIN for E023 and E024 against E019, and E023 meets criteria 1–3 (mean −2.19 s, q95 −1.53).
   - **It cuts both ways.** E023's W1 WIN is carried by row 183910286 (LIRF NM-present); without it, W1 is TIE.
   - **The other LIRF NM-present tail rows net to about 0** (S1: 270 rows, 0.00 s). E023's robust advantage is on R1–R3 and S1c, carried by the treated cell.
   - **No reading of criterion 2 changes.** E019 holds by rule, and it carries D3-C2 and D3-C3 into Days 5–7 and any submission.
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
| H018 v2: rule 8 S1 cell, +4 s central (−5 to +15), mechanism "LIRF NM-present tail predictions fall" | +7.76 s: inside numerically, but **the mechanism did not occur**. The value is the single day-scale row; the other 270 tail rows rose by 3 s on average (D4-C9) |
| H020 v1: the stated CatBoost mechanism | **False** for the installed version (X-D04-S01-0001) |
| **Advisor (D4-C10)**, H018: > 3 h band central 22 (80 % interval 12–40); W1 0 ± 1 s; W1c 0 to +7 s | 5; −1.28 s; −1.64 s (wrong sign) |
| **Advisor (D4-C10)**, H019: `NM_present_excl_LIRF` −0.5 to −4 s (central −2); all rows −0.5 to −3 s; W1 the most likely largest gain; LFPG, EGLL, LTFM to lead | −0.29 s; −0.40 s; W1 the only LOSS; LTFM only. Both primary failure modes were correct |
| **Advisor (D4-C16)**, `H018_review_v2.md` | Did not identify that one day-scale row would decide S1, and accepted H018's rule 8 tail mechanism, which did not occur |

**Corrections and process slips.**
- **D4-C1:** the v1 proposals' `created_utc` values were written by hand, not measured. Measured from v2 on.
- **D4-C2 to D4-C6:** version labels in two Implementation Plans, the `range_check_refs.json` commit order, H019's rule 8 wording, and a dropped twin-rule phrase restored by reading 4(a).
- **Container restart and usage-limit pause:** E023 was allocated in D04-S01 and run in D04-S02. **Its allocation records (gate, ledger, task ledger) stayed uncommitted for about 7 h across the restart,** against brief §4 (D4-C15). No result depends on it. E024's same-second allocation commit is the practice to keep.
- **Gate semantics (D4-C15):** E024's `gate.json` and ledger row say D04-S01, because `gate.py` copies `day` and `session` from the proposal. The gate record is not edited.
- **Ledger decisions (D4-C11):** the `decision` field was null for E019–E024. It is now filled: E019 and E022 PROMOTE, E023 and E024 REJECT; E020 and E021 none by design.
- **STATE.md was stale** during Day 4, the fourth phase running (D4-C13). It was rebuilt at the close.

## 8. Delegated work (INC-0005)

Implemented by `claude-sonnet-5-5` workers to the researcher's specification and reviewed by the researcher before commit:

| Commit | Work |
|---|---|
| D04-S01 start | Environment and data verification (`sessions/D04-S01/SESSION_START.md`). **The planned pipeline digest was never committed; no record depends on it (D4-C12)** |
| `ec8c5ad` | `scripts/range_check.py` (rule 12), baseline figures |
| `0794612` | Day 4 prior EDA (key coverage, incremental R², stability) |
| `7ae934f` | FS3 (`src/prc/priors.py`) and tests |
| `e9120a9` | `gbm.catboost`, `routed_catboost`, resource calibration |
| `99db208` | `range_check --bands`, joint-key EDA, single-training-month prior test |
| `e4c57f8` (main-session commit) | Also committed `research/day-04/eda/range_check_refs.json`, the output of the worker's `--bands` code, without the provenance line (D4-C3, D4-C12) |

Kept with the main session: every proposal, envelope, ack, allocation, interpretation and promotion decision; `route_train_exclude` (`7ea6b55`); the `route_check.py` `-` option (`8597e19`); the CatBoost calibration addendum (`af21355`); and both experiment launches (E023, E024). The Advisor was not delegated or substituted. The phase-close review audited the boundary: no delegated commit touched a proposal, review, ack, envelope, gate or allocation record, ledger, journal, STATE or summary. **INC-0005 is closed.** Delegation on Days 5–7 needs a new incident.

## 9. Open questions for Days 5–7

1. **The S1 constraint (finding 4; Missing Control 1).** A Day 5–7 candidate compared with E019 whose promotion needs S1 (or W1) states under rule 8:
   - the expected direction of its prediction on rows 192622644 (S1) and 183910286 (W1);
   - the `NM_present_LIRF` cell expectation, read as the single-row statistic it is.

   This is a disclosure, not a new reading of criterion 2.
2. **D3-C2 and D3-C3 remain in the champion.** January 2026 has 2.0–2.6 times the 2025 maximum of long-delay NM-missing rows. E023's treatment is the known fix, but it is not promoted.
   - **The hand-off base ruling (X-D04-S02-0001 (e)).** Under ruling R, E023 is the matched reference for a candidate that keeps `route_train_exclude: true` on FS2, and E024 for FS3. E023 is not a default base and not a de facto champion.
   - Such a candidate is judged against E019, and its criterion 4 includes H018 v2's clauses 1–2.
   - **Rule 10** covers E020's, E021's, E023's and E024's configurations. That includes variants differing only by backend or library build, unless they pre-register a mechanism for the difference.
3. **CatBoost on GPU** (Day 5). The H020 review's objections apply: ordered boosting, pre-collapse levels, CTR complexity, and a capacity control. Missing Control 3 also applies: a categorical-handling-only contrast, `get_all_params()` checks, a decision-tied rationale for CLASS-L or GPU, and a committed calibration script.
4. **Priors.** The researcher's planning judgement (not a finding) is that a further LightGBM-on-FS2 variant is not worth its cost. Before "LightGBM already holds the keys" can be used as a finding, it needs its controls: a within-key permuted prior and a K5-only block.

## 10. Phase close (X-D04-S02-0001)

- **ACCEPT** (confidence 0.85). The Day 4 decisions stand under the frozen rules.
- **Ruling H4. Day 4 holdout: 0 of 1, closed unused** (not a TIE).
  - There is no carry-over.
  - No `holdout_check.py` invocation with E023 or E024 as NEW is authorized, in any phase.
  - E019 is Day 5's phase-opening champion.
- **Corrections D4-C7 to D4-C16** are in `research/day-04/acks/PHASE_CLOSE_D04_ack_v1.md` and applied here.
- **INC-0005 is closed. INC-0004 stays open** (owner decision).
- **Advisor's forward view** (recorded only):
  - P(E023's true RMSE < E019's) is 0.85 on January 2026 and 0.65 on July 2026;
  - P(E019 is still champion at the Day 7 freeze) is 0.50.

*Finalised 2026-10-01T01:57:51Z (measured).*
