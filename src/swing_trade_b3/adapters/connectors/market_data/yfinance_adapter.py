from __future__ import annotations

import logging
from datetime import date
from typing import Any, Callable, Dict, Optional

import pandas as pd

LOG = logging.getLogger(__name__)


def _to_yf_symbol(symbol: str) -> str:
    s = symbol.strip()
    if not s.upper().endswith(".SA") and "." not in s:
        return f"{s}.SA"
    return s


def fetch_daily(
    symbol: str,
    start: date,
    end: date,
    *,
    throttle_wait: Optional[Callable[[], None]] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """Fetch daily OHLCV via yfinance and normalize to standard schema.

    Returns DataFrame with columns: date (UTC), symbol, open, high, low, close, volume.
    """
    if throttle_wait is not None:
        throttle_wait()

    import yfinance as yf  # lazy import to keep optional

    yf_symbol = _to_yf_symbol(symbol)
    # yfinance uses end as exclusive; extend by 1 day to include desired end
    df = yf.download(
        tickers=yf_symbol,
        start=pd.Timestamp(start, tz="UTC").date(),
        end=(pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1)).date(),
        interval="1d",
        auto_adjust=False,
        progress=False,
        threads=False,
    )

    if df is None or len(df) == 0:
        return pd.DataFrame(columns=["date", "symbol", "open", "high", "low", "close", "volume"])

    # Ensure single-level columns and expected names
    if isinstance(df.columns, pd.MultiIndex):
        # pick single ticker level
        df = df.droplevel(0, axis=1)

    cols_map = {
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    }
    missing = [c for c in cols_map if c not in df.columns]
    if missing:
        LOG.warning("yfinance: missing expected columns", extra={"missing": missing})
        return pd.DataFrame(columns=["date", "symbol", "open", "high", "low", "close", "volume"])

    out = (
        df.rename(columns=cols_map)[list(cols_map.values())]
        .assign(
            date=pd.to_datetime(df.index, utc=True),
            symbol=str(symbol),
        )
        .reset_index(drop=True)
    )

    # Coerce dtypes and sanitize
    out["date"] = pd.to_datetime(out["date"], utc=True)
    out["symbol"] = out["symbol"].astype("string")
    for c in ["open", "high", "low", "close"]:
        out[c] = pd.to_numeric(out[c], errors="coerce").astype("float64")
    out["volume"] = pd.to_numeric(out["volume"], errors="coerce").astype("Int64")

    # Filter exact range just in case
    s = pd.Timestamp(start, tz="UTC")
    e = pd.Timestamp(end, tz="UTC")
    out = out[(out["date"] >= s) & (out["date"] <= e)]

    if not out.empty and not out["volume"].isna().any():
        out["volume"] = out["volume"].astype("int64")

    return out[["date", "symbol", "open", "high", "low", "close", "volume"]]

