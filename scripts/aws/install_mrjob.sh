#!/bin/bash
# Install MRJob on EMR cluster
# Usage: ./scripts/aws/install_mrjob.sh

set -e

# Get cluster ID
if [ -f .emr_cluster_id ]; then
    CLUSTER_ID=$(cat .emr_cluster_id)
else
    echo "❌ No cluster ID found."
    exit 1
fi

echo "============================================================"
echo "Installing MRJob on EMR Cluster"
echo "============================================================"
echo ""
echo "Cluster ID: $CLUSTER_ID"
echo ""

# Submit installation step
STEP_ID=$(aws emr add-steps \
    --cluster-id "$CLUSTER_ID" \
    --steps Type=CUSTOM_JAR,Name="Install-MRJob",\
ActionOnFailure=CONTINUE,\
Jar=command-runner.jar,\
Args=[sudo,pip3,install,mrjob] \
    --query 'StepIds[0]' \
    --output text)

echo "✓ Installation step submitted: $STEP_ID"
echo ""
echo "Wait for installation to complete:"
echo "  aws emr describe-step --cluster-id $CLUSTER_ID --step-id $STEP_ID"
echo ""
echo "Then submit your MapReduce jobs."
