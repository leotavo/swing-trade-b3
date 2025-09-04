from __future__ import annotations

import pandas as pd

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

    # Remove invalids (no logging in functional core)
    df = df.dropna(subset=STD_COLS)
    df = df[(df[["open", "high", "low", "close"]] >= 0).all(axis=1)]
    df = df[df["volume"] >= 0]
    # Intentionally no logging here (functional core): callers may observe sizes externally

    # Order and dedupe by (symbol, date)
    df = (
        df.sort_values(["symbol", "date"])
        .drop_duplicates(subset=["symbol", "date"], keep="last")
        .reset_index(drop=True)
    )

    # Ensure non-nullable volume as int64
    if not df.empty:  # pragma: no branch
        df["volume"] = df["volume"].astype("int64")

    return df[STD_COLS]

