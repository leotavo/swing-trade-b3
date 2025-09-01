from __future__ import annotations

from . import __version__


def main() -> int:
    print(f"swing-trade-b3 {__version__} - CLI minima ativa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
