---
schema: advisor-review-v1
hypothesis_id: H030
proposal_version: 1
proposal_sha256: 7695dc11a594aafec0e45149cdda3b94bcbab8f17e5614be6a5bfd08faeefd8a
exchange_id: X-D06-S01-0003
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.83
created_utc: 2026-10-03T08:41:46Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.83).** The shared findings and the binding conditions N1–N8 are in `H029_review_v1.md` and apply here unchanged. N5 governs how this reading is recorded.

**What H030 is.** E033's construction, with E040 in place of E031.
- The config block equals `experiments/E033/config.yaml` apart from that one component (parsed YAML comparison).
- It is CLASS-S. E033 and E034 took 8 s and 3.4 GB.
- Gating is status-only.
- **The three readings are pre-registered, mutually exclusive and exhaustive:** robust, spread above tolerance, and fragile.

**Three points are specific to H030.**
1. **The Research Question calls E041's draw "the draw Day 7's submission will be".** It is not. The SUBMIT fit trains on 12 months and is a fresh draw whatever its seed (N4).
2. **The tolerance clause compares a fixed-seed pair** (E041 − E033 = ½ (E040 − E031)).
   - That is the smaller kind of re-draw, so passing it is weaker evidence than E034's seed + GPU pass.
   - N5 therefore records "draw-robust" as "robust to one further fixed-seed (GPU-only) draw", with the labelled min–max over the three draws beside it. That min–max includes the seed + GPU pair E041 − E034.
3. **§Batch paraphrases criteria 1–2 more loosely than the frozen text.** Under N5, `compare.py`'s `passes_criteria_1_to_3` governs.

**The reading cannot realistically fail.**
- A "draw-fragile" outcome needs one of two moves: S1's q90 from −3.29 s to above 0, or criterion 1's mean from −5.62 s to above −1.0 s.
- The largest blend re-draw movement so far is 0.48 s, and a fixed-seed re-draw should be smaller.
- P("draw-fragile") ≈ 0.01.
- At 8 s of CPU it is still worth running: it gives the champion's third draw for rule 13. It is a measurement, not an attack that can show E033 is wrong.

## Scientific Validity

- **The mechanism identity is exact, row by row.**
  - Both blends use the same E029 file, and the blend is a fixed linear sum.
  - The routed rows are identical in E040 and E031 (both equal E029's), so they cancel.
- **The blend's RMSE change is not half the component's.**
  - RMSE is not linear. E034 moved R1 by +0.48 s where E032 moved it by +1.06 s, and W1 by −0.20 s where E032 moved it by −0.73 s.
  - The tolerance is read on the blend's own `fold_delta_rmse` (N5), so this is handled.
- **S1's tolerance clause is close to a single-row test.**
  - Row 192622644 has y = 87,002 s (recorded in E033's analysis). The stored blend predictions are E033 9,008 s and E034 8,639 s.
  - The 369 s change on that row alone accounts for about +0.24 s of E034's +0.27 s S1 movement. This is computed from the recorded S1 RMSE (627.92) and its 190,713 rows; no truth was read here.
  - **The 1.0 s line on S1 alone.** An E040 prediction on that row below about 7,900 s, or above about 14,100 s, would by itself put S1 beyond 1.0 s. The CatBoost draws so far are 10,976 and 10,237 s.
  - Rule 6 already applies. The S1 top-1 row share of `compare.py E041 E033` is therefore reported beside the tolerance reading. The proposal's Alternative Explanations already expect a single-row cause on S1.
- **The W1 row cannot flip sign by re-draw.**
  - On row 183910286 (y 13,865 s), E026 predicts 1,979 s and E033's blend 15,086 s.
  - The blend stays closer to y than E026 for any E040 prediction below about 43,500 s.
- **The byte-identical branch.**
  - If E040 equals E031, then E041 equals E033, and the "draw-robust" conditions hold trivially.
  - N5 records "no further draw" in that case. P 0.01.
- **Rule 10.**
  - The readings apply criteria 1–3 and the 1.0 s reproduction tolerance to a third draw.
  - The phase close ruled that criterion 6 "is satisfied as frozen … rule 10 forbids re-reading it". The proposal's Status ("no candidate, no champion change") already complies, and N5 writes the boundary into the record.
  - "An input to Day 7" means a disclosure and a phase-close question. Anything beyond that, such as averaging draws, needs a new proposal that states its selection.

## Novelty Relative to Existing Research

- This is the first third draw of a champion in the project. Its information value is incremental: rule 13's spread goes from one pair to three.
- It is not redundant with any rejected work. It re-submits no configuration as a candidate (rule 10).

## Experimental Isolation

- **Controlled:**
  - the LightGBM half is E029 byte for byte (manifest-verified; all 8 files match);
  - the weights are E033's;
  - the only difference is the CatBoost draw.
- **Inherited from H029:**
  - any resolved-parameter difference in E040 (N6);
  - any environment change, notably the driver (N2).

  Either is stated beside this reading.

## Validation Quality

- **Folds:** frozen and unchanged. All 8 folds are predicted, and H is never scored.
- **The reading:**
  - `compare.py E041 E026` checks the frozen criteria 1–3;
  - `compare.py E041 E033` gives the per-fold tolerance;
  - `mechanism_check.py E041 E033 NM_present_excl_LIRF` gives the mechanism population;
  - `d06_diagnostics.py diversity` gives the RMS change (N7: run together with E034);
  - `range_check.py E041 --bands` covers rule 12.
- **Integrity:** `route_check.py E041 - E029` runs in the launcher before the checkpoint.
- **Gating** is status-only and independent of E040's accuracy.

## Leakage Review

### Target Leakage

PASS

- No new input. The blend reads manifest-verified predictions with weights fixed a priori.
- The CTRs inside E040 are fold-local (`H029_review_v1.md`).

### Temporal Leakage

CONCERN

Inherited and not blocking: FS2's T features, and CTRs over post-validation months in S1 and W1, bounded by S1c and W1c. Nothing changes here.

### Competition Availability

PASS

Both halves can predict SUBMIT_JAN and SUBMIT_JUL. The composite SUBMIT path is still to be built and pre-registered on Day 7 (X-D05-S05-0001).

## Compute Review

### RAM

PASS

About 3.4 GB (E033 3.38, E034 3.40), inside CLASS-S's 4 GB. Nothing else runs at the same time.

### Runtime

PASS

- About 8 s, against CLASS-S's 5 min target and 450 s timeout.
- The 60 s start guard is generous. In practice E041 is late only if E040 is.

### Disk

PASS

About 60 MB of predictions.

## Weakest Assumption

**That passing a fixed-seed re-draw is evidence that the SUBMIT predictions are robust to the draw.**
- It bounds the blend's spread only from below.
- The seed + GPU pairs (E034 − E033, E041 − E034) are the relevant ones. N5 places them beside the reading.

## Missing Control or Ablation

- None for the reading. E033 is the first draw, and E034 the seed + GPU draw, as the proposal states.
- **Named, not required:** E041 − E034 is the only new seed + GPU pair. It is reported through N5's labelled min–max, not as a separate test.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:
- **H030 v1: exactly one allocation,** `uv run python scripts/gate.py allocate H030 v1` (purpose `primary`).
  - It is made second, after H029 v1, so it is expected to be **E041**.
  - The config is the Proposed Change block: components [E029, E040], weights [0.5, 0.5], seed 42, CLASS-S, folds R1, R2, R3, S1, W1, S1c, W1c, H.
  - It runs by `run_window_2.sh` (SHA-256 `edfe11df…dadf3e`), only after E040 is COMPLETE and route-checked, inside the 2026-10-03 window or a later owner window (N3).
  - Its reading follows H029 §Batch, with N5.
  - It is a control only: no candidate, never NEW, no holdout access, and its ledger decision is null.
- **No reproduction, `rerun` or further allocation** is authorized.
- **Conditions N1–N8 of `H029_review_v1.md` bind this run.**

Required acknowledgement path:
- `research/day-06/acks/H030_ack_v1.md`, citing the proposal hash `7695dc11a594aafec0e45149cdda3b94bcbab8f17e5614be6a5bfd08faeefd8a` and this review's hash.

## Revision

**None required.**

Non-blocking: the Research Question's "the draw Day 7's submission will be" and §Batch's criteria paraphrase are corrected in the record (N4, N5).

## Advisor Prediction

Probability of improvement:

| Event (H030 = E041) | P |
|---|---|
| E041 runs in the 2026-10-03 window | 0.78 |
| E041 runs before the Day 6 phase close | 0.92 |
| Given it runs: criteria 1–3 hold against E026 | 0.99 |
| Given it runs: 7/7 WIN against E026 | 0.95 |
| Given it runs: \|ΔRMSE\| ≤ 1.0 s against E033 on all five development folds | 0.94 |
| Reading "robust to one further fixed-seed draw" | 0.93 |
| Reading "criteria hold; spread above tolerance" (most likely via S1's single row, or R1) | 0.05 |
| Reading "draw-fragile" | 0.01 |
| Reading "no further draw" (E040 byte-identical) | 0.01 |
| More than half of S1's ΔSSE against E033 comes from row 192622644 (rule 6) | 0.50 |
| Development mean below E033's 438.87 (no direction expected) | 0.50 |

Expected magnitude:
- **`compare.py E041 E026` mean ΔRMSE:** −5.3 to −5.9 s (central −5.6).
- **Development mean:** 438.6–439.3 s (central 438.9).
- **Largest per-fold |ΔRMSE| against E033:** 0.1–0.8 s (central 0.3).
- **On `NM_present_excl_LIRF`:** the 5-fold mean ΔRMSE against E033 stays within ±0.4 s (P 0.85).
- **RMS prediction change against E033** (all rows, development folds): 6–22 s (central 14). W1c: 12–37 s.
- **Single rows:**
  - row 192622644: 7,800–10,300 s (E033 9,008; E034 8,639);
  - row 183910286: 12,500–17,500 s (E033 15,086; E034 13,272).
- **Resources:** runtime 7–15 s, peak RSS about 3.4 GB.

Primary expected failure mode:
- **Expected outcome:** the reading passes, as both earlier draws did.
- **Main risk, interpretive:** the pass is recorded as robustness of the SUBMIT predictions, which N4 and N5 prevent.
- **Operational:** E040 finishes late or fails, so E041 is deferred or recorded as "not run (component E040 <status>)".
