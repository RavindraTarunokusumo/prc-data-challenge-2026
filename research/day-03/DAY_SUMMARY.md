# Day 3 summary: congestion reconstruction (DRAFT, pending phase close X-D03-S01-0003)

**Session:** D03-S01. **Branch:** `day-3` (PR #5).
**Provenance:** INC-0004 is open (launch arguments against session metadata) and covers every D03-S01 artifact. The container restarted twice in D03-S01: before X-D03-S01-0001 attempt 2, and after E019.

## 1. The Day 3 question and its answer

**Question (brief §11):** does the reconstructed traffic state around a departure reduce error beyond static and anchor structure?

**Answer: yes, modestly and consistently, split roughly evenly between pushback-time state and in-taxi state.**
- **C (congestion)** is H015 − E017 on NM-present rows outside LIRF, with the training procedure held fixed.
  - **−6.75 s** (q95 −5.97), WIN on all 7 folds.
  - The NM-present bulk improves on every development fold.
  - No single row dominates any fold.
  - This clears the pre-registered −6.0 s floor by 0.75 s.
- **Decomposition** on the same population, adding exactly:
  - **P (at the off-block proxy): −3.47 s;**
  - **T given P (during the taxi): −3.28 s.**
  - Each is consistent (7/7 WIN), but each is below the floor on its own.
- **The EDA's picture of T dominating (10–12 s after the anchor) did not survive in the model.** It partly re-measured the anchor, as the v1 review warned.

**The candidate H015 v2** (E019; congestion on FS1, with the LIRF NM-missing subgroup routed to E005's model):
- it is −38.23 s against the champion E005 (7/7 WIN, criteria 1–3 pass);
- criterion 8 is 0.0 by construction;
- it reproduced byte-for-byte (criterion 6).

**It is not falsified. Its promotion is pending this phase close and holdout access (rule 9).**

## 2. What was built

| Artifact | Purpose |
|---|---|
| `src/prc/congestion.py` | 10 P and 5 T congestion features from admissible movement records. Masking-invariant on real data (1,919,370 rows). **Since `63923e2`, no P feature depends on the row's own takeoff time** (exact self-exclusion) |
| `features.fs2`, `fs2_p` | FS1 + 15 congestion columns; FS1 + the 10 P columns |
| `src/prc/models/routed.py` | Routed Tier 2 model: LIRF NM-missing rows go to a fold-local E005 ridge, the rest to LightGBM |
| `scripts/route_check.py` | Routing integrity: routed rows equal the champion; non-routed rows equal the unrouted twin |
| `scripts/check_fs2_v2.py` | Target-free checks: masking invariance, the old-to-new P diff, LIRF NM-missing counts by month |
| Tests | 123 pass (including two P-feature property tests that fail on the v1 code); ruff clean |
| EDA | `research/day-03/eda/congestion.json` (never-validation months), `fs2_v2_checks.json` (target-free) |

## 3. Advisor exchanges

| Exchange | Content | Decision |
|---|---|---|
| X-D03-S01-0001 (attempt 2, after a container restart) | H015 v1, H016 v1, H017 v1 | **REVISE ×3.** False forward-risk counts; row 192622644 could decide the C clause; five "P" features carried T bits on 0.086 % of rows; the noise scale was on the wrong population |
| X-D03-S01-0002 | H015 v2, H016 v2, H017 v2 | **ACCEPT ×3** (0.85, 0.88, 0.85), with a code freeze for the chain and recording conditions |
| X-D03-S01-0003 | Phase close | Pending |

## 4. Experiments (all sequential, all within class)

| E | Hypothesis | Model / features | Dev mean | Runtime / RAM | Result |
|---|---|---|---|---|---|
| E019 | H015 v2 (candidate) | routed LightGBM, FS2 | **444.49** | 954 s / 4.76 GB | Clauses 1–4 not met |
| E020 | H016 v2 (R ablation) | LightGBM, FS2 | 321.95 | 1,181 s / 4.62 GB | Clause 3 of H015 not met: bit-identical outside the routed rows, **cross-container** |
| E021 | H017 v2 (P/T) | LightGBM, FS2_P | 372.14 | 1,071 s / 4.86 GB | Readings 1 and 2 below the floor |
| E022 | H015 v2 reproduction (seed 43) | as E019 | 444.49 | 1,339 s / 4.63 GB | **Criterion 6 PASS; all 8 prediction files byte-identical to E019** |

## 5. Champion

- **E005 (H004 ridge on FS0) remains champion until the phase close decides.** Development mean 482.73.
- **Candidate: E019 (H015 v2),** development mean 444.49: −38.23 s against E005, with every fold a WIN.
- **Proposed phase-close holdout access** (frozen `phase_close` rule): E019 against E005 on H (December 2025). A LOSS would revert the promotion.

## 6. Findings

1. **C is real and small:** −6.75 s on the insulated population, uniform across folds (−5.35 to −9.52 s), with no dominant row.
2. **P and T contribute about equally** (−3.47 and −3.28 s) beyond E017, which already has the anchor `d_aobt3`.
3. **Deterministic LightGBM is deterministic on real data.** The outputs were identical across processes, across a container restart and across a seed change (E019 = E020 outside the routed rows; E019 = E022). This settles the Day 2 open question.
4. **The congestion block changes the LIRF convention mixture.**
   - Unrouted, FS2 is −56.87 s against E017 on all rows, almost entirely on LIRF NM-missing rows (tail share 0.72). The in-taxi counts are anchored at SCHED for convention records, so they carry the schedule delay more finely.
   - E020's criterion 8 statistic is below +6,500 s on every development fold (S1 +4,292). It is the first unrouted Tier 1 fit to manage that. H016 is not a candidate, so this is an observation.
5. **The routing's cost on 2025 folds is large:** E019 is +122.5 s against E020 on all rows (development mean 444.49 against 321.95). This is the price of declining the convention bet (ruling B). Its 2026 value depends on a convention rate that is not estimable.
6. **There are extreme predictions on NM-missing rows at the nine non-LIRF airports.**
   - Examples: −8,859 s on an EHAM row (y 482 s, `d_sched` 19,981 s) and 11,267 s on a LEBL row (y 1,315 s).
   - FS2 Tier 1 loses to E005 in bulk on this group on four development folds (rule 7 sign disagreement).
   - A candidate for Day 4.

## 7. Missed or corrected predictions (kept)

| Prediction | Outcome |
|---|---|
| H015 v1: LIRF NM-missing counts "52–115", July 2026 "2.4–5.3× any 2025 month" | **False.** July 2025 had 337 rows, more than July 2026's 276 (corrected in v2) |
| H015 v1: "a P feature never reads the row's own takeoff time" | **False** on 0.086 % of rows (fixed in `63923e2`) |
| H015 v1: noise scale on `excl_LIRF_NM_missing` | Wrong population; restated in v2 |
| Advisor (X-D03-S01-0002): C −3 to −5 s, P(promotable) 0.20 | C was −6.75 s |
| H015 v2: C −4 to −15 s | −6.75 s: inside |
| H016 v2: development mean 360–380; all rows −2 to −15 s; criterion 8 S1 +6,000 to +8,000 | **321.95; −56.87 s; +4,292: all outside** (the convention-row mechanism was underestimated) |
| H017 v2: T given P −4 to −12 s | **−3.28 s: below the range** |
| v1 review runtime note "38 vs 23 inputs" | Corrected to 32 vs 17 |

**Process slips.**
- Two container restarts: one killed an Advisor run, which was retried under the contract with `retry.yaml`.
- A transient outage of server-side command approval delayed the E019 checkpoint by about 10 minutes, and E019's analysis was committed after the second restart. Predictions were re-verified against the manifest.
- None changed a result.

## 8. Open questions for Day 4 (brief §11: historical priors and interactions)

1. **Unbounded predictions on NM-missing rows at the nine non-LIRF airports** (finding 6). Is this a structural fix (bounding, or a route like R) or a feature problem (`d_sched` extremes)?
2. **The convention bet** (findings 4 and 5). Should an unrouted FS2 model ever be a candidate, given that its 2026 exposure cannot be estimated? It is a governance question for the Advisor, not a threshold to tune.
3. **Fold-local target statistics and interactions** (airport × hour, airport × runway, stand → runway, operator, aircraft), with CatBoost as the natural candidate, per the brief.
4. **A binned-`d_aobt3` control** for congestion EDA (v1 review (g)), if more congestion features are proposed.
