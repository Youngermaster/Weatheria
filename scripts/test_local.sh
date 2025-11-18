#!/bin/bash
# Test MapReduce jobs locally without Hadoop
# Usage: ./scripts/test_local.sh [job_name]

set -e

echo "============================================================"
echo "Weatheria Climate Observatory - Local Test Runner"
echo "============================================================"

JOB_NAME=${1:-"all"}

# Function to run a job locally
run_local_job() {
    local job_file=$1
    local input_file=$2
    local output_file=$3
    local job_desc=$4
    
    echo ""
    echo "🧪 Testing: $job_desc"
    echo "   Script: $job_file"
    echo "   Input: $input_file"
    echo "   Output: $output_file"
    echo ""
    
    if [ ! -f "$input_file" ]; then
        echo "   ⚠️  Input file not found: $input_file"
        return
    fi
    
    # Run in local mode
    python3 $job_file $input_file > $output_file 2>/dev/null
    
    echo "   ✓ Job completed!"
    echo "   📋 Results (first 10 lines):"
    head -n 10 $output_file | sed 's/^/      /'
}

# Create output directory
mkdir -p output/local

# Run tests
case $JOB_NAME in
    "word-count"|"wordcount"|"1")
        run_local_job \
            "src/mapreduce/word_count.py" \
            "data/raw/sample_text.txt" \
            "output/local/word_count_local.csv" \
            "Word Count Example"
        ;;
        
    "monthly"|"monthly-avg"|"2")
        run_local_job \
            "src/mapreduce/monthly_avg_temp.py" \
            "data/raw/test_weather_data.csv" \
            "output/local/monthly_avg_local.csv" \
            "Monthly Average Temperature"
        ;;
        
    "extreme"|"extreme-temps"|"3")
        run_local_job \
            "src/mapreduce/extreme_temps.py" \
            "data/raw/test_weather_data.csv" \
            "output/local/extreme_temps_local.csv" \
            "Extreme Temperature Detection"
        ;;
        
    "correlation"|"temp-precip"|"4")
        run_local_job \
            "src/mapreduce/temp_precipitation.py" \
            "data/raw/test_weather_data.csv" \
            "output/local/temp_precip_local.csv" \
            "Temperature-Precipitation Correlation"
        ;;
        
    "all")
        echo ""
        echo "Testing all MapReduce jobs locally..."
        
        run_local_job \
            "src/mapreduce/word_count.py" \
            "data/raw/sample_text.txt" \
            "output/local/word_count_local.csv" \
            "Word Count Example"
            
        run_local_job \
            "src/mapreduce/monthly_avg_temp.py" \
            "data/raw/test_weather_data.csv" \
            "output/local/monthly_avg_local.csv" \
            "Monthly Average Temperature"
            
        run_local_job \
            "src/mapreduce/extreme_temps.py" \
            "data/raw/test_weather_data.csv" \
            "output/local/extreme_temps_local.csv" \
            "Extreme Temperature Detection"
            
        run_local_job \
            "src/mapreduce/temp_precipitation.py" \
            "data/raw/test_weather_data.csv" \
            "output/local/temp_precip_local.csv" \
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
        echo "  all                  - Test all jobs (default)"
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "✅ Local tests completed!"
echo "============================================================"
echo ""
echo "📂 Results location: ./output/local/"
