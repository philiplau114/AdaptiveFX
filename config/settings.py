"""
Global settings for AdaptiveFX.

All configurable parameters are centralised here.  Environment variables
are preferred for secrets (MT5 credentials).  Other settings have sensible
defaults that can be overridden via environment variables or direct
assignment.
"""

import os
from pathlib import Path


class Settings:
    """Central configuration class for AdaptiveFX."""

    # ------------------------------------------------------------------
    # MT5 Connection Settings
    # ------------------------------------------------------------------
    MT5_LOGIN: int = int(os.getenv("MT5_LOGIN", "0"))
    MT5_PASSWORD: str = os.getenv("MT5_PASSWORD", "")
    MT5_SERVER: str = os.getenv("MT5_SERVER", "")
    MT5_TIMEOUT: int = int(os.getenv("MT5_TIMEOUT", "60000"))  # milliseconds

    # ------------------------------------------------------------------
    # Data Storage Paths
    # ------------------------------------------------------------------
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_PATH: Path = Path(os.getenv("DATA_PATH", str(BASE_DIR / "data" / "storage")))
    PARAMS_STORE_PATH: Path = BASE_DIR / "store" / "params" / "params_store.json"
    LOG_PATH: Path = Path(os.getenv("LOG_PATH", str(BASE_DIR / "logs")))

    # ------------------------------------------------------------------
    # Optimisation Schedule Settings
    # ------------------------------------------------------------------
    # Day of week and time (UTC) for the weekly optimisation job
    OPTIMIZATION_DAY: str = os.getenv("OPTIMIZATION_DAY", "sunday")
    OPTIMIZATION_TIME: str = os.getenv("OPTIMIZATION_TIME", "02:00")  # HH:MM UTC

    # ------------------------------------------------------------------
    # Regime Detection Settings
    # ------------------------------------------------------------------
    # Number of consecutive candles required to confirm a regime change
    REGIME_CONFIRMATION_CANDLES: int = int(
        os.getenv("REGIME_CONFIRMATION_CANDLES", "3")
    )
    # Number of HMM hidden states (mapped to TRENDING / MEAN_REVERTING / BREAKOUT)
    HMM_N_COMPONENTS: int = int(os.getenv("HMM_N_COMPONENTS", "3"))
    HMM_N_ITER: int = int(os.getenv("HMM_N_ITER", "100"))
    # Minimum bars required before training or predicting
    MIN_BARS_TRAIN: int = int(os.getenv("MIN_BARS_TRAIN", "500"))

    # ------------------------------------------------------------------
    # Logging Settings
    # ------------------------------------------------------------------
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_ROTATION: str = os.getenv("LOG_ROTATION", "1 week")
    LOG_RETENTION: str = os.getenv("LOG_RETENTION", "4 weeks")

    # ------------------------------------------------------------------
    # ZeroMQ Port Settings
    # ------------------------------------------------------------------
    ZMQ_PUB_PORT: int = int(os.getenv("ZMQ_PUB_PORT", "5555"))  # Python publishes
    ZMQ_SUB_PORT: int = int(os.getenv("ZMQ_SUB_PORT", "5556"))  # MT5 EA subscribes
    ZMQ_TOPIC: str = os.getenv("ZMQ_TOPIC", "SIGNAL")

    # ------------------------------------------------------------------
    # Backtesting / GA Settings
    # ------------------------------------------------------------------
    GA_POPULATION_SIZE: int = int(os.getenv("GA_POPULATION_SIZE", "50"))
    GA_N_GENERATIONS: int = int(os.getenv("GA_N_GENERATIONS", "20"))
    GA_CROSSOVER_PROB: float = float(os.getenv("GA_CROSSOVER_PROB", "0.7"))
    GA_MUTATION_PROB: float = float(os.getenv("GA_MUTATION_PROB", "0.3"))
    GA_TOURNAMENT_SIZE: int = int(os.getenv("GA_TOURNAMENT_SIZE", "3"))

    # Backtest fees and slippage (fractional, e.g. 0.00007 = 0.7 pip on a 5-digit broker)
    BACKTEST_FEES: float = float(os.getenv("BACKTEST_FEES", "0.00007"))
    BACKTEST_SLIPPAGE: float = float(os.getenv("BACKTEST_SLIPPAGE", "0.00002"))

    # ------------------------------------------------------------------
    # Risk Management Settings
    # ------------------------------------------------------------------
    MAX_CONCURRENT_POSITIONS: int = int(os.getenv("MAX_CONCURRENT_POSITIONS", "5"))
    RISK_PER_TRADE_PCT: float = float(os.getenv("RISK_PER_TRADE_PCT", "0.02"))  # 2%
    MAX_DRAWDOWN_PCT: float = float(os.getenv("MAX_DRAWDOWN_PCT", "0.30"))  # 30%
    SPREAD_FILTER_PIPS: float = float(os.getenv("SPREAD_FILTER_PIPS", "3.0"))


# Singleton instance
settings = Settings()
