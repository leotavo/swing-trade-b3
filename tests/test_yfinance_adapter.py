from __future__ import annotations

from datetime import date

import pandas as pd

from swing_trade_b3.adapters.connectors.market_data import yfinance_adapter as yf


def test_to_yf_symbol_mapping():
    assert yf._to_yf_symbol("PETR4") == "PETR4.SA"
    assert yf._to_yf_symbol("VALE3.SA") == "VALE3.SA"


def test_fetch_daily_with_stubbed_yfinance(monkeypatch):
    # stub yfinance.download to return a minimal frame
    class Dummy:
        @staticmethod
        def download(tickers, start, end, interval, auto_adjust, progress, threads):  # noqa: ANN001
            idx = pd.to_datetime(["2024-01-01", "2024-01-02"], utc=True)
            df = pd.DataFrame(
                {
                    "Open": [10.0, 10.5],
                    "High": [11.0, 11.2],
                    "Low": [9.5, 10.1],
                    "Close": [10.5, 11.0],
                    "Volume": [1000, 2000],
                },
                index=idx,
            )
            # simulate MultiIndex columns shape that yfinance may return
            df.columns = pd.MultiIndex.from_product([["X"], df.columns])
            return df

    import sys

    monkeypatch.setitem(sys.modules, "yfinance", Dummy)

    out = yf.fetch_daily("TEST3", date(2024, 1, 1), date(2024, 1, 2))
    assert not out.empty
    assert list(out.columns) == ["date", "symbol", "open", "high", "low", "close", "volume"]
    assert out["symbol"].iloc[0] == "TEST3"


def test_fetch_daily_missing_columns_returns_empty(monkeypatch):
    class Dummy:
        @staticmethod
        def download(*a, **k):  # noqa: ANN001
            idx = pd.to_datetime(["2024-01-01"], utc=True)
            # Missing Volume column
            return pd.DataFrame({"Open": [1.0], "High": [1.1], "Low": [0.9], "Close": [1.05]}, index=idx)

    import sys

    monkeypatch.setitem(sys.modules, "yfinance", Dummy)
    out = yf.fetch_daily("ZZ", date(2024, 1, 1), date(2024, 1, 1))
    assert out.empty


def test_fetch_daily_volume_nullable_branch(monkeypatch):
    class Dummy:
        @staticmethod
        def download(*a, **k):  # noqa: ANN001
            idx = pd.to_datetime(["2024-01-01"], utc=True)
            # Volume as None triggers nullable path (no cast to int64)
            return pd.DataFrame(
                {"Open": [1.0], "High": [1.1], "Low": [0.9], "Close": [1.05], "Volume": [None]},
                index=idx,
            )

    import sys

    monkeypatch.setitem(sys.modules, "yfinance", Dummy)
    out = yf.fetch_daily("AA", date(2024, 1, 1), date(2024, 1, 1))
    assert not out.empty
    # volume remains nullable Int64, not int64
    assert str(out["volume"].dtype) == "Int64"
