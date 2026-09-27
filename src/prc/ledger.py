"""Experiment ledger: SQLite working copy + tracked JSONL export (brief §13).

The JSONL export (experiments/ledger.jsonl) is the durable record; the SQLite file is a
queryable mirror rebuilt from it when missing (the container is ephemeral).
"""

from __future__ import annotations

import json
import sqlite3

from prc.paths import EXPERIMENTS, ROOT, RUNTIME

DB = RUNTIME / "ledger.sqlite"
SCHEMA = RUNTIME / "ledger.sqlite.schema.sql"
EXPORT = EXPERIMENTS / "ledger.jsonl"


def _columns(con: sqlite3.Connection) -> list[str]:
    return [r[1] for r in con.execute("PRAGMA table_info(experiments)")]


def connect() -> sqlite3.Connection:
    fresh = not DB.exists()
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA.read_text())
    if fresh and EXPORT.exists():
        cols = _columns(con)
        for line in EXPORT.read_text().splitlines():
            if line.strip():
                rec = json.loads(line)
                keys = [k for k in cols if k in rec]
                con.execute(
                    f"INSERT OR REPLACE INTO experiments ({','.join(keys)}) "
                    f"VALUES ({','.join('?' * len(keys))})",
                    [rec[k] for k in keys],
                )
        con.commit()
    return con


def export(con: sqlite3.Connection) -> None:
    rows = con.execute("SELECT * FROM experiments ORDER BY experiment_id").fetchall()
    EXPORT.write_text("".join(json.dumps(dict(r)) + "\n" for r in rows))


def insert(rec: dict) -> None:
    con = connect()
    keys = list(rec)
    con.execute(
        f"INSERT INTO experiments ({','.join(keys)}) VALUES ({','.join('?' * len(keys))})",
        [rec[k] for k in keys],
    )
    con.commit()
    export(con)
    con.close()


def update(experiment_id: str, **fields) -> None:
    con = connect()
    if con.execute("SELECT 1 FROM experiments WHERE experiment_id=?",
                   (experiment_id,)).fetchone() is None:
        raise KeyError(experiment_id)
    sets = ",".join(f"{k}=?" for k in fields)
    con.execute(f"UPDATE experiments SET {sets} WHERE experiment_id=?",
                [*fields.values(), experiment_id])
    con.commit()
    export(con)
    con.close()


def get(experiment_id: str) -> dict | None:
    con = connect()
    r = con.execute("SELECT * FROM experiments WHERE experiment_id=?",
                    (experiment_id,)).fetchone()
    con.close()
    return dict(r) if r else None


def all_rows() -> list[dict]:
    con = connect()
    rows = [dict(r) for r in con.execute("SELECT * FROM experiments ORDER BY experiment_id")]
    con.close()
    return rows


def relpath(p) -> str:
    return str(p.relative_to(ROOT))
