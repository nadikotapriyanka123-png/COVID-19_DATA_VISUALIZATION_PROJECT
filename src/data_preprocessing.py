"""
Module 2: Data Preprocessing
Cleans and transforms raw COVID-19 data into analysis-ready format.
"""

import pandas as pd
import numpy as np


def check_missing_values(df, name="DataFrame"):
    """Report missing values in the dataset."""
    missing = df.isnull().sum()
    total_missing = missing.sum()
    print(f"[{name}] Missing values: {total_missing}")
    if total_missing > 0:
        cols_with_missing = missing[missing > 0]
        for col, count in cols_with_missing.items():
            print(f"  - {col}: {count} ({count/len(df)*100:.1f}%)")
    return total_missing


def check_duplicates(df, name="DataFrame"):
    """Check and report duplicate rows."""
    dup_count = df.duplicated().sum()
    print(f"[{name}] Duplicate rows: {dup_count}")
    return dup_count


def melt_time_series(df, value_name="Count"):
    """
    Convert wide-format time series to long format.
    JHU datasets have dates as columns; this melts them into rows.
    """
    id_cols = ["Province/State", "Country/Region", "Lat", "Long"]
    existing_id_cols = [col for col in id_cols if col in df.columns]

    melted = df.melt(
        id_vars=existing_id_cols,
        var_name="Date",
        value_name=value_name,
    )
    melted["Date"] = pd.to_datetime(melted["Date"], format="%m/%d/%y")
    print(f"[PREPROCESS] Melted to long format: {melted.shape[0]} rows")
    return melted


def merge_datasets(confirmed, deaths, recovered):
    """
    Merge confirmed, deaths, and recovered datasets into a single DataFrame.
    Returns a merged DataFrame in long format with separate count columns.
    """
    print("[PREPROCESS] Merging datasets...")

    c = melt_time_series(confirmed, value_name="Confirmed")
    d = melt_time_series(deaths, value_name="Deaths")
    r = melt_time_series(recovered, value_name="Recovered")

    id_cols = ["Province/State", "Country/Region", "Lat", "Long", "Date"]

    merged = c.merge(d, on=id_cols, how="outer")
    merged = merged.merge(r, on=id_cols, how="outer")

    merged.sort_values(by=["Country/Region", "Date"], inplace=True)
    merged.reset_index(drop=True, inplace=True)

    print(f"[PREPROCESS] Merged shape: {merged.shape}")
    return merged


def fill_missing(df, method="ffill"):
    """Fill missing values using forward fill or zero fill."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if method == "ffill":
        df[numeric_cols] = df[numeric_cols].ffill()
    df[numeric_cols] = df[numeric_cols].fillna(0)
    print(f"[PREPROCESS] Filled missing values using '{method}'")
    return df


def add_daily_columns(df):
    """Add columns for daily new cases, deaths, and recoveries."""
    df = df.sort_values(["Country/Region", "Date"]).copy()

    for col in ["Confirmed", "Deaths", "Recovered"]:
        daily_col = f"Daily_{col}"
        df[daily_col] = df.groupby("Country/Region")[col].diff().fillna(0)
        df[daily_col] = df[daily_col].clip(lower=0)

    print("[PREPROCESS] Added daily change columns")
    return df


def add_active_cases(df):
    """Add Active Cases column."""
    df["Active"] = df["Confirmed"] - df["Deaths"] - df["Recovered"]
    df["Active"] = df["Active"].clip(lower=0)
    print("[PREPROCESS] Added 'Active' column")
    return df


def add_mortality_rate(df):
    """Add Mortality Rate percentage column."""
    df["Mortality_Rate"] = np.where(
        df["Confirmed"] > 0,
        (df["Deaths"] / df["Confirmed"]) * 100,
        0,
    )
    print("[PREPROCESS] Added 'Mortality_Rate' column")
    return df


def add_recovery_rate(df):
    """Add Recovery Rate percentage column."""
    df["Recovery_Rate"] = np.where(
        df["Confirmed"] > 0,
        (df["Recovered"] / df["Confirmed"]) * 100,
        0,
    )
    print("[PREPROCESS] Added 'Recovery_Rate' column")
    return df


def aggregate_by_country(df):
    """Aggregate data by country (sum across provinces/states)."""
    agg_cols = {
        "Confirmed": "sum",
        "Deaths": "sum",
        "Recovered": "sum",
    }

    daily_cols = [c for c in df.columns if c.startswith("Daily_")]
    for col in daily_cols:
        agg_cols[col] = "sum"

    country_df = df.groupby(["Country/Region", "Date"]).agg(agg_cols).reset_index()
    country_df = add_active_cases(country_df)
    country_df = add_mortality_rate(country_df)
    country_df = add_recovery_rate(country_df)

    print(f"[PREPROCESS] Country-level aggregation: {country_df.shape[0]} rows")
    return country_df


def preprocess_pipeline(confirmed, deaths, recovered):
    """
    Run the full preprocessing pipeline:
    1. Merge datasets
    2. Fill missing values
    3. Add derived columns
    4. Aggregate by country
    """
    print("\n" + "=" * 60)
    print("DATA PREPROCESSING PIPELINE")
    print("=" * 60)

    merged = merge_datasets(confirmed, deaths, recovered)
    merged = fill_missing(merged)
    merged = add_daily_columns(merged)
    merged = add_active_cases(merged)
    merged = add_mortality_rate(merged)
    merged = add_recovery_rate(merged)

    country_df = aggregate_by_country(merged)

    print("\n[PREPROCESS] Pipeline complete.")
    return merged, country_df


if __name__ == "__main__":
    from data_collection import load_all

    frames = load_all()
    if len(frames) == 3:
        merged, country_df = preprocess_pipeline(
            frames["confirmed"], frames["deaths"], frames["recovered"]
        )
        print("\n--- MERGED DATA ---")
        print(merged.head())
        print("\n--- COUNTRY DATA ---")
        print(country_df.head())
