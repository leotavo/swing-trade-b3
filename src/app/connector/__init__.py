"""Data connectors for external market data providers.

Currently supports brapi.dev for B3 historical daily OHLCV.
"""

from .b3 import fetch_daily  # re-export public API

__all__ = ["fetch_daily"]
