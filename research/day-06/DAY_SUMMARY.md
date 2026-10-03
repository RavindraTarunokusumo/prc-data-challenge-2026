# Day 6 summary: adversarial science (DRAFT, for phase close X-D06-S01-0004)

**Session:** D06-S01 (2026-10-02 to 2026-10-03), on the owner's laptop. **Branch:** `day-6` (from `main` at `4ad18a1`).

**Provenance:**
- Researcher `claude-opus-5-5` (`--effort high`); Advisor the fixed `advisor` subagent (definition `30fff5dd3c54`).
- **INC-0012** (owner run window 21:00–21:30 on 2026-10-02; batch 2 run at once on "No, run now.").
- **INC-0013** (owner permission to delegate coding to `claude-sonnet-5-5`): used once (§8).

## 1. The Day 6 question and its answer

**Question (brief §3; advisor policy):** try to show that the champion E033 is wrong: its mechanism (attribution) and its performance claim (draw robustness).

**Answer: the champion survives both attacks, within what they could test.**
- **Attribution (batch 1, the ladder):** at equal weight, no cheaper or simpler second half substitutes for E031 in the blend. Every rung keeps only 39–66 % of E033's −3.96 s on normal taxis (`NM_present_excl_LIRF`); each removed ingredient carries a measurable part. Day 5's accepted scope ("this CatBoost configuration as a whole") stands; no "learner family" claim is made or widened.
- **Draw robustness (batch 2):** a fixed-seed GPU re-draw of the CatBoost half (E040), blended as E033 (E041), meets criteria 1–3 against E019's instance E026 with 7/7 WIN, within 0.40 s of E033 per development fold. Recorded as "robust to one further fixed-seed (GPU-only) draw". The Advisor rated this test as having almost no power to show E033 wrong.
- **Not attacked:** the 12-month composite SUBMIT procedure, and January's long-delay exposure (D3-C3).
- **E033 remains champion.** No Day 6 candidate exists.

## 2. What was built

| Artifact | Purpose |
|---|---|
| `research/day-06/sessions/D06-S01/run_window.sh`, `run_window_2.sh` | Pinned run-window launchers (start rule, status-only deferral, route check, own-path checkpoints) |
| `research/day-06/eda/d06_diagnostics.py` (+ test) | Residual correlation, exact 0.5/0.5 ambiguity decomposition, closed-set resolved-parameter comparison (delegated, INC-0013) |

No change under `src/`, `scripts/`, `config/`, `pyproject.toml` or `uv.lock` in Day 6.

## 3. Advisor exchanges

| Exchange | Content | Decision |
|---|---|---|
| X-D06-S01-0001 | H024–H028 v1 (ladder) | **REVISE ×5** (0.88): lopsided readings, rung A mislabelled, H027's seed refused by the runner, launcher unpinned. Ruling: batch experiments never NEW |
| X-D06-S01-0002 | H024–H028 v2 | **ACCEPT ×5**, conditions C1–C7 |
| X-D06-S01-0003 | H029, H030 v1 (draw robustness) | **ACCEPT ×2** (0.80, 0.83), conditions N1–N8; CLASS-L ruled for H029 alone |

## 4. Experiments (sequential; all controls; none a candidate; all never NEW)

| E | Proposal | What | Dev mean | Runtime / RAM | Reading |
|---|---|---|---|---|---|
| E035 | H026 v2 | rung B: E029 + codes CatBoost (E030) | 440.68 | 12 s / 3.37 GB | statistics carry part (D +1.34 s, q95 +1.65; 5/5 LOSS) |
| E036 | H024 v2 | CatBoost CTRs at complexity 1 (GPU) | 444.46 | 354 s / 6.73 GB | own reading INCONCLUSIVE (closed set: `data_partition`); values +4.96 s vs E031, +0.04 s vs E030 |
| E037 | H025 v2 | rung C: E029 + E036 | 440.04 | 10 s / 3.40 GB | combinations carry part (D +1.65 s, q95 +1.98; 5/5 LOSS), with the closed-set disclosure |
| E038 | H027 v2 | LightGBM twin (subsampling 0.8/0.8, seed 42) | 442.03 | 909 s / 6.61 GB | component; −0.42 s vs E029 |
| E039 | H028 v2 | rung A: E029 + twin | 441.44 | 14 s / 3.41 GB | twin does not reproduce the gain (D +2.43 s; 4/5 LOSS); averaging floor −1.53 s at seed 42 |
| E040 | H029 v1 | seed-42 GPU refit of E031 | 440.97 | 1,497 s / 7.13 GB | pure fixed-seed re-draw (resolved parameters identical); not byte-identical |
| E041 | H030 v1 | E029 + E040 | 438.97 | 9 s / 3.42 GB | robust to one further fixed-seed draw (criteria 1–3 vs E026, 7/7 WIN; \|Δ\| ≤ 0.40 s vs E033) |

All runs COMPLETE, within class, integrity (route check) PASS, no swap, clean tree at each run. E035–E039 ran inside the 2026-10-02 window (19:00:05Z–19:29:17Z); E040–E041 ran on 2026-10-03 at the owner's instruction.

## 5. Champion: E033 (unchanged)

- The phase-opening and phase-closing champion are both E033.
- Standing disclosures unchanged (D3-C1, D3-C3 restated, D5-C8, D5-C9, D5-C10, 1,000-iteration budget), with Day 6 additions proposed for the phase close:
  - **(attribution)** at equal weight, the codes CatBoost, the per-key CatBoost and a LightGBM perturbation twin each keep 39–66 % of E033's gain on normal taxis; the remainder needs E031's configuration;
  - **(draw record)** three draws of the blend (E033, E034, E041) differ by at most 0.60 s per development fold, all with 7/7 WIN against E026; CatBoost alone up to 1.57 s (W1).

## 6. Findings

1. **The categorical statistics carry part of the blend's gain** (rung B): replacing E031 by the codes CatBoost costs +1.34 s on normal taxis. E030 disagrees with E029 *more* than E031 does (RMS 93 against 81 s) but is 4.6 s less accurate: the statistics act through the CatBoost half's accuracy, not through extra disagreement.
2. **The CTR combinations hold E031's advantage** (E036 values, with the closed-set disclosure): per-key statistics alone are level with integer codes on normal taxis (+0.04 s) and 4.96 s behind complexity 4. In the blend (rung C) the combinations carry +1.65 s.
3. **Population split:** rung C is worse than rung B on normal taxis but better on all rows (−0.64 s): per-key statistics help outside `NM_present_excl_LIRF`.
4. **Generic averaging buys more than expected:** a LightGBM twin at half the CatBoost halves' disagreement gives −1.53 s on normal taxis (expected −0.2 to −1.2), 39 % of E033's gain.
5. **GPU refit at a fixed seed is not deterministic,** but unevenly: S1 reproduced to floating point (max 5.7e-7 s), W1c nearly, the other folds fully re-drawn (RMS change 21–33 s). No seed/GPU split is drawn (N4).
6. **The champion's margin is stable across the three draws measured** (≤ 0.60 s per development fold).

## 7. Missed or corrected predictions (kept)

| Prediction | Outcome |
|---|---|
| Rung C: D +0.1 to +1.4 (central +0.6); Advisor P(carries) 0.60 | D +1.65: combinations carry part |
| H024: E036 − E031 +0.5 to +3.5 (Advisor +0.2 to +3.0) | +4.96 (INCONCLUSIVE by closed set) |
| Rung A: G −0.2 to −1.2 | −1.53 |
| H027: residual correlation with E029 0.995–0.999 (all rows); runtime 600–850 s | 0.983–0.996; 909 s (no subsampling speed-up) |
| H029: byte-identical P 0.10 (Advisor 0.01) | not byte-identical |
| H029: largest dev-fold change ≈ 0.6 s (Advisor) | 0.84 s (W1) |
| Rung B, rung A, H030 readings | as forecast |

**Corrections and process slips (researcher):**
- **D6-C1 (v1 proposals):** H027 v1 used a seed the runner refuses (would have lost rung A); the ladder's readings were lopsided; rung A was labelled as support for the claim under attack; "ordered boosting" was wrong (all arms use plain boosting). All caught by X-D06-S01-0001 and fixed in v2.
- **D6-C2 (H029 v1):** E040 was described as "the draw Day 7's submission will be"; wrong (SUBMIT trains on 12 months). Withdrawn in the ack (N4).
- **D6-C3:** a "standing daily window" reading of INC-0012 was assumed, then withdrawn on the owner's "No, run now."
- **D6-C4:** one commit (`07d91ef`) failed lint (import order in the delegated test); fixed in `032c2da`.
- **D6-C5 (Day 5 record):** DAY_SUMMARY D5 §1 says "a second learner family adds signal", broader than H023 v3's accepted scope ("this CatBoost configuration as a whole"). Proposed as an appended correction; Day 6 did not test or widen it.
- **Operations:** on 2026-10-02 an external process held 4.3–5.2 GB of GPU memory during the window (no failure). The W&B re-sync of E035–E039 after analysis timed out twice (runs were mirrored at completion).

## 8. Delegated work (INC-0013)

- `research/day-06/eda/d06_diagnostics.py` and `d06_diagnostics_test.py`: implemented by a `claude-sonnet-5-5` worker to the researcher's specification; reviewed by the researcher. Written in the scratchpad during the window (repository untouched), placed after the window. SHA-256 `5fc21113613c675ec772390672132e78556ca6336bc736e10f7d8bc90c4e10b7`.

## 9. Open questions for Day 7

1. **The SUBMIT procedure** (12 training months, a fresh draw) is untested by any development fold. Whether more or more recent training months help either half is open.
2. **D3-C3** (January long-delay rows) remains untested.
3. CatBoost alone, other weights, or averages of draws: selection hazards; new proposals only (rule 10 covers E030–E041 configurations).
4. The 1,000-iteration budget (CatBoost still improving).
5. Neural models: not attempted.

## 10. Phase close

*Pending X-D06-S01-0004.*
