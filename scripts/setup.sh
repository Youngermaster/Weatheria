#!/bin/bash
# Setup and start the entire Weatheria project
# Usage: ./scripts/setup.sh

set -e

echo "============================================================"
echo "Weatheria Climate Observatory - Complete Setup"
echo "============================================================"
echo ""
echo "This script will:"
echo "  1. Install Python dependencies"
echo "  2. Download weather data"
echo "  3. Start Docker containers"
echo "  4. Load data to HDFS"
echo "  5. Run MapReduce jobs"
echo "  6. Retrieve results"
echo "  7. Start API server"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Step 1: Install dependencies
echo ""
echo "============================================================"
echo "Step 1/7: Installing Python dependencies"
echo "============================================================"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Step 2: Download data
echo ""
echo "============================================================"
echo "Step 2/7: Downloading weather data"
echo "============================================================"

if [ ! -f "data/raw/medellin_weather_2022-2024.csv" ]; then
    python3 scripts/download_data.py
else
    echo "✓ Data already exists: data/raw/medellin_weather_2022-2024.csv"
fi

# Step 3: Start Docker
echo ""
echo "============================================================"
echo "Step 3/7: Starting Docker containers"
echo "============================================================"

docker-compose up -d
echo "Waiting for Hadoop to initialize (30 seconds)..."
sleep 30
echo "✓ Containers started"

# Step 4: Load to HDFS
echo ""
echo "============================================================"
echo "Step 4/7: Loading data to HDFS"
echo "============================================================"

./scripts/load_to_hdfs.sh data/raw/test_weather_data.csv

# Step 5: Run MapReduce
echo ""
echo "============================================================"
echo "Step 5/7: Running MapReduce jobs"
echo "============================================================"

./scripts/run_mapreduce.sh all

# Step 6: Get results
echo ""
echo "============================================================"
echo "Step 6/7: Retrieving results"
echo "============================================================"

./scripts/get_results.sh

# Step 7: Information
echo ""
echo "============================================================"
echo "Step 7/7: Setup Complete!"
echo "============================================================"
echo ""
echo "✅ Weatheria Climate Observatory is ready!"
echo ""
echo "🌐 Access points:"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Hadoop UI: http://localhost:8088"
echo "  - HDFS UI: http://localhost:50070"
echo ""
echo "📂 Results location: ./output/"
echo ""
echo "🚀 To start the API server:"
echo "   ./scripts/start_api.sh"
echo ""
echo "🛑 To stop all services:"
echo "   docker-compose down"
echo ""
echo "📖 For more information, see README.md"
