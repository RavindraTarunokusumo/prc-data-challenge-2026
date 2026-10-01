---
schema: advisor-review-v1
hypothesis_id: LAPTOP_REFS
proposal_version: 2
proposal_sha256: 4a4a03d75eeb6a5318003a9bb5d80ebbf5b34dda0df30b87af6bed61d95312da
exchange_id: X-D05-S04-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.88
created_utc: 2026-10-01T20:16:40Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.88).** Rule L v2 is adopted, and the ratifications are granted, under the authorized scope below.

All seven required revisions of `LAPTOP_REFS_review_v1.md` are met:

| v1 required revision | v2 | Verdict |
|---|---|---|
| 1. E028's role in route integrity | Removed. The reference is E029's routed rows at 1e-6 s. The criterion 8 expectation is restated as non-zero | **Met**, and the evidence is now strong (below) |
| 2. Premises | Interpreter, lock and library facts stated; the cause is given | **Met.** "Established" holds for the proximate cause only ((b)) |
| 3. Where the differences sit | Stated, twin folds included | **Met** |
| 4. Environment validity | Item 6: the environment, its ending events, and per-run recording | **Met.** Versions verified here. One recording gap closed by condition 3(a) |
| 5. Ratification | E026 as E019's instance; ratification requested for E029 and E028; E027 for curves only | **Met.** Ratified ((d)) |
| 6. Boundary disclosure | Item 4: per statistic, per instance | **Met** |
| 7. Operational records | INC-0010; corrections appended in STATE.md, the session record and the E026/E028/E029 analyses | **Met.** Verified as appended, not edited. INC-0010 records that the author of the swap change is unknown, which is the honest record |

The decisive revision is item 1: a route-integrity reference the laptop can meet. The R3 diagnosis alone would not have settled it. The checks run here do:
- **Target-free, real data.** FS2's and FS2_RAW's routed-ridge design matrices are **bit-identical on W1c, S1c and W1**. Each was captured at `Ridge.fit` with the target replaced by a constant, and the solve was skipped. With the researcher's R3, that is 4 of 8 folds, spanning 1 to 10 training months.
- **Synthetic GPU.** Two CatBoost GPU fits earlier in the same process leave the ridge's predictions bit-identical. On the same frame, `routed_catboost` and `routed_lightgbm` give bit-identical routed rows. This answers v1's Missing Control 2 for the tier-1 library and its thread settings.
- **Existing files.** E029 equals E026 bit for bit on every routed row of all 8 folds. E026 ≡ E027 (8 of 8 manifest hashes).

So `route_check.py <X> - E029` at 1e-6 s is attainable by a correctly routed laptop run on FS2 or FS2_RAW. My estimate is P ≈ 0.95 that H021 passes it.

**Verified here.** Checks were read-only, target-free, synthetic, or comparisons of existing prediction files. Scripts and outputs stayed in the session scratchpad, and Python ran with bytecode writing disabled. Nothing was written outside this review directory, and the working tree was clean before and after.
- **What I did not do.** No December target was read. `holdout_check.py` was not run. No model was fitted or scored on a real fold, and no real target entered any computation.
- **The experiment lock** was free at every check. Its last holder was E029, finished.
- **Host.** Boot `cf2c705b` is unchanged. Swap is 4 GiB, with `pswpin`/`pswpout` at 0.
- **Hashes.**
  - The four proposals match the envelope.
  - The six frozen files match `config/frozen.json`.
  - `.claude/agents/advisor.md` is `30fff5dd…`, as in `config/agents.yaml`. `scripts/gate.py` is `28e0977c…` and `uv.lock` is `efa4fd78…`.
  - The v1 proposal and review hashes match the four v1 acks. The X-D05-S04-0001 mirror verifies 2 of 2.
- **Environment (item 6)** matches the venv: CPython 3.13.15, polars 1.44.2 with a 16-thread pool, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, LightGBM 4.7.0 and CatBoost 1.2.10. `POLARS_MAX_THREADS` and `OMP_NUM_THREADS` are unset in the current shell.
- **Prediction files.** E026's, E028's and E029's match their manifests (8 of 8 each).
- **Code.** The worker writes `python` and `polars_threads` into every manifest. `tests/test_models.py`, `tests/test_worker.py` and `tests/test_isolation.py` pass, 55 of 55, all synthetic.
- **Secrets.** No credential assignment appears in the files changed this cycle. File names only were inspected.

## Scientific Validity

### (a) E029 is an attainable route-integrity reference

**Routed-ridge design matrix, FS2 path against FS2_RAW path** (`linear.ridge` on `feats.select(MVT_ID_mvt, role, month, y, *FS0)`, as `routed._routed` calls it; target replaced by a constant):

| Fold | Training rows × columns | FS2 data hash | FS2_RAW data hash | Bit-identical (data, indices, indptr) |
|---|---|---|---|---|
| R3 (researcher) | 1,757,038 × 111 | `61e5db11…` | `61e5db11…` | yes (permuted-target frames) |
| W1c | 153,706 × 98 | `d6e23eb7…` | `d6e23eb7…` | yes |
| S1c | 1,005,519 × 109 | `a17dcfdc…` | `a17dcfdc…` | yes |
| W1 | 1,611,189 × 111 | `eb94d77b…` | `eb94d77b…` | yes |

**Why the result should hold on the other folds:**
- `fs2` and `fs2_raw` differ only in `collapse_rare`, a `with_columns` on four non-FS0 string columns. That step comes before the same sort, the same congestion join and the same final sort.
- The FS0 columns therefore pass through identical operations in both builders.
- The diagnosis's frames went through a `permute` join that the worker does not perform. The four-fold check above did not, so the evidence covers the worker's own frames.

**Process state.**
- **Synthetic GPU check:** 300,000 training rows in 6 chunks, polars at 16 threads, H021's CTR settings at 30 iterations.
  - The ridge's predictions are bit-identical before and after two CatBoost GPU fits.
  - `routed_catboost` and `routed_lightgbm` give bit-identical routed rows (453), equal to the standalone ridge's.
- The researcher's `fs2_after_lgb` covers the LightGBM order.

**Residual risk.**
- R1, R2, S1 and H are not checked. I put the chance that one of them builds a different FS0 layout at about 0.05.
- The hypotheses pre-register the consequence: an integrity failure invalidates all-rows comparisons, and H023 is not allocated. That is a safe failure.

### (b) The cause

**What is established:**
- identical sparsity pattern and target;
- different design-matrix values between the standalone `fs0` frame and the joined FS2 frames;
- all paths bit-identical at `POLARS_MAX_THREADS=4`;
- the `sparse_cg` amplification is consistent with the 190.9 s single-row differences.

That is the proximate cause: the summation order of the ridge's polars statistics depends on the thread pool and the frame layout.

**What is not established:** which polars operation (filter partitioning, mean or std) carries it. The ruling does not need it. The proposal's text presents this as a reading, which is correct.

### (c) Environment of validity

**What item 6 detects.**
- Item 6 binds the right quantities. The manifest's `python` and `polars_threads` will detect an interpreter re-sync or a thread-pool change.
- The run commit pins `uv.lock`.

**What it does not detect:**
- that the venv still matches the lock (no per-run library record);
- the thread variables of the launching shell. The runner passes the shell's environment to the worker (`env = {**os.environ, …}`).

Condition 3(a) closes both by recording, with no code change.

### (d) Ratification

**E029.**
- The breach of H018 v2 review item 9 was benign. It was a reproduction of a reviewed configuration, with no selection, no candidate status and no holdout use.
- On this path the LightGBM is deterministic: E026 ≡ E027, and E029 = E026 on every routed row. An authorized fresh instance would therefore reproduce E029's files bit for bit.
- Refusing ratification would cost compute and yield no information. **Ratified for its three listed uses.**
- Its manifest's `code_commit` is wrong (D5-C6). The ruling rests on the prediction files, whose manifest SHA-256 values are verified here, not on that field.

**E028.** Ratified for the reduced role of item 1 only. It is never a route-integrity reference.

**E027.** No decision rests on it. Its curves may be cited.

### (e) Boundary disclosure

**The margins fit the measured differences:**
- 0.02 s against 0.0072 s for E026 and E029;
- 0.35 s against W1c's +0.339 s for E028;
- 200 s for criterion 8. This bounds the `NM_missing_LIRF` RMSE difference, which cannot exceed the largest single routed-row difference, 190.9 s.

**Zero margins.**
- The H018 v2 clause 2 and rule 12 rows are correctly zero: those populations contain no LIRF row.
- "Decided as computed; the flag is disclosure" is kept.

### (f) Items 2, 3 and 5

Accepted in v1. They are unchanged except for E026 replacing E027, which is byte-identical to it.

## Novelty Relative to Existing Research

A governance request; no experiment. It closes the Day 5 comparison blocker, which a reclaimed container caused: the cloud originals' git-ignored prediction files were lost.

## Experimental Isolation

Not applicable as an experiment.

**For the ruling:**
- E026 and E029 differ from their originals only on routed rows. Those rows are common to every laptop run on the FS2 or FS2_RAW path, so they cancel in comparisons between such runs.
- E028 differs everywhere, and is confined to the criterion 8 statistic, B3 against E005, and reported comparisons.

## Validation Quality

**Nothing frozen changes:** the folds, the metric, the bootstrap and the thresholds. The six frozen hashes are intact.

**Decisions are preserved.**
- The instance comparison reproduced the cloud E023-vs-E019 outcome to 1e-4 s (v1).
- The route-integrity reference is now attainable (a).

## Leakage Review

### Target Leakage

PASS

- No model is fitted or changed.
- The real-data check here replaced the target with a constant and computed no fit.

### Temporal Leakage

PASS

No feature or fold changes.

### Competition Availability

PASS

No input changes.

## Compute Review

### RAM

PASS

No experiment. The checks here peaked at 4.0 GB (real data) and 1.0 GB (synthetic).

### Runtime

PASS

Minutes of read-only checks.

### Disk

PASS

One review file. Scratch output stayed in the session scratchpad.

## Weakest Assumption

**That item 6's environment holds through the whole chain, and that a change would be noticed.**
- Possible changes: a `uv` re-sync to another interpreter, a library rebuild, or a launching shell that sets a thread variable.
- Any one of them ends the instances, or moves the routed rows' bits.
- The manifest fields catch the interpreter and polars changes. Condition 3(a) catches the rest by recording.

## Missing Control or Ablation

None blocking.
- The four unchecked folds (R1, R2, S1, H) are checked at run time by the hypotheses' own integrity clauses, with pre-registered consequences.
- The equal-weight E029 + H022 blend remains the named control for any attribution of complementarity to categorical handling (`H023_review_v1.md`).

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **Rule L v2 is adopted as written** (items 1–7):
   - E026 is E019's instance; E027 is cited for curves only.
   - E029 is E023's instance.
   - E028 is E005's instance in the reduced role only.
   - The identity and restrictions, the boundary-disclosure table, E026's H file as the holdout reference side, the environment of item 6, and E029's routed rows as the route-integrity reference for FS2 and FS2_RAW frames all apply.
2. **Ratifications:**
   - **E029**: as E023's instance, as the LightGBM component of an accepted H023 version, and as the route-integrity reference;
   - **E028**: for item 1's reduced role;
   - **E027**: curves only.
3. **Conditions:**
   - (a) **Environment record, every chain run.** The analysis records:
     - before allocation: the interpreter, the `uv.lock` SHA-256 at the run commit, and the launching shell's thread variables (expected: CPython 3.13.15, `efa4fd78…`, none set);
     - the venv's library versions, read once per session, and again after any `uv` command;
     - after the run: the manifest's `python` and `polars_threads` (expected 3.13.15 and 16).

     Any difference triggers item 6: no comparison against the instances without a new ruling.
   - (b) The item 4 flags are computed and reported for every comparison against an instance in the chain.
   - (c) E029 is a route-integrity reference for FS2 and FS2_RAW frames only.
4. **Not authorized:**
   - E028 as a route-integrity reference;
   - any allocation beyond a review's stated scope (D5-C5);
   - E026–E029 as NEW in any holdout comparison;
   - any edit to the manifests or records of E025–E029;
   - any change that ends item 6's environment during the chain, including `POLARS_MAX_THREADS`, without a new ruling.

Required acknowledgement path: `research/day-05/acks/LAPTOP_REFS_ack_v2.md`.
- It references the proposal hash (`4a4a03d7…`) and this review's hash.
- It adopts items 1–4.
- It is committed before any chain allocation.

## Revision

None required.

**For the record (no new version):**
- "Established" in the Cause section refers to the proximate cause ((b)).
- The worker-level FS2 = FS2_RAW equivalence rests on the four-fold check and the builders' code structure, not on the R3 diagnosis alone, whose frames passed through a `permute` join.

## Advisor Prediction

Probability of improvement (governance outcomes):

| Event | P |
|---|---|
| H021 passes `route_check.py <H021> - E029` on all 8 folds | 0.95 |
| H022 passes the same check | 0.95 |
| H023 passes, given H021 passes | 0.99 |
| An item 6 ending event occurs before the chain completes | 0.05 |
| A boundary flag fires on any statistic of H023 against E026 | 0.08 |

Expected magnitude:
- Against E026 or E029: instance shifts of at most about 0.01 s per fold.
- Against E028: up to about 0.34 s per fold on all rows, and up to about 191 s on single routed rows. Criterion 8 only, with a 200 s margin against +6,500 s.

Primary expected failure mode:
- **Primary.** An environment change mid-chain that is not recorded (an interpreter re-sync, or a shell that sets thread variables). The instances then stop being instances unnoticed. Condition 3(a) exists for this.
- **Secondary.** One of the four unchecked folds builds FS2_RAW with a different FS0 layout. H021's route check then fails, and H023 is not allocated: a safe failure, not a wrong result.
