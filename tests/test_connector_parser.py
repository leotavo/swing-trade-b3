import pandas as pd


def sample_payload() -> dict:
    return {
        "results": [
            {
                "symbol": "TEST3",
                "historicalDataPrice": [
                    {
                        "date": 1704067200,  # 2024-01-01 UTC
                        "open": 10.0,
                        "high": 11.0,
                        "low": 9.5,
                        "close": 10.5,
                        "volume": 1000,
                        "adjustedClose": 10.5,
                    },
                    {
                        "date": 1704153600,  # 2024-01-02 UTC
                        "open": 10.5,
                        "high": 11.2,
                        "low": 10.1,
                        "close": 11.0,
                        "volume": 2000,
                        "adjustedClose": 11.0,
                    },
                    # duplicate of first row to test dedupe
                    {
                        "date": 1704067200,
                        "open": 10.0,
                        "high": 11.0,
                        "low": 9.5,
                        "close": 10.5,
                        "volume": 1000,
                        "adjustedClose": 10.5,
                    },
                ],
            }
        ]
    }


def test_to_ohlcv_shape_and_types():
    from app.connector.b3 import to_ohlcv

    sym = "TEST3"
    df = to_ohlcv(sym, sample_payload())

    # columns and no duplicates
    assert list(df.columns) == [
        "date",
        "symbol",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    assert len(df) == 2  # duplicate removed

    # dtypes
    # dtype check without deprecated is_datetime64tz_dtype
    assert isinstance(df["date"].dtype, pd.DatetimeTZDtype)
    assert str(df["date"].dt.tz) == "UTC"
    for col in ["open", "high", "low", "close"]:
        assert df[col].dtype == "float64"
        assert (df[col] >= 0).all()
    assert df["volume"].dtype == "int64"

    # sorted ascending by date
    assert df["date"].is_monotonic_increasing
