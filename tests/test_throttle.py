from __future__ import annotations

from app.throttle import Throttler


def test_throttler_wait_schedules_correctly():
    calls: list[float] = []

    now = 0.0

    def now_fn() -> float:
        return now

    def sleep_fn(dt: float) -> None:
        nonlocal now
        calls.append(dt)
        now += dt

    t = Throttler(0.5, now_fn=now_fn, sleep_fn=sleep_fn)

    # First call: should not sleep (immediate)
    t.wait()
    assert calls == []

    # Immediately call again: should sleep 0.5s
    t.wait()
    assert calls == [0.5]

    # Immediately again: another 0.5s
    t.wait()
    assert calls == [0.5, 0.5]
