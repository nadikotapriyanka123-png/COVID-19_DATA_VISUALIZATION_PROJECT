"""
Module 5: Regional / Country-wise Analysis
Compares COVID-19 statistics across different regions and countries.
"""

import pandas as pd
import numpy as np


def top_countries_by_confirmed(country_df, top_n=10):
    """Get top N countries by total confirmed cases."""
    latest_date = country_df["Date"].max()
    latest = country_df[country_df["Date"] == latest_date]

    top = (
        latest.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered"]]
        .sum()
        .sort_values("Confirmed", ascending=False)
        .head(top_n)
    )
    top["Mortality_Rate"] = (top["Deaths"] / top["Confirmed"] * 100).round(2)
    top["Recovery_Rate"] = (top["Recovered"] / top["Confirmed"] * 100).round(2)

    print(f"\n--- Top {top_n} Countries by Confirmed Cases ---")
    print(top)
    return top


def top_countries_by_deaths(country_df, top_n=10):
    """Get top N countries by total deaths."""
    latest_date = country_df["Date"].max()
    latest = country_df[country_df["Date"] == latest_date]

    top = (
        latest.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered"]]
        .sum()
        .sort_values("Deaths", ascending=False)
        .head(top_n)
    )
    top["Mortality_Rate"] = (top["Deaths"] / top["Confirmed"] * 100).round(2)

    print(f"\n--- Top {top_n} Countries by Deaths ---")
    print(top)
    return top


def top_countries_by_recovery_rate(country_df, min_cases=10000, top_n=10):
    """Get top N countries with highest recovery rate (minimum confirmed cases)."""
    latest_date = country_df["Date"].max()
    latest = country_df[country_df["Date"] == latest_date]

    filtered = latest[latest["Confirmed"] >= min_cases].copy()
    filtered["Recovery_Rate"] = (filtered["Recovered"] / filtered["Confirmed"] * 100)

    top = (
        filtered.groupby("Country/Region")[["Confirmed", "Recovered", "Recovery_Rate"]]
        .sum()
        .sort_values("Recovery_Rate", ascending=False)
        .head(top_n)
    )

    print(f"\n--- Top {top_n} Countries by Recovery Rate (min {min_cases:,} cases) ---")
    print(top)
    return top


def top_countries_by_mortality_rate(country_df, min_cases=10000, top_n=10):
    """Get top N countries with highest mortality rate."""
    latest_date = country_df["Date"].max()
    latest = country_df[country_df["Date"] == latest_date]

    filtered = latest[latest["Confirmed"] >= min_cases].copy()
    filtered["Mortality_Rate"] = (filtered["Deaths"] / filtered["Confirmed"] * 100)

    top = (
        filtered.groupby("Country/Region")[["Confirmed", "Deaths", "Mortality_Rate"]]
        .sum()
        .sort_values("Mortality_Rate", ascending=False)
        .head(top_n)
    )

    print(f"\n--- Top {top_n} Countries by Mortality Rate (min {min_cases:,} cases) ---")
    print(top)
    return top


def compare_countries(country_df, countries):
    """Compare specific countries side by side."""
    print(f"\n--- Comparing: {', '.join(countries)} ---")

    comparison_data = country_df[country_df["Country/Region"].isin(countries)]
    latest_date = country_df["Date"].max()
    latest = comparison_data[comparison_data["Date"] == latest_date]

    result = (
        latest.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered"]]
        .sum()
        .sort_values("Confirmed", ascending=False)
    )
    result["Mortality_Rate"] = (result["Deaths"] / result["Confirmed"] * 100).round(2)
    result["Recovery_Rate"] = (result["Recovered"] / result["Confirmed"] * 100).round(2)

    print(result)
    return result


def trend_comparison(country_df, countries, column="Confirmed"):
    """Compare trends over time for specific countries."""
    filtered = country_df[country_df["Country/Region"].isin(countries)]
    pivot = filtered.pivot_table(
        index="Date",
        columns="Country/Region",
        values=column,
        aggfunc="sum",
    )
    print(f"\n--- {column} Trend Comparison ---")
    print(f"Countries: {countries}")
    print(pivot.tail(10))
    return pivot


def daily_new_cases_comparison(country_df, countries):
    """Compare daily new cases for specific countries."""
    filtered = country_df[country_df["Country/Region"].isin(countries)]
    pivot = filtered.pivot_table(
        index="Date",
        columns="Country/Region",
        values="Daily_Confirmed",
        aggfunc="sum",
    )
    print(f"\n--- Daily New Cases Comparison ---")
    print(f"Countries: {countries}")
    print(pivot.tail(10))
    return pivot


def continental_analysis(country_df):
    """Analyze trends by continent/region (using Country/Region grouping)."""
    print("\n--- Country/Region Summary ---")

    summary = (
        country_df.groupby("Country/Region")
        .agg({
            "Confirmed": "max",
            "Deaths": "max",
            "Recovered": "max",
        })
        .sort_values("Confirmed", ascending=False)
    )

    total_countries = len(summary)
    total_confirmed = summary["Confirmed"].sum()
    total_deaths = summary["Deaths"].sum()
    total_recovered = summary["Recovered"].sum()

    print(f"  Total Countries/Territories: {total_countries}")
    print(f"  Global Confirmed: {total_confirmed:,.0f}")
    print(f"  Global Deaths: {total_deaths:,.0f}")
    print(f"  Global Recovered: {total_recovered:,.0f}")
    print(f"  Global Mortality Rate: {total_deaths/total_confirmed*100:.2f}%")

    return summary


def run_regional_analysis(country_df):
    """Run complete regional analysis pipeline."""
    print("\n" + "=" * 60)
    print("REGIONAL / COUNTRY-WISE ANALYSIS")
    print("=" * 60)

    top_confirmed = top_countries_by_confirmed(country_df)
    top_deaths = top_countries_by_deaths(country_df)
    top_recovery = top_countries_by_recovery_rate(country_df)
    top_mortality = top_countries_by_mortality_rate(country_df)
    global_summary = continental_analysis(country_df)

    print("\n[REGIONAL] Analysis complete.")
    return {
        "top_confirmed": top_confirmed,
        "top_deaths": top_deaths,
        "top_recovery_rate": top_recovery,
        "top_mortality_rate": top_mortality,
        "global_summary": global_summary,
    }


if __name__ == "__main__":
    from data_collection import load_all
    from data_preprocessing import preprocess_pipeline

    frames = load_all()
    if len(frames) == 3:
        merged, country_df = preprocess_pipeline(
            frames["confirmed"], frames["deaths"], frames["recovered"]
        )
        results = run_regional_analysis(country_df)
