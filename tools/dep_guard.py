#!/usr/bin/env python3
"""nativelite zero-dependency guard (stdlib only).

Fails (exit 1) if the package declares any third-party runtime dependency or
imports anything outside the standard library. Run in CI on every push/PR.
"""
from __future__ import annotations

import ast
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = ROOT / "src" / "fp"
OWN = {"fp"}


def check_manifest() -> list[str]:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    deps = data.get("project", {}).get("dependencies", None)
    if deps is None:
        return ["pyproject.toml [project].dependencies is missing (must be [])"]
    if deps != []:
        return [f"runtime dependencies must be empty, found: {deps!r}"]
    return []


def _roots(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                yield a.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # relative import -> own package
                continue
            if node.module:
                yield node.module.split(".")[0]


def check_imports() -> list[str]:
    allowed = set(sys.stdlib_module_names) | OWN
    problems: list[str] = []
    for path in sorted(PKG_DIR.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for root in _roots(tree):
            if root not in allowed:
                problems.append(f"{path.relative_to(ROOT)}: non-stdlib import '{root}'")
    return problems


def main() -> int:
    problems = check_manifest() + check_imports()
    if problems:
        print("Dependency guard FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("Dependency guard OK: zero third-party runtime dependencies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
