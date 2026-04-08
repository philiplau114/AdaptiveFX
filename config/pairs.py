"""
Currency pair definitions and mappings for AdaptiveFX.

Defines the 27 traded currency pairs, supported timeframes,
correlated groups used by the risk management layer, and the
regime-to-strategy mapping used by Path A.
"""

import MetaTrader5 as mt5

# ---------------------------------------------------------------------------
# 27 Currency Pairs
# ---------------------------------------------------------------------------
CURRENCY_PAIRS: list[str] = [
    # Majors
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD",
    # EUR crosses
    "EURGBP", "EURJPY", "EURCHF", "EURAUD", "EURCAD", "EURNZD",
    # GBP crosses
    "GBPJPY", "GBPCHF", "GBPAUD", "GBPCAD", "GBPNZD",
    # AUD crosses
    "AUDJPY", "AUDCHF", "AUDCAD", "AUDNZD",
    # Other crosses
    "CADJPY", "CADCHF", "NZDJPY", "NZDCHF", "CHFJPY",
]

# ---------------------------------------------------------------------------
# Timeframes
# ---------------------------------------------------------------------------
TIMEFRAMES: dict[str, int] = {
    "M1":  mt5.TIMEFRAME_M1,
    "M5":  mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1":  mt5.TIMEFRAME_H1,
    "H4":  mt5.TIMEFRAME_H4,
    "D1":  mt5.TIMEFRAME_D1,
    "W1":  mt5.TIMEFRAME_W1,
}

# Default timeframe used for regime detection and signal generation
DEFAULT_TIMEFRAME: str = "H1"
# Timeframe used for Walk-Forward optimisation in Path B
OPTIMIZATION_TIMEFRAME: str = "H4"

# ---------------------------------------------------------------------------
# Correlated Groups (used by risk management to limit exposure)
# ---------------------------------------------------------------------------
# Pairs within the same group are highly correlated; the system avoids
# opening simultaneous positions in more than one pair per group.
CORRELATED_GROUPS: dict[str, list[str]] = {
    "USD_RISK_ON": ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD"],
    "USD_RISK_OFF": ["USDJPY", "USDCHF", "USDCAD"],
    "EUR_CROSSES": ["EURGBP", "EURJPY", "EURCHF", "EURAUD", "EURCAD", "EURNZD"],
    "GBP_CROSSES": ["GBPJPY", "GBPCHF", "GBPAUD", "GBPCAD", "GBPNZD"],
    "AUD_CROSSES": ["AUDJPY", "AUDCHF", "AUDCAD", "AUDNZD"],
    "MISC_CROSSES": ["CADJPY", "CADCHF", "NZDJPY", "NZDCHF", "CHFJPY"],
}

# ---------------------------------------------------------------------------
# Regime Labels
# ---------------------------------------------------------------------------
REGIME_TRENDING: str = "TRENDING"
REGIME_MEAN_REVERTING: str = "MEAN_REVERTING"
REGIME_BREAKOUT: str = "BREAKOUT"

ALL_REGIMES: list[str] = [REGIME_TRENDING, REGIME_MEAN_REVERTING, REGIME_BREAKOUT]

# ---------------------------------------------------------------------------
# Regime → Strategy Mapping
# ---------------------------------------------------------------------------
# Maps each detected market regime to the name of the strategy class that
# should be activated for signal generation (Path A).
REGIME_STRATEGY_MAP: dict[str, str] = {
    REGIME_TRENDING:       "TrendFollowingStrategy",
    REGIME_MEAN_REVERTING: "MeanReversionStrategy",
    REGIME_BREAKOUT:       "BreakoutStrategy",
}
