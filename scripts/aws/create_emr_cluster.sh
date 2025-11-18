#!/bin/bash
# Create AWS EMR Cluster
# Usage: ./scripts/aws/create_emr_cluster.sh

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Configuration
CLUSTER_NAME="weatheria-climate-observatory"
BUCKET_NAME=${S3_BUCKET:-"weatheria-climate-data"}
REGION=${AWS_REGION:-"us-east-1"}
KEY_PAIR=${EMR_KEY_PAIR:-"my-key-pair"}
INSTANCE_TYPE="m5.xlarge"
INSTANCE_COUNT=3

echo "============================================================"
echo "Weatheria Climate Observatory - EMR Cluster Creation"
echo "============================================================"
echo ""
echo "Cluster Name: $CLUSTER_NAME"
echo "Region: $REGION"
echo "Instance Type: $INSTANCE_TYPE"
echo "Instance Count: $INSTANCE_COUNT"
echo "Key Pair: $KEY_PAIR"
echo ""

# Confirm
read -p "Create cluster? This will incur AWS charges. (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Check if S3 bucket exists
if ! aws s3 ls "s3://$BUCKET_NAME" &> /dev/null; then
    echo "❌ S3 bucket not found: $BUCKET_NAME"
    echo "   Run: ./scripts/aws/setup_s3.sh"
    exit 1
fi

# Create cluster
echo ""
echo "Creating EMR cluster..."
echo "This may take 10-15 minutes..."
echo ""

CLUSTER_ID=$(aws emr create-cluster \
    --name "$CLUSTER_NAME" \
    --release-label emr-6.10.0 \
    --applications Name=Hadoop Name=Hive Name=Spark \
    --ec2-attributes KeyName="$KEY_PAIR" \
    --instance-type "$INSTANCE_TYPE" \
    --instance-count $INSTANCE_COUNT \
    --use-default-roles \
    --log-uri "s3://$BUCKET_NAME/logs/" \
    --region "$REGION" \
    --query 'ClusterId' \
    --output text)

echo "✓ Cluster created!"
echo ""
echo "Cluster ID: $CLUSTER_ID"

# Save cluster ID
echo "$CLUSTER_ID" > .emr_cluster_id
echo "✓ Cluster ID saved to .emr_cluster_id"

# Wait for cluster to be ready
echo ""
echo "Waiting for cluster to start..."
aws emr wait cluster-running --cluster-id "$CLUSTER_ID"

# Get cluster details
echo ""
echo "Cluster details:"
aws emr describe-cluster --cluster-id "$CLUSTER_ID" \
    --query 'Cluster.[Id,Name,Status.State,MasterPublicDnsName]' \
    --output table

echo ""
echo "============================================================"
echo "✅ EMR cluster is running!"
echo "============================================================"
echo ""
echo "Cluster ID: $CLUSTER_ID"
echo ""
echo "Monitor cluster:"
echo "  aws emr describe-cluster --cluster-id $CLUSTER_ID"
echo ""
echo "Next steps:"
echo "  1. Submit jobs: ./scripts/aws/submit_emr_jobs.sh"
echo "  2. Monitor jobs: aws emr list-steps --cluster-id $CLUSTER_ID"
echo "  3. When done, terminate: ./scripts/aws/terminate_emr_cluster.sh"
echo ""
echo "⚠️  IMPORTANT: Remember to terminate the cluster to avoid charges!"
