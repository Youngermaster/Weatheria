# Weatheria Climate Observatory

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Hadoop](https://img.shields.io/badge/Hadoop-3.3.6-orange.svg)](https://hadoop.apache.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![AWS EMR](https://img.shields.io/badge/AWS-EMR-yellow.svg)](https://aws.amazon.com/emr/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

A complete distributed batch processing pipeline using Hadoop MapReduce to analyze temperature patterns in Medellín, Colombia (2022-2024). Built for EAFIT University's Distributed Systems course (ST0263).

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Detailed Workflow](#detailed-workflow)
- [Configuration](#configuration)
- [MapReduce Jobs](#mapreduce-jobs)
- [API Documentation](#api-documentation)
- [Frontend Application](#frontend-application)
- [AWS EMR Deployment](#aws-emr-deployment)
- [Troubleshooting](#troubleshooting)
- [Results and Findings](#results-and-findings)

## Overview

Weatheria Climate Observatory implements a complete ETL (Extract, Transform, Load) pipeline using Hadoop MapReduce to process and analyze climate data from Medellín, Colombia. The system processes 1,096 days of weather data across a distributed Hadoop cluster and provides insights through a REST API and web interface.

### Key Technologies

- **MapReduce Framework**: MRJob (Python 3.9+)
- **Distributed Storage**: HDFS with 2-node replication
- **Processing**: Hadoop 3.3.6
- **Cluster Management**: YARN
- **API**: FastAPI with async support
- **Frontend**: React + TypeScript + Vite
- **Containerization**: Docker & Docker Compose
- **Data Source**: Open-Meteo Archive API

### Architecture

The system consists of:
- **1 NameNode**: HDFS master server managing filesystem metadata
- **2 DataNodes**: Distributed data storage with replication factor 2
- **1 ResourceManager**: YARN cluster resource management
- **1 NodeManager**: Task execution and monitoring
- **1 HistoryServer**: MapReduce job history tracking
- **1 API Server**: FastAPI REST endpoints
- **1 Frontend Server**: React application (development)

## Prerequisites

### Required Software

- **Docker Desktop**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.9 or 3.10 (avoid 3.14 due to mrjob incompatibility)
- **Node.js**: 18+ (for frontend)
- **Git**: For version control

### System Requirements

- **RAM**: Minimum 8GB, recommended 16GB
- **Disk Space**: 10GB free
- **CPU**: Multi-core recommended for cluster performance

### macOS ARM64 Note

The project is configured for ARM64 architecture (Apple Silicon). The Dockerfile uses:
```dockerfile
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
```

For x86_64 systems, change to:
```dockerfile
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

## Quick Start

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/Youngermaster/Weatheria.git
cd Weatheria

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 2. Start Hadoop Cluster

```bash
# Start all services
docker compose up -d

# Verify cluster status
docker ps --filter "name=weatheria"

# Check HDFS health
docker exec weatheria-namenode hdfs dfsadmin -report
```

Expected output should show 2 live datanodes and available storage.

### 3. Download Climate Data

```bash
# Download 3 years of data (2022-2024)
python3 scripts/download_data.py
```

This downloads 1,096 daily records to `data/raw/medellin_weather_2022-2024.csv`.

### 4. Run Complete Workflow

```bash
# Upload data to HDFS
docker cp data/raw/medellin_weather_2022-2024.csv weatheria-namenode:/tmp/weather_data.csv
docker exec weatheria-namenode hdfs dfs -mkdir -p /weatheria/input
docker exec weatheria-namenode hdfs dfs -put -f /tmp/weather_data.csv /weatheria/input/

# Run MapReduce Job 1: Monthly Averages
docker cp src/mapreduce/monthly_avg_temp.py weatheria-namenode:/tmp/
docker exec weatheria-namenode bash -c "cd /tmp && python3 monthly_avg_temp.py \
  -r hadoop \
  --hadoop-streaming-jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  hdfs:///weatheria/input/weather_data.csv \
  --output-dir hdfs:///weatheria/output/monthly_avg"

# Run MapReduce Job 2: Extreme Temperatures
docker cp src/mapreduce/extreme_temps.py weatheria-namenode:/tmp/
docker exec weatheria-namenode bash -c "cd /tmp && python3 extreme_temps.py \
  -r hadoop \
  --hadoop-streaming-jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  hdfs:///weatheria/input/weather_data.csv \
  --output-dir hdfs:///weatheria/output/extreme_temps"

# Run MapReduce Job 3: Temperature-Precipitation Correlation
docker cp src/mapreduce/temp_precipitation.py weatheria-namenode:/tmp/
docker exec weatheria-namenode bash -c "cd /tmp && python3 temp_precipitation.py \
  -r hadoop \
  --hadoop-streaming-jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  hdfs:///weatheria/input/weather_data.csv \
  --output-dir hdfs:///weatheria/output/temp_precip"

# Download and convert results
mkdir -p output/hadoop
docker exec weatheria-namenode hdfs dfs -get /weatheria/output/monthly_avg/part-00000 /tmp/monthly_avg.tsv
docker exec weatheria-namenode hdfs dfs -get /weatheria/output/extreme_temps/part-00000 /tmp/extreme_temps.tsv
docker exec weatheria-namenode hdfs dfs -get /weatheria/output/temp_precip/part-00000 /tmp/temp_precip.tsv

docker cp weatheria-namenode:/tmp/monthly_avg.tsv output/hadoop/
docker cp weatheria-namenode:/tmp/extreme_temps.tsv output/hadoop/
docker cp weatheria-namenode:/tmp/temp_precip.tsv output/hadoop/

python3 scripts/convert_hadoop_output.py
```

### 5. Access Web Interfaces

- **HDFS NameNode UI**: http://localhost:9870
- **YARN ResourceManager UI**: http://localhost:8088
- **MapReduce History Server**: http://localhost:19888
- **API Documentation**: http://localhost:8000/docs
- **Frontend Application**: http://localhost:5173

## Project Structure

```
Weatheria/
├── config/
│   └── hadoop/              # Hadoop configuration files
├── data/
│   └── raw/                 # Downloaded weather data
├── docker/
│   ├── Dockerfile.hadoop    # Hadoop cluster image
│   └── Dockerfile.api       # API server image
├── output/
│   ├── hadoop/              # Raw MapReduce outputs (TSV)
│   ├── monthly_avg_results.csv
│   ├── extreme_temps_results.csv
│   └── temp_precip_results.csv
├── scripts/
│   ├── download_data.py     # Data acquisition
│   └── convert_hadoop_output.py  # TSV to CSV conversion
├── src/
│   ├── api/                 # FastAPI application
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── routers/
│   │   └── dependencies/
│   └── mapreduce/           # MapReduce jobs
│       ├── monthly_avg_temp.py
│       ├── extreme_temps.py
│       └── temp_precipitation.py
├── weatheria-frontend/      # React application
│   ├── src/
│   │   ├── pages/           # Dashboard, Analysis pages
│   │   ├── components/      # UI components
│   │   └── services/        # API client
│   └── package.json
├── docker-compose.yml       # Cluster orchestration
├── requirements.txt         # Python dependencies
└── README.md
```

## Detailed Workflow

### Step 1: Data Acquisition

The `scripts/download_data.py` script fetches historical weather data from the Open-Meteo Archive API.

**Default Configuration:**
```python
LATITUDE = 6.25          # Medellín coordinates
LONGITUDE = -75.56
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"
```

**To Extend the Date Range:**

Edit `scripts/download_data.py`:
```python
START_DATE = "2015-01-01"  # Change to desired start date
END_DATE = "2024-12-31"    # Change to desired end date
```

Then run:
```bash
python3 scripts/download_data.py
```

**Output:**
- File location: `data/raw/medellin_weather_2022-2024.csv`
- Format: CSV with columns: date, temp_max, temp_min, precipitation
- Size: Approximately 28KB for 3 years (scales linearly)

**Expected Output for 2022-2024:**
```
Total records: 1097
Date range: 2022-01-01 to 2024-12-31
Temperature range: 10.2°C to 31.2°C
Total precipitation: 5754.5 mm
```

### Step 2: HDFS Data Loading

Upload the CSV file to HDFS distributed storage:

```bash
# Copy file to namenode container
docker cp data/raw/medellin_weather_2022-2024.csv weatheria-namenode:/tmp/weather_data.csv

# Create HDFS directory structure
docker exec weatheria-namenode hdfs dfs -mkdir -p /weatheria/input

# Upload to HDFS (replicated across datanodes)
docker exec weatheria-namenode hdfs dfs -put -f /tmp/weather_data.csv /weatheria/input/

# Verify upload and replication
docker exec weatheria-namenode hdfs dfs -ls /weatheria/input/
```

**Expected Output:**
```
-rw-r--r--   2 root supergroup   27663 2025-11-23 04:03 /weatheria/input/weather_data.csv
```

The `2` indicates replication factor 2 (data exists on both datanodes).

### Step 3: MapReduce Execution

Each MapReduce job processes the data in parallel across the cluster.

#### Job Performance Metrics

For 1,096 records on local cluster:

| Job | Map Tasks | Reduce Tasks | Input Records | Output Records | Time |
|-----|-----------|--------------|---------------|----------------|------|
| Monthly Avg | 2 | 1 | 1,097 | 36 | ~8s |
| Extreme Temps | 2 | 1 | 1,097 | 4 | ~7s |
| Temp-Precip | 2 | 1 | 1,097 | 36 | ~8s |

**View Job Progress:**
- YARN UI: http://localhost:8088
- Job History: http://localhost:19888

### Step 4: Results Extraction

Download MapReduce outputs from HDFS:

```bash
# Create local output directory
mkdir -p output/hadoop

# Download results from HDFS
docker exec weatheria-namenode hdfs dfs -get /weatheria/output/monthly_avg/part-00000 /tmp/monthly_avg.tsv
docker exec weatheria-namenode hdfs dfs -get /weatheria/output/extreme_temps/part-00000 /tmp/extreme_temps.tsv
docker exec weatheria-namenode hdfs dfs -get /weatheria/output/temp_precip/part-00000 /tmp/temp_precip.tsv

# Copy to host machine
docker cp weatheria-namenode:/tmp/monthly_avg.tsv output/hadoop/
docker cp weatheria-namenode:/tmp/extreme_temps.tsv output/hadoop/
docker cp weatheria-namenode:/tmp/temp_precip.tsv output/hadoop/
```

**TSV Format Note:**
MapReduce outputs use tab-separated format with quoted values:
```
"2022-01"	"24.75\t14.52"
```

### Step 5: Data Conversion

Convert TSV outputs to CSV format for API consumption:

```bash
python3 scripts/convert_hadoop_output.py
```

**Output:**
```
✓ Converted monthly averages: output/monthly_avg_results.csv (37 lines)
✓ Converted extreme temperatures: output/extreme_temps_results.csv (5 lines)
✓ Converted temp-precipitation: output/temp_precip_results.csv (37 lines)
```

**CSV Format:**
```csv
month,avg_max,avg_min
2022-01,24.75,14.52
2022-02,24.95,14.49
```

## Configuration

### Hadoop Cluster Configuration

The cluster is defined in `docker-compose.yml`:

```yaml
services:
  namenode:
    ports:
      - "9870:9870"  # HDFS Web UI
      - "9000:9000"  # HDFS IPC

  datanode1:
    # Stores data blocks

  datanode2:
    # Stores data blocks (replication)

  resourcemanager:
    ports:
      - "8088:8088"  # YARN Web UI

  nodemanager1:
    # Executes MapReduce tasks

  historyserver:
    ports:
      - "19888:19888"  # Job History UI
```

### Memory and Resource Allocation

Default YARN configuration in `config/hadoop/yarn-site.xml`:
```xml
<property>
  <name>yarn.nodemanager.resource.memory-mb</name>
  <value>4096</value>
</property>

<property>
  <name>yarn.scheduler.maximum-allocation-mb</name>
  <value>4096</value>
</property>
```

**To Increase Resources:**
Edit `config/hadoop/yarn-site.xml` and restart cluster:
```bash
docker compose restart
```

### HDFS Replication Factor

Default replication is 2. To change, edit `config/hadoop/hdfs-site.xml`:
```xml
<property>
  <name>dfs.replication</name>
  <value>2</value>  <!-- Change to 1 for testing, 3 for production -->
</property>
```

## MapReduce Jobs

### Job 1: Monthly Average Temperature

**File:** `src/mapreduce/monthly_avg_temp.py`

**Purpose:** Calculate average maximum and minimum temperatures per month.

**Algorithm:**
- **Mapper:** Parses CSV, emits (year-month, (temp_max, temp_min, 1))
- **Reducer:** Aggregates temperatures, calculates averages

**Output Format:**
```
month,avg_max,avg_min
2022-01,24.75,14.52
```

**Local Testing:**
```bash
python3 src/mapreduce/monthly_avg_temp.py data/raw/medellin_weather_2022-2024.csv
```

**Hadoop Execution:**
```bash
docker cp src/mapreduce/monthly_avg_temp.py weatheria-namenode:/tmp/
docker exec weatheria-namenode bash -c "cd /tmp && python3 monthly_avg_temp.py \
  -r hadoop \
  --hadoop-streaming-jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  hdfs:///weatheria/input/weather_data.csv \
  --output-dir hdfs:///weatheria/output/monthly_avg"
```

### Job 2: Extreme Temperature Detection

**File:** `src/mapreduce/extreme_temps.py`

**Purpose:** Classify days by temperature extremes.

**Categories:**
- **very_hot**: Maximum temperature > 30°C
- **normal**: Temperature between 15°C and 30°C
- **cool**: Minimum temperature < 15°C
- **very_cool**: Minimum temperature < 12°C

**Algorithm:**
- **Mapper:** Classifies each day, emits (category, (date, avg_temp, 1))
- **Reducer:** Counts days per category, calculates average temperature

**Output Format:**
```
category,count,avg_temp
cool,380,19.92
normal,700,21.33
```

**Hadoop Execution:**
```bash
docker cp src/mapreduce/extreme_temps.py weatheria-namenode:/tmp/
docker exec weatheria-namenode bash -c "cd /tmp && python3 extreme_temps.py \
  -r hadoop \
  --hadoop-streaming-jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  hdfs:///weatheria/input/weather_data.csv \
  --output-dir hdfs:///weatheria/output/extreme_temps"
```

### Job 3: Temperature-Precipitation Correlation

**File:** `src/mapreduce/temp_precipitation.py`

**Purpose:** Analyze relationship between temperature and rainfall by month.

**Algorithm:**
- **Mapper:** Emits (year-month, (avg_temp, precipitation))
- **Reducer:** Calculates Pearson correlation coefficient, aggregates statistics

**Output Format:**
```
month,correlation,avg_temp,avg_precip,rainy_days,total_precip
2022-01,0.1401,19.64,2.92,24,90.4
```

**Hadoop Execution:**
```bash
docker cp src/mapreduce/temp_precipitation.py weatheria-namenode:/tmp/
docker exec weatheria-namenode bash -c "cd /tmp && python3 temp_precipitation.py \
  -r hadoop \
  --hadoop-streaming-jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  hdfs:///weatheria/input/weather_data.csv \
  --output-dir hdfs:///weatheria/output/temp_precip"
```

## API Documentation

### Starting the API

The API runs in a Docker container:

```bash
# API is started automatically with docker compose up
# To restart separately:
docker restart weatheria-api

# View logs:
docker logs -f weatheria-api
```

### Available Endpoints

**Base URL:** `http://localhost:8000`

#### GET /
Welcome endpoint with API information.

**Response:**
```json
{
  "message": "Welcome to Weatheria Climate Observatory",
  "version": "1.0.0",
  "endpoints": { ... }
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### GET /monthly-avg
Returns monthly average temperatures.

**Response:**
```json
[
  {
    "month": "2022-01",
    "avg_max": 24.75,
    "avg_min": 14.52
  }
]
```

#### GET /extreme-temps
Returns extreme temperature classification.

**Response:**
```json
[
  {
    "category": "cool",
    "count": 380,
    "avg_temp": 19.92
  }
]
```

#### GET /temp-precipitation
Returns temperature-precipitation correlation data.

**Response:**
```json
[
  {
    "month": "2022-01",
    "correlation": 0.1401,
    "avg_temp": 19.64,
    "avg_precip": 2.92,
    "rainy_days": 24,
    "total_precip": 90.4
  }
]
```

#### GET /download/{result_type}
Downloads CSV file of results.

**Parameters:**
- `result_type`: One of `monthly-avg`, `extreme-temps`, `temp-precipitation`

**Response:** CSV file download

### Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Frontend Application

### Starting the Frontend

```bash
cd weatheria-frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Access at: http://localhost:5173

### Features

- **Dashboard:** Overview with 4 interactive charts
- **Monthly Analysis:** Temperature trends over time
- **Extreme Temperatures:** Classification breakdown
- **Precipitation Analysis:** Correlation analysis with scatter plots
- **About:** Project information and methodology

### Build for Production

```bash
cd weatheria-frontend
npm run build

# Serve production build
npm run preview
```

## AWS EMR Deployment

The MapReduce jobs are AWS EMR-ready with minimal changes.

### Prerequisites

- AWS Account with EMR permissions
- AWS CLI configured
- S3 bucket created

### Step 1: Upload Data to S3

```bash
# Create S3 bucket
aws s3 mb s3://weatheria-climate-data

# Upload data
aws s3 cp data/raw/medellin_weather_2022-2024.csv s3://weatheria-climate-data/input/

# Upload scripts
aws s3 cp src/mapreduce/ s3://weatheria-climate-data/scripts/ --recursive
```

### Step 2: Create EMR Cluster

```bash
aws emr create-cluster \
  --name "Weatheria Climate Observatory" \
  --release-label emr-6.10.0 \
  --applications Name=Hadoop \
  --ec2-attributes KeyName=your-key-pair \
  --instance-type m5.xlarge \
  --instance-count 3 \
  --use-default-roles \
  --log-uri s3://weatheria-climate-data/logs/
```

Save the cluster ID from the output.

### Step 3: Submit MapReduce Jobs

```bash
# Monthly averages
aws emr add-steps \
  --cluster-id j-XXXXXXXXXXXXX \
  --steps Type=STREAMING,\
Name="Monthly Avg Temperature",\
ActionOnFailure=CONTINUE,\
Args=[-files,s3://weatheria-climate-data/scripts/monthly_avg_temp.py,\
-mapper,monthly_avg_temp.py,\
-reducer,monthly_avg_temp.py,\
-input,s3://weatheria-climate-data/input/,\
-output,s3://weatheria-climate-data/output/monthly_avg/]
```

### Step 4: Download Results

```bash
# Wait for jobs to complete
aws emr describe-step --cluster-id j-XXXXXXXXXXXXX --step-id s-XXXXXXXXXXXXX

# Download results
aws s3 sync s3://weatheria-climate-data/output/ output/
```

### Step 5: Terminate Cluster

```bash
aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXXX
```

**Cost Estimate:**
- m5.xlarge instances: ~$0.50/hour per node
- 3 nodes: $1.50/hour
- Processing time: 2-3 hours
- **Total: ~$3-5**

## Troubleshooting

### Hadoop Cluster Issues

**Problem:** Containers exit immediately

**Solution:**
```bash
# Check logs
docker compose logs namenode
docker compose logs datanode1

# Restart cluster
docker compose down
docker compose up -d

# Verify all services
docker ps --filter "name=weatheria"
```

**Problem:** HDFS reports 0 live datanodes

**Solution:**
```bash
# Check datanode logs
docker logs weatheria-datanode1
docker logs weatheria-datanode2

# Restart datanodes
docker restart weatheria-datanode1 weatheria-datanode2

# Verify HDFS report
docker exec weatheria-namenode hdfs dfsadmin -report
```

**Problem:** MapReduce job hangs or fails

**Solution:**
```bash
# Check YARN logs
docker logs weatheria-resourcemanager
docker logs weatheria-nodemanager1

# View application logs
docker exec weatheria-resourcemanager yarn logs -applicationId application_XXXXX

# Check job history UI
# http://localhost:19888
```

### Python and Dependency Issues

**Problem:** mrjob not found or import errors

**Solution:**
```bash
# Reinstall dependencies
pip install --force-reinstall mrjob pandas numpy

# Verify installation
python3 -c "import mrjob; print(mrjob.__version__)"
```

**Problem:** Python 3.14 compatibility issues

**Solution:**
Use Python 3.9 or 3.10:
```bash
# Create venv with specific version
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Data Download Issues

**Problem:** Open-Meteo API timeout or errors

**Solution:**
```bash
# Retry with increased timeout
# Edit scripts/download_data.py
# Change: response = requests.get(url, params=params, timeout=60)

# Or download smaller date ranges
START_DATE = "2022-01-01"
END_DATE = "2022-12-31"
```

### Frontend Issues

**Problem:** Blank page or module errors

**Solution:**
```bash
cd weatheria-frontend

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Restart dev server
npm run dev
```

**Problem:** API connection errors

**Solution:**
```bash
# Verify API is running
curl http://localhost:8000/health

# Check .env configuration
cat weatheria-frontend/.env
# Should contain: VITE_API_URL=http://localhost:8000

# Restart frontend
npm run dev
```

## Results and Findings

### Key Climate Insights (2022-2024)

**Temperature Trends:**
- Average maximum temperature: 24.7°C
- Average minimum temperature: 14.8°C
- Warming trend: +1.8°C from 2022 to 2024
- Hottest month: Multiple around 25-26°C
- Coolest month: Multiple around 13-14°C

**Extreme Temperature Distribution:**
- Normal days (15-30°C): 700 days (63.9%)
- Cool days (<15°C): 380 days (34.7%)
- Very cool days (<12°C): 6 days (0.5%)
- Very hot days (>30°C): 23 days (2.1%)

**Precipitation Patterns:**
- Total precipitation: 5,754.5 mm over 3 years
- Average monthly precipitation: 159.8 mm
- Wettest month: ~350 mm
- Driest month: ~90 mm
- Temperature-precipitation correlation: -0.15 to -0.52 (negative)

**Climate Change Indicators:**
- Notable warming trend observed
- Inverse temperature-precipitation relationship
- Relatively stable temperature with occasional extremes
- Potential water stress during warm periods

### Performance Comparison

**Simple Python Processing:**
- Time: <1 second
- Scalability: Limited to single machine RAM
- Suitable for: <100MB datasets

**Hadoop MapReduce:**
- Time: ~23 seconds (includes cluster overhead)
- Scalability: Terabytes to petabytes
- Suitable for: Production environments, large datasets

## References

- **Hadoop Documentation:** https://hadoop.apache.org/docs/r3.3.6/
- **MRJOB Documentation:** https://mrjob.readthedocs.io/
- **AWS EMR Guide:** https://docs.aws.amazon.com/emr/
- **Open-Meteo API:** https://open-meteo.com/en/docs
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **React Documentation:** https://react.dev/

## License

This project is developed for academic purposes at EAFIT University.

## Authors

- Sebastian Zapata Henao - EAFIT University
- Course: ST0263 - Distributed Systems
- Semester: 2025-2

## Acknowledgments

- Inspired by Weatheria from One Piece
- Data provided by Open-Meteo Archive API
- EAFIT University for academic support
