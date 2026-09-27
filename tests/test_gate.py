"""scripts/gate.py refuses every broken handshake, in an isolated fake repository."""

import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture
def gate(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("gate", REPO / "scripts" / "gate.py")
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    from prc import ledger

    root = tmp_path
    for rel in [*g.FROZEN_FILES, "config/agents.yaml", ".claude/agents/advisor.md",
                "runtime/ledger.sqlite.schema.sql"]:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO / rel, root / rel)
    for d in ("orchestration", "experiments", "research/day-01/proposals",
              "research/day-01/advisor", "research/day-01/acks"):
        (root / d).mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(g, "ROOT", root)
    monkeypatch.setattr(g, "FROZEN", root / "config" / "frozen.json")
    monkeypatch.setattr(g, "AGENTS", root / "config" / "agents.yaml")
    monkeypatch.setattr(g, "TASK_LEDGER", root / "orchestration" / "task-ledger.jsonl")
    monkeypatch.setattr(g, "EXPERIMENTS", root / "experiments")
    monkeypatch.setattr(g, "git_commit", lambda: "0" * 40)
    monkeypatch.setattr(g, "git_dirty", lambda: False)
    monkeypatch.setattr(ledger, "DB", root / "runtime" / "ledger.sqlite")
    monkeypatch.setattr(ledger, "SCHEMA", root / "runtime" / "ledger.sqlite.schema.sql")
    monkeypatch.setattr(ledger, "EXPORT", root / "experiments" / "ledger.jsonl")
    g._root = root
    return g


def handshake(root: Path, name: str, body: str, decision="ACCEPT", ack_ok=True, pin_ok=True):
    day = root / "research" / "day-01"
    prop = day / "proposals" / f"{name}_v1.md"
    prop.write_text(f"---\nsession: D01-S01\n---\n{body}\n")
    p_sha = sha(prop) if pin_ok else "f" * 64
    review = day / "advisor" / f"{name}_review_v1.md"
    review.write_text(f"---\ndecision: {decision}\nproposal_sha256: {p_sha}\n---\nok\n")
    ack = day / "acks" / f"{name}_ack_v1.md"
    ack.write_text(f"proposal {sha(prop)}\nreview {sha(review) if ack_ok else '0' * 64}\n")
    return prop, review, ack


class Args:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def freeze(gate):
    root = gate._root
    pins = "\n".join(sha(root / f) for f in gate.FROZEN_FILES)
    p, r, a = handshake(root, "SPLITS", pins)
    rel = lambda x: str(x.relative_to(root))
    gate.cmd_freeze(Args(proposal=rel(p), review=rel(r), ack=rel(a)))


def test_allocate_refused_before_freeze(gate):
    handshake(gate._root, "H001", "baseline")
    with pytest.raises(SystemExit, match="frozen.json missing"):
        gate.cmd_allocate(Args(hypothesis="H001", version="v1", purpose="primary"))


def test_happy_path_and_duplicate_refusal(gate, capsys):
    freeze(gate)
    capsys.readouterr()
    handshake(gate._root, "H001", "baseline")
    gate.cmd_allocate(Args(hypothesis="H001", version="v1", purpose="primary"))
    assert capsys.readouterr().out.strip() == "E001"
    rec = json.loads((gate._root / "experiments" / "E001" / "gate.json").read_text())
    assert rec["hypothesis_id"] == "H001" and rec["status"] == "ALLOCATED"
    with pytest.raises(SystemExit, match="already has E001"):
        gate.cmd_allocate(Args(hypothesis="H001", version="v1", purpose="primary"))
    gate.cmd_allocate(Args(hypothesis="H001", version="v1", purpose="reproduction"))
    assert capsys.readouterr().out.strip() == "E002"


@pytest.mark.parametrize("kw,msg", [
    ({"decision": "REVISE"}, "not ACCEPT"),
    ({"pin_ok": False}, "does not match"),
    ({"ack_ok": False}, "must reference"),
])
def test_broken_handshakes_refused(gate, kw, msg):
    freeze(gate)
    handshake(gate._root, "H002", "x", **kw)
    with pytest.raises(SystemExit, match=msg):
        gate.cmd_allocate(Args(hypothesis="H002", version="v1", purpose="primary"))


def test_tampered_frozen_file_refused(gate):
    freeze(gate)
    handshake(gate._root, "H003", "x")
    with open(gate._root / "src/prc/metrics.py", "a") as f:
        f.write("# tamper\n")
    with pytest.raises(SystemExit, match="frozen file modified"):
        gate.cmd_allocate(Args(hypothesis="H003", version="v1", purpose="primary"))


def test_freeze_is_once_only_and_requires_pinned_versions(gate):
    root = gate._root
    p, r, a = handshake(root, "SPLITS", "no pins here")
    rel = lambda x: str(x.relative_to(root))
    with pytest.raises(SystemExit, match="not the version pinned"):
        gate.cmd_freeze(Args(proposal=rel(p), review=rel(r), ack=rel(a)))
    freeze(gate)
    with pytest.raises(SystemExit, match="already exists"):
        freeze(gate)


def test_advisor_definition_change_refused(gate):
    with open(gate._root / ".claude/agents/advisor.md", "a") as f:
        f.write("\nextra\n")
    with pytest.raises(SystemExit, match="advisor definition hash changed"):
        gate.cmd_status(Args())
