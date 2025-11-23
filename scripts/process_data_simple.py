#!/usr/bin/env python3
"""
Simple MapReduce-style processing of weather data
Generates the same results as MapReduce jobs without requiring Hadoop
"""

import pandas as pd
import os
from collections import defaultdict
import math

def process_monthly_avg(input_file, output_file):
    """Calculate monthly average temperatures"""
    print("Processing monthly averages...")

    df = pd.read_csv(input_file)
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')

    results = df.groupby('month').agg({
        'temp_max': 'mean',
        'temp_min': 'mean'
    }).round(2)

    with open(output_file, 'w') as f:
        for month, row in results.iterrows():
            f.write(f"{month}\t{row['temp_max']}\t{row['temp_min']}\n")

    print(f"✓ Monthly averages saved to {output_file}")
    return results

def process_extreme_temps(input_file, output_file):
    """Detect days with extreme temperatures"""
    print("Processing extreme temperatures...")

    df = pd.read_csv(input_file)
    df['avg_temp'] = (df['temp_max'] + df['temp_min']) / 2

    categories = defaultdict(lambda: {'count': 0, 'total_temp': 0})

    for _, row in df.iterrows():
        cats = []
        if row['temp_max'] > 30:
            cats.append('very_hot')
        if row['temp_min'] < 15:
            cats.append('cool')
        if row['temp_min'] < 12:
            cats.append('very_cool')
        if not cats:
            cats.append('normal')

        for cat in cats:
            categories[cat]['count'] += 1
            categories[cat]['total_temp'] += row['avg_temp']

    with open(output_file, 'w') as f:
        for cat, data in categories.items():
            avg_temp = round(data['total_temp'] / data['count'], 2)
            f.write(f"{cat}\t{data['count']}\t{avg_temp}\n")

    print(f"✓ Extreme temperatures saved to {output_file}")
    return categories

def process_temp_precipitation(input_file, output_file):
    """Analyze temperature-precipitation correlation by month"""
    print("Processing temperature-precipitation correlation...")

    df = pd.read_csv(input_file)
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    df['avg_temp'] = (df['temp_max'] + df['temp_min']) / 2

    with open(output_file, 'w') as f:
        for month in df['month'].unique():
            month_data = df[df['month'] == month]

            temps = month_data['avg_temp'].values
            precips = month_data['precipitation'].values

            if len(temps) < 2:
                continue

            # Calculate Pearson correlation
            mean_temp = temps.mean()
            mean_precip = precips.mean()

            numerator = sum((t - mean_temp) * (p - mean_precip)
                          for t, p in zip(temps, precips))
            temp_var = sum((t - mean_temp) ** 2 for t in temps)
            precip_var = sum((p - mean_precip) ** 2 for p in precips)

            denominator = math.sqrt(temp_var * precip_var)
            correlation = round(numerator / denominator, 4) if denominator != 0 else 0.0

            rainy_days = sum(1 for p in precips if p > 0)
            total_precip = round(precips.sum(), 2)
            avg_temp = round(mean_temp, 2)
            avg_precip = round(mean_precip, 2)

            f.write(f"{month}\t{correlation}\t{avg_temp}\t{avg_precip}\t{rainy_days}\t{total_precip}\n")

    print(f"✓ Temperature-precipitation correlation saved to {output_file}")

def main():
    """Process all MapReduce jobs"""
    input_file = "data/raw/medellin_weather_2022-2024.csv"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    os.makedirs("output", exist_ok=True)

    print("="* 60)
    print("Weatheria Climate Observatory - Data Processing")
    print("="*60)
    print(f"Input: {input_file}")
    print("")

    # Process all jobs
    process_monthly_avg(input_file, "output/monthly_avg_results.csv")
    process_extreme_temps(input_file, "output/extreme_temps_results.csv")
    process_temp_precipitation(input_file, "output/temp_precip_results.csv")

    print("")
    print("="*60)
    print("✅ All processing complete!")
    print("="*60)
    print("")
    print("Results location: ./output/")
    print("  - monthly_avg_results.csv")
    print("  - extreme_temps_results.csv")
    print("  - temp_precip_results.csv")
    print("")
    print("Next: Start API server to view results")
    print("  Run: source venv/bin/activate && python3 -m src.api.main")

if __name__ == "__main__":
    main()
