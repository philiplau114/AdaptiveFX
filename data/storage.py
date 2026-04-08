"""
Parquet-based data storage module for AdaptiveFX.

Provides read/write helpers that persist OHLCV DataFrames as Parquet files
under ``settings.DATA_PATH / <symbol> / <timeframe>.parquet``.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from loguru import logger

from config.settings import settings


class DataStorage:
    """Manages reading and writing of OHLCV data in Parquet format.

    Attributes:
        base_path: Root directory under which all Parquet files are stored.
    """

    def __init__(self, base_path: Path = settings.DATA_PATH) -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    def _parquet_path(self, symbol: str, timeframe: str) -> Path:
        """Return the full path to a symbol/timeframe Parquet file."""
        return self.base_path / symbol / f"{timeframe}.parquet"

    # ------------------------------------------------------------------
    def save(self, df: pd.DataFrame, symbol: str, timeframe: str) -> None:
        """Persist a DataFrame to Parquet storage.

        Args:
            df: OHLCV DataFrame with a DatetimeIndex.
            symbol: Currency pair symbol, e.g. ``"EURUSD"``.
            timeframe: Timeframe string, e.g. ``"H1"``.
        """
        # TODO: Implement Parquet write
        # path = self._parquet_path(symbol, timeframe)
        # path.parent.mkdir(parents=True, exist_ok=True)
        # df.to_parquet(path, engine="pyarrow", compression="snappy")
        # logger.debug(f"Saved {len(df)} rows → {path}")
        logger.warning(f"save({symbol}, {timeframe}) not yet implemented.")

    # ------------------------------------------------------------------
    def load(
        self,
        symbol: str,
        timeframe: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> pd.DataFrame:
        """Load OHLCV data from Parquet storage with optional date filtering.

        Args:
            symbol: Currency pair symbol.
            timeframe: Timeframe string.
            start_date: Optional inclusive start date for filtering.
            end_date: Optional inclusive end date for filtering.

        Returns:
            Filtered DataFrame, or an empty DataFrame if the file does not exist.
        """
        # TODO: Implement Parquet read with date filtering
        # path = self._parquet_path(symbol, timeframe)
        # if not path.exists():
        #     logger.warning(f"No data file found: {path}")
        #     return pd.DataFrame()
        # df = pd.read_parquet(path, engine="pyarrow")
        # if start_date:
        #     df = df[df.index >= pd.Timestamp(start_date)]
        # if end_date:
        #     df = df[df.index <= pd.Timestamp(end_date)]
        # logger.debug(f"Loaded {len(df)} rows from {path}")
        # return df
        logger.warning(f"load({symbol}, {timeframe}) not yet implemented.")
        return pd.DataFrame()

    # ------------------------------------------------------------------
    def update(self, symbol: str, timeframe: str) -> None:
        """Append the latest bars to an existing Parquet file.

        Reads the most recent timestamp from the stored file, fetches only
        new bars from MT5, and appends them to avoid full re-downloads.

        Args:
            symbol: Currency pair symbol.
            timeframe: Timeframe string.
        """
        # TODO: Implement incremental update
        # existing = self.load(symbol, timeframe)
        # if existing.empty:
        #     logger.info(f"No existing data for {symbol} [{timeframe}]; full download.")
        #     # trigger full collection via MT5DataCollector
        # else:
        #     last_ts = existing.index[-1]
        #     # fetch bars from last_ts to now via MT5DataCollector
        #     # deduplicate and append
        #     pass
        logger.warning(f"update({symbol}, {timeframe}) not yet implemented.")
