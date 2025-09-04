from __future__ import annotations

import json
import logging
import math
import random
import time
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable, Dict, List, Optional, Tuple, cast

import pandas as pd
import requests

from swing_trade_b3 import __version__


LOG = logging.getLogger(__name__)


class NetworkError(RuntimeError):
    pass


class RateLimitError(RuntimeError):
    pass


class ServerError(RuntimeError):
    pass


class ParseError(RuntimeError):
    pass


@dataclass(frozen=True)
class HttpConfig:
    timeout: float = 10.0
    max_retries: int = 3
    backoff_base: float = 0.5  # initial backoff seconds
    backoff_factor: float = 2.0
    jitter: Tuple[float, float] = (0.1, 0.5)


def _user_agent() -> str:
    return f"swing-trade-b3/{__version__} (+github.com/leotavo/swing-trade-b3)"


def _http_get_json(
    url: str,
    *,
    cfg: HttpConfig,
    throttle_wait: Optional[Callable[[], None]] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    headers = {"User-Agent": _user_agent(), "Accept": "application/json"}
    last_err: Exception | None = None
    http_meta: Optional[Dict[str, Any]] = None
    if meta is not None:
        http_meta = cast(Dict[str, Any], meta.setdefault("http", {}))
        http_meta.setdefault("attempts", 0)
        http_meta.setdefault("retries", 0)
        http_meta.setdefault("sleep_total_s", 0.0)
        http_meta.setdefault("last_status", None)
        http_meta.setdefault("throttle_calls", 0)
    for attempt in range(1, cfg.max_retries + 1):
        if throttle_wait is not None:
            throttle_wait()
            if http_meta is not None:
                http_meta["throttle_calls"] = int(http_meta.get("throttle_calls", 0)) + 1
        try:
            resp = requests.get(url, headers=headers, timeout=cfg.timeout)
        except (requests.Timeout, requests.ConnectionError) as exc:
            last_err = exc
            LOG.warning(
                f"http_get timeout/connection (attempt={attempt})",
                extra={"attempt": attempt, "url": url},
            )
        else:
            if resp.status_code == 200:
                if http_meta is not None:
                    http_meta["attempts"] = attempt
                    http_meta["last_status"] = 200
                try:
                    return cast(Dict[str, Any], resp.json())
                except json.JSONDecodeError as exc:  # pragma: no cover
                    raise ParseError(f"Invalid JSON from provider: {exc}") from exc
            if resp.status_code == 429:
                # Rate limit; raise after retries exhausted
                last_err = RateLimitError("HTTP 429 Too Many Requests")
                LOG.warning(
                    f"http_get 429 ratelimited (attempt={attempt})",
                    extra={"attempt": attempt, "url": url, "status": resp.status_code},
                )
                if http_meta is not None:  # pragma: no branch
                    http_meta["last_status"] = 429
            elif 500 <= resp.status_code < 600:
                last_err = ServerError(f"HTTP {resp.status_code}")
                LOG.warning(
                    f"http_get 5xx (status={resp.status_code}, attempt={attempt})",
                    extra={"attempt": attempt, "url": url, "status": resp.status_code},
                )
                if http_meta is not None:  # pragma: no branch
                    http_meta["last_status"] = resp.status_code
            else:
                # Unhandled status — do not retry unless 4xx/5xx categories above
                if http_meta is not None:  # pragma: no branch
                    http_meta["last_status"] = resp.status_code
                resp.raise_for_status()

        if attempt < cfg.max_retries:  # pragma: no branch
            sleep_s = cfg.backoff_base * (cfg.backoff_factor ** (attempt - 1))
            sleep_s += random.uniform(*cfg.jitter)
            if http_meta is not None:  # pragma: no branch
                http_meta["retries"] = int(http_meta.get("retries", 0)) + 1
                prev = float(http_meta.get("sleep_total_s", 0.0))
                http_meta["sleep_total_s"] = round(prev + float(sleep_s), 3)
            time.sleep(sleep_s)
        else:
            break

    if last_err is None:
        last_err = NetworkError("Unspecified network error")
    raise last_err


def _choose_range(start: date, end: date) -> str:
    span_days = (end - start).days
    if span_days <= 31:
        return "1mo"
    if span_days <= 93:
        return "3mo"
    if span_days <= 186:
        return "6mo"
    if span_days <= 366:
        return "1y"
    if span_days <= 5 * 366:
        return "5y"
    return "max"


def _build_url(symbol: str, rng: str) -> str:
    base = "https://brapi.dev/api/quote/%s?interval=1d&range=%s"
    return base % (symbol, rng)


def _normalize_to_ohlcv(symbol: str, payload: Dict[str, Any]) -> pd.DataFrame:
    if not isinstance(payload, dict) or "results" not in payload:
        raise ParseError("Unexpected payload structure: missing 'results'")
    results = payload.get("results")
    if not results or not isinstance(results, list):
        raise ParseError("Unexpected payload: empty 'results'")
    item = results[0]
    series = item.get("historicalDataPrice")
    if series is None:
        raise ParseError("Missing 'historicalDataPrice'")
    if not isinstance(series, list):
        raise ParseError("'historicalDataPrice' not a list")

    rows: List[Dict[str, Any]] = []
    for rec in series:
        try:
            ts = int(rec["date"])  # epoch seconds (UTC)
            o = float(rec["open"]) if rec.get("open") is not None else math.nan
            h = float(rec["high"]) if rec.get("high") is not None else math.nan
            low_val = float(rec["low"]) if rec.get("low") is not None else math.nan
            c = float(rec["close"]) if rec.get("close") is not None else math.nan
            v_raw = rec.get("volume")
            v = int(v_raw) if v_raw is not None else -1
        except (KeyError, ValueError, TypeError) as exc:
            LOG.warning("skip malformed row", extra={"error": str(exc), "rec": rec})
            continue
        rows.append(
            {
                "date": pd.to_datetime(ts, unit="s", utc=True),
                "symbol": str(symbol),
                "open": o,
                "high": h,
                "low": low_val,
                "close": c,
                "volume": v,
            }
        )

    df = pd.DataFrame.from_records(
        rows, columns=["date", "symbol", "open", "high", "low", "close", "volume"]
    )

    # Coerce dtypes
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], utc=True)
        df["symbol"] = df["symbol"].astype("string")
        for col in ["open", "high", "low", "close"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").astype("Int64")

        # Drop invalid rows (NaN or negatives)
        before = len(df)
        df = df.dropna(subset=["open", "high", "low", "close", "volume", "date", "symbol"])
        df = df[(df[["open", "high", "low", "close"]] >= 0).all(axis=1)]
        df = df[df["volume"] >= 0]
        removed = before - len(df)
        if removed:
            LOG.info("removed invalid rows", extra={"removed": removed})

        df = (
            df.sort_values("date")
            .drop_duplicates(subset=["symbol", "date"], keep="last")
            .reset_index(drop=True)
        )

        # Ensure exact dtypes: volume as int64 (not nullable) if possible
        if not df["volume"].isna().any():  # pragma: no branch
            df["volume"] = df["volume"].astype("int64")

    return df


def fetch_daily(
    symbol: str,
    start: date,
    end: date,
    *,
    http: HttpConfig | None = None,
    prefer_max: bool = False,
    throttle_wait: Optional[Callable[[], None]] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """Fetch daily OHLCV for a B3 symbol in [start, end].

    Returns a DataFrame with columns: date (UTC), symbol, open, high, low, close, volume.
    The provider is brapi.dev; data is filtered client-side to [start, end].
    """

    if not symbol or not symbol.strip():
        raise ValueError("symbol must be non-empty")
    if end < start:
        raise ValueError("end date must be >= start date")

    cfg = http or HttpConfig()
    rng = "max" if prefer_max else _choose_range(start, end)
    url = _build_url(symbol, rng)
    payload = _http_get_json(url, cfg=cfg, throttle_wait=throttle_wait, meta=meta)
    df = _normalize_to_ohlcv(symbol, payload)

    # filter date range (inclusive)
    if not df.empty:
        mask = (df["date"] >= pd.Timestamp(start, tz="UTC")) & (
            df["date"]
            <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        )
        df = df[mask].reset_index(drop=True)
        # If filtering yields no rows and we didn't query max, retry with max to cover older ranges
        if df.empty and rng != "max":
            LOG.info("empty after filter; retry with range=max", extra={"symbol": symbol})
            payload = _http_get_json(
                _build_url(symbol, "max"), cfg=cfg, throttle_wait=throttle_wait, meta=meta
            )
            df = _normalize_to_ohlcv(symbol, payload)
            mask = (df["date"] >= pd.Timestamp(start, tz="UTC")) & (
                df["date"]
                <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            )
            df = df[mask].reset_index(drop=True)
            rng = "max"

    if meta is not None:
        meta["range_used"] = rng

    return df


# Public alias for tests/docs
to_ohlcv = _normalize_to_ohlcv
