import pytest

from app.throttle import Throttler


def test_throttler_waits_and_validates():
    now = 0.0
    slept = {"s": 0.0}

    def now_fn():
        return now

    def sleep_fn(s):
        slept["s"] += s
        nonlocal_now[0] += s  # advance time

    # use a list to allow closure mutation in sleep_fn
    nonlocal_now = [now]

    def now_fn2():
        return nonlocal_now[0]

    t = Throttler(1.0, now_fn=now_fn2, sleep_fn=sleep_fn)

    # first call should not sleep
    t.wait()
    assert slept["s"] == 0

    # second call immediately should sleep ~1.0s
    t.wait()
    assert slept["s"] == pytest.approx(1.0, rel=1e-3)

    # advance time beyond next_ready; no further sleep
    nonlocal_now[0] += 1.1
    t.wait()
    assert slept["s"] == pytest.approx(1.0, rel=1e-3)


def test_throttler_rejects_negative_interval():
    with pytest.raises(ValueError):
        Throttler(-0.1)
