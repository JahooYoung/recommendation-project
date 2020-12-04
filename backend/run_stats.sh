#!/bin/bash
cd `dirname $0`

export HADOOP_HOME=/usr/local/hadoop-3.2.1
export JAVA_HOME=/usr/local/jdk1.8.0_271
export CLASSPATH=.:/usr/local/jdk1.8.0_271/lib:/usr/local/jdk1.8.0_271/jre/lib
export HADOOP_CONF_DIR=/usr/local/hadoop-3.2.1/etc/hadoop
export SPARK_HOME=/usr/local/spark-2.4.7-bin-hadoop2.7
export PROJECT_ROOT=/root/rcmd_project
export JRE_HOME=/usr/local/jdk1.8.0_271/jre

source ../venv/bin/activate

python movie_rcmd/stats.py
