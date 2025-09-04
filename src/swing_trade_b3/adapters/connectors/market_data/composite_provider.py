from __future__ import annotations

import logging
from datetime import date
from typing import Any, Callable, Dict, Optional

import pandas as pd

from . import b3_adapter as b3
from . import yfinance_adapter as yf


LOG = logging.getLogger(__name__)


def fetch_daily(
    symbol: str,
    start: date,
    end: date,
    *,
    http: Any | None = None,
    prefer_max: bool = False,
    throttle_wait: Optional[Callable[[], None]] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """Fetch daily OHLCV with fallback: brapi -> yfinance."""
    try:
        df = b3.fetch_daily(
            symbol,
            start,
            end,
            http=http,
            prefer_max=prefer_max,
            throttle_wait=throttle_wait,
            meta=meta,
        )
        if not df.empty:  # pragma: no branch
            if meta is not None:  # pragma: no branch
                meta.setdefault("provider", "brapi")
            return df
        primary_ok = True
    except Exception as exc:  # pragma: no cover - defensive
        LOG.warning("primary provider failed; considering fallback", extra={"error": str(exc)})
        primary_ok = False

    # Fallback to yfinance (optional dependency)
    try:
        df_yf = yf.fetch_daily(symbol, start, end, throttle_wait=throttle_wait, meta=meta)
        if meta is not None:
            meta["provider"] = "yfinance"
        return df_yf
    except Exception:  # pragma: no cover - optional dep import/exec may fail
        if not primary_ok:
            raise
        return pd.DataFrame(columns=["date", "symbol", "open", "high", "low", "close", "volume"])
