import pytest
from swing_trade.position_sizing import (
    PositionSizingConfig,
    calculate_position_size,
    stop_loss_price,
)


def test_calculate_position_size_basic() -> None:
    config = PositionSizingConfig(capital=10_000, risk_per_trade=0.02)
    entry = 100.0
    stop = 95.0
    assert calculate_position_size(config, entry, stop) == 40


def test_calculate_position_size_invalid_stop() -> None:
    config = PositionSizingConfig(capital=10_000, risk_per_trade=0.02)
    with pytest.raises(ValueError):
        calculate_position_size(config, 100.0, 100.0)


def test_stop_loss_price() -> None:
    assert stop_loss_price(100.0, 0.05) == 95.0
