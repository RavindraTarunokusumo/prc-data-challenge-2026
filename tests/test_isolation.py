"""Import boundaries (Advisor recommendation, SPLITS v1 review).

- Feature and model code may not import truth-reading or data-loading code.
- Frozen modules may import only other frozen prc modules.
"""

import ast
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src" / "prc"
FORBIDDEN_FOR_MODELS = {"prc.data", "prc.evaluate", "eval_rows", "truth_frame", "load_silver",
                        "_truth", "holdout_compare", "prc.paths", "SILVER"}
FORBIDDEN_CALLS = {"read_parquet", "scan_parquet", "read_csv", "scan_csv", "open"}
FROZEN_MODULES = {"prc.splits", "prc.metrics", "prc.evaluate"}
FROZEN_ALLOWED = {"prc", "prc.splits", "prc.metrics"}


def imports(path: Path) -> set[str]:
    names = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Import):
            names |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            names.add(mod)
            names |= {f"{mod}.{a.name}" for a in node.names} | {a.name for a in node.names}
    return names


MODEL_FILES = [SRC / "features.py", *sorted((SRC / "models").glob("*.py"))]


@pytest.mark.parametrize("path", MODEL_FILES, ids=lambda p: p.name)
def test_models_do_not_import_truth(path):
    assert not imports(path) & FORBIDDEN_FOR_MODELS


@pytest.mark.parametrize("path", MODEL_FILES, ids=lambda p: p.name)
def test_models_do_not_read_files(path):
    calls = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Call):
            f = node.func
            calls.add(f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", ""))
    assert not calls & FORBIDDEN_CALLS


@pytest.mark.parametrize("module", sorted(FROZEN_MODULES))
def test_frozen_modules_import_only_frozen(module):
    path = SRC / f"{module.split('.')[1]}.py"
    prc_imports = {n for n in imports(path) if n == "prc" or n.startswith("prc.")}
    modules = {n for n in prc_imports if n in FROZEN_ALLOWED or n.count(".") == 1}
    assert modules <= FROZEN_ALLOWED, modules - FROZEN_ALLOWED
