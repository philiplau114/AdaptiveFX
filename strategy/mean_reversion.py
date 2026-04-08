"""
Mean Reversion strategy for AdaptiveFX.

Activated when the regime detector classifies the market as
``MEAN_REVERTING``.  Uses Bollinger Bands to identify price extremes and
an RSI filter to confirm oversold/overbought conditions before entry.
Stop-loss and take-profit are set dynamically using ATR.
"""

from __future__ import annotations

import pandas as pd
from loguru import logger

from strategy.base import BaseStrategy


class MeanReversionStrategy(BaseStrategy):
    """Bollinger Bands + RSI mean-reversion strategy.

    Parameter Space (used by the Genetic Algorithm):
        - ``bb_period``: Bollinger Bands lookback period (int, 10–50).
        - ``bb_std``: Number of standard deviations for the bands (float, 1.5–3.0).
        - ``rsi_period``: RSI calculation period (int, 7–21).
        - ``rsi_low``: RSI oversold threshold (int, 20–40).
        - ``rsi_high``: RSI overbought threshold (int, 60–80).
        - ``atr_period``: ATR period for SL/TP calculation (int, 7–21).
        - ``sl_atr_mult``: SL distance in ATR multiples (float, 1.0–3.0).
        - ``tp_atr_mult``: TP distance in ATR multiples (float, 1.0–4.0).
    """

    NAME: str = "MeanReversionStrategy"

    PARAM_SPACE: dict[str, dict] = {
        "bb_period":   {"type": "int",   "min": 10,  "max": 50,  "default": 20},
        "bb_std":      {"type": "float", "min": 1.5, "max": 3.0, "default": 2.0},
        "rsi_period":  {"type": "int",   "min": 7,   "max": 21,  "default": 14},
        "rsi_low":     {"type": "int",   "min": 20,  "max": 40,  "default": 30},
        "rsi_high":    {"type": "int",   "min": 60,  "max": 80,  "default": 70},
        "atr_period":  {"type": "int",   "min": 7,   "max": 21,  "default": 14},
        "sl_atr_mult": {"type": "float", "min": 1.0, "max": 3.0, "default": 1.5},
        "tp_atr_mult": {"type": "float", "min": 1.0, "max": 4.0, "default": 2.0},
    }

    # ------------------------------------------------------------------
    def get_default_params(self) -> dict:
        """Return default parameter values for the Mean Reversion strategy."""
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
        #         logger.error(f"Parameter {key}={val} out of range.")
        #         return False
        # # rsi_low must be < rsi_high
        # if params.get("rsi_low", 0) >= params.get("rsi_high", 100):
        #     logger.error("rsi_low must be less than rsi_high.")
        #     return False
        # return True
        logger.warning("validate_params() not yet implemented.")
        return True

    # ------------------------------------------------------------------
    def generate_signals(
        self, df: pd.DataFrame, params: dict
    ) -> pd.DataFrame:
        """Generate mean-reversion signals using Bollinger Bands and RSI.

        A long entry is triggered when price closes below the lower
        Bollinger Band and RSI is below ``rsi_low``.  An exit is triggered
        when price returns to the middle band or RSI exceeds ``rsi_high``.

        Args:
            df: OHLCV DataFrame with a DatetimeIndex.
            params: Strategy parameters (see ``PARAM_SPACE``).

        Returns:
            DataFrame with boolean columns ``entries`` and ``exits``.
        """
        # TODO: Implement Bollinger Bands + RSI signal generation
        # import pandas_ta as ta
        #
        # period  = params.get("bb_period",  self.PARAM_SPACE["bb_period"]["default"])
        # std     = params.get("bb_std",     self.PARAM_SPACE["bb_std"]["default"])
        # rsi_p   = params.get("rsi_period", self.PARAM_SPACE["rsi_period"]["default"])
        # rsi_lo  = params.get("rsi_low",    self.PARAM_SPACE["rsi_low"]["default"])
        # rsi_hi  = params.get("rsi_high",   self.PARAM_SPACE["rsi_high"]["default"])
        #
        # bb   = ta.bbands(df['close'], length=period, std=std)
        # rsi  = ta.rsi(df['close'], length=rsi_p)
        #
        # lower_band  = bb[f'BBL_{period}_{std}']
        # middle_band = bb[f'BBM_{period}_{std}']
        #
        # signals = pd.DataFrame(index=df.index)
        # signals['entries'] = (df['close'] < lower_band) & (rsi < rsi_lo)
        # signals['exits']   = (df['close'] > middle_band) | (rsi > rsi_hi)
        # return signals
        logger.warning("generate_signals() not yet implemented.")
        return pd.DataFrame(
            {"entries": False, "exits": False}, index=df.index
        )
