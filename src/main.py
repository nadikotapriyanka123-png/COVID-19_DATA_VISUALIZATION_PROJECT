"""
Main Pipeline: COVID-19 Data Visualization Project
Orchestrates all modules from data collection to visualization.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_collection import download_all, load_all
from data_preprocessing import preprocess_pipeline
from eda import run_eda
from trend_analysis import run_trend_analysis
from regional_analysis import run_regional_analysis, top_countries_by_confirmed
from visualization import generate_all_charts
from results_interpretation import run_interpretation


def main():
    """Run the complete COVID-19 analysis pipeline."""
    print("=" * 60)
    print("COVID-19 DATA VISUALIZATION PROJECT")
    print("Data Analyst Internship - Final Project")
    print("=" * 60)

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")

    print("\n[STEP 1] Data Collection")
    download_all(data_dir)

    print("\n[STEP 2] Loading Datasets")
    frames = load_all(data_dir)

    if len(frames) < 3:
        print("[ERROR] Not all datasets could be loaded. Exiting.")
        return

    print("\n[STEP 3] Data Preprocessing")
    merged, country_df = preprocess_pipeline(
        frames["confirmed"], frames["deaths"], frames["recovered"]
    )

    print("\n[STEP 4] Exploratory Data Analysis")
    run_eda(merged, country_df)

    print("\n[STEP 5] Trend Analysis")
    trend_results = run_trend_analysis(country_df)

    print("\n[STEP 6] Regional / Country-wise Analysis")
    regional_results = run_regional_analysis(country_df)

    print("\n[STEP 7] Data Visualization")
    top_confirmed = top_countries_by_confirmed(country_df)
    generate_all_charts(country_df, trend_results["global_daily"], top_confirmed, output_dir)

    print("\n[STEP 8] Results and Interpretation")
    run_interpretation(trend_results, regional_results)

    print("\n" + "=" * 60)
    print("PROJECT COMPLETE")
    print(f"Charts saved to: {os.path.abspath(output_dir)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
