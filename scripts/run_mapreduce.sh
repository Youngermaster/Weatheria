#!/bin/bash
# Run MapReduce jobs
# Usage: ./scripts/run_mapreduce.sh [job_name]

set -e

echo "============================================================"
echo "Weatheria Climate Observatory - MapReduce Job Runner"
echo "============================================================"

JOB_NAME=${1:-"all"}

# Check if running in Docker
if [ -f "/.dockerenv" ]; then
    echo "✓ Running inside Docker container"
    EXEC_CMD=""
else
    echo "✓ Running locally via Docker"
    EXEC_CMD="docker exec weatheria-hadoop"
fi

# Function to run a MapReduce job
run_job() {
    local job_file=$1
    local input_path=$2
    local output_path=$3
    local job_desc=$4
    
    echo ""
    echo "🔄 Running: $job_desc"
    echo "   Script: $job_file"
    echo "   Input: $input_path"
    echo "   Output: $output_path"
    echo ""
    
    # Remove output directory if exists
    $EXEC_CMD hdfs dfs -rm -r -f $output_path 2>/dev/null || true
    
    # Run the job
    if [ -f "/.dockerenv" ]; then
        python3 /weatheria/scripts/$(basename $job_file) \
            -r hadoop \
            hdfs://$input_path \
            --output-dir hdfs://$output_path
    else
        docker exec weatheria-hadoop python3 /weatheria/scripts/$(basename $job_file) \
            -r hadoop \
            hdfs://$input_path \
            --output-dir hdfs://$output_path
    fi
    
    echo "   ✓ Job completed successfully!"
}

# Run specific job or all jobs
case $JOB_NAME in
    "word-count"|"wordcount"|"1")
        run_job \
            "src/mapreduce/word_count.py" \
            "/user/hadoop/weatheria/input/sample_text.txt" \
            "/user/hadoop/weatheria/output/word_count" \
            "Word Count Example"
        ;;
        
    "monthly"|"monthly-avg"|"2")
        run_job \
            "src/mapreduce/monthly_avg_temp.py" \
            "/user/hadoop/weatheria/input/test_weather_data.csv" \
            "/user/hadoop/weatheria/output/monthly_avg" \
            "Monthly Average Temperature"
        ;;
        
    "extreme"|"extreme-temps"|"3")
        run_job \
            "src/mapreduce/extreme_temps.py" \
            "/user/hadoop/weatheria/input/test_weather_data.csv" \
            "/user/hadoop/weatheria/output/extreme_temps" \
            "Extreme Temperature Detection"
        ;;
        
    "correlation"|"temp-precip"|"4")
        run_job \
            "src/mapreduce/temp_precipitation.py" \
            "/user/hadoop/weatheria/input/test_weather_data.csv" \
            "/user/hadoop/weatheria/output/temp_precip" \
            "Temperature-Precipitation Correlation"
        ;;
        
    "all")
        echo ""
        echo "Running all MapReduce jobs..."
        
        run_job \
            "src/mapreduce/word_count.py" \
            "/user/hadoop/weatheria/input/sample_text.txt" \
            "/user/hadoop/weatheria/output/word_count" \
            "Word Count Example"
            
        run_job \
            "src/mapreduce/monthly_avg_temp.py" \
            "/user/hadoop/weatheria/input/test_weather_data.csv" \
            "/user/hadoop/weatheria/output/monthly_avg" \
            "Monthly Average Temperature"
            
        run_job \
            "src/mapreduce/extreme_temps.py" \
            "/user/hadoop/weatheria/input/test_weather_data.csv" \
            "/user/hadoop/weatheria/output/extreme_temps" \
            "Extreme Temperature Detection"
            
        run_job \
            "src/mapreduce/temp_precipitation.py" \
            "/user/hadoop/weatheria/input/test_weather_data.csv" \
            "/user/hadoop/weatheria/output/temp_precip" \
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
        echo "  all                  - Run all jobs (default)"
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "✅ MapReduce jobs completed!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Retrieve results: ./scripts/get_results.sh"
echo "  2. Start API: ./scripts/start_api.sh"
echo "  3. View Hadoop UI: http://localhost:8088"
