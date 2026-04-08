"""
AdaptiveFX — Main Entry Point

Supports three operating modes:

    collect   — Connect to MT5 and download/update OHLCV data for all 27 pairs.
    optimize  — Run the Path B GA optimisation pipeline (blocking until complete).
    live      — Start the Path A real-time trading loop.

Usage
-----
    python main.py --mode collect
    python main.py --mode optimize
    python main.py --mode live
    python main.py --mode live --pairs EURUSD GBPUSD   # Optional pair filter
"""

from __future__ import annotations

import argparse
import sys

from loguru import logger

from config.settings import settings
from config.pairs import CURRENCY_PAIRS, DEFAULT_TIMEFRAME


# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

logger.remove()
logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> — <level>{message}</level>"
    ),
)
logger.add(
    settings.LOG_PATH / "adaptivefx_{time}.log",
    level=settings.LOG_LEVEL,
    rotation=settings.LOG_ROTATION,
    retention=settings.LOG_RETENTION,
)


# ---------------------------------------------------------------------------
# Mode implementations
# ---------------------------------------------------------------------------

def run_collect(pairs: list[str]) -> None:
    """Collect and store OHLCV data for the specified currency pairs.

    Args:
        pairs: List of currency pair symbols to collect.
    """
    # TODO: Implement data collection mode
    # from data.collector import MT5DataCollector
    # from data.storage import DataStorage
    # from data.validator import DataValidator
    #
    # logger.info(f"Starting data collection for {len(pairs)} pairs.")
    # collector = MT5DataCollector()
    # storage   = DataStorage()
    # validator = DataValidator()
    #
    # if not collector.connect():
    #     logger.error("Cannot connect to MT5. Is the terminal running?")
    #     sys.exit(1)
    #
    # for symbol in pairs:
    #     logger.info(f"Collecting {symbol}...")
    #     for tf in [DEFAULT_TIMEFRAME, "H4", "D1"]:
    #         df = collector.collect_ohlcv(symbol, tf, n_bars=5000)
    #         if not df.empty and validator.validate(df, symbol):
    #             storage.save(df, symbol, tf)
    #         else:
    #             logger.warning(f"Skipped {symbol} [{tf}] — validation failed.")
    #
    # collector.disconnect()
    # logger.info("Data collection complete.")
    logger.warning("collect mode not yet implemented.")


def run_optimize() -> None:
    """Run the weekly optimisation pipeline (Path B, blocking)."""
    # TODO: Implement optimisation mode
    # from optimizer.scheduler import OptimizationScheduler
    #
    # logger.info("Starting strategy optimisation (Path B).")
    # scheduler = OptimizationScheduler()
    # scheduler.optimize_all_pairs()
    # logger.info("Optimisation complete. params_store updated.")
    logger.warning("optimize mode not yet implemented.")


def run_live(pairs: list[str]) -> None:
    """Start the real-time trading loop (Path A).

    For each new bar close on each pair:
    1. Detect market regime.
    2. Map regime to strategy + optimised parameters.
    3. Generate trading signal.
    4. Transmit signal to MT5 EA via ZeroMQ.

    Args:
        pairs: List of currency pair symbols to trade.
    """
    # TODO: Implement live trading loop
    # from data.collector import MT5DataCollector
    # from regime.detector import RegimeDetector
    # from regime.mapper import RegimeMapper
    # from signal.generator import SignalGenerator
    # from signal.transmitter import SignalTransmitter
    # from monitoring.monitor import SystemMonitor
    # import time
    # from collections import defaultdict, deque
    #
    # logger.info(f"Starting live trading loop for {len(pairs)} pairs.")
    #
    # collector    = MT5DataCollector()
    # detector     = RegimeDetector()
    # mapper       = RegimeMapper()
    # generator    = SignalGenerator()
    # transmitter  = SignalTransmitter()
    # monitor      = SystemMonitor()
    #
    # if not collector.connect():
    #     logger.error("Cannot connect to MT5.")
    #     sys.exit(1)
    #
    # transmitter.connect()
    #
    # regime_history = defaultdict(lambda: deque(maxlen=10))
    #
    # try:
    #     while True:
    #         monitor.check_mt5_connection()
    #         monitor.check_optimization_schedule()
    #
    #         for symbol in pairs:
    #             df = collector.collect_ohlcv(symbol, DEFAULT_TIMEFRAME, n_bars=500)
    #             if df.empty:
    #                 continue
    #
    #             raw_regime = detector.predict(df)
    #             regime_history[symbol].append(raw_regime)
    #             confirmed = detector.confirm_regime(
    #                 regime_history[symbol],
    #                 n=settings.REGIME_CONFIRMATION_CANDLES
    #             )
    #             if confirmed is None:
    #                 continue
    #
    #             strategy_name = mapper.map(confirmed, symbol)
    #             params        = mapper.get_params(strategy_name, symbol)
    #
    #             # Dynamically instantiate strategy
    #             import importlib
    #             mod = importlib.import_module("strategy." + strategy_name[:-8].lower())
    #             strategy = getattr(mod, strategy_name)()
    #
    #             signal = generator.generate(symbol, confirmed, strategy, params, df)
    #             if signal:
    #                 transmitter.send(signal)
    #
    #         time.sleep(60)  # poll every minute; refine to align with bar close
    #
    # except KeyboardInterrupt:
    #     logger.info("Live loop interrupted by user.")
    # finally:
    #     transmitter.disconnect()
    #     collector.disconnect()
    logger.warning("live mode not yet implemented.")


# ---------------------------------------------------------------------------
# CLI argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="adaptivefx",
        description="AdaptiveFX — Automated Forex Quantitative Trading System",
    )
    parser.add_argument(
        "--mode",
        choices=["live", "optimize", "collect"],
        required=True,
        help=(
            "Operating mode: "
            "'collect' downloads MT5 data, "
            "'optimize' runs the GA optimisation pipeline, "
            "'live' starts real-time trading."
        ),
    )
    parser.add_argument(
        "--pairs",
        nargs="+",
        default=CURRENCY_PAIRS,
        metavar="SYMBOL",
        help="Currency pairs to process (default: all 27 configured pairs).",
    )
    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Parse CLI arguments and dispatch to the appropriate mode."""
    parser = build_parser()
    args = parser.parse_args()

    settings.LOG_PATH.mkdir(parents=True, exist_ok=True)

    logger.info(f"AdaptiveFX starting — mode={args.mode}, pairs={args.pairs}")

    if args.mode == "collect":
        run_collect(args.pairs)
    elif args.mode == "optimize":
        run_optimize()
    elif args.mode == "live":
        run_live(args.pairs)


if __name__ == "__main__":
    main()
