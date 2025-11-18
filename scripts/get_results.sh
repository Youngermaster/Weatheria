#!/bin/bash
# Retrieve MapReduce results from HDFS
# Usage: ./scripts/get_results.sh

set -e

echo "============================================================"
echo "Weatheria Climate Observatory - Results Retriever"
echo "============================================================"

# Create output directory
mkdir -p output

# Check if running in Docker
if [ -f "/.dockerenv" ]; then
    HDFS_CMD="hdfs dfs"
else
    HDFS_CMD="docker exec weatheria-hadoop hdfs dfs"
fi

echo ""
echo "📥 Retrieving results from HDFS..."

# Function to get results
get_result() {
    local hdfs_path=$1
    local local_file=$2
    local job_name=$3
    
    echo ""
    echo "   $job_name"
    
    # Check if output exists
    if $HDFS_CMD -test -e $hdfs_path 2>/dev/null; then
        # Get the results
        if [ -f "/.dockerenv" ]; then
            $HDFS_CMD -cat $hdfs_path/part-* > $local_file 2>/dev/null || \
            $HDFS_CMD -cat $hdfs_path > $local_file 2>/dev/null
        else
            docker exec weatheria-hadoop hdfs dfs -cat $hdfs_path/part-* > $local_file 2>/dev/null || \
            docker exec weatheria-hadoop hdfs dfs -cat $hdfs_path > $local_file 2>/dev/null
        fi
        
        echo "   ✓ Saved to: $local_file"
        
        # Show sample
        echo "   📋 Sample (first 5 lines):"
        head -n 5 $local_file | sed 's/^/      /'
    else
        echo "   ⚠️  No results found at: $hdfs_path"
    fi
}

# Get all results
get_result \
    "/user/hadoop/weatheria/output/word_count" \
    "output/word_count_results.csv" \
    "Word Count Results"

get_result \
    "/user/hadoop/weatheria/output/monthly_avg" \
    "output/monthly_avg_results.csv" \
    "Monthly Average Temperature"

get_result \
    "/user/hadoop/weatheria/output/extreme_temps" \
    "output/extreme_temps_results.csv" \
    "Extreme Temperature Detection"

get_result \
    "/user/hadoop/weatheria/output/temp_precip" \
    "output/temp_precip_results.csv" \
    "Temperature-Precipitation Correlation"

echo ""
echo "============================================================"
echo "✅ Results retrieved successfully!"
echo "============================================================"
echo ""
echo "📂 Results location: ./output/"
echo ""
echo "Next steps:"
echo "  1. View results: cat output/*.csv"
echo "  2. Start API: ./scripts/start_api.sh"
echo "  3. Access API docs: http://localhost:8000/docs"
