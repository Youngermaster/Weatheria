#!/bin/bash
# Submit MapReduce jobs to EMR cluster
# Usage: ./scripts/aws/submit_emr_jobs.sh [job_name]

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Get cluster ID
if [ -f .emr_cluster_id ]; then
    CLUSTER_ID=$(cat .emr_cluster_id)
else
    echo "❌ No cluster ID found. Create cluster first:"
    echo "   ./scripts/aws/create_emr_cluster.sh"
    exit 1
fi

BUCKET_NAME=${S3_BUCKET:-"weatheria-climate-data"}
JOB_NAME=${1:-"all"}

echo "============================================================"
echo "Weatheria Climate Observatory - EMR Job Submission"
echo "============================================================"
echo ""
echo "Cluster ID: $CLUSTER_ID"
echo "S3 Bucket: s3://$BUCKET_NAME"
echo ""

# Check cluster status
CLUSTER_STATE=$(aws emr describe-cluster --cluster-id "$CLUSTER_ID" \
    --query 'Cluster.Status.State' --output text)

if [ "$CLUSTER_STATE" != "RUNNING" ] && [ "$CLUSTER_STATE" != "WAITING" ]; then
    echo "❌ Cluster is not running. Current state: $CLUSTER_STATE"
    exit 1
fi

echo "✓ Cluster is ready"
echo ""

# Function to submit a job
submit_job() {
    local job_name=$1
    local script_file=$2
    local input_path=$3
    local output_path=$4
    local description=$5
    
    echo "📤 Submitting: $description"
    
    STEP_ID=$(aws emr add-steps \
        --cluster-id "$CLUSTER_ID" \
        --steps Type=STREAMING,Name="$job_name",\
ActionOnFailure=CONTINUE,\
Args=[-files,"s3://$BUCKET_NAME/scripts/$script_file",\
-mapper,"$script_file",\
-reducer,"$script_file",\
-input,"s3://$BUCKET_NAME/$input_path",\
-output,"s3://$BUCKET_NAME/$output_path"] \
        --query 'StepIds[0]' \
        --output text)
    
    echo "   ✓ Step submitted: $STEP_ID"
    echo "   Job: $job_name"
    echo ""
}

# Submit jobs
case $JOB_NAME in
    "word-count"|"wordcount"|"1")
        submit_job \
            "word-count" \
            "word_count.py" \
            "input/sample_text.txt" \
            "output/word_count" \
            "Word Count Example"
        ;;
        
    "monthly"|"monthly-avg"|"2")
        submit_job \
            "monthly-avg" \
            "monthly_avg_temp.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/monthly_avg" \
            "Monthly Average Temperature"
        ;;
        
    "extreme"|"extreme-temps"|"3")
        submit_job \
            "extreme-temps" \
            "extreme_temps.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/extreme_temps" \
            "Extreme Temperature Detection"
        ;;
        
    "correlation"|"temp-precip"|"4")
        submit_job \
            "temp-precipitation" \
            "temp_precipitation.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/temp_precip" \
            "Temperature-Precipitation Correlation"
        ;;
        
    "all")
        echo "Submitting all jobs..."
        echo ""
        
        submit_job \
            "word-count" \
            "word_count.py" \
            "input/sample_text.txt" \
            "output/word_count" \
            "Word Count Example"
            
        submit_job \
            "monthly-avg" \
            "monthly_avg_temp.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/monthly_avg" \
            "Monthly Average Temperature"
            
        submit_job \
            "extreme-temps" \
            "extreme_temps.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/extreme_temps" \
            "Extreme Temperature Detection"
            
        submit_job \
            "temp-precipitation" \
            "temp_precipitation.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/temp_precip" \
            "Temperature-Precipitation Correlation"
        ;;
        
    *)
        echo "❌ Unknown job: $JOB_NAME"
        echo ""
        echo "Available jobs:"
        echo "  1, word-count        - Word count example"
        echo "  2, monthly           - Monthly average temperature"
        echo "  3, extreme           - Extreme temperature detection"
        echo "  4, correlation       - Temperature-precipitation correlation"
        echo "  all                  - Submit all jobs (default)"
        exit 1
        ;;
esac

echo "============================================================"
echo "✅ Jobs submitted!"
echo "============================================================"
echo ""
echo "Monitor jobs:"
echo "  aws emr list-steps --cluster-id $CLUSTER_ID"
echo ""
echo "Check specific step:"
echo "  aws emr describe-step --cluster-id $CLUSTER_ID --step-id <STEP_ID>"
echo ""
echo "Next steps:"
echo "  1. Wait for jobs to complete (5-15 minutes)"
echo "  2. Download results: ./scripts/aws/download_results.sh"
