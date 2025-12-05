<div align="center">

# GradientCast

### Enterprise-Grade AI for Time Series Intelligence

**Zero-shot forecasting and anomaly detection powered by foundation models**

[Get Started](#quick-start) | [Documentation](#documentation) | [Pricing](#pricing) | [Examples](examples/)

---

</div>

## What is GradientCast?

GradientCast delivers production-ready AI services for time series forecasting and anomaly detection. Our foundation model approach eliminates the traditional ML pipeline—no training data preparation, no model tuning, no infrastructure management. Connect to our API and get results in seconds.

| Capability | Service | Description |
|------------|---------|-------------|
| **Forecasting** | GradientCastFM | State-of-the-art 0-shot forecasting using transformer-based foundation models |
| **Anomaly Detection** | GradientCastPulseAD | Real-time deviation detection with configurable thresholds |
| **Pattern Analysis** | GradientCastDenseAD | Intelligent pattern-based anomaly detection with severity classification |

---

## Why GradientCast?

<table>
<tr>
<td width="33%" valign="top">

### Immediate Impact

No training required. No data labeling. No MLOps complexity. Pass your time series data and receive predictions immediately. Production-ready from day one.

</td>
<td width="33%" valign="top">

### Foundation Model Performance

Built on cutting-edge transformer architectures trained on billions of time series patterns. Achieves state-of-the-art accuracy across domains without domain-specific tuning.

</td>
<td width="33%" valign="top">

### Enterprise Scale

GPU-accelerated inference on Azure infrastructure. Auto-scaling from prototype to production. 99.9% uptime SLA for enterprise customers.

</td>
</tr>
</table>

---

## Quick Start

### Installation

```bash
pip install gradientcast
```

### Forecasting

```python
from gradientcast import GradientCastFM

fm = GradientCastFM(api_key="your-api-key")

result = fm.forecast(
    input_data={"revenue": [1200, 1350, 1280, 1420, 1380, 1510]},
    horizon_len=7,
    freq="D"
)

print(result["revenue"])  # [1545.2, 1572.8, 1598.4, ...]
```

### Anomaly Detection (PulseAD)

```python
from gradientcast import GradientCastPulseAD

ad = GradientCastPulseAD(api_key="your-api-key")

result = ad.detect({
    "metric": [
        {"timestamp": "01/01/2025, 12:00 PM", "value": 1500000},
        {"timestamp": "01/01/2025, 01:00 PM", "value": 1520000},
        {"timestamp": "01/01/2025, 02:00 PM", "value": 1480000},
        {"timestamp": "01/01/2025, 03:00 PM", "value": 800000},  # Anomaly
    ]
})

if result.has_anomaly:
    print(f"Alert: {result.anomalies[0].percent_delta} deviation detected")
```

### Pattern-Based Anomaly Detection (DenseAD)

```python
from gradientcast import GradientCastDenseAD
from datetime import datetime, timedelta

ad = GradientCastDenseAD(api_key="your-api-key")

# Generate 25 hourly data points (minimum required)
base = datetime(2025, 1, 1)
data = [
    {"timestamp": (base + timedelta(hours=i)).strftime("%m/%d/%Y, %I:%M %p"),
     "value": 3000000 + i * 10000}
    for i in range(25)
]
data[-1]["value"] = 500000  # Inject anomaly at the end

result = ad.detect(data)

if result.has_anomaly:
    print(f"Alert: {result.alert_severity} severity detected")
    for point in result.anomalies:
        print(f"  {point.datetime}: {point.actual_value}")
```

---

## Use Cases

| Industry | Application | GradientCast Service |
|----------|-------------|---------------------|
| **E-commerce** | Demand forecasting, inventory optimization | GradientCastFM |
| **Finance** | Revenue projection, cash flow prediction | GradientCastFM |
| **SaaS** | User growth forecasting, churn prediction | GradientCastFM |
| **Infrastructure** | Traffic anomaly detection, outage prediction | GradientCastPulseAD |
| **IoT** | Sensor anomaly detection, predictive maintenance | GradientCastDenseAD |
| **Security** | Behavioral anomaly detection, threat identification | GradientCastDenseAD |

---

## Documentation

### SDK Reference

- [Installation & Setup](#installation)
- [GradientCastFM](gradientcast/client.py) — Forecasting API
- [GradientCastPulseAD](gradientcast/client.py) — Deviation-based detection
- [GradientCastDenseAD](gradientcast/client.py) — Pattern-based detection
- [Error Handling](gradientcast/_exceptions.py)
- [Pandas Integration](gradientcast/_pandas.py)

### Tutorials

- [Quickstart](examples/quickstart.ipynb) — Get started in 5 minutes
- [Forecasting Basics](examples/forecasting/) — Single/multi-series, covariates, batch processing
- [PulseAD Guide](examples/anomaly_detection/pulseAD/) — Threshold configuration, simulation
- [DenseAD Guide](examples/anomaly_detection/densityAD/) — Severity tuning, pattern detection

---

## Technical Specifications

| Specification | Details |
|--------------|---------|
| **Infrastructure** | Azure ML managed endpoints, East US region |
| **Compute** | CPU (Intel Xeon) and GPU (NVIDIA A100) options |
| **Scaling** | Auto-scaling 2-10 instances based on demand |
| **Latency** | p50 < 500ms (CPU), p50 < 200ms (GPU) |
| **Timeout** | 180 seconds maximum request duration |
| **Concurrency** | 10-30 concurrent requests per instance |
| **Availability** | 99.9% SLA (Enterprise plans) |

### Supported Data Frequencies

| Code | Frequency |
|------|-----------|
| `H` | Hourly |
| `T` / `MIN` | Minute |
| `D` | Daily |
| `B` | Business day |
| `W` | Weekly |
| `M` | Monthly |
| `Q` | Quarterly |
| `Y` | Yearly |

---

## Requirements

- Python 3.8+
- `requests` >= 2.25.0
- `pandas` >= 1.3.0 (optional)

---

## Pricing

### Free Trial

Try GradientCast risk-free: **14 days, 5,000 API calls**, full access to all services.

[Start Free Trial](mailto:support@gradientcast.com?subject=Free%20Trial%20Request)

---

### GradientCastFM (Forecasting)

Seat-based pricing for data science and analytics teams.

<table>
<tr>
<th width="20%"></th>
<th width="20%">Starter</th>
<th width="20%">Team</th>
<th width="20%">Business</th>
<th width="20%">Enterprise</th>
</tr>
<tr>
<td><strong>Price</strong></td>
<td>$49/month</td>
<td>$39/seat/month</td>
<td>$29/seat/month</td>
<td>Custom</td>
</tr>
<tr>
<td><strong>Seats</strong></td>
<td>1</td>
<td>2 – 10</td>
<td>11 – 50</td>
<td>Unlimited</td>
</tr>
<tr>
<td><strong>API Calls</strong></td>
<td>10,000/month</td>
<td>10,000/seat/month</td>
<td>15,000/seat/month</td>
<td>Custom</td>
</tr>
<tr>
<td><strong>Compute</strong></td>
<td>CPU</td>
<td>CPU</td>
<td>CPU + GPU</td>
<td>Dedicated</td>
</tr>
<tr>
<td><strong>Support</strong></td>
<td>Community</td>
<td>Email</td>
<td>Priority</td>
<td>24/7 dedicated</td>
</tr>
<tr>
<td><strong>SLA</strong></td>
<td>—</td>
<td>99.5%</td>
<td>99.9%</td>
<td>99.99%</td>
</tr>
</table>

**Overage:** $0.003/call (CPU), $0.01/call (GPU)

**Examples:**
- Solo analyst: **$49/month**
- 5-person data team: 5 × $39 = **$195/month** (50K calls)
- 25-person org: 25 × $29 = **$725/month** (375K calls)

---

### GradientCastAD (Anomaly Detection)

Volume-based pricing for engineering teams and automated monitoring systems.

<table>
<tr>
<th width="20%"></th>
<th width="20%">Starter</th>
<th width="20%">Growth</th>
<th width="20%">Scale</th>
<th width="20%">Enterprise</th>
</tr>
<tr>
<td><strong>Price</strong></td>
<td>$99/month</td>
<td>$299/month</td>
<td>$799/month</td>
<td>Custom</td>
</tr>
<tr>
<td><strong>API Calls</strong></td>
<td>50,000</td>
<td>250,000</td>
<td>1,000,000</td>
<td>Custom</td>
</tr>
<tr>
<td><strong>Effective Rate</strong></td>
<td>$0.0020/call</td>
<td>$0.0012/call</td>
<td>$0.0008/call</td>
<td>Volume discounts</td>
</tr>
<tr>
<td><strong>Services</strong></td>
<td>PulseAD + DenseAD</td>
<td>PulseAD + DenseAD</td>
<td>PulseAD + DenseAD</td>
<td>All + dedicated</td>
</tr>
<tr>
<td><strong>Support</strong></td>
<td>Email</td>
<td>Priority</td>
<td>Priority</td>
<td>24/7 dedicated</td>
</tr>
<tr>
<td><strong>SLA</strong></td>
<td>99.5%</td>
<td>99.9%</td>
<td>99.9%</td>
<td>99.99%</td>
</tr>
</table>

**Overage:** $0.003/call (PulseAD), $0.002/call (DenseAD)

**Examples:**
- 100 metrics × hourly × 30 days = 72K calls → **Growth ($299/month)**
- 500 metrics × hourly × 30 days = 360K calls → **Scale ($799/month)**

---

### Bundles (FM + AD)

Save when you use both forecasting and anomaly detection.

| Bundle | Price | Includes | Savings |
|--------|-------|----------|---------|
| **Startup** | $129/month | FM Starter + AD Starter | 13% off |
| **Growth** | $499/month | FM Team (5 seats) + AD Growth | 16% off |
| **Enterprise** | Custom | Unlimited | Negotiated |

---

### Get Your API Key

To purchase a subscription or start a free trial:

**Email: [support@gradientcast.com](mailto:support@gradientcast.com)**

Include your preferred plan and expected usage. We typically respond within 24 hours.

---

## Contact

| Channel | Contact |
|---------|---------|
| **Sales & Subscriptions** | [support@gradientcast.com](mailto:support@gradientcast.com) |
| **Technical Support** | [support@gradientcast.com](mailto:support@gradientcast.com) |
| **GitHub Issues** | [Open an issue](https://github.com/GradientCast/gradientcast/issues) |

---

<div align="center">

**GradientCast** — Time Series Intelligence, Simplified

[Get Your API Key](mailto:support@gradientcast.com) | [View Examples](examples/) | [Read the Docs](#documentation)

</div>
