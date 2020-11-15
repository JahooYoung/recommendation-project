#!/bin/bash

if [[ $NODE_ID != "1" ]]; then
    echo "==== start zookeeper ===="
    echo `expr $NODE_ID - 1` > $ZOOKEEPER_HOME/data/myid
    zkServer.sh start
fi
