#!/usr/bin/env python3
"""
Convert Hadoop MapReduce output (TSV) to CSV format for API
"""

import csv
import os


def convert_monthly_avg():
    """Convert monthly average output"""
    input_file = "output/hadoop/monthly_avg.tsv"
    output_file = "output/monthly_avg_results.csv"

    with open(input_file, 'r') as fin, open(output_file, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['month', 'avg_max', 'avg_min'])

        for line in fin:
            # Remove quotes and parse - Hadoop output uses quotes around values
            line = line.strip().replace('"', '')
            # Replace literal \t with actual tab
            line = line.replace('\\t', '\t')
            # Split by tab - first tab separates key from value
            parts = line.split('\t', 1)  # Split only on first tab
            if len(parts) >= 2:
                month = parts[0]
                # Second part contains "avg_max\tavg_min" format
                value_part = parts[1]
                temps = value_part.split('\t')
                if len(temps) >= 2:
                    writer.writerow([month, temps[0], temps[1]])

    print(f"✓ Converted monthly averages: {output_file}")


def convert_extreme_temps():
    """Convert extreme temperatures output"""
    input_file = "output/hadoop/extreme_temps.tsv"
    output_file = "output/extreme_temps_results.csv"

    with open(input_file, 'r') as fin, open(output_file, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['category', 'count', 'avg_temp'])

        for line in fin:
            # Remove quotes and parse
            line = line.strip().replace('"', '')
            line = line.replace('\\t', '\t')
            parts = line.split('\t', 1)  # Split only on first tab
            if len(parts) >= 2:
                category = parts[0]
                # Second part contains "count\tavg_temp"
                value_part = parts[1]
                stats = value_part.split('\t')
                if len(stats) >= 2:
                    writer.writerow([category, stats[0], stats[1]])

    print(f"✓ Converted extreme temperatures: {output_file}")


def convert_temp_precip():
    """Convert temperature-precipitation correlation output"""
    input_file = "output/hadoop/temp_precip.tsv"
    output_file = "output/temp_precip_results.csv"

    with open(input_file, 'r') as fin, open(output_file, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['month', 'correlation', 'avg_temp', 'avg_precip', 'rainy_days', 'total_precip'])

        for line in fin:
            # Remove quotes and parse
            line = line.strip().replace('"', '')
            line = line.replace('\\t', '\t')
            parts = line.split('\t', 1)  # Split only on first tab
            if len(parts) >= 2:
                month = parts[0]
                # Second part contains "corr\tavg_temp\tavg_precip\trainy_days\ttotal_precip"
                value_part = parts[1]
                stats = value_part.split('\t')
                if len(stats) >= 5:
                    writer.writerow([month, stats[0], stats[1], stats[2], stats[3], stats[4]])

    print(f"✓ Converted temp-precipitation: {output_file}")


if __name__ == '__main__':
    print("Converting Hadoop MapReduce outputs to CSV format...\n")

    convert_monthly_avg()
    convert_extreme_temps()
    convert_temp_precip()

    print("\n✓ All conversions completed successfully!")
