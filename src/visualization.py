"""
Module 6: Data Visualization
Generates charts and graphs to communicate COVID-19 analytical findings.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np


sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (14, 7)
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12


def save_fig(fig, name, output_dir="outputs"):
    """Save figure to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{name}.png")
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[VIZ] Saved: {filepath}")
    return filepath


# ──────────────────────────────────────────────────────────
# 1. Global Trend Line Chart
# ──────────────────────────────────────────────────────────
def plot_global_trend(global_daily, output_dir="outputs"):
    """Plot global confirmed, deaths, and recovered over time."""
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(global_daily["Date"], global_daily["Confirmed"], label="Confirmed", color="blue", linewidth=2)
    ax.plot(global_daily["Date"], global_daily["Deaths"], label="Deaths", color="red", linewidth=2)
    ax.plot(global_daily["Date"], global_daily["Recovered"], label="Recovered", color="green", linewidth=2)

    ax.set_title("COVID-19 Global Trend: Confirmed, Deaths, and Recovered")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Count")
    ax.legend()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45)

    fig.tight_layout()
    return save_fig(fig, "01_global_trend", output_dir)


# ──────────────────────────────────────────────────────────
# 2. Top 10 Countries Bar Chart
# ──────────────────────────────────────────────────────────
def plot_top_countries_bar(top_confirmed, output_dir="outputs"):
    """Bar chart of top 10 countries by confirmed cases."""
    fig, ax = plt.subplots(figsize=(14, 7))

    countries = top_confirmed.index.tolist()
    confirmed = top_confirmed["Confirmed"].values

    colors = sns.color_palette("Reds_r", n_colors=len(countries))
    bars = ax.barh(countries[::-1], confirmed[::-1], color=colors)

    for bar, val in zip(bars, confirmed[::-1]):
        ax.text(bar.get_width() + max(confirmed) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:,.0f}", va="center", fontsize=10)

    ax.set_title("Top 10 Countries by Confirmed COVID-19 Cases")
    ax.set_xlabel("Total Confirmed Cases")
    ax.set_ylabel("Country")

    fig.tight_layout()
    return save_fig(fig, "02_top10_countries_bar", output_dir)


# ──────────────────────────────────────────────────────────
# 3. Deaths vs Recoveries Comparison
# ──────────────────────────────────────────────────────────
def plot_deaths_vs_recovered(top_confirmed, output_dir="outputs"):
    """Comparison bar chart of deaths vs recoveries for top countries."""
    fig, ax = plt.subplots(figsize=(14, 7))

    countries = top_confirmed.index.tolist()
    x = np.arange(len(countries))
    width = 0.35

    ax.bar(x - width / 2, top_confirmed["Deaths"].values, width, label="Deaths", color="red")
    ax.bar(x + width / 2, top_confirmed["Recovered"].values, width, label="Recovered", color="green")

    ax.set_title("Deaths vs Recoveries: Top 10 Countries")
    ax.set_xlabel("Country")
    ax.set_ylabel("Count")
    ax.set_xticks(x)
    ax.set_xticklabels(countries, rotation=45, ha="right")
    ax.legend()

    fig.tight_layout()
    return save_fig(fig, "03_deaths_vs_recovered", output_dir)


# ──────────────────────────────────────────────────────────
# 4. Daily New Cases Bar Chart
# ──────────────────────────────────────────────────────────
def plot_daily_new_cases(global_daily, output_dir="outputs"):
    """Bar chart of daily new confirmed cases globally."""
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.bar(global_daily["Date"], global_daily["Daily_Confirmed"],
           color="steelblue", alpha=0.7, width=1)

    rolling = global_daily["Daily_Confirmed"].rolling(window=7).mean()
    ax.plot(global_daily["Date"], rolling, color="red", linewidth=2, label="7-Day Moving Avg")

    ax.set_title("Global Daily New COVID-19 Confirmed Cases")
    ax.set_xlabel("Date")
    ax.set_ylabel("New Cases")
    ax.legend()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45)

    fig.tight_layout()
    return save_fig(fig, "04_daily_new_cases", output_dir)


# ──────────────────────────────────────────────────────────
# 5. Monthly Heatmap
# ──────────────────────────────────────────────────────────
def plot_monthly_heatmap(country_df, top_n=10, output_dir="outputs"):
    """Heatmap of monthly confirmed cases for top N countries."""
    latest_date = country_df["Date"].max()
    latest = country_df[country_df["Date"] == latest_date]
    top_countries = (
        latest.groupby("Country/Region")["Confirmed"]
        .sum().sort_values(ascending=False).head(top_n).index.tolist()
    )

    filtered = country_df[country_df["Country/Region"].isin(top_countries)].copy()
    filtered["Month"] = filtered["Date"].dt.to_period("M")

    pivot = filtered.pivot_table(
        index="Country/Region",
        columns="Month",
        values="Daily_Confirmed",
        aggfunc="sum",
    )

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.heatmap(pivot, cmap="YlOrRd", annot=False, fmt=".0f",
                linewidths=0.5, ax=ax, cbar_kws={"label": "Daily Confirmed Cases"})

    ax.set_title("Monthly COVID-19 Confirmed Cases Heatmap (Top 10 Countries)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Country")
    plt.xticks(rotation=45, ha="right")

    fig.tight_layout()
    return save_fig(fig, "05_monthly_heatmap", output_dir)


# ──────────────────────────────────────────────────────────
# 6. Pie Chart - Distribution by Region
# ──────────────────────────────────────────────────────────
def plot_pie_chart(top_confirmed, output_dir="outputs"):
    """Pie chart of confirmed case distribution among top countries."""
    fig, ax = plt.subplots(figsize=(10, 10))

    countries = top_confirmed.index.tolist()
    confirmed = top_confirmed["Confirmed"].values

    other_total = confirmed.sum() * 0.05
    labels = countries + ["Others"]
    sizes = list(confirmed) + [other_total]

    colors = sns.color_palette("Set2", n_colors=len(labels))
    explode = [0.05] * len(countries) + [0]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%",
        startangle=140, colors=colors, explode=explode,
        textprops={"fontsize": 10},
    )

    ax.set_title("Distribution of COVID-19 Confirmed Cases (Top 10 Countries)")

    fig.tight_layout()
    return save_fig(fig, "06_pie_distribution", output_dir)


# ──────────────────────────────────────────────────────────
# 7. Mortality Rate Trend
# ──────────────────────────────────────────────────────────
def plot_mortality_trend(global_daily, output_dir="outputs"):
    """Line chart of global mortality rate over time."""
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(global_daily["Date"], global_daily["Mortality_Rate"],
            color="darkred", linewidth=2)

    ax.set_title("Global COVID-19 Mortality Rate Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Mortality Rate (%)")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45)

    fig.tight_layout()
    return save_fig(fig, "07_mortality_trend", output_dir)


# ──────────────────────────────────────────────────────────
# 8. Country Comparison Line Chart
# ──────────────────────────────────────────────────────────
def plot_country_comparison(country_df, countries, column="Confirmed", output_dir="outputs"):
    """Line chart comparing trends for specific countries."""
    filtered = country_df[country_df["Country/Region"].isin(countries)]

    fig, ax = plt.subplots(figsize=(14, 7))

    for country in countries:
        country_data = filtered[filtered["Country/Region"] == country]
        ax.plot(country_data["Date"], country_data[column], label=country, linewidth=2)

    ax.set_title(f"COVID-19 {column} Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel(column)
    ax.legend()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45)

    fig.tight_layout()
    return save_fig(fig, f"08_country_comparison_{column.lower()}", output_dir)


# ──────────────────────────────────────────────────────────
# Generate All Charts
# ──────────────────────────────────────────────────────────
def generate_all_charts(country_df, global_daily, top_confirmed, output_dir="outputs"):
    """Generate all visualization charts."""
    print("\n" + "=" * 60)
    print("DATA VISUALIZATION")
    print("=" * 60)

    plot_global_trend(global_daily, output_dir)
    plot_top_countries_bar(top_confirmed, output_dir)
    plot_deaths_vs_recovered(top_confirmed, output_dir)
    plot_daily_new_cases(global_daily, output_dir)
    plot_monthly_heatmap(country_df, output_dir=output_dir)
    plot_pie_chart(top_confirmed, output_dir)
    plot_mortality_trend(global_daily, output_dir)

    comparison_countries = ["US", "India", "Brazil", "France", "Germany"]
    available = [c for c in comparison_countries if c in country_df["Country/Region"].values]
    if available:
        plot_country_comparison(country_df, available, "Confirmed", output_dir)
        plot_country_comparison(country_df, available, "Deaths", output_dir)

    print(f"\n[VIZ] All charts saved to '{output_dir}/'")


if __name__ == "__main__":
    from data_collection import load_all
    from data_preprocessing import preprocess_pipeline
    from trend_analysis import run_trend_analysis
    from regional_analysis import top_countries_by_confirmed

    frames = load_all()
    if len(frames) == 3:
        merged, country_df = preprocess_pipeline(
            frames["confirmed"], frames["deaths"], frames["recovered"]
        )
        trend_results = run_trend_analysis(country_df)
        top_confirmed = top_countries_by_confirmed(country_df)
        generate_all_charts(country_df, trend_results["global_daily"], top_confirmed)
