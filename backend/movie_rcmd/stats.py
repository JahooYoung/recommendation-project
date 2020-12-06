import json
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

MONGODB_URI = 'mongodb://node1:27017,node2:27017,node3:27017,node4:27017/rcmd_db?replicaSet=mongorepl'
ZK_QUORUM = 'node2:2181,node3:2181,node4:2181'

def stats(rdd, spark):
    sc = spark.sparkContext

    print(rdd.collect())
    rdd = rdd.map(lambda obj: json.loads(obj)['is_rcmd'])
    print('after json.loads  ====>  ', rdd.collect())
    rcmd_click_num = rdd.filter(lambda x: x).count()
    ts = datetime.now().timestamp()
    result_rdd = sc.parallelize([(ts, rcmd_click_num)])
    result = spark.createDataFrame(result_rdd, ['timestamp', 'rcmd_click_num'])
    result.write.format('mongo').mode('append') \
        .option('collection', 'movie_rcmd_rcmdstat') \
        .save()

def main():
    spark = SparkSession.builder \
        .master('yarn') \
        .appName('Movie Click Stats') \
        .config('spark.mongodb.input.uri', MONGODB_URI) \
        .config('spark.mongodb.output.uri', MONGODB_URI) \
        .config('spark.yarn.archive', 'hdfs:///home/spark_jars.zip') \
        .getOrCreate()
    # spark = SparkSession.builder\
    #     .appName('Movie Click Stats') \
    #     .config('spark.mongodb.input.uri', MONGODB_URI) \
    #     .config('spark.mongodb.output.uri', MONGODB_URI) \
    #     .getOrCreate()
    sc = spark.sparkContext
    ssc = StreamingContext(sc, 60)
    KafkaUtils.createStream(ssc, ZK_QUORUM, 'exlink_group_1', {'exlink': 1}) \
        .map(lambda x: x[1]) \
        .window(300, 60) \
        .foreachRDD(lambda rdd: stats(rdd, spark))

    ssc.start()
    ssc.awaitTermination()

if __name__ == '__main__':
    main()
