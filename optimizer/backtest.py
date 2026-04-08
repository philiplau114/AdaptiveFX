"""
Vectorbt backtesting engine for AdaptiveFX.

Replaces the Freqtrade-based backtesting engine originally used in
GeneTrader.  Vectorbt's vectorised execution is 10–30× faster than
loop-based approaches, making it ideal for the large number of evaluations
required by the Genetic Algorithm (Path B).
"""

from __future__ import annotations

import pandas as pd
from loguru import logger

from config.settings import settings


class VectorbtBacktester:
    """Runs vectorbt Portfolio backtests for strategy evaluation.

    Attributes:
        fees: Fractional commission per trade (e.g. 0.00007 ≈ 0.7 pip).
        slippage: Fractional slippage per trade.
    """

    def __init__(
        self,
        fees: float = settings.BACKTEST_FEES,
        slippage: float = settings.BACKTEST_SLIPPAGE,
    ) -> None:
        self.fees = fees
        self.slippage = slippage

    # ------------------------------------------------------------------
    def run(
        self,
        df: pd.DataFrame,
        signals: pd.DataFrame,
        params: dict,
    ) -> dict:
        """Run a single-asset vectorbt backtest.

        Args:
            df: OHLCV DataFrame with a DatetimeIndex and a ``close`` column.
            signals: DataFrame with boolean columns ``entries`` and ``exits``
                as produced by a strategy's ``generate_signals()`` method.
            params: Strategy parameters (used for SL/TP configuration).

        Returns:
            Dictionary of backtest metrics:
            ``sharpe_ratio``, ``max_drawdown``, ``win_rate``,
            ``profit_factor``, ``total_trades``.
        """
        # TODO: Implement vectorbt Portfolio.from_signals() backtest
        # import vectorbt as vbt
        # pf = vbt.Portfolio.from_signals(
        #     df['close'],
        #     entries=signals['entries'],
        #     exits=signals['exits'],
        #     fees=self.fees,
        #     slippage=self.slippage,
        #     sl_stop=params.get('sl_atr_mult', 1.5) / 1000,  # approximate
        #     tp_stop=params.get('tp_atr_mult', 3.0) / 1000,
        # )
        # return {
        #     'sharpe_ratio':  pf.sharpe_ratio(),
        #     'max_drawdown':  abs(pf.max_drawdown()),
        #     'win_rate':      pf.trades.win_rate() if pf.trades.count() > 0 else 0.0,
        #     'profit_factor': pf.trades.profit_factor() if pf.trades.count() > 0 else 0.0,
        #     'total_trades':  int(pf.trades.count()),
        # }
        logger.warning("run() not yet implemented.")
        return {
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "total_trades": 0,
        }

    # ------------------------------------------------------------------
    def run_multi_pair(
        self,
        dfs: dict[str, pd.DataFrame],
        strategy,
        genes: list,
    ) -> dict:
        """Run a backtest across multiple currency pairs and aggregate results.

        This method is called by the GA fitness evaluator to assess how a
        particular gene set (parameter combination) performs across all pairs
        in the optimisation batch.

        Args:
            dfs: Dictionary mapping symbol → OHLCV DataFrame.
            strategy: Instantiated strategy object (subclass of BaseStrategy).
            genes: Gene list from an :class:`Individual` instance.

        Returns:
            Aggregated backtest metrics dictionary (mean across all pairs).
        """
        # TODO: Implement multi-pair backtest aggregation
        # params = strategy.param_space  # decode genes first
        # individual = Individual(strategy.PARAM_SPACE, genes)
        # params = individual.decode()
        #
        # all_results = []
        # for symbol, df in dfs.items():
        #     signals = strategy.generate_signals(df, params)
        #     result  = self.run(df, signals, params)
        #     all_results.append(result)
        #
        # import numpy as np
        # return {
        #     'sharpe_ratio':  np.mean([r['sharpe_ratio']  for r in all_results]),
        #     'max_drawdown':  np.mean([r['max_drawdown']   for r in all_results]),
        #     'win_rate':      np.mean([r['win_rate']       for r in all_results]),
        #     'profit_factor': np.mean([r['profit_factor']  for r in all_results]),
        #     'total_trades':  int(np.sum([r['total_trades'] for r in all_results])),
        # }
        logger.warning("run_multi_pair() not yet implemented.")
        return {
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "total_trades": 0,
        }
