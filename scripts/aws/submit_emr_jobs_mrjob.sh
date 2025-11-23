#!/bin/bash
# Submit MapReduce jobs to EMR using MRJob directly
# Usage: ./scripts/aws/submit_emr_jobs_mrjob.sh [job_name]

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
JOB_NAME=${1:-"monthly"}

echo "============================================================"
echo "Weatheria Climate Observatory - MRJob EMR Submission"
echo "============================================================"
echo ""
echo "Cluster ID: $CLUSTER_ID"
echo "S3 Bucket: s3://$BUCKET_NAME"
echo ""

# Detect Python command (Windows uses 'python', Linux/Mac use 'python3')
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ Python not found!"
    exit 1
fi

# Check if mrjob is installed locally
if ! $PYTHON_CMD -c "import mrjob" 2>/dev/null; then
    echo "⚠️  Installing mrjob locally..."
    $PIP_CMD install mrjob boto3
fi

# Function to run MRJob on EMR
run_mrjob() {
    local script_file=$1
    local input_path=$2
    local output_path=$3
    local description=$4
    
    echo "🚀 Running: $description"
    echo "   Script: $script_file"
    echo "   Input: s3://$BUCKET_NAME/$input_path"
    echo "   Output: s3://$BUCKET_NAME/$output_path"
    echo ""
    
    # Clean up previous output if exists
    echo "   Cleaning previous output..."
    aws s3 rm "s3://$BUCKET_NAME/$output_path/" --recursive 2>/dev/null || true
    
    # Run MRJob with EMR runner with explicit configuration
    $PYTHON_CMD "$script_file" \
        -r emr \
        --cluster-id="$CLUSTER_ID" \
        --region=us-east-1 \
        --no-output \
        --output-dir="s3://$BUCKET_NAME/$output_path" \
        "s3://$BUCKET_NAME/$input_path"
    
    echo ""
    echo "   ✓ Job completed!"
    echo ""
}

# Select and run job
case $JOB_NAME in
    "monthly"|"monthly-avg"|"2")
        run_mrjob \
            "src/mapreduce/monthly_avg_temp.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/monthly_avg" \
            "Monthly Average Temperature"
        ;;
        
    "extreme"|"extreme-temps"|"3")
        run_mrjob \
            "src/mapreduce/extreme_temps.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/extreme_temps" \
            "Extreme Temperature Detection"
        ;;
        
    "correlation"|"temp-precip"|"4")
        run_mrjob \
            "src/mapreduce/temp_precipitation.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/temp_precip" \
            "Temperature-Precipitation Correlation"
        ;;
        
    "all")
        echo "Running all jobs..."
        echo ""
        
        run_mrjob \
            "src/mapreduce/monthly_avg_temp.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/monthly_avg" \
            "Monthly Average Temperature"
            
        run_mrjob \
            "src/mapreduce/extreme_temps.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/extreme_temps" \
            "Extreme Temperature Detection"
            
        run_mrjob \
            "src/mapreduce/temp_precipitation.py" \
            "input/medellin_weather_2022-2024.csv" \
            "output/temp_precip" \
            "Temperature-Precipitation Correlation"
        ;;
        
    *)
        echo "❌ Unknown job: $JOB_NAME"
        echo ""
        echo "Available jobs:"
        echo "  monthly          - Monthly average temperature"
        echo "  extreme          - Extreme temperature detection"
        echo "  correlation      - Temperature-precipitation correlation"
        echo "  all              - Run all jobs"
        exit 1
        ;;
esac

echo "============================================================"
echo "✅ Jobs completed successfully!"
echo "============================================================"
echo ""
echo "Download results:"
echo "  ./scripts/aws/download_results.sh"
