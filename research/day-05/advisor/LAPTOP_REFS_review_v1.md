---
schema: advisor-review-v1
hypothesis_id: LAPTOP_REFS
proposal_version: 1
proposal_sha256: e6d76c9c1729cdde8fa3cec9012052bc42b0866ac0306eee25888552bfcfbb94
exchange_id: X-D05-S04-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: REVISE
confidence: 0.90
created_utc: 2026-10-01T19:22:20Z
---

# Advisor Review

## Summary Assessment

**Decision: REVISE (0.90).** Rule L is not adopted in this exchange.

The instance idea is sound for E027 and E029, and the evidence for it is stronger than the request says. It fails for E028 in its main use, the route integrity check. Four of the request's factual premises are wrong.

1. **What holds (verified here).**
   - E026/E027 against E019, and E029 against E023, have **exactly equal per-airport RMSE at all nine non-LIRF airports on all seven scored folds**. Only LIRF differs.
   - The frozen comparison run on instances, `prc.evaluate.compare(E029, E027)`, **reproduces the committed `E023_vs_E019.json` to 1e-4 s.** Every fold point, every q10/q90, every outcome, the mean (−2.0357, q95 −1.3136) and the three criterion flags are equal. The one exception is R3's q10 (−2.1746 against −2.1745).
   - So E027 and E029 can stand in for E019 and E023 in `compare.py`, `mechanism_check.py`, `range_check.py`, the H018 clauses and the holdout reference side. Rule L items 2, 3 and 5 are acceptable as written.
2. **What fails: E028 as the `route_check` reference.**
   - On the laptop, the routed rows of E027 and E029 are identical to each other on all 8 folds.
   - **Both differ from E028 on every routed row of every fold, by up to 190.9 s** (table in (b)).
   - On the cloud, the same check gave 0.0 on all folds (`route_check_E019.json`, `route_check_E023.json`).
   - So any routed laptop run that follows E027's code path fails `route_check.py <X> - E028` at 1e-6 s. H023 (½ E029 + ½ H021) fails it with certainty.
   - The request asks for E028 in exactly this role, and H021, H022 and H023 pre-register INVALID on it.
3. **Premises that are wrong** (corrections D5-C1 to D5-C6, under Revision).
   - (a) "Same `uv.lock`." E027–E029 ran with lock `efa4fd78…` and the cloud runs with `39df945c…`. The difference is additions only (W&B), but the hash is not the same.
   - (b) "Different CPU" as the difference. The laptop interpreter is **CPython 3.13.15**, so the same lock resolves numpy 2.5.3, scipy 1.18.1 and xgboost 3.4.1. The cloud ran CPython 3.11.15 (D01-S01), with numpy 2.4.6, scipy 1.17.1 and xgboost 3.2.0. The brief and CLAUDE.md say Python 3.11. No record states this deviation.
   - (c) "Swap 0." **The VM has had 4 GiB of swap since boot `cf2c705b` (16:33:25Z),** so every one of E026–E029 ran with swap available. It was never used.
   - (d) "The reproductions already run under their original ACCEPTs." **E027, E028 and E029 are outside their reviews' authorized scope.** E029 is contrary to H018 v2 review item 9.
4. **The boundary disclosure (item 4) covers fold quantiles only.** It must cover every statistic decided against an instance, with a margin per instance.

**Verified here.** Every check was read-only, target-free, synthetic, or a comparison or re-scoring of existing prediction files. Scratch scripts and outputs stayed in the session scratchpad, and Python ran with bytecode writing disabled. Nothing was written outside this review directory and the exchange directory, and the tree was clean before and after.
- **What I did not do.**
  - No December target was read, and `holdout_check.py` was not run.
  - No model was fitted on a real fold.
  - Nothing was written to `research/comparisons/`: the frozen `prc.evaluate.compare` was called from the scratchpad.
  - The experiment lock was free at every check, so no experiment was running. The GPU held only the desktop (about 965 MiB).
- **Hashes.**
  - The four proposals match the envelope.
  - The six frozen files match `config/frozen.json`.
  - `.claude/agents/advisor.md` is `30fff5dd…`, as in `config/agents.yaml`, and `scripts/gate.py` is `28e0977c…`, as in the gate records.
  - `uv.lock` is `efa4fd78…`, as INC-0009 records.
  - The X-D04-S02-0001 mirror verifies 4/4.
- **Predictions.** The prediction files of E026–E029 match their manifests, 8/8 each. E026 and E027 are byte-identical on all 8 folds.
- **Instances**, from the committed `metrics.json` files and the existing prediction files: see (a) and (b).
- **Single rows.** Row 192622644 (S1) is 8,136.5 s in E026/E027, 7,040.9 s in E029 and 2,512.7 s in E028. Row 183910286 (W1) is 1,979.5, 7,938.4 and 2,507.3 s. Both agree with the cloud records.
- **Environment:** `.venv/pyvenv.cfg`, the package versions, `git diff 562e29f HEAD -- uv.lock`, `swapon`, `/proc/vmstat`, the current boot's kernel log and `.wslconfig` (see (d)).
- **Solver.** In scikit-learn 1.9.1, `Ridge(solver="auto")` on sparse input with an intercept resolves to `sparse_cg` with `tol=1e-4` (`_ridge.py`).
- **Tests.** `tests/test_models.py` passes 31/31 (synthetic only). No real-silver test was run.
- **Secrets.** `.env` is git-ignored and untracked. No credential-assignment pattern appears in tracked files; only file names were listed, and no value was printed.

## Scientific Validity

### (a) E027 and E029 are row-level instances outside the routed rows

**Per-airport RMSE, instance minus original** (committed `metrics.json`):

| Fold | Fold RMSE (s) | Non-LIRF airports (9) | LIRF |
|---|---|---|---|
| R1 | +0.0001 | 0 exactly | +0.0006 |
| R2 | −0.0004 | 0 exactly | −0.0024 |
| R3 | −0.0035 | 0 exactly | −0.0156 |
| S1 | −0.0072 | 0 exactly | −0.0276 |
| W1 | +0.0007 | 0 exactly | +0.0030 |
| S1c | −0.0001 | 0 exactly | −0.0002 |
| W1c | +0.0003 | 0 exactly | +0.0014 |

The figures are the same for E026, E027 against E019 and for E029 against E023 (to 1e-5).

**Reading.**
- Exact float equality over thousands of rows at nine airports means the LightGBM predictions there are the same on both hosts. The difference sits at LIRF, where the routed rows take the ridge.
- **The E026 analysis ("CPU-architecture-dependent floating-point paths in the same LightGBM build") and the journal's E026 line ("not bit-stable from Intel Xeon to AMD Ryzen") are not supported.** Correction D5-C3.
- **This is why the instance comparison reproduces the original exactly.** In both E029 − E027 and E023 − E019, the routed rows are common to the two members of the pair, so they cancel. The rest is identical across hosts.
- The same holds for a candidate whose routed rows equal E027's.

### (b) E028 does not reproduce the laptop's routed ridge

Routed rows (LIRF and NM-missing; target-free silver columns), per fold:

| Fold | Routed rows | E027 = E029 | Rows with \|E027 − E028\| > 1e-6 s | Median \|Δ\| (s) | Max \|Δ\| (s) | Rows > 10 s |
|---|---|---|---|---|---|---|
| R1 | 168 | 168/168 | 168 | 0.068 | 0.090 | 0 |
| R2 | 115 | 115/115 | 115 | 0.013 | 0.050 | 0 |
| R3 | 52 | 52/52 | 52 | 0.17 | **190.9** | 1 |
| S1 | 337 | 337/337 | 337 | 0.041 | **60.1** | 2 |
| W1 | 58 | 58/58 | 58 | 0.17 | **63.3** | 1 |
| S1c | 337 | 337/337 | 337 | 0.037 | 4.66 | 0 |
| W1c | 58 | 58/58 | 58 | 0.15 | 0.29 | 0 |
| H | 88 | 88/88 | 88 | 0.013 | 0.083 | 0 |

**What the evidence shows.**
- **The ridge inside `_routed` is deterministic on the laptop:** E026 ≡ E027 byte for byte, and E027 = E029 on every routed row, although their LightGBM training sets differ.
- **But it is not the computation E028 performs.** E028 calls `ridge(fs0(view))`. The routed path calls `ridge(fs2(view).select(FS0 columns))`. On the cloud these two were bit-identical; on the laptop they are not.
- **The cause is not established.** The ridge is scikit-learn's `sparse_cg`, an iterative solve stopped at relative residual 1e-4, on an ill-conditioned one-hot plus standardized design. Any difference in input bits or in the order of floating-point reductions changes the iterate path. Most predictions then agree to about 0.01–0.2 s, and rows in poorly determined directions move by tens of seconds.
- **Candidate sources** (none tested):
  - frame layout or threading in polars (16 threads here, 4 on the cloud) feeding the quantile, median, mean and std fills;
  - BLAS threading state in the process;
  - the numpy/scipy versions in (d).
- **E028 against E005 is not "BLAS low-order bits" either.**
  - It differs at every airport on every fold: W1c +0.339 s on all rows, and LTFM +1.94 s on W1c.
  - The request reports the development folds only (max 0.0113 s).
  - `compare(E027, E028)` gives W1c −21.6558 s, against the committed E019 − E005 of −21.3170 s. All outcomes are unchanged.

**Consequences.**
- **Route integrity.** `route_check.py <X> - E028` cannot pass at 1e-6 s for a run on the FS2 frame path.
  - For H023 it cannot pass at all. Its routed rows are ½ E029 + ½ H021, and E029 differs from E028 on every routed row.
  - So rule L item 1, as written for E028, makes every pre-registered integrity clause in this batch fail.
- **Criterion 8** (`NM_missing_LIRF.delta_rmse_bulk` against E005, ≤ +6,500 s). Against E028 it will be small and non-zero, not "0.0". This is harmless against the bound, but the expectation must be restated.
- **Not affected.** Comparisons against E027 or E029 on `NM_present_excl_LIRF` and `NM_missing_other` exclude LIRF entirely, so the routed-ridge question does not touch them.

### (c) The instance differences are not a CPU effect alone

**Interpreter and libraries.**
- **Laptop:** `.venv` is CPython **3.13.15** (`pyvenv.cfg`; venv created 15:48Z, at the D05-S01 start).
  - The lock's `python_full_version >= '3.12'` branch gives numpy 2.5.3, scipy 1.18.1 and xgboost 3.4.1. INC-0007 records xgboost 3.4.1.
- **Cloud:** D01-S01 recorded Python 3.11.15 and xgboost 3.2.0. The lock's `< '3.12'` branch gives numpy 2.4.6 and scipy 1.17.1.
- **Unchanged:** LightGBM 4.7.0, CatBoost 1.2.10, polars 1.44.2, scikit-learn 1.9.1 and pandas 3.0.6.
- The brief (§11, Day 1) and CLAUDE.md say Python 3.11. Neither the D05-S02 verification nor INC-0007 records the interpreter; both checked the lock hash only.

**The lockfile.**
- E026 ran on lock `39df945c…`; E027, E028 and E029 ran on `efa4fd78…` (`gate.json`).
- The diff adds W&B and its dependencies and restructures environment markers. No pre-existing package changes version.
- E026 ≡ E027 byte for byte confirms that the addition did not touch the model path.

**Consequence.** The ridge path in (b) runs through numpy and scipy, and their versions differ between the hosts. So "different CPU" is not shown to be the cause of any difference. The request should state the facts and leave the cause open.

### (d) Swap

- **Configuration.** `C:\Users\rvind\.wslconfig` reads `[wsl2] memory=11GB swap=4GB`. It was modified at **16:30:17Z**, inside the INC-0008 OOM sequence (16:19–16:33Z).
- **When it took effect.** The current boot `cf2c705b` began at **16:33:25Z**, and its kernel log shows `Adding 4194304k swap on /dev/sdc` at boot. `swapon --show` lists 4 GiB.
- **Use.** `pswpin` and `pswpout` are 0 since boot, and no OOM event is logged. Swap was available to E026–E029 but never used, so their resource figures stand.
- **Records that say "swap 0" for this boot:**
  - `research/STATE.md` (Day 5 section);
  - D05-S04 `SESSION_START.md` ("Environment: WSL2 10,951 MiB, swap 0", measured at 16:58:33Z, 25 minutes into this boot);
  - the E026 analysis (Host);
  - this exchange's envelope.
- **INC-0007's closure condition (swap 0) no longer holds,** and INC-0008 does not mention the change.
- **Why it matters for Day 5.**
  - Brief §4: "No swap: an OOM kill is recorded as RESOURCE_FAILURE".
  - The runner's guard and `within_class` are RSS-based, and swapped-out pages do not count in RSS.
  - H021 and H022 are expected to approach the CLASS-M RAM target (`H021_review_v1.md`).

### (e) Allocation scope

| Run | Allocated as | What the original review authorized | Status |
|---|---|---|---|
| E025, E026 | H015 v2 reproduction | One conditional reproduction (E022, Day 3). The Day 5 laptop reproduction is the hand-off procedure (brief §3; HANDOFF_D04 §5, finalised under X-D04-S02-0001) | Covered by the hand-off |
| E027 | H015 v2 reproduction (curves) | Not covered: a second laptop reproduction | Outside scope (benign) |
| E028 | H004 v1 reproduction | One conditional reproduction (E009, Day 1) | Outside scope (benign) |
| E029 | H018 v2 reproduction | Item 4: only if criteria 1–3 passed against E019, and they failed (S1 TIE). Item 9: "Not authorized: … any other fit with `route_train_exclude: true` on a frozen fold" | **Contrary to item 9** |

- **Why the gate did not stop them.** `gate.py` refuses only a second *primary*. Reproduction allocations are unlimited, so the gate cannot enforce a review's reproduction scope. The researcher must.
- **Harm.** None to the science. These are reproductions of reviewed configurations, with no selection, no candidate status and no holdout use.
- **But the record must say so,** and the use of E028 and E029 needs ratification. Correction D5-C5.
- **A clean option for E019.** E026 is byte-identical to E027 and is within the hand-off's scope, so it can serve as E019's instance without ratification. The curves live in E027 either way.

### (f) The boundary disclosure

Item 4 flags a fold when its deciding bootstrap quantile lies within 0.02 s of 0. That covers fold outcomes only.

**Other thresholds are decided against the instance too:**
- criterion 1: the point estimate against −1.0 s, and q95 against 0;
- criterion 3: the airport ratios against 1.03;
- criterion 8: against +6,500 s;
- H018 v2's clause 2 (bulk dRMSE against 0 on R1, R2, R3 and W1);
- B3: S1c's point against 0.

**The margin must also fit each instance:**
- For E027 and E029, 0.02 s is about three times the largest development-fold difference (0.0072 s). It is adequate.
- For E028, the measured fold-level difference reaches 0.339 s (W1c). A 0.02 s margin does not describe it.

### (g) Items 2, 3 and 5

- **Item 2 (identity and restrictions).** Correct and necessary.
  - E029's gate record says `day-04`, a phase with 0 accesses, so `holdout_check.py` would accept it as NEW. "E029 is never NEW" closes the same loophole as ruling H4 did for E023 and E024.
- **Item 3 (E029's configuration inside a new blend candidate).** Rule 10 is not engaged.
  - The blend is a new configuration.
  - H023's own clauses (B2) require the CatBoost half to add signal beyond E029. The blend therefore cannot be promoted on E023's known margin alone.
- **Item 5 (holdout reference side E027).** Acceptable. E027's H file differs from E019's only on the 88 routed rows, by the mechanism in (b). The disclosure in (f) applies.

## Novelty Relative to Existing Research

- **This is a governance request; it proposes no experiment.**
- **The problem is real and new.** The git-ignored originals stayed on a reclaimed container, and the hand-off covered integrity, not availability.
- **The alternatives are correctly declined:**
  - editing manifests would rewrite completed records;
  - comparing `metrics.json` only would lose the bootstrap, rules 1, 6 and 7, and criterion 8.

## Experimental Isolation

Not applicable as an experiment.

**For the ruling itself:**
- E027 (or E026) and E029 differ from their originals only on routed rows, and those cancel in any comparison whose two sides share the laptop routed path.
- E028 differs from E005 on every row, and from the laptop routed path on every routed row.

## Validation Quality

- **Nothing frozen changes.** Folds, metric, bootstrap and thresholds are untouched; the six frozen hashes are intact.
- **The instance approach preserves decisions for E027 and E029.** This is demonstrated, not assumed: the frozen comparison reproduces the cloud outcome to 1e-4 s.
- **For E028 it does not preserve the route integrity check, which is defined at 1e-6 s.**
- **Environment scope.** An instance is an instance only within the environment it was produced in: interpreter, lockfile and the numerical state behind (b). A later re-sync to Python 3.11, a lock change or a library rebuild would end that, mid-chain.

## Leakage Review

### Target Leakage

PASS

- No model is fitted or changed.
- This review read development and diagnostic truth only through `prc.evaluate.truth_frame`, inside the frozen `compare`. No December target was read.

### Temporal Leakage

PASS

No feature or fold changes.

### Competition Availability

PASS

No input changes.

## Compute Review

### RAM

PASS

- No experiment.
- The read-only comparisons in this review peaked at 0.53 GB.
- The swap finding (d) bears on later RSS-based class checks, not on this request.

### Runtime

PASS

Minutes of read-only scripts.

### Disk

PASS

One review file per proposal. Scratch output stayed in the session scratchpad.

## Weakest Assumption

**That an instance which passes the frozen fold-level reproduction rule is interchangeable with its original at row level, for every use.**
- It is, for E027 (or E026) and E029: they are identical outside the routed rows, and the routed rows cancel against laptop runs on the same path.
- It is not, for E028 in `route_check`. A 0.011 s fold-level agreement hides routed-row differences of up to 190.9 s from the path the candidates use.

## Missing Control or Ablation

These are named, not designed.
1. **The cause of the laptop ridge path difference,** established on target-free evidence before the chain runs. One example of admissible evidence is permuted-target ridge fits on the frame paths involved, computing no metric, as the GPU calibrations did.
2. **Whether the CatBoost (FS2_RAW) path reproduces E027's routed rows,** if v2 chooses those rows as the integrity reference. The `_routed` code is shared, but the frame, the tier-1 library and its thread settings differ.

## Decision

REVISE

## Execution Authorization

Authorized scope: none. REVISE does not permit execution, and rule L is not adopted in this exchange.
- **No allocation** of H021, H022 or H023 v1.
- **Still allowed:**
  - target-free checks;
  - synthetic tests;
  - permuted-target calibrations that compute no metric;
  - comparisons of existing prediction files under the frozen functions (written outside `research/comparisons/`, or recorded as audit only).

Required acknowledgement path: `research/day-05/acks/LAPTOP_REFS_ack_v1.md`.
- It references the proposal hash and this review's hash.
- It appends corrections D5-C1 to D5-C6. No completed record is edited.
- It is committed before the v2 envelope.
- It authorizes nothing.

## Revision

**Required (minimal):**

1. **E028's role in route integrity** ((b)).
   - Remove E028 as the `route_check` reference, or show on committed laptop evidence that a correctly routed run on the candidates' code path meets it.
   - Whatever reference and tolerance v2 adopts must be attainable by a correctly routed laptop run, and must be fixed before the run. The choice is the researcher's.
   - Restate the criterion 8 expectation against E028 (not 0.0).
2. **Premises** ((c), (d)): replace "Same `uv.lock` … different CPU" with the facts.
   - Lock `efa4fd78…` (additions only) for E027–E029, `39df945c…` for E026.
   - CPython 3.13.15 with numpy 2.5.3, scipy 1.18.1 and xgboost 3.4.1, against the cloud's 3.11.15 with 2.4.6, 1.17.1 and 3.2.0.
   - Leave the cause open.
3. **Where the differences sit** ((a), (b)). State that E027 and E029 equal their originals at nine airports and differ only at LIRF, and that E028 differs everywhere (W1c +0.339 s). Report the twin folds, not only the development folds.
4. **Environment validity.** State the environment in which the instances hold, and the event that ends it: an interpreter, lock or library change, or a fix to the ridge path. Bind every run in the H021–H023 chain to that environment.
5. **Ratification** ((e)).
   - Disclose that E027, E028 and E029 were allocated outside their reviews' scope, E029 contrary to H018 v2 item 9.
   - Request ratification of those you rely on. Alternatively name E026 as E019's instance.
6. **Boundary disclosure** ((f)).
   - Extend item 4 to every frozen or pre-registered statistic decided against an instance.
   - Give a margin per instance, from its measured differences.
   - Keep "decided as computed; the flag is disclosure".
7. **Operational records** (D5-C1, D5-C2), before the v2 envelope:
   - an incident recording the swap change (who made it, when, and the owner's decision: restore swap 0, or keep it with the RSS-guard limitation stated);
   - the Python 3.13 interpreter (the owner's decision for Days 5–7);
   - corrected statements in STATE.md and the D05-S04 session record, as appended corrections.

**Acceptable as is:**
- E027 (or E026) as E019's instance and E029 as E023's, for `compare.py`, `mechanism_check.py`, `range_check.py`, the H018 clause statistics and the holdout reference side;
- item 2 (identity and restrictions), item 3 (rule 10 not engaged for a new blend) and item 5;
- the alternatives considered, and the refusal to edit manifests.

**Corrections to append** (D5-C1 to D5-C6). These are facts from Scientific Validity; no record is edited.
- **D5-C1. Swap.**
  - `.wslconfig` reads `swap=4GB`, modified at 16:30:17Z. Boot `cf2c705b` (16:33:25Z) attached 4 GiB of swap. It was unused: `pswpin` and `pswpout` are 0.
  - E026–E029 ran with swap available.
  - STATE.md, D05-S04 `SESSION_START.md`, the E026 analysis and this envelope say "swap 0". INC-0007's closing condition no longer holds.
- **D5-C2. Interpreter.**
  - The laptop runs CPython 3.13.15, so numpy 2.5.3, scipy 1.18.1 and xgboost 3.4.1. The cloud ran 3.11.15, with 2.4.6, 1.17.1 and 3.2.0.
  - This is unrecorded against the brief's Python 3.11.
  - The lock hash changed with W&B (additions only).
- **D5-C3. Location of the instance differences.**
  - E026, E027 and E029 equal their originals at nine airports. The difference is in LIRF's routed rows.
  - The E026 analysis's LightGBM/CPU attribution and the journal's "not bit-stable from Intel Xeon to AMD Ryzen" are not supported.
  - E028 against E005 is not "low-order bits": W1c +0.339 s, LTFM +1.94 s on W1c, with a `sparse_cg` solve at tol 1e-4.
- **D5-C4. Laptop routed-ridge path.** E027 = E029 on all routed rows. Both differ from E028 on every routed row, with a maximum of 190.9 s (R3). On the cloud the paths were bit-identical.
- **D5-C5. Allocation scope.** E027, E028 and E029 are outside their reviews' scope, E029 contrary to H018 v2 item 9. `gate.py` does not enforce reproduction scope.
- **D5-C6. E029 provenance.**
  - E029's `manifest.json` says `code_commit` `ed5151f`. That commit was made at 18:41:35Z, during E029's run (18:38–18:53Z); the run commit is `f89dc60`.
  - The predictions are `f89dc60`'s code. `ed5151f` leaves the LightGBM, ridge and feature paths unchanged, and the worker loaded its modules at start.
  - Practice: no commit under `src/` or `scripts/` while an experiment runs (INC-0008's "light work only").

## Advisor Prediction

These are for a v2 that keeps E027 (or E026) and E029 as instances, and fixes E028's role.

Probability of improvement (governance outcomes):

| Event | P |
|---|---|
| Any development-fold outcome of a Day 5 candidate against E027 differs from what it would be against E019 | ≤ 0.03 |
| The boundary flag fires on at least one fold or criterion in H023 against E027 | 0.08 |
| The CatBoost/FS2_RAW routed path reproduces E027's routed rows bit for bit | 0.50 |
| The laptop ridge path difference is traced to a cause before the chain runs | 0.60 |

Expected magnitude:
- Against E027 or E029: instance-induced shifts of at most about 0.01 s per fold.
- Against E028: up to about 0.34 s (W1c) on all rows, and tens of seconds on single routed rows.

Primary expected failure mode:
- **Primary.** A v2 keeps a 1e-6 s integrity reference that the candidates' path cannot meet, and the chain self-invalidates on routed rows that are irrelevant to every mechanism clause.
- **Secondary.** The environment changes mid-chain (an interpreter re-sync to 3.11, or a swap or memory change with a restart), and the instances stop being instances without anyone noticing.
