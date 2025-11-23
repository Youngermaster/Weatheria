# Weatheria Climate Observatory

A distributed MapReduce pipeline for analyzing climate data from Medellin, Colombia (2022-2024) using AWS EMR and Python.

## Overview

This project processes 3 years of daily weather data using Hadoop MapReduce on AWS EMR, analyzing temperature patterns, extreme weather events, and precipitation correlations. Results are served through a FastAPI REST interface.

**Course**: ST0263 - Distributed Systems (Telematica)  
**University**: EAFIT  
**Data Source**: Open-Meteo Historical Weather API  
**Records**: 1095 days (2022-2024)  

## Technology Stack

- **MapReduce**: MRJob 0.7.4 (Python framework)
- **Cloud Platform**: AWS EMR 6.10.0 (Hadoop 3.3.3)
- **Storage**: AWS S3
- **API**: FastAPI
- **Frontend**: React + TypeScript + Vite
- **Language**: Python 3.11+

## Project Structure

```
weatheria/
├── src/
│   ├── mapreduce/           # MapReduce job implementations
│   │   ├── monthly_avg_temp.py
│   │   ├── extreme_temps.py
│   │   └── temp_precipitation.py
│   └── api/                 # FastAPI application
│       ├── main.py
│       ├── routers/
│       └── models/
├── weatheria-frontend/      # React web application
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── services/
│   └── package.json
├── scripts/
│   ├── download_data.py     # Fetch weather data
│   └── aws/                 # AWS deployment scripts
│       ├── setup_s3.sh
│       ├── create_emr_cluster.sh
│       ├── submit_emr_jobs_mrjob.sh
│       ├── download_results.sh
│       └── terminate_emr_cluster.sh
├── data/
│   └── raw/
│       └── medellin_weather_2022-2024.csv
├── output/                  # MapReduce results
├── tests/                   # Unit tests
└── docs/                    # Additional documentation
```

## MapReduce Jobs

### 1. Monthly Average Temperatures
**Script**: `src/mapreduce/monthly_avg_temp.py`  
**Output**: Monthly averages of max/min temperatures  
**Format**: `year-month TAB avg_max TAB avg_min`

### 2. Extreme Temperature Detection
**Script**: `src/mapreduce/extreme_temps.py`  
**Output**: Classification of days by temperature ranges  
**Categories**: very_hot (>30C), normal, cool (<15C), very_cool (<12C)  
**Format**: `category TAB count TAB avg_temp`

### 3. Temperature-Precipitation Correlation
**Script**: `src/mapreduce/temp_precipitation.py`  
**Output**: Monthly correlation between temperature and precipitation  
**Format**: `year-month TAB correlation TAB avg_temp TAB avg_precip TAB rainy_days TAB total_precip`

## API Endpoints

Base URL: `http://localhost:8000`

- `GET /monthly-avg` - All monthly temperature averages
- `GET /monthly-avg/hottest` - Hottest month
- `GET /monthly-avg/coolest` - Coolest month
- `GET /extreme-temps` - Extreme temperature statistics
- `GET /temp-precipitation` - Temperature-precipitation correlations

Interactive docs: `http://localhost:8000/docs`

## Quick Start

### Local Setup

```bash
# Clone repository
git clone <your-repo-url>
cd weatheria

# Install Python dependencies
pip install -r requirements.txt

# Download weather data
python scripts/download_data.py

# Start API server
cd src
uvicorn api.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd weatheria-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Access the web interface at `http://localhost:5173`

### AWS EMR Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete AWS deployment instructions.

## Results Summary

Based on 1095 days of data from Medellin (2022-2024):

**Temperature Patterns**:
- Average daily max: 24.6C - 29.15C
- Average daily min: 14.13C - 16.75C
- Hottest month: March 2024 (29.15C avg max)
- Coolest month: November 2022 (24.6C avg max)

**Extreme Weather**:
- Normal days: 700 (64%)
- Cool days (<15C): 380 (35%)
- Very hot days (>30C): 23 (2%)
- Very cool days (<12C): 6 (<1%)

**Precipitation Correlation**:
- Average correlation: -0.22 (weak negative)
- Interpretation: Slightly less rain on hotter days
- Average rainy days: 28 per month
- Monthly precipitation range: 106.5mm - 231.2mm

## Requirements

- Python 3.11+
- AWS Account (Academic or Standard)
- 2GB disk space minimum
- Internet connection for data download

## License

MIT License - See LICENSE file for details

## Authors

EAFIT University - Distributed Systems Course

## References

- Open-Meteo Historical Weather API: https://open-meteo.com/
- MRJob Documentation: https://mrjob.readthedocs.io/
- AWS EMR Guide: https://docs.aws.amazon.com/emr/
