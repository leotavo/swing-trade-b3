import subprocess
import sys


def _run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    try:
        return subprocess.call(cmd)
    except FileNotFoundError as exc:
        print(f"Command not found: {exc}", file=sys.stderr)
        return 127


def lint() -> None:
    # Ruff lint
    rc = _run([sys.executable, "-m", "ruff", "check", "."])
    sys.exit(rc)


def format() -> None:
    # Black format
    rc = _run([sys.executable, "-m", "black", "."])
    sys.exit(rc)


def typecheck() -> None:
    # Mypy type check
    rc = _run([sys.executable, "-m", "mypy", "."])
    sys.exit(rc)


def test() -> None:
    # Pytest uses default options from pyproject.toml (coverage + 100% required)
    # Treat "no tests collected" (exit 5) as success for now
    rc = _run([sys.executable, "-m", "pytest", "-q"])
    if rc == 5:
        # no tests collected; do not fail developer workflow at this stage
        rc = 0
    sys.exit(rc)
