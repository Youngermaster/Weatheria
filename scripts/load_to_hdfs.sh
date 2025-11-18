#!/bin/bash
# Load data to HDFS
# Usage: ./scripts/load_to_hdfs.sh [data_file]

set -e

echo "============================================================"
echo "Weatheria Climate Observatory - HDFS Data Loader"
echo "============================================================"

# Default data file
DATA_FILE=${1:-"data/raw/test_weather_data.csv"}
TEXT_FILE="data/raw/sample_text.txt"

# Check if running in Docker
if [ -f "/.dockerenv" ]; then
    echo "✓ Running inside Docker container"
    HDFS_CMD="hdfs dfs"
else
    echo "✓ Running locally (use Docker for full Hadoop setup)"
    echo "⚠️  Starting Hadoop container..."
    docker-compose up -d hadoop
    sleep 5
    HDFS_CMD="docker exec weatheria-hadoop hdfs dfs"
fi

echo ""
echo "📂 Creating HDFS directories..."
$HDFS_CMD -mkdir -p /user/hadoop/weatheria/input
$HDFS_CMD -mkdir -p /user/hadoop/weatheria/output

echo ""
echo "📤 Uploading data files to HDFS..."

# Upload weather data
if [ -f "$DATA_FILE" ]; then
    echo "   Uploading: $DATA_FILE"
    if [ -f "/.dockerenv" ]; then
        $HDFS_CMD -put -f "$DATA_FILE" /user/hadoop/weatheria/input/
    else
        docker cp "$DATA_FILE" weatheria-hadoop:/tmp/weather_data.csv
        docker exec weatheria-hadoop hdfs dfs -put -f /tmp/weather_data.csv /user/hadoop/weatheria/input/
    fi
    echo "   ✓ Weather data uploaded"
else
    echo "   ⚠️  File not found: $DATA_FILE"
fi

# Upload text file for word count
if [ -f "$TEXT_FILE" ]; then
    echo "   Uploading: $TEXT_FILE"
    if [ -f "/.dockerenv" ]; then
        $HDFS_CMD -put -f "$TEXT_FILE" /user/hadoop/weatheria/input/
    else
        docker cp "$TEXT_FILE" weatheria-hadoop:/tmp/sample_text.txt
        docker exec weatheria-hadoop hdfs dfs -put -f /tmp/sample_text.txt /user/hadoop/weatheria/input/
    fi
    echo "   ✓ Text file uploaded"
fi

echo ""
echo "📋 HDFS directory listing:"
$HDFS_CMD -ls /user/hadoop/weatheria/input

echo ""
echo "👀 Sample data (first 10 lines):"
$HDFS_CMD -cat /user/hadoop/weatheria/input/$(basename $DATA_FILE) | head -n 10

echo ""
echo "============================================================"
echo "✅ Data successfully loaded to HDFS!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Run MapReduce jobs: ./scripts/run_mapreduce.sh"
echo "  2. Retrieve results: ./scripts/get_results.sh"
