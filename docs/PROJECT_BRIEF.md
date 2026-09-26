# PRC 2026 — Autonomous ML Research Project

**Operating brief — Claude researcher + Claude Advisor contract**
**Version:** 3.0 (supersedes v2.0, "Codex-orchestrated Gemini research contract")
**Canonical repository:** `RavindraTarunokusumo/prc-data-challenge-2026` (public)
**Team:** `genuine-cabbage`

> v3 changes *who* does the research and *where* Days 1–4 run. It does not change
> what counts as good science. Every v2 integrity rule (frozen splits,
> pre-registration, immutable history, leaderboard isolation, contamination ban)
> carries over unchanged unless this document explicitly says otherwise. The
> substitution is recorded as protocol deviation `docs/incidents/INC-0001`.

---

## 1. Objective

Predict **taxi-out time** for the PRC Data Challenge 2026 from aviation movement
data, primary metric **RMSE**.

Research question:

> **Can a Claude research agent, reviewed by a fixed Claude Advisor at maximum
> reasoning effort and constrained by deterministic, repository-auditable
> governance, independently discover competitive methodology on consumer-grade
> and cloud-CPU compute?**

This is an independent hobby research project. There is no institutional
supervision, no manual feature selection or hyperparameter tuning, no human
interpretation of intermediate results and no leaderboard-guided optimisation.
The human operator may start, stop or recover the run for safety,
infrastructure or explicit policy reasons only. Every intervention is logged in
`docs/incidents/`.

## 2. What changed from v2

| Area | v2.0 | v3.0 |
|---|---|---|
| Primary researcher | Gemini 3.8 Flash via Antigravity `agy` | **Claude, main Claude Code session** (`claude-opus-5-5`, effort `high`) |
| Advisor | Codex Advisor/Orchestrator | **`advisor` subagent** (`.claude/agents/advisor.md`, Opus, effort `max`) |
| Orchestration | Codex drives `agy` over WSL2 | Researcher session spawns the Advisor via the Agent tool; exchanges mirrored to `orchestration/advisor-exchanges/` |
| Days 1–4 compute | RTX 5060 laptop (WSL2) | **Claude Code cloud container**: 4 vCPU, 15 GB RAM, ~30 GB disk, **no GPU** |
| Days 5–7 compute | Laptop | Laptop, operated by the project owner (out of scope for the cloud session) |
| Budget | n/a | Promotional cloud credit first, then the owner's subscription usage |

### 2.1 Consequence: researcher and orchestrator are the same agent

In v2 Codex (orchestrator) and Gemini (researcher) were separate models. In v3
the researcher session also orchestrates. Separation of powers is therefore
enforced by **files and scripts, not by trust**:

- The Advisor runs in its own subagent context, reads only the hashed proposal
  and repository state, and writes only to `research/day-XX/advisor/` and
  `orchestration/advisor-exchanges/`.
- `scripts/gate.py` (built on Day 1) refuses to allocate an experiment ID unless
  the review file exists, its `decision` is `ACCEPT`, its `proposal_sha256`
  matches the proposal on disk, and an acknowledgement file references both hashes.
- The researcher may never edit a review file, a frozen split, the metric
  implementation or a completed record. Corrections are appended as new files.

## 3. Scope of this cloud session: Days 1–4

| Day | Theme | Runs where |
|---|---|---|
| 1 | Infrastructure, dataset audit, frozen splits, evaluator, baselines | Cloud (CPU) |
| 2 | Static and temporal structure | Cloud (CPU) |
| 3 | Congestion reconstruction (highest priority) | Cloud (CPU) |
| 4 | Fold-safe historical priors and interactions | Cloud (CPU) |
| 5 | Model architecture day, CPU vs GPU, optional small neural models | Owner's laptop |
| 6 | Adversarial science day | Owner's laptop |
| 7 | Final synthesis, submission, freeze | Owner's laptop |

A "day" is a **research phase**, not a wall-clock day. Phase boundaries are
closed by a `DAY_SUMMARY.md` and a git commit, and a phase may end early when
its questions are answered.

**Hand-off contract at the end of Day 4:** the repository must allow the owner to
continue on the laptop from files alone:

- `research/STATE.md` current, including the champion and open questions;
- `research/day-04/DAY_SUMMARY.md`;
- `docs/reproducibility/HANDOFF_D04.md`, with environment setup, data
  re-download, champion reproduction command and the expected metrics;
- every scientific artifact committed, and every git-ignored artifact covered by a manifest.

## 4. Compute (cloud, Days 1–4)

```text
CPU    4 vCPU
RAM    15 GB, no swap
Disk   ~30 GB free
GPU    none
```

Resource ceilings (calibrate on Day 1; may only be tightened afterwards):

| Class | Runtime target | RAM target | Examples |
|---|---|---|---|
| CLASS-S | < 5 min | < 4 GB | EDA, baselines, feature checks, small ablations |
| CLASS-M | < 30 min | < 8 GB | Typical boosting experiment across all folds |
| CLASS-L | < 90 min | < 11 GB | Feature rebuilds, confirmation runs (needs explicit Advisor justification) |

- **Hard RAM limit per experiment:** 11 GB, enforced with `ulimit -v` or a `resource` guard in the runner.
- **Hard disk budget for `data/`:** 20 GB.
- **No swap:** an OOM kill is recorded as `RESOURCE_FAILURE`, never silently retried.

Tier 3 GPU/neural experiments are **out of scope** for Days 1–4. GPU boosting
comparisons move to Day 5.

**Container lifetime:** the container is reclaimed when idle. Anything
uncommitted is lost. The checkpoint rule (§13) is therefore a hard requirement,
not a nicety.

## 5. Data access

### 5.1 Sources

- Competition data page: <https://prc-data-challenge-2026.netlify.app/data.html>
- Competition object storage: OpenSky MinIO/S3 (endpoint to be confirmed during the Day 1 audit; default `s3.opensky-network.org`)
- Team submission bucket: `prc-2026-genuine-cabbage` (**write-only at freeze; never read or written during Days 1–4**)
- OpenSky account: used only if a pre-registered hypothesis needs OpenSky data the competition does not ship, and only for data available at prediction time

### 5.2 Credentials

**The repository is public. Credentials are never written to any tracked file,
commit message, log, prompt mirror or report.**

They are read from environment variables:

| Variable | Purpose |
|---|---|
| `PRC_S3_ENDPOINT` | MinIO endpoint host |
| `PRC_S3_ACCESS_KEY` | MinIO access key |
| `PRC_S3_SECRET_KEY` | MinIO secret key |
| `PRC_TEAM_NAME` | `genuine-cabbage` |
| `PRC_SUBMISSION_BUCKET` | `prc-2026-genuine-cabbage` |
| `OPENSKY_USERNAME` / `OPENSKY_PASSWORD` | OpenSky account (optional use) |

Provisioning order: cloud-environment variables, then a local git-ignored `.env`
(see `.env.example`). `scripts/fetch_data.py` loads them and never echoes them.
The session mirror redacts any value matching a known secret before writing.

### 5.3 Network

The cloud environment's network policy must allow the competition hosts
(`prc-data-challenge-2026.netlify.app` and the MinIO endpoint). Until then the
dataset import is `HOLD`, recorded in `docs/incidents/INC-0002`.

### 5.4 Import procedure

1. `uv run python scripts/fetch_data.py --list`: inventory the bucket and record it in `data/manifests/remote_inventory.json`.
2. `uv run python scripts/fetch_data.py --pull`: download into `data/raw/`, verify sizes and write `data/manifests/raw_manifest.json` (path, size, SHA-256, source key, ETag, download time).
3. Convert to Parquet in `data/processed/`, with its own manifest.
4. The Day 1 dataset audit (`docs/methodology/DATASET_AUDIT.md`) covers schemas, row counts, time coverage, target distribution, missingness, and **which columns are available at prediction time for the Jan/Jul 2026 test periods**.

## 6. Agent architecture

```text
Owner (launch / safety only)
        │
        ▼
Claude researcher — main Claude Code session (claude-opus-5-5, high)
  proposes · implements · runs · analyses · selects next work
        │  writes research/day-XX/proposals/H###_vN.md  (+ SHA-256)
        │  writes orchestration/advisor-exchanges/<exchange-id>/envelope.yaml
        ▼
Advisor — `advisor` subagent (Opus, max effort), fresh context per review
  reads hashed proposal + repo state
  writes research/day-XX/advisor/H###_review_vN.md
        │  ACCEPT / REVISE / REJECT / HOLD
        ▼
Researcher writes acknowledgement → scripts/gate.py → experiment ID
        ▼
smoke → screening → full evaluation → error analysis → ablation → decision
        ▼
checkpoint (metrics, journal, STATE.md, ledger, manifests, mirror, git commit)
```

### 6.1 Researcher responsibilities

The researcher controls EDA, hypotheses, features, model families, experiment
configuration within approved bounds, implementation and tests, error analysis,
ablations, interpretation and next-experiment selection.

The researcher does **not** control its own model or effort tier, the Advisor's
identity or policy, frozen splits and metrics, resource ceilings, deletion of
history, leaderboard policy, or whether a proposal skips review.

### 6.2 Advisor responsibilities

The Advisor acts as scientific reviewer, methodological critic, leakage checker,
resource critic and audit checker. It never implements experiments, never
rewrites a proposal into an accepted one, never selects features or
hyperparameters on the researcher's behalf, and never sees leaderboard feedback.

The Advisor starts each review with a **fresh context**. Its only memory is the
repository, which makes reviews independent and reproducible.

### 6.3 Budget discipline

The Advisor runs at maximum effort and is the most expensive component.

- It is invoked for **proposal reviews, the Day 1 split-freeze review, and phase-closing reviews only**.
- Related small proposals (e.g. several baselines) may be **batched** into one review exchange. Each still gets its own decision section.
- Trivial infrastructure work (tooling, tests, manifests) needs no Advisor review, but it may not change frozen artifacts.

## 7. Communication contract (summary)

See `docs/governance/COMMUNICATION_CONTRACT.md` for the normative text.

- Exchange ID: `X-D{day:02}-S{session:02}-{seq:04}`.
- Every Advisor call gets a task envelope (`schema: advisor-task-envelope-v1`), stored at `orchestration/advisor-exchanges/<exchange-id>/envelope.yaml`.
- The Advisor's final message is stored verbatim as `response.md`. Its review file is written into `research/`.
- Handshake: proposal + hash → review (`decision`, `proposal_sha256`) → acknowledgement → `gate.py` → experiment ID.
- Any material change makes a new proposal version and restarts review. `REVISE` never permits execution.

## 8. Proposal and review schemas

The v2 schemas (§9, §10) are retained with these field substitutions:

- `researcher: claude` and `researcher_model_id: claude-opus-5-5`, replacing the Gemini fields;
- `advisor: advisor-subagent` and `advisor_model`: the recorded resolved ID;
- `agy_conversation_id` is replaced by `exchange_id` and `session`;
- `Expected Peak VRAM` must be `0 (CPU)` for Days 1–4, and `Compute Backend` must be `CPU`.

Templates: `docs/governance/templates/proposal.md` and `review.md`.

## 9. Validation strategy

The public test periods are **January 2026** and **July 2026**, so random
validation is unacceptable as the primary signal. Day 1 freezes, in
`config/splits.yaml`, at least:

- **Rolling temporal folds**, e.g. train Jan–Sep 2025 → validate Oct; → Nov; → Dec;
- **A seasonal fold approximating July**, e.g. validate Jul/Aug 2025 with training excluding those months, subject to the temporal-leakage review;
- **A protected local holdout**, accessed at most once per phase and logged each time.

Exact definitions depend on the dataset audit. After the Day 1 freeze commit,
fold definitions and `src/prc/metrics.py` are immutable. `scripts/gate.py`
verifies their hashes before every run.

## 10. Metrics and promotion

Primary: RMSE (in the competition's target units). Always reported alongside:
RMSE by airport, month, traffic regime, aircraft category and taxi-time quantile.

A candidate is promoted to champion only if:

1. overall RMSE improves;
2. the improvement holds on a majority of the frozen folds, including the seasonal fold;
3. no airport degrades by more than a pre-registered tolerance (default: +3 % RMSE);
4. the required ablation supports the claimed mechanism;
5. there is no leakage violation;
6. a re-run reproduces the result within tolerance;
7. resource use is within class;
8. Advisor objections are resolved.

Decisions: `PROMOTE | REJECT | INCONCLUSIVE | RESOURCE_FAILURE | INVALID`.

## 11. Research programme, Days 1–4

- **Day 1 — Infrastructure and baselines.** Environment (`uv`, Python 3.11), dataset import and audit, prediction-time availability audit, frozen splits and metric (Advisor-reviewed), evaluator determinism test, `gate.py`, SQLite ledger, resource calibration, Tier 0 baselines (mean, airport median, time-conditioned median, linear), then LightGBM and XGBoost baselines. Initial champion.
- **Day 2 — Static and temporal structure.** Airport, runway, stand, aircraft type, wake category, operator, destination, flight type, schedule, hour, weekday, month, cyclic encodings, airport × time interactions. The question is how much signal exists without inferred operational state.
- **Day 3 — Congestion reconstruction (highest priority).** Recent departures and arrivals in 5/15/30-minute windows, same-runway activity, airport-wide and runway pressure, arrival/departure imbalance, traffic acceleration, queue / aircraft-ahead proxies, peak behaviour. Every window must use only information available at prediction time. Heavy residual analysis.
- **Day 4 — Historical priors and interactions.** Fold-local target statistics (airport × hour, airport × runway, stand → runway, operator, aircraft), conditional medians and interaction features, plus CatBoost as the natural candidate for high-cardinality categoricals. Close with the hand-off package (§3).

The model families allowed in Days 1–4 are Tier 0, Tier 1 (LightGBM / XGBoost / CatBoost on CPU) and Tier 2 structural alternatives (per-airport, global + residual, two-stage).

## 12. Integrity rules (carried over from v2)

- **No blind hyperparameter search.** A proposal may justify roughly 10–30 targeted trials. The Advisor rejects large searches that lack a scientific rationale.
- **Pre-registration.** The expected result and falsification criterion are written before execution.
- **Negative results are kept.** Failed hypotheses stay in the journal.
- **Failure handling.** Any scientifically meaningful change after a failure (OOM, timeout) gets a new experiment ID.
- **Leaderboard isolation.** Zero submissions and zero leaderboard reads during Days 1–4. The submission bucket is untouched.
- **Contamination ban.** No searching for other PRC 2026 teams' repositories, features, solutions or leaderboard discussions. General literature (taxi-out prediction, surface congestion, queueing theory, boosting, temporal validation) is allowed and must be cited.
- **Immutable history.** Completed records are never rewritten, and corrections are appended.

## 13. Checkpoint after every experiment (mandatory)

1. Save metrics and write the analysis.
2. Update the SQLite ledger (`runtime/ledger.sqlite`, schema tracked in `runtime/ledger.sqlite.schema.sql`), plus the `experiments/ledger.jsonl` tracked export.
3. Update `research/EXPERIMENT_JOURNAL.md` and `research/STATE.md`.
4. Write manifests for every ignored artifact the claim depends on.
5. Mirror the Advisor exchange and refresh checksums.
6. `git commit` and push.

## 14. Repository layout

As v2 §20, minus the `agy`-specific paths:

```text
AGENTS.md  CLAUDE.md  README.md  pyproject.toml  .gitignore  .env.example
.claude/agents/advisor.md
config/        agents.yaml  resources.yaml  splits.yaml (Day 1)
docs/          PROJECT_BRIEF.md  governance/  methodology/  reports/  reproducibility/  incidents/
orchestration/ advisor-exchanges/  task-ledger.jsonl  session-registry.jsonl  locks/
data/          raw/  processed/  cache/  manifests/        (content git-ignored; manifests tracked)
research/      STATE.md  PROJECT_LOG.md  EXPERIMENT_JOURNAL.md  day-01/ … day-04/
experiments/   E###/{config.yaml, metrics.json, analysis.md, resource-usage.json, manifest.json}
models/  checkpoints/  predictions/  runtime/  scripts/  src/prc/  tests/
```

## 15. Provenance statement (for the final report)

> Days 1–4 of this project were conducted as an autonomous ML research run in a
> Claude Code cloud session. A Claude model served as primary researcher and
> generated hypotheses, implemented features and models, ran experiments and
> analysed results. A fixed Claude Advisor subagent at maximum reasoning effort
> reviewed every proposed experiment before execution and could accept, revise,
> reject or hold it, but could not implement experiments or access leaderboard
> results. Deterministic scripts enforced frozen validation splits, resource
> limits, hash-verified review gating and append-only history. The substitution
> of Claude for the originally planned Gemini/Codex pair is recorded as protocol
> deviation INC-0001. Days 5–7 were continued by the project owner on local
> hardware under the same governance.
