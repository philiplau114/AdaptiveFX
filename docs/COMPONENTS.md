# Component Specifications — AdaptiveFX

## Overview

This document provides a detailed specification for every module in the AdaptiveFX system, including inputs, outputs, and inter-module dependencies.

---

## 1. `config/settings.py` — `Settings`

| Attribute | Description | Default |
|-----------|-------------|---------|
| `MT5_LOGIN` | MT5 account number | env var `MT5_LOGIN` |
| `MT5_PASSWORD` | MT5 account password | env var `MT5_PASSWORD` |
| `MT5_SERVER` | MT5 broker server | env var `MT5_SERVER` |
| `DATA_PATH` | Root path for Parquet storage | `./data/storage` |
| `PARAMS_STORE_PATH` | Path to params_store JSON | `./store/params/params_store.json` |
| `REGIME_CONFIRMATION_CANDLES` | Candles required to confirm a regime | `3` |
| `HMM_N_COMPONENTS` | HMM hidden states | `3` |
| `GA_POPULATION_SIZE` | GA individuals per generation | `50` |
| `GA_N_GENERATIONS` | GA generations per optimisation | `20` |
| `ZMQ_PUB_PORT` | ZeroMQ publisher port | `5555` |

---

## 2. `config/pairs.py`

| Constant | Type | Description |
|----------|------|-------------|
| `CURRENCY_PAIRS` | `list[str]` | 27 traded currency pairs |
| `TIMEFRAMES` | `dict[str, int]` | Timeframe name → MT5 constant mapping |
| `DEFAULT_TIMEFRAME` | `str` | Used by Path A (signal generation) |
| `OPTIMIZATION_TIMEFRAME` | `str` | Used by Path B (GA backtest) |
| `CORRELATED_GROUPS` | `dict[str, list[str]]` | Groups of correlated pairs |
| `REGIME_STRATEGY_MAP` | `dict[str, str]` | Regime label → strategy class name |

---

## 3. `data/collector.py` — `MT5DataCollector`

| Method | Input | Output | Dependency |
|--------|-------|--------|-----------|
| `connect()` | — | `bool` | MetaTrader5 |
| `collect_ohlcv(symbol, timeframe, n_bars)` | str, str, int | `pd.DataFrame` | MetaTrader5 |
| `collect_all_pairs(timeframe, n_bars)` | str, int | `dict[str, DataFrame]` | `collect_ohlcv` |
| `disconnect()` | — | None | MetaTrader5 |

**Output DataFrame columns:** `[open, high, low, close, tick_volume]` with `DatetimeIndex`.

---

## 4. `data/storage.py` — `DataStorage`

| Method | Input | Output | Dependency |
|--------|-------|--------|-----------|
| `save(df, symbol, timeframe)` | DataFrame, str, str | None | pyarrow |
| `load(symbol, timeframe, start_date, end_date)` | str, str, datetime?, datetime? | `pd.DataFrame` | pyarrow |
| `update(symbol, timeframe)` | str, str | None | `MT5DataCollector`, pyarrow |

**Storage path:** `{DATA_PATH}/{symbol}/{timeframe}.parquet`

---

## 5. `data/validator.py` — `DataValidator`

| Method | Input | Output | Dependency |
|--------|-------|--------|-----------|
| `check_missing(df)` | DataFrame | `dict` | pandas |
| `check_outliers(df)` | DataFrame | `dict` | numpy |
| `validate(df, symbol)` | DataFrame, str | `bool` | `check_missing`, `check_outliers` |

**Result dict keys:** `missing_count`, `missing_pct`, `has_missing` / `outlier_count`, `outlier_indices`, `has_outliers`.

---

## 6. `regime/trainer.py` — `RegimeTrainer`

| Method | Input | Output | Dependency |
|--------|-------|--------|-----------|
| `prepare_features(df)` | DataFrame | `pd.DataFrame` | pandas-ta, numpy |
| `train_hmm(features)` | DataFrame | `GaussianHMM` | hmmlearn |
| `train_svm(features, labels)` | DataFrame, ndarray | `Pipeline` | scikit-learn |
| `save_model(symbol)` | str | None | joblib |
| `load_model(symbol)` | str | `(HMM, SVC)` | joblib |

**Features extracted:** log returns, rolling volatility (20-bar), ATR (14), volume delta, RSI, Bollinger Band width.

---

## 7. `regime/detector.py` — `RegimeDetector`

| Method | Input | Output | Dependency |
|--------|-------|--------|-----------|
| `train(df)` | DataFrame | None | `RegimeTrainer` |
| `predict(df)` | DataFrame | `str` | `RegimeTrainer`, trained models |
| `confirm_regime(regime_history, n)` | list[str], int | `str\|None` | — |

**Output regimes:** `TRENDING`, `MEAN_REVERTING`, `BREAKOUT`.

---

## 8. `regime/mapper.py` — `RegimeMapper`

| Method | Input | Output | Dependency |
|--------|-------|--------|-----------|
| `map(regime, symbol)` | str, str | `str` | `REGIME_STRATEGY_MAP` |
| `get_params(strategy_name, symbol)` | str, str | `dict` | `ParamsStore` |

---

## 9. `strategy/base.py` — `BaseStrategy` (abstract)

| Method | Input | Output | Notes |
|--------|-------|--------|-------|
| `generate_signals(df, params)` | DataFrame, dict | `pd.DataFrame` | Abstract |
| `validate_params(params)` | dict | `bool` | Abstract |
| `get_default_params()` | — | `dict` | Concrete, override in subclasses |
| `calculate_atr(df, period)` | DataFrame, int | `pd.Series` | Concrete utility |
| `apply_sl_tp(entry, atr, sl_mult, tp_mult, direction)` | floats, str | `(float, float)` | Concrete utility |

---

## 10. Strategy Subclasses

| Class | File | Key Indicators | Regime |
|-------|------|---------------|--------|
| `TrendFollowingStrategy` | `strategy/trend_following.py` | EMA crossover, ADX | TRENDING |
| `MeanReversionStrategy` | `strategy/mean_reversion.py` | Bollinger Bands, RSI | MEAN_REVERTING |
| `BreakoutStrategy` | `strategy/breakout.py` | Donchian Channel, ATR | BREAKOUT |

Each subclass defines `PARAM_SPACE` used by the GA for parameter search bounds.

---

## 11. `optimizer/genetic_algorithm/individual.py` — `Individual`

| Method | Input | Output | Notes |
|--------|-------|--------|-------|
| `__init__(param_space, genes?)` | dict, list? | — | Random genes if not provided |
| `decode()` | — | `dict` | genes → params dict |
| `from_params(param_space, params)` | dict, dict | `Individual` | Class method |

---

## 12. `optimizer/genetic_algorithm/operators.py`

| Function | Input | Output |
|----------|-------|--------|
| `crossover(ind1, ind2, prob)` | Individual×2, float | `(Individual, Individual)` |
| `mutate(individual, prob, param_space?)` | Individual, float, dict? | `Individual` |
| `select_tournament(population, k)` | list[Individual], int | `Individual` |

---

## 13. `optimizer/genetic_algorithm/population.py` — `Population`

| Method | Input | Output |
|--------|-------|--------|
| `initialize(size)` | int | None |
| `evolve(fitness_scores)` | list[float] | None |
| `get_best()` | — | `Individual\|None` |

---

## 14. `optimizer/backtest.py` — `VectorbtBacktester`

| Method | Input | Output |
|--------|-------|--------|
| `run(df, signals, params)` | DataFrame, DataFrame, dict | `dict` |
| `run_multi_pair(dfs, strategy, genes)` | dict, strategy, list | `dict` |

**Result dict keys:** `sharpe_ratio`, `max_drawdown`, `win_rate`, `profit_factor`, `total_trades`.

---

## 15. `optimizer/fitness.py` — `fitness_function`

| Parameter | Description |
|-----------|-------------|
| `backtest_result` | dict from VectorbtBacktester |

**Returns:** float fitness score (higher = better).  Returns `-999.0` on disqualification.

---

## 16. `optimizer/scheduler.py` — `OptimizationScheduler`

| Method | Input | Output |
|--------|-------|--------|
| `run_weekly()` | — | None (blocking) |
| `optimize_all_pairs()` | — | None |
| `update_params_store(symbol, regime, strategy, params, result)` | str×3, dict×2 | None |

---

## 17. `signal/generator.py` — `SignalGenerator`

| Method | Input | Output |
|--------|-------|--------|
| `generate(symbol, regime, strategy, params, df)` | str×2, Strategy, dict, DataFrame | `dict\|None` |

---

## 18. `signal/transmitter.py` — `SignalTransmitter`

| Method | Input | Output |
|--------|-------|--------|
| `connect(port?)` | int? | None |
| `send(signal)` | dict | None |
| `disconnect()` | — | None |

---

## 19. `execution/mt5_executor.py` — `MT5Executor`

| Method | Input | Output |
|--------|-------|--------|
| `place_order(signal)` | dict | `dict\|None` |
| `close_order(ticket)` | int | `bool` |
| `get_open_positions()` | — | `list[dict]` |

---

## 20. `store/params_store.py` — `ParamsStore`

| Method | Input | Output |
|--------|-------|--------|
| `load()` | — | None |
| `save()` | — | None |
| `get_params(symbol, regime)` | str, str | `dict` |
| `update_params(symbol, regime, strategy, params, result?)` | str×3, dict, dict? | None |
| `get_last_updated()` | — | `str\|None` |

---

## 21. `monitoring/monitor.py` — `SystemMonitor`

| Method | Input | Output |
|--------|-------|--------|
| `check_data_freshness()` | — | `bool` |
| `check_mt5_connection()` | — | `bool` |
| `check_optimization_schedule()` | — | `bool` |
| `send_alert(message)` | str | None |
