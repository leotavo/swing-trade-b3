"""Lightweight developer CLI helpers used via Poetry scripts.

Commands are intentionally thin wrappers around the underlying tools to
mirror what runs in CI. They print the exact command executed and exit
with the same return code, making them convenient to use locally:

- poetry run lint       -> ruff check .
- poetry run format     -> black .
- poetry run typecheck  -> mypy .
- poetry run test       -> pytest -q
- poetry run ci         -> ruff + black --check + mypy + pytest (in sequence)

Note: The function name "format" is kept for backwards compatibility with
the existing Poetry script entry. A convenience alias "fmt" is also
provided.
"""

from __future__ import annotations

import subprocess
import sys


def _run(cmd: list[str]) -> int:
    """Run a command, echoing it, and return its exit code.

    - Returns 127 when the executable is not found
    - Returns 130 on KeyboardInterrupt
    """
    print("$", " ".join(cmd))
    try:
        rc = subprocess.call(cmd)
        return rc
    except FileNotFoundError as exc:
        print(f"Command not found: {exc}", file=sys.stderr)
        return 127
    except KeyboardInterrupt:
        # Align with common shell convention for interrupted commands
        return 130


def lint() -> None:
    """Run ruff linter."""
    rc = _run([sys.executable, "-m", "ruff", "check", "."])
    raise SystemExit(rc)


def format() -> None:  # noqa: A001 - keep name for script compatibility
    """Run black code formatter (in-place)."""
    rc = _run([sys.executable, "-m", "black", "."])
    raise SystemExit(rc)


def fmt() -> None:
    """Alias for format(), provided for convenience."""
    format()


def typecheck() -> None:
    """Run mypy type checker."""
    rc = _run([sys.executable, "-m", "mypy", "."])
    raise SystemExit(rc)


def test() -> None:
    """Run pytest with repo defaults (coverage enforced via pyproject)."""
    rc = _run([sys.executable, "-m", "pytest", "-q"])
    if rc == 5:
        # No tests collected - treat as success for local workflow convenience
        rc = 0
    raise SystemExit(rc)


def ci() -> None:
    """Run the same sequence as CI: ruff, black --check, mypy, pytest.

    Exits with the first non-zero code encountered.
    """
    steps = [
        [sys.executable, "-m", "ruff", "check", "."],
        [sys.executable, "-m", "black", "--check", "."],
        [sys.executable, "-m", "mypy", "."],
        [sys.executable, "-m", "pytest", "-q"],
    ]
    for cmd in steps:
        rc = _run(cmd)
        if rc != 0 and rc != 5:  # allow "no tests collected" to pass
            raise SystemExit(rc)
    raise SystemExit(0)

