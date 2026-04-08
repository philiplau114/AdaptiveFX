"""
Regime-to-strategy mapping module for AdaptiveFX.

Translates a detected market regime label into the corresponding strategy
class name and retrieves the associated optimised parameters from the
params_store, providing Path A with a ready-to-execute configuration.
"""

from __future__ import annotations

from loguru import logger

from config.pairs import REGIME_STRATEGY_MAP


class RegimeMapper:
    """Maps detected market regimes to trading strategies and parameters.

    Attributes:
        params_store: A :class:`store.params_store.ParamsStore` instance
            used to retrieve optimised parameters.
    """

    def __init__(self) -> None:
        # Lazy import to avoid circular dependencies
        from store.params_store import ParamsStore

        self.params_store = ParamsStore()
        self.params_store.load()

    # ------------------------------------------------------------------
    def map(self, regime: str, symbol: str) -> str:
        """Return the strategy class name associated with a regime.

        Args:
            regime: Detected regime label (``TRENDING``, ``MEAN_REVERTING``,
                or ``BREAKOUT``).
            symbol: Currency pair symbol (used for logging).

        Returns:
            Strategy class name string, e.g. ``"TrendFollowingStrategy"``.

        Raises:
            KeyError: If ``regime`` is not found in ``REGIME_STRATEGY_MAP``.
        """
        # TODO: Validate regime and return mapped strategy name
        # strategy_name = REGIME_STRATEGY_MAP.get(regime)
        # if strategy_name is None:
        #     raise KeyError(f"Unknown regime '{regime}' for {symbol}.")
        # logger.debug(f"{symbol}: regime={regime} → strategy={strategy_name}")
        # return strategy_name
        logger.warning(f"map({regime}, {symbol}) not yet implemented.")
        return REGIME_STRATEGY_MAP.get(regime, "TrendFollowingStrategy")

    # ------------------------------------------------------------------
    def get_params(self, strategy_name: str, symbol: str) -> dict:
        """Retrieve optimal parameters for a strategy+symbol combination.

        Parameters are loaded from the params_store JSON that is updated
        weekly by Path B.

        Args:
            strategy_name: Strategy class name, e.g. ``"TrendFollowingStrategy"``.
            symbol: Currency pair symbol.

        Returns:
            Dictionary of optimised parameters.  Returns an empty dict if no
            stored parameters are found.
        """
        # TODO: Look up params_store for strategy_name + symbol
        # regime = {v: k for k, v in REGIME_STRATEGY_MAP.items()}.get(strategy_name)
        # if regime is None:
        #     logger.error(f"No regime mapping for strategy '{strategy_name}'.")
        #     return {}
        # params = self.params_store.get_params(symbol, regime)
        # logger.debug(f"Params for {symbol}/{strategy_name}: {params}")
        # return params
        logger.warning(
            f"get_params({strategy_name}, {symbol}) not yet implemented."
        )
        return {}
