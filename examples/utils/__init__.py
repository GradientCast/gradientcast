"""Utility functions for GradientCast examples."""

from .synthetic_data import (
    generate_trend_series,
    generate_seasonal_series,
    generate_trend_seasonal_series,
    generate_multivariate_series,
    generate_anomaly_series,
    generate_timestamps,
    generate_ad_payload_data,
    generate_covariates,
    generate_electricity_like_data,
)

__all__ = [
    "generate_trend_series",
    "generate_seasonal_series",
    "generate_trend_seasonal_series",
    "generate_multivariate_series",
    "generate_anomaly_series",
    "generate_timestamps",
    "generate_ad_payload_data",
    "generate_covariates",
    "generate_electricity_like_data",
]
