import pytest
from swing_trade.position_sizing import PositionSizingConfig, calculate_position_size
from swing_trade.signals import generate_signal_with_position


def test_calculate_position_size():
    config = PositionSizingConfig(capital=10_000, risk_per_trade=0.02)
    entry = 100.0
    stop = 95.0
    assert calculate_position_size(config, entry, stop) == 40


def test_generate_signal_with_position_buy():
    prices = [100, 101, 102, 103, 104, 105]
    config = PositionSizingConfig(capital=10_000, risk_per_trade=0.02)
    result = generate_signal_with_position(prices, config, 0.02)
    assert result["signal"] == "buy"
    assert result["position_size"] == 95
    assert result["stop_loss"] == pytest.approx(102.9)


def test_generate_signal_with_position_sell():
    prices = [105, 104, 103, 102, 101, 100]
    config = PositionSizingConfig(capital=10_000, risk_per_trade=0.02)
    result = generate_signal_with_position(prices, config, 0.02)
    assert result["signal"] == "sell"
    assert result["position_size"] == 0
    assert result["stop_loss"] is None
