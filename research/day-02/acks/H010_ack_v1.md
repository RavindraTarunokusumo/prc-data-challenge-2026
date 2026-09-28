# Acknowledgement — H010 v1 (exchange X-D02-S01-0001)

- proposal: `research/day-02/proposals/H010_v1.md`, sha256 `3e273bd053d99337e6877ed2b2a2212461feb620bb525c26697372a9790a3a4a`
- review: `research/day-02/advisor/H010_review_v1.md`, sha256 `d5756c014b8da15309df95bf4e7b63ff398347089e1c2bf102ce34f0cc2d3bd9`
- decision received: **ACCEPT** (confidence 0.75), conditional. Both hashes verified by the researcher.

**Adopted preconditions.** All of these must hold before `gate.py allocate H010 v1`:
- (a) An H009 version ≥ 2 has decision ACCEPT, and its acknowledgement is committed.
- (b) That version keeps FS1 exactly (`src/prc/features.py: fs1` as at `cba278d`, or byte-identical output), with the same model, parameters, folds and seed as H009 v1.
- (c) That version keeps its M3 clause: subgroup LIRF NM-missing, statistic full dRMSE, 3-of-5 rule.
- (d) The H009 primary run is COMPLETE.
- (e) No other experiment runs concurrently.

**Lapse rule adopted.** If (b) or (c) does not hold, this ACCEPT lapses and `H010_v2` is required.

**Mechanism correction.** The Mechanism section's claim that without `d_sched` "the model cannot scale its prediction with the time between schedule and takeoff" is **wrong** for FS1_NO_DSCHED. `hour_utc` and `weekday` (takeoff, T) against `sched_hour_local` and `sched_weekday_local` (P) give the delay at hour resolution plus a day-crossing bit. H010 − H009 therefore measures what **exact** `d_sched` adds beyond an hour-resolution proxy. A null M3 result would not show that the convention is absent.

**Shared evidence corrections.**
- The ranking-unseen shares are not 0 %: stand 0.08 %, operator prefix 0.26 %, destination 0.05 % against the Jan–Nov training vocabulary. They map to `__RARE__`.
- `created_utc` 2026-09-28T18:24:00Z was not a measured time. It postdates the commit (18:22:24Z) and the envelope (18:22:07Z).
