from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

import pandas as pd

LOG = logging.getLogger(__name__)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _std_cols() -> list[str]:
    return ["date", "symbol", "open", "high", "low", "close", "volume"]


def save_raw(
    symbol: str,
    df: pd.DataFrame,
    base_dir: str | Path = "data/raw",
    *,
    fmt: str = "csv",  # 'csv' or 'parquet'
    compression: Optional[str] = None,  # for parquet only: 'snappy', 'zstd', 'gzip', 'brotli'
) -> list[Path]:
    """Persist raw OHLCV data partitioned by year: data/raw/{symbol}/YYYY.csv.

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
    cols = _std_cols()
    for col in cols:
        if col not in df.columns:
            raise ValueError(f"missing column in df: {col}")
    df = df[cols].copy()

    df["date"] = pd.to_datetime(df["date"], utc=True)
    df["year"] = df["date"].dt.year

    written: List[Path] = []
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
