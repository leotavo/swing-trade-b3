from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol, runtime_checkable

import pandas as pd


@runtime_checkable
class DataProviderPort(Protocol):
    def fetch_daily(self, symbol: str, start: date, end: date) -> pd.DataFrame: ...


@runtime_checkable
class RepositoryPort(Protocol):
    def save_raw(self, symbol: str, df: pd.DataFrame) -> None: ...
    def load_raw(self, symbol: str, start: date | None = None, end: date | None = None) -> pd.DataFrame: ...
    def save_processed(self, symbol: str, df: pd.DataFrame) -> None: ...


@runtime_checkable
class OrderExecutorPort(Protocol):
    def place_order(self, symbol: str, qty: int, side: str) -> str: ...


@runtime_checkable
class Strategy(Protocol):
    def generate(self, df: pd.DataFrame) -> pd.DataFrame: ...


@dataclass(frozen=True)
class Signal:
    date: pd.Timestamp
    symbol: str
    action: str  # "buy" | "sell"

