# Forecasting Tuning Guide

Quick reference for optimizing GradientCastFM forecasts.

---

## Frequency Selection

| Data Granularity | Frequency Code | Example Use Cases |
|-----------------|----------------|-------------------|
| Hourly or finer | `H` | Server metrics, IoT sensors |
| Daily | `D` | Sales, website traffic |
| Weekly | `W` | Weekly aggregates |
| Monthly | `M` | Revenue, subscriptions |
| Quarterly | `Q` | Financial reports |
| Yearly | `Y` | Annual planning |

**Tip:** Match the frequency to your data's natural granularity for best results.

---

## Context Length

The model automatically determines optimal context length, but these guidelines help:

| Horizon | Recommended Context | Rationale |
|---------|---------------------|-----------|
| 1-7 days | 30+ days | Capture weekly patterns |
| 1-4 weeks | 60+ days | Capture monthly patterns |
| 1-12 months | 2+ years | Capture yearly seasonality |

**Rule of thumb:** Provide at least 3x the horizon length as context.

---

## Covariates

### When to Use Covariates

**Use covariates when:**
- External factors clearly influence your target
- You have reliable future values (forecasts, schedules)
- Base forecasts show systematic errors

**Skip covariates when:**
- Historical patterns are sufficient
- Future covariate values are uncertain
- Simpler model is preferred

### Covariate Types

| Type | Example | Format |
|------|---------|--------|
| Static Numerical | Store size | `{"store_size": {"series_1": 5000}}` |
| Static Categorical | Region | `{"region": {"series_1": "west"}}` |
| Dynamic Numerical | Temperature | `{"temp": {"series_1": [72, 75, ...]}}` |
| Dynamic Categorical | Day of week | `{"dow": {"series_1": ["Mon", "Tue", ...]}}` |

**Important:** Dynamic covariates must cover `context_length + horizon_length`.

---

## XReg Modes

| Mode | How It Works | Best For |
|------|--------------|----------|
| `xreg + timesfm` | Fit covariates first, forecast residuals | Strong covariate effects |
| `timesfm + xreg` | Forecast first, fit residuals with covariates | Strong time patterns |

**Default:** `xreg + timesfm` works well for most cases. Try both if unsure.

---

## Batch Processing

### Optimal Batch Sizes

| Batch Size | Latency | Throughput | Use Case |
|------------|---------|------------|----------|
| 1-5 | Low | Low | Real-time, interactive |
| 10-50 | Medium | High | Batch processing |
| 50-100 | Higher | Highest | Large-scale pipelines |

### Tips

1. **Group by frequency** - Batch series with the same granularity
2. **Similar context lengths** - Avoid mixing 30-day and 2-year contexts
3. **Increase timeout** - Use `timeout=300` for large batches

---

## Common Issues

### Forecast Looks Flat

- **Cause:** Insufficient context or noisy data
- **Fix:** Provide more historical data, try `seasonality_boost=True`

### High Latency

- **Cause:** Large batch or long context
- **Fix:** Reduce batch size, ensure appropriate timeout

### Covariates Not Helping

- **Cause:** Weak correlation or wrong mode
- **Fix:** Verify covariate relevance, try alternate `xreg_mode`

### Missing Values

- **Cause:** Gaps in time series
- **Fix:** Interpolate gaps before calling API

---

## Performance Benchmarks

Typical latencies (may vary):

| Scenario | Latency |
|----------|---------|
| Single series, 30 points | ~300-500ms |
| 10 series, 60 points each | ~800-1200ms |
| 50 series, 120 points each | ~2-4s |

---

## Quick Checklist

Before calling the API:

- [ ] Frequency matches data granularity
- [ ] Sufficient context length (3x+ horizon)
- [ ] No missing values in series
- [ ] Dynamic covariates include horizon
- [ ] Appropriate timeout for batch size
