# Weatheria - Climate Observatory 

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Hadoop](https://img.shields.io/badge/hadoop-3.3.6-yellow.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![AWS EMR](https://img.shields.io/badge/AWS-EMR%206.10.0-orange.svg)
![React](https://img.shields.io/badge/React-19.2.0-61dafb.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7+-blue.svg)

A distributed data engineering platform for climate analysis using MapReduce on AWS EMR, featuring a FastAPI backend and modern React frontend for interactive data visualization.

## Architecture Summary

**AWS Infrastructure:**
- **EMR Cluster**: 3-node Hadoop cluster for MapReduce processing
  - Job 1: Monthly Average Temperatures
  - Job 2: Extreme Temperature Classification
  - Job 3: Temperature-Precipitation Correlation
- **S3 Bucket**: `weatheria-climate-data` for data storage
- **Backend EC2**: FastAPI server at http://3.88.63.182:8000
- **Frontend EC2**: React application at http://54.85.123.135:5173

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [MapReduce Jobs](#mapreduce-jobs)
- [API Documentation](#api-documentation)
- [Frontend Application](#frontend-application)
- [AWS EMR Deployment](#aws-emr-deployment)
- [Results and Findings](#results-and-findings)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Overview

Weatheria is a complete ETL (Extract, Transform, Load) pipeline for weather data analysis, built for distributed processing at scale. The system analyzes 3 years of daily weather data (2022-2024) from Medellin, Colombia using MapReduce on AWS EMR, exposing results through a REST API and visualizing them in an interactive web dashboard.

**Key Features:**
- **Data Collection**: 1,095 daily records from Open-Meteo Historical Weather API
- **Distributed Processing**: MapReduce jobs on AWS EMR cluster (3 nodes)
- **REST API**: FastAPI backend with automatic documentation
- **Interactive Visualization**: React + TypeScript frontend with real-time charts
- **Cloud-Native**: Fully deployed on AWS (EMR, S3)

## Architecture

![Arquitectura Hadoop](Arquitectura%20Hadoop.png)

## Prerequisites

### For Local Development

- **Python 3.11+** - MapReduce jobs and API backend
- **Node.js 18+** - Frontend development
- **pip** - Python package manager
- **npm** - Node.js package manager

### For AWS Deployment

- **AWS Account** with EMR permissions (AWS Academy account supported)
- **AWS CLI** configured with credentials
- **S3 Bucket** for data storage
- **Git Bash** (Windows) or standard terminal (Linux/Mac)

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Youngermaster/Weatheria.git
cd Weatheria
```

### 2. Backend Setup

Install Python dependencies and start the API server:

```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
cd src/api
python main.py
```

The API will be available at `http://localhost:8000` 
Interactive documentation: `http://localhost:8000/docs`

### 3. Frontend Setup

Install Node.js dependencies and start the development server:

```bash
# Navigate to frontend directory
cd weatheria-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. AWS EMR Deployment (Optional)

For production deployment on AWS EMR, follow the detailed guide in [DEPLOYMENT.md](DEPLOYMENT.md).

Quick deployment summary:

```bash
# 1. Download weather data
python scripts/download_data.py

# 2. Setup S3 bucket and upload data
bash scripts/aws/setup_s3.sh

# 3. Create EMR cluster
bash scripts/aws/create_emr_cluster.sh

# 4. Submit MapReduce jobs
bash scripts/aws/submit_emr_jobs_mrjob.sh monthly
bash scripts/aws/submit_emr_jobs_mrjob.sh extreme
bash scripts/aws/submit_emr_jobs_mrjob.sh correlation

# 5. Download results
bash scripts/aws/download_results.sh

# 6. Terminate cluster (IMPORTANT - avoid charges)
bash scripts/aws/terminate_emr_cluster.sh
```

## Project Structure

```
weatheria/
├── data/
│  ├── raw/             # Raw weather data from API
│  │  └── medellin_weather_2022-2024.csv
│  └── processed/          # Processed MapReduce outputs
├── src/
│  ├── mapreduce/          # MapReduce job implementations
│  │  ├── monthly_avg_temp.py   # Monthly temperature analysis
│  │  ├── extreme_temps.py     # Temperature classification
│  │  └── temp_precipitation.py  # Correlation analysis
│  └── api/             # FastAPI backend
│    ├── main.py         # Application entry point
│    ├── config.py        # Configuration settings
│    ├── models/
│    │  └── schemas.py      # Pydantic data models
│    └── routers/
│      ├── monthly.py      # Monthly averages endpoint
│      ├── extremes.py     # Extreme temperatures endpoint
│      └── correlation.py    # Correlation endpoint
├── weatheria-frontend/       # React TypeScript application
│  ├── src/
│  │  ├── services/
│  │  │  └── api.ts       # Backend API client (Axios)
│  │  ├── pages/
│  │  │  ├── Dashboard.tsx    # Main dashboard with charts
│  │  │  ├── MonthlyAnalysis.tsx # Monthly temperature analysis
│  │  │  ├── ExtremeAnalysis.tsx # Temperature distribution
│  │  │  ├── PrecipitationAnalysis.tsx
│  │  │  └── About.tsx
│  │  ├── components/
│  │  │  ├── DashboardLayout.tsx
│  │  │  ├── StatCard.tsx
│  │  │  └── ui/         # shadcn/ui components
│  │  ├── types/
│  │  │  └── index.ts      # TypeScript interfaces
│  │  └── lib/
│  │    └── utils.ts      # Utility functions
│  ├── package.json
│  ├── vite.config.ts
│  └── tailwind.config.js
├── scripts/
│  ├── download_data.py       # Data collection from Open-Meteo API
│  └── aws/             # AWS deployment automation
│    ├── setup_s3.sh
│    ├── create_emr_cluster.sh
│    ├── submit_emr_jobs_mrjob.sh
│    ├── download_results.sh
│    └── terminate_emr_cluster.sh
├── output/             # MapReduce results (CSV files)
│  ├── monthly_avg_fixed.csv
│  ├── extreme_temps_fixed.csv
│  └── temp_precip_fixed.csv
├── requirements.txt         # Python dependencies
├── DEPLOYMENT.md          # Detailed AWS EMR deployment guide
└── README.md            # This file
```

## MapReduce Jobs

All MapReduce jobs are implemented using the **MRJob** Python framework and designed for AWS EMR execution.

### 1. Monthly Average Temperature (`monthly_avg_temp.py`)

Calculates average maximum and minimum temperatures per month across 3 years.

**Algorithm:**
```python
# Map phase: Extract year-month and temperatures
(year-month) → (max_temp, min_temp, count)

# Reduce phase: Calculate averages
(year-month) → (avg_max_temp, avg_min_temp)
```

**Input:** Daily weather records (1,095 days) 
**Output:** Monthly aggregates (36 months)

```csv
month,avg_max_temp,avg_min_temp
2022-01,25.85,14.30
2022-02,27.60,15.00
2022-03,28.45,15.80
```

**Execution time on EMR:** ~40 seconds

### 2. Extreme Temperature Classification (`extreme_temps.py`)

Categorizes days by temperature into 4 categories based on maximum temperature.

**Categories:**
- **Very Cool:** max_temp < 20°C (cold days)
- **Cool:** 20°C ≤ max_temp < 27°C (pleasant days)
- **Normal:** 27°C ≤ max_temp < 30°C (typical tropical weather)
- **Very Hot:** max_temp ≥ 30°C (heat wave days)

**Algorithm:**
```python
# Map phase: Classify each day
temperature → category

# Reduce phase: Count per category
category → total_count
```

**Output:** Count per category

```csv
category,count
very_cool,6
cool,380
normal,700
very_hot,23
```

**Execution time on EMR:** ~17 seconds

### 3. Temperature-Precipitation Correlation (`temp_precipitation.py`)

Analyzes the relationship between temperature and precipitation by month.

**Algorithm:**
```python
# Map phase: Extract monthly data
(year-month) → (temperature, precipitation)

# Reduce phase: Calculate correlation coefficient
(year-month) → correlation
```

**Output:** Monthly correlation coefficients

```csv
month,correlation
2022-01,-0.31
2022-02,0.14
2022-03,-0.22
```

**Interpretation:**
- Negative correlation: Higher temperatures → Lower precipitation
- Positive correlation: Higher temperatures → Higher precipitation
- Values range from -1.0 to +1.0

**Execution time on EMR:** ~29 seconds

## API Documentation

The FastAPI backend provides RESTful endpoints for accessing processed climate data.

**Base URL:** `http://localhost:8000`

### Endpoints

#### 1. Monthly Averages
```http
GET /monthly-avg
```

Returns monthly average temperatures (max and min) for 36 months.

**Response:**
```json
[
 {
  "month": "2022-01",
  "avg_max_temp": 25.85,
  "avg_min_temp": 14.30
 }
]
```

#### 2. Extreme Temperatures
```http
GET /extreme-temps
```

Returns count of days per temperature category.

**Response:**
```json
[
 {
  "category": "very_cool",
  "count": 6
 },
 {
  "category": "cool",
  "count": 380
 },
 {
  "category": "normal",
  "count": 700
 },
 {
  "category": "very_hot",
  "count": 23
 }
]
```

#### 3. Temperature-Precipitation Correlation
```http
GET /temp-precipitation
```

Returns monthly correlation between temperature and precipitation.

**Response:**
```json
[
 {
  "month": "2022-01",
  "correlation": -0.31
 }
]
```

#### 4. Statistics
```http
GET /stats
```

Returns general dataset statistics.

#### 5. Health Check
```http
GET /health
```

API health check endpoint.

#### 6. Download Results
```http
GET /download/{type}
```

Download raw CSV results. Types: `monthly-avg`, `extreme-temps`, `temp-precipitation`

### Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### CORS Configuration

The API allows cross-origin requests from all origins for development. For production, configure specific origins in `src/api/config.py`.

## Frontend Application

Modern React + TypeScript single-page application with interactive data visualizations.

### Tech Stack

- **React 19.2.0** - UI framework
- **TypeScript 5.7+** - Type safety
- **Vite 7.2.4** - Build tool and dev server
- **Recharts 3.4.1** - Data visualization library
- **Tailwind CSS** - Utility-first CSS framework
- **Axios 1.13.2** - HTTP client
- **Lucide React** - Icon library
- **shadcn/ui** - UI component library

### Pages

#### 1. Dashboard (`/`)
Main overview with 4 visualization cards:
- **Temperature Trends:** Line chart showing monthly max/min temperatures over 3 years
- **Temperature Distribution:** Pie chart showing distribution of temperature categories
- **Precipitation Patterns:** Bar chart of monthly precipitation
- **Correlation Analysis:** Scatter plot of temperature vs. precipitation

#### 2. Monthly Analysis (`/monthly`)
Detailed monthly temperature analysis:
- Area chart with max/min temperature ranges
- Monthly statistics table
- Temperature trend identification

#### 3. Extreme Analysis (`/extreme`)
Temperature category distribution:
- Bar chart showing count per category
- Pie chart showing percentage distribution
- Category definitions and insights

#### 4. Precipitation Analysis (`/precipitation`)
Temperature-precipitation correlation:
- Scatter plots by month
- Correlation coefficient visualization
- Seasonal pattern identification

#### 5. About (`/about`)
Project information and methodology

### API Integration

The frontend uses Axios to communicate with the FastAPI backend:

```typescript
// src/services/api.ts
const weatheriaApi = {
 getMonthlyAverages: () => axios.get('/monthly-avg'),
 getExtremeTemperatures: () => axios.get('/extreme-temps'),
 getTemperaturePrecipitation: () => axios.get('/temp-precipitation'),
 getStats: () => axios.get('/stats')
}
```

**Data Flow:**
1. User navigates to page
2. React component calls API service method
3. Axios fetches data from backend
4. Data is typed with TypeScript interfaces
5. Recharts renders interactive visualization
6. User interacts with charts (hover, zoom, filter)

### Development

```bash
# Install dependencies
cd weatheria-frontend
npm install

# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## AWS EMR Deployment

The project was successfully deployed on AWS Elastic MapReduce for distributed data processing.

### Deployment Summary

**Cluster Configuration:**
- **Cluster ID:** j-3FG55B8H77VI3
- **EMR Release:** 6.10.0 (Hadoop 3.3.3, Python 3.9)
- **Instance Type:** m5.xlarge (4 vCPU, 16 GB RAM)
- **Instance Count:** 3 nodes (1 master, 2 core)
- **Region:** us-east-1 (N. Virginia)
- **S3 Bucket:** weatheria-climate-data

**Processing Results:**
- **Total Processing Time:** ~2 minutes
- **Job 1 - Monthly Avg:** 40 seconds
- **Job 2 - Extreme Temps:** 17 seconds
- **Job 3 - Correlation:** 29 seconds

**Cost Analysis:**
- **Instance Cost:** $0.50/hour per m5.xlarge node
- **Total Cluster Cost:** $1.50/hour (3 nodes)
- **Actual Runtime:** ~0.5 hours
- **Total Cost:** ~$0.75 (less than $1 for complete processing)

### Quick Deployment Guide

#### Prerequisites
1. AWS account with EMR permissions
2. AWS CLI installed and configured
3. Python 3.11+ with required packages
4. S3 bucket created

#### Step 1: Download Weather Data
```bash
python scripts/download_data.py
```
Downloads 1,095 daily records from Open-Meteo API.

#### Step 2: Setup S3 Bucket
```bash
bash scripts/aws/setup_s3.sh
```
Creates bucket structure and uploads data/scripts to S3.

#### Step 3: Create EMR Cluster
```bash
bash scripts/aws/create_emr_cluster.sh
```
Provisions 3-node EMR cluster. Note the cluster ID from output.

#### Step 4: Submit MapReduce Jobs
```bash
# Submit all three jobs
bash scripts/aws/submit_emr_jobs_mrjob.sh monthly
bash scripts/aws/submit_emr_jobs_mrjob.sh extreme
bash scripts/aws/submit_emr_jobs_mrjob.sh correlation

# Monitor job progress
aws emr describe-step --cluster-id j-XXXXXXXXXXXXX --step-id s-XXXXXXXXXXXXX
```

#### Step 5: Download Results
```bash
bash scripts/aws/download_results.sh
```
Syncs results from S3 to local `output/` directory.

#### Step 6: Terminate Cluster (IMPORTANT!)
```bash
bash scripts/aws/terminate_emr_cluster.sh
```
Terminates cluster to avoid ongoing charges.

### Detailed Deployment

For comprehensive deployment instructions including:
- AWS CLI installation (Windows/Linux/Mac)
- AWS credentials configuration (Academic accounts)
- MRJob configuration
- Manual AWS console setup
- Troubleshooting common issues

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for the complete guide.

### AWS Academic Account Notes

If using AWS Academy:
1. Get temporary credentials from AWS Details
2. Include `aws_session_token` in credentials file
3. Credentials expire after ~3 hours - refresh as needed
4. Use default region: us-east-1

## Results and Findings

### Dataset Overview
- **Records:** 1,095 daily observations
- **Period:** January 1, 2022 - December 31, 2024
- **Location:** Medellin, Colombia (6.25°N, 75.56°W)
- **Source:** Open-Meteo Historical Weather API

### Temperature Trends

**Warmest Period:**
- **Month:** May 2022
- **Average Max Temperature:** 29.15°C
- **Insight:** Peak of dry season

**Coolest Period:**
- **Month:** November 2022
- **Average Min Temperature:** 14.13°C
- **Insight:** Rainy season trough

**Overall Temperature Range:**
- **Maximum Temperatures:** 24.6°C - 29.15°C (monthly averages)
- **Minimum Temperatures:** 14.13°C - 16.75°C (monthly averages)
- **Characteristic:** Stable tropical climate with minimal seasonal variation

### Temperature Distribution

| Category | Days | Percentage | Description |
|----------|------|------------|-------------|
| Very Cool (< 20°C) | 6 | <1% | Rare cold fronts |
| Cool (20-27°C) | 380 | 35% | Pleasant weather |
| Normal (27-30°C) | 700 | 64% | Typical tropical |
| Very Hot (≥ 30°C) | 23 | 2% | Heat waves |

**Key Insight:** Medellin exhibits remarkable temperature stability, with 64% of days experiencing "normal" tropical temperatures (27-30°C). Extreme temperature events are rare.

### Temperature-Precipitation Correlation

**Correlation Range:** -0.64 to +0.14

**Pattern Analysis:**
- **Negative Correlation Months:** Temperature inversely related to precipitation (hotter = drier)
- **Positive Correlation Months:** Temperature directly related to precipitation (hotter = wetter)
- **Overall Trend:** Generally weak correlation, indicating complex climate dynamics

**Example Months:**
- **January 2022:** -0.31 (dry season pattern)
- **February 2022:** +0.14 (transition period)
- **October 2023:** -0.52 (strong inverse relationship)

### Climate Insights

1. **Stable Tropical Climate:** Medellin exhibits minimal seasonal temperature variation compared to temperate regions.

2. **Elevation Effect:** At 1,495m elevation, Medellin experiences cooler temperatures than typical equatorial locations.

3. **Bimodal Rainfall Pattern:** Weak temperature-precipitation correlations suggest complex interactions between Pacific/Caribbean weather systems.

4. **Heat Resilience:** Only 2% of days exceed 30°C, indicating natural climate moderation.

## Troubleshooting

### AWS EMR Issues

#### Problem: Cluster creation fails with "Invalid subnet"

**Solution:**
```bash
# Check available subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxxxxxxx"

# Use subnet from output in cluster creation
aws emr create-cluster --ec2-attributes SubnetId=subnet-xxxxxxxx ...
```

#### Problem: "Access Denied" when accessing S3

**Solution:**
```bash
# Verify AWS credentials
aws sts get-caller-identity

# Check S3 bucket permissions
aws s3api get-bucket-acl --bucket weatheria-climate-data

# Update bucket policy if needed
aws s3api put-bucket-policy --bucket weatheria-climate-data --policy file://policy.json
```

#### Problem: MapReduce job fails with "Python module not found"

**Solution:**
```bash
# Add bootstrap action to install dependencies
aws emr create-cluster \
 --bootstrap-actions Path=s3://weatheria-climate-data/scripts/bootstrap.sh
```

#### Problem: Session token expired (AWS Academy)

**Solution:**
1. Return to AWS Academy > Learner Lab
2. Click "AWS Details" > "Show" credentials
3. Update `~/.aws/credentials` with new token
4. Retry AWS command

### Backend API Issues

#### Problem: API returns 500 error when loading data

**Solution:**
```bash
# Check if CSV files exist
ls output/monthly_avg_fixed.csv output/extreme_temps_fixed.csv output/temp_precip_fixed.csv

# Verify CSV encoding (should be UTF-8)
file output/monthly_avg_fixed.csv

# Re-download results if corrupted
bash scripts/aws/download_results.sh
```

#### Problem: CORS errors when accessing from frontend

**Solution:**
Edit `src/api/config.py`:
```python
allow_origins = ["http://localhost:5173"] # Specify frontend URL
```

### Frontend Issues

#### Problem: Frontend shows "Failed to fetch" errors

**Solutions:**
1. **Verify backend is running:**
  ```bash
  curl http://localhost:8000/health
  ```

2. **Check API base URL in `src/services/api.ts`:**
  ```typescript
  const API_BASE_URL = 'http://localhost:8000';
  ```

3. **Check browser console for CORS errors** - see Backend API Issues above

#### Problem: npm install fails with dependency conflicts

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and lock file
rm -rf node_modules pnpm-lock.yaml

# Reinstall
npm install
```

#### Problem: Charts not rendering

**Solution:**
1. Open browser console (F12) - check for errors
2. Verify data format matches TypeScript interfaces
3. Ensure Recharts is installed: `npm list recharts`

### Data Download Issues

#### Problem: Open-Meteo API timeout

**Solution:**
```python
# In scripts/download_data.py, increase timeout
response = requests.get(url, timeout=60) # Increase from 30 to 60 seconds

# Add retry logic
from time import sleep
for attempt in range(3):
  try:
    response = requests.get(url, timeout=60)
    break
  except requests.Timeout:
    if attempt < 2:
      sleep(10)
    else:
      raise
```

### General Tips

- **Check logs:** EMR cluster logs in S3 (`s3://weatheria-climate-data/logs/`)
- **Monitor costs:** Use AWS Cost Explorer to track spending
- **Terminate clusters:** Always terminate EMR clusters after use
- **Use Git:** Commit changes frequently during development
- **Test locally:** Run MapReduce jobs with small data samples before EMR deployment

## References

### Data Source
- **Open-Meteo Historical Weather API:** [https://open-meteo.com/](https://open-meteo.com/)
- **Documentation:** [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api)

### Technologies
- **Apache Hadoop:** [https://hadoop.apache.org/](https://hadoop.apache.org/)
- **MRJob Documentation:** [https://mrjob.readthedocs.io/](https://mrjob.readthedocs.io/)
- **AWS EMR Guide:** [https://docs.aws.amazon.com/emr/](https://docs.aws.amazon.com/emr/)
- **FastAPI Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **React Documentation:** [https://react.dev/](https://react.dev/)
- **Recharts Documentation:** [https://recharts.org/](https://recharts.org/)

### Academic Resources
- White, T. (2015). *Hadoop: The Definitive Guide* (4th ed.). O'Reilly Media.
- Dean, J., & Ghemawat, S. (2008). MapReduce: Simplified Data Processing on Large Clusters. *Communications of the ACM*, 51(1), 107-113.