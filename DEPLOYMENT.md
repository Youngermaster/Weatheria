# AWS EMR Deployment Guide

Complete guide for deploying Weatheria MapReduce jobs on AWS EMR.

## Prerequisites

- AWS Academic Account (or standard AWS account)
- Python 3.11+ installed locally
- AWS CLI installed
- Git Bash (Windows) or standard terminal (Linux/Mac)
- Basic knowledge of terminal commands

## Quick Deployment

```bash
# 1. Configure AWS credentials
aws configure

# 2. Download weather data
python scripts/download_data.py

# 3. Create S3 bucket and upload data
bash scripts/aws/setup_s3.sh

# 4. Create EMR cluster
bash scripts/aws/create_emr_cluster.sh

# 5. Submit MapReduce jobs
bash scripts/aws/submit_emr_jobs_mrjob.sh monthly
bash scripts/aws/submit_emr_jobs_mrjob.sh extreme
bash scripts/aws/submit_emr_jobs_mrjob.sh correlation

# 6. Download results
bash scripts/aws/download_results.sh

# 7. Terminate cluster (IMPORTANT)
bash scripts/aws/terminate_emr_cluster.sh
```

## Detailed Steps

### 1. AWS CLI Installation

**Windows:**
```powershell
# Download and install
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Verify
aws --version
```

**Linux/Mac:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify
aws --version
```

### 2. AWS Credentials Configuration

**For AWS Academic Accounts:**

AWS Academy provides temporary credentials with session tokens. Get them from:
1. AWS Academy > Modules > Learner Lab
2. Click "AWS Details"
3. Click "Show" under AWS CLI credentials
4. Copy the credentials

Create/edit `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
aws_session_token = YOUR_SESSION_TOKEN
```

Create/edit `~/.aws/config`:
```ini
[default]
region = us-east-1
output = json
```

**Test configuration:**
```bash
aws sts get-caller-identity
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- mrjob==0.7.4
- boto3
- pandas
- numpy
- requests
- fastapi
- uvicorn

### 4. Configure MRJob

Create `~/.mrjob.conf`:
```yaml
runners:
  emr:
    region: us-east-1
    ec2_key_pair_file: null
    cleanup: ALL
    pool_wait_minutes: 0
```

### 5. Download Weather Data

```bash
python scripts/download_data.py
```

This downloads 3 years of daily weather data from Open-Meteo API for Medellin, Colombia.

**Output:** `data/raw/medellin_weather_2022-2024.csv` (1095 records)

### 6. Setup S3 Bucket

```bash
bash scripts/aws/setup_s3.sh
```

This script:
- Creates S3 bucket `weatheria-climate-data`
- Creates folder structure: /input/, /output/, /scripts/, /logs/
- Uploads weather data to S3
- Uploads MapReduce scripts to S3

**Verify:**
```bash
aws s3 ls s3://weatheria-climate-data/ --recursive
```

### 7. Create EMR Cluster

```bash
bash scripts/aws/create_emr_cluster.sh
```

Cluster configuration:
- EMR Version: 6.10.0
- Applications: Hadoop, Hive, Spark
- Instances: 3 nodes (1 master + 2 core)
- Instance Type: m5.xlarge
- Region: us-east-1

**Cost:** Approximately $1.50/hour

The script saves the cluster ID to `.emr_cluster_id` file.

**Monitor cluster:**
```bash
# Check status
aws emr describe-cluster --cluster-id $(cat .emr_cluster_id) --query 'Cluster.Status.State'

# View in AWS Console
# https://console.aws.amazon.com/emr/
```

Wait until cluster status is "WAITING" (typically 5-10 minutes).

### 8. Submit MapReduce Jobs

The project includes three MapReduce jobs. Submit them using:

```bash
# Monthly average temperatures
bash scripts/aws/submit_emr_jobs_mrjob.sh monthly

# Extreme temperature detection
bash scripts/aws/submit_emr_jobs_mrjob.sh extreme

# Temperature-precipitation correlation
bash scripts/aws/submit_emr_jobs_mrjob.sh correlation
```

Each job:
- Uses MRJob's native EMR runner (`-r emr`)
- Processes data from S3 input path
- Writes results to S3 output path
- Takes 15-40 seconds to complete

**Monitor jobs:**
```bash
# List all steps
aws emr list-steps --cluster-id $(cat .emr_cluster_id)

# Check specific step
aws emr describe-step --cluster-id $(cat .emr_cluster_id) --step-id <step-id>
```

### 9. Download Results

```bash
bash scripts/aws/download_results.sh
```

This downloads all MapReduce results from S3 to `output/` directory and fixes file encoding.

Results files:
- `output/monthly_avg_fixed.csv`
- `output/extreme_temps_fixed.csv`
- `output/temp_precip_fixed.csv`

### 10. Test API with Results

```bash
cd src
uvicorn api.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` to test endpoints.

### 11. Terminate Cluster (CRITICAL)

**Always terminate the cluster when done to avoid charges:**

```bash
bash scripts/aws/terminate_emr_cluster.sh
```

**Verify termination:**
```bash
aws emr describe-cluster --cluster-id $(cat .emr_cluster_id) --query 'Cluster.Status.State'
```

Should show "TERMINATING" or "TERMINATED".

## Troubleshooting

### Issue: "Credentials not configured"

**Solution:** Ensure AWS credentials are properly set in `~/.aws/credentials`. For Academic accounts, include the `aws_session_token`.

### Issue: "S3 bucket already exists"

**Solution:** S3 bucket names are globally unique. Edit `scripts/aws/setup_s3.sh` and change `BUCKET_NAME` to something unique (e.g., add your initials).

### Issue: "Cluster creation failed"

**Possible causes:**
- Insufficient AWS permissions
- Region quota limits
- Invalid instance types

**Solution:** Check AWS console for error details or try a different region.

### Issue: "Job failed with code 1"

**Solution:** Check job logs:
```bash
aws emr list-steps --cluster-id $(cat .emr_cluster_id)
aws emr describe-step --cluster-id $(cat .emr_cluster_id) --step-id <step-id>
```

### Issue: "Command not found: bash"

**Windows users:** Install Git Bash or use Windows Subsystem for Linux (WSL).

### Issue: "Python command not found on EMR"

**Solution:** The submit script auto-detects `python` vs `python3`. If issues persist, manually specify in the script.

## File Format Notes

MapReduce output uses tab-separated values (TSV). The download script automatically:
- Converts UTF-16 LE to UTF-8
- Removes quotes
- Fixes escaped tab characters (`\t` to actual tabs)

## Cost Management

**EMR Cluster Costs:**
- m5.xlarge: ~$0.50/hour per instance
- 3 instances = ~$1.50/hour total
- Always terminate when not in use

**S3 Storage:**
- Data stored: <1MB
- Cost: <$0.01/month
- Clean up bucket when project complete

**Best Practices:**
1. Terminate cluster immediately after downloading results
2. Use spot instances for cost savings (optional)
3. Set up billing alerts in AWS Console

## Architecture

```
Local Machine
    |
    | (AWS CLI)
    v
AWS S3 (weatheria-climate-data)
    |
    | (Data input)
    v
AWS EMR Cluster (3 nodes)
    |
    | (MapReduce processing)
    v
AWS S3 (results output)
    |
    | (Download)
    v
Local Machine (FastAPI serves results)
```

## Advanced Configuration

### Custom Cluster Settings

Edit `scripts/aws/create_emr_cluster.sh`:

```bash
# Change instance type
--instance-type m5.2xlarge

# Change instance count
--instance-count 5

# Add spot instances
--use-spot-instances

# Change EMR version
--release-label emr-6.10.0
```

### Custom Job Configuration

Edit `scripts/aws/submit_emr_jobs_mrjob.sh`:

```bash
# Change number of reducers
--num-reducers 5

# Add job timeout
--max-hours-idle 1

# Custom output format
--output-format csv
```

## Security Notes

- Never commit AWS credentials to Git
- Use IAM roles instead of access keys when possible
- Rotate credentials regularly (required for Academic accounts)
- Restrict S3 bucket permissions to your account only

## References

- AWS EMR Documentation: https://docs.aws.amazon.com/emr/
- MRJob Documentation: https://mrjob.readthedocs.io/
- AWS CLI Reference: https://docs.aws.amazon.com/cli/
- Open-Meteo API: https://open-meteo.com/
