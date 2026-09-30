# SESSION_START — D04-S01

- **Start (UTC):** 2026-09-30T16:06:53Z (measured with `date -u`)
- **Phase:** Day 4, historical priors and interactions (brief §11), then the hand-off package (brief §3)
- **Resolved researcher model:** `claude-opus-5-5` (`get_session`: `configured_model`, `session_context.model`, `external_metadata.last_served_model`). Effort: metadata `high`, launch arguments `--model claude-opus-5-5 --effort medium` (**INC-0004**, open, non-blocking).
- **Delegation (INC-0005):** by owner instruction, worker subagents on `claude-sonnet-5-5` carry out verification, digests, implementation to specification, and experiment launches. Hypotheses, proposals, acks, gate allocations and interpretation stay with this session. The Advisor is unchanged.
- **Advisor:** `advisor` subagent, alias `opus`, effort `max`; definition SHA-256 `30fff5dd3c54…` (`gate.py status` OK).
- **Git commit:** `564f2c8` (`origin/main`, merge of PR #5, Day 3). Branch `day-4` created from it.
- **Dirty state at start:** clean working tree. Git-ignored `.env`, `data/raw/`, `data/processed/`, `predictions/` and `runtime/ledger.sqlite` carried over.
- **Container:** restarted since D03-S01 ended (boot id `b973b4fe-…` → `dd719b28-…`). 4 vCPU (`Intel(R) Xeon(R) Processor @ 2.10GHz`), 15 GB RAM, 28 GB free disk.

## Recovered state

Rebuilt from `research/STATE.md`, `research/day-03/DAY_SUMMARY.md` (final), the phase-close review `PHASE_CLOSE_D03_review_v1.md`, the task ledger, the session registry and the exchange mirrors.

- **Verification this session** (by a Sonnet worker, reviewed by the researcher):
  - raw 14/14 SHA-256 match;
  - silver matches its manifest and the frozen pin (`efde4262…`);
  - E019 predictions 8/8 match its manifest;
  - frozen files OK (`gate.py status`: `32c41c0f9331`);
  - `pytest` 123/123 pass; `ruff` clean;
  - ledgers agree: 22 experiments in SQLite and 22 in the JSONL.
- **Network allowlist** read (`config/network.yaml`).
- **Champion: E019** (H015 v2: routed LightGBM on FS2), development mean 444.49, holdout H WIN against E005 (−35.36 s). Standing disclosures D3-C1 to D3-C3.
- **Accepted findings:**
  - Day 3: C −6.75 s on `NM_present_excl_LIRF`, split into P −3.47 s and T|P −3.28 s.
  - Real-data determinism of deterministic LightGBM.
  - Day 2: M1, M2, M3.
- **Inconclusive:** H006, H009 v3, H013 v2. **Rejected:** H005, H007.
- **Standing rules 1–12**, batch conditions B1–B4, rulings H, B, R, H3.
- **Remaining budget:**
  - `rate_limit_info.status` = `allowed`. The promotional credit is spent; Day 4 runs on the owner's daily limit (INC-0005).
  - Holdout: Day 4 has 0 of 1 accesses used (rule 9).
- **Last exchange ID:** X-D03-S01-0003 (closed). Next: X-D04-S01-0001.
- **Last experiment:** E022. Next allocation: E023.

## Open questions (Day 3 DAY_SUMMARY §8)

1. Out-of-range predictions on non-LIRF NM-missing rows (D3-C2) and the January exposure (D3-C3). A treatment is its own hypothesis with an isolating ablation; rule 12 applies.
2. The convention bet: an unrouted candidate is admissible only under the routing answer's conditions.
3. Fold-local target statistics and interactions, with CatBoost.
4. A binned-`d_aobt3` control, if more congestion features are proposed.

## First planned action

1. A worker digest of the pipeline (data, splits, features, models, runner, compare tools).
2. Target-free and never-validation-month EDA for historical-prior keys (cardinality, coverage of the ranking months, stability across months).
3. One batched Day 4 proposal set for X-D04-S01-0001: the D3-C2 treatment first, then fold-local priors and CatBoost on top.
