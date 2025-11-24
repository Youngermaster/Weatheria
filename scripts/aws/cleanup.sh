#!/bin/bash
# Clean up all AWS resources
# Usage: ./scripts/aws/cleanup.sh

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

BUCKET_NAME=${S3_BUCKET:-"weatheria-climate-data"}

echo "============================================================"
echo "Weatheria Climate Observatory - AWS Cleanup"
echo "============================================================"
echo ""
echo "WARNING: This will delete all AWS resources!"
echo ""
echo "This includes:"
echo "  - EMR cluster (if running)"
echo "  - S3 bucket: $BUCKET_NAME"
echo "  - All data and results"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 1
fi

# Terminate EMR cluster if exists
if [ -f .emr_cluster_id ]; then
    echo ""
    echo "Terminating EMR cluster..."
    CLUSTER_ID=$(cat .emr_cluster_id)
    aws emr terminate-clusters --cluster-ids "$CLUSTER_ID" 2>/dev/null || true
    rm -f .emr_cluster_id
    echo "Cluster terminated"
fi

# Empty and delete S3 bucket
echo ""
echo "Deleting S3 bucket..."
if aws s3 ls "s3://$BUCKET_NAME" &> /dev/null; then
    # Empty bucket first
    aws s3 rm "s3://$BUCKET_NAME" --recursive
    # Delete bucket
    aws s3 rb "s3://$BUCKET_NAME"
    echo "Bucket deleted"
else
    echo "Bucket doesn't exist"
fi

echo ""
echo "============================================================"
echo "SUCCESS: AWS cleanup complete!"
echo "============================================================"
