"""
Module 1: Data Collection
Downloads COVID-19 datasets from Johns Hopkins University GitHub repository.
"""

import os
import requests
import pandas as pd


BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

DATASETS = {
    "confirmed": "time_series_covid19_confirmed_global.csv",
    "deaths": "time_series_covid19_deaths_global.csv",
    "recovered": "time_series_covid19_recovered_global.csv",
}


def download_dataset(dataset_key, data_dir="data"):
    """Download a single COVID-19 dataset from JHU GitHub."""
    filename = DATASETS[dataset_key]
    url = BASE_URL + filename
    filepath = os.path.join(data_dir, filename)

    os.makedirs(data_dir, exist_ok=True)

    if os.path.exists(filepath):
        print(f"[INFO] '{filename}' already exists. Skipping download.")
        return filepath

    print(f"[INFO] Downloading '{filename}'...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"[INFO] Saved to '{filepath}'")
        return filepath
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to download '{filename}': {e}")
        return None


def download_all(data_dir="data"):
    """Download all COVID-19 datasets."""
    print("=" * 60)
    print("COVID-19 DATA COLLECTION")
    print("=" * 60)
    filepaths = {}
    for key in DATASETS:
        path = download_dataset(key, data_dir)
        if path:
            filepaths[key] = path
    print(f"\n[INFO] Downloaded {len(filepaths)}/{len(DATASETS)} datasets.")
    return filepaths


def load_dataset(filepath):
    """Load a downloaded CSV dataset into a DataFrame."""
    df = pd.read_csv(filepath)
    print(f"[INFO] Loaded '{os.path.basename(filepath)}': {df.shape[0]} rows x {df.shape[1]} cols")
    return df


def load_all(data_dir="data"):
    """Load all downloaded datasets."""
    frames = {}
    for key, filename in DATASETS.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            frames[key] = load_dataset(filepath)
        else:
            print(f"[WARNING] '{filename}' not found. Run download_all() first.")
    return frames


if __name__ == "__main__":
    download_all()
    frames = load_all()
    for key, df in frames.items():
        print(f"\n--- {key.upper()} ---")
        print(df.head())
