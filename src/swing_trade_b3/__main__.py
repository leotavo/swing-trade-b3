from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import date, datetime, timezone

import pandas as pd

from . import __version__
from .adapters.connectors.market_data.composite_provider import fetch_daily
from .adapters.persistence.repositories import (
    load_raw,
    save_processed,
    save_raw,
)
from .services.signals import clean_and_validate


def _parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError as exc:  # pragma: no cover
        raise argparse.ArgumentTypeError(f"invalid date (YYYY-MM-DD): {s}") from exc


def _make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="swing-trade-b3", description="Ferramentas B3")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="cmd")

    # fetch command
    pf = sub.add_parser(
        "fetch",
        help="Coleta OHLCV diário de um símbolo no período informado",
    )
    pf.add_argument("--symbol", "-s", nargs="+", required=False, help="Ticker(s), ex.: PETR4 VALE3")
    pf.add_argument("--start", required=True, type=_parse_date, help="Data inicial YYYY-MM-DD")
    pf.add_argument("--end", required=True, type=_parse_date, help="Data final YYYY-MM-DD")
    pf.add_argument("--out", default="data/raw", help="Diretório base de saída (default: data/raw)")
    pf.add_argument(
        "--force-max",
        action="store_true",
        help="Força range=max no provedor (baixa todo histórico e filtra)",
    )
    pf.add_argument(
        "--throttle",
        type=float,
        default=0.0,
        help="Intervalo mínimo entre requisições em segundos (ex.: 0.2)",
    )
    pf.add_argument(
        "--format",
        choices=["csv", "parquet"],
        default="csv",
        help="Formato de saída para dados brutos (csv|parquet)",
    )
    pf.add_argument(
        "--compression",
        choices=["none", "snappy", "zstd"],
        default="none",
        help="Compressão para Parquet (snappy|zstd). Ignorado em CSV.",
    )
    pf.add_argument(
        "--symbols-file",
        help="Arquivo texto com 1 ticker por linha (ignora linhas vazias e iniciadas por #)",
    )
    pf.add_argument(
        "--json-summary",
        metavar="PATH|-",
        help="Emite resumo em JSON (use '-' para stdout)",
    )
    pf.add_argument(
        "--log-json",
        action="store_true",
        help="Ativa logging estruturado em JSON no stdout",
    )

    # process command
    pp = sub.add_parser(
        "process",
        help="Processa dados brutos de data/raw para data/processed",
    )
    pp.add_argument("--symbol", "-s", nargs="+", required=True, help="Ticker(s), ex.: PETR4 VALE3")
    pp.add_argument("--start", type=_parse_date, help="Data inicial YYYY-MM-DD", required=False)
    pp.add_argument("--end", type=_parse_date, help="Data final YYYY-MM-DD", required=False)
    pp.add_argument(
        "--raw", default="data/raw", help="Diretório base dos dados brutos (default: data/raw)"
    )
    pp.add_argument(
        "--out", default="data/processed", help="Diretório de saída (default: data/processed)"
    )
    pp.add_argument(
        "--format",
        choices=["csv", "parquet"],
        default="parquet",
        help="Formato de saída para dados processados (csv|parquet)",
    )
    pp.add_argument(
        "--compression",
        choices=["none", "snappy", "zstd"],
        default="snappy",
        help="Compressão para Parquet (snappy|zstd). Ignorado em CSV.",
    )
    pp.add_argument(
        "--log-json",
        action="store_true",
        help="Ativa logging estruturado em JSON no stdout",
    )

    return p


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover
        payload: dict[str, object] = {
            "time": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        std = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
        }
        for k, v in record.__dict__.items():
            if k not in std:
                payload[k] = v
        return json.dumps(payload, ensure_ascii=False)


def _setup_logging(as_json: bool) -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.INFO)
    h = logging.StreamHandler()
    if as_json:
        h.setFormatter(_JsonFormatter())
    root.addHandler(h)


def _cmd_fetch(args: argparse.Namespace) -> int:
    _setup_logging(bool(args.log_json))
    symbols: list[str] = []
    if args.symbol:
        symbols.extend([s.strip() for s in args.symbol if s.strip()])
    if args.symbols_file:
        try:
            with open(args.symbols_file, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    symbols.append(line)
        except OSError as exc:
            print(f"Aviso: não foi possível ler --symbols-file ({exc})")

    start: date = args.start
    end: date = args.end
    out_dir: str = args.out
    out_fmt: str = args.format
    compression: str = args.compression
    throttle_s: float = float(args.throttle or 0.0)

    if end < start:
        print("Erro: --end deve ser >= --start")
        return 2
    if not symbols:
        print("Erro: --symbol não pode ser vazio")
        return 2

    successes = 0
    failures: list[tuple[str, str]] = []
    per_symbol: list[dict[str, object]] = []
    run_started = datetime.now(timezone.utc)
    for sym in symbols:
        t0 = time.monotonic()
        meta: dict[str, object] = {}
        try:
            throttle_calls = {"n": 0}

            def maybe_throttle() -> None:
                # track calls; actual sleep controlled by caller
                throttle_calls["n"] += 1
                if throttle_s > 0:
                    time.sleep(throttle_s)

            df = fetch_daily(
                sym,
                start,
                end,
                prefer_max=bool(args.force_max),
                throttle_wait=maybe_throttle,
                meta=meta,
            )
            if df.empty:
                print(f"[{sym}] Nenhum dado retornado no intervalo.")
                failures.append((sym, "no_data"))
                per_symbol.append(
                    {
                        "symbol": sym,
                        "status": "no_data",
                        "rows": 0,
                        "files": [],
                        "provider": meta.get("provider"),
                        "range_used": meta.get("range_used"),
                        "date_first": None,
                        "date_last": None,
                        "http": meta.get("http"),
                    }
                )
                continue

            # Persist raw partitions
            parquet_kwargs = {}
            if out_fmt == "parquet":
                parquet_kwargs["compression"] = None if compression == "none" else compression
            paths = save_raw(sym, df, base_dir=out_dir, fmt=out_fmt, **parquet_kwargs)
            successes += 1
            first = df["date"].min()
            last = df["date"].max()
            per_symbol.append(
                {
                    "symbol": sym,
                    "status": "ok",
                    "rows": int(len(df)),
                    "provider": meta.get("provider"),
                    "date_first": str(first.date()),
                    "date_last": str(last.date()),
                    "files": [str(p) for p in paths],
                    "range_used": meta.get("range_used"),
                    "duration_s": round(time.monotonic() - t0, 3),
                    "http": meta.get("http"),
                }
            )
        except Exception as exc:
            logging.error("falha na coleta", exc_info=False)
            print(f"[{sym}] Erro: {exc}")
            failures.append((sym, str(exc)))
            per_symbol.append(
                {
                    "symbol": sym,
                    "status": "failed",
                    "rows": 0,
                    "files": [],
                    "provider": meta.get("provider"),
                    "date_first": None,
                    "date_last": None,
                    "range_used": meta.get("range_used"),
                    "duration_s": round(time.monotonic() - t0, 3),
                    "http": meta.get("http"),
                }
            )

    # final summary (M2-SI-7.2)
    total = len(symbols)
    print(f"Resumo: {successes}/{total} símbolos com sucesso.")
    if failures:
        print("Falhas:")
        for sym, msg in failures:
            print(f" - {sym}: {msg}")

    json_summary = getattr(args, "json_summary", None)
    if json_summary:
        run_ended = datetime.now(timezone.utc)
        payload = {
            "run": {
                "started_at": run_started.isoformat(),
                "ended_at": run_ended.isoformat(),
                "duration_s": round((run_ended - run_started).total_seconds(), 3),
                "provider": "brapi.dev",
                "args": {
                    "start": str(start),
                    "end": str(end),
                    "format": out_fmt,
                    "compression": None if compression == "none" else compression,
                    "throttle": throttle_s if throttle_s > 0 else None,
                    "force_max": bool(args.force_max),
                    "symbols": symbols,
                },
            },
            "symbols": per_symbol,
            "summary": {
                "ok": successes,
                "no_data": sum(1 for s in per_symbol if s["status"] == "no_data"),
                "failed": len(failures),
                "total": len(symbols),
            },
        }

        try:
            if json_summary == "-":
                print(json.dumps(payload, ensure_ascii=False))
            else:
                from pathlib import Path

                Path(json_summary).parent.mkdir(parents=True, exist_ok=True)
                with open(json_summary, "w", encoding="utf-8") as fh:
                    json.dump(payload, fh, ensure_ascii=False, indent=2)
        except OSError as exc:
            print(f"Aviso: falha ao gravar JSON summary ({exc})")

    return 0 if successes > 0 else 1


def _cmd_process(args: argparse.Namespace) -> int:
    _setup_logging(bool(args.log_json))
    symbols: list[str] = [s.strip() for s in (args.symbol or [])]
    start: date | None = args.start
    end: date | None = args.end
    raw_dir: str = args.raw
    out_dir: str = args.out
    out_fmt: str = args.format
    compression: str = args.compression

    if end is not None and start is not None and end < start:
        print("Erro: --end deve ser >= --start")
        return 2
    if not symbols:
        print("Erro: --symbol não pode ser vazio")
        return 2

    successes = 0
    failures: list[tuple[str, str]] = []
    for sym in symbols:
        try:
            df_raw = load_raw(
                sym,
                raw_dir,
                start=pd.Timestamp(start, tz="UTC") if start else None,
                end=pd.Timestamp(end, tz="UTC") if end else None,
            )
            if df_raw.empty:
                print(f"[{sym}] Nenhum dado bruto encontrado no intervalo.")
                failures.append((sym, "sem dados brutos"))
                continue
            df = clean_and_validate(df_raw)
            parquet_kwargs = {}
            if out_fmt == "parquet":
                parquet_kwargs["compression"] = None if compression == "none" else compression
            path = save_processed(sym, df, base_dir=out_dir, fmt=out_fmt, **parquet_kwargs)
            print(f"[{sym}] Processado {len(df)} linhas -> {path}")
            successes += 1
        except Exception as exc:
            logging.error("falha no processamento", exc_info=False)
            print(f"[{sym}] Erro no processamento: {exc}")
            failures.append((sym, str(exc)))

    total = len(symbols)
    print(f"Resumo processamento: {successes}/{total} símbolos com sucesso.")
    if failures:
        print("Falhas:")
        for sym, msg in failures:
            print(f" - {sym}: {msg}")

    return 0 if successes > 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = _make_parser()
    # Ensure pytest or shell flags don't leak into parsing when argv is None
    argv = [] if argv is None else argv
    # Use parse_known_args to be resilient to external flags (e.g., pytest -q)
    args, _unknown = parser.parse_known_args(argv)
    if args.cmd == "fetch":
        return _cmd_fetch(args)
    if args.cmd == "process":
        return _cmd_process(args)
    # default: show brief info when no subcommand
    print(f"swing-trade-b3 {__version__} - use 'fetch --help' para coletar dados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

