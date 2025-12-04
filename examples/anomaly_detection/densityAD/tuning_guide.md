# DensityAD Tuning Guide

Quick reference for configuring GradientCastDenseAD (intelligent pattern detection).

---

## How DensityAD Works

**Important:** DensityAD evaluates only the most recent data points in the time series you provide. Historical data serves as context for feature engineering and pattern learning, but anomaly detection is performed only on the latest point(s) in the window.

1. **Feature Engineering**: Extracts rolling stats, z-scores, lags, seasonal features from historical context
2. **Pattern Detection**: Identifies points with unusual density patterns (evaluated on recent data only)
3. **Post-Processing**: Filters noise with valley threshold and contiguous requirements
4. **Severity Classification**: Assigns low/medium/high/critical based on magnitude

For real-time monitoring, pass a sliding window of historical data with each new data point appended at the end. The detector will analyze only the newest point(s) while using the history for context.

---

## Core Parameters

### Detection Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `contamination` | 0.05 (5%) | Expected proportion of anomalies |
| `n_neighbors` | 20 | Neighbors for local density calculation |

### Contamination Guidelines

| Value | Sensitivity | Use Case |
|-------|-------------|----------|
| 0.01-0.03 | Low | Clean data, few expected anomalies |
| 0.05 | Medium | Balanced detection (default) |
| 0.10-0.15 | High | Noisy data, catch more issues |

### N Neighbors Guidelines

| Value | Effect | When to Use |
|-------|--------|-------------|
| 5-10 | Local focus | Detect point-level anomalies |
| 15-25 | Balanced | General purpose (default ~20) |
| 30-50 | Global view | Detect pattern-level changes |

---

## Post-Processing Parameters

### Valley Threshold

Minimum value to consider for detection. Filters low-volume noise.

| Dimension Type | Recommended | Example |
|----------------|-------------|---------|
| AllUp (total) | 3,000,000 | Total user count |
| High volume | 500,000-1,000,000 | Regional metrics |
| Medium volume | 100,000-500,000 | Product metrics |
| Low volume | 10,000-100,000 | Feature metrics |

### Minimum Contiguous Anomalies

Requires N consecutive anomalies to confirm.

| Value | Effect | When to Use |
|-------|--------|-------------|
| 1 | No filtering | Catch isolated spikes |
| 2 | Light filtering | Balance sensitivity (default) |
| 3-4 | Strong filtering | Reduce noise in volatile data |

---

## Severity Levels

Based on normalized anomaly score and z-score deviation:

| Severity | Normalized Score | Typical Deviation | Action |
|----------|-----------------|-------------------|--------|
| Low | 30-50 | 10-25% | Monitor |
| Medium | 50-70 | 25-40% | Investigate |
| High | 70-85 | 40-60% | Alert |
| Critical | 85+ | 60%+ | Immediate |

---

## Configuration Examples

### High Sensitivity

```python
result = dense_ad.detect(
    data,
    contamination=0.10,
    n_neighbors=15,
    min_contiguous_anomalies=1,
    valley_threshold=100000
)
```

### Balanced (Recommended Start)

```python
result = dense_ad.detect(
    data,
    contamination=0.05,
    n_neighbors=20,
    min_contiguous_anomalies=2
)
```

### Low Sensitivity

```python
result = dense_ad.detect(
    data,
    contamination=0.02,
    n_neighbors=30,
    min_contiguous_anomalies=3,
    valley_threshold=2000000
)
```

---

## Common Scenarios

### Too Many False Positives

**Symptoms:** Many alerts for normal variations

**Solutions:**
1. Decrease `contamination` (0.05 → 0.02)
2. Increase `n_neighbors` (20 → 30)
3. Increase `min_contiguous_anomalies` (2 → 3)
4. Increase `valley_threshold`

### Missing Real Anomalies

**Symptoms:** Known issues not being flagged

**Solutions:**
1. Increase `contamination` (0.05 → 0.10)
2. Decrease `n_neighbors` (20 → 15)
3. Decrease `min_contiguous_anomalies` (2 → 1)
4. Lower `valley_threshold`

### Low-Volume Metrics Noisy

**Symptoms:** Small metrics causing many alerts

**Solutions:**
1. Increase `valley_threshold` for that dimension
2. Use higher `min_contiguous_anomalies`
3. Consider using PulseAD for simple threshold detection

---

## Magnitude Metrics

Each anomaly includes magnitude information:

| Metric | Description | Range |
|--------|-------------|-------|
| `anomaly_score` | Raw density score | 1.0+ (higher = more anomalous) |
| `normalized_score` | Scaled score | 0-100 |
| `zscore_24h` | Deviation from 24h mean | ±σ units |
| `deviation_pct` | Percentage deviation | ±% |
| `expected_value_24h` | Rolling mean | Same as value units |

---

## Integration Pattern

```python
def process_streaming_data(history, new_point):
    """Process each new datapoint in production.

    The detector uses 'history' as context but only evaluates the
    most recent point(s) for anomalies. The new_point is the actual
    data point being checked for anomalous behavior.
    """
    # Append new point to history - this is the point being evaluated
    history.append(new_point)

    # Keep rolling window (e.g., 720 hours = 30 days)
    if len(history) > 720:
        history = history[-720:]

    # Detect: history provides context, but only latest point(s) are evaluated
    result = dense_ad.detect(
        history,
        contamination=0.05,
        n_neighbors=20,
        min_contiguous_anomalies=2,
        return_window_hours=24  # Return results for last 24 hours
    )

    if result.has_anomaly:
        for anomaly in result.anomalies:
            if anomaly.magnitude.severity in ['high', 'critical']:
                send_alert(anomaly)
            else:
                log_warning(anomaly)

    return result
```

---

## Data Requirements

- **Minimum history**: 24+ data points (for feature engineering)
- **Recommended history**: 168+ points (1 week hourly) for pattern detection
- **Timestamp format**: `MM/DD/YYYY, HH:MM AM/PM`
- **Value type**: Integer (will be converted if float)

---

## Quick Checklist

Before deployment:

- [ ] Contamination calibrated on historical data
- [ ] Valley threshold appropriate for metric volume
- [ ] Contiguous requirement reduces false positives adequately
- [ ] Sufficient history in data window (24+ points minimum)
- [ ] Severity-based alerting configured
- [ ] Return window set for desired timeline length
