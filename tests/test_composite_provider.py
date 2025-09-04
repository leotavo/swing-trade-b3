from __future__ import annotations

from datetime import date

import pandas as pd

from swing_trade_b3.adapters.connectors.market_data import composite_provider as cp


def test_composite_provider_primary_ok(monkeypatch):
    def primary_ok(symbol, start, end, **kwargs):  # noqa: ANN001
        return pd.DataFrame.from_records(
            [
                {
                    "date": pd.Timestamp("2024-01-01", tz="UTC"),
                    "symbol": symbol,
                    "open": 1.0,
                    "high": 1.1,
                    "low": 0.9,
                    "close": 1.05,
                    "volume": 10,
                }
            ]
        )

    monkeypatch.setattr(cp.b3, "fetch_daily", primary_ok)
    meta = {}
    out = cp.fetch_daily("SYM", date(2024, 1, 1), date(2024, 1, 2), meta=meta)
    assert len(out) == 1
    assert meta.get("provider") == "brapi"


def test_composite_provider_fallback(monkeypatch):
    def primary_fail(*a, **k):  # noqa: ANN001
        raise RuntimeError("boom")

    def fallback_ok(symbol, start, end, **kwargs):  # noqa: ANN001
        return pd.DataFrame.from_records(
            [
                {
                    "date": pd.Timestamp("2024-01-01", tz="UTC"),
                    "symbol": symbol,
                    "open": 1.0,
                    "high": 1.1,
                    "low": 0.9,
                    "close": 1.05,
                    "volume": 10,
                }
            ]
        )

    monkeypatch.setattr(cp.b3, "fetch_daily", primary_fail)
    monkeypatch.setattr(cp.yf, "fetch_daily", fallback_ok)
    out = cp.fetch_daily("SYM", date(2024, 1, 1), date(2024, 1, 2))
    assert len(out) == 1


def test_composite_provider_primary_empty_then_fallback(monkeypatch):
    def primary_empty(*a, **k):  # noqa: ANN001
        return pd.DataFrame(columns=["date", "symbol", "open", "high", "low", "close", "volume"])

    def fallback_ok(symbol, start, end, **kwargs):  # noqa: ANN001
        return pd.DataFrame.from_records(
            [
                {
                    "date": pd.Timestamp("2024-01-02", tz="UTC"),
                    "symbol": symbol,
                    "open": 1.0,
                    "high": 1.2,
                    "low": 0.8,
                    "close": 1.1,
                    "volume": 5,
                }
            ]
        )

    monkeypatch.setattr(cp.b3, "fetch_daily", primary_empty)
    monkeypatch.setattr(cp.yf, "fetch_daily", fallback_ok)
    out = cp.fetch_daily("SYM", date(2024, 1, 1), date(2024, 1, 2))
    assert len(out) == 1
