import pandas as pd

from app.persistence import save_raw
from app.processing import clean_and_validate, load_raw, save_processed, STD_COLS


def make_df(rows):
    return pd.DataFrame.from_records(rows)


def test_save_raw_and_load_raw_csv_roundtrip(tmp_path):
    # two years, unordered, with duplicates
    rows = [
        {
            "date": "2023-01-02",
            "symbol": "PETR4",
            "open": 10,
            "high": 11,
            "low": 9,
            "close": 10.5,
            "volume": 100,
        },
        {
            "date": "2024-02-03",
            "symbol": "PETR4",
            "open": 12,
            "high": 13,
            "low": 11,
            "close": 12.5,
            "volume": 200,
        },
        {
            "date": "2023-01-02",
            "symbol": "PETR4",
            "open": 10,
            "high": 11,
            "low": 9,
            "close": 10.5,
            "volume": 100,
        },
    ]
    df = make_df(rows)

    paths = save_raw("PETR4", df, base_dir=tmp_path / "data" / "raw", fmt="csv")
    # two partitions
    assert len(paths) == 2
    assert all(p.suffix == ".csv" for p in paths)

    # merge again with an extra row; dedupe should keep unique
    more = make_df(
        [
            {
                "date": "2024-02-04",
                "symbol": "PETR4",
                "open": 12,
                "high": 14,
                "low": 11,
                "close": 13,
                "volume": 210,
            },
            {
                "date": "2023-01-02",
                "symbol": "PETR4",
                "open": 10,
                "high": 11,
                "low": 9,
                "close": 10.5,
                "volume": 100,
            },
        ]
    )
    save_raw("PETR4", more, base_dir=tmp_path / "data" / "raw", fmt="csv")

    # load back and filter
    all_df = load_raw("PETR4", base_dir=tmp_path / "data" / "raw")
    assert set(all_df.columns) == set(STD_COLS)
    # expect 3 unique rows total
    assert len(all_df) == 3

    # date filter
    sub = load_raw(
        "PETR4",
        base_dir=tmp_path / "data" / "raw",
        start=pd.Timestamp("2024-02-04", tz="UTC"),
        end=pd.Timestamp("2024-02-04", tz="UTC"),
    )
    assert len(sub) == 1


def test_save_raw_empty_and_parquet_merge(tmp_path, monkeypatch):
    import pandas as pd
    from pathlib import Path as _P

    # empty frame returns []
    empty = pd.DataFrame(columns=["date", "symbol", "open", "high", "low", "close", "volume"])
    assert save_raw("Z", empty, base_dir=tmp_path / "data" / "raw", fmt="csv") == []

    # Patch parquet IO to avoid pyarrow and still touch a file
    def fake_to_parquet(self, path, **kwargs):  # noqa: ANN001
        p = _P(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")

    monkeypatch.setattr(pd.DataFrame, "to_parquet", fake_to_parquet)
    monkeypatch.setattr(
        pd,
        "read_parquet",
        lambda path: pd.DataFrame(
            columns=["date", "symbol", "open", "high", "low", "close", "volume"]
        ),
    )

    df1 = pd.DataFrame.from_records(
        [
            {
                "date": "2022-12-31",
                "symbol": "Z",
                "open": 1,
                "high": 1,
                "low": 1,
                "close": 1,
                "volume": 1,
            }
        ]
    )
    save_raw("Z", df1, base_dir=tmp_path / "data" / "raw", fmt="parquet")

    # Second call should take parquet exists branch and merge
    df2 = pd.DataFrame.from_records(
        [
            {
                "date": "2022-12-31",
                "symbol": "Z",
                "open": 1,
                "high": 1,
                "low": 1,
                "close": 1,
                "volume": 1,
            },
            {
                "date": "2023-01-01",
                "symbol": "Z",
                "open": 2,
                "high": 2,
                "low": 2,
                "close": 2,
                "volume": 2,
            },
        ]
    )
    out_paths = save_raw("Z", df2, base_dir=tmp_path / "data" / "raw", fmt="parquet")
    assert any(p.suffix == ".parquet" for p in out_paths)


def test_save_raw_requires_columns(tmp_path):
    df = pd.DataFrame(
        {
            "date": ["2023-01-01"],
            "symbol": ["X"],
            "open": [1],
            "high": [1],
            "low": [1],
            "close": [1],
        }
    )
    try:
        save_raw("X", df, base_dir=tmp_path / "data" / "raw", fmt="csv")
        assert False, "expected ValueError for missing column 'volume'"
    except ValueError as exc:
        assert "missing column" in str(exc)


def test_clean_and_validate_handles_types_and_invalids():
    raw = pd.DataFrame.from_records(
        [
            {
                "date": "2023-01-01",
                "symbol": "A",
                "open": "10",
                "high": 12.0,
                "low": 8,
                "close": 11.0,
                "volume": "100",
            },
            {
                "date": "2023-01-02",
                "symbol": "A",
                "open": 9,
                "high": -1,
                "low": 7,
                "close": 8,
                "volume": 50,
            },  # invalid high
            {
                "date": "2023-01-01",
                "symbol": "A",
                "open": "10",
                "high": 12.0,
                "low": 8,
                "close": 11.0,
                "volume": "100",
            },  # duplicate
            {
                "date": "2023-01-03",
                "symbol": "A",
                "open": 10,
                "high": 11,
                "low": 9,
                "close": 10,
                "volume": None,
            },  # invalid volume
        ]
    )
    df = clean_and_validate(raw)
    # one valid unique row remains
    assert len(df) == 1
    assert list(df.columns) == STD_COLS
    assert df["volume"].dtype == "int64"


def test_clean_and_validate_empty_and_missing_column():
    import pytest

    # empty
    empty = pd.DataFrame()
    out = clean_and_validate(empty)
    assert list(out.columns) == STD_COLS
    # missing required column
    with pytest.raises(ValueError):
        clean_and_validate(
            pd.DataFrame(
                {
                    "date": ["2023-01-01"],
                    "symbol": ["X"],
                    "open": [1],
                    "high": [1],
                    "low": [1],
                    "close": [1],
                }
            )
        )


def test_save_processed_csv_merges_idempotently(tmp_path):
    rows1 = [
        {
            "date": "2023-01-01",
            "symbol": "B",
            "open": 1,
            "high": 2,
            "low": 0.5,
            "close": 1.5,
            "volume": 10,
        },
        {
            "date": "2023-01-02",
            "symbol": "B",
            "open": 2,
            "high": 3,
            "low": 1.5,
            "close": 2.5,
            "volume": 12,
        },
    ]
    rows2 = [
        {
            "date": "2023-01-02",
            "symbol": "B",
            "open": 2,
            "high": 3,
            "low": 1.5,
            "close": 2.5,
            "volume": 12,
        },  # duplicate
        {
            "date": "2023-01-03",
            "symbol": "B",
            "open": 3,
            "high": 4,
            "low": 2.5,
            "close": 3.5,
            "volume": 14,
        },
    ]
    df1 = pd.DataFrame.from_records(rows1)
    df2 = pd.DataFrame.from_records(rows2)

    out = tmp_path / "data" / "processed"
    p1 = save_processed("B", df1, base_dir=out, fmt="csv")
    assert p1.name.endswith(".csv")
    p2 = save_processed("B", df2, base_dir=out, fmt="csv")
    assert p2 == p1

    # Verify file contents merged to 3 unique rows
    final = pd.read_csv(p1, parse_dates=["date"])  # type: ignore[arg-type]
    assert len(final) == 3


def test_load_raw_skips_bad_and_handles_parquet_stub(tmp_path, monkeypatch):
    # Create symbol dir with a bad CSV and a fake Parquet; ensure it returns empty when only bad files exist
    sym_dir = tmp_path / "data" / "raw" / "BAD"
    sym_dir.mkdir(parents=True, exist_ok=True)
    # bad csv missing columns
    (sym_dir / "bad.csv").write_text("date\n2023-01-01\n")

    # parquet file with stubbed reader
    (sym_dir / "2020.parquet").write_text("binary")

    # Monkeypatch parquet reader to return a minimal valid frame
    def fake_read_parquet(path):  # noqa: ANN001
        return pd.DataFrame.from_records(
            [
                {
                    "date": "2020-01-01",
                    "symbol": "BAD",
                    "open": 1,
                    "high": 1,
                    "low": 1,
                    "close": 1,
                    "volume": 1,
                }
            ]
        )

    monkeypatch.setattr(pd, "read_parquet", fake_read_parquet)

    # existing but empty dir -> first case: remove the parquet to trigger empty files path
    (sym_dir / "2020.parquet").unlink()
    df_empty = load_raw("BAD", base_dir=tmp_path / "data" / "raw")
    assert df_empty.empty

    # Add parquet back and load
    (sym_dir / "2020.parquet").write_text("binary")
    df = load_raw("BAD", base_dir=tmp_path / "data" / "raw")
    assert not df.empty


def test_load_raw_empty_dir_returns_empty(tmp_path):
    sym_dir = tmp_path / "data" / "raw" / "EMPTY"
    sym_dir.mkdir(parents=True, exist_ok=True)
    out = load_raw("EMPTY", base_dir=tmp_path / "data" / "raw")
    assert out.empty
