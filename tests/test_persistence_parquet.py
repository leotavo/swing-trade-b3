from __future__ import annotations

from pathlib import Path

import pandas as pd


def test_save_raw_parquet(tmp_path):
    from swing_trade_b3.adapters.persistence.repositories import save_raw

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2023-01-02", "2023-01-03"], utc=True),
            "symbol": ["TEST3", "TEST3"],
            "open": [10.0, 10.5],
            "high": [11.0, 11.2],
            "low": [9.5, 10.1],
            "close": [10.5, 11.0],
            "volume": [1000, 2000],
        }
    )

    out = tmp_path / "data" / "raw"
    paths = save_raw("TEST3", df, base_dir=out, fmt="parquet")

    assert len(paths) == 1
    p: Path = paths[0]
    assert p.suffix == ".parquet"
    assert p.exists()

    # Read back
    back = pd.read_parquet(p)
    assert len(back) == 2
    assert list(back.columns) == [
        "date",
        "symbol",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]


def test_save_raw_parquet_with_compression(tmp_path):
    from swing_trade_b3.adapters.persistence.repositories import save_raw

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2023-01-02", "2023-01-03"], utc=True),
            "symbol": ["TEST3", "TEST3"],
            "open": [10.0, 10.5],
            "high": [11.0, 11.2],
            "low": [9.5, 10.1],
            "close": [10.5, 11.0],
            "volume": [1000, 2000],
        }
    )

    out = tmp_path / "data" / "raw"
    paths = save_raw("TEST3", df, base_dir=out, fmt="parquet", compression="snappy")
    assert len(paths) == 1
    p = paths[0]
    assert p.suffix == ".parquet"
    # read back
    back = pd.read_parquet(p)
    assert len(back) == 2
