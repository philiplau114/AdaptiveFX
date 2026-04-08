# Risk Management — AdaptiveFX

## Overview

AdaptiveFX enforces a multi-layered risk management framework to protect trading capital.  Risk controls operate at the position, portfolio, pair, and system levels.

---

## 1. Position-Level Rules

### 1.1 Risk Per Trade — 2%

Each trade risks at most 2% of current account equity.

```
Risk Amount   = Account Equity × 0.02
SL Distance   = |Entry Price − Stop Loss Price|
Lot Size      = Risk Amount / (SL Distance × Pip Value)
```

This ensures that no single losing trade reduces the account by more than 2%.

### 1.2 ATR-Based Stop Loss and Take Profit

Stop-loss and take-profit levels are set dynamically using the Average True Range (ATR) rather than fixed pip values, so that risk adapts to current market volatility.

| Parameter | Range (GA-optimised) |
|-----------|---------------------|
| SL multiplier (`sl_atr_mult`) | 1.0 – 3.0 × ATR |
| TP multiplier (`tp_atr_mult`) | 1.5 – 6.0 × ATR |

### 1.3 Spread Filter

Trades are not entered if the current bid/ask spread exceeds **3.0 pips** (configurable via `settings.SPREAD_FILTER_PIPS`).  This prevents entering during illiquid or high-spread conditions (e.g. news releases, session open/close).

---

## 2. Portfolio-Level Rules

### 2.1 Maximum Concurrent Positions — 5

At most **5 positions** may be open simultaneously across all 27 currency pairs.  New signals are suppressed if this limit is reached.

```python
if len(executor.get_open_positions()) >= settings.MAX_CONCURRENT_POSITIONS:
    # do not send new signal
    pass
```

### 2.2 Correlated Pairs Filter

Currency pairs are grouped by their structural correlation (see `config/pairs.py → CORRELATED_GROUPS`).  The system will not open more than **1 position per correlated group** at a time.

| Group | Pairs |
|-------|-------|
| USD_RISK_ON | EURUSD, GBPUSD, AUDUSD, NZDUSD |
| USD_RISK_OFF | USDJPY, USDCHF, USDCAD |
| EUR_CROSSES | EURGBP, EURJPY, EURCHF, EURAUD, EURCAD, EURNZD |
| GBP_CROSSES | GBPJPY, GBPCHF, GBPAUD, GBPCAD, GBPNZD |
| AUD_CROSSES | AUDJPY, AUDCHF, AUDCAD, AUDNZD |
| MISC_CROSSES | CADJPY, CADCHF, NZDJPY, NZDCHF, CHFJPY |

**Rationale:** Pairs in the same group move together.  Opening positions in both EURUSD and GBPUSD during a trending USD move effectively doubles directional exposure.

---

## 3. Drawdown Circuit Breakers

### 3.1 Trade-Level Disqualification (GA Optimisation)

During Path B optimisation, any parameter set that produces a backtest drawdown exceeding **30%** is automatically disqualified (fitness score = −999).  This ensures only robust strategies reach the params_store.

### 3.2 Account Drawdown Circuit Breaker (Live Trading)

If the live account drawdown reaches **20%**, the system enters a cooldown mode:
- No new positions are opened.
- An alert is dispatched via `SystemMonitor.send_alert()`.
- The system resumes only after manual reset or automatic recovery above the threshold.

```
Drawdown = (Peak Equity − Current Equity) / Peak Equity
```

---

## 4. Regime Transition Handling

### 4.1 Confirmation Window

A regime change is not acted upon until **3 consecutive candles** agree on the new regime (configurable via `settings.REGIME_CONFIRMATION_CANDLES`).  This prevents premature strategy switches due to transient signals.

### 4.2 Open Position Behaviour During Regime Change

When a confirmed regime change occurs:
- Existing positions are **not forcibly closed**.
- The SL/TP of existing positions are left unchanged.
- New signals are generated using the newly selected strategy and optimised parameters.
- The system tolerates a brief overlap where the previous strategy's positions close naturally.

---

## 5. GA Optimisation Fitness Disqualification Rules

The following rules cause a parameter set to be automatically disqualified during optimisation, regardless of other metrics:

| Rule | Threshold | Penalty |
|------|-----------|---------|
| Max drawdown too high | > 30% | Score = −999 |
| Profit factor below break-even | < 1.0 | Score = −999 |
| Win rate too low | < 25% | Score = −999 |
| Too few trades (insufficient confidence) | < 20 | Score = −999 |

---

## 6. Practical Risk Summary

| Control | Limit | Level |
|---------|-------|-------|
| Risk per trade | 2% of equity | Position |
| Max concurrent positions | 5 | Portfolio |
| Correlated pairs | 1 per group | Portfolio |
| Spread filter | 3.0 pips max | Position |
| ATR-based SL/TP | Volatility-adaptive | Position |
| GA drawdown disqualification | 30% | Optimisation |
| Account circuit breaker | 20% drawdown | System |
| Regime confirmation | 3 candles | Signal |
