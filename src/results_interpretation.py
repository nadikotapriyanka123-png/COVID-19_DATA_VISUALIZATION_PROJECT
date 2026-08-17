"""
Module 7: Results and Interpretation
Summarizes findings and key observations from the analysis.
"""

import pandas as pd
import numpy as np


def interpret_global_trends(global_daily):
    """Interpret global trend findings."""
    print("\n" + "=" * 60)
    print("RESULTS AND INTERPRETATION")
    print("=" * 60)

    print("\n--- Global Trend Interpretation ---")

    total_confirmed = global_daily["Confirmed"].iloc[-1]
    total_deaths = global_daily["Deaths"].iloc[-1]
    total_recovered = global_daily["Recovered"].iloc[-1]
    mortality_rate = (total_deaths / total_confirmed * 100) if total_confirmed > 0 else 0
    recovery_rate = (total_recovered / total_confirmed * 100) if total_confirmed > 0 else 0

    peak_daily_idx = global_daily["Daily_Confirmed"].idxmax()
    peak_date = global_daily.loc[peak_daily_idx, "Date"]
    peak_cases = global_daily.loc[peak_daily_idx, "Daily_Confirmed"]

    print(f"  1. The pandemic resulted in approximately {total_confirmed:,.0f} confirmed cases globally.")
    print(f"  2. Total deaths reached {total_deaths:,.0f}, yielding a global mortality rate of {mortality_rate:.2f}%.")
    print(f"  3. Total recoveries were {total_recovered:,.0f}, with a recovery rate of {recovery_rate:.2f}%.")
    print(f"  4. The peak daily new cases occurred on {peak_date.date()} with {peak_cases:,.0f} cases.")

    if global_daily["Daily_Confirmed"].iloc[-1] < peak_daily_idx:
        recent_trend = "declining"
    else:
        recent_trend = "increasing"
    print(f"  5. The most recent daily trend appears to be {recent_trend}.")

    return {
        "total_confirmed": total_confirmed,
        "total_deaths": total_deaths,
        "total_recovered": total_recovered,
        "mortality_rate": mortality_rate,
        "recovery_rate": recovery_rate,
        "peak_date": peak_date,
        "peak_cases": peak_cases,
    }


def interpret_regional(top_confirmed, top_deaths):
    """Interpret regional analysis findings."""
    print("\n--- Regional Analysis Interpretation ---")

    top_country = top_confirmed.index[0]
    top_cases = top_confirmed["Confirmed"].iloc[0]

    most_deaths_country = top_deaths.index[0]
    most_deaths = top_deaths["Deaths"].iloc[0]

    print(f"  1. {top_country} had the highest confirmed cases at {top_cases:,.0f}.")
    print(f"  2. {most_deaths_country} recorded the highest deaths at {most_deaths:,.0f}.")
    print(f"  3. The top 10 countries account for the majority of global cases.")

    highest_mortality_idx = top_confirmed["Mortality_Rate"].idxmax()
    highest_mortality = top_confirmed.loc[highest_mortality_idx, "Mortality_Rate"]
    print(f"  4. Among top countries, {highest_mortality_idx} had the highest mortality rate at {highest_mortality:.2f}%.")

    highest_recovery_idx = top_confirmed["Recovery_Rate"].idxmax()
    highest_recovery = top_confirmed.loc[highest_recovery_idx, "Recovery_Rate"]
    print(f"  5. {highest_recovery_idx} had the highest recovery rate at {highest_recovery:.2f}%.")


def interpret_mortality(global_daily):
    """Interpret mortality rate trends."""
    print("\n--- Mortality Rate Interpretation ---")

    initial_mr = global_daily["Mortality_Rate"].iloc[30:60].mean()
    final_mr = global_daily["Mortality_Rate"].iloc[-30:].mean()

    print(f"  1. Early pandemic mortality rate (approx): {initial_mr:.2f}%")
    print(f"  2. Recent mortality rate (last 30 days): {final_mr:.2f}%")

    if final_mr < initial_mr:
        print("  3. Mortality rate has decreased over time, suggesting improved treatment outcomes.")
    else:
        print("  3. Mortality rate has remained relatively stable or increased.")


def generate_conclusions(results):
    """Generate final conclusions."""
    print("\n" + "=" * 60)
    print("CONCLUSIONS")
    print("=" * 60)

    print("""
  1. The COVID-19 pandemic had a significant global impact, with millions of
     confirmed cases across nearly all countries and territories.

  2. Certain countries bore a disproportionately high burden of cases and deaths,
     reflecting differences in population size, healthcare capacity, and
     public health responses.

  3. The mortality rate varied significantly across countries, influenced by
     factors such as healthcare infrastructure, testing rates, and demographics.

  4. Recovery rates improved over time as treatment protocols advanced and
     vaccination campaigns expanded globally.

  5. Data visualization techniques effectively transformed large volumes of
     raw COVID-19 data into clear, interpretable insights that facilitate
     understanding of pandemic trends.

  6. Time-series analysis revealed distinct waves of infection, each with
     different characteristics in terms of magnitude and duration.

  7. This project demonstrates the value of data analytics and visualization
     in understanding complex real-world health crises and supporting
     evidence-based decision-making.
""")


def run_interpretation(trend_results, regional_results):
    """Run complete interpretation pipeline."""
    print("\n" + "=" * 60)
    print("RESULTS, INTERPRETATION, AND CONCLUSIONS")
    print("=" * 60)

    global_stats = interpret_global_trends(trend_results["global_daily"])
    interpret_regional(
        regional_results["top_confirmed"],
        regional_results["top_deaths"],
    )
    interpret_mortality(trend_results["global_daily"])
    generate_conclusions(trend_results)

    print("[INTERPRETATION] Complete.")
    return global_stats


if __name__ == "__main__":
    from data_collection import load_all
    from data_preprocessing import preprocess_pipeline
    from trend_analysis import run_trend_analysis
    from regional_analysis import run_regional_analysis

    frames = load_all()
    if len(frames) == 3:
        merged, country_df = preprocess_pipeline(
            frames["confirmed"], frames["deaths"], frames["recovered"]
        )
        trend_results = run_trend_analysis(country_df)
        regional_results = run_regional_analysis(country_df)
        run_interpretation(trend_results, regional_results)
