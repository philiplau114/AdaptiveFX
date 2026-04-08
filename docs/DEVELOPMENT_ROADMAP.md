# Development Roadmap — AdaptiveFX

## Overview

The AdaptiveFX project is structured into four sequential development phases, each building on the previous.  Each phase has clear deliverables and measurable success criteria.

---

## Phase 1 — Data Foundation (Weeks 1–3)

**Goal:** Establish a reliable, validated local data pipeline for all 27 currency pairs.

### Deliverables

- [ ] `data/collector.py` — MT5DataCollector fully implemented and tested
- [ ] `data/storage.py` — Parquet read/write with incremental update
- [ ] `data/validator.py` — Missing-candle and outlier detection
- [ ] `config/settings.py` — All environment variables wired up
- [ ] `config/pairs.py` — All 27 pairs confirmed tradeable on target broker
- [ ] `tests/test_data.py` — 100% test coverage for data module
- [ ] Initial historical download: 5 years of H1 and H4 data for all 27 pairs

### Success Criteria

- All 27 pairs download without errors
- DataValidator passes for all downloaded pairs
- Parquet files load within 200ms per pair per timeframe
- Incremental update adds only new bars (no duplicates)

---

## Phase 2 — Regime Detection (Weeks 4–7)

**Goal:** Train and validate HMM + SVM regime classifiers for all 27 pairs.

### Deliverables

- [ ] `regime/trainer.py` — Feature engineering + HMM + SVM training
- [ ] `regime/detector.py` — Real-time regime prediction with confirmation
- [ ] `regime/mapper.py` — Regime → strategy name + params lookup
- [ ] `store/params_store.py` — JSON load/save/get/update
- [ ] `tests/test_regime.py` — Unit and integration tests for regime module
- [ ] Trained models saved for all 27 pairs to `models/` directory
- [ ] Visual validation: regime labels plotted against price for 3 pairs

### Success Criteria

- HMM converges (positive log-likelihood) for all 27 pairs
- SVM cross-validation accuracy ≥ 70% on held-out data
- Regime confirmation (3 candles) reduces false switches by ≥ 50%
- End-to-end latency of regime detection ≤ 100ms per pair

---

## Phase 3 — Strategy Optimisation (Weeks 8–12)

**Goal:** Implement all three strategies and run full GA optimisation.

### Deliverables

- [ ] `strategy/base.py` — Abstract base with ATR SL/TP utilities
- [ ] `strategy/trend_following.py` — EMA crossover + ADX, fully implemented
- [ ] `strategy/mean_reversion.py` — Bollinger Bands + RSI, fully implemented
- [ ] `strategy/breakout.py` — Donchian Channel + ATR, fully implemented
- [ ] `optimizer/genetic_algorithm/` — individual, operators, population complete
- [ ] `optimizer/backtest.py` — VectorbtBacktester with fees and slippage
- [ ] `optimizer/fitness.py` — Full fitness function with disqualification rules
- [ ] `optimizer/scheduler.py` — Weekly scheduler operational
- [ ] `tests/test_strategy.py`, `tests/test_optimizer.py` — Full test coverage
- [ ] First successful full optimisation run (27 pairs × 3 strategies)
- [ ] `store/params/params_store.json` populated with real optimised parameters

### Success Criteria

- GA converges in ≤ 30 minutes for one pair/strategy on standard hardware
- Full 27-pair optimisation completes within 8 hours
- Best parameters achieve Sharpe ≥ 1.0 and max drawdown ≤ 20% in backtest
- Profit factor ≥ 1.2 and win rate ≥ 35% for at least 2 of 3 strategies

---

## Phase 4 — Live Integration (Weeks 13–16)

**Goal:** Connect the fully optimised system to MT5 for live paper trading, then real trading.

### Deliverables

- [ ] `signal/generator.py` — Full signal generation pipeline
- [ ] `signal/transmitter.py` — ZeroMQ PUB socket, tested with MT5 EA
- [ ] `execution/mt5_executor.py` — MT5 order placement with risk sizing
- [ ] `ea/AdaptiveFX_EA.mq5` — Production MQL5 EA receiving ZeroMQ signals
- [ ] `monitoring/monitor.py` — All health checks operational with alerts
- [ ] `main.py` — All three modes (live, optimize, collect) fully operational
- [ ] 30-day paper trading run on MT5 demo account
- [ ] Risk management circuit breakers tested in simulation

### Success Criteria

- Signal latency (regime detection → ZeroMQ send) ≤ 500ms
- MT5 EA executes 100% of received signals without errors
- Paper trading Sharpe ≥ 0.8 over 30 days
- No position exceeds 2% risk per trade
- Correlated pairs filter prevents simultaneous entries in the same group
- System runs unattended for 7+ days without requiring manual intervention

---

## Summary Timeline

| Phase | Focus | Duration | Key Milestone |
|-------|-------|----------|--------------|
| 1 | Data Foundation | Weeks 1–3 | 27 pairs validated in Parquet |
| 2 | Regime Detection | Weeks 4–7 | All models trained and validated |
| 3 | Strategy Optimisation | Weeks 8–12 | params_store populated with real data |
| 4 | Live Integration | Weeks 13–16 | 30-day paper trading pass |

**Total estimated duration:** 16 weeks (4 months) for one developer.  Parallel development of Phase 2 and 3 is possible if a second developer is available, reducing total time to ~10 weeks.
