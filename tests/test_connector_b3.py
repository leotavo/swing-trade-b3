from datetime import date, timedelta

import pandas as pd
import pytest

from app.connector.b3 import (
    HttpConfig,
    ParseError,
    RateLimitError,
    ServerError,
    _build_url,
    _choose_range,
    _http_get_json,
    _normalize_to_ohlcv,
    fetch_daily,
)


def test_choose_range_thresholds():
    today = date.today()
    # 1mo: span <= 31 days
    assert _choose_range(today - timedelta(days=10), today) == "1mo"
    # 3mo: <= 93
    assert _choose_range(today - timedelta(days=60), today) == "3mo"
    # 6mo: <= 186
    assert _choose_range(today - timedelta(days=120), today) == "6mo"
    # 1y: <= 366
    assert _choose_range(today - timedelta(days=300), today) == "1y"
    # 5y: <= 5 * 366
    assert _choose_range(today - timedelta(days=1000), today) == "5y"
    # max otherwise
    assert _choose_range(today - timedelta(days=5 * 366 + 10), today) == "max"


def test_build_url():
    assert _build_url("PETR4", "1mo").endswith("/PETR4?interval=1d&range=1mo")


def test_normalize_to_ohlcv_happy_and_errors():
    ts = int(pd.Timestamp("2024-01-02", tz="UTC").timestamp())
    payload = {
        "results": [
            {
                "symbol": "PETR4",
                "historicalDataPrice": [
                    {
                        "date": ts,
                        "open": "10",
                        "high": 11,
                        "low": 9,
                        "close": "10.5",
                        "volume": "100",
                    },
                    {
                        "date": ts,
                        "open": None,
                        "high": 11,
                        "low": 9,
                        "close": 10.5,
                        "volume": 100,
                    },  # dropped
                    {"open": 1},  # malformed
                ],
            }
        ]
    }
    df = _normalize_to_ohlcv("PETR4", payload)
    assert len(df) == 1
    assert set(df.columns) == {"date", "symbol", "open", "high", "low", "close", "volume"}
    assert df.loc[0, "volume"] == 100
    assert df["open"].dtype == "float64"

    with pytest.raises(ParseError):
        _normalize_to_ohlcv("X", {})
    with pytest.raises(ParseError):
        _normalize_to_ohlcv("X", {"results": None})
    with pytest.raises(ParseError):
        _normalize_to_ohlcv("X", {"results": []})
    with pytest.raises(ParseError):
        _normalize_to_ohlcv("X", {"results": [{}]})
    with pytest.raises(ParseError):
        _normalize_to_ohlcv("X", {"results": [{"historicalDataPrice": {}}]})


class FakeResp:
    def __init__(self, status, data=None, err=None):
        self.status_code = status
        self._data = data or {}
        self._err = err

    def json(self):
        return self._data

    def raise_for_status(self):
        if self._err:
            raise self._err


def test_http_get_json_success_and_errors(monkeypatch):
    calls = {"n": 0}

    def fake_get(url, headers=None, timeout=None):  # noqa: ARG001
        calls["n"] += 1
        return FakeResp(200, {"ok": True})

    monkeypatch.setattr("app.connector.b3.requests.get", fake_get)

    meta = {}
    out = _http_get_json(
        "http://x", cfg=HttpConfig(max_retries=2), throttle_wait=lambda: None, meta=meta
    )
    assert out == {"ok": True}
    assert meta["http"]["attempts"] == 1
    assert meta["http"]["throttle_calls"] >= 1

    # 429 then exhaust retries -> RateLimitError
    seq = [FakeResp(429), FakeResp(429)]

    def fake_get_429(url, headers=None, timeout=None):  # noqa: ARG001
        return seq.pop(0)

    monkeypatch.setattr("app.connector.b3.requests.get", fake_get_429)
    monkeypatch.setattr("app.connector.b3.time.sleep", lambda s: None)
    with pytest.raises(RateLimitError):
        _http_get_json("http://x", cfg=HttpConfig(max_retries=2), meta={})

    # 500 -> ServerError
    monkeypatch.setattr("app.connector.b3.requests.get", lambda *a, **k: FakeResp(503))
    with pytest.raises(ServerError):
        _http_get_json("http://x", cfg=HttpConfig(max_retries=1), meta={})

    # 400 -> raise_for_status
    err = Exception("bad request")
    monkeypatch.setattr("app.connector.b3.requests.get", lambda *a, **k: FakeResp(400, err=err))
    with pytest.raises(Exception):
        _http_get_json("http://x", cfg=HttpConfig(max_retries=1), meta={})

    # Timeout/Connection exception path
    class TimeoutEx(Exception):
        pass

    import requests as _req

    monkeypatch.setattr(
        "app.connector.b3.requests.get", lambda *a, **k: (_ for _ in ()).throw(_req.Timeout("t"))
    )
    with pytest.raises(_req.Timeout):
        _http_get_json("http://x", cfg=HttpConfig(max_retries=1), meta={})

    # No attempts (max_retries=0) → default NetworkError
    from app.connector.b3 import NetworkError

    with pytest.raises(NetworkError):
        _http_get_json("http://x", cfg=HttpConfig(max_retries=0))


def test_fetch_daily_filters_and_retries(monkeypatch):
    # First attempt returns out-of-range -> empty -> triggers range=max retry
    def fake_http_get(url, cfg, throttle_wait=None, meta=None):  # noqa: ARG001
        if "range=max" in url:
            ts = int(pd.Timestamp("2023-01-02", tz="UTC").timestamp())
            return {
                "results": [
                    {
                        "historicalDataPrice": [
                            {"date": ts, "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1}
                        ]
                    }
                ]
            }
        # first call returns rows all OUTSIDE the [start,end] range → empty after filter
        ts_old = int(pd.Timestamp("2000-01-01", tz="UTC").timestamp())
        return {
            "results": [
                {
                    "historicalDataPrice": [
                        {"date": ts_old, "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1}
                    ]
                }
            ]
        }

    monkeypatch.setattr("app.connector.b3._http_get_json", fake_http_get)
    start = date(2023, 1, 1)
    end = date(2023, 1, 3)
    meta = {}
    df = fetch_daily("PETR4", start, end, meta=meta)
    assert not df.empty and meta["range_used"] == "max"

    # prefer_max skips retry logic and uses max directly
    monkeypatch.setattr("app.connector.b3._http_get_json", fake_http_get)
    df2 = fetch_daily("PETR4", start, end, prefer_max=True, meta=meta)
    assert not df2.empty

    # invalid args
    with pytest.raises(ValueError):
        fetch_daily(" ", start, end)
    with pytest.raises(ValueError):
        fetch_daily("X", end, start)
