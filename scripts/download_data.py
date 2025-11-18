#!/usr/bin/env python3
"""
Download weather data from Open-Meteo API for Medellín, Colombia
Usage: python scripts/download_data.py
"""

import os
import sys
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Configuration
LATITUDE = 6.25
LONGITUDE = -75.56
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"
TIMEZONE = "America/Bogota"
OUTPUT_DIR = "data/raw"
OUTPUT_FILE = "medellin_weather_2022-2024.csv"


def download_medellin_weather(
    start_date: str,
    end_date: str,
    output_file: str,
    latitude: float = LATITUDE,
    longitude: float = LONGITUDE,
) -> pd.DataFrame:
    """
    Download weather data from Open-Meteo for Medellín
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        output_file: Path to save CSV file
        latitude: Latitude coordinate
        longitude: Longitude coordinate
    
    Returns:
        DataFrame with weather data
    """
    
    # API endpoint
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": TIMEZONE
    }
    
    print("=" * 60)
    print("Weatheria Climate Observatory - Data Download")
    print("=" * 60)
    print(f"📍 Location: Medellín, Colombia ({latitude}, {longitude})")
    print(f"📅 Period: {start_date} to {end_date}")
    print(f"🌐 Source: Open-Meteo Archive API")
    print("=" * 60)
    print("\n⏳ Downloading data...")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': data['daily']['time'],
            'temp_max': data['daily']['temperature_2m_max'],
            'temp_min': data['daily']['temperature_2m_min'],
            'precipitation': data['daily']['precipitation_sum']
        })
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print(f"✅ Data saved to: {output_file}")
        print(f"📊 Total records: {len(df)}")
        print(f"📏 Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"🌡️  Temperature range: {df['temp_min'].min():.1f}°C to {df['temp_max'].max():.1f}°C")
        print(f"💧 Total precipitation: {df['precipitation'].sum():.1f} mm")
        
        print("\n📋 Sample data (first 5 rows):")
        print(df.head().to_string(index=False))
        
        print("\n📊 Basic statistics:")
        print(df.describe().to_string())
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading data: {e}")
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"❌ Error parsing data: {e}")
        sys.exit(1)


def main():
    """Main function"""
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    
    # Download data
    df = download_medellin_weather(
        start_date=START_DATE,
        end_date=END_DATE,
        output_file=output_path
    )
    
    print("\n" + "=" * 60)
    print("✨ Download completed successfully!")
    print("=" * 60)
    print(f"\n💡 Next steps:")
    print(f"   1. Review the data: cat {output_path}")
    print(f"   2. Load to HDFS: ./scripts/load_to_hdfs.sh")
    print(f"   3. Run MapReduce jobs: ./scripts/run_mapreduce.sh")


if __name__ == "__main__":
    main()
