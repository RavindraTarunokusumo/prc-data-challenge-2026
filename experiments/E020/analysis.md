# E020 analysis: H016 v2 primary (unrouted LightGBM on FS2; R ablation of H015 v2)

**Role:** reference and ablation. It is not a candidate, not reproduced, and never NEW (H016 v2, ACCEPT X-D03-S01-0002).

## Run

| Item | Value |
|---|---|
| Configuration | `lightgbm` on FS2 (`63923e2`), E017's parameters, seed 42 |
| Status | COMPLETE: 1,180.9 s, peak RSS 4.62 GB (CLASS-M: within class) |
| Development mean | **321.95 s**. R1 284.67, R2 248.97, R3 300.02, S1 420.73, W1 355.37; S1c 440.87, W1c 441.90 |

**Provenance (item 8).**
- **CPU:** Intel(R) Xeon(R) Processor @ 2.10GHz.
- **Container restart since the previous chain experiment: yes.** The container restarted after E019 completed. E020 ran under kernel boot id `b973b4fe-…`, and E019 under `ac2b2cff-…`.
- **INC-0004** open.

## H015 v2 clause 3: routing integrity (`route_check.py E019 E020 E005`): not met

| Fold | R1 | R2 | R3 | S1 | W1 | S1c | W1c | H |
|---|---|---|---|---|---|---|---|---|
| Routed rows | 168 | 115 | 52 | 337 | 58 | 337 | 58 | 88 |
| 3(a) max \|E019 − E005\| on routed rows | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 3(b) max \|E019 − E020\| elsewhere | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

- **3(a):** the routed part implements E005's model class exactly.
- **3(b):** E019 and E020 are **bit-identical outside the routed subgroup on all 8 folds.** The two runs were separate processes in **different container instances** (a restart intervened), so this is a **cross-container** determinism result for the deterministic FS2 LightGBM procedure. The determinism premise of criterion 6 stands.
- File: `research/comparisons/route_check_E019.json`.

## H016 v2 pre-registered expectations against outcomes

| Comparison | Expectation | Outcome |
|---|---|---|
| Development mean | 360–380 s (record note: 363.8–376.8) | **321.95 s: outside, better by about 40 s** |
| H016 − E017, all rows | −2 to −15 s | **−56.87 s** (q95 −37.02). Outside, larger. 5 WIN, 2 TIE (R3, W1c); criteria 1–2 pass, criterion 3 fails (EHAM +7.2 %) |
| H016 − E017, `NM_present_excl_LIRF` | Equal to H015 − E017 | **Equal:** −6.75 s, per fold identical to E019's (clause 3(b)) |
| H015 − H016, `LIRF_NM_missing` (R effect) | Full > 0 on ≥ 3 of 5 dev folds; bulk < 0 on S1 | **Full > 0 on 5 of 5** (+2,558 to +8,185 s); **bulk −4,291.85 s on S1** (< 0 on all folds). As pre-registered |
| Criterion 8 statistic against E005, S1 | +6,000 to +8,000 s | **+4,291.8 s: outside, smaller** |

**Rule 11 (reported whatever its sign).**
- **H016 − E017 on all rows is −56.87 s,** next to C = −6.75 s on H015 v2's clause population.
- Congestion *does* improve the all-rows metric of the unrouted model, but the reason is not queueing: the gain is concentrated on the LIRF NM-missing rows. See the next section.

## Where the all-rows gain comes from (disclosure)

- **Outside the routed subgroup, E020 is identical to E019** (clause 3(b)). E019 − E017 on those rows is small (C), and on `excl_LIRF_NM_missing` it is −3.35 s.
- **So the −56.87 s beyond that sits on the LIRF NM-missing rows (1–2 % of LIRF DEP rows).**
  - Tail share of the SSE change is 0.722 on the development folds.
  - Top-10 shares are 0.76–0.99 on R1, S1, W1 and S1c. W1's top-1 share is 0.74; W1c's top-1 share is 2.72 on a TIE.
- **Mechanism, as H016 v2's Mechanism section anticipated.** A convention record at LIRF has its T window anchored at SCHED, so FS2's in-taxi counts over (SCHED, *t_to*) grow with the schedule delay. The M3 convention signal then arrives through a second, finer channel than `d_sched`'s hour-resolution proxy.
- **This does not change H015.** Those rows are routed to E005's model in H015 by design (ruling B). The gain is exactly the convention bet that R declines, and its 2026 value depends on a convention rate that is not estimable.
- **Criterion 8 at +4,291.8 s on S1** (below the +6,500 s bound on every development fold: R1 +2,823.6, R2 +1,634.1, R3 +2,319.0, S1 +4,291.8, W1 +1,066.6).
  - This is the first unrouted Tier 1 fit to stay below the bound on all development folds (Day 2: +5,782 to +7,104 on S1).
  - **Recorded as an observation only.** H016 is not a candidate (rule 9, role) and cannot be promoted. Whether an unrouted FS2 candidate should be proposed is a Day 4 or phase-close question, and it would carry the same unestimable 2026 convention exposure.

**Rule 6.**
- Against E017 on all rows: dominant rows on W1 (top-1 0.74; the LIRF NM-missing row 183903219 was pre-registered) and on R3/W1c (on TIE folds).
- On `NM_present_excl_LIRF`: none (|top-1| ≤ 0.10), as pre-registered.

**Rule 7 against E005.** NM-missing rows at the nine non-LIRF airports lose in bulk on R1, R2, R3, W1 and W1c (+27.5 to +279.8 s), identical to E019 (the same predictions). This is E019's observation 1: extreme predictions such as −8,859 s on EHAM row 197540199.

## Next

H017 v2 (FS2_P, chain step 3). Then the conditional reproduction of H015 v2: clauses 1, 2, 3 and 4 are all not met, so the reproduction is due (Validation Plan step 4).

## Correction D3-C4 (appended 2026-09-30T07:06:50Z; X-D03-S01-0003)

The CPU model string for this run is **"Intel(R) Xeon(R) Processor @ 2.80GHz"**, not "@ 2.10GHz" as stated above (`provenance.yaml` is correct). E019 ran on "@ 2.10GHz", so the determinism results held across two CPU model strings.
