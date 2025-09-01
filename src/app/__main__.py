from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import date, datetime, timezone

from . import __version__
from .connector import fetch_daily
from .persistence import save_raw


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

    return p


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _cmd_fetch(args: argparse.Namespace) -> int:
    _setup_logging()
    symbols: list[str] = [s.strip() for s in (args.symbol or [])]
    start: date = args.start
    end: date = args.end
    base_out: str = args.out
    throttle_s: float = float(args.throttle)
    out_fmt: str = args.format
    compression: str = args.compression
    symbols_file: str | None = args.symbols_file
    json_summary: str | None = args.json_summary

    # Merge symbols from file if provided
    if symbols_file:
        try:
            with open(symbols_file, "r", encoding="utf-8") as fh:
                extra = [ln.strip() for ln in fh if ln.strip() and not ln.strip().startswith("#")]
                symbols.extend(extra)
        except OSError as exc:
            print(f"Erro ao ler --symbols-file: {exc}")
            return 1

    if end < start:
        print("Erro: --end deve ser >= --start")
        return 2
    if not symbols:
        print("Erro: --symbol não pode ser vazio")
        return 2

    # Setup throttler if requested
    throttle_wait = None
    if throttle_s > 0:
        from .throttle import Throttler

        throttle_wait = Throttler(throttle_s).wait

    successes = 0
    failures: list[tuple[str, str]] = []
    per_symbol: list[dict] = []
    run_started = datetime.now(timezone.utc)
    for symbol in symbols:
        if not symbol:
            continue
        t0 = time.monotonic()
        meta: dict = {}
        try:
            df = fetch_daily(
                symbol,
                start,
                end,
                prefer_max=bool(args.force_max),
                throttle_wait=throttle_wait,
                meta=meta,
            )
        except Exception as exc:
            logging.error("falha na coleta", exc_info=False)
            msg = str(exc)
            print(f"[{symbol}] Erro na coleta: {msg}")
            failures.append((symbol, msg))
            per_symbol.append(
                {
                    "symbol": symbol,
                    "status": "error",
                    "error": msg,
                    "files": [],
                    "rows": 0,
                    "duration_s": round(time.monotonic() - t0, 3),
                    "http": meta.get("http"),
                }
            )
            continue

        rows = len(df)
        if rows == 0:
            msg = f"Nenhuma linha no período [{start}..{end}]. Nada a salvar."
            print(f"[{symbol}] {msg}")
            failures.append((symbol, "sem dados no período"))
            per_symbol.append(
                {
                    "symbol": symbol,
                    "status": "no_data",
                    "files": [],
                    "rows": 0,
                    "range_used": meta.get("range_used"),
                    "duration_s": round(time.monotonic() - t0, 3),
                    "http": meta.get("http"),
                }
            )
            continue

        parquet_kwargs = {}
        if out_fmt == "parquet":
            parquet_kwargs["compression"] = None if compression == "none" else compression

        paths = save_raw(symbol, df, base_out, fmt=out_fmt, **parquet_kwargs)
        first = df["date"].min()
        last = df["date"].max()
        print(
            f"[{symbol}] OK: {rows} linhas ({first.date()}..{last.date()}); salvo em {len(paths)} arquivo(s)."
        )
        for p in paths:
            print(f" - {p}")
        successes += 1
        per_symbol.append(
            {
                "symbol": symbol,
                "status": "ok",
                "rows": int(rows),
                "date_first": str(first.date()),
                "date_last": str(last.date()),
                "files": [str(p) for p in paths],
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


def main(argv: list[str] | None = None) -> int:
    parser = _make_parser()
    # Use parse_known_args to be resilient to external flags (e.g., pytest -q)
    args, _unknown = parser.parse_known_args(argv)
    if args.cmd == "fetch":
        return _cmd_fetch(args)
    # default: show brief info when no subcommand
    print(f"swing-trade-b3 {__version__} - use 'fetch --help' para coletar dados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
