#!/bin/bash
# AWS S3 Setup Script
# Usage: ./scripts/aws/setup_s3.sh

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Configuration
BUCKET_NAME=${S3_BUCKET:-"weatheria-climate-data"}
REGION=${AWS_REGION:-"us-east-1"}

echo "============================================================"
echo "Weatheria Climate Observatory - S3 Setup"
echo "============================================================"
echo ""
echo "Bucket: $BUCKET_NAME"
echo "Region: $REGION"
echo ""

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   brew install awscli  # macOS"
    echo "   pip install awscli   # Python"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured"
    echo ""
    echo "Configure AWS credentials:"
    echo "   aws configure"
    exit 1
fi

echo "✓ AWS CLI configured"
echo ""

# Create S3 bucket
echo "Creating S3 bucket..."
if aws s3 ls "s3://$BUCKET_NAME" 2>&1 | grep -q 'NoSuchBucket'; then
    aws s3 mb "s3://$BUCKET_NAME" --region "$REGION"
    echo "✓ Bucket created: s3://$BUCKET_NAME"
else
    echo "✓ Bucket already exists: s3://$BUCKET_NAME"
fi

# Create folder structure
echo ""
echo "Creating folder structure..."
aws s3api put-object --bucket "$BUCKET_NAME" --key input/
aws s3api put-object --bucket "$BUCKET_NAME" --key output/
aws s3api put-object --bucket "$BUCKET_NAME" --key scripts/
aws s3api put-object --bucket "$BUCKET_NAME" --key logs/
echo "✓ Folders created"

# Upload data
echo ""
echo "Uploading data files..."
if [ -f "data/raw/medellin_weather_2022-2024.csv" ]; then
    aws s3 cp data/raw/medellin_weather_2022-2024.csv \
        "s3://$BUCKET_NAME/input/medellin_weather_2022-2024.csv"
    echo "✓ Weather data uploaded"
else
    echo "⚠️  Weather data not found. Run: python3 scripts/download_data.py"
fi

if [ -f "data/raw/sample_text.txt" ]; then
    aws s3 cp data/raw/sample_text.txt \
        "s3://$BUCKET_NAME/input/sample_text.txt"
    echo "✓ Sample text uploaded"
fi

# Upload MapReduce scripts
echo ""
echo "Uploading MapReduce scripts..."
aws s3 sync src/mapreduce/ "s3://$BUCKET_NAME/scripts/" \
    --exclude "*.pyc" \
    --exclude "__pycache__/*"
echo "✓ Scripts uploaded"

# List bucket contents
echo ""
echo "S3 bucket contents:"
aws s3 ls "s3://$BUCKET_NAME/" --recursive --human-readable

echo ""
echo "============================================================"
echo "✅ S3 setup complete!"
echo "============================================================"
echo ""
echo "Bucket URL: s3://$BUCKET_NAME"
echo ""
echo "Next steps:"
echo "  1. Create EMR cluster: ./scripts/aws/create_emr_cluster.sh"
echo "  2. Submit jobs: ./scripts/aws/submit_emr_jobs.sh"
