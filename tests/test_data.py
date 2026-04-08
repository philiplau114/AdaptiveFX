"""
Unit tests for the data module (data/collector.py, data/storage.py, data/validator.py).

All tests are currently placeholders.  Replace the ``pass`` / ``TODO``
sections with actual assertions once the corresponding implementation is
complete.
"""

import pytest
import pandas as pd


# ---------------------------------------------------------------------------
# MT5DataCollector
# ---------------------------------------------------------------------------

class TestMT5DataCollector:
    """Tests for data.collector.MT5DataCollector."""

    def test_connect_returns_bool(self):
        """connect() should return a boolean."""
        # TODO: Mock MetaTrader5.initialize and verify return value
        from data.collector import MT5DataCollector
        collector = MT5DataCollector(login=0, password="", server="")
        result = collector.connect()
        assert isinstance(result, bool)

    def test_collect_ohlcv_returns_dataframe(self):
        """collect_ohlcv() should return a DataFrame (empty when not implemented)."""
        # TODO: Mock mt5.copy_rates_from_pos and verify column names
        from data.collector import MT5DataCollector
        collector = MT5DataCollector()
        df = collector.collect_ohlcv("EURUSD", "H1", 100)
        assert isinstance(df, pd.DataFrame)

    def test_collect_all_pairs_returns_dict(self):
        """collect_all_pairs() should return a dict."""
        # TODO: Mock individual collect_ohlcv calls
        from data.collector import MT5DataCollector
        collector = MT5DataCollector()
        result = collector.collect_all_pairs("H1", 100)
        assert isinstance(result, dict)

    def test_disconnect_does_not_raise(self):
        """disconnect() should not raise an exception."""
        # TODO: Verify mt5.shutdown() is called
        from data.collector import MT5DataCollector
        collector = MT5DataCollector()
        collector.disconnect()  # should not raise


# ---------------------------------------------------------------------------
# DataStorage
# ---------------------------------------------------------------------------

class TestDataStorage:
    """Tests for data.storage.DataStorage."""

    def test_save_does_not_raise(self, tmp_path):
        """save() should not raise for a valid DataFrame."""
        # TODO: Verify that a Parquet file is written to the expected path
        from data.storage import DataStorage
        storage = DataStorage(base_path=tmp_path)
        df = pd.DataFrame({"close": [1.1, 1.2]})
        storage.save(df, "EURUSD", "H1")

    def test_load_returns_dataframe(self, tmp_path):
        """load() should return a DataFrame (empty when file is absent)."""
        # TODO: Write a fixture Parquet file and assert non-empty load
        from data.storage import DataStorage
        storage = DataStorage(base_path=tmp_path)
        df = storage.load("EURUSD", "H1")
        assert isinstance(df, pd.DataFrame)

    def test_update_does_not_raise(self, tmp_path):
        """update() should not raise."""
        # TODO: Verify incremental append behaviour
        from data.storage import DataStorage
        storage = DataStorage(base_path=tmp_path)
        storage.update("EURUSD", "H1")


# ---------------------------------------------------------------------------
# DataValidator
# ---------------------------------------------------------------------------

class TestDataValidator:
    """Tests for data.validator.DataValidator."""

    def test_check_missing_empty_df(self):
        """check_missing() should handle an empty DataFrame gracefully."""
        # TODO: Assert missing_count == 0 for an empty DataFrame
        from data.validator import DataValidator
        validator = DataValidator()
        result = validator.check_missing(pd.DataFrame())
        assert isinstance(result, dict)
        assert "has_missing" in result

    def test_check_outliers_no_outliers(self):
        """check_outliers() should return no outliers for clean data."""
        # TODO: Create a synthetic clean DataFrame and assert has_outliers=False
        from data.validator import DataValidator
        validator = DataValidator()
        df = pd.DataFrame({"close": [1.1000 + i * 0.0001 for i in range(50)]})
        result = validator.check_outliers(df)
        assert isinstance(result, dict)
        assert "has_outliers" in result

    def test_validate_returns_bool(self):
        """validate() should return a boolean."""
        # TODO: Assert True for valid data, False for invalid
        from data.validator import DataValidator
        validator = DataValidator()
        df = pd.DataFrame({"close": [1.1, 1.2, 1.3]})
        result = validator.validate(df, "EURUSD")
        assert isinstance(result, bool)
