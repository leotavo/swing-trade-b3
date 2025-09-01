from __future__ import annotations

from pathlib import Path

import pandas as pd


def make_raw() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": [
                "2023-01-02",
                "2023-01-03",
                "2023-01-03",  # duplicate date
                "2023-01-04",
                "2023-01-05",
            ],
            "symbol": ["TEST3", "TEST3", "TEST3", "TEST3", "TEST3"],
            "open": [10.0, 10.5, 10.5, 10.6, None],  # last row None -> removed
            "high": [11.0, 11.2, 11.2, 11.3, 11.4],
            "low": [9.5, 10.1, 10.1, 10.2, 10.3],
            "close": [10.5, 11.0, 11.0, 11.1, 11.2],
            "volume": [1000, 2000, 2000, -5, 3000],  # negative volume row removed
        }
    )


def test_clean_and_validate_basic():
    from app.processing import clean_and_validate

    raw = make_raw()
    df = clean_and_validate(raw)

    # Columns and types
    assert list(df.columns) == ["date", "symbol", "open", "high", "low", "close", "volume"]
    assert isinstance(df["date"].dtype, pd.DatetimeTZDtype)
    assert str(df["date"].dt.tz) == "UTC"
    assert df["symbol"].dtype == "string"
    for col in ["open", "high", "low", "close"]:
        assert df[col].dtype == "float64"
    assert df["volume"].dtype == "int64"

    # Invalid rows removed (negative volume, None in open) and duplicate dropped -> expect 2 rows
    assert len(df) == 2

    # Dedup by (symbol,date)
    assert df["date"].is_monotonic_increasing
    assert df.drop_duplicates(["symbol", "date"]).shape[0] == df.shape[0]


def test_save_processed_idempotent(tmp_path: Path):
    from app.processing import clean_and_validate, save_processed
    import pandas as pd

    raw = make_raw()
    df = clean_and_validate(raw)

    p = save_processed("TEST3", df, base_dir=tmp_path, fmt="parquet", compression="snappy")
    assert p.exists() and p.suffix == ".parquet"

    # Save again with duplicated content -> should remain the same length
    p2 = save_processed("TEST3", df, base_dir=tmp_path, fmt="parquet", compression="snappy")
    assert p2 == p

    back = pd.read_parquet(p)
    assert len(back) == len(df)
    # Sorted and unique by (symbol,date)
    assert back.sort_values(["symbol", "date"]).equals(back)
    assert back.drop_duplicates(["symbol", "date"]).shape[0] == back.shape[0]
