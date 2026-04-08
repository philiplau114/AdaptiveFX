# Data Design — AdaptiveFX

## 1. Parquet File Schema

All OHLCV data is stored as Parquet files using the **Apache Parquet** format via `pyarrow`.

### File Naming Convention

```
data/storage/
├── EURUSD/
│   ├── H1.parquet
│   ├── H4.parquet
│   └── D1.parquet
├── GBPUSD/
│   ├── H1.parquet
│   └── ...
└── ...
```

### Column Schema

| Column | Type | Description |
|--------|------|-------------|
| `time` (index) | `datetime64[ns, UTC]` | Bar open timestamp (UTC) |
| `open` | `float64` | Open price |
| `high` | `float64` | High price |
| `low` | `float64` | Low price |
| `close` | `float64` | Close price |
| `tick_volume` | `int64` | MT5 tick volume (proxy for real volume) |

### Parquet Configuration

| Setting | Value |
|---------|-------|
| Engine | `pyarrow` |
| Compression | `snappy` |
| Row group size | Default (128 MB) |
| Index | `time` column, sorted ascending |

---

## 2. params_store Full JSON Schema

The params_store JSON is the bridge between Path B (optimisation) and Path A (real-time trading).

### Top-Level Structure

```json
{
  "last_updated": "<ISO-8601 UTC timestamp>",
  "<SYMBOL>": {
    "<REGIME>": {
      "strategy":          "<StrategyClassName>",
      "params":            { ... },
      "fitness_score":     <float>,
      "backtest_sharpe":   <float>,
      "backtest_drawdown": <float>,
      "optimized_at":      "<ISO-8601 UTC timestamp>"
    }
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `last_updated` | ISO-8601 string | Timestamp when the file was last written |
| `strategy` | string | Strategy class name (e.g. `"TrendFollowingStrategy"`) |
| `params` | object | Strategy-specific optimised parameters |
| `fitness_score` | float | Composite GA fitness score (higher = better) |
| `backtest_sharpe` | float | Annualised Sharpe ratio from vectorbt backtest |
| `backtest_drawdown` | float | Maximum drawdown fraction (e.g. 0.112 = 11.2%) |
| `optimized_at` | ISO-8601 string | Timestamp of this specific optimisation run |

### Valid Keys

| Key | Values |
|-----|--------|
| `<SYMBOL>` | One of the 27 `CURRENCY_PAIRS` |
| `<REGIME>` | `TRENDING`, `MEAN_REVERTING`, or `BREAKOUT` |

### TrendFollowingStrategy `params` Schema

```json
{
  "ema_fast":      8,
  "ema_slow":      21,
  "adx_threshold": 25,
  "atr_period":    14,
  "sl_atr_mult":   1.5,
  "tp_atr_mult":   3.0
}
```

### MeanReversionStrategy `params` Schema

```json
{
  "bb_period":   20,
  "bb_std":      2.0,
  "rsi_period":  14,
  "rsi_low":     30,
  "rsi_high":    70,
  "atr_period":  14,
  "sl_atr_mult": 1.5,
  "tp_atr_mult": 2.0
}
```

### BreakoutStrategy `params` Schema

```json
{
  "donchian_period": 20,
  "atr_period":      14,
  "atr_mult":        1.5,
  "sr_lookback":     24,
  "sl_atr_mult":     1.5,
  "tp_atr_mult":     3.0
}
```

---

## 3. Signal Message Schema

Trading signals are transmitted from Python to the MT5 EA as JSON strings over ZeroMQ.

### ZeroMQ Message Format

```
"SIGNAL <JSON_payload>\n"
```

### Signal JSON Schema

```json
{
  "symbol":      "EURUSD",
  "direction":   "BUY",
  "entry_price": 1.08542,
  "sl":          1.08312,
  "tp":          1.09002,
  "timestamp":   "2026-04-06T08:00:00+00:00",
  "strategy":    "TrendFollowingStrategy",
  "regime":      "TRENDING"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Currency pair (MT5 symbol name) |
| `direction` | string | `"BUY"` or `"SELL"` |
| `entry_price` | float | Suggested entry price (5 decimal places) |
| `sl` | float | Stop-loss price |
| `tp` | float | Take-profit price |
| `timestamp` | ISO-8601 string | Signal generation time (UTC) |
| `strategy` | string | Strategy class name that generated the signal |
| `regime` | string | Detected market regime at signal time |

---

## 4. Data Update Schedule

| Job | Trigger | Description |
|-----|---------|-------------|
| Continuous OHLCV update | Every H1 bar close | Append new bars to Parquet storage |
| Full historical download | On first run / manual | Download all 27 pairs for the configured history depth |
| Path B optimisation | Every Sunday 02:00 UTC | Full GA optimisation, update params_store |
| Data freshness check | Every 15 minutes | Alert if any pair data is older than 2 hours |
| MT5 connection check | Every 5 minutes | Reconnect if MT5 terminal becomes unreachable |

---

## 5. Data Volume Estimates

| Pair | Timeframe | Bars/Year | Parquet Size |
|------|-----------|-----------|--------------|
| 1 pair | H1 | ~6,500 | ~500 KB |
| 1 pair | H4 | ~1,600 | ~130 KB |
| 1 pair | D1 | ~260 | ~22 KB |
| 27 pairs | H1 (2 years) | ~351,000 | ~27 MB |
| 27 pairs | H4 (5 years) | ~216,000 | ~17 MB |

Total estimated storage for all timeframes and 5 years of history: **< 100 MB**.
