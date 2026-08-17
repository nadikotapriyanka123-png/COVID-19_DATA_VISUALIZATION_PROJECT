"""
Module 3: Exploratory Data Analysis (EDA)
Statistical analysis and summary of COVID-19 data.
"""

import pandas as pd
import numpy as np


def dataset_overview(df, name="DataFrame"):
    """Print comprehensive overview of the dataset."""
    print("\n" + "=" * 60)
    print(f"EXPLORATORY DATA ANALYSIS: {name}")
    print("=" * 60)

    print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nData Types:\n{df.dtypes}")

    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nTotal Missing: {df.isnull().sum().sum()}")

    print(f"\nDuplicate Rows: {df.duplicated().sum()}")

    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes,
        "missing": df.isnull().sum().sum(),
        "duplicates": df.duplicated().sum(),
    }


def statistical_summary(df):
    """Generate statistical summary for numeric columns."""
    print("\n--- Statistical Summary ---")
    numeric_df = df.select_dtypes(include=[np.number])
    summary = numeric_df.describe()
    print(summary)
    return summary


def time_range_info(df):
    """Display information about the date range in the dataset."""
    if "Date" in df.columns:
        print(f"\n--- Time Range ---")
        print(f"Start Date: {df['Date'].min()}")
        print(f"End Date:   {df['Date'].max()}")
        print(f"Total Days: {(df['Date'].max() - df['Date'].min()).days}")
    else:
        print("[WARNING] 'Date' column not found.")


def country_summary(df, top_n=10):
    """Display summary statistics for top countries."""
    if "Country/Region" not in df.columns:
        print("[WARNING] 'Country/Region' column not found.")
        return None

    latest_date = df["Date"].max()
    latest_data = df[df["Date"] == latest_date]

    country_stats = (
        latest_data.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered"]]
        .sum()
        .sort_values("Confirmed", ascending=False)
    )

    print(f"\n--- Top {top_n} Countries (as of {latest_date.date()}) ---")
    print(country_stats.head(top_n))

    print(f"\n--- Bottom 5 Countries ---")
    print(country_stats.tail(5))

    return country_stats


def correlation_analysis(df):
    """Analyze correlations between numeric variables."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        print("[WARNING] Not enough numeric columns for correlation analysis.")
        return None

    corr_matrix = df[numeric_cols].corr()
    print("\n--- Correlation Matrix ---")
    print(corr_matrix)
    return corr_matrix


def distribution_analysis(df):
    """Analyze distribution of key columns."""
    print("\n--- Distribution Analysis ---")

    for col in ["Confirmed", "Deaths", "Recovered"]:
        if col in df.columns:
            print(f"\n{col}:")
            print(f"  Mean:   {df[col].mean():.2f}")
            print(f"  Median: {df[col].median():.2f}")
            print(f"  Std:    {df[col].std():.2f}")
            print(f"  Min:    {df[col].min():.2f}")
            print(f"  Max:    {df[col].max():.2f}")
            print(f"  Skew:   {df[col].skew():.2f}")


def run_eda(df, country_df=None):
    """Run complete EDA pipeline."""
    overview = dataset_overview(df, "Merged COVID-19 Data")
    statistical_summary(df)
    time_range_info(df)
    country_stats = country_summary(country_df if country_df is not None else df)
    correlation_analysis(df)
    distribution_analysis(df)

    print("\n[EDA] Analysis complete.")
    return overview, country_stats


if __name__ == "__main__":
    from data_collection import load_all
    from data_preprocessing import preprocess_pipeline

    frames = load_all()
    if len(frames) == 3:
        merged, country_df = preprocess_pipeline(
            frames["confirmed"], frames["deaths"], frames["recovered"]
        )
        run_eda(merged, country_df)
