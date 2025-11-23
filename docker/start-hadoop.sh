#!/bin/bash
set -e

# Set environment variables
export HADOOP_HOME=/opt/hadoop
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

echo "Starting HDFS and YARN services..."

# Start HDFS
$HADOOP_HOME/sbin/start-dfs.sh

# Wait for HDFS
sleep 15

# Start YARN
$HADOOP_HOME/sbin/start-yarn.sh

# Wait for YARN
sleep 10

# Create directories
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hadoop/weatheria/input
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hadoop/weatheria/output

echo "✓ Hadoop services started!"
echo ""
$HADOOP_HOME/bin/hdfs dfs -ls /
