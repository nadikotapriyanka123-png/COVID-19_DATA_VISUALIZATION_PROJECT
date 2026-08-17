"""
Module 4: COVID-19 Trend Analysis
Analyzes confirmed cases, deaths, and recoveries over time.
"""

import pandas as pd
import numpy as np


def global_daily_trends(country_df):
    """Calculate global daily trends by aggregating all countries."""
    print("\n--- Global Daily Trends ---")

    global_daily = (
        country_df.groupby("Date")
        .agg({
            "Confirmed": "sum",
            "Deaths": "sum",
            "Recovered": "sum",
        })
        .reset_index()
    )

    global_daily["Daily_Confirmed"] = global_daily["Confirmed"].diff().fillna(0).clip(lower=0)
    global_daily["Daily_Deaths"] = global_daily["Deaths"].diff().fillna(0).clip(lower=0)
    global_daily["Daily_Recovered"] = global_daily["Recovered"].diff().fillna(0).clip(lower=0)

    global_daily["Mortality_Rate"] = np.where(
        global_daily["Confirmed"] > 0,
        (global_daily["Deaths"] / global_daily["Confirmed"]) * 100,
        0,
    )
    global_daily["Recovery_Rate"] = np.where(
        global_daily["Confirmed"] > 0,
        (global_daily["Recovered"] / global_daily["Confirmed"]) * 100,
        0,
    )

    print(f"  Date Range: {global_daily['Date'].min().date()} to {global_daily['Date'].max().date()}")
    print(f"  Total Confirmed: {global_daily['Confirmed'].iloc[-1]:,.0f}")
    print(f"  Total Deaths:    {global_daily['Deaths'].iloc[-1]:,.0f}")
    print(f"  Total Recovered: {global_daily['Recovered'].iloc[-1]:,.0f}")

    return global_daily


def weekly_trends(country_df):
    """Calculate weekly aggregated trends."""
    print("\n--- Weekly Trends ---")

    df = country_df.copy()
    df["Week"] = df["Date"].dt.to_period("W")

    weekly = (
        df.groupby("Week")
        .agg({
            "Daily_Confirmed": "sum",
            "Daily_Deaths": "sum",
            "Daily_Recovered": "sum",
        })
        .reset_index()
    )

    weekly["Week_Start"] = weekly["Week"].dt.start_time

    print(f"  Total Weeks: {len(weekly)}")
    print(f"  Peak Week (Confirmed): {weekly.loc[weekly['Daily_Confirmed'].idxmax(), 'Week']}")
    print(f"  Peak Weekly Cases: {weekly['Daily_Confirmed'].max():,.0f}")

    return weekly


def monthly_trends(country_df):
    """Calculate monthly aggregated trends."""
    print("\n--- Monthly Trends ---")

    df = country_df.copy()
    df["Month"] = df["Date"].dt.to_period("M")

    monthly = (
        df.groupby("Month")
        .agg({
            "Confirmed": "last",
            "Deaths": "last",
            "Recovered": "last",
            "Daily_Confirmed": "sum",
            "Daily_Deaths": "sum",
            "Daily_Recovered": "sum",
        })
        .reset_index()
    )

    monthly["Month_Start"] = monthly["Month"].dt.start_time
    monthly["Mortality_Rate"] = np.where(
        monthly["Confirmed"] > 0,
        (monthly["Deaths"] / monthly["Confirmed"]) * 100,
        0,
    )

    print(f"  Total Months: {len(monthly)}")
    print(f"  Peak Month (Confirmed): {monthly.loc[monthly['Daily_Confirmed'].idxmax(), 'Month']}")
    print(f"  Peak Monthly Cases: {monthly['Daily_Confirmed'].max():,.0f}")

    return monthly


def growth_rate_analysis(global_daily):
    """Analyze growth rates of confirmed cases."""
    print("\n--- Growth Rate Analysis ---")

    df = global_daily.copy()
    df["Growth_Rate"] = df["Confirmed"].pct_change() * 100
    df["Growth_Rate"] = df["Growth_Rate"].replace([np.inf, -np.inf], 0).fillna(0)

    avg_growth = df["Growth_Rate"].mean()
    max_growth = df["Growth_Rate"].max()
    max_growth_date = df.loc[df["Growth_Rate"].idxmax(), "Date"]

    print(f"  Average Daily Growth Rate: {avg_growth:.2f}%")
    print(f"  Maximum Daily Growth Rate: {max_growth:.2f}%")
    print(f"  Date of Max Growth:        {max_growth_date.date()}")

    return df


def doubling_time_analysis(global_daily):
    """Calculate estimated doubling time of cases."""
    print("\n--- Doubling Time Analysis ---")

    df = global_daily.copy()
    df["Daily_Growth"] = df["Confirmed"].pct_change().replace([np.inf, -np.inf], 0).fillna(0)

    df["Doubling_Time"] = np.where(
        df["Daily_Growth"] > 0,
        np.log(2) / np.log(1 + df["Daily_Growth"]),
        np.nan,
    )

    avg_doubling = df["Doubling_Time"].mean()
    print(f"  Average Doubling Time: {avg_doubling:.1f} days")

    return df


def run_trend_analysis(country_df):
    """Run complete trend analysis pipeline."""
    print("\n" + "=" * 60)
    print("TREND ANALYSIS")
    print("=" * 60)

    global_daily = global_daily_trends(country_df)
    weekly = weekly_trends(country_df)
    monthly = monthly_trends(country_df)
    growth = growth_rate_analysis(global_daily)
    doubling = doubling_time_analysis(global_daily)

    print("\n[TREND] Analysis complete.")
    return {
        "global_daily": global_daily,
        "weekly": weekly,
        "monthly": monthly,
        "growth": growth,
        "doubling": doubling,
    }


if __name__ == "__main__":
    from data_collection import load_all
    from data_preprocessing import preprocess_pipeline

    frames = load_all()
    if len(frames) == 3:
        merged, country_df = preprocess_pipeline(
            frames["confirmed"], frames["deaths"], frames["recovered"]
        )
        results = run_trend_analysis(country_df)
