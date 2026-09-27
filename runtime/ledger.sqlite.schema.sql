-- Experiment ledger (brief §13). runtime/ledger.sqlite is git-ignored and rebuilt from the
-- tracked export experiments/ledger.jsonl after a container reset (src/prc/ledger.py).
CREATE TABLE IF NOT EXISTS experiments (
    experiment_id      TEXT PRIMARY KEY,          -- E###
    hypothesis_id      TEXT NOT NULL,             -- H###
    proposal_version   INTEGER NOT NULL,
    purpose            TEXT NOT NULL,             -- primary | reproduction | rerun
    day                TEXT NOT NULL,             -- day-XX
    session            TEXT,
    proposal_sha256    TEXT NOT NULL,
    review_sha256      TEXT NOT NULL,
    ack_sha256         TEXT NOT NULL,
    frozen_sha256      TEXT NOT NULL,             -- sha256 of config/frozen.json at allocation
    allocated_utc      TEXT NOT NULL,
    allocated_commit   TEXT NOT NULL,
    status             TEXT NOT NULL,             -- ALLOCATED | RUNNING | COMPLETE | RESOURCE_FAILURE | TIMEOUT | INVALID
    decision           TEXT,                      -- PROMOTE | REJECT | INCONCLUSIVE | RESOURCE_FAILURE | INVALID
    job_class          TEXT,
    runtime_s          REAL,
    peak_rss_gb        REAL,
    mean_rmse_dev      REAL,
    rmse_by_fold       TEXT,                      -- JSON
    run_commit         TEXT,
    finished_utc       TEXT,
    notes              TEXT
);
