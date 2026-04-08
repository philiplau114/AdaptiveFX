# Feasibility Study — AdaptiveFX

## Executive Summary

AdaptiveFX is a technically ambitious but feasible project.  The core technologies (HMM, SVM, Vectorbt, DEAP, ZeroMQ) are mature and widely used in algorithmic trading.  The primary risks are data quality, overfitting, and the complexity of the MT5 integration.  With careful implementation and the phased development roadmap, the project can be completed by a single experienced Python developer in approximately 4 months.

---

## 1. Component Feasibility Scores

| Component | Feasibility | Complexity | Notes |
|-----------|-------------|------------|-------|
| MT5 Data Collection | 🟢 High | Low | Official MT5 Python API, well-documented |
| Parquet Storage | 🟢 High | Low | Mature library, trivial implementation |
| Data Validation | 🟢 High | Low | Standard statistical techniques |
| HMM Training (hmmlearn) | 🟡 Medium | Medium | Requires careful feature engineering; convergence not guaranteed |
| SVM Classification | 🟢 High | Low-Medium | Mature algorithm; sklearn makes it straightforward |
| Regime Confirmation Logic | 🟢 High | Low | Simple sliding window |
| Vectorbt Backtesting | 🟢 High | Medium | API learning curve; excellent documentation |
| DEAP Genetic Algorithm | 🟡 Medium | Medium | GA tuning (mutation rates, population size) requires experimentation |
| Forex Fitness Function | 🟡 Medium | Medium | Designing a well-calibrated multi-component score is non-trivial |
| Strategy Implementation | 🟢 High | Low-Medium | Standard indicators via pandas-ta |
| ZeroMQ Signalling | 🟢 High | Low | Simple PUB/SUB; MT5 MQL5 zmq library available |
| MT5 Order Execution | 🟡 Medium | Medium | Broker-specific quirks; requires thorough testing on demo |
| MQL5 EA Development | 🟡 Medium | Medium | Requires MQL5 knowledge (separate skill set) |
| Risk Management Logic | 🟢 High | Low | Rule-based; straightforward to implement |
| Monitoring & Alerting | 🟢 High | Low | loguru + simple HTTP webhook to Telegram/Slack |

---

## 2. Risk Table

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| HMM fails to converge on some pairs | Medium | High | Use multiple random restarts; fallback to rule-based regime detection |
| Overfitting in GA optimisation | High | High | Walk-forward validation; out-of-sample testing before live deployment |
| MT5 broker data gaps / quality issues | Medium | Medium | DataValidator + automatic re-download on detection |
| Regime mislabelling during volatile markets | Medium | Medium | 3-candle confirmation window; conservative strategy selection |
| ZeroMQ connectivity failures | Low | High | Heartbeat check + automatic reconnect; fallback to direct MT5 API |
| MT5 terminal goes offline | Low | High | SystemMonitor check every 5 minutes; automated restart script |
| params_store becomes stale during market regime shift | Medium | Medium | Weekly scheduled re-optimisation; manual trigger option |
| Spread widens during news events | Medium | Medium | Spread filter (3 pip max); no trading during scheduled high-impact news |
| Live performance diverges from backtest | High | High | Conservative lot sizing; 30-day paper trading before real money |
| MQL5 EA bugs in order placement | Medium | High | Extensive demo testing; logging of all order requests and responses |

---

## 3. Effort Estimate

| Phase | Task | Estimated Hours |
|-------|------|----------------|
| 1 | Data pipeline (collector, storage, validator) | 40h |
| 2 | Regime detection (trainer, detector, mapper) | 60h |
| 3 | Strategy implementation (3 strategies) | 30h |
| 3 | GA + Vectorbt integration | 50h |
| 3 | Fitness function + scheduler | 20h |
| 4 | Signal generation + ZeroMQ | 20h |
| 4 | MT5 execution + MQL5 EA | 40h |
| 4 | Monitoring + alerting | 15h |
| 4 | Testing + paper trading | 50h |
| All | Documentation + config | 20h |
| **Total** | | **~345 hours (~10–14 weeks solo)** |

---

## 4. Using GitHub Copilot Agentic AI for Implementation

### 點樣幫你 (How Copilot Can Help)

GitHub Copilot 嘅 Agentic AI 可以大幅加速呢個項目嘅實現：

| 任務 | Copilot 可以做咩 | 預計節省時間 |
|------|-----------------|------------|
| 填寫 TODO 實現 | 根據 docstring 和 type hints 自動生成實現代碼 | 50–70% |
| 寫 pytest 測試 | 根據函數簽名生成全面測試 | 60–80% |
| 調試 HMM 收斂問題 | 分析錯誤信息，建議超參數調整 | 40–60% |
| 寫 MQL5 EA | 生成 ZeroMQ 接收和訂單放置代碼 | 50–70% |
| 代碼審查 | 自動識別邊界情況、安全問題 | 持續改進 |

### 最佳使用方式

1. **逐個 TODO 實現** — 打開每個 `# TODO` 部分，Copilot 會根據 docstring 自動補全
2. **Chat 模式問架構問題** — "點樣用 hmmlearn 訓練 GaussianHMM？"
3. **Inline Suggestion** — 打 `def prepare_features`，Copilot 會建議完整實現
4. **Multi-file Context** — Copilot 理解跨文件的依賴關係（如 RegimeMapper 依賴 ParamsStore）
5. **測試生成** — 在 test 文件中問 "Generate tests for DataValidator"

### 注意事項

- Copilot 生成的代碼需要人工審查，特別是金融邏輯部分
- 風險管理邏輯（lot sizing, circuit breakers）必須手動驗證
- 永遠先在 demo 帳戶測試，唔好直接上 live

---

## 5. Conclusion

**AdaptiveFX is feasible to implement** with the following conditions:

1. ✅ The architecture design (dual-path, params_store bridge) is sound and well-precedented in production quant systems.
2. ✅ All chosen technologies are mature, open-source, and well-documented.
3. ⚠️ The HMM regime detection requires careful validation — it is the highest-risk component technically.
4. ⚠️ Overfitting is the primary business risk — walk-forward validation and conservative live deployment are essential.
5. ✅ GitHub Copilot can significantly accelerate implementation, particularly for boilerplate, tests, and indicator logic.
6. ✅ The modular architecture means each component can be developed, tested, and validated independently.

**Recommended next step:** Complete Phase 1 (data pipeline) and validate that high-quality Parquet data is available for all 27 pairs before investing time in regime detection and strategy optimisation.
