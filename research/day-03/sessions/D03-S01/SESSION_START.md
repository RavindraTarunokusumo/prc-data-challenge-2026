# SESSION_START — D03-S01

- **Start (UTC):** 2026-09-29T13:50:04Z (measured with `date -u`)
- **Phase:** Day 3, congestion reconstruction (brief §11, highest priority)
- **Resolved researcher model:** `claude-opus-5-5` served (`get_session`: `configured_model`, `session_context.model`, `external_metadata.last_served_model`). **The launch arguments disagree:** `--model claude-sonnet-5-5 --effort medium`, while the metadata effort is `high`. Recorded as **INC-0004** (open, non-blocking; owner decision).
- **Advisor:** `advisor` subagent, alias `opus`, effort `max`; definition SHA-256 `30fff5dd3c54…` verified by `gate.py status`
- **Git commit:** `c636850` (`origin/inc-0003-resolution`, open PR #4, merged into `day-3`). Branch `day-3` created from `origin/main` @ `07c5c3a` (merge of PR #3, Day 2), with PR #4's single commit merged in so that INC-0003's closure is carried.
- **Dirty state at start:** clean working tree. Git-ignored `.env`, `data/raw/`, `data/processed/`, `predictions/` and `runtime/ledger.sqlite` carried over in the container.

## Recovered state

Rebuilt from `research/STATE.md`, `research/day-02/DAY_SUMMARY.md` (final), the D02-S01 session summary, the phase-close review `PHASE_CLOSE_D02_review_v1.md`, the task ledger, the session registry and the exchange mirrors.

- **Verification this session:** raw 14/14 SHA-256 match; silver matches its manifest and the frozen pin (`efde4262…`); frozen files OK (`gate.py status`: `32c41c0f9331`); `pytest` 101/101; `ruff` clean. 4 vCPU, 15 GB RAM, 28 GB free disk.
- **Network allowlist** read (`config/network.yaml`).
- **Champion:** E005 (H004 ridge, FS0), by rule. Development mean 482.73. It trails every Day 2 Tier 1 fit by 51.5–59.6 s on NM-present rows on every development fold.
- **Accepted findings:** Day 1 chain H002 → H003 → H004. Day 2: M1 (static keys, ~7 s on `NM_present_excl_LIRF`, both procedures), M2 (anchor, −51.3 s on NM-present rows), M3 (convention via `d_sched`).
- **Inconclusive:** H006, H009 v3 (criterion 6), H013 v2 (criterion 8). **Rejected:** H005, H007.
- **Standing rules 1–11**, batch conditions B1–B4, rulings H, B, R (X-D02-S01-0006).
- **Missing controls named for Day 3** (phase-close review): (1) matched procedure for every mechanism reference; (2) a real-data determinism check by prediction-file hashes before criterion 6 is treated as a determinism check; (3) any explicit LIRF NM-missing treatment is its own hypothesis with an isolating ablation, a rule 8 pre-registration for S1 at July's rate, and fold-local fitting; (4) clause noise scale ≥ 3× the measured seed/procedure shift, or say why decisive.
- **Remaining budget:** `rate_limit_info.status` = `allowed`. Holdout: Day 3 has 0 of 1 accesses used (rule 9; nothing carries over from Day 2).
- **Last exchange ID:** X-D02-S01-0006 (closed). Next: X-D03-S01-0001.
- **Last experiment:** E018. Next allocation: E019.

## Open questions (DAY_SUMMARY §8)

1. The LIRF NM-missing convention decides promotion (criterion 8) and, on S1, accuracy. Ruling B: no new threshold; an alternative resolution needs a forward-risk rationale that does not rest on E006–E018.
2. Congestion reconstruction, built on the Day 2 disclosure tooling.
3. Comparison base: matched reference sharing the candidate's training procedure (E017 for deterministic FS1 candidates); criterion 4 carries every mechanism claim.

## First planned action

Congestion EDA: target-free on all months (feature distributions, coverage in the ranking file, month-edge effects), and target relationships only on never-validation months (Jan, Mar–Jun, Aug 2025), following the Day 2 EDA hygiene. Then implement the congestion feature block (P- and T-labelled groups kept separable, never reading other DEP rows' block times), with tests, and a batched Day 3 proposal set for X-D03-S01-0001.
