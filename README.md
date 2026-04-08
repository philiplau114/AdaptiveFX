# AdaptiveFX

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![MT5](https://img.shields.io/badge/MetaTrader-5-blue)](https://www.metatrader5.com/)
[![Vectorbt](https://img.shields.io/badge/vectorbt-0.26.2%2B-orange)](https://vectorbt.dev/)
[![DEAP](https://img.shields.io/badge/DEAP-1.4.1%2B-red)](https://deap.readthedocs.io/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)]()

> A fully automated forex quantitative trading system powered by HMM+SVM regime detection, Genetic Algorithm optimization, and Vectorbt backtesting — built for 27 currency pairs.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER  (Shared)                               │
│                                                                             │
│   MT5 Terminal ──► MT5 Python API ──► Export History ──► CSV / Parquet     │
└────────────────────────────┬────────────────────────────────────────────────┘
                             │  (same local data source)
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
┌─────────────────────────┐   ┌──────────────────────────────────────────────┐
│   PATH A  (Real-time)   │   │           PATH B  (Offline / Weekly)         │
│                         │   │                                              │
│  regime_detection_ml    │   │  GeneTrader GA Core                          │
│  ┌───────────────────┐  │   │  ┌────────────────────────────────────────┐  │
│  │  HMM  +  SVM      │  │   │  │  operators / individual / population   │  │
│  └────────┬──────────┘  │   │  └────────────────┬───────────────────────┘  │
│           │             │   │                   │                           │
│           ▼             │   │                   ▼                           │
│    Regime Label         │   │      Vectorbt Backtesting Engine              │
│  (per currency pair)    │   │  ┌────────────────────────────────────────┐  │
│           │             │   │  │  Portfolio.from_signals() + fees/slip  │  │
│           ▼             │   │  └────────────────┬───────────────────────┘  │
│   Regime → Strategy     │   │                   │                           │
│       Map               │   │                   ▼                           │
│           │             │   │           Fitness Score                       │
│           ▼             │   │   (Sharpe·0.30 | DD·0.25 | WR·0.15           │
│   Selected Strategy  ◄──┼───┤    PF·0.20 | TradeCount·0.10)               │
│   + Optimal Params      │   │                   │                           │
│  (from params_store)    │   │                   ▼                           │
└──────────┬──────────────┘   │         Optimal Parameters                   │
           │                  │         ──► params_store.json (weekly)        │
           │                  └──────────────────────────────────────────────┘
           ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        SIGNAL GENERATION LAYER                           │
│                                                                          │
│   Strategy (Trend / MeanReversion / Breakout) + Optimal Params          │
│       ──► Signal { symbol, direction, entry, SL, TP, timestamp }        │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   │
                                   ▼ ZeroMQ PUB/SUB
┌──────────────────────────────────────────────────────────────────────────┐
│                           EXECUTION LAYER                                │
│                                                                          │
│   MT5 Python API / ZeroMQ  ──►  MT5 EA  ──►  Place Order (TP / SL)     │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

- **27 Currency Pairs** — major, minor, and cross pairs fully covered
- **Dual-Path Architecture** — real-time regime detection (Path A) + weekly offline optimization (Path B)
- **HMM + SVM Regime Detection** — three regimes: Trending, Mean-Reverting, Breakout
- **Genetic Algorithm Optimization** — DEAP-powered GA with Vectorbt backtesting (10–30× faster than loop-based approaches)
- **Three Adaptive Strategies** — Trend Following (EMA + ADX), Mean Reversion (BB + RSI), Breakout (ATR + Donchian)
- **params_store Bridge** — regime-specific optimal parameters persisted as JSON, updated weekly
- **ZeroMQ Signal Transmission** — low-latency PUB/SUB between Python and MT5 EA
- **Forex-Specific Fitness Function** — accounts for spread costs, drawdown penalties, and trade confidence
- **Risk Management** — max 5 concurrent positions, 2% risk per trade, correlated-pairs filter, circuit breakers
- **Loguru Logging** — structured, coloured logs throughout every component

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Data Collection | MetaTrader5 Python API | OHLCV data from MT5 terminal |
| Data Storage | Apache Parquet (pyarrow) | Efficient columnar storage |
| Regime Detection | hmmlearn + scikit-learn | HMM training + SVM classification |
| Backtesting | vectorbt | Vectorised, ultra-fast backtesting |
| Optimisation | DEAP (GA) | Genetic algorithm parameter search |
| Technical Indicators | pandas-ta | EMA, BB, RSI, ATR, ADX, Donchian |
| Signal Transport | pyzmq (ZeroMQ) | PUB/SUB between Python ↔ MT5 EA |
| Scheduling | schedule | Weekly optimisation jobs |
| Logging | loguru | Structured logging |
| Testing | pytest | Unit tests |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/philiplau114/AdaptiveFX.git
cd AdaptiveFX
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `MetaTrader5` package requires a Windows environment with MT5 terminal installed.

### 3. Configure Environment

```bash
cp store/params/params_store.json.example store/params/params_store.json
```

Set the following environment variables (or create a `.env` file):

```bash
MT5_LOGIN=your_account_number
MT5_PASSWORD=your_password
MT5_SERVER=your_broker_server
DATA_PATH=./data/storage
```

### 4. Run

```bash
# Collect data
python main.py --mode collect

# Run weekly optimisation (Path B)
python main.py --mode optimize

# Start live trading (Path A)
python main.py --mode live
```

---

## 📁 Project Structure

```
AdaptiveFX/
├── main.py                          # Entry point (--mode live|optimize|collect)
├── requirements.txt                 # Python dependencies
├── README.md
│
├── config/
│   ├── __init__.py
│   ├── settings.py                  # Global settings (MT5, paths, schedule)
│   └── pairs.py                     # 27 pairs, timeframes, regime→strategy map
│
├── data/
│   ├── __init__.py
│   ├── collector.py                 # MT5DataCollector
│   ├── storage.py                   # Parquet read/write (DataStorage)
│   └── validator.py                 # Data quality checks (DataValidator)
│
├── regime/
│   ├── __init__.py
│   ├── detector.py                  # RegimeDetector (HMM+SVM predict)
│   ├── trainer.py                   # RegimeTrainer (feature extraction, fit)
│   └── mapper.py                    # RegimeMapper (regime → strategy)
│
├── strategy/
│   ├── __init__.py
│   ├── base.py                      # Abstract BaseStrategy
│   ├── trend_following.py           # EMA crossover + ADX
│   ├── mean_reversion.py            # Bollinger Bands + RSI
│   └── breakout.py                  # ATR breakout + Donchian
│
├── optimizer/
│   ├── __init__.py
│   ├── genetic_algorithm/
│   │   ├── __init__.py
│   │   ├── individual.py            # Gene encoding/decoding
│   │   ├── operators.py             # crossover, mutate, select
│   │   └── population.py            # Population management
│   ├── backtest.py                  # VectorbtBacktester
│   ├── fitness.py                   # Forex fitness function
│   └── scheduler.py                 # Weekly optimisation scheduler
│
├── signal/
│   ├── __init__.py
│   ├── generator.py                 # SignalGenerator
│   └── transmitter.py               # ZeroMQ SignalTransmitter
│
├── execution/
│   ├── __init__.py
│   └── mt5_executor.py              # MT5Executor (place/close orders)
│
├── store/
│   ├── __init__.py
│   ├── params_store.py              # ParamsStore (load/save/get/update)
│   └── params/
│       └── params_store.json.example
│
├── monitoring/
│   ├── __init__.py
│   └── monitor.py                   # SystemMonitor
│
├── tests/
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_regime.py
│   ├── test_strategy.py
│   └── test_optimizer.py
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── COMPONENTS.md
│   ├── DATA_DESIGN.md
│   ├── RISK_MANAGEMENT.md
│   ├── DEVELOPMENT_ROADMAP.md
│   └── FEASIBILITY_STUDY.md
│
└── ea/
    └── AdaptiveFX_EA.mq5.example    # MQL5 EA ZeroMQ template
```

---

## ⚠️ Disclaimer

**For educational and research purposes only.**
This software is provided as-is without any warranty. Trading foreign exchange on margin carries a high level of risk and may not be suitable for all investors. Past performance is not indicative of future results. Never risk money you cannot afford to lose. The authors accept no liability for any financial losses incurred through the use of this software.