from statistics import mean
from typing import List

from .position_sizing import (
    PositionSizingConfig,
    calculate_position_size,
    stop_loss_price,
)


def generate_signal_with_position(
    prices: List[float],
    config: PositionSizingConfig,
    stop_loss_pct: float,
) -> dict:
    """Generate trading signal and position size based on price history.

    The signal is ``buy`` when the last price is above the simple moving average
    of the last five prices; otherwise ``sell``. For buy signals the function
    calculates position size and stop loss price.

    Args:
        prices: Historical closing prices ordered from oldest to newest.
        config: Position sizing configuration.
        stop_loss_pct: Percentage used to compute the stop loss for buys.

    Returns:
        Dictionary with signal information including position size and stop loss.
    """
    if len(prices) < 5:
        raise ValueError("At least five prices are required to generate a signal")

    last_price = prices[-1]
    sma = mean(prices[-5:])
    signal = "buy" if last_price > sma else "sell"

    if signal == "buy":
        sl_price = stop_loss_price(last_price, stop_loss_pct)
        size = calculate_position_size(config, last_price, sl_price)
    else:
        sl_price = None
        size = 0

    return {
        "signal": signal,
        "entry_price": last_price,
        "stop_loss": sl_price,
        "position_size": size,
    }
