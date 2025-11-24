#!/bin/bash
# Initialize and start Hadoop services
set -e

echo "============================================================"
echo "Initializing Hadoop Services"
echo "============================================================"

# Configure Hadoop environment
export HADOOP_HOME=/opt/hadoop
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Configure core-site.xml
cat <<EOF > $HADOOP_HOME/etc/hadoop/core-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/tmp/hadoop-root</value>
    </property>
</configuration>
EOF

# Configure hdfs-site.xml
cat <<EOF > $HADOOP_HOME/etc/hadoop/hdfs-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///tmp/hadoop-root/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///tmp/hadoop-root/dfs/data</value>
    </property>
    <property>
        <name>dfs.permissions.enabled</name>
        <value>false</value>
    </property>
</configuration>
EOF

# Configure mapred-site.xml
cat <<EOF > $HADOOP_HOME/etc/hadoop/mapred-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>\$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:\$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>
EOF

# Configure yarn-site.xml
cat <<EOF > $HADOOP_HOME/etc/hadoop/yarn-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
EOF

# Configure hadoop-env.sh
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Setup SSH for Hadoop
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa || true
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys || true
chmod 0600 ~/.ssh/authorized_keys || true
ssh-keyscan -H localhost >> ~/.ssh/known_hosts 2>/dev/null || true

# Format namenode (only if not already formatted)
if [ ! -d "/tmp/hadoop-root/dfs/name/current" ]; then
    echo "Formatting HDFS namenode..."
    $HADOOP_HOME/bin/hdfs namenode -format -force
fi

# Start HDFS
echo "Starting HDFS..."
$HADOOP_HOME/sbin/start-dfs.sh

# Wait for HDFS to be ready
sleep 10

# Start YARN
echo "Starting YARN..."
$HADOOP_HOME/sbin/start-yarn.sh

# Wait for services to be ready
sleep 10

echo "Hadoop services started successfully!"
echo ""
echo "Web UIs available at:"
echo "  - HDFS NameNode: http://localhost:50070"
echo "  - YARN ResourceManager: http://localhost:8088"
echo ""

# Create HDFS directories
echo "Creating HDFS directories..."
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hadoop/weatheria/input
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hadoop/weatheria/output
$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /user/hadoop/weatheria

echo "HDFS directories created!"
echo ""
$HADOOP_HOME/bin/hdfs dfs -ls /user/hadoop/weatheria/

echo ""
echo "============================================================"
echo "Hadoop initialization complete!"
echo "============================================================"
