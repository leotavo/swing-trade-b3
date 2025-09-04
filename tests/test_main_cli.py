import json
from pathlib import Path

import pandas as pd
import pytest

from argparse import Namespace

from swing_trade_b3.__main__ import _parse_date, main
from swing_trade_b3 import __main__ as main_mod


def test_parse_date_valid_and_invalid():
    assert _parse_date("2024-01-02").isoformat() == "2024-01-02"
    with pytest.raises(Exception):
        _parse_date("2024-13-01")


def test_fetch_command_success_empty_and_errors(monkeypatch, tmp_path, capsys):
    # Stub fetch_daily: return df for OK, empty for EMPTY, raise for ERR; also call throttle when present
    def fake_fetch(
        symbol, start, end, prefer_max=False, throttle_wait=None, meta=None, **kwargs
    ):  # noqa: ARG001
        if throttle_wait is not None:
            throttle_wait()
        if symbol == "OK":
            if meta is not None:
                meta["range_used"] = "1mo"
                meta["http"] = {
                    "attempts": 1,
                    "retries": 0,
                    "sleep_total_s": 0.0,
                    "last_status": 200,
                    "throttle_calls": 1,
                }
            return pd.DataFrame.from_records(
                [
                    {
                        "date": pd.Timestamp("2024-01-02", tz="UTC"),
                        "symbol": "OK",
                        "open": 1.0,
                        "high": 2.0,
                        "low": 0.5,
                        "close": 1.5,
                        "volume": 10,
                    }
                ]
            )
        if symbol == "EMPTY":
            if meta is not None:
                meta["range_used"] = "1mo"
                meta["http"] = {"attempts": 1}
            return pd.DataFrame(
                columns=["date", "symbol", "open", "high", "low", "close", "volume"]
            )  # empty
        raise RuntimeError("boom")

    # Stub save_raw to avoid filesystem writes; return fake paths
    def fake_save_raw(symbol, df, base_dir, fmt="csv", **kwargs):  # noqa: ARG001
        return [Path(base_dir) / symbol / "2024.csv"]

    monkeypatch.setattr("swing_trade_b3.__main__.fetch_daily", fake_fetch)
    monkeypatch.setattr("swing_trade_b3.__main__.save_raw", fake_save_raw)

    symbols_file = tmp_path / "symbols.txt"
    symbols_file.write_text("# comment\nFILE1\n\n")

    rc = main(
        [
            "fetch",
            "--symbol",
            "OK",
            "",
            "EMPTY",
            "ERR",
            "--symbols-file",
            str(symbols_file),
            "--start",
            "2024-01-01",
            "--end",
            "2024-01-10",
            "--out",
            str(tmp_path / "out"),
            "--format",
            "csv",
            "--compression",
            "none",
            "--throttle",
            "0.01",
            "--log-json",
            "--json-summary",
            "-",
        ]
    )
    assert rc == 0  # one success (OK), EMPTY counts as failure in summary for no_data
    out = capsys.readouterr().out
    assert "Resumo:" in out and "Falhas:" in out
    # stdout json summary present
    assert out.strip().endswith("}")

    # Now write JSON summary to file
    summary_path = tmp_path / "summary.json"
    rc = main(
        [
            "fetch",
            "--symbol",
            "OK",
            "--start",
            "2024-01-01",
            "--end",
            "2024-01-10",
            "--out",
            str(tmp_path / "out"),
            "--json-summary",
            str(summary_path),
        ]
    )
    assert rc == 0 and summary_path.exists()
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    assert data["summary"]["ok"] >= 1

    # Force OSError when writing summary
    def boom_open(*a, **k):  # noqa: ANN001
        raise OSError("disk full")

    monkeypatch.setattr("builtins.open", boom_open)
    rc = main(
        [
            "fetch",
            "--symbol",
            "OK",
            "--start",
            "2024-01-01",
            "--end",
            "2024-01-10",
            "--out",
            str(tmp_path / "out"),
            "--json-summary",
            str(tmp_path / "x" / "sum.json"),
        ]
    )
    assert rc == 0


def test_fetch_command_validations(tmp_path):
    # end < start
    rc = main(
        [
            "fetch",
            "--symbol",
            "X",
            "--start",
            "2024-01-10",
            "--end",
            "2024-01-01",
            "--out",
            str(tmp_path),
        ]
    )
    assert rc == 2
    # missing symbols
    rc = main(["fetch", "--start", "2024-01-01", "--end", "2024-01-02", "--out", str(tmp_path)])
    assert rc == 2


def test_process_command_happy_and_no_data(tmp_path, capsys):
    # Prepare raw CSVs
    raw_dir = tmp_path / "data" / "raw" / "SYM"
    raw_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_records(
        [
            {
                "date": "2023-01-01",
                "symbol": "SYM",
                "open": 1,
                "high": 2,
                "low": 0.5,
                "close": 1.5,
                "volume": 10,
            },
            {
                "date": "2023-01-02",
                "symbol": "SYM",
                "open": 2,
                "high": 3,
                "low": 1.5,
                "close": 2.5,
                "volume": 20,
            },
        ]
    ).to_csv(raw_dir / "2023.csv", index=False)

    out_dir = tmp_path / "data" / "processed"

    rc = main(
        [
            "process",
            "--symbol",
            "SYM",
            "--raw",
            str(tmp_path / "data" / "raw"),
            "--out",
            str(out_dir),
            "--format",
            "csv",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "Processado" in out
    # Output file exists
    assert (out_dir / "SYM.csv").exists()

    # No data case
    rc = main(
        [
            "process",
            "--symbol",
            "NONE",
            "--raw",
            str(tmp_path / "data" / "raw"),
            "--out",
            str(out_dir),
            "--format",
            "csv",
        ]
    )
    assert rc == 1
    out = capsys.readouterr().out
    assert "Nenhum dado bruto" in out

    # invalid date range
    rc = main(
        [
            "process",
            "--symbol",
            "X",
            "--raw",
            str(tmp_path / "data" / "raw"),
            "--out",
            str(out_dir),
            "--format",
            "csv",
            "--start",
            "2024-02-02",
            "--end",
            "2024-01-01",
        ]
    )
    assert rc == 2


def test_fetch_parquet_kwargs_and_process_exceptions(monkeypatch, tmp_path, capsys):
    # Ensure fetch branch sets parquet compression kwargs
    def fake_fetch(symbol, start, end, **kwargs):  # noqa: ARG001
        return pd.DataFrame.from_records(
            [
                {
                    "date": pd.Timestamp("2024-01-02", tz="UTC"),
                    "symbol": symbol,
                    "open": 1.0,
                    "high": 1.5,
                    "low": 0.5,
                    "close": 1.2,
                    "volume": 10,
                }
            ]
        )

    def fake_save_raw(symbol, df, base_dir, fmt="csv", **kwargs):  # noqa: ARG001
        # validate that fmt and compression are passed when parquet selected
        assert fmt in ("csv", "parquet")
        return [Path(base_dir) / symbol / "2024.parquet"]

    monkeypatch.setattr("swing_trade_b3.__main__.fetch_daily", fake_fetch)
    monkeypatch.setattr("swing_trade_b3.__main__.save_raw", fake_save_raw)
    rc = main(
        [
            "fetch",
            "--symbol",
            "P",
            "--start",
            "2024-01-01",
            "--end",
            "2024-01-10",
            "--out",
            str(tmp_path / "out"),
            "--format",
            "parquet",
            "--compression",
            "snappy",
        ]
    )
    assert rc == 0

    # Process: hit parquet kwargs and exception branch
    ns = Namespace(
        log_json=False,
        symbol=["S"],
        start=None,
        end=None,
        raw=str(tmp_path / "raw"),
        out=str(tmp_path / "processed"),
        format="parquet",
        compression="snappy",
    )

    # monkeypatch save_processed to raise
    def boom(*a, **k):  # noqa: ANN001
        raise RuntimeError("write failed")

    monkeypatch.setattr(main_mod, "save_processed", boom)
    rc = main_mod._cmd_process(ns)
    assert rc == 1

    # Prepare real raw data and run via main() with parquet format, stubbing save_processed to avoid pyarrow
    raw_dir = tmp_path / "data" / "raw" / "XPTO"
    raw_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_records(
        [
            {
                "date": "2023-01-01",
                "symbol": "XPTO",
                "open": 1,
                "high": 2,
                "low": 0.5,
                "close": 1.5,
                "volume": 10,
            }
        ]
    ).to_csv(raw_dir / "2023.csv", index=False)

    def fake_save_processed(symbol, df, base_dir, fmt="parquet", **kwargs):  # noqa: ARG001
        # ensure parquet kwargs branch was evaluated
        assert fmt == "parquet"
        p = Path(base_dir) / f"{symbol}.parquet"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
        return p

    monkeypatch.setattr(main_mod, "save_processed", fake_save_processed)
    rc = main(
        [
            "process",
            "--symbol",
            "XPTO",
            "--raw",
            str(tmp_path / "data" / "raw"),
            "--out",
            str(tmp_path / "data" / "processed"),
            "--format",
            "parquet",
            "--compression",
            "snappy",
        ]
    )
    assert rc == 0


def test_cmd_process_not_symbols_direct():
    ns2 = Namespace(
        log_json=False,
        symbol=[],
        start=None,
        end=None,
        raw="raw",
        out="out",
        format="csv",
        compression="none",
    )

    assert main_mod._cmd_process(ns2) == 2


def test_module_entrypoint_executes_and_exits():
    import runpy

    with pytest.raises(SystemExit) as ex:
        runpy.run_module("swing_trade_b3.__main__", run_name="__main__")
    assert ex.value.code == 0


def test_fetch_symbols_file_oserror(monkeypatch, tmp_path):
    bad_path = tmp_path / "does-not-exist.txt"

    def boom_open(path, *a, **k):  # noqa: ANN001
        if str(path) == str(bad_path):
            raise OSError("permission denied")
        return open(path, *a, **k)  # fallback

    monkeypatch.setattr("builtins.open", boom_open)
    rc = main(
        [
            "fetch",
            "--symbol",
            "X",
            "--symbols-file",
            str(bad_path),
            "--start",
            "2024-01-01",
            "--end",
            "2024-01-02",
            "--out",
            str(tmp_path / "out"),
        ]
    )
    assert rc == 1


def test_cmd_process_exception_branch(monkeypatch, tmp_path):
    # Prepare raw data so load_raw returns non-empty
    sym = "EXC"
    raw_dir = tmp_path / "data" / "raw" / sym
    raw_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_records(
        [
            {
                "date": "2023-01-01",
                "symbol": sym,
                "open": 1,
                "high": 1,
                "low": 1,
                "close": 1,
                "volume": 1,
            }
        ]
    ).to_csv(raw_dir / "2023.csv", index=False)

    ns3 = Namespace(
        log_json=False,
        symbol=[sym],
        start=None,
        end=None,
        raw=str(tmp_path / "data" / "raw"),
        out=str(tmp_path / "data" / "processed"),
        format="csv",
        compression="none",
    )

    def boom(*a, **k):  # noqa: ANN001
        raise RuntimeError("fail")

    monkeypatch.setattr(main_mod, "save_processed", boom)
    rc = main_mod._cmd_process(ns3)
    assert rc == 1
