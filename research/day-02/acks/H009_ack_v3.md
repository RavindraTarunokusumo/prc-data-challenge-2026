# Acknowledgement — H009 v3 (exchange X-D02-S01-0003)

- proposal: `research/day-02/proposals/H009_v3.md`, sha256 `f013c86f75d0cfb3b8643862cf3829991ad095a38f045f2e965e1f298f303a20`
- review: `research/day-02/advisor/H009_review_v3.md`, sha256 `7cc7a069f022d2594e2be89a2709e0cb256dd1a9883c9647a59387876b08d81e`
- decision received: **ACCEPT** (confidence 0.85). Both hashes verified by the researcher.

## Adopted preconditions (before `gate.py allocate H009 v3`)

- (a) This acknowledgement is committed.
- (b) `research/STATE.md` is refreshed, with a measured header time.
- (c) The E006 and E010 reuse conditions hold: `uv.lock` is `39df945c…`, `gbm.py` and `fs0` are unchanged, and silver is pinned. The analysis records H009's `gate.json` `uv_lock_sha256`.
- (d) `scripts/compare.py`, `scripts/mechanism_check.py` and `src/prc/attribution.py` stay unchanged from `5ba9230` until clauses 1–4 are computed. Any earlier change needs a new exchange.
- (e) No other experiment runs concurrently.

**Not authorized:**
- any change to features, parameters, folds, seed or clause code;
- any search or early stopping;
- scoring H outside the frozen phase-close check;
- redefining any population after the H009 run.

**Reproduction** (seed 43): only if H009 passes criteria 1–3 against E005 and none of clauses 2–4 is met.

## Criterion 8 resolution rule (recorded)

The LIRF bulk-trade objection (X-D01-S01-0004) is resolved if **both** hold:
- clause 3 is not met, so M3 is supported;
- `NM_missing_LIRF.delta_rmse_bulk` against E005 is ≤ +6,500 s on every development fold.

B3 carries: an S1 WIN with an S1c point dRMSE ≥ 0 against E005 is an objection.

## Residual exposures (recorded; not a change of claim)

1. **Late departures in clause 2(a).** Rows with `d_sched` ≥ 3,600 s and a normal taxi time carry 16–27 % of E006's SSE in `NM_present_excl_LIRF`.
   - Differences there come from the trees' use of `d_sched`, not from static structure.
   - Same-input evidence (E011 against E006): ≤ 1.4 s on the development folds.
2. **W1c sensitivity.** The same rows carried 22 of W1c's 30 s in E011 against E006. W1c is the likeliest twin to come out LOSS, and a LOSS there would void a W1 WIN (frozen twin rule).
3. **LIRF late departures in clause 2(b).** About ±2.0 s on S1. The clause needs two failing folds to falsify, so it stays insulated.
4. **Row 183910286 in M2 on W1** (LIRF, y = 13,865 s, `d_sched` = 13,862 s). It can move W1 by about 11 s. Row 192622644 can move S1 and S1c by a similar amount. Both are small against the expected −40 to −100 s.
