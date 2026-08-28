#!/usr/bin/env python3
"""Local dev runner for fp-py — stdlib only, no third-party task runner.

Run the tight dev loop on your own machine (free) instead of via paid agents:

  python -m pip install -e ".[dev]"   # one-time setup
  python dev.py check                 # guard + tests (what CI runs)
  python dev.py test                  # unittest suite
  python dev.py cov                   # tests + coverage report
  python dev.py guard                 # zero-dependency guard
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable


def run(*args: str) -> int:
    print(f"$ {' '.join(args)}")
    return subprocess.call(args, cwd=str(ROOT))


def test() -> int:
    return run(PY, "-m", "unittest", "discover", "-s", "tests", "-t", ".")


def cov() -> int:
    rc = run(PY, "-m", "coverage", "run", "--source=fp",
             "-m", "unittest", "discover", "-s", "tests", "-t", ".")
    return rc or run(PY, "-m", "coverage", "report", "-m")


def guard() -> int:
    return run(PY, "tools/dep_guard.py")


def check() -> int:
    return guard() or test()


COMMANDS = {"test": test, "cov": cov, "guard": guard, "check": check}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print(f"unknown command {cmd!r}; choose from: {', '.join(COMMANDS)}")
        return 2
    return fn()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
