from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from swing_trade_b3.services.signals import STD_COLS, clean_and_validate


LOG = logging.getLogger(__name__)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_raw(
    symbol: str,
    df: pd.DataFrame,
    base_dir: str | Path = "data/raw",
    *,
    fmt: str = "csv",  # 'csv' or 'parquet'
    compression: Optional[str] = None,  # for parquet only
) -> list[Path]:
    """Persist raw OHLCV data partitioned by year: data/raw/{symbol}/YYYY.(csv|parquet).

    - Merges with existing files if present and deduplicates by (symbol, date).
    - Maintains ascending order by date.
    Returns list of written file paths.
    """
    if df.empty:
        LOG.info("no data to persist", extra={"symbol": symbol})
        return []

    base = Path(base_dir) / symbol
    ensure_dir(base)

    # ensure correct columns order
    cols = STD_COLS
    for col in cols:
        if col not in df.columns:
            raise ValueError(f"missing column in df: {col}")
    df = df[cols].copy()

    df["date"] = pd.to_datetime(df["date"], utc=True)
    df["year"] = df["date"].dt.year

    written: list[Path] = []
    for year, part in df.groupby("year"):
        part = part.drop(columns=["year"]).copy()

        if fmt == "parquet":
            path = base / f"{int(year)}.parquet"
            if path.exists():
                try:
                    existing = pd.read_parquet(path)
                except Exception:  # pragma: no cover - defensive
                    existing = pd.DataFrame(columns=cols)
                merged = part if existing.empty else pd.concat([existing, part], ignore_index=True)
            else:
                merged = part
            merged = (
                merged.drop_duplicates(subset=["symbol", "date"], keep="last")
                .sort_values("date")
                .reset_index(drop=True)
            )
            to_kwargs: dict = {"index": False}
            if compression and compression.lower() != "none":
                to_kwargs["compression"] = compression
            merged.to_parquet(path, **to_kwargs)
            size_bytes = path.stat().st_size if path.exists() else None
        else:
            path = base / f"{int(year)}.csv"
            if path.exists():
                try:
                    existing = pd.read_csv(path, parse_dates=["date"])
                except Exception:  # pragma: no cover - defensive
                    existing = pd.DataFrame(columns=cols)
                merged = part if existing.empty else pd.concat([existing, part], ignore_index=True)
            else:
                merged = part
            merged = (
                merged.drop_duplicates(subset=["symbol", "date"], keep="last")
                .sort_values("date")
                .reset_index(drop=True)
            )
            merged.to_csv(path, index=False)
            size_bytes = path.stat().st_size if path.exists() else None

        written.append(path)
        LOG.info(
            "saved raw partition",
            extra={
                "symbol": symbol,
                "year": int(year),
                "rows": len(merged),
                "path": str(path),
                "bytes": int(size_bytes) if size_bytes is not None else None,
            },
        )

    return written


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
                df = pd.read_csv(path, parse_dates=["date"])
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
            if getattr(start, "tz", None) is not None
            else pd.Timestamp(start, tz="UTC")
        )
        all_df = all_df[all_df["date"] >= s]
    if end is not None:
        e = (
            pd.Timestamp(end).tz_convert("UTC")
            if getattr(end, "tz", None) is not None
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
        if compression and compression.lower() != "none":  # pragma: no branch
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
