#!/bin/bash

if [[ $NODE_ID == "3" ]]; then
    echo "==== start hdfs ===="
    hdfs namenode -format
    scp -Br /data/hadoop/dfs/name node4:/data/hadoop/dfs
    hdfs zkfc -formatZK
    $HADOOP_HOME/sbin/start-dfs.sh
fi

if [[ $NODE_ID != "1" ]]; then
    hdfs --daemon start journalnode
fi

# if [[ $NODE_ID == "3" ]]; then
#     echo "==== start yarn ===="
#     $HADOOP_HOME/sbin/start-yarn.sh
# fi

mongod -f /data/mongodb/mongodb.conf
