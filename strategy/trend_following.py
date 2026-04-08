"""
Trend Following strategy for AdaptiveFX.

Activated when the regime detector classifies the market as ``TRENDING``.
The strategy uses a dual-EMA crossover to identify trend direction and an
ADX filter to ensure sufficient trend strength before entering a trade.
Stop-loss and take-profit are set dynamically using ATR.
"""

from __future__ import annotations

import pandas as pd
from loguru import logger

from strategy.base import BaseStrategy


class TrendFollowingStrategy(BaseStrategy):
    """EMA crossover + ADX trend-strength filter strategy.

    Parameter Space (used by the Genetic Algorithm):
        - ``ema_fast``: Fast EMA period (int, range 5–50).
        - ``ema_slow``: Slow EMA period (int, range 20–200).
        - ``adx_threshold``: Minimum ADX value to permit entry (int, 15–40).
        - ``atr_period``: ATR period for SL/TP calculation (int, 7–21).
        - ``sl_atr_mult``: SL distance in ATR multiples (float, 1.0–3.0).
        - ``tp_atr_mult``: TP distance in ATR multiples (float, 1.5–6.0).
    """

    NAME: str = "TrendFollowingStrategy"

    # GA parameter space definition
    PARAM_SPACE: dict[str, dict] = {
        "ema_fast":      {"type": "int",   "min": 5,   "max": 50,  "default": 8},
        "ema_slow":      {"type": "int",   "min": 20,  "max": 200, "default": 21},
        "adx_threshold": {"type": "int",   "min": 15,  "max": 40,  "default": 25},
        "atr_period":    {"type": "int",   "min": 7,   "max": 21,  "default": 14},
        "sl_atr_mult":   {"type": "float", "min": 1.0, "max": 3.0, "default": 1.5},
        "tp_atr_mult":   {"type": "float", "min": 1.5, "max": 6.0, "default": 3.0},
    }

    # ------------------------------------------------------------------
    def get_default_params(self) -> dict:
        """Return default parameter values for the Trend Following strategy."""
        return {key: spec["default"] for key, spec in self.PARAM_SPACE.items()}

    # ------------------------------------------------------------------
    def validate_params(self, params: dict) -> bool:
        """Validate strategy parameters against their defined ranges.

        Args:
            params: Parameter dictionary to validate.

        Returns:
            True if all parameters are within bounds, False otherwise.
        """
        # TODO: Validate each parameter against PARAM_SPACE bounds
        # for key, spec in self.PARAM_SPACE.items():
        #     if key not in params:
        #         logger.error(f"Missing parameter: {key}")
        #         return False
        #     val = params[key]
        #     if not (spec["min"] <= val <= spec["max"]):
        #         logger.error(f"Parameter {key}={val} out of range [{spec['min']}, {spec['max']}].")
        #         return False
        # # Additional semantic check: fast EMA must be shorter than slow EMA
        # if params.get("ema_fast", 0) >= params.get("ema_slow", 1):
        #     logger.error("ema_fast must be less than ema_slow.")
        #     return False
        # return True
        logger.warning("validate_params() not yet implemented.")
        return True

    # ------------------------------------------------------------------
    def generate_signals(
        self, df: pd.DataFrame, params: dict
    ) -> pd.DataFrame:
        """Generate EMA crossover signals with ADX filter.

        Args:
            df: OHLCV DataFrame with a DatetimeIndex.
            params: Strategy parameters (see ``PARAM_SPACE``).

        Returns:
            DataFrame with boolean columns ``entries`` and ``exits``.
        """
        # TODO: Implement EMA crossover + ADX signal generation
        # import pandas_ta as ta
        #
        # fast  = params.get("ema_fast",      self.PARAM_SPACE["ema_fast"]["default"])
        # slow  = params.get("ema_slow",      self.PARAM_SPACE["ema_slow"]["default"])
        # adx_t = params.get("adx_threshold", self.PARAM_SPACE["adx_threshold"]["default"])
        #
        # ema_fast = ta.ema(df['close'], length=fast)
        # ema_slow = ta.ema(df['close'], length=slow)
        # adx      = ta.adx(df['high'], df['low'], df['close'])['ADX_14']
        #
        # bullish_cross = (ema_fast > ema_slow) & (ema_fast.shift(1) <= ema_slow.shift(1))
        # bearish_cross = (ema_fast < ema_slow) & (ema_fast.shift(1) >= ema_slow.shift(1))
        # trend_strong  = adx > adx_t
        #
        # signals = pd.DataFrame(index=df.index)
        # signals['entries'] = bullish_cross & trend_strong
        # signals['exits']   = bearish_cross
        # return signals
        logger.warning("generate_signals() not yet implemented.")
        return pd.DataFrame(
            {"entries": False, "exits": False}, index=df.index
        )
