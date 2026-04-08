"""
Abstract base class for all trading strategies in AdaptiveFX.

Every concrete strategy (TrendFollowing, MeanReversion, Breakout) must
subclass ``BaseStrategy`` and implement the abstract methods defined here.
Common utilities (ATR-based SL/TP calculation, parameter validation
helpers) are provided in this base class so they don't need to be
duplicated.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd
from loguru import logger


class BaseStrategy(ABC):
    """Abstract base class for AdaptiveFX trading strategies.

    Subclasses must implement :meth:`generate_signals` and
    :meth:`validate_params`.  The Genetic Algorithm optimiser calls these
    methods during the fitness evaluation loop.
    """

    # Strategy name — override in subclasses
    NAME: str = "BaseStrategy"

    # ------------------------------------------------------------------
    @abstractmethod
    def generate_signals(
        self, df: pd.DataFrame, params: dict
    ) -> pd.DataFrame:
        """Generate buy/sell entry and exit signals from OHLCV data.

        Args:
            df: OHLCV DataFrame with a DatetimeIndex.
            params: Strategy-specific parameter dictionary (as returned by
                :meth:`get_default_params` or the GA optimiser).

        Returns:
            DataFrame with two boolean columns: ``entries`` (long signal)
            and ``exits`` (close signal), aligned with ``df``'s index.
        """
        ...

    # ------------------------------------------------------------------
    @abstractmethod
    def validate_params(self, params: dict) -> bool:
        """Validate that a parameter dictionary is within acceptable bounds.

        Args:
            params: Strategy parameter dictionary to validate.

        Returns:
            True if all parameters are valid, False otherwise.
        """
        ...

    # ------------------------------------------------------------------
    def get_default_params(self) -> dict:
        """Return the default parameter set for this strategy.

        Subclasses should override this method to provide strategy-specific
        defaults.

        Returns:
            Dictionary of parameter names → default values.
        """
        return {}

    # ------------------------------------------------------------------
    def calculate_atr(
        self, df: pd.DataFrame, period: int = 14
    ) -> pd.Series:
        """Calculate the Average True Range (ATR) for a DataFrame.

        Args:
            df: OHLCV DataFrame with ``high``, ``low``, and ``close`` columns.
            period: ATR lookback period in bars.

        Returns:
            Series of ATR values aligned with ``df``'s index.
        """
        # TODO: Implement via pandas-ta or manual rolling calculation
        # import pandas_ta as ta
        # return ta.atr(df['high'], df['low'], df['close'], length=period)
        logger.warning("calculate_atr() not yet implemented.")
        return pd.Series(dtype=float, index=df.index)

    # ------------------------------------------------------------------
    def apply_sl_tp(
        self,
        entry_price: float,
        atr: float,
        sl_atr_mult: float = 1.5,
        tp_atr_mult: float = 3.0,
        direction: str = "long",
    ) -> tuple[float, float]:
        """Calculate Stop Loss and Take Profit prices from ATR.

        Args:
            entry_price: Trade entry price.
            atr: ATR value at the time of entry.
            sl_atr_mult: ATR multiplier for the stop loss distance.
            tp_atr_mult: ATR multiplier for the take profit distance.
            direction: ``"long"`` or ``"short"``.

        Returns:
            Tuple of ``(stop_loss_price, take_profit_price)``.
        """
        # TODO: Implement direction-aware SL/TP calculation
        # sl_dist = atr * sl_atr_mult
        # tp_dist = atr * tp_atr_mult
        # if direction == "long":
        #     return entry_price - sl_dist, entry_price + tp_dist
        # else:
        #     return entry_price + sl_dist, entry_price - tp_dist
        logger.warning("apply_sl_tp() not yet implemented.")
        return 0.0, 0.0
