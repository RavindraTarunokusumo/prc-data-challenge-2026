# SESSION_START — D02-S01

- **Start (UTC):** 2026-09-28T18:11:06Z
- **Phase:** Day 2 — static and temporal structure (brief §11): how much signal exists without inferred operational state
- **Resolved researcher model:** `claude-opus-5-5` (session metadata: `session_context.model` = `claude-opus-5-5`, `external_metadata.last_served_model` = `claude-opus-5-5`), effort `high`
- **Advisor:** `advisor` subagent, alias `opus`, effort `max`; definition SHA-256 `30fff5dd3c54…` verified by `gate.py status`
- **Git commit:** `d909de9` (`origin/main`, merge of PR #2 `day-1`); working branch `day-2` created from it
- **Dirty state at start:** clean working tree (git-ignored `.env`, `data/raw/`, `data/processed/`, `predictions/`, `runtime/ledger.sqlite` carried over in the container)

## Recovered state
Rebuilt from `research/STATE.md`, `research/day-01/DAY_SUMMARY.md`, the D01-S01 session summary, the task ledger, the session registry and the exchange mirrors.

- **Verification this session:** raw 14/14 SHA-256 match; silver matches its manifest; the six frozen files match `config/frozen.json`; `pytest` 90/90; `ruff` clean. 4 vCPU, 15 GB RAM, 28 GB free disk.
- **Network allowlist** read (`config/network.yaml`).
- **Champion:** E005 (H004 ridge, FS0). Development mean 482.73 (R1 477.8, R2 323.5, R3 431.6, S1 670.0, W1 510.7). Day 1 holdout: WIN (411.29 vs 514.74). Phase-opening champion for Day 2.
- **Accepted findings:** H002, H003, H004 promoted in sequence (Day 1 chain).
- **Rejected:** H005 (raw anchor), H007 (XGBoost FS0).
- **Inconclusive:** H006 (LightGBM FS0, dev mean 377.87). Its margin runs through LIRF NM-missing rows and the block-at-schedule convention (label T); on NM-present rows it beats E005 by 31–40 s bulk on every fold (C1).
- **Standing Advisor rules:** 1 tail attribution; 2 forward exposure (pre-register S1c/W1c sign); 3 holdout only via phase close; 4 calendar-month identity; 5 all folds + H with W1c fallback; 6 row concentration (B4); 7 NM × LIRF subgroup disclosure; 8 recording-convention disclosure. Batch conditions B1–B4 (Day 1 chain) are carried as practice.
- **Remaining budget:** promotional cloud credit (`rate_limit_info.status` = `allowed`). Holdout: 0 of 1 day-02 accesses used.
- **Last exchange ID:** X-D01-S01-0004 (closed). Next: X-D02-S01-0001.

## Open questions (from DAY_SUMMARY §5)
1. LIRF block-at-schedule convention and NM-missing rows (standing rule 8).
2. Trusting day-scale anchors (≥ 20,000 s).
3. Structural separation of populations (NM-present / NM-missing / LIRF convention).
4. Static structure: stand, aircraft type, operator, destination, local time (brief Day 2 theme).
5. January 2026 anchor tail (EHAM 3–9 Jan), not reproduced by any fold.

## First planned action
Target-free and training-fold-only EDA of static and temporal keys (stand, type, operator, destination, local time), then a batched Day 2 proposal set for review exchange X-D02-S01-0001.
