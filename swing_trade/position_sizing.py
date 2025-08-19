from dataclasses import dataclass


@dataclass
class PositionSizingConfig:
    """Configuration for position sizing rules.

    Attributes:
        capital: Total trading capital available.
        risk_per_trade: Fraction of capital to risk per trade (e.g., 0.02 for 2%).
    """

    capital: float
    risk_per_trade: float


def stop_loss_price(entry_price: float, stop_loss_pct: float) -> float:
    """Calculate absolute stop loss price given an entry price and percentage.

    Args:
        entry_price: Price where the position is opened.
        stop_loss_pct: Stop loss percentage expressed as decimal (0.02 == 2%).

    Returns:
        Price level for the stop loss.
    """
    return entry_price * (1 - stop_loss_pct)


def calculate_position_size(
    config: PositionSizingConfig, entry_price: float, stop_loss_price: float
) -> int:
    """Calculate quantity of shares to trade based on risk parameters.

    Args:
        config: Position sizing configuration.
        entry_price: Price where the position is opened.
        stop_loss_price: Price where the trade will be exited if it goes against us.

    Returns:
        Integer number of shares to trade.

    Raises:
        ValueError: If the stop loss is not below the entry price.
    """
    risk_amount = config.capital * config.risk_per_trade
    risk_per_share = entry_price - stop_loss_price
    if risk_per_share <= 0:
        raise ValueError("Stop loss must be below entry price")
    return int(risk_amount / risk_per_share)
