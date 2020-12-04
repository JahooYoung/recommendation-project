#!/bin/bash

if [[ $NODE_ID == "3" ]]; then
    echo "==== start hdfs ===="
    hdfs namenode -format
    scp -Br /data/hadoop/dfs/name node4:/data/hadoop/dfs
    hdfs zkfc -formatZK
    $HADOOP_HOME/sbin/start-dfs.sh
fi

if [[ $NODE_ID != "1" ]]; then
    echo "==== start hdfs journal node ===="
    hdfs --daemon start journalnode
fi

if [[ $NODE_ID != "4" ]]; then
    echo "==== start kafka ===="
    PROPS=$KAFKA_HOME/config/server.properties
    sed -ri "s/\{NODE_ID\}/$NODE_ID/" $PROPS
    kafka-server-start.sh -daemon $PROPS
    if [[ $NODE_ID == "2" ]]; then
        # node2 is the last node to start
        sleep 3
        kafka-topics.sh --bootstrap-server node1:9092,node2:9092,node3:9092 --create --replication-factor 3 --partitions 1 --topic exlink
    fi
fi

# if [[ $NODE_ID == "3" ]]; then
#     echo "==== start yarn ===="
#     $HADOOP_HOME/sbin/start-yarn.sh
# fi

mongod -f /data/mongodb/mongodb.conf
