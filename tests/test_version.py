import tomllib
from pathlib import Path

from swing_trade import __version__


def test_version_matches_pyproject():
    """Ensure package version matches configuration."""
    data = tomllib.loads(Path("pyproject.toml").read_text())
    expected = data["project"]["version"]
    assert __version__ == expected
