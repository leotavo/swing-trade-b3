from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable


NowFn = Callable[[], float]
SleepFn = Callable[[float], None]


@dataclass
class Throttler:
    min_interval_s: float
    now_fn: NowFn = time.monotonic
    sleep_fn: SleepFn = time.sleep

    def __post_init__(self) -> None:
        if self.min_interval_s < 0:
            raise ValueError("min_interval_s must be >= 0")
        # Initialize so first call is allowed immediately
        self._next_ready = self.now_fn()

    def wait(self) -> None:
        now = self.now_fn()
        if now < self._next_ready:
            self.sleep_fn(self._next_ready - now)
            now = self._next_ready
        # Schedule next availability
        self._next_ready = now + self.min_interval_s
