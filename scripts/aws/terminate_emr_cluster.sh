#!/bin/bash
# Terminate EMR cluster
# Usage: ./scripts/aws/terminate_emr_cluster.sh

set -e

# Get cluster ID
if [ -f .emr_cluster_id ]; then
    CLUSTER_ID=$(cat .emr_cluster_id)
else
    echo "ERROR: No cluster ID found"
    exit 1
fi

echo "============================================================"
echo "Weatheria Climate Observatory - Terminate EMR Cluster"
echo "============================================================"
echo ""
echo "Cluster ID: $CLUSTER_ID"
echo ""

# Get cluster info
CLUSTER_INFO=$(aws emr describe-cluster --cluster-id "$CLUSTER_ID" \
    --query 'Cluster.[Name,Status.State]' --output text)

echo "Cluster: $CLUSTER_INFO"
echo ""

# Confirm termination
read -p "WARNING: Terminate this cluster? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 1
fi

# Terminate cluster
echo ""
echo "Terminating cluster..."
aws emr terminate-clusters --cluster-ids "$CLUSTER_ID"

echo "Termination initiated"
echo ""
echo "Cluster will shut down in a few minutes."
echo ""

# Remove cluster ID file
rm -f .emr_cluster_id

echo "============================================================"
echo "SUCCESS: Cluster termination in progress"
echo "============================================================"
echo ""
echo "Monitor status:"
echo "  aws emr describe-cluster --cluster-id $CLUSTER_ID"
