# PulseAD Tuning Guide

Quick reference for configuring GradientCastPulseAD (deviation-based anomaly detection).

---

## How PulseAD Works

**Important:** PulseAD evaluates only the most recent data points in the time series you provide. Historical data serves as context for establishing expected behavior patterns, but anomaly detection is performed only on the latest point(s).

1. Uses historical data as context to learn expected behavior patterns
2. Evaluates only the most recent data point(s) against those expectations
3. Flags anomalies when deviation exceeds threshold AND value exceeds minimum

```
Anomaly = (percent_delta > threshold) AND (value > minimum)
```

For real-time monitoring, pass a sliding window of historical data with each new data point appended at the end. The detector will analyze only the newest point(s) while using the history for context.

---

## Threshold Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `percentage_threshold` | 15% (0.15) | Minimum deviation to flag as anomaly |
| `minimum_value_threshold` | 100,000 | Filter out low-volume noise |

### Percentage Threshold Guidelines

| Use Case | Recommended | Example |
|----------|-------------|---------|
| Critical metrics (revenue, core KPIs) | 5-10% | Catch issues early |
| Standard monitoring | 15-20% | Balance sensitivity |
| Volatile/noisy metrics | 25-30% | Reduce false positives |

### Minimum Value Guidelines

| Volume Level | Recommended | Example Metrics |
|--------------|-------------|-----------------|
| Very high | 1,000,000+ | Page views, requests |
| High | 100,000-1,000,000 | Active users |
| Medium | 10,000-100,000 | Transactions |
| Low | 1,000-10,000 | Signups, purchases |

---

## Configuration Examples

### Basic Configuration

```python
from gradientcast import ThresholdConfig

config = ThresholdConfig(
    default_percentage=0.15,
    default_minimum=100000
)
```

### Strict Monitoring

```python
config = ThresholdConfig(
    default_percentage=0.10,  # Stricter: 10%
    default_minimum=50000
)
```

### Relaxed Monitoring

```python
config = ThresholdConfig(
    default_percentage=0.25,  # Relaxed: 25%
    default_minimum=100000
)
```

### Per-Dimension Overrides

```python
config = ThresholdConfig(
    default_percentage=0.20,
    default_minimum=100000,
    per_dimension_overrides={
        "critical_revenue": {
            "percentage_threshold": 0.05,
            "minimum_value_threshold": 1000000
        },
        "experimental_feature": {
            "percentage_threshold": 0.40,
            "minimum_value_threshold": 1000
        }
    }
)
```

---

## Detection Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `frequency` | `H` | Data frequency (H, D, W, M, Q, Y) |
| `forecast_horizon` | 3 | Points to forecast ahead |
| `validation_points` | 3 | Latest points to validate |

### Frequency Selection

| Data Granularity | Frequency |
|------------------|-----------|
| Hourly or finer | `H` |
| Daily | `D` |
| Weekly | `W` |
| Monthly | `M` |

---

## Common Scenarios

### High False Positive Rate

**Problem:** Too many alerts for normal variations

**Solutions:**
1. Increase `percentage_threshold` (e.g., 15% → 25%)
2. Increase `minimum_value_threshold` to filter noise
3. Ensure sufficient historical data (10+ points)

### Missing Real Anomalies

**Problem:** Actual issues not being flagged

**Solutions:**
1. Decrease `percentage_threshold` (e.g., 15% → 10%)
2. Check if values are above `minimum_value_threshold`
3. Verify data quality and timestamp format

### Noisy Low-Volume Metrics

**Problem:** Small metrics causing many alerts

**Solutions:**
1. Increase `minimum_value_threshold`
2. Use per-dimension overrides for low-volume metrics
3. Consider using DensityAD for pattern-based detection

---

## Integration Patterns

### Real-Time Monitoring

```python
def process_new_datapoint(history, new_point):
    """Process each new datapoint as it arrives.

    The detector uses 'history' as context but only evaluates the
    most recent point(s) for anomalies. The new_point is the actual
    data point being checked for anomalous behavior.
    """
    # Append new point to history - this is the point being evaluated
    history.append(new_point)

    # Keep a rolling window (e.g., last 720 points for hourly data = 30 days)
    if len(history) > 720:
        history = history[-720:]

    # Detect: history provides context, but only latest point(s) are evaluated
    result = ad.detect({"metric": history})

    if result.has_anomaly:
        latest = result.anomalies[-1]  # Most recent anomaly
        send_alert(latest)

    return result
```

### Batch Processing

```python
def analyze_batch(data_batch):
    """Analyze multiple metrics in one call."""
    result = ad.detect(data_batch)

    for anomaly in result.anomalies:
        log_anomaly(anomaly.dimension, anomaly.percent_delta)

    return result
```

---

## Data Requirements

- **Minimum history:** 4+ data points (validation_points + 1)
- **Recommended history:** 10+ points for reliable detection
- **Timestamp format:** `MM/DD/YYYY, HH:MM AM/PM`

---

## Quick Checklist

Before deployment:

- [ ] Thresholds calibrated on historical data
- [ ] Minimum value set appropriately for metric volume
- [ ] Per-dimension overrides for critical metrics
- [ ] Sufficient history in data window
- [ ] Timestamps in correct format
- [ ] Alert handling implemented
