from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

LOG = logging.getLogger(__name__)


STD_COLS = ["date", "symbol", "open", "high", "low", "close", "volume"]


def clean_and_validate(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Normalize and validate raw OHLCV into the processed dataset schema.

    Guarantees columns: date (UTC), symbol (string), open/high/low/close (float64), volume (int64),
    without nulls/negatives, deduped by (symbol,date), sorted by symbol,date (date strictly increasing per symbol).
    """
    if df_raw.empty:
        return pd.DataFrame(columns=STD_COLS).astype(
            {
                "date": "datetime64[ns, UTC]",
                "symbol": "string",
                "open": "float64",
                "high": "float64",
                "low": "float64",
                "close": "float64",
                "volume": "int64",
            }
        )

    df = df_raw.copy()

    # Ensure all required columns exist
    for col in STD_COLS:
        if col not in df.columns:
            raise ValueError(f"missing required column: {col}")

    # Coerce types
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df["symbol"] = df["symbol"].astype("string")
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").astype("Int64")

    # Remove invalids
    before = len(df)
    df = df.dropna(subset=STD_COLS)  # type: ignore[arg-type]
    df = df[(df[["open", "high", "low", "close"]] >= 0).all(axis=1)]
    df = df[df["volume"] >= 0]
    removed = before - len(df)
    if removed:
        LOG.info("processing: removed invalid rows", extra={"removed": int(removed)})

    # Order and dedupe by (symbol, date)
    df = (
        df.sort_values(["symbol", "date"])
        .drop_duplicates(subset=["symbol", "date"], keep="last")
        .reset_index(drop=True)
    )

    # Ensure non-nullable volume as int64
    if not df.empty:
        df["volume"] = df["volume"].astype("int64")

    # Validate strictly increasing date per symbol (after dedupe and sort)
    # If not strictly increasing, sorting/dedupe already enforces monotonic increase;
    # We can assert here to catch anomalies (optional):
    # for _, grp in df.groupby("symbol"):
    #     if not grp["date"].is_monotonic_increasing:
    #         raise AssertionError("dates must be strictly increasing per symbol")

    return df[STD_COLS]


def load_raw(
    symbol: str,
    base_dir: str | Path = "data/raw",
    *,
    start: Optional[pd.Timestamp] = None,
    end: Optional[pd.Timestamp] = None,
) -> pd.DataFrame:
    """Load raw OHLCV partitions for a symbol from data/raw and optionally filter by date.

    Supports CSV and Parquet files under data/raw/{symbol}/. Ensures STD_COLS and UTC timezone.
    """
    root = Path(base_dir) / symbol
    if not root.exists():
        return pd.DataFrame(columns=STD_COLS)

    files = list(root.glob("*.csv")) + list(root.glob("*.parquet"))
    if not files:
        return pd.DataFrame(columns=STD_COLS)

    frames: list[pd.DataFrame] = []
    for path in files:
        try:
            if path.suffix == ".csv":
                df = pd.read_csv(path, parse_dates=["date"])  # type: ignore[arg-type]
            else:
                df = pd.read_parquet(path)
        except Exception as exc:  # pragma: no cover - defensive
            LOG.warning(
                "processing: skip unreadable raw", extra={"path": str(path), "error": str(exc)}
            )
            continue
        # normalize columns order
        missing = [c for c in STD_COLS if c not in df.columns]
        if missing:
            LOG.warning(
                "processing: raw file missing columns",
                extra={"path": str(path), "missing": missing},
            )
            continue
        df = df[STD_COLS].copy()
        frames.append(df)

    if not frames:
        return pd.DataFrame(columns=STD_COLS)

    all_df = pd.concat(frames, ignore_index=True)
    # timezone/typing normalization
    all_df["date"] = pd.to_datetime(all_df["date"], utc=True)
    # optional filtering
    if start is not None:
        s = (
            pd.Timestamp(start).tz_convert("UTC")
            if start.tz is not None
            else pd.Timestamp(start, tz="UTC")
        )
        all_df = all_df[all_df["date"] >= s]
    if end is not None:
        e = (
            pd.Timestamp(end).tz_convert("UTC")
            if end.tz is not None
            else pd.Timestamp(end, tz="UTC")
        )
        all_df = all_df[all_df["date"] <= e]

    return all_df.reset_index(drop=True)


def save_processed(
    symbol: str,
    df: pd.DataFrame,
    base_dir: str | Path = "data/processed",
    *,
    fmt: str = "parquet",
    compression: Optional[str] = "snappy",
) -> Path:
    """Persist processed dataset for a symbol.

    Default: Parquet with snappy compression at data/processed/{symbol}.parquet.
    Idempotent merge with dedupe and ordering.
    """
    out_dir = Path(base_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Ensure cleaned schema
    dfc = clean_and_validate(df)

    if fmt == "parquet":
        path = out_dir / f"{symbol}.parquet"
        if path.exists():
            try:
                existing = pd.read_parquet(path)
            except Exception:  # pragma: no cover
                existing = pd.DataFrame(columns=STD_COLS)
            merged = pd.concat([existing, dfc], ignore_index=True)
        else:
            merged = dfc

        merged = (
            merged.sort_values(["symbol", "date"])
            .drop_duplicates(subset=["symbol", "date"], keep="last")
            .reset_index(drop=True)
        )

        to_kwargs: dict = {"index": False}
        if compression and compression.lower() != "none":
            to_kwargs["compression"] = compression
        merged.to_parquet(path, **to_kwargs)
    else:
        path = out_dir / f"{symbol}.csv"
        if path.exists():
            try:
                existing = pd.read_csv(path, parse_dates=["date"])
            except Exception:  # pragma: no cover
                existing = pd.DataFrame(columns=STD_COLS)
            merged = pd.concat([existing, dfc], ignore_index=True)
        else:
            merged = dfc
        merged = (
            merged.sort_values(["symbol", "date"])
            .drop_duplicates(subset=["symbol", "date"], keep="last")
            .reset_index(drop=True)
        )
        merged.to_csv(path, index=False)

    LOG.info(
        "saved processed dataset",
        extra={
            "symbol": symbol,
            "rows": int(len(dfc)),
            "rows_merged": int(len(merged)),
            "path": str(path),
        },
    )

    return path
