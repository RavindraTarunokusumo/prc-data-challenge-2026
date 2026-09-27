---
schema: advisor-review-v1
hypothesis_id: SPLITS
proposal_version: 2
proposal_sha256: 827e0319241fb5da37aa9eb956ca7073c5323756439212a03567e9af2d65d561
exchange_id: X-D01-S01-0002
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-09-27T11:57:52Z
---

# Advisor Review

## Summary Assessment

v2 resolves all six required revisions of review v1. In the six files to be frozen I found:
- no leakage path;
- no metric or evaluator bug;
- no unpinned input to the evaluation population.

Decision: **ACCEPT** the freeze of exactly the six pinned files.

**Verified here** (read-only; no December target was read):
- **Hashes.**
  - The proposal SHA-256 matches the envelope.
  - The six pinned hashes, the three supporting hashes (`regime_stats.json`, `gate.py`, `data.py`) and the v1 review hash all match the files on disk.
  - Silver matches both the frozen pin and its manifest.
  - Commits `312fb1d` and `a9d0b18`, which landed after the envelope, touch no frozen candidate.
- **Tests.** `uv run pytest` passes 83/83, and `uv run ruff check .` is clean.
- **Row counts.** Every pinned count reproduces. H was counted by rows only, without selecting target columns. SUBMIT_JAN + SUBMIT_JUL = 344,841. `month` equals the UTC year-month of `MVT_TIME_UTC_mvt` in every row.
- **LFPG runway shares.** The new target-free facts in §6.5 reproduce:

  | Month | 27L | 27R |
  |---|---|---|
  | Jan 2026 | 29.5 % | 0.0 % |
  | Jul 2026 | 20.4 % | 0.1 % |
  | Dec 2025 (partly reverted) | 12.7 % | 7.4 % |

- **Secrets.** No configured secret value (S3 keys, OpenSky password) occurs in any tracked file.

**Three findings change how the frozen rule must be read,** though none blocks the freeze. All three are measured or traced below.

1. **The rule certifies that a gain is real, not where it comes from.**
   - The probe is an oracle change of +60 s applied only to rows with y > 3,600 s (0.14–0.53 % of each fold).
   - It WINs all seven folds and passes criteria 1–3: mean dRMSE −1.30 s, q95 −1.09 s.
   - The proposal says the 1.0 s floor "is set at the tail-only sensitivity" and that "the bootstrap interval carries the tail variability". Neither holds on the v2 fold set.
   - The floor is therefore a minimum effect size, not a tail guard.
2. **The twin rule catches only sign reversals.**
   - When a candidate equals the champion on S1c and W1c, both twins are TIE and the S1 and W1 WINs still count.
   - A gain that exists only with post-validation training months therefore passes.
3. **The holdout "phase" is the day directory of the new experiment's proposal,** not the phase in which the access happens.

All three can be handled without touching frozen files, under brief §10 item 4 (the ablation supports the mechanism) and item 8 (Advisor objections). **Revision** states how I will apply them, so they can be pre-registered.

## Scientific Validity

**Status of the v1 required revisions**

| v1 item | Status | Evidence |
|---|---|---|
| R1 population and boundary | Resolved | <ul><li>The evaluator loads silver itself and checks its SHA-256 once per process.</li><li>It checks the frozen row count on every truth read.</li><li>`splits.py`, `metrics.py` and `evaluate.py` import only each other; `__init__.py` is frozen.</li><li>The AST closure test passes.</li></ul> |
| R2 holdout guard | Resolved; residuals in Validation Quality (d) | <ul><li>The phase comes from `gate.json`, both experiments must be COMPLETE, and the frozen limit is counted against the task ledger.</li><li>The access is logged before truth is read, and a test asserts this ordering.</li><li>`truth_frame` and `evaluate` refuse H and the final folds.</li><li>The holdout tests use synthetic truth.</li><li>`audit_dataset.py` refuses to run once `config/frozen.json` exists.</li></ul> |
| R3 promotion rule | Resolved | <ul><li>Paired bootstrap over airport × UTC-day clusters.</li><li>Every parameter comes from the frozen config, and nothing can be overridden by the caller.</li><li>The seed policy and the rerun quantity are specified.</li></ul> |
| R4 winter | Resolved | W1 (February) is in the promotion set, and H has a pre-registered decision use. |
| R5 S1 forward exposure | Resolved; the rule is lenient (finding 2) | The LFPG evidence reproduces, and S1c and W1c are frozen now. |
| R6 labels | Resolved | P/T/F are defined against *t_off* and *t_to*. Cross-month information is inadmissible and structurally absent. |

**Operating characteristics of the frozen rule**

Set-up:
- Truth comes from the real development and diagnostic folds.
- The references are constant fold-training medians with synthetic or oracle perturbations.
- No model or feature was evaluated, and no December data was used.

| Probe | Result |
|---|---|
| Null: two equally good predictors differing by N(0, 25 s) noise, 200 replications | <ul><li>Per-fold WIN rate 0.07–0.145 and LOSS rate 0.07–0.14 (nominal 0.10).</li><li>Criterion 2 passed in 1.0 % of replications and criterion 1 in 0 %.</li><li>The full rule never passed.</li></ul> |
| Power: a consistent bulk-only gain of about 1.1 s (rows with y < 3,600 s), 100 replications | <ul><li>Passes in 100 % of replications with 25 s seed noise.</li><li>Passes in 76 % with 100 s seed noise. Every failure is on the −1.0 s point threshold.</li></ul> |
| Tail-only oracle: +60 s on rows with y > 3,600 s (222–762 rows per fold) | <ul><li>WINs all seven folds, and every q10–q90 interval lies below 0.</li><li>Mean −1.30 s, q95 −1.09 s.</li><li>Passes criteria 1–3.</li></ul> |
| Twin construction: the tail-only oracle, but identical to the champion on S1c and W1c | <ul><li>S1c and W1c are TIE.</li><li>The S1 and W1 WINs are counted, and the rule passes.</li></ul> |

- **Calibration and power.** The rule is calibrated against noise and has adequate power at about 1 s.
- **The floor is below the tail-only sensitivity.**
  - W1 alone has 762 tail rows, and the oracle moves its RMSE by −2.09 s.
  - Even on v1's four folds, the tail-only mean was 1.10 s.
- **The tail change is not noise.** It is systematic in sign and spread over many airport-days, so the bootstrap correctly calls it real. Deciding whether it came from the claimed mechanism is a question of attribution, which is item 4.

**Weaknesses in the record (non-blocking)**
- **`created_utc` is not a measured time.** The proposal's `created_utc` (12:20:00Z) is later than:
  - the proposal file's write time (11:34:29Z);
  - the envelope (11:34:45Z);
  - this review (11:57:52Z).
- **Unread config.**
  - `promotion.winter_fold`, `criterion_2.twin_rule` and the whole `reproduction` block are read by no code.
  - Criterion 6 is therefore binding by pre-registration only.
  - The reproduction seed is not enforced; the worker takes it from the experiment's config.
- **EDDF omitted.** §6.5 leaves EDDF (+12 s) out of both lists of p90 differences. This is harmless.
- **`AOBT_3` labelling.** `AOBT_3` is labelled P by what it describes, but when the archived NM value became final is not established. The Days 5–7 causal-only variant must state this assumption, as it does for the runway.
- **Cost estimate.** The "1.75×" figure overstates the cost. Training volume in month-units rises by about 1.3–1.45×.

## Novelty Relative to Existing Research

Not applicable.
- This is the second exchange of the run, and the journal is empty.
- v2 revises SPLITS v1 and duplicates no completed or rejected work.
- Commit `312fb1d` postdates the envelope and is outside it, so it was not reviewed. It changes H001–H008 and adds `scripts/compare.py` and `scripts/holdout_check.py`.

## Experimental Isolation

For a freeze, isolation means that the frozen boundary contains everything that decides validation outcomes. It now does.

**Inside the boundary:**
- `config/splits.yaml`: folds, population pins, promotion and phase-close parameters;
- `splits.py` (masking), `metrics.py`, `evaluate.py`, `__init__.py`;
- the audit;
- silver, by hash;
- every scored fold, by row count.

`paths.py` and `data.py` are no longer on the evaluator's path.

**Residual, outside the boundary but auditable through recorded commits:**
- **The worker.** `worker.py` chooses the folds and the seed. It is also the only thing between feature code and unmasked silver.
- **The environment.**
  - `uv.lock` is tracked, and each allocation records the commit.
  - numpy does not guarantee `Generator.multinomial` streams across versions, so a lock upgrade mid-run could flip borderline fold outcomes.
  - Treat a `uv.lock` change after the freeze as needing a logged note.
- **The isolation test can be bypassed.** The forbidden set does not cover `from prc.paths import SILVER` followed by a direct parquet read.

## Validation Quality

**(a) Fold design.**
- **R1–R3** are rolling folds with no gap, so they are temporal analogues of Jan 2026.
- **S1 and W1** are seasonal analogues, and part of their training data comes after the validation month:

  | Fold | Post-validation training months |
  |---|---|
  | S1 | 3 of 9 |
  | W1 | 8 of 9 |

- **The month after validation is absent in every development fold,** as in ranking. For R3 that month is the holdout; for S1 and W1 it is the embargo. This also removes DEP-to-ARR links across the month end.
- **Winter now enters selection twice:**
  - through W1, which carries weight 1/5 in criterion 1 and can veto by LOSS;
  - through H at every phase close, where a LOSS reverts the phase's promotions.

  That answers R4.

**(b) Twin rule.**
- **Leniency.** A twin demotes its partner's WIN only if the twin itself is a significant LOSS. Forward-only gains therefore pass (finding 2).
- **W1c confound.** W1c trains on one month, so a LOSS there can mean data hunger rather than forward exposure. The effect is conservative, because W1 is not a required WIN.

**(c) Calendar-month identity (new finding).**
- In every development fold the validation calendar month (Feb, Jul, Sep, Oct, Nov) is absent from its training months.
- At test time, both Jan 2025 and Jul 2025 are in training.
- No frozen fold can therefore validate information keyed on calendar-month identity, such as month-of-year levels or same-month priors.
- This is inherent to one labelled year. §6.5 does not mention it, so it is recorded here.

**(d) Holdout.** The guard works as described. Three residuals remain:
- **The phase label comes from the proposal's day directory.**
  - A promotion in phase N may rest on an experiment allocated from an earlier phase's proposal, for example a rerun of a Day 2 hypothesis promoted on Day 3. The phase-N check is then refused.
  - Conversely, an access left unused in one phase can be spent later.
  - Neither case leaks data, but the first can silently skip the pre-registered check.
- **`holdout_compare` returns more than the decision needs.**
  - It returns full segment tables (by airport and by taxi band, with bias) for both experiments.
  - v1 R2 allowed aggregates, so this is compliant.
  - Over four to seven phase closes, however, it invites hypotheses adapted to the holdout.
- **`load_silver(unmask_holdout_for=<any string>)` unmasks December with only a ledger line.**

**(e) Cluster assumption.**
- Clustering by airport × UTC day treats airports on the same day, and consecutive days, as independent.
- Multi-day and clustered disruptions break that assumption, so the intervals are somewhat narrow. Examples are LTFM on 19–23 February and the January–February cluster.
- The null probe cannot detect this, because its noise is independent.
- Not blocking.

## Leakage Review

### Target Leakage

PASS

- **Masking.** The frozen masking is correct; it is tested on real silver for all ten folds.
- **Truth access.**
  - The evaluator is the only reader of truth for scored folds.
  - Truth for H and the final folds is refused everywhere except `holdout_compare`.
- **December.** December targets are masked by default, and no test reads them.
- **Residual.** The remaining risk sits in non-frozen model code (the isolation-test bypass) and is checked per hypothesis.

### Temporal Leakage

CONCERN

- **Causal folds.** R1–R3 and both twins are strictly causal.
- **Forward exposure.**
  - S1 and W1 train on post-validation months by design.
  - The frozen control catches only a significant reversal on the causal twin (finding 2).
  - Graded forward exposure is left to review (standing rule 2).
- **Documented in §6.5.**
  - S1's recency optimism: June targets are available to S1, whereas the real Jul 2026 test has nothing after Dec 2025.
  - The asymmetries at month edges.

### Competition Availability

PASS

- Each ranking month is scored with same-month information only.
- Cross-month information is excluded structurally.
- The labels are now usable.
- The LFPG runway facts for the test months reproduce.

## Compute Review

### RAM

PASS

Seven truth reads plus one `promotion_check` peak at 0.53 GB RSS.

### Runtime

PASS

- Seven truth reads take 0.43 s.
- `promotion_check` over 7 folds with 2,000 resamples takes 0.71 s.
- The test suite takes 9.3 s.
- CLASS-S.

### Disk

PASS

The freeze writes only `config/frozen.json` and one ledger line.

## Weakest Assumption

**The assumption.** The design assumes that a candidate transfers to Jan/Jul 2026 if it meets three conditions:
- its mean gain is paired-significant and at least 1 s;
- it WINs S1;
- it WINs two other folds.

**Why it is weak.**
- The rule establishes that a gain is real on the 2025 folds, not where the gain comes from.
- Two kinds of gain pass it, as measured above:
  - gains concentrated in the tail (0.2–0.5 % of rows);
  - gains that need post-validation months.
- Transfer therefore rests on attribution under brief §10 item 4, and no frozen code performs that attribution.

## Missing Control or Ablation

None blocks the freeze.

Two controls remain outside the frozen rule:
1. the tail/bulk attribution of each promotion margin;
2. a graded S1-versus-S1c and W1-versus-W1c contrast, not only a LOSS check.

Both can be computed from stored predictions and the frozen folds. They are required below as standing review rules.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

- **The freeze.** One run of:

  ```
  uv run python scripts/gate.py freeze \
    --proposal research/day-01/proposals/SPLITS_v2.md \
    --review research/day-01/advisor/SPLITS_review_v2.md \
    --ack research/day-01/acks/SPLITS_ack_v2.md
  ```

  - It freezes exactly the six files at the pinned SHA-256.
  - It is followed by the brief §13 checkpoint.
- **Lapse condition.** If any of the six files changes before the freeze, this ACCEPT lapses and a v3 is required.
- **Not authorized:**
  - any experiment, because each H### needs its own ACCEPT;
  - any change to the six files after the freeze, which requires an incident;
  - any read of December targets outside `evaluate.holdout_compare` under `phase_close`.

Required acknowledgement path: `research/day-01/acks/SPLITS_ack_v2.md`.
- It must reference the proposal hash (`827e0319…`) and this review's hash.
- It should also record two corrections:
  - finding 1: the 1.0 s floor is a minimum effect size, not a tail guard;
  - the proposal's `created_utc` is not a measured time.

## Revision

None required.

**Standing review rules.** This is how I will apply brief §10 items 4 and 8 from now on. Pre-register against them.

1. **Tail attribution.**
   - Every promotion claim reports, per development fold, the paired dRMSE on rows with y < 3,600 s next to the full-population dRMSE.
   - If most of the criterion-1 margin comes from rows with y ≥ 3,600 s, the hypothesis needs a pre-registered tail mechanism. Otherwise item 4 is not met.
2. **Forward exposure.**
   - Scope: hypotheses built on regime-sensitive keys (runway, stand, operator, airport × time) or on any fold-local prior.
   - They pre-register the expected sign of dRMSE on S1c and W1c.
   - An S1 WIN whose S1c point dRMSE is ≥ 0 is not evidence of July transfer, even though the frozen rule counts it.
3. **Holdout use.**
   - Proposals may cite H only through the phase-close outcome.
   - A phase's promotions must rest on experiments allocated from that phase's proposals.
   - If the phase-close check is refused, the phase's promotions stand as unverified and will be flagged at the next phase-close review.
4. **Calendar-month identity.** Features keyed on calendar-month identity must say so. Their development-fold evidence does not transfer ((c) above).
5. **Fold coverage.**
   - Every candidate predicts all seven scored folds, including W1c with its single training month, plus H.
   - Features that need a longer history pre-register their W1c fallback.

**Recommended** (non-frozen code; can be done at any time without an incident):
- **Seeds and folds.** The worker or gate takes the seed from the `reproduction` block according to the run's purpose, and requires fold H in every primary run.
- **Unmasking.** `load_silver` unmasks only for a gate-allocated experiment whose config lists a final fold.
- **Isolation test.** `test_isolation.py` also forbids `prc.paths.SILVER` and `read_parquet`/`scan_parquet` in `features.py` and `models/*`.
- **Compare CLI.** `scripts/compare.py` requires both experiments to be COMPLETE in the ledger.
- **Holdout CLI.** `scripts/holdout_check.py` persists only the decision quantities.
- **Lock file.** Allocation records include the SHA-256 of `uv.lock`.

## Advisor Prediction

Probability of improvement: not applicable, because no model experiment is proposed. P = 0.85 that no frozen file needs an incident-driven amendment before the Day 4 hand-off.

Expected magnitude: no direct effect on RMSE.
- Day 1 promotions from Tier 0 to GBM will clear every criterion by tens of seconds.
- From Day 3 on, P = 0.6 that at least one hypothesis fails only criterion 1 (a mean gain below 1.0 s) despite WINning S1 and at least two other folds. The researcher will then bundle features, and bundled hypotheses need leave-one-out ablations.
- P = 0.85 that every phase-close check on H in Days 1–4 returns WIN or TIE.

Primary expected failure mode: a promotion whose margin comes mostly from tail rows or from memorised post-validation regimes. Both pass the frozen rule, and such a gain then fails to appear in Jan/Jul 2026. P = 0.3 that at least one promotion in Days 2–4 is flagged under standing rule 1 or 2.
