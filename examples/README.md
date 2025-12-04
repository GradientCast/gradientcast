# GradientCast Examples

Tutorials and examples for time series forecasting and anomaly detection.

## Quick Start

```bash
pip install gradientcast
```

Open [quickstart.ipynb](quickstart.ipynb) to run your first forecast.

---

## Folder Structure

```
examples/
├── quickstart.ipynb              # Start here
├── utils/
│   └── synthetic_data.py         # Data generation utilities
├── forecasting/
│   ├── 01_basics.ipynb           # Core forecasting concepts
│   ├── 02_covariates.ipynb       # Using external variables
│   ├── 03_batch_forecasting.ipynb # Multi-series forecasting
│   └── tuning_guide.md           # Parameter reference
└── anomaly_detection/
    ├── pulseAD/                  # Threshold-based detection
    │   ├── 01_quickstart.ipynb
    │   ├── 02_tuning.ipynb
    │   ├── 03_simulation.ipynb
    │   └── tuning_guide.md
    └── densityAD/                # Pattern-based detection
        ├── 01_quickstart.ipynb
        ├── 02_tuning.ipynb
        ├── 03_simulation.ipynb
        └── tuning_guide.md
```

---

## Forecasting

**GradientCastFM** - Time series forecasting with foundation models.

| Notebook | Description |
|----------|-------------|
| [01_basics.ipynb](forecasting/01_basics.ipynb) | Single/multi-series forecasting, frequencies, response structure |
| [02_covariates.ipynb](forecasting/02_covariates.ipynb) | Improve accuracy with external variables |
| [03_batch_forecasting.ipynb](forecasting/03_batch_forecasting.ipynb) | Performance optimization for production |
| [tuning_guide.md](forecasting/tuning_guide.md) | Parameter reference |

---

## Anomaly Detection

Both anomaly detection methods require historical data as context but evaluate only the most recent data point(s) for anomalies. For real-time monitoring, pass a sliding window of historical data with each new data point appended at the end.

### PulseAD (Deviation-Based)

**GradientCastPulseAD** - Detects significant deviations from expected behavior.

| Notebook | Description |
|----------|-------------|
| [01_quickstart.ipynb](anomaly_detection/pulseAD/01_quickstart.ipynb) | Basic detection, response structure, visualization |
| [02_tuning.ipynb](anomaly_detection/pulseAD/02_tuning.ipynb) | Threshold configuration, per-dimension overrides |
| [03_simulation.ipynb](anomaly_detection/pulseAD/03_simulation.ipynb) | Real-time simulation with visualization |
| [tuning_guide.md](anomaly_detection/pulseAD/tuning_guide.md) | Threshold reference |

**Best for:** Regular patterns, sudden drops or spikes, threshold-based alerting

### DensityAD (Pattern-Based)

**GradientCastDenseAD** - Pattern detection with severity classification.

| Notebook | Description |
|----------|-------------|
| [01_quickstart.ipynb](anomaly_detection/densityAD/01_quickstart.ipynb) | Pattern detection, severity levels, magnitude metrics |
| [02_tuning.ipynb](anomaly_detection/densityAD/02_tuning.ipynb) | Contamination, neighbors, filtering parameters |
| [03_simulation.ipynb](anomaly_detection/densityAD/03_simulation.ipynb) | Real-time simulation with severity visualization |
| [tuning_guide.md](anomaly_detection/densityAD/tuning_guide.md) | Detection parameter reference |

**Best for:** Complex patterns, severity-based alerting, multi-feature analysis

---

## API Key Configuration

Replace `"your-api-key-here"` in the notebooks with your GradientCast API key.

```python
GRADIENTCAST_API_KEY = "your-api-key-here"
```

---

## Choosing the Right Tool

| Need | Tool | Description |
|------|------|-------------|
| Predict future values | GradientCastFM | Foundation model forecasting |
| Detect significant deviations | GradientCastPulseAD | Dual-threshold detection |
| Detect pattern anomalies | GradientCastDenseAD | Pattern analysis with severity |

---

## Requirements

- Python 3.8+
- gradientcast
- matplotlib (for visualizations)
- pandas (optional, for DataFrame support)
- pillow (optional, for GIF export)

```bash
pip install gradientcast matplotlib pandas pillow
```

---

## Resources

- [Documentation](https://docs.gradientcast.ai)
- [API Reference](https://docs.gradientcast.ai/api)
- [Support](mailto:support@gradientcast.ai)
