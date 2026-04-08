"""
Trading signal generation module for AdaptiveFX (Path A).

Combines the regime-mapped strategy with the optimised parameters from the
params_store to generate a structured trading signal dictionary ready for
transmission to the MT5 EA via ZeroMQ.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
from loguru import logger


class SignalGenerator:
    """Generates structured trading signals for a given symbol and regime.

    The generated signal dictionary is the contract between the Python
    analysis layer and the MT5 EA execution layer.

    Signal Schema
    -------------
    {
        "symbol":    str   — currency pair, e.g. "EURUSD"
        "direction": str   — "BUY" or "SELL"
        "entry_price": float
        "sl":        float — stop-loss price
        "tp":        float — take-profit price
        "timestamp": str   — ISO-8601 UTC timestamp
        "strategy":  str   — strategy class name
        "regime":    str   — detected market regime
    }
    """

    # ------------------------------------------------------------------
    def generate(
        self,
        symbol: str,
        regime: str,
        strategy,
        params: dict,
        df: pd.DataFrame,
    ) -> dict | None:
        """Generate a trading signal for the given symbol and regime.

        Args:
            symbol: Currency pair symbol, e.g. ``"EURUSD"``.
            regime: Detected market regime label.
            strategy: Instantiated strategy object (subclass of BaseStrategy).
            params: Optimised parameter dictionary from params_store.
            df: Most recent OHLCV DataFrame.

        Returns:
            Signal dictionary if a valid entry condition is met, otherwise
            ``None`` (no signal this candle).
        """
        # TODO: Implement signal generation pipeline
        # signals = strategy.generate_signals(df, params)
        # if signals.empty or not signals['entries'].iloc[-1]:
        #     logger.debug(f"No entry signal for {symbol} [{regime}].")
        #     return None
        #
        # atr = strategy.calculate_atr(df, params.get('atr_period', 14)).iloc[-1]
        # entry_price = df['close'].iloc[-1]
        # sl, tp = strategy.apply_sl_tp(
        #     entry_price, atr,
        #     sl_atr_mult=params.get('sl_atr_mult', 1.5),
        #     tp_atr_mult=params.get('tp_atr_mult', 3.0),
        #     direction='long',
        # )
        # signal = {
        #     "symbol":      symbol,
        #     "direction":   "BUY",
        #     "entry_price": round(entry_price, 5),
        #     "sl":          round(sl, 5),
        #     "tp":          round(tp, 5),
        #     "timestamp":   datetime.now(timezone.utc).isoformat(),
        #     "strategy":    strategy.NAME,
        #     "regime":      regime,
        # }
        # logger.info(f"Signal generated: {signal}")
        # return signal
        logger.warning(f"generate({symbol}) not yet implemented.")
        return None
