"""
Synthetic Data Generation Utilities for GradientCast Examples.

This module provides functions to generate realistic time series data
for testing and demonstrating GradientCast forecasting and anomaly detection.
"""

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Union


def generate_trend_series(
    n_points: int,
    trend_type: str = 'linear',
    base_value: float = 100.0,
    trend_strength: float = 1.0,
    noise_level: float = 0.1
) -> List[float]:
    """
    Generate a time series with a specified trend pattern.

    Args:
        n_points: Number of data points to generate
        trend_type: Type of trend ('linear', 'exponential', 'logarithmic', 'flat')
        base_value: Starting value of the series
        trend_strength: Multiplier for trend magnitude
        noise_level: Standard deviation of noise as fraction of base_value

    Returns:
        List of float values representing the time series
    """
    t = np.arange(n_points)

    if trend_type == 'linear':
        trend = base_value + trend_strength * t
    elif trend_type == 'exponential':
        trend = base_value * (1 + 0.01 * trend_strength) ** t
    elif trend_type == 'logarithmic':
        trend = base_value + trend_strength * 10 * np.log1p(t)
    else:  # flat
        trend = np.full(n_points, base_value)

    noise = np.random.normal(0, base_value * noise_level, n_points)
    return (trend + noise).tolist()


def generate_seasonal_series(
    n_points: int,
    base_value: float = 100.0,
    seasonality: str = 'weekly',
    amplitude: float = 0.2,
    noise_level: float = 0.05
) -> List[float]:
    """
    Generate a time series with seasonal patterns.

    Args:
        n_points: Number of data points to generate
        base_value: Mean value of the series
        seasonality: Type of seasonality ('hourly', 'daily', 'weekly', 'monthly', 'yearly')
        amplitude: Amplitude of seasonal component as fraction of base_value
        noise_level: Standard deviation of noise as fraction of base_value

    Returns:
        List of float values representing the time series
    """
    t = np.arange(n_points)

    period_map = {
        'hourly': 24,
        'daily': 7,
        'weekly': 52,
        'monthly': 12,
        'yearly': 1
    }
    period = period_map.get(seasonality, 7)

    seasonal = base_value * amplitude * np.sin(2 * np.pi * t / period)
    noise = np.random.normal(0, base_value * noise_level, n_points)

    return (base_value + seasonal + noise).tolist()


def generate_trend_seasonal_series(
    n_points: int,
    base_value: float = 100.0,
    trend_strength: float = 0.5,
    seasonal_period: int = 7,
    seasonal_amplitude: float = 0.2,
    noise_level: float = 0.05
) -> List[float]:
    """
    Generate a time series with both trend and seasonal components.

    Args:
        n_points: Number of data points
        base_value: Starting value
        trend_strength: Linear trend per point
        seasonal_period: Period of seasonal cycle
        seasonal_amplitude: Amplitude as fraction of base_value
        noise_level: Noise as fraction of base_value

    Returns:
        List of float values
    """
    t = np.arange(n_points)

    trend = base_value + trend_strength * t
    seasonal = base_value * seasonal_amplitude * np.sin(2 * np.pi * t / seasonal_period)
    noise = np.random.normal(0, base_value * noise_level, n_points)

    return (trend + seasonal + noise).tolist()


def generate_multivariate_series(
    n_series: int,
    n_points: int,
    base_values: Optional[List[float]] = None,
    correlation: float = 0.5,
    noise_level: float = 0.1
) -> Dict[str, List[float]]:
    """
    Generate multiple correlated time series.

    Args:
        n_series: Number of series to generate
        n_points: Number of points per series
        base_values: Optional list of base values for each series
        correlation: Correlation coefficient between series (0 to 1)
        noise_level: Noise level as fraction of base values

    Returns:
        Dictionary mapping series names to their values
    """
    if base_values is None:
        base_values = [100.0 + i * 50 for i in range(n_series)]

    # Generate correlated random components
    common_component = np.random.randn(n_points)

    series_dict = {}
    for i in range(n_series):
        base = base_values[i] if i < len(base_values) else 100.0

        # Mix of common and individual components
        individual = np.random.randn(n_points)
        combined = correlation * common_component + np.sqrt(1 - correlation**2) * individual

        # Add trend and scale
        trend = np.linspace(0, base * 0.3, n_points)
        values = base + trend + combined * base * noise_level

        series_dict[f"series_{i}"] = values.tolist()

    return series_dict


def generate_anomaly_series(
    n_points: int,
    base_value: float = 1000000.0,
    anomaly_indices: Optional[List[int]] = None,
    anomaly_magnitude: float = 0.5,
    anomaly_direction: str = 'both',
    noise_level: float = 0.05
) -> Tuple[List[float], List[bool]]:
    """
    Generate a time series with injected anomalies.

    Args:
        n_points: Number of data points
        base_value: Base value of the series
        anomaly_indices: Indices where anomalies should occur (random if None)
        anomaly_magnitude: Size of anomaly as fraction of base_value
        anomaly_direction: Direction of anomalies ('up', 'down', 'both')
        noise_level: Noise level as fraction of base_value

    Returns:
        Tuple of (values list, anomaly flags list)
    """
    # Generate base series with slight trend
    t = np.arange(n_points)
    trend = base_value + 0.001 * base_value * t
    noise = np.random.normal(0, base_value * noise_level, n_points)
    values = trend + noise

    # Create anomaly mask
    anomaly_flags = [False] * n_points

    if anomaly_indices is None:
        # Randomly select ~5% of points as anomalies
        n_anomalies = max(1, int(n_points * 0.05))
        anomaly_indices = np.random.choice(n_points, n_anomalies, replace=False).tolist()

    for idx in anomaly_indices:
        if 0 <= idx < n_points:
            if anomaly_direction == 'up':
                sign = 1
            elif anomaly_direction == 'down':
                sign = -1
            else:
                sign = np.random.choice([-1, 1])

            values[idx] += sign * base_value * anomaly_magnitude
            anomaly_flags[idx] = True

    return values.tolist(), anomaly_flags


def generate_timestamps(
    n_points: int,
    start_date: Optional[datetime] = None,
    freq: str = 'H'
) -> List[str]:
    """
    Generate a list of timestamp strings.

    Args:
        n_points: Number of timestamps
        start_date: Starting datetime (defaults to 30 days ago)
        freq: Frequency ('H' for hourly, 'D' for daily, 'M' for monthly)

    Returns:
        List of formatted timestamp strings
    """
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)

    freq_delta = {
        'H': timedelta(hours=1),
        'D': timedelta(days=1),
        'W': timedelta(weeks=1),
        'M': timedelta(days=30),
    }
    delta = freq_delta.get(freq, timedelta(hours=1))

    timestamps = []
    for i in range(n_points):
        dt = start_date + i * delta
        timestamps.append(dt.strftime("%m/%d/%Y, %I:%M %p"))

    return timestamps


def generate_ad_payload_data(
    n_points: int,
    base_value: float = 1500000.0,
    inject_anomalies: bool = True,
    anomaly_ratio: float = 0.05
) -> List[Dict[str, Union[str, int]]]:
    """
    Generate data in the format expected by GradientCast AD endpoints.

    Args:
        n_points: Number of data points
        base_value: Base value for the series
        inject_anomalies: Whether to inject anomalies
        anomaly_ratio: Fraction of points to make anomalous

    Returns:
        List of dicts with 'timestamp' and 'value' keys
    """
    timestamps = generate_timestamps(n_points, freq='H')

    if inject_anomalies:
        n_anomalies = max(1, int(n_points * anomaly_ratio))
        anomaly_indices = np.random.choice(
            range(n_points // 2, n_points),  # Anomalies in second half
            n_anomalies,
            replace=False
        ).tolist()
        values, _ = generate_anomaly_series(
            n_points, base_value, anomaly_indices,
            anomaly_magnitude=0.4, noise_level=0.03
        )
    else:
        values, _ = generate_anomaly_series(
            n_points, base_value, anomaly_indices=[], noise_level=0.03
        )

    return [
        {"timestamp": ts, "value": int(v)}
        for ts, v in zip(timestamps, values)
    ]


def generate_covariates(
    n_points: int,
    series_ids: List[str],
    include_horizon: bool = True,
    horizon_len: int = 7
) -> Dict[str, Dict[str, Dict[str, Union[List, float, str]]]]:
    """
    Generate sample covariates for forecasting with covariates.

    Args:
        n_points: Number of historical data points
        series_ids: List of series identifiers
        include_horizon: Whether to extend dynamic covariates for forecast horizon
        horizon_len: Length of forecast horizon

    Returns:
        Dictionary with covariate structures for the SDK
    """
    total_len = n_points + horizon_len if include_horizon else n_points

    # Static numerical covariates
    static_numerical = {
        "base_price": {sid: 100.0 + i * 50 for i, sid in enumerate(series_ids)}
    }

    # Static categorical covariates
    categories = ["electronics", "clothing", "food", "home"]
    static_categorical = {
        "category": {sid: categories[i % len(categories)] for i, sid in enumerate(series_ids)}
    }

    # Dynamic numerical covariates (e.g., temperature)
    dynamic_numerical = {
        "temperature": {
            sid: [20 + 10 * np.sin(2 * np.pi * t / 24) + np.random.normal(0, 2)
                  for t in range(total_len)]
            for sid in series_ids
        }
    }

    # Dynamic categorical covariates (e.g., day of week)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dynamic_categorical = {
        "day_of_week": {
            sid: [days[t % 7] for t in range(total_len)]
            for sid in series_ids
        }
    }

    return {
        "static_numerical_covariates": static_numerical,
        "static_categorical_covariates": static_categorical,
        "dynamic_numerical_covariates": dynamic_numerical,
        "dynamic_categorical_covariates": dynamic_categorical
    }


def generate_electricity_like_data(
    n_days: int = 90,
    countries: List[str] = None
) -> Tuple[Dict[str, List[float]], Dict[str, Dict]]:
    """
    Generate electricity-price-like data similar to the covariates example.

    Args:
        n_days: Number of days of hourly data
        countries: List of country codes (defaults to ["FR", "BE"])

    Returns:
        Tuple of (price data dict, covariates dict)
    """
    if countries is None:
        countries = ["FR", "BE"]

    n_points = n_days * 24  # Hourly data

    prices = {}
    for country in countries:
        base = 50 if country == "FR" else 55

        # Daily pattern (higher during day)
        hourly = np.tile([
            0.8, 0.7, 0.7, 0.7, 0.8, 0.9,  # 0-5
            1.0, 1.2, 1.3, 1.2, 1.1, 1.0,  # 6-11
            1.0, 1.1, 1.1, 1.2, 1.3, 1.4,  # 12-17
            1.3, 1.2, 1.1, 1.0, 0.9, 0.8   # 18-23
        ], n_days)

        # Weekly pattern (lower on weekends)
        weekly = np.array([1.0 if (i // 24) % 7 < 5 else 0.85 for i in range(n_points)])

        # Trend
        trend = np.linspace(0, 5, n_points)

        # Noise
        noise = np.random.normal(0, 3, n_points)

        prices[country] = (base * hourly * weekly + trend + noise).tolist()

    # Generate matching covariates
    covariates = generate_covariates(n_points, countries, include_horizon=True, horizon_len=24)

    # Add generation forecast as dynamic covariate
    covariates["dynamic_numerical_covariates"]["gen_forecast"] = {
        country: [5000 + 2000 * np.sin(2 * np.pi * t / 24) + np.random.normal(0, 200)
                  for t in range(n_points + 24)]
        for country in countries
    }

    return prices, covariates
