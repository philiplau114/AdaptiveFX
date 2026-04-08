"""
Unit tests for the strategy module
(strategy/base.py, strategy/trend_following.py,
 strategy/mean_reversion.py, strategy/breakout.py).

All tests are currently placeholders.  Replace the ``pass`` / ``TODO``
sections with actual assertions once the corresponding implementation is
complete.
"""

import pytest
import pandas as pd


def _make_ohlcv(n: int = 100) -> pd.DataFrame:
    """Create a minimal synthetic OHLCV DataFrame for testing."""
    import numpy as np
    close = 1.1000 + np.cumsum(np.random.randn(n) * 0.0005)
    return pd.DataFrame(
        {
            "open":  close - 0.0002,
            "high":  close + 0.0005,
            "low":   close - 0.0005,
            "close": close,
            "tick_volume": np.random.randint(500, 2000, n),
        }
    )


# ---------------------------------------------------------------------------
# TrendFollowingStrategy
# ---------------------------------------------------------------------------

class TestTrendFollowingStrategy:
    """Tests for strategy.trend_following.TrendFollowingStrategy."""

    def test_default_params_are_complete(self):
        """get_default_params() should return all required keys."""
        # TODO: Assert all PARAM_SPACE keys are present with correct types
        from strategy.trend_following import TrendFollowingStrategy
        strategy = TrendFollowingStrategy()
        params = strategy.get_default_params()
        for key in strategy.PARAM_SPACE:
            assert key in params

    def test_validate_params_accepts_defaults(self):
        """validate_params() should accept the default parameter set."""
        # TODO: Assert True for defaults once implementation is complete
        from strategy.trend_following import TrendFollowingStrategy
        strategy = TrendFollowingStrategy()
        assert strategy.validate_params(strategy.get_default_params())

    def test_generate_signals_returns_correct_columns(self):
        """generate_signals() should return a DataFrame with 'entries'/'exits'."""
        # TODO: Assert signal DataFrame is non-empty with correct columns
        from strategy.trend_following import TrendFollowingStrategy
        strategy = TrendFollowingStrategy()
        df = _make_ohlcv(200)
        signals = strategy.generate_signals(df, strategy.get_default_params())
        assert isinstance(signals, pd.DataFrame)
        assert "entries" in signals.columns
        assert "exits" in signals.columns


# ---------------------------------------------------------------------------
# MeanReversionStrategy
# ---------------------------------------------------------------------------

class TestMeanReversionStrategy:
    """Tests for strategy.mean_reversion.MeanReversionStrategy."""

    def test_default_params_are_complete(self):
        """get_default_params() should return all required keys."""
        # TODO: Assert all PARAM_SPACE keys are present
        from strategy.mean_reversion import MeanReversionStrategy
        strategy = MeanReversionStrategy()
        params = strategy.get_default_params()
        for key in strategy.PARAM_SPACE:
            assert key in params

    def test_validate_params_accepts_defaults(self):
        """validate_params() should accept the default parameter set."""
        # TODO: Assert True for defaults
        from strategy.mean_reversion import MeanReversionStrategy
        strategy = MeanReversionStrategy()
        assert strategy.validate_params(strategy.get_default_params())

    def test_generate_signals_returns_correct_columns(self):
        """generate_signals() should return a DataFrame with 'entries'/'exits'."""
        # TODO: Assert signal DataFrame structure
        from strategy.mean_reversion import MeanReversionStrategy
        strategy = MeanReversionStrategy()
        df = _make_ohlcv(200)
        signals = strategy.generate_signals(df, strategy.get_default_params())
        assert isinstance(signals, pd.DataFrame)
        assert "entries" in signals.columns
        assert "exits" in signals.columns


# ---------------------------------------------------------------------------
# BreakoutStrategy
# ---------------------------------------------------------------------------

class TestBreakoutStrategy:
    """Tests for strategy.breakout.BreakoutStrategy."""

    def test_default_params_are_complete(self):
        """get_default_params() should return all required keys."""
        # TODO: Assert all PARAM_SPACE keys are present
        from strategy.breakout import BreakoutStrategy
        strategy = BreakoutStrategy()
        params = strategy.get_default_params()
        for key in strategy.PARAM_SPACE:
            assert key in params

    def test_validate_params_accepts_defaults(self):
        """validate_params() should accept the default parameter set."""
        # TODO: Assert True for defaults
        from strategy.breakout import BreakoutStrategy
        strategy = BreakoutStrategy()
        assert strategy.validate_params(strategy.get_default_params())

    def test_generate_signals_returns_correct_columns(self):
        """generate_signals() should return a DataFrame with 'entries'/'exits'."""
        # TODO: Assert signal DataFrame structure
        from strategy.breakout import BreakoutStrategy
        strategy = BreakoutStrategy()
        df = _make_ohlcv(200)
        signals = strategy.generate_signals(df, strategy.get_default_params())
        assert isinstance(signals, pd.DataFrame)
        assert "entries" in signals.columns
        assert "exits" in signals.columns
