import pytest
from swing_trade.position_sizing import (
    PositionSizingConfig,
    calculate_position_size,
    stop_loss_price,
)
from swing_trade.signals import TradeSignal, generate_signal_with_position


def test_calculate_position_size() -> None:
    config = PositionSizingConfig(capital=10_000, risk_per_trade=0.02)
    entry = 100.0
    stop = 95.0
    assert calculate_position_size(config, entry, stop) == 40


def test_generate_signal_with_position_buy() -> None:
    prices = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0]
    config = PositionSizingConfig(capital=10_000, risk_per_trade=0.02)
    result = generate_signal_with_position(prices, config, 0.02)
    assert isinstance(result, TradeSignal)
    assert result.signal == "buy"
    assert result.position_size == 95
    assert result.stop_loss == pytest.approx(102.9)


def test_generate_signal_with_position_sell() -> None:
    prices = [105.0, 104.0, 103.0, 102.0, 101.0, 100.0]
    config = PositionSizingConfig(capital=10_000, risk_per_trade=0.02)
    result = generate_signal_with_position(prices, config, 0.02)
    assert result.signal == "sell"
    assert result.position_size == 0
    assert result.stop_loss is None


@pytest.mark.parametrize("pct", [0.0, -0.01])  # type: ignore[misc]
def test_stop_loss_price_invalid_pct(pct: float) -> None:
    with pytest.raises(ValueError):
        stop_loss_price(100.0, pct)


@pytest.mark.parametrize("pct", [0.0, -0.01])  # type: ignore[misc]
def test_generate_signal_with_position_invalid_pct(pct: float) -> None:
    prices = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0]
    config = PositionSizingConfig(capital=10_000, risk_per_trade=0.02)
    with pytest.raises(ValueError):
        generate_signal_with_position(prices, config, pct)
