"""Execution gate (brief §2.1, COMMUNICATION_CONTRACT §4).

Commands:
    uv run python scripts/gate.py status
    uv run python scripts/gate.py freeze --proposal P --review R --ack A
    uv run python scripts/gate.py allocate H### vN [--purpose primary|reproduction|rerun]

`freeze` writes config/frozen.json once, after an ACCEPTed split-freeze review whose
proposal pins the SHA-256 of every frozen file. `allocate` issues the next E### only if
the proposal hash, the ACCEPT review, the acknowledgement, the frozen-file hashes and the
Advisor definition hash all verify. Every refusal exits non-zero with the reason.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prc import ledger
from prc.paths import EXPERIMENTS, ROOT, git_commit, git_dirty, sha256_file

FROZEN = ROOT / "config" / "frozen.json"
AGENTS = ROOT / "config" / "agents.yaml"
TASK_LEDGER = ROOT / "orchestration" / "task-ledger.jsonl"
FROZEN_FILES = (
    "config/splits.yaml",
    "src/prc/__init__.py",
    "src/prc/metrics.py",
    "src/prc/splits.py",
    "src/prc/evaluate.py",
    "docs/methodology/DATASET_AUDIT.md",
)
HEX = re.compile(r"\b[0-9a-f]{64}\b")


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def refuse(msg: str) -> None:
    sys.exit(f"GATE REFUSED: {msg}")


def front_matter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---"):
        refuse(f"{rel(path)} has no YAML front matter")
    return yaml.safe_load(text.split("---", 2)[1]) or {}


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def check_advisor_definition() -> str:
    cfg = yaml.safe_load(AGENTS.read_text())
    expected = cfg["advisor"]["definition_sha256"]
    actual = sha256_file(ROOT / cfg["advisor"]["definition"])
    if actual != expected:
        refuse(f"advisor definition hash changed ({actual[:12]} != {expected[:12]})")
    return actual


def check_frozen() -> str:
    if not FROZEN.exists():
        refuse("config/frozen.json missing: the Day 1 split freeze has not happened")
    frozen = json.loads(FROZEN.read_text())
    for path, digest in frozen["files"].items():
        if sha256_file(ROOT / path) != digest:
            refuse(f"frozen file modified: {path}")
    return sha256_file(FROZEN)


def check_review(proposal: Path, review: Path, ack: Path) -> tuple[str, str, str]:
    for p in (proposal, review, ack):
        if not p.exists():
            refuse(f"missing {rel(p)}")
    p_sha, r_sha, a_sha = sha256_file(proposal), sha256_file(review), sha256_file(ack)
    fm = front_matter(review)
    if str(fm.get("decision", "")).strip() != "ACCEPT":
        refuse(f"{rel(review)} decision is {fm.get('decision')!r}, not ACCEPT")
    if str(fm.get("proposal_sha256", "")).strip() != p_sha:
        refuse(f"{rel(review)} proposal_sha256 does not match {rel(proposal)} on disk")
    ack_hashes = set(HEX.findall(ack.read_text()))
    if not {p_sha, r_sha} <= ack_hashes:
        refuse(f"{rel(ack)} must reference the proposal hash and the review hash")
    return p_sha, r_sha, a_sha


def append_task_ledger(rec: dict) -> None:
    with open(TASK_LEDGER, "a") as f:
        f.write(json.dumps(rec) + "\n")


def cmd_status(_: argparse.Namespace) -> None:
    print("advisor definition:", check_advisor_definition()[:12], "OK")
    print("frozen files:", check_frozen()[:12], "OK")
    rows = ledger.all_rows()
    print(f"experiments allocated: {len(rows)}")


def cmd_freeze(a: argparse.Namespace) -> None:
    if FROZEN.exists():
        refuse("config/frozen.json already exists; frozen artifacts are immutable")
    check_advisor_definition()
    proposal, review, ack = (ROOT / a.proposal, ROOT / a.review, ROOT / a.ack)
    p_sha, r_sha, a_sha = check_review(proposal, review, ack)
    pinned = set(HEX.findall(proposal.read_text()))
    files = {}
    for path in FROZEN_FILES:
        digest = sha256_file(ROOT / path)
        if digest not in pinned:
            refuse(f"{path} (sha256 {digest[:12]}) is not the version pinned in the proposal")
        files[path] = digest
    frozen = {
        "schema": "frozen-artifacts-v1",
        "frozen_utc": now(),
        "files": files,
        "proposal": {"path": a.proposal, "sha256": p_sha},
        "review": {"path": a.review, "sha256": r_sha},
        "ack": {"path": a.ack, "sha256": a_sha},
        "code_commit": git_commit(),
    }
    FROZEN.write_text(json.dumps(frozen, indent=1) + "\n")
    append_task_ledger({"event": "freeze", "utc": frozen["frozen_utc"],
                        "frozen_sha256": sha256_file(FROZEN), "files": files})
    print("frozen:", ", ".join(files))


def cmd_allocate(a: argparse.Namespace) -> None:
    hid, ver = a.hypothesis, a.version
    if not re.fullmatch(r"H\d{3}", hid) or not re.fullmatch(r"v\d+", ver):
        refuse("usage: allocate H### vN")
    adv_sha = check_advisor_definition()
    frozen_sha = check_frozen()
    matches = sorted(ROOT.glob(f"research/day-*/proposals/{hid}_{ver}.md"))
    if len(matches) != 1:
        refuse(f"expected exactly one proposal {hid}_{ver}.md, found {len(matches)}")
    proposal = matches[0]
    day_dir = proposal.parents[1]
    review = day_dir / "advisor" / f"{hid}_review_{ver}.md"
    ack = day_dir / "acks" / f"{hid}_ack_{ver}.md"
    p_sha, r_sha, a_sha = check_review(proposal, review, ack)

    rows = ledger.all_rows()
    prior = [r for r in rows if r["hypothesis_id"] == hid and r["proposal_version"] == int(ver[1:])]
    if prior and a.purpose == "primary":
        refuse(f"{hid} {ver} already has {prior[0]['experiment_id']}; use --purpose "
               "reproduction|rerun")
    n = max([int(r["experiment_id"][1:]) for r in rows] + [0]) + 1
    eid = f"E{n:03d}"
    pfm = front_matter(proposal)
    rec = {
        "experiment_id": eid,
        "hypothesis_id": hid,
        "proposal_version": int(ver[1:]),
        "purpose": a.purpose,
        "day": day_dir.name,
        "session": pfm.get("session"),
        "proposal_sha256": p_sha,
        "review_sha256": r_sha,
        "ack_sha256": a_sha,
        "frozen_sha256": frozen_sha,
        "allocated_utc": now(),
        "allocated_commit": git_commit(),
        "status": "ALLOCATED",
    }
    exp_dir = EXPERIMENTS / eid
    exp_dir.mkdir(parents=True, exist_ok=False)
    (exp_dir / "gate.json").write_text(json.dumps(
        {**rec, "proposal": rel(proposal), "review": rel(review), "ack": rel(ack),
         "advisor_definition_sha256": adv_sha, "gate_sha256": sha256_file(Path(__file__)),
         "uv_lock_sha256": sha256_file(ROOT / "uv.lock"),
         "git_dirty_at_allocation": git_dirty()},
        indent=1) + "\n")
    ledger.insert(rec)
    append_task_ledger({"event": "allocate", "utc": rec["allocated_utc"],
                        "experiment_id": eid, "hypothesis_id": hid, "version": ver,
                        "purpose": a.purpose, "proposal_sha256": p_sha, "review_sha256": r_sha})
    print(eid)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    f = sub.add_parser("freeze")
    f.add_argument("--proposal", required=True)
    f.add_argument("--review", required=True)
    f.add_argument("--ack", required=True)
    f.set_defaults(fn=cmd_freeze)
    al = sub.add_parser("allocate")
    al.add_argument("hypothesis")
    al.add_argument("version")
    al.add_argument("--purpose", default="primary", choices=["primary", "reproduction", "rerun"])
    al.set_defaults(fn=cmd_allocate)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
