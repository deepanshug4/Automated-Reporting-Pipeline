"""
Transform step: turn raw rows into business metrics. This is where the
'analytics' lives — the numbers a stakeholder actually wants.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["units"] = pd.to_numeric(df["units"], errors="coerce")
    df["period"] = df["date"].dt.to_period("M").astype(str)

    total_revenue = df["revenue"].sum()
    total_units = df["units"].sum()

    by_period = (df.groupby("period")
                   .agg(revenue=("revenue", "sum"),
                        units=("units", "sum"))
                   .reset_index()
                   .sort_values("period"))

    by_region = (df.groupby("region")
                   .agg(revenue=("revenue", "sum"))
                   .reset_index()
                   .sort_values("revenue", ascending=False))

    by_product = (df.groupby("product")
                    .agg(revenue=("revenue", "sum"),
                         units=("units", "sum"))
                    .reset_index()
                    .sort_values("revenue", ascending=False))

    # Period-over-period revenue change (for alerting).
    pct_change = None
    if len(by_period) >= 2:
        last = by_period.iloc[-1]["revenue"]
        prev = by_period.iloc[-2]["revenue"]
        if prev:
            pct_change = (last - prev) / prev * 100

    logger.info("Transform complete: $%.2f revenue across %d periods.",
                total_revenue, len(by_period))

    return {
        "total_revenue": float(total_revenue),
        "total_units": int(total_units),
        "by_period": by_period,
        "by_region": by_region,
        "by_product": by_product,
        "latest_pct_change": pct_change,
    }