# Weatheria Climate Observatory
## Hadoop MapReduce System for Medellín Temperature Analysis (2022-2024)

### Project Overview
Academic project for EAFIT University (ST0263: Tópicos Especiales en Telemática, 2025-2)
**Due Date:** November 23, 2025
**Presentation:** November 24, 2025, 8:00 AM - 12:00 PM

Inspired by Weatheria, the sky island from One Piece dedicated to climate science research, this project implements a complete distributed batch processing pipeline using Hadoop MapReduce to analyze temperature patterns in Medellín, Colombia.

---

## Project Requirements

### Core Components
1. **Data Acquisition** (Manual)
   - Download climate data from open sources (CSV/JSON/text)
   - Source: Open-Meteo API for Medellín historical weather data
   - Time period: 2022-2024
   - Variables: temperature_2m_max, temperature_2m_min, precipitation_sum

2. **HDFS Loading**
   - Upload data to Hadoop Distributed File System
   - Can be done manually or via reproducible script
   - Deploy on cloud (AWS EMR recommended)

3. **MapReduce Processing**
   - Implement in Python (using MRJOB) or Java
   - Minimum one MapReduce job producing meaningful results
   - Analysis types: aggregation, filtering, counting, statistical analysis

4. **Results Output**
   - Store results back to HDFS
   - Export to CSV format
   - Serve via REST API (Flask or FastAPI)

5. **Deliverables**
   - GitHub repository with:
     - MapReduce code (.py or .java)
     - HDFS loading scripts
     - Sample input/output files
     - API code for visualization
     - Clear README.md with execution instructions
   - Sustentation video (max 10 minutes) explaining:
     - Data source and rationale
     - Loading process
     - MapReduce program explanation
     - Results obtained

---

## Technical Stack

### Development Environment
- **Local Testing:** Docker + Hadoop standalone/pseudo-distributed
- **Production:** AWS EMR (Elastic MapReduce)
- **Storage:** HDFS locally, S3 for AWS
- **Programming:** Python 3.9+
- **MapReduce Framework:** MRJOB
- **API Framework:** FastAPI
- **Data Processing:** pandas, numpy

### Tools & Services
- **Docker:** sequenceiq/hadoop-docker
- **AWS Services:** EMR, S3, EC2 (optional for API)
- **Version Control:** Git/GitHub
- **Testing:** pytest for unit tests

---

## Project Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   DATA ACQUISITION                       │
│  Open-Meteo API → Download CSV → Local Storage          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   HDFS LOADING                           │
│  Local CSV → hdfs dfs -put → /input/weather_data.csv    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                MAPREDUCE PROCESSING                      │
│  Mapper → Shuffle & Sort → Reducer                      │
│  Jobs:                                                   │
│    1. Monthly average temperature                       │
│    2. Extreme temperature days detection                │
│    3. Temperature-precipitation correlation             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   HDFS OUTPUT                            │
│  /output/part-00000 → hdfs dfs -get → results.csv       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   API ENDPOINT                           │
│  FastAPI serving results via HTTP endpoints             │
│  GET /results, GET /stats, GET /trends                  │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Setup & Data Acquisition (Days 1-2)

#### Tasks:
1. **Choose and download climate data**
   - Source: Open-Meteo Archive API
   - Location: Medellín (latitude: 6.25, longitude: -75.56)
   - Date range: 2022-01-01 to 2024-12-31
   - API endpoint example:
   ```
   https://archive-api.open-meteo.com/v1/archive?
   latitude=6.25&longitude=-75.56
   &start_date=2022-01-01&end_date=2024-12-31
   &daily=temperature_2m_max,temperature_2m_min,precipitation_sum
   &timezone=America/Bogota
   ```

2. **Setup local development environment**
   ```bash
   # Install Docker
   docker pull sequenceiq/hadoop-docker:2.7.1
   
   # Run Hadoop container
   docker run -it -p 8088:8088 -p 50070:50070 \
     --name hadoop sequenceiq/hadoop-docker:2.7.1 /etc/bootstrap.sh -bash
   
   # Install Python dependencies
   pip install mrjob pandas numpy requests
   ```

3. **Create project structure**
   ```
   weatheria-climate-observatory/
   ├── data/
   │   ├── raw/              # Downloaded CSV files
   │   └── processed/        # Cleaned data
   ├── src/
   │   ├── mapreduce/        # MapReduce jobs
   │   ├── api/              # FastAPI application
   │   └── utils/            # Helper scripts
   ├── scripts/
   │   ├── download_data.py  # Data acquisition script
   │   └── load_hdfs.sh      # HDFS loading script
   ├── tests/                # Unit tests
   ├── output/               # MapReduce results
   ├── docs/                 # Documentation
   ├── requirements.txt
   ├── README.md
   └── .gitignore
   ```

---

### Phase 2: MapReduce Development (Days 3-6)

#### Job 1: Monthly Average Temperature
**Objective:** Calculate average max and min temperatures per month

```python
# src/mapreduce/monthly_avg_temp.py
from mrjob.job import MRJob
from mrjob.step import MRStep
import csv
from datetime import datetime

class MonthlyAvgTemperature(MRJob):
    """
    MapReduce job to calculate monthly average temperatures
    Input: CSV with date, temp_max, temp_min
    Output: month, avg_temp_max, avg_temp_min
    """
    
    def mapper(self, _, line):
        """
        Emit (year-month, (temp_max, temp_min, 1))
        """
        # Parse CSV line
        # Extract date, temp_max, temp_min
        # Emit (year_month, (temp_max, temp_min, 1))
        pass
    
    def reducer(self, key, values):
        """
        Calculate average for each month
        """
        # Sum all temperatures and counts
        # Calculate averages
        # Emit results
        pass

if __name__ == '__main__':
    MonthlyAvgTemperature.run()
```

#### Job 2: Extreme Temperature Detection
**Objective:** Identify days with extreme temperatures (>30°C or <15°C)

```python
# src/mapreduce/extreme_temps.py
from mrjob.job import MRJob

class ExtremeTemperatures(MRJob):
    """
    Detect days with extreme temperature conditions
    """
    
    def mapper(self, _, line):
        """
        Filter extreme temperature days
        Emit category and date info
        """
        pass
    
    def reducer(self, category, values):
        """
        Count extreme days by category
        """
        pass
```

#### Job 3: Temperature-Precipitation Correlation
**Objective:** Analyze relationship between temperature and rainfall

```python
# src/mapreduce/temp_precipitation.py
from mrjob.job import MRJob
from mrjob.step import MRStep

class TempPrecipitationCorrelation(MRJob):
    """
    Analyze correlation between temperature and precipitation
    """
    
    def mapper(self, _, line):
        """
        Emit (month, (temp, precipitation))
        """
        pass
    
    def reducer(self, month, values):
        """
        Calculate correlation coefficient
        """
        pass
```

#### Testing Strategy:
1. **Unit tests** with sample data (10-100 rows)
2. **Local execution** with MRJOB's local runner
3. **Docker Hadoop** testing with medium dataset (1000 rows)
4. **AWS EMR** final execution with full dataset

---

### Phase 3: HDFS Integration (Days 7-8)

#### Local HDFS Setup:
```bash
# scripts/load_hdfs.sh

#!/bin/bash
# Load data to HDFS

# Create input directory
hdfs dfs -mkdir -p /user/hadoop/weatheria/input

# Upload CSV files
hdfs dfs -put data/raw/medellin_weather_2022-2024.csv \
  /user/hadoop/weatheria/input/

# Verify upload
hdfs dfs -ls /user/hadoop/weatheria/input

# Check file content
hdfs dfs -cat /user/hadoop/weatheria/input/medellin_weather_2022-2024.csv | head -n 10
```

#### Execute MapReduce on Hadoop:
```bash
# Run Job 1: Monthly averages
python src/mapreduce/monthly_avg_temp.py \
  -r hadoop \
  hdfs:///user/hadoop/weatheria/input/medellin_weather_2022-2024.csv \
  --output-dir hdfs:///user/hadoop/weatheria/output/monthly_avg

# Run Job 2: Extreme temperatures
python src/mapreduce/extreme_temps.py \
  -r hadoop \
  hdfs:///user/hadoop/weatheria/input/medellin_weather_2022-2024.csv \
  --output-dir hdfs:///user/hadoop/weatheria/output/extreme_temps

# Run Job 3: Temperature-precipitation
python src/mapreduce/temp_precipitation.py \
  -r hadoop \
  hdfs:///user/hadoop/weatheria/input/medellin_weather_2022-2024.csv \
  --output-dir hdfs:///user/hadoop/weatheria/output/temp_precip
```

#### Retrieve Results:
```bash
# Get results from HDFS
hdfs dfs -get /user/hadoop/weatheria/output/monthly_avg/part-00000 \
  output/monthly_avg_results.csv

hdfs dfs -get /user/hadoop/weatheria/output/extreme_temps/part-00000 \
  output/extreme_temps_results.csv

hdfs dfs -get /user/hadoop/weatheria/output/temp_precip/part-00000 \
  output/temp_precip_results.csv
```

---

### Phase 4: REST API Development (Days 9-10)

#### FastAPI Implementation:
```python
# src/api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
from typing import List, Dict
import os

app = FastAPI(
    title="Weatheria Climate Observatory API",
    description="API for accessing Medellín climate analysis results",
    version="1.0.0"
)

# Load results on startup
RESULTS_DIR = "output"

@app.get("/")
def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Weatheria Climate Observatory",
        "description": "MapReduce-based weather analysis for Medellín (2022-2024)",
        "endpoints": {
            "/monthly-avg": "Monthly average temperatures",
            "/extreme-temps": "Extreme temperature days",
            "/temp-precipitation": "Temperature-precipitation correlation",
            "/download/{result_type}": "Download CSV results"
        }
    }

@app.get("/monthly-avg")
def get_monthly_averages():
    """Get monthly average temperature results"""
    try:
        df = pd.read_csv(f"{RESULTS_DIR}/monthly_avg_results.csv", 
                        sep='\t', 
                        names=['month', 'avg_max', 'avg_min'])
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/extreme-temps")
def get_extreme_temperatures():
    """Get extreme temperature detection results"""
    try:
        df = pd.read_csv(f"{RESULTS_DIR}/extreme_temps_results.csv",
                        sep='\t',
                        names=['category', 'count'])
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/temp-precipitation")
def get_temp_precipitation():
    """Get temperature-precipitation correlation results"""
    try:
        df = pd.read_csv(f"{RESULTS_DIR}/temp_precip_results.csv",
                        sep='\t',
                        names=['month', 'correlation', 'avg_temp', 'avg_precip'])
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_statistics():
    """Get overall statistics"""
    try:
        monthly = pd.read_csv(f"{RESULTS_DIR}/monthly_avg_results.csv", sep='\t')
        return {
            "total_months_analyzed": len(monthly),
            "max_temperature": float(monthly['avg_max'].max()),
            "min_temperature": float(monthly['avg_min'].min()),
            "overall_avg": float(monthly['avg_max'].mean())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{result_type}")
def download_results(result_type: str):
    """Download CSV file of results"""
    file_mapping = {
        "monthly-avg": "monthly_avg_results.csv",
        "extreme-temps": "extreme_temps_results.csv",
        "temp-precipitation": "temp_precip_results.csv"
    }
    
    if result_type not in file_mapping:
        raise HTTPException(status_code=404, detail="Result type not found")
    
    file_path = f"{RESULTS_DIR}/{file_mapping[result_type]}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=file_mapping[result_type]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Run API:
```bash
# Install FastAPI dependencies
pip install fastapi uvicorn

# Run server
python src/api/main.py

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/monthly-avg
curl http://localhost:8000/stats
```

---

### Phase 5: AWS EMR Deployment (Days 11-13)

#### AWS S3 Setup:
```bash
# Create S3 bucket
aws s3 mb s3://weatheria-climate-data

# Upload data
aws s3 cp data/raw/medellin_weather_2022-2024.csv \
  s3://weatheria-climate-data/input/

# Upload MapReduce scripts
aws s3 cp src/mapreduce/ s3://weatheria-climate-data/scripts/ --recursive
```

#### Create EMR Cluster:
```bash
# Create cluster with Hadoop
aws emr create-cluster \
  --name "Weatheria Climate Observatory" \
  --release-label emr-6.10.0 \
  --applications Name=Hadoop Name=Hive \
  --ec2-attributes KeyName=my-key-pair \
  --instance-type m5.xlarge \
  --instance-count 3 \
  --use-default-roles \
  --log-uri s3://weatheria-climate-data/logs/

# Note the cluster ID (e.g., j-XXXXXXXXXXXXX)
```

#### Submit MapReduce Jobs:
```bash
# Job 1: Monthly averages
aws emr add-steps \
  --cluster-id j-XXXXXXXXXXXXX \
  --steps Type=STREAMING,Name="Monthly Avg Temperature",\
ActionOnFailure=CONTINUE,\
Args=[-files,s3://weatheria-climate-data/scripts/monthly_avg_temp.py,\
-mapper,monthly_avg_temp.py,\
-reducer,monthly_avg_temp.py,\
-input,s3://weatheria-climate-data/input/,\
-output,s3://weatheria-climate-data/output/monthly_avg/]

# Monitor job
aws emr describe-step --cluster-id j-XXXXXXXXXXXXX --step-id s-XXXXXXXXXXXXX

# Download results
aws s3 sync s3://weatheria-climate-data/output/ output/
```

#### Terminate Cluster (Important for cost savings!):
```bash
aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXXX
```

---

### Phase 6: Documentation & Video (Days 14-15)

#### README.md Structure:
```markdown
# Weatheria Climate Observatory

[Badge images: Python, Hadoop, AWS, FastAPI]

## Overview
Climate analysis system for Medellín using Hadoop MapReduce...

## Data Source
- Open-Meteo Archive API
- Location: Medellín, Colombia
- Period: 2022-2024
- Variables: temperature, precipitation

## Architecture
[Include architecture diagram]

## Installation
### Local Setup
[Step-by-step instructions]

### AWS Setup
[EMR deployment guide]

## Usage
### Run MapReduce Jobs
[Commands]

### Start API
[Commands]

### Access Results
[API endpoints]

## Results
[Include visualizations and key findings]

## Authors
[Your name and team]

## License
MIT
```

#### Video Script (10 minutes):
1. **Introduction (1 min)**
   - Project name and inspiration
   - Problem statement
   - Technology overview

2. **Data Source (1.5 min)**
   - Why Open-Meteo?
   - What data was collected
   - Show CSV sample

3. **HDFS Loading (1 min)**
   - Demonstrate data upload
   - Show HDFS directory structure

4. **MapReduce Explanation (4 min)**
   - Job 1: Monthly averages (code walkthrough)
   - Job 2: Extreme temperatures
   - Job 3: Correlation analysis
   - Show execution on Hadoop/EMR

5. **Results & API (2 min)**
   - Key findings
   - API demonstration
   - Access to results

6. **Conclusion (0.5 min)**
   - Summary of achievements
   - Future improvements

---

## Data Download Script

```python
# scripts/download_data.py
import requests
import pandas as pd
from datetime import datetime

def download_medellin_weather(start_date, end_date, output_file):
    """
    Download weather data from Open-Meteo for Medellín
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        output_file: Path to save CSV file
    """
    
    # Medellín coordinates
    latitude = 6.25
    longitude = -75.56
    
    # API endpoint
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "America/Bogota"
    }
    
    print(f"Downloading weather data for Medellín...")
    print(f"Period: {start_date} to {end_date}")
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': data['daily']['time'],
            'temp_max': data['daily']['temperature_2m_max'],
            'temp_min': data['daily']['temperature_2m_min'],
            'precipitation': data['daily']['precipitation_sum']
        })
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"✓ Data saved to {output_file}")
        print(f"Total records: {len(df)}")
        
        # Show sample
        print("\nSample data:")
        print(df.head())
        
        return df
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    download_medellin_weather(
        start_date="2022-01-01",
        end_date="2024-12-31",
        output_file="data/raw/medellin_weather_2022-2024.csv"
    )
```

---

## Testing Checklist

### Local Testing:
- [ ] Data download script works
- [ ] CSV file is properly formatted
- [ ] MapReduce jobs run with `mrjob` local runner
- [ ] Results are correct with sample data
- [ ] HDFS upload/download works in Docker
- [ ] MapReduce executes on Hadoop in Docker
- [ ] API starts and serves results
- [ ] All endpoints return correct data

### AWS Testing:
- [ ] S3 bucket created and accessible
- [ ] Data uploaded to S3
- [ ] EMR cluster launches successfully
- [ ] MapReduce jobs execute on EMR
- [ ] Results written to S3
- [ ] Results downloadable from S3
- [ ] Cluster terminates properly

### Documentation:
- [ ] README.md is complete
- [ ] All code is commented
- [ ] Requirements.txt is up to date
- [ ] .gitignore includes sensitive files
- [ ] Sample input/output files included
- [ ] Video recorded and uploaded

---

## Cost Estimation (AWS)

### EMR Cluster:
- Instance type: m5.xlarge
- Count: 3 nodes (1 master + 2 core)
- Cost: ~$0.50/hour per node = $1.50/hour total
- Estimated runtime: 2-3 hours for testing
- **Total: $3-5**

### S3 Storage:
- Data size: ~10-50 MB
- Cost: Negligible (under $0.01)

### **Total Project Cost: ~$5-10**

**Tip:** Use spot instances to reduce costs by 70%!

---

## Troubleshooting

### Common Issues:

1. **MRJOB not finding Hadoop**
   ```bash
   export HADOOP_HOME=/usr/local/hadoop
   export PATH=$PATH:$HADOOP_HOME/bin
   ```

2. **Python 2 vs Python 3 in Hadoop**
   ```bash
   # Use python3 explicitly
   python3 src/mapreduce/job.py -r hadoop hdfs:///input/data.csv
   ```

3. **HDFS permission denied**
   ```bash
   hdfs dfs -chmod 777 /user/hadoop/weatheria
   ```

4. **EMR job fails**
   - Check CloudWatch logs
   - Verify S3 paths are correct
   - Ensure Python script has no syntax errors

5. **API can't find output files**
   ```bash
   # Ensure output directory exists and contains CSV files
   ls -la output/
   ```

---

## Future Enhancements

1. **Advanced Analytics:**
   - Implement climate change trend detection
   - Add seasonal pattern analysis
   - Create predictive models

2. **Visualization:**
   - Add Plotly/Matplotlib charts to API
   - Create interactive dashboard
   - Generate PDF reports

3. **Automation:**
   - Schedule daily data updates
   - Automated EMR job execution
   - CI/CD pipeline with GitHub Actions

4. **Scalability:**
   - Process multiple cities simultaneously
   - Expand to entire Colombia
   - Compare with global climate data

---

## References

- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [MRJOB Documentation](https://mrjob.readthedocs.io/)
- [Hadoop Documentation](https://hadoop.apache.org/docs/)
- [AWS EMR Guide](https://docs.aws.amazon.com/emr/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [One Piece Wiki - Weatheria](https://onepiece.fandom.com/wiki/Weatheria)

---

## Project Timeline

| Phase | Days | Status |
|-------|------|--------|
| Setup & Data Acquisition | 1-2 | ⏳ |
| MapReduce Development | 3-6 | ⏳ |
| HDFS Integration | 7-8 | ⏳ |
| API Development | 9-10 | ⏳ |
| AWS Deployment | 11-13 | ⏳ |
| Documentation & Video | 14-15 | ⏳ |

**Total Duration:** 15 days
**Buffer:** 3 days before deadline

---

## Success Criteria

✓ Data successfully loaded to HDFS
✓ At least 3 MapReduce jobs implemented and executed
✓ Results stored in HDFS and exported to CSV
✓ Functional API serving results
✓ Complete GitHub repository
✓ 10-minute sustentation video
✓ Clear documentation in README

---

## Contact & Support

For questions or issues:
- Create a GitHub issue in the repository
- Contact the course professor
- Review Hadoop/MRJOB documentation


**Inspired by Weatheria - Where Science Meets the Clouds** ☁️🌡️

*"In the world of One Piece, Weatheria is a floating island where scientists study weather patterns. In our world, this project brings that same spirit of climate research using modern distributed computing technologies."*
