# Architecture — AdaptiveFX

## 1. Full System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER  (Shared)                               │
│                                                                             │
│   MT5 Terminal ──► MT5 Python API ──► Export History ──► CSV / Parquet     │
│                    data/collector.py              data/storage.py           │
└────────────────────────────┬────────────────────────────────────────────────┘
                             │  (same local Parquet source)
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
┌──────────────────────────────┐  ┌──────────────────────────────────────────┐
│   PATH A  (Real-time)        │  │      PATH B  (Offline / Weekly)          │
│   Frequency: per candle      │  │      Frequency: every Sunday 02:00 UTC   │
│                              │  │                                          │
│  ┌────────────────────────┐  │  │  ┌──────────────────────────────────┐   │
│  │  regime/detector.py    │  │  │  │  optimizer/genetic_algorithm/    │   │
│  │  HMM (hmmlearn)        │  │  │  │  individual.py / operators.py   │   │
│  │  SVM (scikit-learn)    │  │  │  │  population.py                  │   │
│  └──────────┬─────────────┘  │  │  └────────────────┬─────────────────┘   │
│             │                │  │                   │                      │
│             ▼                │  │                   ▼                      │
│      Regime Label            │  │      optimizer/backtest.py               │
│  (TRENDING / MEAN_REV /      │  │      vectorbt Portfolio.from_signals()   │
│   BREAKOUT)                  │  │      fees=0.00007, slippage=0.00002      │
│             │                │  │                   │                      │
│             ▼                │  │                   ▼                      │
│  regime/mapper.py            │  │      optimizer/fitness.py                │
│  REGIME_STRATEGY_MAP         │  │      Sharpe·0.30 + PF·0.20              │
│             │                │  │      - DD·0.25 + WR·0.15 + TC·0.10     │
│             │                │  │                   │                      │
│             │       ◄────────┼──┤      Optimal Parameters                 │
│             ▼       params   │  │      store/params_store.py               │
│   Strategy + Params          │  │      (JSON, updated weekly)              │
└──────────┬───────────────────┘  └──────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        SIGNAL GENERATION LAYER                           │
│                                                                          │
│   signal/generator.py                                                    │
│   Strategy.generate_signals(df, params) → { symbol, direction,          │
│                                             entry, SL, TP, timestamp }  │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   │  ZeroMQ PUB/SUB
                                   │  signal/transmitter.py
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           EXECUTION LAYER                                │
│                                                                          │
│   execution/mt5_executor.py   ──►   MT5 EA   ──►  Place Order (TP/SL)  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Path A — Detailed Flow (Real-time, per candle)

```
New candle closes (H1 or M15)
        │
        ▼
data/collector.py
  MT5DataCollector.collect_ohlcv(symbol, timeframe, n_bars)
        │
        ▼
data/validator.py
  DataValidator.validate(df, symbol)  ─── FAIL ──► skip candle, log alert
        │ PASS
        ▼
regime/trainer.py (pre-loaded at startup)
  RegimeTrainer.prepare_features(df)
        │
        ▼
regime/detector.py
  RegimeDetector.predict(df)
  RegimeDetector.confirm_regime(history, n=3)  ─── None ──► previous regime
        │ confirmed
        ▼
regime/mapper.py
  RegimeMapper.map(regime, symbol)          → strategy_name
  RegimeMapper.get_params(strategy_name, symbol) → params (from params_store)
        │
        ▼
strategy/<strategy>.py
  Strategy.generate_signals(df, params)    → signals
        │
        ▼
signal/generator.py
  SignalGenerator.generate(symbol, regime, strategy, params, df)
        │ signal dict or None
        ▼
signal/transmitter.py
  SignalTransmitter.send(signal)
        │ ZeroMQ PUB
        ▼
MT5 EA (AdaptiveFX_EA.mq5)
  Receives JSON signal, places order with SL/TP
```

---

## 3. Path B — Detailed Flow (Offline, weekly)

```
optimizer/scheduler.py
  OptimizationScheduler.run_weekly()   ← triggered every Sunday 02:00 UTC
        │
        ▼
  For each symbol in CURRENCY_PAIRS (27 pairs):
    For each regime in ALL_REGIMES (3 regimes):
          │
          ▼
    data/storage.py
      DataStorage.load(symbol, OPTIMIZATION_TIMEFRAME)
          │
          ▼
    optimizer/genetic_algorithm/population.py
      Population.initialize(size=50)
          │
          ▼
    For generation in range(N_GENERATIONS=20):
      For each Individual in Population:
        individual.decode()                 → params dict
        strategy.generate_signals(df, params)
        VectorbtBacktester.run(df, signals, params) → backtest_result
        fitness_function(backtest_result)   → scalar score
      Population.evolve(fitness_scores)
          │
          ▼
    Population.get_best()                  → best Individual
          │
          ▼
    store/params_store.py
      ParamsStore.update_params(symbol, regime, strategy, params, result)
      ParamsStore.save()                   → params_store.json
```

---

## 4. params_store as the Bridge

```
PATH B (Writer)                         PATH A (Reader)
───────────────                         ──────────────
OptimizationScheduler                   RegimeMapper
    │                                       │
    │  writes weekly                        │  reads per candle
    ▼                                       ▼
store/params/params_store.json  ◄──────────┤
{                                           │
  "EURUSD": {                               │
    "TRENDING": {                           │
      "strategy": "TrendFollowingStrategy", │
      "params": { "ema_fast": 8, ... },     │
      "fitness_score": 1.84,               │
      "optimized_at": "2026-04-06T..."     │
    }                                       │
  }                                         │
}                                          ─┘
```

---

## 5. Component Interaction Table

| Source Component | Target Component | Data Exchanged | Transport |
|-----------------|-----------------|---------------|-----------|
| MT5DataCollector | DataStorage | OHLCV DataFrame | In-process |
| DataStorage | RegimeTrainer | OHLCV DataFrame | In-process |
| RegimeDetector | RegimeMapper | Regime label (str) | In-process |
| RegimeMapper | ParamsStore | symbol, regime | In-process |
| ParamsStore | RegimeMapper | params dict | In-process |
| Strategy | SignalGenerator | signals DataFrame | In-process |
| SignalGenerator | SignalTransmitter | signal dict | In-process |
| SignalTransmitter | MT5 EA | JSON string | ZeroMQ PUB/SUB |
| VectorbtBacktester | fitness_function | backtest result dict | In-process |
| OptimizationScheduler | ParamsStore | optimal params | In-process |

---

## 6. Technology Selection Rationale

| Requirement | Chosen Technology | Rationale |
|-------------|------------------|-----------|
| Ultra-fast backtesting (GA) | vectorbt | NumPy/Numba vectorisation; 10-30× faster than loop-based approaches |
| Regime detection | hmmlearn + scikit-learn | HMM for unsupervised state discovery; SVM for stable classification |
| GA optimisation | DEAP | Mature, highly configurable; supports multi-objective and parallel evaluation |
| Data storage | Apache Parquet (pyarrow) | Columnar format, excellent compression, fast I/O for large OHLCV datasets |
| Signal transport | ZeroMQ | Low-latency PUB/SUB; no broker required; native MQL5 support |
| Technical indicators | pandas-ta | Pandas-native, no TA-Lib C dependency required |
| Scheduling | schedule | Lightweight, Pythonic cron alternative |
| Logging | loguru | Structured, coloured, zero-config logging with rotation |

---

## 7. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Separate Path A and Path B | Decouples time-critical real-time decisions from compute-intensive optimisation |
| params_store JSON as bridge | Simple, human-readable, version-controllable; atomic write avoids race conditions |
| 3 confirmations candles for regime change | Reduces spurious strategy switches caused by noisy model output |
| Per-pair, per-regime optimisation | Captures pair-specific microstructure differences; avoids one-size-fits-all params |
| ATR-based SL/TP | Adapts risk sizing to current market volatility automatically |
| Correlated groups for risk management | Prevents doubling up on correlated exposure (e.g. EURUSD + GBPUSD both trending) |
