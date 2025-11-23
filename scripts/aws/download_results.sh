#!/bin/bash
# Download results from S3
# Usage: ./scripts/aws/download_results.sh

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

BUCKET_NAME=${S3_BUCKET:-"weatheria-climate-data"}

echo "============================================================"
echo "Weatheria Climate Observatory - Download Results from S3"
echo "============================================================"
echo ""
echo "S3 Bucket: s3://$BUCKET_NAME"
echo ""

# Create output directory
mkdir -p output

# Function to download results
download_result() {
    local s3_path=$1
    local local_file=$2
    local job_name=$3
    
    echo "📥 Downloading: $job_name"
    
    # Download all part files and combine
    aws s3 cp "s3://$BUCKET_NAME/$s3_path/" - \
        --recursive \
        --exclude "*" \
        --include "part-*" \
        > "$local_file" 2>/dev/null || true
    
    if [ -s "$local_file" ]; then
        echo "   ✓ Saved to: $local_file"
        echo "   📋 Sample (first 5 lines):"
        head -n 5 "$local_file" | sed 's/^/      /'
    else
        echo "   ⚠️  No results found"
    fi
    echo ""
}

# Download all results directly to output/ directory (for API compatibility)
download_result \
    "output/word_count" \
    "output/word_count_results.csv" \
    "Word Count Results"

download_result \
    "output/monthly_avg" \
    "output/monthly_avg_results.csv" \
    "Monthly Average Temperature"

download_result \
    "output/extreme_temps" \
    "output/extreme_temps_results.csv" \
    "Extreme Temperature Detection"

download_result \
    "output/temp_precip" \
    "output/temp_precip_results.csv" \
    "Temperature-Precipitation Correlation"

echo "============================================================"
echo "✅ Results downloaded!"
echo "============================================================"
echo ""
echo "📂 Results location: ./output/"
echo ""
echo "Files are ready for API consumption!"
