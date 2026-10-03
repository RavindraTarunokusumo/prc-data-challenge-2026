# Day 6 summary: adversarial science (FINAL; phase close X-D06-S01-0004 ACCEPT; holdout closed unused; E033 remains champion)

**Session:** D06-S01 (2026-10-02 to 2026-10-03), on the owner's laptop. **Branch:** `day-6` (from `main` at `4ad18a1`).

**Provenance:**
- Researcher `claude-opus-5-5` (`--effort high`); Advisor the fixed `advisor` subagent (definition `30fff5dd3c54`).
- **INC-0012** (owner run window 21:00–21:30 on 2026-10-02; batch 2 run at once on "No, run now.").
- **INC-0013** (owner permission to delegate coding to `claude-sonnet-5-5`): used once (§8).

## 1. The Day 6 question and its answer

**Question (brief §3; advisor policy):** try to show that the champion E033 is wrong: its mechanism (attribution) and its performance claim (draw robustness).

**Answer: no Day 6 result contradicts the champion's promotion, but neither Day 6 batch had real power against its performance claim (D6-C12).** The attacks that could (the 12-month SUBMIT procedure; January's long-delay exposure, D3-C3) were not run.
- **Attribution (batch 1, the ladder).** At equal weight, neither the codes CatBoost, nor the per-key CatBoost, nor a perturbation twin of E029 substitutes for E031 in the blend (the pre-registered non-substitution sentence; nothing more is inferred, D6-C9). The rungs keep 39–66 % of E033's −3.96 s on normal taxis, against the most favourable of three champion draws (41–70 % against the three-draw mean). Rung B ("statistics carry part") is at its threshold and depends on the draw (D6-C6); "statistics" and "combinations" are not separated from CatBoost's `data_partition` (D6-C7). Day 5's accepted scope ("this CatBoost configuration as a whole") stands; no "learner family" claim is made or widened.
- **Draw robustness (batch 2).** A fixed-seed GPU re-draw of the CatBoost half (E040), blended as E033 (E041), meets criteria 1–3 against E019's instance E026 with 7/7 WIN, within 0.40 s of E033 per development fold on all rows: "robust to one further fixed-seed (GPU-only) draw". On the mechanism population, though, the January analogue (W1) gain over E029 is −1.59, −0.31 and +0.40 s across the three draws (D6-C11). The Advisor rated batch 2 as having almost no power to show E033 wrong.
- **E033 remains champion.** No Day 6 candidate existed. **Holdout: closed unused (ruling H6).**

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
- Standing disclosures carried: D3-C1, D3-C3 (restated D5-C16), D5-C8, D5-C9 (updated below), D5-C10, the 1,000-iteration budget.
- **Day 6 additions (X-D06-S01-0004 item 3):**
  - **(attribution)** At equal weight, three substitutes for E031 fall short. D against E033 on normal taxis: rung B (codes CatBoost) +1.34 s, 5/5 development folds LOSS; rung C (per-key CatBoost) +1.65 s, 5/5 LOSS; rung A (LightGBM twin) +2.43 s, 4/5 LOSS (W1 TIE). They keep 39–66 % of E033's gain on normal taxis against the most favourable of three champion draws (41–70 % against their mean). Rung B is at its threshold (D +0.97 s against E041; D6-C6). The labels "statistics" and "combinations" are not separated from `data_partition` (D6-C7). No necessity claim (D6-C9): the scope remains "this CatBoost configuration as a whole".
  - **(draw record)** Three draws (E033; E034, seed + GPU; E041, fixed seed): on all rows the per-fold spread is ≤ 0.60 s and every draw has 7/7 WIN against E026. **On the mechanism population the per-fold spread reaches 2.00 s on W1, and clause 1's W1 gain over E029 is −1.59, −0.31, +0.40 s by draw** (updates D5-C9). CatBoost alone: W1 spread 1.57 s on all rows, 3.94 s on normal taxis. The evaluated and H figures are one draw; SUBMIT is a further draw (rule 13).

## 6. Findings

1. **Rung B: the categorical statistics carry part of the blend's gain against E033** (+1.34 s on normal taxis), **at the threshold and draw-dependent** (+0.97 s against E041; D6-C6), and read "as CatBoost resolves the configuration, `data_partition` included" (D6-C7). E030 disagrees with E029 more than E031 does (RMS 93 against 81 s) but is 4.6 s less accurate.
2. **E036's values (own reading INCONCLUSIVE; D6-C8):** per-key statistics alone are level with integer codes on normal taxis (+0.04 s) and 4.96 s behind complexity 4. This is *consistent with* the combinations carrying E031's advantage, but not separated from `data_partition`. Rung C's reading ("combinations carry part", +1.65 s) stands with that disclosure.
3. **Exploratory only (D6-C10):** rung C is worse than rung B on normal taxis but better on all rows (−0.64 s, a difference of two means; not pre-registered or bootstrapped).
4. **Generic averaging:** a LightGBM twin at about half the CatBoost halves' disagreement gives −1.53 s on normal taxis (seed 42), more than expected.
5. **GPU refit at a fixed seed is not deterministic,** but unevenly: S1 reproduced to floating point (max 5.7e-7 s), W1c nearly, the other folds fully re-drawn (RMS change 21–33 s). No seed/GPU split is drawn (N4).
6. **The champion's margin is stable across the three draws on all rows** (≤ 0.60 s per development fold); **on normal taxis W1 spreads 2.00 s** (D6-C11).

## 7. Missed or corrected predictions (kept)

| Prediction | Outcome |
|---|---|
| Rung C: D +0.1 to +1.4 (central +0.6); Advisor P(carries) 0.60 | D +1.65: combinations carry part |
| H024: E036 − E031 +0.5 to +3.5 (Advisor +0.2 to +3.0) | +4.96 (INCONCLUSIVE by closed set) |
| Rung A: G −0.2 to −1.2 | −1.53 |
| H027: residual correlation with E029 0.995–0.999 (all rows); runtime 600–850 s | 0.983–0.996; 909 s (no subsampling speed-up) |
| H029: byte-identical P 0.10 (Advisor 0.01) | not byte-identical |
| H029: largest dev-fold change ≈ 0.6 s (Advisor) | 0.84 s (W1) |
| **E036 − E030 (D6-C15):** Advisor −1.9 to −4.7 s (central −3.6); researcher −1.5 to −4.5 (central −3.4) | **+0.04** |
| **Closed-set violation (D6-C15):** Advisor P 0.08 | violated (`data_partition`) |
| **Rung C (D6-C15):** Advisor P("carries part") 0.12, D −0.15 to +1.4 s | "carries part", +1.65 |
| **H029 (D6-C15):** Advisor ±0.7 s on the normal-taxi mean (P 0.75) | +0.74 |
| **Advisor and researcher record (D6-C15):** both expected per-key statistics to carry most of E031's advantage over codes, and rung C most likely to carry | wrong in the same direction |
| Rung B, rung A, H030 readings | as forecast |

**Corrections and process slips (researcher):**
- **D6-C1 (v1 proposals):** H027 v1 used a seed the runner refuses (would have lost rung A); the ladder's readings were lopsided; rung A was labelled as support for the claim under attack; "ordered boosting" was wrong (all arms use plain boosting). All caught by X-D06-S01-0001 and fixed in v2.
- **D6-C2 (H029 v1):** E040 was described as "the draw Day 7's submission will be"; wrong (SUBMIT trains on 12 months). Withdrawn in the ack (N4).
- **D6-C3:** a "standing daily window" reading of INC-0012 was assumed, then withdrawn on the owner's "No, run now."
- **D6-C4:** one commit (`07d91ef`) failed lint (import order in the delegated test); fixed in `032c2da`.
- **D6-C5 (Day 5 record):** DAY_SUMMARY D5 §1 says "a second learner family adds signal", broader than H023 v3's accepted scope ("this CatBoost configuration as a whole"). Proposed as an appended correction; Day 6 did not test or widen it.
- **Operations:** on 2026-10-02 an external process held 4.3–5.2 GB of GPU memory during the window (no failure).
- **Phase-close corrections D6-C6 to D6-C15** (`research/day-06/acks/PHASE_CLOSE_D06_ack_v1.md`), applied here:
  - D6-C6 (rung B draw-dependent), D6-C7 (`data_partition`), D6-C8 (INCONCLUSIVE values not a finding), D6-C9 (no necessity claim), D6-C10 (finding 3 exploratory), D6-C11 (draw record on the mechanism population), D6-C12 (§1 wording);
  - **D6-C13:** E036–E039 never reached W&B (failed to initialise at completion); only E035, E040 and E041 are mirrored. The draft's "runs were mirrored at completion" was wrong;
  - D6-C14: the delegated script and closed-set output were placed about 21 s before the window closed (after the queue ended; no consequence); the test file's provenance line was missing (added); the lock file's `E041` text is a stale stamp;
  - D6-C15: the missed forecasts above.

## 8. Delegated work (INC-0013)

- `research/day-06/eda/d06_diagnostics.py` and `d06_diagnostics_test.py`: implemented by a `claude-sonnet-5-5` worker to the researcher's specification; reviewed by the researcher. Written in the scratchpad during the window (repository untouched); placed at 19:29:37Z, after the queue ended and about 21 s before the window closed (D6-C14 (a)). The test file's provenance line was added at the phase close (D6-C14 (b)). SHA-256 `5fc21113613c675ec772390672132e78556ca6336bc736e10f7d8bc90c4e10b7`.

## 9. Open questions for Day 7

1. **The SUBMIT procedure** (12 training months, a fresh draw) is untested by any development fold, and H cannot test it (SUBMIT trains on December; ruling H6 (f)).
2. **D3-C3** (January long-delay rows) remains untested.
3. CatBoost alone, other weights, or averages of draws: selection hazards; new proposals only (rule 10 covers E030–E041 configurations).
4. The 1,000-iteration budget (CatBoost still improving).
5. Neural models: not attempted.
6. Named by the phase close (not required): a run with `data_partition` equalised between complexity 1 and 4; a second draw of E030; the causal-only variant anticipated by the dataset audit.

## 10. Phase close

- **X-D06-S01-0004: ACCEPT** (0.84). The Day 6 decisions stand; E033 remains champion; no ledger decision changes.
- **Ruling H6:** "Day 6: 0 of 1, closed unused" (no comparison; not a TIE). No carry-over. No `holdout_check.py` with any of E035–E041 as NEW, in any phase.
- **Standing rule 14:** when several draws of a stochastic reference exist, any reading against it also reports the point contrast against each draw (exact identity, same rows). Disclosure only.
- **Incidents:** INC-0012 and INC-0013 closed; INC-0009 (amended, D6-C13), INC-0010 and INC-0004 stay open.

*Finalised 2026-10-03 (D06-S01).*
